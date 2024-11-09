from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
import pytz
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

# Spotify API credentials
CLIENT_ID = '1c37db7966804c17ada79eff73b8b247'
CLIENT_SECRET = '90977a877a8f4ba08bc95fe2ef7585df'
REDIRECT_URI = 'http://localhost:8888/callback/'

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracks.db'
db = SQLAlchemy(app)

# Spotify API scope
SCOPE = 'user-read-recently-played'

# Spotify client with OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

# Track model for the database
class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_name = db.Column(db.String(200), nullable=False)
    artist_name = db.Column(db.String(200), nullable=False)
    played_at = db.Column(db.String(200), unique=True, nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

# Function to fetch and store new tracks
def fetch_recent_tracks():
    results = sp.current_user_recently_played(limit=10)

    for item in results['items']:
        track_name = item['track']['name']
        artist_name = item['track']['artists'][0]['name']
        played_at = item['played_at']

        # Check if track already exists in the database
        if not Track.query.filter_by(played_at=played_at).first():
            # Save new track to the database
            new_track = Track(track_name=track_name, artist_name=artist_name, played_at=played_at)
            db.session.add(new_track)
            db.session.commit()
            print(f"Saved new track: {track_name} by {artist_name} at {played_at}")

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_recent_tracks, 'interval', minutes=1)
scheduler.start()

@app.route('/recent-tracks', methods=['GET'])
def recent_tracks():
    fetch_recent_tracks()
    # Fetch all tracks from the database
    tracks = Track.query.order_by(Track.played_at.desc()).all()
    return jsonify([{'track_id': t.id, 'track_name': t.track_name, 'artist_name': t.artist_name, 'played_at': t.played_at} for t in tracks])

@app.route('/recent-count', methods=['GET'])
def recent_count():
    count = Track.query.count()
    return jsonify(count)

@app.route('/today-tracks', methods=['GET'])
def today_tracks():
    today = datetime.utcnow().date()
    tracks = Track.query.filter(func.date(Track.played_at) == today) \
                        .order_by(Track.played_at.desc()).all()
    return jsonify([{'track_name': t.track_name, 'artist_name': t.artist_name, 'played_at': t.played_at} for t in tracks])

@app.route('/today-count', methods=['GET'])
def today_count():
    today = datetime.utcnow().date()
    count = Track.query.filter(func.date(Track.played_at) == today).count()
    return jsonify(count)

@app.route('/month-tracks', methods=['GET'])
def month_tracks():
    now = datetime.utcnow()
    current_month = now.month
    current_year = now.year
    tracks = db.session.query(
        Track.track_name, 
        Track.artist_name, 
        Track.played_at
    ).filter(
        db.extract('month', Track.played_at) == current_month,
        db.extract('year', Track.played_at) == current_year
    ).all()
    if not tracks:
        return jsonify({"message": "No tracks found for the current month."}), 404
    tracks_dic = [{'track_name': track[0], 'artist_name': track[1], 'played_at': track[2]} for track in tracks]
    print(tracks_dic)
    return jsonify(tracks_dic)

@app.route('/month-count', methods=['GET'])
def month_count():
    now = datetime.utcnow()
    current_month = now.month
    current_year = now.year
    count = db.session.query(
        Track.track_name, 
        Track.artist_name, 
        Track.played_at
    ).filter(
        db.extract('month', Track.played_at) == current_month,
        db.extract('year', Track.played_at) == current_year
    ).count()
    if not count:
        return jsonify({"message": "No tracks found for the current month."}), 404
    print(count)
    return jsonify(count)

if __name__ == '__main__':
    app.run(debug=True)
