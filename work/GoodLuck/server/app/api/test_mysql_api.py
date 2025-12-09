#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import requests
import json
import time

# API基础URL
BASE_URL = 'http://localhost:5001'

def test_health():
    """测试健康检查接口"""
    print("🔍 测试健康检查接口...")
    try:
        response = requests.get(f'{BASE_URL}/api/health')
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def test_register():
    """测试用户注册"""
    print("\n📝 测试用户注册...")
    user_data = {
        'username': 'testuser',
        'password': '123456',
        'height': 175.5,
        'weight': 70.2
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/auth/register',
            json=user_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 注册失败: {e}")
        return False

def test_login():
    """测试用户登录"""
    print("\n🔐 测试用户登录...")
    login_data = {
        'username': 'testuser',
        'password': '123456'
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/auth/login',
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"响应: {result}")
        
        if response.status_code == 200 and 'data' in result and 'token' in result['data']:
            return result['data']['token']
        return None
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        return None

def test_profile(token):
    """测试获取用户信息"""
    print("\n👤 测试获取用户信息...")
    
    try:
        response = requests.get(
            f'{BASE_URL}/api/auth/profile',
            headers={'Authorization': f'Bearer {token}'}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 获取用户信息失败: {e}")
        return False

def test_add_rating(token):
    """测试添加评分"""
    print("\n⭐ 测试添加评分...")
    rating_data = {
        'rating_content': '测试评分内容 - 表现优秀'
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/ratings',
            json=rating_data,
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 添加评分失败: {e}")
        return False

def test_get_history(token):
    """测试获取历史记录"""
    print("\n📚 测试获取历史记录...")
    
    try:
        response = requests.get(
            f'{BASE_URL}/api/history',
            headers={'Authorization': f'Bearer {token}'}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 获取历史记录失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("🧪 班级管理系统 API 测试")
    print("=" * 60)
    
    # 测试健康检查
    if not test_health():
        print("❌ API服务未启动，请先运行 python run_mysql_api.py")
        return
    
    # 测试注册（可能会失败，如果用户已存在）
    test_register()
    
    # 测试登录
    token = test_login()
    if not token:
        print("❌ 登录失败，无法继续测试需要认证的接口")
        return
    
    print(f"\n🎟️ 获得访问令牌: {token[:50]}...")
    
    # 测试需要认证的接口
    test_profile(token)
    test_add_rating(token)
    test_get_history(token)
    
    print("\n" + "=" * 60)
    print("✅ API测试完成！")

if __name__ == '__main__':
    main()
