from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Date, Float, Text, JSON
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy import select
from sqlalchemy.orm import relationship, Session
from sqlalchemy import exc
from sqlalchemy import and_
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


base = declarative_base()
engine = create_engine('sqlite:///temperatuur.sqlite')
session = Session(engine)

class Bewerking():
   def save(self):
      with Session(engine) as session:
         session.add(self)
         session.commit()


class Kamer(base, Bewerking):
   __tablename__='kamer'
   id = Column(Integer, primary_key=True)
   locatie = Column(String, nullable=False, unique=True)

   sensor = relationship('Sensor', backref='kamer')

class Sensor(base,Bewerking):
   __tablename__="sensor"
   id = Column(Integer, primary_key=True)
   kamerid = Column(Integer,ForeignKey('kamer.id'))
   naam = Column(String, nullable=False)

   sensor_data = relationship('SensorData', backref='sensor')

class SensorData(base, Bewerking):
   __tablename__='sensor_data'
   id = Column(Integer, primary_key=True)
   sensorid = Column(Integer,ForeignKey('sensor.id'), nullable=False)
   stralingstemperatuur = Column(JSON)
   luchttemperatuur = Column(JSON)
   datum = Column(String, nullable=False)
   tijd = Column(String, nullable=False)

from flask_login import UserMixin  
class Gebruiker(base, Bewerking, UserMixin):
   __tablename__='gebruiker'
   id = Column(Integer, primary_key=True)
   gebruikersnaam = Column(String, nullable=False, unique=True)
   email = Column(String, nullable=False, unique=True)
   wachtwoord = Column(String, nullable=False)

def krijg_temperatuur():
    """Deze functie geeft de luchttemperatuur, tijd en datum terug van alle sensordata in de tabel"""
    temperatuur = [temperatuur for temperatuur in session.query(SensorData.luchttemperatuur, SensorData.tijd, SensorData.datum)]
    return temperatuur

def krijg_temperatuur_grafiek(datum, kamer):
    """Deze functie geeft de luchttemperatuur, tijd en datum terug van alle sensordata in de tabel"""
    temperatuur = [temperatuur for temperatuur in session.query(SensorData.tijd, SensorData.luchttemperatuur, SensorData.stralingstemperatuur).filter(SensorData.datum == datum).join(Sensor).join(Kamer).filter(Kamer.locatie == kamer)]
    return temperatuur

def krijg_kamers():
    """Deze functie geeft alle kamers terug die in de database zitten."""
    kamers = [kamer for kamer in session.query(Kamer.locatie)]
    return kamers

   
    
if __name__=='__main__':
   base.metadata.create_all(engine)

   kdata = [("A2.24"),("A2.32")]

   sdata =[(1, "lucht thermometer"),(2., "stralings thermometer")]

   gdata = [("werner","werner@test.nl" ,"Hond123")]


   for x in gdata:
      g = Gebruiker(gebruikersnaam=x[0], email=x[1], wachtwoord=x[2])
      session.add(g)
   for x in kdata:
      k = Kamer(locatie=x)
      session.add(k)
   for x in sdata:
      s = Sensor(kamerid=x[0], naam =x[1])
      session.add(s)

   session.commit()
