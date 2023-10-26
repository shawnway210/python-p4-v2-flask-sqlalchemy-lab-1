# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        body = {
            'id': earthquake.id,
            'location': earthquake.location,
            'magnitude': earthquake.magnitude,
            'year': earthquake.year
        }
        status = 200

        return make_response(body, status)
    else:
        body = {
            'message': f'Earthquake {id} not found.'
        }
        status = 404
    return make_response(body, status)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    count = len(earthquakes)
    quakes_data =[]
    for earthquake in earthquakes:
        quake_data = {
            'id': earthquake.id,
            'location': earthquake.location,
            'magnitude': earthquake.magnitude,
            'year': earthquake.year
        }
        quakes_data.append(quake_data)
    response = {
        'count': count,
        'quakes': quakes_data
    }
    status = 200
    
    return make_response(response, status)




if __name__ == '__main__':
    app.run(port=5555, debug=True)
