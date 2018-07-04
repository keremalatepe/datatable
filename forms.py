# forms.py

from wtforms import Form, StringField, SelectField, validators

class AlbumForm(Form):

    artist = StringField('Artist')
    title = StringField('Title')
    release_date = StringField('Release Date')
    publisher = StringField('Publisher')
    album_name = StringField('Album Name')
