package repo

import (
    "context"
    "database/sql"

    "backend/internal/models"
)

func LoadAccountLimit(ctx context.Context, db *sql.DB) (models.AccountLimit, error) {
    var a models.AccountLimit
    row := db.QueryRowContext(ctx, `SELECT id, college_min, college_max, year_min, year_max, major_min, major_max, class_min, class_max, student_min, student_max, require_digit, require_lower, require_upper, require_special FROM account_limit WHERE id=1`)
    err := row.Scan(&a.ID, &a.CollegeMin, &a.CollegeMax, &a.YearMin, &a.YearMax, &a.MajorMin, &a.MajorMax, &a.ClassMin, &a.ClassMax, &a.StudentMin, &a.StudentMax, &a.RequireDigit, &a.RequireLower, &a.RequireUpper, &a.RequireSpecial)
    return a, err
}

