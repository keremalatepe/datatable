# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<postgres>:<1234>@localhost/baykar_proje'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = "flask rocks!"
db = SQLAlchemy(app)  
