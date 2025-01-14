package main

import (
	"fmt"
	_ "net/http"
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
	fmt.Println(pass_count)
}

func (rc ReportingClient) AddPayment(user_id string, payment_count int) {
	fmt.Println(payment_count)
}
