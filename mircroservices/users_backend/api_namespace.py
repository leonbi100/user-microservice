from flask import request, jsonify, make_response
from flask_restplus import Namespace, Resource, fields, abort
from users_backend.models import User
from datetime import datetime
from users_backend.schemas import UserSignupSchema, UserSchema
from users_backend.db import db
from sqlalchemy import exc
from flask_jwt_extended import (
    jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
from users_backend.app import api

user_namespace = Namespace('users', description='Users operations API')
token_namespace = Namespace('token', description='Users operations API')

get_user_model = user_namespace.model('Get Single User Model', {
    'id': fields.String,
})

login_model = user_namespace.model('Login Model', {
    'email': fields.String,
    'password': fields.String
})

signup_model = user_namespace.model('Signup Model', {
    'username': fields.String,
    'email': fields.String,
    'password': fields.String
})

@user_namespace.route('/')
class AllUsers(Resource):
    @jwt_required
    @user_namespace.response(200, 'Success')
    def get(self):
        '''
        Returns all users
        '''
        users = User.query.all()
        return UserSchema().dump(users, many=True)

@user_namespace.route('/<int:id>')
class UserId(Resource):

    @jwt_required
    @user_namespace.response(200, 'Success')
    @user_namespace.response(400, 'Validation Error')
    @user_namespace.response(404, 'Not Found')
    def get(self, id):
        '''
        Input user id and returns that user's data
        '''
        return User.query.filter_by(id=id).first_or_404()

@user_namespace.route('/login')
class UserLogin(Resource):

    @user_namespace.doc('login')
    @user_namespace.expect(login_model, envelope='resource')
    @user_namespace.response(200, 'Success')
    @user_namespace.response(400, 'Validation Error')
    @user_namespace.response(401, 'Unauthorized')
    @user_namespace.response(404, 'Not Found')
    def post(self):
        '''
        Login and return an Authorization header
        '''
        res = request.get_json()
        user = User.query.filter_by(email=res['email']).first()
        if not user:
            abort(404, "No account with email {}".format(res['email']))
        if not user.verify_password(res['password']):
            abort(401, "Incorrect Password")
        
        access_token = create_access_token(identity=res['email'])
        refresh_token = create_refresh_token(identity=res['email'])

        resp = jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        })
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return make_response(resp, 200)
        
        

@user_namespace.route('/signup')
class UserSignup(Resource):

    @user_namespace.doc('signup')
    @user_namespace.expect(signup_model)
    @user_namespace.response(200, 'Success')
    @user_namespace.response(400, 'Validation Error')
    @user_namespace.response(500, 'Internal Server Error')
    def post(self):
        '''
        Creates an account for the input user info
        '''
        try:
            new_user = UserSignupSchema().load(request.get_json())
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError as err:
            db.session.rollback()
            abort(409, err.orig.args)


@user_namespace.route('/logout')
class LogOut(Resource):
    @user_namespace.doc('logout')
    @user_namespace.response(200, 'Success')
    def post(self):
        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        return make_response(resp, 200)
        

@token_namespace.route('/refresh')
class RefreshToken(Resource):
    @jwt_refresh_token_required
    def post(self):
        # Create the new access token
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)

        # Set the access JWT and CSRF double submit protection cookies
        # in this response
        resp = jsonify({'refresh': True})
        set_access_cookies(resp, access_token)
        return make_response(resp, 200)
