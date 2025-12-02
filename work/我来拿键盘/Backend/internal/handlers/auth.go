package handlers

import (
	"database/sql"
	"encoding/json"
	"errors"
	"net/http"
	"time"

	"backend/internal/models"
	"backend/internal/repo"
	"backend/internal/service"

	"github.com/golang-jwt/jwt/v5"
	"github.com/redis/go-redis/v9"
	"golang.org/x/crypto/bcrypt"
)

type AuthHandler struct {
	DB    *sql.DB
	Redis *redis.Client
}

func (h AuthHandler) Register(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, models.SimpleResponse{Success: false, Message: "method not allowed"})
		return
	}
	var req models.RegisterRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "invalid json"})
		return
	}
	ctx := r.Context()
	lim, err := repo.LoadAccountLimit(ctx, h.DB)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "load settings failed"})
		return
	}
	if err = service.ValidateStudentID(req.StudentID, lim); err != nil {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: err.Error()})
		return
	}
	if err = service.ValidatePassword(req.Password, lim); err != nil {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: err.Error()})
		return
	}
	exists, err := repo.UserExists(ctx, h.DB, req.StudentID, req.Name)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "query failed"})
		return
	}
	if exists {
		writeJSON(w, http.StatusConflict, models.SimpleResponse{Success: false, Message: "studentId or name already exists"})
		return
	}
	hash, err := bcrypt.GenerateFromPassword([]byte(req.Password), bcrypt.DefaultCost)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "password hash failed"})
		return
	}
	if err = repo.CreateUser(ctx, h.DB, req.StudentID, req.Name, string(hash), time.Now()); err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "insert failed"})
		return
	}
	uid, err := repo.GetUserIDByStudentID(ctx, h.DB, req.StudentID)
	if err == nil {
		_ = repo.UpsertUserSettingDefaultAvatar(ctx, h.DB, uid, 1)
	}
	writeJSON(w, http.StatusOK, models.SimpleResponse{Success: true, Message: "registered"})
}

func (h AuthHandler) Login(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, models.SimpleResponse{Success: false, Message: "method not allowed"})
		return
	}
	var req models.LoginRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "invalid json"})
		return
	}

	ctx := r.Context()

	// 1. 首先验证用户是否存在于数据库中
	// 这是一个关键修复：防止用户被删除后仍然可以通过Redis缓存登录
	_, err := repo.GetUserIDByStudentID(ctx, h.DB, req.StudentID)
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			// 用户不存在，清除可能存在的Redis缓存
			if h.Redis != nil {
				_ = h.Redis.Del(ctx, "user:pwdhash:"+req.StudentID).Err()
			}
			writeJSON(w, http.StatusUnauthorized, models.SimpleResponse{Success: false, Message: "invalid credentials"})
			return
		}
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "query failed"})
		return
	}

	var hash string
	if h.Redis != nil {
		v, _ := h.Redis.Get(ctx, "user:pwdhash:"+req.StudentID).Result()
		if v != "" {
			hash = v
		}
	}
	
	if hash == "" {
		hash, err = repo.GetPasswordHash(ctx, h.DB, req.StudentID)
	}
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			writeJSON(w, http.StatusUnauthorized, models.SimpleResponse{Success: false, Message: "invalid credentials"})
			return
		}
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "query failed"})
		return
	}
	
	err = bcrypt.CompareHashAndPassword([]byte(hash), []byte(req.Password))
	if err != nil {
		writeJSON(w, http.StatusUnauthorized, models.SimpleResponse{Success: false, Message: "invalid credentials"})
		return
	}
	if h.Redis != nil && hash != "" {
		// 设置24小时过期时间，而不是永久缓存
		_ = h.Redis.Set(ctx, "user:pwdhash:"+req.StudentID, hash, 24*time.Hour).Err()
	}

	// 生成JWT token
	token, err := generateToken(req.StudentID)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "token generation failed"})
		return
	}
	writeJSON(w, http.StatusOK, models.LoginResponse{Success: true, Message: "ok", Token: token})
}

// 生成JWT token的函数
func generateToken(studentID string) (string, error) {
	// 创建claims
	claims := jwt.MapClaims{
		"studentId": studentID,
		"exp":       time.Now().Add(time.Hour * 24 * 7).Unix(), // 7天有效期
		"iat":       time.Now().Unix(),
	}

	// 创建token
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)

	// 使用密钥签名token
	// 注意：在生产环境中，密钥应该从环境变量或配置文件中读取
	tokenString, err := token.SignedString([]byte("your_secret_key_here"))
	return tokenString, err
}

func writeJSON(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(v)
}
