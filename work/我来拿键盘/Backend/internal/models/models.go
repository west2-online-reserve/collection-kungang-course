package models

import "time"

type AccountLimit struct {
	ID             int
	CollegeMin     int
	CollegeMax     int
	YearMin        int
	YearMax        int
	MajorMin       int
	MajorMax       int
	ClassMin       int
	ClassMax       int
	StudentMin     int
	StudentMax     int
	RequireDigit   bool
	RequireLower   bool
	RequireUpper   bool
	RequireSpecial bool
}

type User struct {
	ID           int64
	StudentID    string
	Name         string
	PasswordHash string
	CreatedAt    time.Time
}

type RegisterRequest struct {
	StudentID string `json:"studentId"`
	Name      string `json:"name"`
	Password  string `json:"password"`
}

type SimpleResponse struct {
	Success bool   `json:"success"`
	Message string `json:"message"`
}

type LoginRequest struct {
	StudentID string `json:"studentId"`
	Password  string `json:"password"`
}

type LoginResponse struct {
	Success bool   `json:"success"`
	Message string `json:"message"`
	Token   string `json:"token,omitempty"`
}

type Avatar struct {
	ID   int
	Path string
}

type UserSetting struct {
	UserID     int64
	AvatarID   *int
	AvatarPath *string
	UpdatedAt  time.Time
}

// 用户信息响应结构体
type UserInfoResponse struct {
	StudentID string  `json:"studentId"`
	Name      string  `json:"name"`
	AvatarURL *string `json:"avatarUrl"`
}

type UpdateAvatarRequest struct {
	StudentID string `json:"studentId"`
	AvatarID  int    `json:"avatarId"`
}

// 修改密码请求
type ChangePasswordRequest struct {
	CurrentPassword string `json:"currentPassword"`
	NewPassword     string `json:"newPassword"`
}

// 修改姓名请求
type ChangeNameRequest struct {
	CurrentPassword string `json:"currentPassword"`
	NewName         string `json:"newName"`
}

// 历史事件模型
type HistoryEvent struct {
	ID          int       `json:"id"`
	Title       string    `json:"title"`
	Description string    `json:"description"`
	EventDate   time.Time `json:"eventDate"`
	ImagePath   *string   `json:"imagePath"`
	CreatedAt   time.Time `json:"createdAt"`
	UpdatedAt   time.Time `json:"updatedAt"`
}

// 历史时间轴模型
type HistoryTimeline struct {
	ID                  int       `json:"id"`
	EventID             int       `json:"eventId"`
	OrderIndex          int       `json:"orderIndex"`
	TimelineDate        time.Time `json:"timelineDate"`
	TimelineTitle       string    `json:"timelineTitle"`
	TimelineDescription string    `json:"timelineDescription"`
	ImagePath           *string   `json:"imagePath"`
}

// 创建历史事件请求
type CreateHistoryEventRequest struct {
	Title       string    `json:"title" binding:"required"`
	Description string    `json:"description" binding:"required"`
	EventDate   time.Time `json:"eventDate" binding:"required"`
	ImagePath   *string   `json:"imagePath"`
}

// 创建时间轴请求
type CreateTimelineRequest struct {
	EventID             int       `json:"eventId" binding:"required"`
	OrderIndex          int       `json:"orderIndex" binding:"required"`
	TimelineDate        time.Time `json:"timelineDate" binding:"required"`
	TimelineTitle       string    `json:"timelineTitle" binding:"required"`
	TimelineDescription string    `json:"timelineDescription" binding:"required"`
	ImagePath           *string   `json:"imagePath"`
}

// 完整历史事件响应（包含时间轴）
type HistoryEventResponse struct {
	Event    HistoryEvent      `json:"event"`
	Timeline []HistoryTimeline `json:"timeline"`
}
