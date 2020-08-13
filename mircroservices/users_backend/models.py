from flask import Flask
from datetime import datetime
from users_backend.app import db, app

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime, default=datetime.now)

    def hash_password(self, password):
        from users.app import bcrypt
        self.password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        from users.app import bcrypt
        return crypt.check_password_hash(password, self.password_hash)

    def __repr__(self):
        return '<User {}>'.format(self.username)  