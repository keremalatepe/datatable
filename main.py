# main.py

from app import app
from db_setup import init_db, db_session
from forms import AlbumForm, ConfigurationForm
from flask import flash, render_template, request, redirect
from models import Album, Configuration
from flask_table import create_table

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    results = db_session.query(Album)

    return render_template('results.html', table=results)

@app.route('/configurations', methods=['GET', 'POST'])
def configurations():
    results = []
    results = db_session.query(Configuration)

    return render_template('configurations.html', table=results)    



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

#conf eklendiginde data tablosunun guncellenebilmesi icin fonksiyon
def reload_table():
    i = 1
    q = True
    while q:
        qry = db_session.query(Album).filter(Album.id==i)
        album = qry.first()
        if album is None:
            q = False
            continue
        i += 1
        album.name = reload_table_type(album)
        db_session.commit()


#conf eklendiginde tek tek tum conflarla karsilastirmasi icin fonksiyon. 
#conf_type() fonksiyonunun aynisi
def reload_table_type(form):
    k = 0
    conf_type = 1
    ctr1 = 0
    i = 1
    q = True
    while q:
        
        qry1 = db_session.query(Configuration).filter(Configuration.id == i)
        configuration1 = qry1.first()
        if configuration1 is None:
            q = False
            continue

        ctr2 = 0
        if k == 0:
            if configuration1.title == form.title:
                ctr1 += 1
            if configuration1.release_date == form.release_date:
                ctr1 += 1
            if configuration1.publisher == form.publisher:
                ctr1 += 1
            if configuration1.album_name == form.album_name:
                ctr1 += 1
            k += 1
        else:
            if configuration1.title == form.title:
                ctr2 += 1
            if configuration1.release_date == form.release_date:
                ctr2 += 1
            if configuration1.publisher == form.publisher:
                ctr2 += 1
            if configuration1.album_name == form.album_name:
                ctr2 += 1
        if ctr2 > ctr1:
            ctr1 = ctr2
            conf_type = i
        i+=1


    qry2 = db_session.query(Configuration).filter(Configuration.id == conf_type)
    configuration1 = qry2.first()
    return configuration1.artist


#yeni conf eklemek icin
@app.route('/new_configuration', methods=['GET', 'POST'])
def new_configuration():
    """
    Add a new album
    """
    form = ConfigurationForm(request.form)

    if request.method == 'POST':
        # save the album
        configuration = Configuration()
        save_changes_configuration(configuration, form, new=True)
        return redirect('/configurations')

    return render_template('new_configuration.html', form=form)


#data table a element eklerken veya guncellerken conf tipini belirlemek icin 
#tek tek her biriyle benzer olan eleman sayisina bakip en cok benzeyeni donduruyor
def configuration_type(form):
    k = 0
    conf_type = 1
    ctr1 = 0
    i = 1
    q = True
    while q:
        
        qry1 = db_session.query(Configuration).filter(Configuration.id == i)
        configuration1 = qry1.first()
        if configuration1 is None:
            q = False
            continue

        ctr2 = 0
        if k == 0:
            if configuration1.title == form.title.data:
                ctr1 += 1
            if configuration1.release_date == form.release_date.data:
                ctr1 += 1
            if configuration1.publisher == form.publisher.data:
                ctr1 += 1
            if configuration1.album_name == form.album_name.data:
                ctr1 += 1
            k += 1
        else:
            if configuration1.title == form.title.data:
                ctr2 += 1
            if configuration1.release_date == form.release_date.data:
                ctr2 += 1
            if configuration1.publisher == form.publisher.data:
                ctr2 += 1
            if configuration1.album_name == form.album_name.data:
                ctr2 += 1
        if ctr2 > ctr1:
            ctr1 = ctr2
            conf_type = i
        i+=1


    qry2 = db_session.query(Configuration).filter(Configuration.id == conf_type)
    configuration1 = qry2.first()
    return configuration1.artist

#datatable a yeni eklenen veya guncellenen verinin kaydedilmesi icin
def save_changes(album, form, new=False):

    if new:
        # Add the new album to the database
        album.artist = form.artist.data
        album.name = configuration_type(form)
        album.title = form.title.data
        album.release_date = form.release_date.data
        album.publisher = form.publisher.data
        album.album_name = form.album_name.data
        db_session.add(album)
    else:
        album.artist = form.artist.data
        album.name = configuration_type(form)
        album.title = form.title.data
        album.release_date = form.release_date.data
        album.publisher = form.publisher.data
        album.album_name = form.album_name.data
        
    # commit the data to the database
    db_session.commit()

#conf tablea a yeni eklenen veya guncellenen verinin kaydedilmesi icin
def save_changes_configuration(configuration, form, new=False):

    if new:
        configuration.artist = form.artist.data
        configuration.title = form.title.data
        configuration.release_date = form.release_date.data
        configuration.publisher = form.publisher.data
        configuration.album_name = form.album_name.data
        #database e ekliyor
        db_session.add(configuration)
    else:
     
        configuration.artist = form.artist.data
        configuration.title = form.title.data
        configuration.release_date = form.release_date.data
        configuration.publisher = form.publisher.data
        configuration.album_name = form.album_name.data

    #databasede paylasiyor
    db_session.commit()
    #datatable in goncellenmesi icin fonksiyon cagiriliyor
    reload_table()


#datatable editlemesi icin fonksiyon
@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = db_session.query(Album).filter(Album.id==id)
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

#conf table editlenmesi icin fonksiyon
@app.route('/item/configuration/<int:id>', methods=['GET', 'POST'])
def edit_configuration(id):
    qry = db_session.query(Configuration).filter(
                Configuration.id==id)
    configuration = qry.first()

    if configuration:
        form = ConfigurationForm(formdata=request.form, obj=configuration)
        if request.method == 'POST' and form.validate():
            save_changes_configuration(configuration, form)
            return redirect('/configurations')
        return render_template('edit_configuration.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)


if __name__ == '__main__':
    import os
    app.debug = True
    app.run(port=5001)