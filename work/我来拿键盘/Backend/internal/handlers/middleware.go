package handlers

import (
	"context"
	"net/http"
	"strings"

	"github.com/golang-jwt/jwt/v5"
)

// TokenMiddleware 验证JWT token的中间件
func TokenMiddleware(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		// 从Authorization header获取token
		authHeader := r.Header.Get("Authorization")
		if authHeader == "" {
			// 如果没有token，仍然允许访问，但不设置用户信息
			next(w, r)
			return
		}
		
		// 检查Bearer前缀
		parts := strings.Split(authHeader, " ")
		if len(parts) != 2 || parts[0] != "Bearer" {
			writeJSON(w, http.StatusUnauthorized, map[string]interface{}{
				"success": false,
				"message": "invalid authorization header format",
			})
			return
		}
		
		tokenString := parts[1]
		
		// 解析和验证token
		token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
			// 验证签名方法
			if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, jwt.ErrSignatureInvalid
			}
			return []byte("your_secret_key_here"), nil
		})
		
		if err != nil || !token.Valid {
			writeJSON(w, http.StatusUnauthorized, map[string]interface{}{
				"success": false,
				"message": "invalid token",
			})
			return
		}
		
		// 从token中提取用户信息
		claims, ok := token.Claims.(jwt.MapClaims)
		if !ok {
			writeJSON(w, http.StatusUnauthorized, map[string]interface{}{
				"success": false,
				"message": "invalid token claims",
			})
			return
		}
		
		studentID, ok := claims["studentId"].(string)
		if !ok {
			writeJSON(w, http.StatusUnauthorized, map[string]interface{}{
				"success": false,
				"message": "invalid studentId in token",
			})
			return
		}
		
		// 将studentId存储到context中
		ctx := context.WithValue(r.Context(), "studentId", studentID)
		next(w, r.WithContext(ctx))
	}
}
