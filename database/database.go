package main

import (
	"database/sql"
	"fmt"
	_ "github.com/lib/pq"
)

type DatabaseClientInterface interface {
	Ping() bool
}

func CreateConnection(user, password, host, port, db_name, sslmode string) DatabaseClientInterface {
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
		_, err := db.Exec("CREATE DATABASE " + db_name)
		if err != nil {
			panic(err)
		}
	}

	db, err = sql.Open(driver, connStr+" dbname="+db_name)
	if err != nil {
		panic(err)
	}

	_, err = db.Exec(`CREATE TABLE IF NOT EXISTS tests (
        user_id text PRIMARY KEY,
        user_name char(32),
        last_test_result char(20)[],
        pass_count integer NOT NULL,
        payment_count integer NOT NULL
    )`)
	if err != nil {
		panic(err)
	}

	return DatabaseClient{db}
}

type DatabaseClient struct {
	db *sql.DB
}

func (dbc DatabaseClient) Ping() bool {
	err := dbc.db.Ping()
	if err != nil {
		return false
	}
	return true
}
