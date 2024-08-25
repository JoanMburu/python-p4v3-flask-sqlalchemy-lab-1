from flask import Flask, make_response, jsonify
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
    return make_response(jsonify(body), 200)


@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    with db.session() as session:
        earthquake = session.get(Earthquake, id)
        if earthquake:
            response_body = {
                'id': earthquake.id,
                'location': earthquake.location,
                'magnitude': earthquake.magnitude,
                'year': earthquake.year
            }
            return make_response(jsonify(response_body), 200)
        else:
            return make_response(jsonify({'message': f'Earthquake {id} not found.'}), 404)


@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    with db.session() as session:
        earthquakes = session.query(Earthquake).filter(Earthquake.magnitude >= magnitude).all()
        quakes = [
            {
                'id': quake.id,
                'location': quake.location,
                'magnitude': quake.magnitude,
                'year': quake.year
            }
            for quake in earthquakes
        ]
        response_body = {
            'count': len(quakes),
            'quakes': quakes
        }
        return make_response(jsonify(response_body), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
