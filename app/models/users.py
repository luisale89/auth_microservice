
from enum import unique
from app.extensions import db
from datetime import datetime

from werkzeug.security import generate_password_hash
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    fname = db.Column(db.String(128))
    lname = db.Column(db.String(128))
    profile_img = db.Column(db.String(256))
    home_address = db.Column(JSON)
    personal_phone = db.Column(db.String(32))
    since = db.Column(db.DateTime, default=datetime.utcnow)
    email_confirm = db.Column(db.Boolean)
    status = db.Column(db.String(12))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    #relationships
    country = db.relationship('Country', back_populates='users', uselist=False, lazy=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "public_id" : self.public_id,
            "fname" : self.fname,
            "lname" : self.lname,
            "profile_img": self.profile_img if self.profile_img is not None else "https://server.com/default.png",
            "home_address": self.home_address,
            "personal_phone": self.personal_phone,
            "user_since": self.since,
            "user_status": self.status, 
            "country": self.country.name if self.country is not None else None
        }

    def serialize_private(self):
        return {
            "email": self.email,
        }

    @property
    def password(self):
        raise AttributeError('Cannot view password')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, method='sha256')


class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    code = db.Column(db.String(24), unique=True)
    #relations
    users = db.relationship('User', back_populates='country', lazy=False)

    def __repr__(self) -> str:
        return '<%r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code
        }

    def serialize_users(self):
        return {"users": list(map(lambda x: x.id, self.users))} if self.users is not None else {"users": []}


class TokenBlacklist(db.Model):
    __tablename__ = 'tokenblacklist'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_identity = db.Column(db.String(64), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    revoked_date = db.Column(db.DateTime)
    expires = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Token %r>' % self.token_type

    def serialize(self):
        return {
            'token_id': self.id,
            'jti': self.jti,
            'token_type': self.token_type,
            'user_identity': self.user_identity,
            'revoked': self.revoked,
            'revoked_date': self.revoked_date,
            'expires': self.expires
        }
