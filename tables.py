from flask_table import Table, Col, LinkCol
from flask import Flask, Markup, request, url_for

class Results(Table):
    id = Col('Id', show=False ,allow_sort =True)
    artist = Col('Artist',allow_sort =True)
    title = Col('Title',allow_sort =True)
    release_date = Col('Release Date',allow_sort =True)
    publisher = Col('Publisher',allow_sort =True)
    media_type = Col('Media',allow_sort =True)
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'), allow_sort=True)
