import hashlib

from flask import jsonify


def hash_password(password: str) -> str:
    """密码哈希"""
    return hashlib.sha256(password.encode()).hexdigest()


def success_response(data=None, message='操作成功'):
    """成功响应"""
    return jsonify({
        'code': 200,
        'message': message,
        'data': data
    })


def error_response(message='操作失败', code=400):
    """错误响应"""
    return jsonify({
        'code': code,
        'message': message,
        'data': None
    }), code
