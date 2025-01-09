package main

import (
	"database/sql"
	"fmt"
	"github.com/joho/godotenv"
	_ "github.com/lib/pq"
	"os"
)

func create_and_connect_to_db(user, password, host, port, db_name, sslmode string) *sql.DB {
	const driver = "postgres"
	connStr := fmt.Sprintf("user=%v password=%v host=%v port=%v sslmode=%v",
		user, password, host, port, sslmode)

	db, err := sql.Open(driver, connStr)
	if err != nil {
		panic(err)
	}

	var exists bool
	err = db.QueryRow("SELECT EXISTS (SELECT FROM pg_database WHERE datname = $1)", db_name).Scan(&exists)
	if err != nil {
		panic(err)
	}

	if !exists {
		_, err = db.Exec("CREATE DATABASE " + db_name)
		if err != nil {
			panic(err)
		}
	}

	db, err = sql.Open(driver, connStr+" dbname="+db_name)
	if err != nil {
		panic(err)
	}

	return db
}

func main() {
	if err := godotenv.Load(); err != nil {
		fmt.Println("No .env file found")
	}

	user := os.Getenv("PG_USER")
	password := os.Getenv("PG_PASSWORD")
	host := os.Getenv("HOST")
	port := os.Getenv("PORT")
	db_name := os.Getenv("DB_NAME")
	ssl := os.Getenv("SSL")

	db := create_and_connect_to_db(user, password, host, port, db_name, ssl)
	defer db.Close()

	row := db.QueryRow("SELECT NOW()")
	var result string
	err := row.Scan(&result)
	if err != nil {
		panic(err)
	}

	fmt.Printf("DATABASE TIME: %s\n", result)
}
