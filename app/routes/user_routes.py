from flask import Blueprint
from app.controllers import user_controller
from app.decorators.auth_decorator import token_required

user_bp = Blueprint('users', __name__)

user_bp.get('/')(token_required('admin')(user_controller.get_all_users))
user_bp.post('/')(token_required('admin')(user_controller.create_user))
user_bp.put('/<int:user_id>')(token_required()(user_controller.update_user))
user_bp.delete('/<int:user_id>')(token_required()(user_controller.delete_user))
