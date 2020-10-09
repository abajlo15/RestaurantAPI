from flask_restplus import Namespace, Resource, fields
from model import db
from model.restaurant import Restaurant
from service.auth_service import admin_only
from controller.restaurant_controller import restaurant_dto

api = Namespace(name='Admin API', path='/api/admin')

@api.route('/db/init-db')
class DatabaseResource(Resource):
    @api.doc(description='Initialize database', security='Admin Auth', responses={200: 'Success', 401: 'Not Authorized', 403: 'Forbidden'})
    @admin_only
    def post(self):
        db.create_all()
        return {'message': 'Database initialization complete.'}


@api.route('/u/<email>')
@api.param('email', 'Restaurant email address')
@api.response(404, 'Restaurant not found.')
class RestaurantResource(Resource):
    @api.doc(description='Get a Restaurant', responses={200: 'Success', 403: 'Forbidden'}, security='Admin Auth')
    @api.marshal_with(restaurant_dto)
    def get(self, email):
        restaurant = Restaurant.query.filter_by(email=email).first()
        if not restaurant:
            api.abort(404)
        else:
            return restaurant 

    @api.doc(description='Delete a restaurant', responses={200: 'Success', 403: 'Forbidden'}, security='Admin Auth')
    def delete(self, email):
        restaurant = Restaurant.query.filter_by(email=email).first()
        if not restaurant:
            api.abort(404)
        else:
            db.session.delete(restaurant)
            db.session.commit()
            return {'message' : 'The restaurant has been deleted!'}


@api.route('/u')
class RestaurantListResource(Resource):
    @api.doc(description='Get all restaurants', responses={200: 'Success', 403: 'Forbidden'}, security='Admin Auth')
    @api.marshal_list_with(restaurant_dto)
    @admin_only
    def get(self):
        restaurants = Restaurant.query.all()

        output = []

        for restaurant in restaurants:
            restaurant_data = {}
            restaurant_data['email'] = restaurant.email
            restaurant_data['ime_restorana'] = restaurant.ime_restorana
            restaurant_data['jelo_1'] = restaurant.jelo_1
            restaurant_data['jelo_2'] = restaurant.jelo_2
            restaurant_data['jelo_3'] = restaurant.jelo_3
            restaurant_data['password'] = restaurant.password
            restaurant_data['admin'] = restaurant.admin
            restaurant_data['created'] = restaurant.created
            restaurant_data['updated'] = restaurant.updated
            output.append(restaurant_data)

        return output                     