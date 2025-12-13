-- 清理旧数据的 SQL 脚本
-- 使用方法：gsql -h <IP> -p <端口> -U <用户名> -d stray_animal_db -f clean_old_data.sql

-- 方案1：删除所有表（完全重置）
-- 取消下面的注释来执行完全重置
/*
DROP TABLE IF EXISTS adoption_applications CASCADE;
DROP TABLE IF EXISTS health_logs CASCADE;
DROP TABLE IF EXISTS feed_records CASCADE;
DROP TABLE IF EXISTS animals CASCADE;
DROP TABLE IF EXISTS users CASCADE;
*/

-- 方案2：仅删除数据，保留表结构（推荐）
-- 按依赖关系倒序删除
DELETE FROM adoption_applications;
DELETE FROM health_logs;
DELETE FROM feed_records;
DELETE FROM animals;
DELETE FROM users;

-- 重置序列（自增ID）
ALTER SEQUENCE users_user_id_seq RESTART WITH 1;
ALTER SEQUENCE animals_animal_id_seq RESTART WITH 1;
ALTER SEQUENCE feed_records_record_id_seq RESTART WITH 1;
ALTER SEQUENCE health_logs_log_id_seq RESTART WITH 1;
ALTER SEQUENCE adoption_applications_application_id_seq RESTART WITH 1;

-- 显示清理结果
SELECT '数据已清空，表结构保留' AS status;
