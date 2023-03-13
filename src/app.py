'''
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
'''
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv('DATABASE_URL')
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace('postgres://', 'postgresql://')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        'msg': 'Hello, this is your GET /user response '
    }

    return jsonify(response_body), 200

#[GET] /people Get a list of all the people in the database

@app.route('/people', methods=['GET'])
def get_people():

    characters = Characters.query.all()
    
    character_list = [character.serialize() for character in characters]

    response_body = {
        'response' : 'OK',
        'status': '200',
        'data' :  character_list
    }

    return jsonify(response_body), 200

#[GET] /people/<int:people_id> Get a one single people information

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_details(people_id):
    
    character = Characters.query.get(people_id)

    response_body = {
        'response' : 'OK',
        'status': '200',
        'data' :  character.serialize_details()
    }

    return jsonify(response_body), 200

#[GET] /planets Get a list of all the planets in the database

@app.route('/planets', methods=['GET'])
def get_planets():

    planets = Planets.query.all()

    planet_list = [planet.serialize() for planet in planets]

    response_body = {
        'response': 'OK',
        'status': '200',
        'data': planet_list
    }

    return jsonify(planet_list), 200

#[GET] /planets/<int:planet_id> Get one single planet information

@app.route('/planets/<int:planet_id>', methods=['GET'])

def get_planet_details(planet_id):

    planet = Planets.query.get(planet_id)

    response_body = {
        'response': 'OK',
        'status': '200',
        'data': planet.serialize_details()
    }

    return jsonify(response_body), 200


#[GET] /users Get a list of all the blog post users

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()

    user_list = [user.serialize() for user in users]

    response_body = {
        'response': 'OK',
        'status': '200',
        'data': user_list
    }

    return jsonify(response_body), 200

#[GET] /users/favorites Get all the favorites that belong to the current user.

@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    
    data = request.json
    user = User.query.get(data["id"])
    
    user_favorite_characters = user.favorite_characters

    user_favorite_character_list = [user_favorite_character.serialize() for user_favorite_character in user_favorite_characters ]
    
    user_favorite_planets = user.favorite_planets

    user_favorite_planet_list = [user_favorite_planet.serialize() for user_favorite_planet in user_favorite_planets]
    response_body = {
        'response': 'OK',
        'status': '200',
        'favorite_characters': user_favorite_character_list,
        'favorite_planets': user_favorite_planet_list
    }

    return jsonify(response_body), 200

#[POST] /favorite/planet/<int:planet_id> Add a new favorite planet to the current user with the planet id = planet_id.

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    
    #get planet based on id on the url to serialize data and send it in the body of the response
        data = request.json

        user = User.query.get(data["id"])

        planet = Planets.query.get(planet_id)

        user.favorite_planets.append(planet)

        db.session.add(user)
        db.session.commit()

        response = {
            'response': 'OK',
            'status': '200',
            'description': 'Succesfully added a favorite,'
        }

        return jsonify(response)

#[POST] /favorite/people/<int:people_id> Add a new favorite people to the current user with the people id = people_id.
@app.route('/favorite/people/<int:people_id>', methods=['GET', 'POST'])
def add_favorite_character(people_id):
    
    data = request.json
    user = User.query.get(data['id'])

    character = Characters.query.get(people_id)

    user.favorite_characters.append(character)

    db.session.add(user)
    db.session.commit()

    response = {
        'response': 'OK',
        'status': '200',
        'description': 'Succesfully added a favorite,'
    }
    
    return jsonify(response), 200
#[DELETE] /favorite/planet/<int:planet_id> Delete favorite planet with the id = planet_id.
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):

        data = request.json
        user = User.query.get(data['id'])

        planet = Planets.query.get(planet_id)

        user.favorite_planets.remove(planet)

        db.session.commit()

        response = {
            'response': 'OK',
            'status': '200',
            'description': 'Succesfully deleted a favorite'
        }

        return jsonify(response), 200

#[DELETE] /favorite/people/<int:people_id> Delete favorite people with the id = people_id.
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_character(people_id):

        data = request.json

        user = User.query.get(data['id'])

        character = Characters.query.get(people_id)

        user.favorite_characters.remove(character)

        db.session.commit()

        response = {
            'response': 'OK',
            'status': '200',
            'description': 'Succesfully deleted a favorite'
        }    

        return jsonify(response), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
