from flask import request, jsonify
from app import db, bcrypt
from app.models.user import User, Token
from app.utils.token import generate_token

def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password'], bcrypt):
        token_str = generate_token()
        token = Token(token=token_str, user_id=user.id)
        db.session.add(token)
        db.session.commit()
        return jsonify({'token': token_str})
    return jsonify({'message': 'Invalid credentials'}), 401

def logout():
    token_value = request.headers.get('Authorization')
    token = Token.query.filter_by(token=token_value).first()
    if token:
        db.session.delete(token)
        db.session.commit()
    return jsonify({'message': 'Logged out'})

def me():
    user = request.user
    return jsonify({'id': user.id, 'username': user.username, 'role': user.role.name})
