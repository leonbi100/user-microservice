from users_backend.app import app
from users_backend.models import User
from datetime import datetime
from flask_marshmallow import Marshmallow
from marshmallow import fields, post_load, pre_load

ma = Marshmallow(app)

class UserSignupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    password = fields.Str()

    @post_load
    def make_user(self, data, **kwargs):
        password = data['password']
        del data['password']
        new_user = User(**data)
        new_user.hash_password(password)
        return new_user

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    date_created = ma.auto_field()
    date_modified = ma.auto_field()