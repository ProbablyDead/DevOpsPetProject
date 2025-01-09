package main

import (
	"fmt"
	"github.com/joho/godotenv"
	"os"
)

func main() {
	if err := godotenv.Load(); err != nil {
		fmt.Println("No .env file found")
	}

	user := os.Getenv("DB_USER")
	password := os.Getenv("DB_PASSWORD")
	host := os.Getenv("DB_HOST")
	port := os.Getenv("DB_PORT")
	db_name := os.Getenv("DB_NAME")
	ssl := os.Getenv("DB_SSL")

	db := GetDBClient(user, password, host, port, db_name, ssl)
	go db.AddPass("1", "yakiza", []string{"hello", "hi"})
	go db.AddPayment("1")
	for {
	}
}
