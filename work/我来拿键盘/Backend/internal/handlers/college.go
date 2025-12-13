package handlers

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"strconv"
	"time"

	"github.com/gorilla/mux"
)

type CollegeHandler struct {
	DB *sql.DB
}

type CollegeComment struct {
	ID        int64            `json:"id"`
	CollegeID int              `json:"collegeId"`
	UserID    int64            `json:"userId"`
	UserName  string           `json:"userName"`
	ParentID  *int64           `json:"parentId,omitempty"`
	Content   string           `json:"content"`
	CreatedAt string           `json:"createdAt"`
	LikeCount int              `json:"likeCount"`
	IsLiked   bool             `json:"isLiked"`
	AvatarURL *string          `json:"avatarUrl,omitempty"`
	Replies   []CollegeComment `json:"replies,omitempty"`
}

// GetComments 获取学院的所有评论（包含嵌套结构）
func (h *CollegeHandler) GetComments(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	collegeID, _ := strconv.Atoi(vars["collegeId"])

	// 获取当前用户ID（如果已登录）
	var currentUserID *int64
	studentID := r.Context().Value("studentId")
	if studentID != nil {
		var uid int64
		err := h.DB.QueryRow("SELECT id FROM users WHERE student_id = ?", studentID.(string)).Scan(&uid)
		if err == nil {
			currentUserID = &uid
		}
	}

	// 获取所有顶级评论
	rows, err := h.DB.Query(`
		SELECT c.id, c.college_id, c.user_id, u.name, c.content, c.created_at, COALESCE(us.avatar_path, a.path)
		FROM college_comments c
		JOIN users u ON c.user_id = u.id
		LEFT JOIN user_settings us ON u.id = us.user_id
		LEFT JOIN avatars a ON us.avatar_id = a.id
		WHERE c.college_id = ? AND c.parent_id IS NULL
		ORDER BY c.created_at DESC
		LIMIT 50
	`, collegeID)

	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var comments []CollegeComment
	for rows.Next() {
		var c CollegeComment
		var avatarPath sql.NullString
		if err := rows.Scan(&c.ID, &c.CollegeID, &c.UserID, &c.UserName, &c.Content, &c.CreatedAt, &avatarPath); err != nil {
			continue
		}

		// 获取点赞数
		h.DB.QueryRow("SELECT COUNT(*) FROM college_comment_likes WHERE comment_id = ?", c.ID).Scan(&c.LikeCount)

		// 检查当前用户是否已点赞
		if currentUserID != nil {
			var count int
			h.DB.QueryRow("SELECT COUNT(*) FROM college_comment_likes WHERE comment_id = ? AND user_id = ?", c.ID, *currentUserID).Scan(&count)
			c.IsLiked = count > 0
		}

		// 获取回复
		c.Replies = h.getReplies(c.ID, currentUserID)
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
		comments = []CollegeComment{}
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(comments)
}

// getReplies 递归获取评论的回复
func (h *CollegeHandler) getReplies(parentID int64, currentUserID *int64) []CollegeComment {
	rows, err := h.DB.Query(`
		SELECT c.id, c.college_id, c.user_id, u.name, c.parent_id, c.content, c.created_at, COALESCE(us.avatar_path, a.path)
		FROM college_comments c
		JOIN users u ON c.user_id = u.id
		LEFT JOIN user_settings us ON u.id = us.user_id
		LEFT JOIN avatars a ON us.avatar_id = a.id
		WHERE c.parent_id = ?
		ORDER BY c.created_at ASC
	`, parentID)

	if err != nil {
		return []CollegeComment{}
	}
	defer rows.Close()

	var replies []CollegeComment
	for rows.Next() {
		var c CollegeComment
		var pid sql.NullInt64
		var avatarPath sql.NullString
		if err := rows.Scan(&c.ID, &c.CollegeID, &c.UserID, &c.UserName, &pid, &c.Content, &c.CreatedAt, &avatarPath); err != nil {
			continue
		}
		if pid.Valid {
			c.ParentID = &pid.Int64
		}

		// 获取点赞数
		h.DB.QueryRow("SELECT COUNT(*) FROM college_comment_likes WHERE comment_id = ?", c.ID).Scan(&c.LikeCount)

		// 检查当前用户是否已点赞
		if currentUserID != nil {
			var count int
			h.DB.QueryRow("SELECT COUNT(*) FROM college_comment_likes WHERE comment_id = ? AND user_id = ?", c.ID, *currentUserID).Scan(&count)
			c.IsLiked = count > 0
		}

		// 递归获取回复的回复
		c.Replies = h.getReplies(c.ID, currentUserID)
		// 设置头像URL
		if avatarPath.Valid && avatarPath.String != "" {
			c.AvatarURL = &avatarPath.String
		} else {
			// 使用默认头像
			defaultAvatar := "/static/avatar/default1.png"
			c.AvatarURL = &defaultAvatar
		}
		replies = append(replies, c)
	}

	return replies
}

// PostComment 发表评论或回复
func (h *CollegeHandler) PostComment(w http.ResponseWriter, r *http.Request) {
	// 获取用户ID
	studentID := r.Context().Value("studentId").(string)

	var userID int64
	err := h.DB.QueryRow("SELECT id FROM users WHERE student_id = ?", studentID).Scan(&userID)
	if err != nil {
		http.Error(w, "用户不存在", http.StatusUnauthorized)
		return
	}

	var req struct {
		CollegeID int    `json:"collegeId"`
		ParentID  *int64 `json:"parentId,omitempty"`
		Content   string `json:"content"`
	}

	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "invalid request", http.StatusBadRequest)
		return
	}

	if req.Content == "" {
		http.Error(w, "评论内容不能为空", http.StatusBadRequest)
		return
	}

	var result sql.Result
	if req.ParentID != nil {
		result, err = h.DB.Exec(`
			INSERT INTO college_comments (college_id, user_id, parent_id, content, created_at)
			VALUES (?, ?, ?, ?, ?)
		`, req.CollegeID, userID, req.ParentID, req.Content, time.Now())
	} else {
		result, err = h.DB.Exec(`
			INSERT INTO college_comments (college_id, user_id, content, created_at)
			VALUES (?, ?, ?, ?)
		`, req.CollegeID, userID, req.Content, time.Now())
	}

	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	id, _ := result.LastInsertId()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"success": true,
		"message": "评论成功",
		"id":      id,
	})
}

