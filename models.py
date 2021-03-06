from app import db


class Album(db.Model):
    """"""
    __tablename__ = "albums"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    artist = db.Column(db.String)
    title = db.Column(db.String)
    release_date = db.Column(db.String)
    publisher = db.Column(db.String)
    album_name = db.Column(db.String)


class Configuration(db.Model):
    """"""
    __tablename__ = "configurations"

    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String)
    title = db.Column(db.String)
    release_date = db.Column(db.String)
    publisher = db.Column(db.String)
    album_name = db.Column(db.String)
