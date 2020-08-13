from users.app import ma
from users.models import User
from datetime import datetime

class UserSchema(Schema):
    class Meta:
        model = User
    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    password = ma.auto_field()