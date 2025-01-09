package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
)

type ServerInterface interface {
	StartServing()
}

func GetServer(host, port string, db_client DatabaseClientInterface) ServerInterface {
	return Server{host: host, port: port, db_client: db_client}
}

func (s *Server) get_root(w http.ResponseWriter, r *http.Request) {
	io.WriteString(w, "Pings\n")
}

type User struct {
	UserID     string   `json:"user_id"`
	Username   string   `json:"user_name"`
	TestResult []string `json:"test_result"`
}

func (s Server) post_add_payment(_ http.ResponseWriter, r *http.Request) {
	b, err := io.ReadAll(r.Body)
	if err != nil {
		panic(err)
	}

	user := User{}
	json.Unmarshal(b, &user)

	go s.db_client.AddPayment(user.UserID)
}

func (s Server) post_add_pass(_ http.ResponseWriter, r *http.Request) {
	b, err := io.ReadAll(r.Body)
	if err != nil {
		panic(err)
	}

	user := User{}
	json.Unmarshal(b, &user)

	go s.db_client.AddPass(user.UserID, user.Username, user.TestResult)
}

type Server struct {
	host      string
	port      string
	db_client DatabaseClientInterface
}

// StartServing implements ServerInterface.
func (s Server) StartServing() {
	http.HandleFunc("/", s.get_root)
	http.HandleFunc("/add_payment", s.post_add_payment)
	http.HandleFunc("/add_pass", s.post_add_pass)

	err := http.ListenAndServe(s.host+":"+s.port, nil)
	if errors.Is(err, http.ErrServerClosed) {
		fmt.Println("Server closed")
	} else if err != nil {
		panic(err)
	}
}
