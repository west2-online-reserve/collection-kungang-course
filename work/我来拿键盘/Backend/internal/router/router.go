package router

import (
	"net/http"
	"strings"

	"backend/internal/handlers"
	
	"github.com/gorilla/mux"
)

// corsMiddleware 处理跨域请求
func corsMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// 设置允许的源
		w.Header().Set("Access-Control-Allow-Origin", "*")
		// 设置允许的HTTP方法
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		// 设置允许的请求头
		w.Header().Set("Access-Control-Allow-Headers", "Origin, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")
		// 允许客户端读取的响应头
		w.Header().Set("Access-Control-Expose-Headers", "Content-Length")
		// 允许发送Cookie
		w.Header().Set("Access-Control-Allow-Credentials", "true")

		// 处理预检请求
		if r.Method == "OPTIONS" {
			w.WriteHeader(http.StatusNoContent)
			return
		}

		// 继续处理请求
		next.ServeHTTP(w, r)
	})
}

// 静态文件服务中间件
func staticFileMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// 检查请求是否匹配静态文件路径
		if strings.HasPrefix(r.URL.Path, "/static/") {
			// 提供静态文件服务
			fileHandler := http.FileServer(http.Dir("."))
			fileHandler.ServeHTTP(w, r)
			return
		}
		// 其他请求继续处理
		next.ServeHTTP(w, r)
	})
}

func New(auth handlers.AuthHandler) http.Handler {
	r := mux.NewRouter()
	
	r.HandleFunc("/api/register", auth.Register)
	r.HandleFunc("/api/login", auth.Login)
	
	user := handlers.UserHandler{Auth: auth}
	r.HandleFunc("/api/user/avatar/update", handlers.TokenMiddleware(user.UpdateAvatar))
	r.HandleFunc("/api/user/avatar/upload", handlers.TokenMiddleware(user.UploadAvatar))
	r.HandleFunc("/api/user/info", handlers.TokenMiddleware(user.GetUserInfo))
	r.HandleFunc("/api/user/password/change", handlers.TokenMiddleware(user.ChangePassword))
	r.HandleFunc("/api/user/name/change", handlers.TokenMiddleware(user.ChangeName))

	// 初始化HistoryHandler并注册相关路由
	history := handlers.HistoryHandler{DB: auth.DB}
	// 历史事件相关路由
	r.HandleFunc("/api/history/events", history.GetAllHistoryEvents)      // 获取所有事件
	r.HandleFunc("/api/history/event", history.GetHistoryEventByID)       // 根据ID获取单个事件
	r.HandleFunc("/api/history/event/create", history.CreateHistoryEvent) // 创建事件
	r.HandleFunc("/api/history/event/update", history.UpdateHistoryEvent) // 更新事件
	r.HandleFunc("/api/history/event/delete", history.DeleteHistoryEvent) // 删除事件
	// 时间轴相关路由
	r.HandleFunc("/api/history/timelines", history.GetTimelinesByEventID) // 根据事件ID获取时间轴
	r.HandleFunc("/api/history/timeline/create", history.CreateTimeline)  // 创建时间轴条目
	
	// 打卡相关路由 - 使用路径参数
	checkin := handlers.CheckinHandler{DB: auth.DB, Redis: auth.Redis}
	r.HandleFunc("/api/checkin/comments/{locationId}", handlers.TokenMiddleware(checkin.GetComments))      // 获取评论
	r.HandleFunc("/api/checkin/danmaku/{locationId}", handlers.TokenMiddleware(checkin.GetDanmaku))       // 获取弹幕
	r.HandleFunc("/api/checkin/submit", handlers.TokenMiddleware(checkin.SubmitCheckin))       // 提交打卡

	// 学院相关路由 - 使用路径参数
	college := handlers.CollegeHandler{DB: auth.DB}
	r.HandleFunc("/api/college/comments/{collegeId}", handlers.TokenMiddleware(college.GetComments))          // 获取学院评论
	r.HandleFunc("/api/college/comment", handlers.TokenMiddleware(college.PostComment)).Methods("POST")       // 发表评论
	r.HandleFunc("/api/college/comment/{commentId}", handlers.TokenMiddleware(college.DeleteComment)).Methods("DELETE") // 删除评论
	r.HandleFunc("/api/college/comment/{commentId}/like", handlers.TokenMiddleware(college.ToggleLike)).Methods("POST") // 点赞/取消点赞


	// 合成大西瓜 游戏路由
	game := handlers.GameHandler{DB: auth.DB}
	r.HandleFunc("/api/game/watermelon/score", handlers.TokenMiddleware(game.SubmitScore)).Methods("POST")
	r.HandleFunc("/api/game/watermelon/leaderboard", game.Leaderboard).Methods("GET")
	r.HandleFunc("/api/game/watermelon/personal", handlers.TokenMiddleware(game.Personal)).Methods("GET")

	// 应用中间件：先应用CORS中间件，再应用静态文件服务中间件
	return corsMiddleware(staticFileMiddleware(r))
}
