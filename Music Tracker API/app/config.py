import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@localhost:5432/MusicTracker'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CLIENT_ID = '1c37db7966804c17ada79eff73b8b247'
    CLIENT_SECRET = '90977a877a8f4ba08bc95fe2ef7585df'
    REDIRECT_URI = 'http://localhost:8888/callback/'
    SPOTIFY_SCOPE = 'user-read-recently-played'
