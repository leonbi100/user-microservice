from flask import Flask
from flask_restplus import Api
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['RESTPLUS_MASK_SWAGGER'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/sync_video_users'
app.config['PROPAGATE_EXCEPTIONS'] = True

app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)


api = Api(app, version='0.1', title='Users Backend API',
            description='User API for Video Sync App')

from users_backend.api_namespace import user_namespace
api.add_namespace(user_namespace)