from flask import Flask
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from users_backend import app

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
db.create_all()
ma = Marshmallow(app)


api = Api(app, version='0.1', title='Users Backend API',
            description='User API for Video Sync App')

app.config['RESTPLUS_MASK_SWAGGER'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/sync_video_users'

from users_backend.api_namespace import api_namespace
api.add_namespace(api_namespace)