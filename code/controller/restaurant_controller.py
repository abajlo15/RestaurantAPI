from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from model import db
from model.restaurant import Restaurant
from service.auth_service import authenticated, authenticated_admin

api = Namespace(name='Restaurants API', path='/api/restaurants')

restaurant_dto = api.model('Restaurant', {
    'email': fields.String(required=True, description='Email'),
    'ime_restorana': fields.String(required=True, description='Ime Restorana'),
    'jelo_1': fields.String(required=True, description='Jelo s jelovnika'),
    'jelo_2': fields.String(required=True, description='Jelo s jelovnika'),
    'jelo_3': fields.String(required=True, description='Jelo s jelovnika'),
    'password': fields.String(required=True, description='Password'),
    'admin': fields.Boolean(required=True, description='Admin'),
    'created': fields.DateTime(required=True, description='Created'),
    'updated': fields.DateTime(required=True, description='Updated')
})

restaurant_signup_dto = api.model('RestaurantSignup', {
    'email': fields.String(required=True, description='Email'),
    'ime_restorana': fields.String(required=True, description='Ime Restorana'),
    'jelo_1': fields.String(required=True, description='Jelo s jelovnika'),
    'jelo_2': fields.String(required=True, description='Jelo s jelovnika'),
    'jelo_3': fields.String(required=True, description='Jelo s jelovnika'),
    'password': fields.String(required=True, description='Password')
})

restaurant_update_dto = api.model('RestaurantUpdate', {
    'ime_restorana': fields.String(required=True, description='Ime Restorana'),
    'jelo_1': fields.String(required=True, description='Jelo s jelovnika'),
    'jelo_2': fields.String(required=True, description='Jelo s jelovnika'),
    'jelo_3': fields.String(required=True, description='Jelo s jelovnika'),
})

@api.route('/')
class RestaurantListResource(Resource):
    @api.doc(description='Signup', responses={201: 'Success'})
    @api.expect(restaurant_signup_dto)
    def post(self):
        hashed_password = generate_password_hash(api.payload['password'], method='sha256')
        new_restaurant = Restaurant(email=api.payload['email'], ime_restorana=api.payload['ime_restorana'], jelo_1=api.payload['jelo_1'],jelo_2=api.payload['jelo_2'],jelo_3=api.payload['jelo_3'], password=hashed_password, admin=False)
        db.session.add(new_restaurant)
        db.session.commit()
        
        return {'message': 'New Restaurant created!'}, 201

    @api.doc(description='Get Restaurant details', responses={200: 'Success', 401: 'Unauthorized'}, security='Bearer Auth')
    @authenticated
    def get(current_restaurant, self):
        return {
            'email': current_restaurant.email,
            'ime_restorana': current_restaurant.ime_restorana,
            'jelo_1': current_restaurant.jelo_1,
            'jelo_2': current_restaurant.jelo_2,
            'jelo_3': current_restaurant.jelo_3,
            'password': current_restaurant.password,
            'admin': current_restaurant.admin,
            'created': str(current_restaurant.created),
            'updated': str(current_restaurant.updated)
        }


    @api.doc(description='Update Restaurant details', responses={200: 'Success', 401: 'Unauthorized'}, security='Bearer Auth')
    @api.expect(restaurant_update_dto)
    @authenticated
    def put(current_restaurant, self):
        if 'ime_restorana' in api.payload:
            current_restaurant.ime_restorana = api.payload['ime_restorana']

        if 'jelo_1' in api.payload:
            current_restaurant.jelo_1 = api.payload['jelo_1']

        if 'jelo_2' in api.payload:
            current_restaurant.jelo_2 = api.payload['jelo_2']

        if 'jelo_3' in api.payload:
            current_restaurant.jelo_3 = api.payload['jelo_3']


        db.session.commit()        
        
        return {'message': 'Restaurant updated!'}, 200   


@api.route('/<email>')
@api.param('email', 'Restaurant email address')
@api.response(404, 'Restaurant not found.')
class RestaurantResource(Resource):
    @api.doc(description='Get a restaurant', responses={200: 'Success', 403: 'Forbidden'}, security='Bearer Auth')
    @api.marshal_with(restaurant_dto)
    @authenticated_admin
    def get(current_restaurant, self, email):
        restaurant = Restaurant.query.filter_by(email=email).first()
        if not user:
            api.abort(404)
        else:
            return user         