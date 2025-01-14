package main

import (
	"bytes"
	"encoding/json"
	"net/http"
)

type ReportingClientInterface interface {
	AddPass(user_id, user_name string, test_result []string, pass_count int)
	AddPayment(user_id string, payment_count int)
}

func GetReportingClient(reporting_host, reporting_port string) ReportingClientInterface {
	return ReportingClient{"http://" + reporting_host + ":" + reporting_port}
}

type ReportingClient struct {
	connection_string string
}

func (rc ReportingClient) AddPass(user_id, user_name string, test_result []string, pass_count int) {
	data, err := json.Marshal(
		struct {
			UserID    string   `json:"user_id"`
			UserName  string   `json:"user_name"`
			Test      []string `json:"test"`
			PassCount int      `json:"pass_count"`
		}{
			user_id,
			user_name,
			test_result,
			pass_count,
		},
	)
	if err != nil {
		panic(err)
	}
	r := bytes.NewReader(data)
	_, err = http.Post(rc.connection_string+"/add_pass", "application/json", r)
	if err != nil {
		panic(err)
	}
}

func (rc ReportingClient) AddPayment(user_id string, payment_count int) {
	data, err := json.Marshal(
		struct {
			UserID       string `json:"user_id"`
			PaymentCount int    `json:"payment_count"`
		}{
			user_id,
			payment_count,
		},
	)
	if err != nil {
		panic(err)
	}
	r := bytes.NewReader(data)
	_, err = http.Post(rc.connection_string+"/add_payment", "application/json", r)
	if err != nil {
		panic(err)
	}
}
