#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

import sys
import os
from mysql_pymysql import DatabaseConfig, ClassManagementSystem

def check_requirements():
    """检查依赖是否安装"""
    required_modules = ['flask', 'flask_cors', 'flask_jwt_extended', 'pymysql']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print("❌ 缺少以下依赖模块:")
        for module in missing_modules:
            print(f"   - {module}")
        print("\n💡 请运行以下命令安装依赖:")
        print("pip install -r requirements_mysql.txt")
        return False
    
    return True

def check_database_connection():
    """检查数据库连接"""
    print("🔍 检查数据库连接...")
    
    # 使用默认配置测试连接
    config = DatabaseConfig(
        host='localhost',
        user='root',
        password='629528',  # 修改为您的MySQL密码
        database='class_management'
    )
    
    system = ClassManagementSystem(config)
    
    try:
        if system.initialize():
            print("✅ 数据库连接成功！")
            system.close()
            return True
        else:
            print("❌ 数据库连接失败！")
            return False
    except Exception as e:
        print(f"❌ 数据库连接错误: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 班级管理系统 API 启动程序")
    print("=" * 60)
    
    # 检查依赖
    if not check_requirements():
        sys.exit(1)
    
    # 检查数据库连接
    if not check_database_connection():
        print("\n💡 请检查以下配置:")
        print("1. MySQL服务是否启动")
        print("2. 用户名和密码是否正确")
        print("3. 网络连接是否正常")
        print("\n📝 配置文件位置: mysql.py (第768行)")
        sys.exit(1)
    
    # 启动Flask应用
    print("\n🌟 启动 Flask API 应用...")
    print("📍 访问地址: http://localhost:5001")
    print("📖 API文档: 请查看 README_mysql.md")
    print("⚠️  按 Ctrl+C 停止服务")
    print("-" * 60)
    
    try:
        # 导入并运行Flask应用
        from app_mysql import app
        app.run(
            host='0.0.0.0',
            port=5001,
            debug=True
        )
    except ImportError as e:
        print(f"❌ 导入应用失败: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 服务已停止")
    except Exception as e:
        print(f"❌ 服务启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
