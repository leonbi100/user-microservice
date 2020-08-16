from flask import Flask
from datetime import datetime
from users_backend.app import app
from flask_bcrypt import Bcrypt
from users_backend.db import db

bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime, nullable=True)

    def hash_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        if not self.password_hash or not password:
            return False
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)  

