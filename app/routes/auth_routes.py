from flask import Blueprint
from app.controllers import auth_controller
from app.decorators.auth_decorator import token_required

auth_bp = Blueprint('auth', __name__)

auth_bp.post('/login')(auth_controller.login)
auth_bp.post('/logout')(token_required()(auth_controller.logout))
auth_bp.get('/me')(token_required()(auth_controller.me))
