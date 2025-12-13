package main

import (
	"fmt"
	"net/http"

	"backend/internal/cache"
	"backend/internal/db"
	"backend/internal/handlers"
	"backend/internal/router"
)

func main() {
	fmt.Println("Starting backend server...")
	
	fmt.Println("Connecting to database...")
	database, err := db.Open()
	if err != nil {
		fmt.Printf("Database connection error: %v\n", err)
		panic(err)
	}
	fmt.Println("Database connected successfully")
	
	fmt.Println("Running database migrations...")
	if err = db.Migrate(database); err != nil {
		fmt.Printf("Migration error: %v\n", err)
		panic(err)
	}
	if err = db.MigrateWatermelon(database); err != nil {
		fmt.Printf("Watermelon migration error: %v\n", err)
		panic(err)
	}
	if err = db.MigrateCheckinAndCollege(database); err != nil {
		fmt.Printf("Checkin and College migration error: %v\n", err)
		panic(err)
	}
	fmt.Println("Migrations completed successfully")
	
	fmt.Println("Ensuring default account limits...")
	if err = db.EnsureDefaultAccountLimit(database); err != nil {
		fmt.Printf("Default account limit error: %v\n", err)
		panic(err)
	}
	
	fmt.Println("Ensuring default avatars...")
	if err = db.EnsureDefaultAvatars(database); err != nil {
		fmt.Printf("Default avatars error: %v\n", err)
		panic(err)
	}
	
	fmt.Println("Connecting to Redis...")
	redisClient, redisErr := cache.Open()
	if redisErr != nil {
		fmt.Printf("Redis connection error: %v\n", err)
	}
	fmt.Println("Redis connection attempt completed")
	
	auth := handlers.AuthHandler{DB: database, Redis: redisClient}
	
	fmt.Println("Setting up router...")
	handler := router.New(auth)
	
	fmt.Println("Starting server on port 8080...")
	if err := http.ListenAndServe(":8080", handler); err != nil {
		fmt.Printf("Server error: %v\n", err)
		panic(err)
	}
}
