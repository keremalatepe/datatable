# main.py

from app import app
from db_setup import init_db, db_session
from forms import AlbumForm, ConfigurationForm
from flask import flash, render_template, request, redirect
from models import Album, Configuration
import models
from flask_table import create_table
from sqlalchemy import inspect


init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    results = db_session.query(Album)
    a1 = table_as_dict(results)
    return render_template('results.html', table=a1)

@app.route('/configurations', methods=['GET', 'POST'])
def configurations():
    results = []
    results = db_session.query(Configuration)
    a1 = table_as_dict_conf(results)
    return render_template('configurations.html', table=a1)    



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
        return redirect('/')

    return render_template('new_album.html', form=form)


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

        a1 = object_as_dict(configuration1)
        for key in set(a1) & set(form):
            if a1[key] == form[key]:
                ctr2+=1       

        if ctr2 > ctr1:
            ctr1 = ctr2
            conf_type = i
        i+=1

    qry2 = db_session.query(Configuration).filter(Configuration.id == conf_type)
    configuration1 = qry2.first()
    return configuration1.artist

def table_as_dict(table):
    q = True
    i = 1
    a = []
    while q: 
        obj = table.filter(Album.id == i).first()
        i+=1
        if obj is None:
            q = False
            continue
        obj_dict = object_as_dict(obj)
        a.append(dict(obj_dict))
    return a

def table_as_dict_conf(table):
    q = True
    i = 1
    a = []
    while q: 
        obj = table.filter(Configuration.id == i).first()
        i+=1
        if obj is None:
            q = False
            continue
        obj_dict = object_as_dict(obj)
        a.append(dict(obj_dict))
    return a


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


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
        album1 = object_as_dict(album)
        i += 1
        album.name = configuration_type(album1)
        db_session.commit()

#conf tablea a yeni eklenen veya guncellenen verinin kaydedilmesi icin
def save_changes_configuration(configuration, form, new=False):

    if new:
        form_data = dict((key, request.form.get(key)) for key in request.form.keys())
        a = object_as_dict(configuration)
        for key in set(form_data) & set(a):
            a[key] = form_data[key]
        for key, value in a.items():
            setattr(configuration, key, value)
        #database e ekliyor
        db_session.add(configuration)
    else:
     
        form_data = dict((key, request.form.get(key)) for key in request.form.keys())
        a = object_as_dict(configuration)
        for key in set(form_data) & set(a):
            a[key] = form_data[key]
        for key, value in a.items():
            setattr(configuration, key, value)

    #databasede paylasiyor
    db_session.commit()
    #datatable in goncellenmesi icin fonksiyon cagiriliyor
    reload_table()


#datatable a yeni eklenen veya guncellenen verinin kaydedilmesi icin
def save_changes(album, form, new=False):

    if new:
        # Add the new album to the database
        form_data = dict((key, request.form.get(key)) for key in request.form.keys())
        a = object_as_dict(album)
        form_data["name"] = configuration_type(form_data)
        for key in set(form_data) & set(a):
            a[key] = form_data[key]
        for key, value in a.items():
            setattr(album, key, value)

        db_session.add(album)
    else:

        form_data = dict((key, request.form.get(key)) for key in request.form.keys())
        a = object_as_dict(album)
        form_data["name"] = configuration_type(form_data)
        for key in set(form_data) & set(a):
            a[key] = form_data[key]
        qry3 = db_session.query(Album).get(a["id"])

        for key, value in a.items():
            setattr(qry3, key, value)
        
    # commit the data to the database
    db_session.commit()


if __name__ == '__main__':
    import os
    app.debug = True
    app.run(port=5001)