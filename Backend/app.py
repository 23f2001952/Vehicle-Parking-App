from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models  import User,ParkingLot
from application.security import jwt
from application.routes import api_bp

app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(api_bp,url_prefix='/api')
    app.app_context().push()
    
    with app.app_context():
        db.create_all()

        if not User.query.filter_by(email="admin@admin.com").first():
            db.session.add(User(username='admin', email="admin@admin.com", password=generate_password_hash("admin"), role="admin"))

        if not User.query.filter_by(email="dev@user.com").first():
            db.session.add(User(username='dev', email="dev@user.com", password=generate_password_hash("devanshu")))

        db.session.commit()

    return app

app = create_app()

from application.routes import *


if __name__ == "__main__":
    app.run()