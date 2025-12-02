package service

import (
    "errors"
    "strconv"
    "strings"

    "backend/internal/models"
)

func ValidateStudentID(s string, lim models.AccountLimit) error {
    if len(s) != 9 {
        return errors.New("studentId must be 9 digits")
    }
    for _, ch := range s {
        if ch < '0' || ch > '9' {
            return errors.New("studentId must be digits")
        }
    }
    a := toInt(s[0:2])
    b := toInt(s[2:4])
    c := toInt(s[4:6])
    d := toInt(s[6:7])
    e := toInt(s[7:9])
    if a < lim.CollegeMin || a > lim.CollegeMax {
        return errors.New("invalid college code")
    }
    if b < lim.YearMin || b > lim.YearMax {
        return errors.New("invalid year code")
    }
    if c < lim.MajorMin || c > lim.MajorMax {
        return errors.New("invalid major code")
    }
    if d < lim.ClassMin || d > lim.ClassMax {
        return errors.New("invalid class code")
    }
    if e < lim.StudentMin || e > lim.StudentMax {
        return errors.New("invalid student code")
    }
    return nil
}

func ValidatePassword(p string, lim models.AccountLimit) error {
    if len(p) < 6 {
        return errors.New("password too short")
    }
    hasDigit := false
    hasLower := false
    hasUpper := false
    hasLetter := false
    hasSpecial := false
    for _, ch := range p {
        if ch >= '0' && ch <= '9' {
            hasDigit = true
            continue
        }
        if ch >= 'a' && ch <= 'z' {
            hasLower = true
            hasLetter = true
            continue
        }
        if ch >= 'A' && ch <= 'Z' {
            hasUpper = true
            hasLetter = true
            continue
        }
        hasSpecial = true
    }
    if !(hasDigit && hasLetter) {
        return errors.New("password must contain digit and letter")
    }
    if lim.RequireDigit && !hasDigit {
        return errors.New("password must contain digit")
    }
    if lim.RequireLower && !hasLower {
        return errors.New("password must contain lowercase")
    }
    if lim.RequireUpper && !hasUpper {
        return errors.New("password must contain uppercase")
    }
    if lim.RequireSpecial && !hasSpecial {
        return errors.New("password must contain special")
    }
    return nil
}

func toInt(s string) int {
    v, _ := strconv.Atoi(strings.TrimSpace(s))
    return v
}

