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

	db_user := os.Getenv("DB_USER")
	db_password := os.Getenv("DB_PASSWORD")
	db_host := os.Getenv("DB_HOST")
	db_port := os.Getenv("DB_PORT")
	db_name := os.Getenv("DB_NAME")
	db_ssl := os.Getenv("DB_SSL")

	reporting_host := os.Getenv("REPORTING_HOST")
	reporting_port := os.Getenv("REPORTING_PORT")

	srv_host := os.Getenv("SRV_HOST")
	srv_port := os.Getenv("SRV_PORT")

	reporting_client := GetReportingClient(reporting_host, reporting_port)
	db := GetDBClient(db_user, db_password, db_host, db_port, db_name, db_ssl)
	svr := GetServer(srv_host, srv_port, db, reporting_client)

	svr.StartServing()
}
