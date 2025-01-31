package main

func main() {
	conf := GetConfig()

	reporting_client := GetReportingClient(
		conf.Reporting.host,
		conf.Reporting.port,
	)

	db := GetDBClient(
		conf.Database.user,
		conf.Database.password,
		conf.Database.host,
		conf.Database.port,
		conf.Database.dbName,
		conf.Database.ssl,
	)

	svr := GetServer(
		conf.Server.host,
		conf.Server.port,
		db,
		reporting_client,
	)

	svr.StartServing()
}
