from functools import wraps
from flask import request, jsonify
from app.models.user import Token, User
from app import db

def token_required(role_required=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token_value = request.headers.get('Authorization')
            if not token_value:
                return jsonify({'message': 'Token is missing'}), 401

            token = db.session.query(Token).filter_by(token=token_value).first()
            if not token:
                return jsonify({'message': 'Invalid token'}), 401

            user = db.session.get(User, token.user_id)
            if role_required and user.role.name != role_required:
                return jsonify({'message': 'Forbidden'}), 403

            request.user = user
            return f(*args, **kwargs)
        return wrapper
    return decorator
