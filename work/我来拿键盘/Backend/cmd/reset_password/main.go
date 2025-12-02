package main

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/go-sql-driver/mysql"
	"golang.org/x/crypto/bcrypt"
)

func main() {
	// 连接数据库
	dsn := "root:123456@tcp(localhost:3306)/fzu_history?parseTime=true"
	db, err := sql.Open("mysql", dsn)
	if err != nil {
		log.Fatal("Failed to connect to database:", err)
	}
	defer db.Close()

	// 测试连接
	if err := db.Ping(); err != nil {
		log.Fatal("Failed to ping database:", err)
	}

	fmt.Println("Connected to database successfully")

	// 要重置的用户信息
	studentID := "102400232"
	newPassword := "Test123456"

	// 生成密码哈希
	hash, err := bcrypt.GenerateFromPassword([]byte(newPassword), bcrypt.DefaultCost)
	if err != nil {
		log.Fatal("Failed to generate password hash:", err)
	}

	// 更新数据库
	result, err := db.Exec("UPDATE users SET password_hash = ? WHERE student_id = ?", string(hash), studentID)
	if err != nil {
		log.Fatal("Failed to update password:", err)
	}

	rowsAffected, _ := result.RowsAffected()
	if rowsAffected == 0 {
		fmt.Printf("Warning: No user found with student_id = %s\n", studentID)
	} else {
		fmt.Printf("✅ Password reset successfully for student_id = %s\n", studentID)
		fmt.Printf("   New password: %s\n", newPassword)
	}

	// 验证密码
	var storedHash string
	err = db.QueryRow("SELECT password_hash FROM users WHERE student_id = ?", studentID).Scan(&storedHash)
	if err != nil {
		log.Fatal("Failed to verify password:", err)
	}

	err = bcrypt.CompareHashAndPassword([]byte(storedHash), []byte(newPassword))
	if err == nil {
		fmt.Println("✅ Password verification successful!")
	} else {
		fmt.Println("❌ Password verification failed!")
	}
}
