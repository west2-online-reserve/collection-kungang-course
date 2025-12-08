#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
华为云 openGauss 数据库初始化脚本
使用 Python 连接华为云数据库并执行初始化
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import DB_CONFIG
import hashlib

def hash_password(password):
    """密码哈希函数"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_database():
    """初始化数据库"""
    print("开始连接华为云 openGauss 数据库...")
    
    # 首先连接到默认数据库
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database='postgres'  # 先连接到默认数据库
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        print("连接成功！")
        
        # 检查数据库是否存在
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_CONFIG['database'],))
        exists = cur.fetchone()
        
        if not exists:
            print(f"创建数据库 {DB_CONFIG['database']}...")
            cur.execute(f"CREATE DATABASE {DB_CONFIG['database']}")
            print("数据库创建成功！")
        else:
            print(f"数据库 {DB_CONFIG['database']} 已存在")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"连接数据库失败: {e}")
        print("\n请检查：")
        print("1. config.py 中的数据库配置是否正确")
        print("2. 华为云安全组是否允许当前IP访问数据库端口")
        print("3. 数据库用户名和密码是否正确")
        return False
    
    # 连接到目标数据库并创建表
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        cur = conn.cursor()
        
        print("\n开始创建数据表...")
        
        # 创建 users 表
        print("创建 users 表...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL CHECK (role IN ('管理员', '普通用户')),
                contact VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建 animals 表
        print("创建 animals 表...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS animals (
                animal_id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                species VARCHAR(50) NOT NULL CHECK (species IN ('猫', '狗')),
                zone VARCHAR(100) NOT NULL,
                status VARCHAR(50) NOT NULL CHECK (status IN ('流浪中', '已领养', '住院治疗', '已死亡')),
                is_sterilized BOOLEAN DEFAULT FALSE,
                photo_url TEXT,
                found_date DATE DEFAULT CURRENT_DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建 feed_records 表
        print("创建 feed_records 表...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS feed_records (
                record_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                animal_id INTEGER NOT NULL REFERENCES animals(animal_id) ON DELETE CASCADE,
                feed_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                food_content VARCHAR(200) NOT NULL
            )
        """)
        
        # 创建 health_logs 表
        print("创建 health_logs 表...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS health_logs (
                log_id SERIAL PRIMARY KEY,
                animal_id INTEGER NOT NULL REFERENCES animals(animal_id) ON DELETE CASCADE,
                action_type VARCHAR(50) NOT NULL CHECK (action_type IN ('绝育', '疫苗', '治疗', '驱虫')),
                cost DECIMAL(10, 2) NOT NULL DEFAULT 0,
                log_date DATE NOT NULL DEFAULT CURRENT_DATE,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建 adoption_applications 表
        print("创建 adoption_applications 表...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS adoption_applications (
                application_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                animal_id INTEGER NOT NULL REFERENCES animals(animal_id) ON DELETE CASCADE,
                status VARCHAR(20) NOT NULL CHECK (status IN ('待审核', '已通过', '已驳回')),
                apply_reason TEXT NOT NULL,
                create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建 animal_photos 表
        print("创建 animal_photos 表...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS animal_photos (
                photo_id SERIAL PRIMARY KEY,
                animal_id INTEGER NOT NULL REFERENCES animals(animal_id) ON DELETE CASCADE,
                user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                photo_url TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建索引
        print("创建索引...")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_animals_zone ON animals(zone)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_animals_status ON animals(status)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_feed_records_animal ON feed_records(animal_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_health_logs_animal ON health_logs(animal_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_adoption_user ON adoption_applications(user_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_adoption_animal ON adoption_applications(animal_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_animal_photos_animal ON animal_photos(animal_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_animal_photos_user ON animal_photos(user_id)")
        
        # 插入默认管理员账号
        print("创建默认管理员账号...")
        admin_password_hash = hash_password('admin123')
        cur.execute("""
            INSERT INTO users (username, password_hash, role, contact) 
            SELECT %s, %s, %s, %s
            WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = %s)
        """, ('admin', admin_password_hash, '管理员', 'admin@campus.edu', 'admin'))
        
        # 插入示例数据
        print("插入示例数据...")
        cur.execute("""
            INSERT INTO animals (name, species, zone, status, is_sterilized, photo_url, found_date) 
            SELECT * FROM (VALUES
                ('小橘', '猫', '图书馆', '流浪中', true, '/images/cat1.jpg', '2024-10-15'),
                ('大黄', '狗', '宿舍A栋', '流浪中', false, '/images/dog1.jpg', '2024-11-20'),
                ('小白', '猫', '食堂', '已领养', true, '/images/cat2.jpg', '2024-09-05'),
                ('花花', '猫', '教学楼', '流浪中', false, '/images/cat3.jpg', '2024-12-01'),
                ('小黑', '猫', '操场', '流浪中', true, '/images/cat4.jpg', '2024-11-10'),
                ('旺财', '狗', '宿舍B栋', '住院治疗', false, '/images/dog2.jpg', '2024-10-25')
            ) AS v(name, species, zone, status, is_sterilized, photo_url, found_date)
            WHERE NOT EXISTS (SELECT 1 FROM animals LIMIT 1)
        """)
        
        conn.commit()
        print("\n✓ 数据库初始化完成！")
        print("\n默认管理员账号：")
        print("  用户名: admin")
        print("  密码: admin123")
        print("\n请及时修改默认密码！")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"\n✗ 初始化失败: {e}")
        if conn:
            conn.rollback()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("华为云 openGauss 数据库初始化工具")
    print("=" * 60)
    print("\n请确保已在 config.py 中配置正确的数据库连接信息\n")
    
    success = init_database()
    
    if success:
        print("\n数据库初始化成功！现在可以启动后端服务了。")
    else:
        print("\n数据库初始化失败，请检查配置和网络连接。")
