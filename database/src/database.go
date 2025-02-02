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

const DEFAULT_DATABASE_NAME string = "postgres"
const TABLE_NAME string = "tests"

func GetDBClient(user, password, host, port, db_name, sslmode string) DatabaseClientInterface {
	dbc := DatabaseClient{user, password, host, port, DEFAULT_DATABASE_NAME, sslmode, ""}
	dbc.update_connection_string()
	create_and_add_connection_to_database(&dbc, db_name)
	return dbc
}

func create_and_add_connection_to_database(dbc *DatabaseClient, db_name string) {
	dbpool := dbc.get_pool()

	var exists bool
	err := dbpool.QueryRow(context.Background(),
		"SELECT EXISTS (SELECT FROM pg_database WHERE datname = $1)",
		db_name).Scan(&exists)
	if err != nil {
		panic(err)
	}

	if !exists {
		_, err := dbpool.Exec(context.Background(), "CREATE DATABASE "+db_name)
		if err != nil {
			panic(err)
		}
	}

	dbpool.Close()

	dbc.db_name = db_name
	dbc.update_connection_string()
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
	user,
	password,
	host,
	port,
	db_name,
	sslmode,
	connection_str string
}

func (dbc *DatabaseClient) update_connection_string() {
	dbc.connection_str = fmt.Sprintf("user=%v password=%v host=%v port=%v database=%v sslmode=%v",
		dbc.user, dbc.password, dbc.host, dbc.port, dbc.db_name, dbc.sslmode)
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
	if err != nil {
		panic(err)
	}

	ch <- row
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
	if err != nil {
		ch <- -1
		return
	}

	ch <- row
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

	d := true
	defer func() { done <- d }()

	var exists bool
	err := dbpool.QueryRow(context.Background(),
		"SELECT EXISTS(SELECT 1 FROM "+TABLE_NAME+" WHERE user_id=$1)",
		user_id).Scan(&exists)
	if err != nil {
		d = false
		return
	}

	if exists {
		_, err = dbpool.Query(context.Background(),
			`UPDATE `+TABLE_NAME+
				` SET user_name = $1, test_result = $2, pass_count = pass_count + 1
                WHERE user_id = $3
            `, user_name, test_result, user_id)
		if err != nil {
			d = false
			return
		}
	} else {
		_, err = dbpool.Query(context.Background(),
			`INSERT INTO `+TABLE_NAME+` (user_id, user_name, test_result, pass_count, payment_count)
        VALUES($1, $2, $3, $4, $5)
        `, user_id, user_name, test_result, 1, 0)
		if err != nil {
			d = false
			return
		}
	}
}

// AddPayment implements DatabaseClientInterface.
func (dbc DatabaseClient) AddPayment(user_id string, done chan bool) {
	dbpool := dbc.get_pool()
	defer dbpool.Close()

	d := true
	defer func() { done <- d }()

	_, err := dbpool.Query(context.Background(),
		`UPDATE `+TABLE_NAME+
			` SET payment_count = payment_count + 1
            WHERE user_id = $1
        `, user_id)
	if err != nil {
		d = false
	}
}
