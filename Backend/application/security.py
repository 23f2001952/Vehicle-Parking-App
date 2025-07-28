from flask_jwt_extended import JWTManager
from application.models import User

jwt = JWTManager()

@jwt.user_identity_loader
def load(user):
    return str(user.id)

@jwt.user_lookup_loader
def user_lookup_callback(__jwt_header,jwt_data):
    identity = jwt_data['sub']
    print(identity)
    return User.query.filter_by(id=identity).one_or_none()
