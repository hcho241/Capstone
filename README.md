# Capstone
`docker run --name postgres -e POSTGRES_PASSWORD=<your password here> -p 5432:5432 -d postgres`
`docker build -t accounts_app .` (from solution root)
`docker run --name accounts_app_cont -p 8100:8100 -e PGHOST=<host name> -e PGDATABASE=<database name> PGUSER=<user name> PGPASSWORD=<your password here> -d accounts_app`

Use scripts in `support/data-def.sql` to create database and tables.
