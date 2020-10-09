from . import db

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    ime_restorana = db.Column(db.String(50))
    password = db.Column(db.String(80))
    jelo_1 = db.Column(db.String(30))
    jelo_2 = db.Column(db.String(30))
    jelo_3 = db.Column(db.String(30))
    admin = db.Column(db.Boolean)
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())