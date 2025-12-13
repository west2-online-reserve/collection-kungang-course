package handlers

import (
	"encoding/json"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"time"

	"backend/internal/models"
	"backend/internal/repo"

	"golang.org/x/crypto/bcrypt"
)

type UserHandler struct {
	Auth AuthHandler
}

func (h UserHandler) UpdateAvatar(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, models.SimpleResponse{Success: false, Message: "method not allowed"})
		return
	}
	var req models.UpdateAvatarRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "invalid json"})
		return
	}
	ctx := r.Context()
	uid, err := repo.GetUserIDByStudentID(ctx, h.Auth.DB, req.StudentID)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "user not found"})
		return
	}
	if err = repo.UpsertUserSettingDefaultAvatar(ctx, h.Auth.DB, uid, req.AvatarID); err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "update failed"})
		return
	}
	writeJSON(w, http.StatusOK, models.SimpleResponse{Success: true, Message: "updated"})
}

func (h UserHandler) UploadAvatar(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, models.SimpleResponse{Success: false, Message: "method not allowed"})
		return
	}
	if err := r.ParseMultipartForm(10 << 20); err != nil {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "invalid form"})
		return
	}
	// 从context中获取studentId（从token中解析的）
	studentID, exists := r.Context().Value("studentId").(string)
	if !exists {
		writeJSON(w, http.StatusUnauthorized, models.SimpleResponse{Success: false, Message: "unauthorized"})
		return
	}
	file, header, err := r.FormFile("avatar")
	if err != nil {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "file missing"})
		return
	}
	defer file.Close()
	ctx := r.Context()
	uid, err := repo.GetUserIDByStudentID(ctx, h.Auth.DB, studentID)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "user not found"})
		return
	}
	// 使用正确的avatar存储路径
	avatarDir := "g:/Codes/Web/kungang-course/WorkOne/Backend/static/avatar"
	_ = os.MkdirAll(avatarDir, 0755)
	ext := filepath.Ext(header.Filename)
	if ext == "" {
		ext = ".png"
	}
	filename := studentID + "_" + time.Now().Format("20060102150405") + ext
	dst := filepath.Join(avatarDir, filename)
	out, err := os.Create(dst)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "save failed"})
		return
	}
	defer out.Close()
	if _, err = io.Copy(out, file); err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "save failed"})
		return
	}
	// 存储相对路径用于URL访问
	relativePath := "/static/avatar/" + filename
	if err = repo.SetUserCustomAvatar(ctx, h.Auth.DB, uid, relativePath); err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "update failed"})
		return
	}
	// 返回完整的头像URL
	writeJSON(w, http.StatusOK, struct {
		Success   bool   `json:"success"`
		Message   string `json:"message"`
		AvatarURL string `json:"avatarUrl"`
	}{
		Success:   true,
		Message:   "uploaded successfully",
		AvatarURL: relativePath,
	})
}

func (h UserHandler) GetUserInfo(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, models.SimpleResponse{Success: false, Message: "method not allowed"})
		return
	}

	// 优先从context中获取studentId（从token中解析的）
	studentID, exists := r.Context().Value("studentId").(string)

	// 如果context中没有，则从query参数获取
	if !exists {
		studentID = r.URL.Query().Get("studentId")
		if studentID == "" {
			writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "studentId is required"})
			return
		}
	}
	ctx := r.Context()
	studentID, name, avatarPath, err := repo.GetUserInfoByStudentID(ctx, h.Auth.DB, studentID)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "user not found"})
		return
	}

	// 创建响应对象
	response := models.UserInfoResponse{
		StudentID: studentID,
		Name:      name,
		AvatarURL: avatarPath,
	}

	// 如果没有头像路径，使用默认头像
	defaultAvatar := "/static/avatar/default1.png"
	if avatarPath == nil {
		response.AvatarURL = &defaultAvatar
	}

	writeJSON(w, http.StatusOK, response)
}

// 修改密码处理函数
func (h UserHandler) ChangePassword(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, models.SimpleResponse{Success: false, Message: "method not allowed"})
		return
	}
	var req models.ChangePasswordRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "invalid json"})
		return
	}
	// 从context中获取studentId
	studentID, exists := r.Context().Value("studentId").(string)
	if !exists {
		writeJSON(w, http.StatusUnauthorized, models.SimpleResponse{Success: false, Message: "unauthorized"})
		return
	}
	// 验证当前密码
	hashedPassword, err := repo.GetPasswordHash(r.Context(), h.Auth.DB, studentID)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "failed to get password hash"})
		return
	}
	if err := bcrypt.CompareHashAndPassword([]byte(hashedPassword), []byte(req.CurrentPassword)); err != nil {
		writeJSON(w, http.StatusUnauthorized, models.SimpleResponse{Success: false, Message: "current password is incorrect"})
		return
	}
	// 对新密码进行哈希处理
	newHashedPassword, err := bcrypt.GenerateFromPassword([]byte(req.NewPassword), bcrypt.DefaultCost)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "failed to hash new password"})
		return
	}
	// 更新密码
	if err := repo.UpdateUserPassword(r.Context(), h.Auth.DB, studentID, string(newHashedPassword)); err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "failed to update password"})
		return
	}

	// 清除 Redis 中的密码缓存
	if h.Auth.Redis != nil {
		_ = h.Auth.Redis.Del(r.Context(), "user:pwdhash:"+studentID).Err()
	}

	writeJSON(w, http.StatusOK, models.SimpleResponse{Success: true, Message: "password updated successfully"})
}

// 修改姓名处理函数
func (h UserHandler) ChangeName(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, models.SimpleResponse{Success: false, Message: "method not allowed"})
		return
	}
	var req models.ChangeNameRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "invalid json"})
		return
	}
	// 从context中获取studentId
	studentID, exists := r.Context().Value("studentId").(string)
	if !exists {
		writeJSON(w, http.StatusUnauthorized, models.SimpleResponse{Success: false, Message: "unauthorized"})
		return
	}
	// 验证当前密码
	hashedPassword, err := repo.GetPasswordHash(r.Context(), h.Auth.DB, studentID)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "failed to get password hash"})
		return
	}
	if err := bcrypt.CompareHashAndPassword([]byte(hashedPassword), []byte(req.CurrentPassword)); err != nil {
		writeJSON(w, http.StatusUnauthorized, models.SimpleResponse{Success: false, Message: "current password is incorrect"})
		return
	}
	// 更新姓名
	if err := repo.UpdateUserName(r.Context(), h.Auth.DB, studentID, req.NewName); err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "failed to update name"})
		return
	}
	writeJSON(w, http.StatusOK, models.SimpleResponse{Success: true, Message: "name updated successfully"})
}
