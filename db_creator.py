from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from app import db

engine = create_engine('postgresql://postgres:1234@localhost/baykar_proje', echo=True)
Base = declarative_base()



class Album(Base):
    """"""
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    artist = Column(String)
    title = Column(String)
    release_date = Column( )
    publisher = Column(String)
    album_name = Column(String)


class Configuration(Base):
    """"""
    __tablename__ = "configurations"

    id = Column(Integer, primary_key=True)
    artist = Column(String)
    title = Column(String)
    release_date = Column(String)
    publisher = Column(String)
    album_name = Column(String)
    
# create tables
Base.metadata.create_all(engine)