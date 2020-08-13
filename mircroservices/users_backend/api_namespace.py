from flask import request
from flask_restplus import Namespace, Resource, fields, abort
from users_backend.models import User
from datetime import datetime

api_namespace = Namespace('users', description='Users operations API')

get_user_model = api_namespace.model('Get Single User Model', {
    'id': fields.String,
})

login_model = api_namespace.model('Login Model', {
    'username': fields.String,
    'password': fields.String
})

signup_model = api_namespace.model('Signup Model', {
    'username': fields.String,
    'email': fields.String,
    'password': fields.String,
    'confirm_password': fields.String
})

@api_namespace.route('/')
class User(Resource):

    def get(self):
        '''
        Returns all users
        '''
        return User.all()

@api_namespace.route('/<int:id>')
class User(Resource):

    @api_namespace.response(200, 'Success')
    @api_namespace.response(400, 'Validation Error')
    @api_namespace.response(404, 'Not Found')
    def get(self, id):
        '''
        Input user id and returns that user's data
        '''
        return User.query.filter_by(id=id).first_or_404()

@api_namespace.route('/login')
class UserLogin(Resource):

    @api_namespace.doc('login')
    @api_namespace.expect(login_model, envelope='resource')
    @api_namespace.response(200, 'Success')
    @api_namespace.response(400, 'Validation Error')
    @api_namespace.response(404, 'Not Found')
    def post(self):
        '''
        Login and return an Authorization header
        '''
        print(request)
        

@api_namespace.route('/signup')
class UserSignup(Resource):

    @api_namespace.doc('signup')
    @api_namespace.expect(signup_model)
    @api_namespace.response(200, 'Success')
    @api_namespace.response(400, 'Validation Error')
    @api_namespace.response(500, 'Internal Server Error')
    def post(self):
        '''
        Creates an account for the input user info
        '''
        user = UserSchema(request.get_json)
        print(user)
        
        
