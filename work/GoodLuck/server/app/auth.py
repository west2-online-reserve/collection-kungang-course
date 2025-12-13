import datetime
import hashlib

from flask import Flask, request, jsonify,Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from jwt import ExpiredSignatureError, InvalidTokenError



from .api.tools import error_response, success_response, hash_password


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
from .database import get_db
from . import config
system=get_db(config.DataBase_Name)







@auth_bp.route('/login', methods=['GET', 'POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()

        if not data:
            return error_response('请求数据不能为空')

        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if not username or not password:
            return error_response('用户名和密码不能为空')

        # 验证用户
        user = system.user_manager.get_user_by_username(username)
        if not user:
            return error_response('用户不存在',400)

        hashed_password = hash_password(password)
        if user['password'] != hashed_password:
            return error_response('密码错误',401)

        # 添加登录记录
        system.login_manager.add_login_record(user['id'])

        # 生成JWT令牌
        access_token = create_access_token(identity=str(user['id']))
        #############################################
        # from flask_jwt_extended import decode_token
        # try:
        #     decoded = decode_token(access_token)
        #     print(f"✅ Token 解码成功: {decoded}")
        # except Exception as decode_error:
        #     print(f"❌ Token 解码失败: {decode_error}")
        #####################################################
        # print(access_token)
        return success_response(

            data={

                'token': access_token,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'role': user['role'],
                    'height': user['height'],
                    'weight': user['weight']
                }
            },
            message='登录成功'
        )

    except Exception as e:
        return error_response(f'登录失败: {str(e)}', 500)




@auth_bp.route('/register', methods=['POST'])
def register():

    """用户注册"""
    try:
        data = request.get_json()

        if not data:
            return error_response('请求数据不能为空')

        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        height = data.get('height')
        weight = data.get('weight')

        # 验证必填字段
        if not username or not password:
            return error_response('用户名和密码不能为空')

        if len(username) < 3:
            return error_response('用户名至少3位')

        if len(password) < 6:
            return error_response('密码至少6位')

        # 检查用户是否已存在
        existing_user = system.user_manager.get_user_by_username(username)
        if existing_user:
            return error_response('用户名已存在')

        # 创建用户
        hashed_password = hash_password(password)
        if system.user_manager.add_user(username, hashed_password, height, weight):
            return success_response(message='注册成功')
        else:
            return error_response('注册失败')

    except Exception as e:
        return error_response(f'注册失败: {str(e)}', 500)


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """获取用户信息"""
    try:
        user_id = get_jwt_identity()

        # 通过ID获取用户信息
        users = system.user_manager.get_all_users()
        user=None
        for u in users:
            if int(u['id']) == int(user_id):
                user=u
                break

        if not user:
            return error_response('用户不存在', 404)

        return success_response(
            data={
                'id': user['id'],
                'username': user['username'],
                'role': user['role'],
                'height': user['height'],
                'weight': user['weight']
            }
        )

    except Exception as e:
        return error_response(f'获取用户信息失败: {str(e)}', 500)


@auth_bp.route('/change_password', methods=['PUT'])
@jwt_required()
def change_password():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            return error_response('请求数据不能为空')

        users = system.user_manager.get_all_users()
        user = next((u for u in users if int(u['id']) == int(user_id)), None)
        if not user:
            return error_response('用户不存在', 404)



        password=data.get('password')
        hashed_password = hash_password(password)
        # print(password)
        username=None
        height =None
        weight =None



        if system.user_manager.update_user(user['id'],username, hashed_password, height, weight):

            return success_response(message='更新成功')
        return error_response('更新失败')
    except Exception as e:
        return error_response(f'更新失败: {str(e)}', 500)

@auth_bp.route('/update_simple_profile', methods=['PUT'])
@jwt_required()
def update_simple_profile():
    """更新用户信息"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            return error_response('请求数据不能为空')

        users = system.user_manager.get_all_users()
        user = next((u for u in users if int(u['id']) == int(user_id)), None)
        if not user:
            return error_response('用户不存在', 404)

        password=None
        username=data.get('username', user['username']).strip()
        height = data.get('height')
        weight = data.get('weight')



        if system.user_manager.update_user(user['id'],username, password, height, weight):

            return success_response(message='更新成功')
        return error_response('更新失败')
    except Exception as e:
        return error_response(f'更新失败: {str(e)}', 500)


@auth_bp.route('/refresh',methods=['GET'])
@jwt_required()
def refresh():
    try:
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

        access_token = create_access_token(identity=str(user['id']))
        return success_response(

            data={

                'token': access_token,

            },
            message='刷新token'
        )
    except Exception as e:
        return error_response(f'服务错误: {str(e)}', 500)



