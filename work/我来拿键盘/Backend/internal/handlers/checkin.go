package handlers

import (
	"database/sql"
	"encoding/json"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"time"

	"github.com/gorilla/mux"
	"github.com/redis/go-redis/v9"
)

type CheckinHandler struct {
	DB    *sql.DB
	Redis *redis.Client
}

type CheckinComment struct {
	ID         int64   `json:"id"`
	LocationID int     `json:"locationId"`
	UserID     int64   `json:"userId"`
	UserName   string  `json:"userName"`
	Content    string  `json:"content"`
	ImageURL   string  `json:"imageUrl,omitempty"`
	CreatedAt  string  `json:"createdAt"`
	AvatarURL  *string `json:"avatarUrl,omitempty"`
}

// GetComments 获取某个地点的打卡评论
func (h *CheckinHandler) GetComments(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	locationID, _ := strconv.Atoi(vars["locationId"])

	rows, err := h.DB.Query(`
		SELECT c.id, c.location_id, c.user_id, u.name, c.content, COALESCE(c.image_url, ''), c.created_at, COALESCE(us.avatar_path, a.path)
		FROM checkin_comments c
		JOIN users u ON c.user_id = u.id
		LEFT JOIN user_settings us ON u.id = us.user_id
		LEFT JOIN avatars a ON us.avatar_id = a.id
		WHERE c.location_id = ?
		ORDER BY c.created_at DESC
		LIMIT 50
	`, locationID)

	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var comments []CheckinComment
	for rows.Next() {
		var c CheckinComment
		var avatarPath sql.NullString
		if err := rows.Scan(&c.ID, &c.LocationID, &c.UserID, &c.UserName, &c.Content, &c.ImageURL, &c.CreatedAt, &avatarPath); err != nil {
			continue
		}
		// 设置头像URL
		if avatarPath.Valid && avatarPath.String != "" {
			c.AvatarURL = &avatarPath.String
		} else {
			// 使用默认头像
			defaultAvatar := "/static/avatar/default1.png"
			c.AvatarURL = &defaultAvatar
		}
		comments = append(comments, c)
	}

	if comments == nil {
		comments = []CheckinComment{}
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(comments)
}

// GetDanmaku 获取弹幕（所有打卡的文字内容）
func (h *CheckinHandler) GetDanmaku(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	locationID, _ := strconv.Atoi(vars["locationId"])

	rows, err := h.DB.Query(`
		SELECT c.id, c.content
		FROM checkin_comments c
		WHERE c.location_id = ?
		ORDER BY c.created_at DESC
		LIMIT 20
	`, locationID)

	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var danmaku []map[string]interface{}
	for rows.Next() {
		var id int64
		var content string
		if err := rows.Scan(&id, &content); err != nil {
			continue
		}
		danmaku = append(danmaku, map[string]interface{}{
			"id":      id,
			"content": content,
		})
	}

	if danmaku == nil {
		danmaku = []map[string]interface{}{}
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(danmaku)
}

// SubmitCheckin 提交打卡
func (h *CheckinHandler) SubmitCheckin(w http.ResponseWriter, r *http.Request) {
	// 获取用户ID
	// 获取用户ID
	studentID := r.Context().Value("studentId").(string)

	// 查询用户ID
	var userID int64
	err := h.DB.QueryRow("SELECT id FROM users WHERE student_id = ?", studentID).Scan(&userID)
	if err != nil {
		http.Error(w, "用户不存在", http.StatusUnauthorized)
		return
	}

	// 解析表单
	err = r.ParseMultipartForm(10 << 20) // 10 MB max
	if err != nil {
		http.Error(w, "无法解析表单", http.StatusBadRequest)
		return
	}

	locationID, _ := strconv.Atoi(r.FormValue("locationId"))
	content := r.FormValue("content")

	if content == "" {
		http.Error(w, "打卡内容不能为空", http.StatusBadRequest)
		return
	}

	var imageURL string

	// 处理图片上傳
	file, handler, err := r.FormFile("image")
	if err == nil {
		defer file.Close()

		// 创建上传目录
		uploadDir := "./static/checkin"
		os.MkdirAll(uploadDir, os.ModePerm)

		// 生成唯一文件名
		filename := strconv.FormatInt(time.Now().UnixNano(), 10) + filepath.Ext(handler.Filename)
		filepath := filepath.Join(uploadDir, filename)

		// 保存文件
		dst, err := os.Create(filepath)
		if err != nil {
			log.Printf("创建文件失败: %v", err)
		} else {
			defer dst.Close()
			if _, err := io.Copy(dst, file); err != nil {
				log.Printf("保存文件失败: %v", err)
			} else {
				imageURL = "/static/checkin/" + filename
			}
		}
	}

	// 插入数据库
	var result sql.Result
	if imageURL != "" {
		result, err = h.DB.Exec(`
			INSERT INTO checkin_comments (location_id, user_id, content, image_url, created_at)
			VALUES (?, ?, ?, ?, NOW())
		`, locationID, userID, content, imageURL)
	} else {
		result, err = h.DB.Exec(`
			INSERT INTO checkin_comments (location_id, user_id, content, created_at)
			VALUES (?, ?, ?, NOW())
		`, locationID, userID, content)
	}

	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	id, _ := result.LastInsertId()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"success": true,
		"message": "打卡成功",
		"id":      id,
	})
}
