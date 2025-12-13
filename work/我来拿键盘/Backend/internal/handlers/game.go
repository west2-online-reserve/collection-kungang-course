package handlers

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"net/http"

	"backend/internal/models"
	"backend/internal/repo"
)

type GameHandler struct {
	DB *sql.DB
}

func (h GameHandler) SubmitScore(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, models.SimpleResponse{Success: false, Message: "method not allowed"})
		return
	}
	var req models.SubmitScoreRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil || req.Score < 0 {
		writeJSON(w, http.StatusBadRequest, models.SimpleResponse{Success: false, Message: "invalid json"})
		return
	}
	ctx := r.Context()
	var userID sql.NullInt64
	// 如果有studentId，则获取对应的用户ID
	if v := ctx.Value("studentId"); v != nil {
		sid, _ := v.(string)
		if sid != "" {
			if dbID, err := repo.GetUserIDByStudentID(ctx, h.DB, sid); err == nil {
				userID = sql.NullInt64{Int64: dbID, Valid: true}
			}
		}
	}
	if err := repo.InsertWatermelonScore(ctx, h.DB, userID, req.Score); err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "insert failed"})
		return
	}
	writeJSON(w, http.StatusOK, models.SimpleResponse{Success: true, Message: "ok"})
}

func (h GameHandler) Leaderboard(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()
	items, err := repo.GetTopWatermelonScores(ctx, h.DB, 20)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, models.SimpleResponse{Success: false, Message: "query failed"})
		return
	}
	var respItems []models.RankItem
	// 这里我们暂时使用userID的字符串表示作为ID显示
	for _, it := range items {
		idStr := ""
		if it.UserID.Valid {
			idStr = fmt.Sprintf("%d", it.UserID.Int64)
		} else {
			idStr = "匿名"
		}
		respItems = append(respItems, models.RankItem{ID: idStr, Score: it.Score, Time: it.Created.Unix()})
	}
	writeJSON(w, http.StatusOK, models.LeaderboardResponse{Success: true, Items: respItems})
}

func (h GameHandler) Personal(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()
	v := ctx.Value("studentId")
	if v == nil {
		writeJSON(w, http.StatusUnauthorized, models.SimpleResponse{Success: false, Message: "unauthorized"})
		return
	}
	sid, _ := v.(string)
	uid, err := repo.GetUserIDByStudentID(ctx, h.DB, sid)
	if err != nil {
		writeJSON(w, http.StatusUnauthorized, models.SimpleResponse{Success: false, Message: "unauthorized"})
		return
	}
	last := 0
	if s, err := repo.GetUserLastScore(ctx, h.DB, uid); err == nil {
		last = s
	}
	top5, _ := repo.GetUserTop5Scores(ctx, h.DB, uid)
	writeJSON(w, http.StatusOK, models.PersonalResponse{Success: true, LastScore: last, Top5: top5})
}
