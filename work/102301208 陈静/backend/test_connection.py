#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试华为云 openGauss 数据库连接
"""

import psycopg2
from config import DB_CONFIG

def test_connection():
    """测试数据库连接"""
    print("=" * 60)
    print("测试华为云 openGauss 数据库连接")
    print("=" * 60)
    print("\n连接信息：")
    print(f"  主机: {DB_CONFIG['host']}")
    print(f"  端口: {DB_CONFIG['port']}")
    print(f"  数据库: {DB_CONFIG['database']}")
    print(f"  用户: {DB_CONFIG['user']}")
    print("\n正在连接...")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # 测试查询
        cur.execute("SELECT version()")
        version = cur.fetchone()
        
        print("\n✓ 连接成功！")
        print(f"\n数据库版本: {version[0]}")
        
        # 检查表是否存在
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cur.fetchall()
        
        if tables:
            print("\n已存在的表：")
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print("\n数据库中还没有表，请运行 init_database.py 进行初始化")
        
        cur.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print("\n✗ 连接失败！")
        print(f"\n错误信息: {e}")
        print("\n请检查：")
        print("1. config.py 中的数据库配置是否正确")
        print("2. 华为云安全组是否允许当前IP访问数据库端口")
        print("3. 数据库实例是否正常运行")
        print("4. 用户名和密码是否正确")
        return False
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
        return False

if __name__ == '__main__':
    test_connection()
