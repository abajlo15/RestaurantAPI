from flask_restplus import Api

from .auth_controller import api as auth_ns
from .restaurant_controller import api as restaurant_ns
from .admin_controller import api as admin_ns

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
    'Basic Auth': {
        'type': 'basic',
        'in': 'header',
        'name': 'Authorization'
    },
    'Admin Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-Admin-Token'
    }
}

api = Api(
    title='Restaurant API',
    version='1.0.0',
    description='Sveučilište u Zadru - Antonio Bajlo - Razvoj web aplikacija',
    contact='abajlo15@unizd.hr',
    authorizations=authorizations,
    serve_challenge_on_401=False
)

api.add_namespace(auth_ns)
api.add_namespace(restaurant_ns)
api.add_namespace(admin_ns)