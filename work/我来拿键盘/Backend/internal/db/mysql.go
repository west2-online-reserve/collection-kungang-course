package db

import (
	"database/sql"
	"os"

	_ "github.com/go-sql-driver/mysql"
)

func Open() (*sql.DB, error) {
	// 从环境变量读取数据库配置
	host := os.Getenv("DB_HOST")
	if host == "" {
		host = "127.0.0.1" // 本地开发默认值
	}

	port := os.Getenv("DB_PORT")
	if port == "" {
		port = "3306"
	}

	user := os.Getenv("DB_USER")
	if user == "" {
		user = "root"
	}

	password := os.Getenv("DB_PASSWORD")
	if password == "" {
		password = "123456"
	}

	dbName := os.Getenv("DB_NAME")
	if dbName == "" {
		dbName = "fzu_history" // 默认数据库名
	}

	// 构建 DSN（不包含数据库名，用于创建数据库）
	dsn := user + ":" + password + "@tcp(" + host + ":" + port + ")/"

	// 先连接 MySQL 服务器（不指定数据库）
	tmp, err := sql.Open("mysql", dsn)
	if err != nil {
		return nil, err
	}

	// 创建数据库（如果不存在）
	if _, err = tmp.Exec("CREATE DATABASE IF NOT EXISTS " + dbName + " CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci"); err != nil {
		return nil, err
	}
	_ = tmp.Close()

	// 连接到指定的数据库
	dsn2 := user + ":" + password + "@tcp(" + host + ":" + port + ")/" + dbName + "?parseTime=true&charset=utf8mb4"
	db, err := sql.Open("mysql", dsn2)
	if err != nil {
		return nil, err
	}

	// 测试连接
	if err = db.Ping(); err != nil {
		return nil, err
	}

	return db, nil
}

func Migrate(db *sql.DB) error {
	_, err := db.Exec(`
        CREATE TABLE IF NOT EXISTS account_limit (
            id INT PRIMARY KEY,
            college_min TINYINT NOT NULL,
            college_max TINYINT NOT NULL,
            year_min TINYINT NOT NULL,
            year_max TINYINT NOT NULL,
            major_min TINYINT NOT NULL,
            major_max TINYINT NOT NULL,
            class_min TINYINT NOT NULL,
            class_max TINYINT NOT NULL,
            student_min TINYINT NOT NULL,
            student_max TINYINT NOT NULL,
            require_digit BOOLEAN NOT NULL,
            require_lower BOOLEAN NOT NULL,
            require_upper BOOLEAN NOT NULL,
            require_special BOOLEAN NOT NULL
        )`)
	if err != nil {
		return err
	}
	_, err = db.Exec(`
        CREATE TABLE IF NOT EXISTS users (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            student_id CHAR(9) NOT NULL UNIQUE,
            name VARCHAR(255) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            created_at DATETIME NOT NULL
        )`)
	if err != nil {
		return err
	}
	_, err = db.Exec(`
        CREATE TABLE IF NOT EXISTS avatars (
            id INT PRIMARY KEY AUTO_INCREMENT,
            path VARCHAR(512) NOT NULL
        )`)
	if err != nil {
		return err
	}
	_, err = db.Exec(`
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id BIGINT PRIMARY KEY,
            avatar_id INT NULL,
            avatar_path VARCHAR(512) NULL,
            updated_at DATETIME NOT NULL,
            CONSTRAINT fk_user_settings_user FOREIGN KEY (user_id) REFERENCES users(id),
            CONSTRAINT fk_user_settings_avatar FOREIGN KEY (avatar_id) REFERENCES avatars(id)
        )`)
	return err
}

// Create watermelon scores table
func MigrateWatermelon(db *sql.DB) error {
	_, err := db.Exec(`
        CREATE TABLE IF NOT EXISTS watermelon_scores (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            user_id BIGINT NULL,
            user_name VARCHAR(255) NOT NULL,
            score INT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_score (score DESC),
            INDEX idx_user (user_id),
            INDEX idx_created (created_at)
        )`)
	return err
}

// Create checkin and college comment tables
func MigrateCheckinAndCollege(db *sql.DB) error {
	// 创建打卡评论表
	_, err := db.Exec(`
        CREATE TABLE IF NOT EXISTS checkin_comments (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            location_id INT NOT NULL,
            user_id BIGINT NOT NULL,
            content TEXT NOT NULL,
            image_url VARCHAR(512) NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_checkin_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4`)
	if err != nil {
		return err
	}

	// 创建打卡评论索引 (忽略错误，因为索引可能已存在)
	_, _ = db.Exec(`CREATE INDEX idx_checkin_location ON checkin_comments(location_id)`)
	_, _ = db.Exec(`CREATE INDEX idx_checkin_created ON checkin_comments(created_at)`)

	// 创建学院评论表
	_, err = db.Exec(`
        CREATE TABLE IF NOT EXISTS college_comments (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            college_id INT NOT NULL,
            user_id BIGINT NOT NULL,
            parent_id BIGINT NULL,
            content TEXT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_college_comment_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            CONSTRAINT fk_college_comment_parent FOREIGN KEY (parent_id) REFERENCES college_comments(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4`)
	if err != nil {
		return err
	}

	// 创建学院评论索引
	_, _ = db.Exec(`CREATE INDEX idx_college_comment_college ON college_comments(college_id)`)
	_, _ = db.Exec(`CREATE INDEX idx_college_comment_parent ON college_comments(parent_id)`)
	_, _ = db.Exec(`CREATE INDEX idx_college_comment_created ON college_comments(created_at)`)

	// 创建学院评论点赞表
	_, err = db.Exec(`
        CREATE TABLE IF NOT EXISTS college_comment_likes (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            comment_id BIGINT NOT NULL,
            user_id BIGINT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY unique_like (comment_id, user_id),
            CONSTRAINT fk_comment_like_comment FOREIGN KEY (comment_id) REFERENCES college_comments(id) ON DELETE CASCADE,
            CONSTRAINT fk_comment_like_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4`)
	if err != nil {
		return err
	}

	// 创建点赞表索引
	_, _ = db.Exec(`CREATE INDEX idx_comment_like_comment ON college_comment_likes(comment_id)`)
	return nil
}

func EnsureDefaultAccountLimit(db *sql.DB) error {
	_, err := db.Exec(`INSERT INTO account_limit (
        id, college_min, college_max, year_min, year_max, major_min, major_max, class_min, class_max, student_min, student_max,
        require_digit, require_lower, require_upper, require_special
    ) VALUES (1, 1, 99, 0, 99, 0, 5, 0, 9, 0, 99, 1, 0, 0, 0)
    ON DUPLICATE KEY UPDATE id=id`)
	return err
}

func EnsureDefaultAvatars(db *sql.DB) error {
	_, err := db.Exec(`INSERT INTO avatars (id, path) VALUES (1, '/static/avatar/default1.png') ON DUPLICATE KEY UPDATE id=id`)
	return err
}
