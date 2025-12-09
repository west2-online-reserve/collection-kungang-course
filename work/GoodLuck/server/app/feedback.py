from flask import Flask, request, jsonify,Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from . import config

from .api.tools import error_response, success_response, hash_password


feedback_bp = Blueprint('feedback', __name__, url_prefix='/api')
from .database import get_db

system=get_db(config.DataBase_Name)

@feedback_bp.route('/feedback', methods=['POST'])
@jwt_required()
def feedback():
    try:
        data=request.get_json()
        user_id = get_jwt_identity()


        # 通过ID获取用户信息
        users = system.user_manager.get_all_users()
        user = None
        for u in users:
            if int(u['id']) == int(user_id):
                user = u
                break

        if not user:
            return error_response('用户不存在', 404)
        content=data.get('content')
        email=data.get('email','')
        system.feedback_manager.add_feedback(user['id'],content, email)

        return success_response('')

    except Exception as e:
        return error_response( str(e),400)



