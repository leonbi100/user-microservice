from flask_sqlalchemy import SQLAlchemy
from users_backend.app import app
from flask_migrate import Migrate

db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.create_all()