#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
查看数据库当前状态
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG

def show_database_status():
    """显示数据库状态"""
    print("=" * 60)
    print("数据库状态查看")
    print("=" * 60)
    
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        
        print("\n✓ 数据库连接成功！")
        print(f"\n数据库: {DB_CONFIG['database']}")
        print(f"主机: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
        
        # 检查表是否存在
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cur.fetchall()
        
        if not tables:
            print("\n⚠️  数据库中没有表，需要运行 init_database.py 初始化")
            return
        
        print("\n" + "=" * 60)
        print("数据表统计")
        print("=" * 60)
        
        table_names = ['users', 'animals', 'feed_records', 'health_logs', 'adoption_applications']
        
        for table_name in table_names:
            try:
                cur.execute(f"SELECT COUNT(*) as count FROM {table_name}")
                result = cur.fetchone()
                count = result['count'] if result else 0
                print(f"\n{table_name}: {count} 条记录")
                
                # 显示部分数据
                if count > 0 and count <= 5:
                    cur.execute(f"SELECT * FROM {table_name} LIMIT 5")
                    records = cur.fetchall()
                    for record in records:
                        print(f"  - {dict(record)}")
                elif count > 5:
                    cur.execute(f"SELECT * FROM {table_name} LIMIT 3")
                    records = cur.fetchall()
                    for record in records:
                        print(f"  - {dict(record)}")
                    print(f"  ... 还有 {count - 3} 条记录")
                        
            except Exception as e:
                print(f"\n{table_name}: 表不存在或查询失败")
        
        # 检查是否有英文数据
        print("\n" + "=" * 60)
        print("数据语言检查")
        print("=" * 60)
        
        # 检查用户角色
        cur.execute("SELECT DISTINCT role FROM users")
        roles = cur.fetchall()
        print(f"\n用户角色: {[r['role'] for r in roles]}")
        
        # 检查动物状态
        cur.execute("SELECT DISTINCT status FROM animals")
        statuses = cur.fetchall()
        print(f"动物状态: {[s['status'] for s in statuses]}")
        
        # 检查动物物种
        cur.execute("SELECT DISTINCT species FROM animals")
        species = cur.fetchall()
        print(f"动物物种: {[s['species'] for s in species]}")
        
        # 检查是否有英文数据
        has_english = False
        english_roles = ['admin', 'volunteer', 'user']
        english_statuses = ['Stray', 'Adopted', 'Hospitalized', 'Deceased']
        english_species = ['Cat', 'Dog']
        
        for role in roles:
            if role['role'] in english_roles:
                has_english = True
                break
        
        if not has_english:
            for status in statuses:
                if status['status'] in english_statuses:
                    has_english = True
                    break
        
        if not has_english:
            for sp in species:
                if sp['species'] in english_species:
                    has_english = True
                    break
        
        if has_english:
            print("\n⚠️  检测到英文数据，建议运行以下命令清理并重新初始化：")
            print("  python reset_database.py")
        else:
            print("\n✓ 数据已完全中文化")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"\n✗ 查询失败: {e}")

if __name__ == '__main__':
    show_database_status()
