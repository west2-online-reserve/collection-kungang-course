package handlers

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"strconv"

	"backend/internal/models"
	"backend/internal/repo"
)

// HistoryHandler 处理历史事件相关的请求
type HistoryHandler struct {
	DB *sql.DB
}

// CreateHistoryEvent 创建新的历史事件
func (h HistoryHandler) CreateHistoryEvent(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, models.SimpleResponse{Success: false, Message: "method not allowed"})
		return
	}

	var req models.CreateHistoryEventRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "invalid json"})
		return
	}

	ctx := r.Context()
	eventID, err := repo.CreateHistoryEvent(ctx, h.DB, &req)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "create event failed"})
		return
	}

	response := map[string]interface{}{
		"success": true,
		"message": "event created",
		"id":      eventID,
	}
	writeJSON(w, http.StatusOK, response)
}

// GetAllHistoryEvents 获取所有历史事件
func (h HistoryHandler) GetAllHistoryEvents(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, models.SimpleResponse{Success: false, Message: "method not allowed"})
		return
	}

	ctx := r.Context()
	events, err := repo.GetAllHistoryEvents(ctx, h.DB)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "query events failed"})
		return
	}

	writeJSON(w, http.StatusOK, events)
}

// GetHistoryEventByID 根据ID获取单个历史事件（包含时间轴）
func (h HistoryHandler) GetHistoryEventByID(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, models.SimpleResponse{Success: false, Message: "method not allowed"})
		return
	}

	// 解析URL参数中的ID
	idStr := r.URL.Query().Get("id")
	if idStr == "" {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "missing event id"})
		return
	}

	id, err := strconv.Atoi(idStr)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "invalid event id"})
		return
	}

	ctx := r.Context()
	completeEvent, err := repo.GetCompleteHistoryEvent(ctx, h.DB, id)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "query event failed"})
		return
	}

	if completeEvent == nil {
		writeJSON(w, http.StatusNotFound, models.SimpleResponse{Success: false, Message: "event not found"})
		return
	}

	writeJSON(w, http.StatusOK, completeEvent)
}

// UpdateHistoryEvent 更新历史事件
func (h HistoryHandler) UpdateHistoryEvent(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPut {
		writeJSON(w, http.StatusMethodNotAllowed, models.SimpleResponse{Success: false, Message: "method not allowed"})
		return
	}

	// 解析URL参数中的ID
	idStr := r.URL.Query().Get("id")
	if idStr == "" {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "missing event id"})
		return
	}

	id, err := strconv.Atoi(idStr)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "invalid event id"})
		return
	}

	var req models.CreateHistoryEventRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "invalid json"})
		return
	}

	ctx := r.Context()

	// 先检查事件是否存在
	existingEvent, err := repo.GetHistoryEventByID(ctx, h.DB, id)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "query event failed"})
		return
	}

	if existingEvent == nil {
		writeJSON(w, http.StatusNotFound, models.SimpleResponse{Success: false, Message: "event not found"})
		return
	}

	// 更新事件
	if err := repo.UpdateHistoryEvent(ctx, h.DB, id, &req); err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "update event failed"})
		return
	}

	writeJSON(w, http.StatusOK, models.SimpleResponse{Success: true, Message: "event updated"})
}

// DeleteHistoryEvent 删除历史事件
func (h HistoryHandler) DeleteHistoryEvent(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodDelete {
		writeJSON(w, http.StatusMethodNotAllowed, models.SimpleResponse{Success: false, Message: "method not allowed"})
		return
	}

	// 解析URL参数中的ID
	idStr := r.URL.Query().Get("id")
	if idStr == "" {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "missing event id"})
		return
	}

	id, err := strconv.Atoi(idStr)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "invalid event id"})
		return
	}

	ctx := r.Context()

	// 先检查事件是否存在
	existingEvent, err := repo.GetHistoryEventByID(ctx, h.DB, id)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "query event failed"})
		return
	}

	if existingEvent == nil {
		writeJSON(w, http.StatusNotFound, models.SimpleResponse{Success: false, Message: "event not found"})
		return
	}

	// 删除事件
	if err := repo.DeleteHistoryEvent(ctx, h.DB, id); err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "delete event failed"})
		return
	}

	writeJSON(w, http.StatusOK, models.SimpleResponse{Success: true, Message: "event deleted"})
}

// CreateTimeline 创建新的时间轴条目
func (h HistoryHandler) CreateTimeline(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, models.SimpleResponse{Success: false, Message: "method not allowed"})
		return
	}

	var req models.CreateTimelineRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "invalid json"})
		return
	}

	ctx := r.Context()

	// 先检查关联的事件是否存在
	existingEvent, err := repo.GetHistoryEventByID(ctx, h.DB, req.EventID)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "query event failed"})
		return
	}

	if existingEvent == nil {
		writeJSON(w, http.StatusNotFound, models.SimpleResponse{Success: false, Message: "associated event not found"})
		return
	}

	// 创建时间轴条目
	timelineID, err := repo.CreateTimeline(ctx, h.DB, &req)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "create timeline failed"})
		return
	}

	response := map[string]interface{}{
		"success": true,
		"message": "timeline created",
		"id":      timelineID,
	}
	writeJSON(w, http.StatusOK, response)
}

// GetTimelinesByEventID 根据事件ID获取时间轴条目
func (h HistoryHandler) GetTimelinesByEventID(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, models.SimpleResponse{Success: false, Message: "method not allowed"})
		return
	}

	// 解析URL参数中的事件ID
	eventIDStr := r.URL.Query().Get("eventId")
	if eventIDStr == "" {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "missing event id"})
		return
	}

	eventID, err := strconv.Atoi(eventIDStr)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "invalid event id"})
		return
	}

	ctx := r.Context()

	// 先检查事件是否存在
	existingEvent, err := repo.GetHistoryEventByID(ctx, h.DB, eventID)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "query event failed"})
		return
	}

	if existingEvent == nil {
		writeJSON(w, http.StatusNotFound, models.SimpleResponse{Success: false, Message: "event not found"})
		return
	}

	// 获取时间轴条目
	timelines, err := repo.GetTimelinesByEventID(ctx, h.DB, eventID)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "query timelines failed"})
		return
	}

	writeJSON(w, http.StatusOK, timelines)
}
