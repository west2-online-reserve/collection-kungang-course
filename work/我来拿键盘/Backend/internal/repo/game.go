package repo

import (
	"context"
	"database/sql"
	"time"
)

type WatermelonScore struct {
	ID      int64
	UserID  sql.NullInt64
	Score   int
	Created time.Time
}

func InsertWatermelonScore(ctx context.Context, db *sql.DB, userID sql.NullInt64, score int) error {
	_, err := db.ExecContext(ctx, `INSERT INTO watermelon_scores (user_id, score, created_at) VALUES (?, ?, NOW())`, userID, score)
	return err
}

func GetTopWatermelonScores(ctx context.Context, db *sql.DB, limit int) ([]WatermelonScore, error) {
	rows, err := db.QueryContext(ctx, `SELECT id, user_id, score, created_at FROM watermelon_scores ORDER BY score DESC, created_at ASC LIMIT ?`, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []WatermelonScore
	for rows.Next() {
		var s WatermelonScore
		if err := rows.Scan(&s.ID, &s.UserID, &s.Score, &s.Created); err != nil {
			return nil, err
		}
		list = append(list, s)
	}
	return list, rows.Err()
}

func GetUserTop5Scores(ctx context.Context, db *sql.DB, userID int64) ([]int, error) {
	rows, err := db.QueryContext(ctx, `SELECT score FROM watermelon_scores WHERE user_id = ? ORDER BY score DESC, created_at ASC LIMIT 5`, userID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var scores []int
	for rows.Next() {
		var s int
		if err := rows.Scan(&s); err != nil {
			return nil, err
		}
		scores = append(scores, s)
	}
	return scores, rows.Err()
}

func GetUserLastScore(ctx context.Context, db *sql.DB, userID int64) (int, error) {
	row := db.QueryRowContext(ctx, `SELECT score FROM watermelon_scores WHERE user_id = ? ORDER BY created_at DESC LIMIT 1`, userID)
	var s int
	if err := row.Scan(&s); err != nil {
		return 0, err
	}
	return s, nil
}
