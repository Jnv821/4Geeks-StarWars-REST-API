from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# When doing many to many it is best to create a table instead of a model.

favorites = db.Table(
    'favorites',
    db.Column('id',db.Integer, primary_key=True),
    db.Column('id_user',db.Integer, db.ForeignKey('user.id')),
    db.Column('id_characters',db.Integer, db.ForeignKey('characters.id')),
    db.Column('id_planets',db.Integer, db.ForeignKey('planets.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32),unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_characters = db.relationship('Characters', secondary=favorites, backref='characters_favorited_by')
    favorite_planets = db.relationship('Planets', secondary=favorites, backref='planets_favorited_by')

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }

    def serialize_favorites(self):
        return {
            "id": self.id,
            "username": self.username,
            "favorite_characters": self.favorite_characters,
            "favorite_planets": self.favorite_planets
        }

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    hair_color = db.Column(db.String(250))
    skin_color = db.Column(db.String(250))
    birth_year = db.Column(db.String(250))
    gender = db.Column(db.String(250))
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
    
    def serialize_details(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "birth_year": self.birth_year,
            "gender": self.gender
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(250))
    diameter = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    gravity = db.Column(db.String(250))
    population = db.Column(db.Integer)
    climate = db.Column(db.String(250))
    terrain = db.Column(db.String(250))
    surface_water = db.Column(db.Integer)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def serialize_details(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water
        }