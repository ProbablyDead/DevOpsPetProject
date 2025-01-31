package main

import (
	"fmt"
	"github.com/joho/godotenv"
	"os"
)

type DatabaseConfig struct {
	user     string
	password string
	host     string
	port     string
	dbName   string
	ssl      string
}

type ServerConfig struct {
	host, port string
}

type ReportigConfig struct {
	host, port string
}

type Config struct {
	Server    ServerConfig
	Database  DatabaseConfig
	Reporting ReportigConfig
}

func GetConfig() *Config {
	if err := godotenv.Load(); err != nil {
		fmt.Println("No .env file found")
	}

	return &Config{
		Server: ServerConfig{
			host: getEnv("SRV_HOST", ""),
			port: getEnv("SRV_PORT", "80"),
		},
		Database: DatabaseConfig{
			user:     getEnv("DB_USER", ""),
			password: getEnv("DB_PASSWORD", ""),
			host:     getEnv("DB_HOST", ""),
			port:     getEnv("DB_PORT", "5432"),
			dbName:   getEnv("DB_NAME", "telegram"),
			ssl:      getEnv("DB_SSL", "disabled"),
		},
		Reporting: ReportigConfig{
			host: getEnv("REPORTING_HOST", ""),
			port: getEnv("REPORTING_PORT", "80"),
		},
	}
}

func getEnv(key string, defaultVal string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}

	return defaultVal
}
