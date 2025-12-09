"""

"""
import os
from datetime import timedelta

class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # MySQL数据库配置
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or '629528'  # 修改为您的MySQL密码
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'class_management'
    
    # CORS配置
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    MYSQL_HOST = 'localhost'

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    # 生产环境下强制使用环境变量
    if not os.environ.get('SECRET_KEY'):
        raise ValueError("生产环境必须设置 SECRET_KEY 环境变量")
    if not os.environ.get('JWT_SECRET_KEY'):
        raise ValueError("生产环境必须设置 JWT_SECRET_KEY 环境变量")
    if not os.environ.get('MYSQL_PASSWORD'):
        raise ValueError("生产环境必须设置 MYSQL_PASSWORD 环境变量")

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    MYSQL_DATABASE = 'class_management_test'

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
