### Intro

This is a test REST API application that allows you to get wallet information on the TRON network.


There are two endpoints:
- `POST /wallet_info data = {"wallet_address": value}`. Use this for request wallet info. Response: `{bandwidth: value, energy: value, balance: value}`
- `GET /wallet_info?page={required=True}&per_page={required=False}`. Get records of requests for wallet information.

### Installation and run

```bash
git clone <url repository>
cd <project path>
```

```
docker compose up -d
docker exec tron_service alembic upgrade head
```

Then go to your browser and open `http://localhost:8000/docs`. Test with open api docs!

### Structure

- `routers/*` is a directory for storing API routes.
- `schemas/*` — Data schemas used for validation and serialization.
- `services/*` — Logic of interaction with the database, tron api and processing of business logic.
- `tests/*` — Tests to cover basic scenarios (using pytest).
- `container.py` - Container dependecies injection.
- `database.py` - Database connection.
- `exceptions.py` - Custom exception.
- `models.py` — Models for the database that define the structure of tables.
- `main.py` - Main file.


### Tests
In the tests directory. There are two types of tests:
- integration
- unit

They require a test database to run. This process can be automated, but in this context it is done using the following operations. Please follow:

```bash
docker exec -it tron_postgres bash
psql -U admin -d tron_db
create database test_db;
```


Then -> `\q` and `ctrl + d`.

Okay! Run tests:
```bash
docker exec tron_service pytest app/tests
```