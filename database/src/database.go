package main

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v5/pgxpool"
)

type DatabaseClientInterface interface {
	AddPass(user_id, user_name string, test_result []string, done chan bool)
	AddPayment(user_id string, done chan bool)
	GetPassCount(user_id string, ch chan int)
	GetPaymentCount(user_id string, ch chan int)
}

const DATABASE_NAME string = "telegram"
const TABLE_NAME string = "tests"

func GetDBClient(user, password, host, port, db_name, sslmode string) DatabaseClientInterface {
	dbc := DatabaseClient{get_connection_string(user, password, host, port, sslmode)}
	create_and_add_connection_to_database(&dbc)
	return dbc
}

func get_connection_string(user, password, host, port, sslmode string) string {
	return fmt.Sprintf("user=%v password=%v host=%v port=%v sslmode=%v",
		user, password, host, port, sslmode)
}

func create_and_add_connection_to_database(dbc *DatabaseClient) {
	dbpool := dbc.get_pool()

	var exists bool
	err := dbpool.QueryRow(context.Background(),
		"SELECT EXISTS (SELECT FROM pg_database WHERE datname = $1)",
		DATABASE_NAME).Scan(&exists)
	if err != nil {
		panic(err)
	}

	if !exists {
		_, err := dbpool.Exec(context.Background(), "CREATE DATABASE "+DATABASE_NAME)
		if err != nil {
			panic(err)
		}
	}

	dbpool.Close()

	dbc.connection_str += " dbname=" + DATABASE_NAME
	dbpool = dbc.get_pool()
	defer dbpool.Close()

	_, err = dbpool.Exec(context.Background(),
		`CREATE TABLE IF NOT EXISTS `+TABLE_NAME+` (
	       user_id text PRIMARY KEY,
	       user_name varchar(32),
	       test_result varchar(20)[],
	       pass_count integer NOT NULL,
	       payment_count integer NOT NULL
	   )`)
	if err != nil {
		panic(err)
	}
}

type DatabaseClient struct {
	connection_str string
}

// GetPassCount implements DatabaseClientInterface.
func (dbc DatabaseClient) GetPassCount(user_id string, ch chan int) {
	dbpool := dbc.get_pool()
	defer dbpool.Close()

	var row int
	err := dbpool.QueryRow(context.Background(),
		`SELECT pass_count FROM `+TABLE_NAME+
			` WHERE user_id = $1
        `, user_id).Scan(&row)

	ch <- row
	if err != nil {
		panic(err)
	}
}

// GetPaymentCount implements DatabaseClientInterface.
func (dbc DatabaseClient) GetPaymentCount(user_id string, ch chan int) {
	dbpool := dbc.get_pool()
	defer dbpool.Close()

	var row int
	err := dbpool.QueryRow(context.Background(),
		`SELECT payment_count FROM `+TABLE_NAME+
			` WHERE user_id = $1
        `, user_id).Scan(&row)

	ch <- row
	if err != nil {
		panic(err)
	}
}

func (dbc DatabaseClient) get_pool() *pgxpool.Pool {
	dbpool, err := pgxpool.New(context.Background(), dbc.connection_str)
	if err != nil {
		panic(err)
	}
	return dbpool
}

// AddPass implements DatabaseClientInterface.
func (dbc DatabaseClient) AddPass(user_id string, user_name string, test_result []string, done chan bool) {
	dbpool := dbc.get_pool()
	defer dbpool.Close()

	var exists bool
	err := dbpool.QueryRow(context.Background(),
		"SELECT EXISTS(SELECT 1 FROM "+TABLE_NAME+" WHERE user_id=$1)",
		user_id).Scan(&exists)
	if err != nil {
		panic(err)
	}

	if exists {
		_, err = dbpool.Query(context.Background(),
			`UPDATE `+TABLE_NAME+
				` SET user_name = $1, test_result = $2, pass_count = pass_count + 1
                WHERE user_id = $3
            `, user_name, test_result, user_id)
		if err != nil {
			panic(err)
		}
	} else {
		_, err = dbpool.Query(context.Background(),
			`INSERT INTO `+TABLE_NAME+` (user_id, user_name, test_result, pass_count, payment_count)
        VALUES($1, $2, $3, $4, $5)
        `, user_id, user_name, test_result, 1, 0)
		if err != nil {
			panic(err)
		}
	}
	done <- true
}

// AddPayment implements DatabaseClientInterface.
func (dbc DatabaseClient) AddPayment(user_id string, done chan bool) {
	dbpool := dbc.get_pool()
	defer dbpool.Close()

	_, err := dbpool.Query(context.Background(),
		`UPDATE `+TABLE_NAME+
			` SET payment_count = payment_count + 1
            WHERE user_id = $1
        `, user_id)
	if err != nil {
		panic(err)
	}
	done <- true
}
