from .db import db

class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_name = db.Column(db.String(200), nullable=False)
    artist_name = db.Column(db.String(200), nullable=False)
    played_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Track {self.track_name} by {self.artist_name}>'

