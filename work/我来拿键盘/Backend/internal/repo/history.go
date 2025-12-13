package repo

import (
	"context"
	"database/sql"
	"time"

	"backend/internal/models"
)

// 创建历史事件
func CreateHistoryEvent(ctx context.Context, db *sql.DB, event *models.CreateHistoryEventRequest) (int, error) {
	var id int
	err := db.QueryRowContext(
		ctx,
		`INSERT INTO history_events (title, description, event_date, image_path) VALUES (?, ?, ?, ?) RETURNING id`,
		event.Title,
		event.Description,
		event.EventDate,
		event.ImagePath,
	).Scan(&id)
	return id, err
}

// 获取所有历史事件（按日期倒序）
func GetAllHistoryEvents(ctx context.Context, db *sql.DB) ([]models.HistoryEvent, error) {
	rows, err := db.QueryContext(
		ctx,
		`SELECT id, title, description, event_date, image_path, created_at, updated_at FROM history_events ORDER BY event_date DESC`,
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var events []models.HistoryEvent
	for rows.Next() {
		var event models.HistoryEvent
		var imagePath sql.NullString
		err := rows.Scan(
			&event.ID,
			&event.Title,
			&event.Description,
			&event.EventDate,
			&imagePath,
			&event.CreatedAt,
			&event.UpdatedAt,
		)
		if err != nil {
			return nil, err
		}
		if imagePath.Valid {
			val := imagePath.String
			event.ImagePath = &val
		}
		events = append(events, event)
	}

	return events, rows.Err()
}

// 根据ID获取历史事件
func GetHistoryEventByID(ctx context.Context, db *sql.DB, id int) (*models.HistoryEvent, error) {
	var event models.HistoryEvent
	var imagePath sql.NullString

	err := db.QueryRowContext(
		ctx,
		`SELECT id, title, description, event_date, image_path, created_at, updated_at FROM history_events WHERE id = ?`,
		id,
	).Scan(
		&event.ID,
		&event.Title,
		&event.Description,
		&event.EventDate,
		&imagePath,
		&event.CreatedAt,
		&event.UpdatedAt,
	)

	if err == sql.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}

	if imagePath.Valid {
		val := imagePath.String
		event.ImagePath = &val
	}

	return &event, nil
}

// 更新历史事件
func UpdateHistoryEvent(ctx context.Context, db *sql.DB, id int, event *models.CreateHistoryEventRequest) error {
	_, err := db.ExecContext(
		ctx,
		`UPDATE history_events SET title = ?, description = ?, event_date = ?, image_path = ?, updated_at = ? WHERE id = ?`,
		event.Title,
		event.Description,
		event.EventDate,
		event.ImagePath,
		time.Now(),
		id,
	)
	return err
}

// 删除历史事件
func DeleteHistoryEvent(ctx context.Context, db *sql.DB, id int) error {
	_, err := db.ExecContext(ctx, `DELETE FROM history_events WHERE id = ?`, id)
	return err
}

// 创建时间轴条目
func CreateTimeline(ctx context.Context, db *sql.DB, timeline *models.CreateTimelineRequest) (int, error) {
	var id int
	err := db.QueryRowContext(
		ctx,
		`INSERT INTO history_timeline (event_id, order_index, timeline_date, timeline_title, timeline_description, image_path) VALUES (?, ?, ?, ?, ?, ?) RETURNING id`,
		timeline.EventID,
		timeline.OrderIndex,
		timeline.TimelineDate,
		timeline.TimelineTitle,
		timeline.TimelineDescription,
		timeline.ImagePath,
	).Scan(&id)
	return id, err
}

// 根据事件ID获取时间轴（按order_index排序）
func GetTimelinesByEventID(ctx context.Context, db *sql.DB, eventID int) ([]models.HistoryTimeline, error) {
	rows, err := db.QueryContext(
		ctx,
		`SELECT id, event_id, order_index, timeline_date, timeline_title, timeline_description, image_path FROM history_timeline WHERE event_id = ? ORDER BY order_index ASC`,
		eventID,
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var timelines []models.HistoryTimeline
	for rows.Next() {
		var timeline models.HistoryTimeline
		var imagePath sql.NullString
		err := rows.Scan(
			&timeline.ID,
			&timeline.EventID,
			&timeline.OrderIndex,
			&timeline.TimelineDate,
			&timeline.TimelineTitle,
			&timeline.TimelineDescription,
			&imagePath,
		)
		if err != nil {
			return nil, err
		}
		if imagePath.Valid {
			val := imagePath.String
			timeline.ImagePath = &val
		}
		timelines = append(timelines, timeline)
	}

	return timelines, rows.Err()
}

// 获取完整的历史事件（包含时间轴）
func GetCompleteHistoryEvent(ctx context.Context, db *sql.DB, id int) (*models.HistoryEventResponse, error) {
	// 获取事件基本信息
	event, err := GetHistoryEventByID(ctx, db, id)
	if err != nil {
		return nil, err
	}
	if event == nil {
		return nil, nil
	}

	// 获取关联的时间轴
	timelines, err := GetTimelinesByEventID(ctx, db, id)
	if err != nil {
		return nil, err
	}

	return &models.HistoryEventResponse{
		Event:    *event,
		Timeline: timelines,
	}, nil
}
