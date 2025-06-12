from flask import request, jsonify
from app import db, bcrypt
from app.models.user import User
from app.models.role import Role

def get_all_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username, 'role': u.role.name} for u in users])

def create_user():
    data = request.get_json()
    role = Role.query.filter_by(name=data['role']).first()
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], password_hash=hashed_pw, role=role)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created'})

def update_user(user_id):
    user = request.user
    if user.id != user_id and user.role.name != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.get_json()
    if 'password' in data:
        user.password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    db.session.commit()
    return jsonify({'message': 'User updated'})

def delete_user(user_id):
    user = request.user
    if user.id != user_id and user.role.name != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    target = User.query.get_or_404(user_id)
    db.session.delete(target)
    db.session.commit()
    return jsonify({'message': 'User deleted'})
