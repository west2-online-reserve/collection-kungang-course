package models

type SubmitScoreRequest struct {
    ID    string `json:"id"`
    Score int    `json:"score"`
}

type RankItem struct {
    ID    string `json:"id"`
    Score int    `json:"score"`
    Time  int64  `json:"time"`
}

type LeaderboardResponse struct {
    Success bool       `json:"success"`
    Items   []RankItem `json:"items"`
}

type PersonalResponse struct {
    Success   bool   `json:"success"`
    LastScore int    `json:"lastScore"`
    Top5      []int  `json:"top5"`
}

