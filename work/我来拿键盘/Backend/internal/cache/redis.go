package cache

import (
	"context"
	"os"

	"github.com/redis/go-redis/v9"
)

func Open() (*redis.Client, error) {
	// 从环境变量读取 Redis 地址
	addr := os.Getenv("REDIS_ADDR")
	if addr == "" {
		// 如果设置了 DB_HOST 环境变量（说明在 Docker 环境中）
		// 则使用 Docker 服务名，否则使用本地地址
		dbHost := os.Getenv("DB_HOST")
		if dbHost != "" && dbHost != "127.0.0.1" && dbHost != "localhost" {
			// Docker 环境
			addr = "redis:6379"
		} else {
			// 本地开发环境
			addr = "127.0.0.1:6379"
		}
	}
	
	password := os.Getenv("REDIS_PASSWORD")
	db := 0
	
	client := redis.NewClient(&redis.Options{
		Addr:     addr,
		Password: password,
		DB:       db,
	})
	
	// 测试连接（如果失败返回 nil，不阻止程序启动）
	if err := client.Ping(context.Background()).Err(); err != nil {
		return nil, nil
	}
	
	return client, nil
}
