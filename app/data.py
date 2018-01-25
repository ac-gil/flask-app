import csv
from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, and_
from sqlalchemy.sql import text,func

# FLASK app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# SQLAlchemy object
db = SQLAlchemy(app)

# ------------------------------Cars Class-----------------------------


class Cars(db.Model):
    make = db.Column(db.String)
    model = db.Column(db.String(50))
    year = db.Column(db.Integer)
    chassis_id = db.Column(db.String(50))
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_updated = db.Column(db.DateTime)
    price = db.Column(db.Numeric(precision=5, scale=2, asdecimal=False))


db.create_all()

# ------------------------------SEED METHOD-----------------------------


def seed():
    with open('cars.csv') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for line in csv_reader:
            car = Cars(
                make=line[0],
                model=line[1],
                year=None if (line[2] == '') else int(line[2]),
                chassis_id=line[3],
                id=int(line[4]),
                last_updated=datetime.strptime(line[5], '%Y-%m-%d %H:%M:%S'),
                price=None if (line[6] == '') else float(line[6])
            )
            try:
                db.session.add(car)
                db.session.commit()
            except exc.IntegrityError:
                db.session().rollback()


# call seed method
seed()


# ------------------------------API SECTION-----------------------------

# welcome
@app.route('/')
def welcome():
    return "Welcome!"


# get a single car by id
@app.route('/car/<id>', methods=['GET'])
def get_car(id):
    car = Cars.query.filter_by(id=id).first()
    if not car:
        return jsonify({'error': 'there is no car with that id'}), 400
    return jsonify({
        'make': car.make,
        'model': car.model,
        'year': car.year,
        'id': car.id,
        'last_updated': car.last_updated,
        'price': car.price
    })


# get all cars
@app.route('/car', methods=['GET'])
def get_all_cars():
    cars = Cars.query.all()
    output = []
    for car in cars:
        car_data = {}
        car_data['make'] = car.make
        car_data['model'] = car.model
        car_data['year'] = car.year
        car_data['id'] = car.id
        car_data['last_updated'] = car.last_updated
        car_data['price'] = car.price
        output.append(car_data)
    return jsonify({'cars': output})


# add a new car
@app.route('/car', methods=['POST'])
def add_car():
    post = request.get_json()
    car = Cars(
        make=post['make'] if 'make' in post else None,
        model=post['model'] if 'model' in post else None,
        year=int(post['year']) if 'year' in post else None,
        chassis_id=post['chassis_id'] if 'chassis_id' in post else None,
        id=None,
        last_updated=datetime.now(),
        price=float(post['price']) if 'price' in post else None,
    )
    try:
        db.session.add(car)
        db.session.commit()
    except exc.IntegrityError:
        db.session().rollback()
    return "car added to database.", 201

# price avg
@app.route('/avgprice', methods=['POST'])
def avg_price():
    post = request.get_json()
    v_make = post['make']
    v_model = post['model']
    v_year = int(post['year'])
    result = db.session.query(func.avg(Cars.price).label('average')).filter(and_(Cars.model==v_model, Cars.make==v_make,Cars.year==v_year)).first()
    if result.average is None:
        return jsonify({'avg_price': 'AVG not found'}), 400
    else:
        return jsonify({'avg_price': result.average})


# run app
app.run(host='0.0.0.0')