// ToggleLike 点赞或取消点赞
func (h *CollegeHandler) ToggleLike(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	commentID, _ := strconv.ParseInt(vars["commentId"], 10, 64)

	// 获取用户ID
	studentID := r.Context().Value("studentId").(string)

	var userID int64
	err := h.DB.QueryRow("SELECT id FROM users WHERE student_id = ?", studentID).Scan(&userID)
	if err != nil {
		http.Error(w, "用户不存在", http.StatusUnauthorized)
		return
	}

	// 检查是否已点赞
	var count int
	h.DB.QueryRow("SELECT COUNT(*) FROM college_comment_likes WHERE comment_id = ? AND user_id = ?", commentID, userID).Scan(&count)

	var liked bool
	if count > 0 {
		// 取消点赞
		_, err = h.DB.Exec("DELETE FROM college_comment_likes WHERE comment_id = ? AND user_id = ?", commentID, userID)
		liked = false
	} else {
		// 点赞
		_, err = h.DB.Exec("INSERT INTO college_comment_likes (comment_id, user_id, created_at) VALUES (?, ?, ?)", commentID, userID, time.Now())
		liked = true
	}

	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// 获取最新点赞数
	var likeCount int
	h.DB.QueryRow("SELECT COUNT(*) FROM college_comment_likes WHERE comment_id = ?", commentID).Scan(&likeCount)

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"success":   true,
		"liked":     liked,
		"likeCount": likeCount,
	})
}

// DeleteComment 删除评论（仅限自己的评论）
func (h *CollegeHandler) DeleteComment(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	commentID, _ := strconv.ParseInt(vars["commentId"], 10, 64)

	// 获取用户ID
	studentID := r.Context().Value("studentId").(string)

	var userID int64
	err := h.DB.QueryRow("SELECT id FROM users WHERE student_id = ?", studentID).Scan(&userID)
	if err != nil {
		http.Error(w, "用户不存在", http.StatusUnauthorized)
		return
	}

	// 验证评论所有权
	var commentUserID int64
	err = h.DB.QueryRow("SELECT user_id FROM college_comments WHERE id = ?", commentID).Scan(&commentUserID)
	if err != nil {
		http.Error(w, "评论不存在", http.StatusNotFound)
		return
	}

	if commentUserID != userID {
		http.Error(w, "无权删除此评论", http.StatusForbidden)
		return
	}

	// 删除评论（级联删除回复和点赞）
	_, err = h.DB.Exec("DELETE FROM college_comments WHERE id = ?", commentID)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"success": true,
		"message": "删除成功",
	})
}
