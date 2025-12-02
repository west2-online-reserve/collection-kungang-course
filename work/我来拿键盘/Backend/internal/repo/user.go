package repo

import (
	"context"
	"database/sql"
	"time"
)

func UserExists(ctx context.Context, db *sql.DB, studentID, name string) (bool, error) {
	var c int
	err := db.QueryRowContext(ctx, `SELECT COUNT(1) FROM users WHERE student_id=? OR name=?`, studentID, name).Scan(&c)
	return c > 0, err
}

func CreateUser(ctx context.Context, db *sql.DB, studentID, name, passwordHash string, createdAt time.Time) error {
	_, err := db.ExecContext(ctx, `INSERT INTO users (student_id, name, password_hash, created_at) VALUES (?, ?, ?, ?)`, studentID, name, passwordHash, createdAt)
	return err
}

func GetPasswordHash(ctx context.Context, db *sql.DB, studentID string) (string, error) {
	var hash string
	row := db.QueryRowContext(ctx, `SELECT password_hash FROM users WHERE student_id=?`, studentID)
	err := row.Scan(&hash)
	return hash, err
}

func GetUserIDByStudentID(ctx context.Context, db *sql.DB, studentID string) (int64, error) {
    var id int64
    err := db.QueryRowContext(ctx, `SELECT id FROM users WHERE student_id=?`, studentID).Scan(&id)
    return id, err
}

func GetUserNameByID(ctx context.Context, db *sql.DB, userID int64) (string, error) {
    var name string
    err := db.QueryRowContext(ctx, `SELECT name FROM users WHERE id=?`, userID).Scan(&name)
    return name, err
}

func UpsertUserSettingDefaultAvatar(ctx context.Context, db *sql.DB, userID int64, avatarID int) error {
	_, err := db.ExecContext(ctx, `INSERT INTO user_settings (user_id, avatar_id, avatar_path, updated_at) VALUES (?, ?, NULL, ?) ON DUPLICATE KEY UPDATE avatar_id=VALUES(avatar_id), avatar_path=NULL, updated_at=VALUES(updated_at)`, userID, avatarID, time.Now())
	return err
}

func SetUserCustomAvatar(ctx context.Context, db *sql.DB, userID int64, path string) error {
	_, err := db.ExecContext(ctx, `INSERT INTO user_settings (user_id, avatar_id, avatar_path, updated_at) VALUES (?, NULL, ?, ?) ON DUPLICATE KEY UPDATE avatar_id=NULL, avatar_path=VALUES(avatar_path), updated_at=VALUES(updated_at)`, userID, path, time.Now())
	return err
}

// 根据学生ID获取用户信息（包括头像）
func GetUserInfoByStudentID(ctx context.Context, db *sql.DB, studentID string) (string, string, *string, error) {
	var name string
	var avatarPath *string

	// 联合查询users和user_settings表获取用户信息和头像路径
	// 优先使用user_settings中的avatar_path（自定义头像）
	// 如果没有，则使用user_settings关联的avatars表中的path（默认头像）
	row := db.QueryRowContext(ctx, `
		SELECT u.name, COALESCE(us.avatar_path, a.path)
		FROM users u 
		LEFT JOIN user_settings us ON u.id = us.user_id 
		LEFT JOIN avatars a ON us.avatar_id = a.id
		WHERE u.student_id = ?
	`, studentID)

	err := row.Scan(&name, &avatarPath)
	if err != nil {
		return "", "", nil, err
	}

	return studentID, name, avatarPath, nil
}

// 更新用户密码
func UpdateUserPassword(ctx context.Context, db *sql.DB, studentID, newPasswordHash string) error {
	_, err := db.ExecContext(ctx, `UPDATE users SET password_hash = ? WHERE student_id = ?`, newPasswordHash, studentID)
	return err
}

// 更新用户姓名
func UpdateUserName(ctx context.Context, db *sql.DB, studentID, newName string) error {
	_, err := db.ExecContext(ctx, `UPDATE users SET name = ? WHERE student_id = ?`, newName, studentID)
	return err
}
