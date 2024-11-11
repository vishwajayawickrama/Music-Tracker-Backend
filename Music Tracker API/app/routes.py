from flask import Blueprint, jsonify
from app.models import Track
from app.services import fetch_recent_tracks
from .db import db
from datetime import datetime
from sqlalchemy import func

track_bp = Blueprint('track_bp', __name__)

# Recent tracks
@track_bp.route('/recent-tracks', methods=['GET'])
def recent_tracks():
    fetch_recent_tracks()
    tracks = Track.query.order_by(Track.played_at.desc()).all()
    return jsonify([{'track_id': t.id, 'track_name': t.track_name, 'artist_name': t.artist_name, 'played_at': t.played_at} for t in tracks])

# Recent Count
@track_bp.route('/recent-count', methods=['GET'])
def recent_count():
    count = Track.query.count()
    return jsonify(count)

# Daily Tracks
@track_bp.route('/today-tracks', methods=['GET'])
def today_tracks():
    today = datetime.utcnow().date()
    tracks = Track.query.filter(func.date(Track.played_at) == today).order_by(Track.played_at.desc()).all()
    return jsonify([{'track_name': t.track_name, 'artist_name': t.artist_name, 'played_at': t.played_at} for t in tracks])

# Daily Count
@track_bp.route('/today-count', methods=['GET'])
def today_count():
    today = datetime.utcnow().date()
    count = Track.query.filter(func.date(Track.played_at) == today).count()
    return jsonify(count)

# Monthly tracks
@track_bp.route('/month-tracks', methods=['GET'])
def month_tracks():
    now = datetime.utcnow()
    current_month = now.month
    current_year = now.year
    tracks = db.session.query(
        Track.track_name, Track.artist_name, Track.played_at
    ).filter(
        db.extract('month', Track.played_at) == current_month,
        db.extract('year', Track.played_at) == current_year
    ).all()
    tracks_dic = [{'track_name': track[0], 'artist_name': track[1], 'played_at': track[2]} for track in tracks]
    return jsonify(tracks_dic) if tracks else jsonify({"message": "No tracks found for the current month."})

# Monthly Count
@track_bp.route('/month-count', methods=['GET'])
def month_count():
    now = datetime.utcnow()
    current_month = now.month
    current_year = now.year
    count = db.session.query(
        Track.track_name, Track.artist_name, Track.played_at
    ).filter(
        db.extract('month', Track.played_at) == current_month,
        db.extract('year', Track.played_at) == current_year
    ).count()
    return jsonify(count) if count else jsonify({"message": "No tracks found for the current Month."})

# Yearly Tracks
@track_bp.route('/year-tracks', methods=['GET'])
def year_tracks():
    now = datetime.utcnow()
    current_year = now.year
    tracks = db.session.query(
        Track.track_name, Track.artist_name, Track.played_at
    ).filter(
        db.extract('year', Track.played_at) == current_year
    ).all()
    tracks_dic = [{'track_name': track[0], 'artist_name': track[1], 'played_at': track[2]} for track in tracks]
    return jsonify(tracks_dic) if tracks else jsonify({"message": "No tracks found for the current year."})

# Yearly Count
@track_bp.route('/year-count', methods=['GET'])
def year_count():
    now = datetime.utcnow()
    current_year = now.year
    count = Track.query.filter(
        db.extract('year', Track.played_at) == current_year
    ).count()
    return jsonify(count) if count else jsonify({"message": "No tracks found for the current year."})

