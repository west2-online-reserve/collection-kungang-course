-- 华为云 openGauss 数据库初始化脚本
-- 使用方法：
-- gsql -h <华为云IP> -p <端口> -U <用户名> -W <密码> -d postgres -f init_db.sql

-- 创建数据库（如果不存在）
-- 注意：如果数据库已存在，请注释掉下面这行
CREATE DATABASE stray_animal_db;

-- 连接到新创建的数据库
-- 如果使用 gsql 命令行，请手动执行: \c stray_animal_db

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('管理员', '普通用户')),
    contact VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Animals table
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
);

-- Feed records table
CREATE TABLE IF NOT EXISTS feed_records (
    record_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    animal_id INTEGER NOT NULL REFERENCES animals(animal_id) ON DELETE CASCADE,
    feed_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    food_content VARCHAR(200) NOT NULL
);

-- Health logs table
CREATE TABLE IF NOT EXISTS health_logs (
    log_id SERIAL PRIMARY KEY,
    animal_id INTEGER NOT NULL REFERENCES animals(animal_id) ON DELETE CASCADE,
    action_type VARCHAR(50) NOT NULL CHECK (action_type IN ('绝育', '疫苗', '治疗', '驱虫')),
    cost DECIMAL(10, 2) NOT NULL DEFAULT 0,
    log_date DATE NOT NULL DEFAULT CURRENT_DATE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Adoption applications table
CREATE TABLE IF NOT EXISTS adoption_applications (
    application_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    animal_id INTEGER NOT NULL REFERENCES animals(animal_id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL CHECK (status IN ('待审核', '已通过', '已驳回')),
    apply_reason TEXT NOT NULL,
    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Animal photos table
CREATE TABLE IF NOT EXISTS animal_photos (
    photo_id SERIAL PRIMARY KEY,
    animal_id INTEGER NOT NULL REFERENCES animals(animal_id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    photo_url TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_animals_zone ON animals(zone);
CREATE INDEX idx_animals_status ON animals(status);
CREATE INDEX idx_feed_records_animal ON feed_records(animal_id);
CREATE INDEX idx_health_logs_animal ON health_logs(animal_id);
CREATE INDEX idx_adoption_user ON adoption_applications(user_id);
CREATE INDEX idx_adoption_animal ON adoption_applications(animal_id);
CREATE INDEX idx_animal_photos_animal ON animal_photos(animal_id);
CREATE INDEX idx_animal_photos_user ON animal_photos(user_id);

-- Insert sample admin user (password: admin123)
-- 使用 WHERE NOT EXISTS 避免重复插入
INSERT INTO users (username, password_hash, role, contact) 
SELECT 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', '管理员', 'admin@campus.edu'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'admin');

-- Insert sample data
-- 只在表为空时插入示例数据
INSERT INTO animals (name, species, zone, status, is_sterilized, photo_url, found_date) 
SELECT * FROM (VALUES
    ('小橘', '猫', '图书馆', '流浪中', true, '/images/cat1.jpg', '2024-10-15'),
    ('大黄', '狗', '宿舍A栋', '流浪中', false, '/images/dog1.jpg', '2024-11-20'),
    ('小白', '猫', '食堂', '已领养', true, '/images/cat2.jpg', '2024-09-05'),
    ('花花', '猫', '教学楼', '流浪中', false, '/images/cat3.jpg', '2024-12-01'),
    ('小黑', '猫', '操场', '流浪中', true, '/images/cat4.jpg', '2024-11-10'),
    ('旺财', '狗', '宿舍B栋', '住院治疗', false, '/images/dog2.jpg', '2024-10-25')
) AS v(name, species, zone, status, is_sterilized, photo_url, found_date)
WHERE NOT EXISTS (SELECT 1 FROM animals LIMIT 1);
