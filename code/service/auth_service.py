from flask import request,make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

from model import db
from model.restaurant import Restaurant

from config import secret_key, admin_key

class Auth:

    @staticmethod
    def login(request):
        auth = request.authorization

        if not auth or not auth.restaurantname or not auth.password:
            return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

        restaurant = Restaurant.query.filter_by(email=auth.restaurantname).first()

        if not restaurant:
            return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

        if check_password_hash(restaurant.password, auth.password):
            token = jwt.encode({'email' : restaurant.email, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, secret_key)

            return {'token' : token.decode('UTF-8')}

        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    @staticmethod
    def logout(data):
        # TODO store token in blacklist table
        return {},200  

# decorator used for guarding api endpoints from public access
def authenticated(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return {'message' : 'Auth token is missing!'}, 401

        try: 
            data = jwt.decode(token, secret_key)
            current_restaurant = Restaurant.query.filter_by(email=data['email']).first()
        except:
            return {'message' : 'Auth token is invalid!'}, 401

        print("AUTH OK =>", current_restaurant.email)    

        return f(current_restaurant, *args, **kwargs)

    return decorated

# decorator used for guarding api endpoints from non-admin access
def authenticated_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return {'message' : 'Auth token is missing!'}, 401

        try: 
            data = jwt.decode(token, secret_key)
            current_restaurant = Restaurant.query.filter_by(email=data['email']).first()
        except:
            return {'message' : 'Auth token is invalid!'}, 401

        if current_restaurant.admin:
            print("ADMIN AUTH OK =>", current_restaurant.email)    
            return f(current_restaurant, *args, **kwargs)
        else:
            return {'message' : 'Admin permission required!'}, 403

    return decorated    

# decorator used for guarding api endpoints from non-admin access (plain method)
def admin_only(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'X-Admin-Token' in request.headers:
            token = request.headers['X-Admin-Token']

        if not token:
            return {'message' : 'Auth token is missing!'}, 401

        if token == admin_key:
            return f(*args, **kwargs)

    return decorated   