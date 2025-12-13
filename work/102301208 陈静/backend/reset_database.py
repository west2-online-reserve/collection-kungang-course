#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
重置数据库脚本 - 删除所有表和数据，然后重新初始化
警告：此操作将删除所有数据，请谨慎使用！
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import DB_CONFIG

def reset_database():
    """重置数据库"""
    print("=" * 60)
    print("数据库重置工具")
    print("=" * 60)
    print("\n⚠️  警告：此操作将删除所有表和数据！")
    
    # 确认操作
    confirm = input("\n请输入 'YES' 确认重置数据库: ")
    if confirm != 'YES':
        print("操作已取消")
        return False
    
    print("\n开始连接数据库...")
    
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        print("连接成功！")
        print("\n开始删除所有表...")
        
        # 删除所有表（按依赖关系倒序删除）
        tables = [
            'adoption_applications',
            'health_logs',
            'feed_records',
            'animals',
            'users'
        ]
        
        for table in tables:
            try:
                print(f"删除表 {table}...")
                cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
                print(f"✓ 表 {table} 已删除")
            except Exception as e:
                print(f"✗ 删除表 {table} 失败: {e}")
        
        print("\n✓ 所有表已删除！")
        
        cur.close()
        conn.close()
        
        print("\n现在可以运行 init_database.py 重新初始化数据库")
        return True
        
    except Exception as e:
        print(f"\n✗ 操作失败: {e}")
        return False

def clear_data_only():
    """仅清空数据，保留表结构"""
    print("=" * 60)
    print("清空数据工具")
    print("=" * 60)
    print("\n⚠️  警告：此操作将删除所有数据，但保留表结构！")
    
    # 确认操作
    confirm = input("\n请输入 'YES' 确认清空数据: ")
    if confirm != 'YES':
        print("操作已取消")
        return False
    
    print("\n开始连接数据库...")
    
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        cur = conn.cursor()
        
        print("连接成功！")
        print("\n开始清空数据...")
        
        # 按依赖关系倒序删除数据
        tables = [
            'adoption_applications',
            'health_logs',
            'feed_records',
            'animals',
            'users'
        ]
        
        for table in tables:
            try:
                print(f"清空表 {table}...")
                cur.execute(f"DELETE FROM {table}")
                print(f"✓ 表 {table} 数据已清空")
            except Exception as e:
                print(f"✗ 清空表 {table} 失败: {e}")
        
        conn.commit()
        print("\n✓ 所有数据已清空！")
        
        cur.close()
        conn.close()
        
        print("\n现在可以运行 init_database.py 重新插入初始数据")
        return True
        
    except Exception as e:
        print(f"\n✗ 操作失败: {e}")
        if conn:
            conn.rollback()
        return False

def show_menu():
    """显示菜单"""
    print("\n" + "=" * 60)
    print("数据库管理工具")
    print("=" * 60)
    print("\n请选择操作：")
    print("1. 删除所有表并重置（完全重置）")
    print("2. 仅清空数据（保留表结构）")
    print("3. 退出")
    print("\n" + "=" * 60)
    
    choice = input("\n请输入选项 (1/2/3): ")
    
    if choice == '1':
        if reset_database():
            print("\n✓ 数据库已重置！")
            print("\n下一步：运行以下命令重新初始化")
            print("  python init_database.py")
    elif choice == '2':
        if clear_data_only():
            print("\n✓ 数据已清空！")
            print("\n下一步：运行以下命令重新插入数据")
            print("  python init_database.py")
    elif choice == '3':
        print("退出")
    else:
        print("无效选项")

if __name__ == '__main__':
    show_menu()
