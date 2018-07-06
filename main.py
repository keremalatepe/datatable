# main.py

from app import app
from db_setup import init_db, db_session
from forms import AlbumForm, VersionForm
from flask import flash, render_template, request, redirect
from models import Album, Version
from flask_table import create_table

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    results = db_session.query(Album)

    return render_template('results.html', table=results)

@app.route('/versions', methods=['GET', 'POST'])
def versions():
    results = []
    results = db_session.query(Version)

    return render_template('versions.html', table=results)    



@app.route('/new_album', methods=['GET', 'POST'])
def new_album():
    """
    Add a new album
    """
    form = AlbumForm(request.form)

    if request.method == 'POST':
        # save the album
        album = Album()
        save_changes(album, form, new=True)
        flash('Album created successfully!')
        return redirect('/')

    return render_template('new_album.html', form=form)

@app.route('/new_version', methods=['GET', 'POST'])
def new_version():
    """
    Add a new album
    """
    form = VersionForm(request.form)

    if request.method == 'POST':
        # save the album
        version = Version()
        save_changes_version(version, form, new=True)
        return redirect('/versions')

    return render_template('new_version.html', form=form)



def version_type(form):
    k = 0
    vers_type = 1
    ctr1 = 0
    i = 1
    q = True
    while q:
        
        qry1 = db_session.query(Version).filter(Version.id == i)
        version1 = qry1.first()
        if version1 is None:
            q = False
            continue

        ctr2 = 0
        if k == 0:
            if version1.title == form.title.data:
                ctr1 += 1
            if version1.release_date == form.release_date.data:
                ctr1 += 1
            if version1.publisher == form.publisher.data:
                ctr1 += 1
            if version1.album_name == form.album_name.data:
                ctr1 += 1
            k += 1
        else:
            if version1.title == form.title.data:
                ctr2 += 1
            if version1.release_date == form.release_date.data:
                ctr2 += 1
            if version1.publisher == form.publisher.data:
                ctr2 += 1
            if version1.album_name == form.album_name.data:
                ctr2 += 1
        if ctr2 > ctr1:
            ctr1 = ctr2
            vers_type = i
        i+=1


    qry2 = db_session.query(Version).filter(Version.id == vers_type)
    version1 = qry2.first()
    return version1.artist


def save_changes(album, form, new=False):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object
    if new:
        # Add the new album to the database
        album.artist = form.artist.data
        album.name = version_type(form)
        album.title = form.title.data
        album.release_date = form.release_date.data
        album.publisher = form.publisher.data
        album.album_name = form.album_name.data
        db_session.add(album)
    else:
        album.artist = form.artist.data
        album.name = version_type(form)
        album.title = form.title.data
        album.release_date = form.release_date.data
        album.publisher = form.publisher.data
        album.album_name = form.album_name.data
        
    # commit the data to the database
    db_session.commit()

def save_changes_version(version, form, new=False):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object
    if new:
        # Add the new album to the database
        version.artist = form.artist.data
        version.title = form.title.data
        version.release_date = form.release_date.data
        version.publisher = form.publisher.data
        version.album_name = form.album_name.data
        db_session.add(version)
    else:
     
        version.artist = form.artist.data
        version.title = form.title.data
        version.release_date = form.release_date.data
        version.publisher = form.publisher.data
        version.album_name = form.album_name.data

    # commit the data to the database
    db_session.commit()

@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = db_session.query(Album).filter(
                Album.id==id)
    album = qry.first()

    if album:
        form = AlbumForm(formdata=request.form, obj=album)
        if request.method == 'POST' and form.validate():
            # save edits
            save_changes(album, form)
            return redirect('/')
        return render_template('edit_album.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)

@app.route('/item/version/<int:id>', methods=['GET', 'POST'])
def edit_version(id):
    qry = db_session.query(Version).filter(
                Version.id==id)
    version = qry.first()

    if version:
        form = VersionForm(formdata=request.form, obj=version)
        if request.method == 'POST' and form.validate():
            # save edits
            save_changes_version(version, form)
            return redirect('/versions')
        return render_template('edit_version.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)


if __name__ == '__main__':
    import os
    app.debug = True
    app.run(port=5001)