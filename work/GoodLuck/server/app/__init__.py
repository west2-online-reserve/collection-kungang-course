from datetime import timedelta

from flask import Flask, jsonify
from flask_cors import CORS  # 解决跨域问题
from flask_jwt_extended import JWTManager

from .auth import auth_bp
from .feedback import feedback_bp
from .upload import upload_bp
from .example import example_bp
from .history import history_bp
from .train_plan import train_bp
from .admin import admin_bp
from . import config

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.JWT_ACCESS_TOKEN_EXPIRES
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    app.config['JWT_ALGORITHM'] = config.JWT_ALGORITHM


    jwt = JWTManager(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(train_bp)
    app.register_blueprint(example_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(admin_bp)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'status': 'error',
            'message': 'Token已过期'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'status': 'error',
            'message': '无效的Token'
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'status': 'error',
            'message': '缺少访问令牌'
        }), 401


    from .database import get_db
    get_db()

    # ... 其他配置（如数据库）

    CORS(app)  # 启用CORS支持[1,4](@ref)
    return app