
# Challenge---Data-Engineer

This project implements an ETL (Extract, Transform, Load) pipeline that processes football match data and stores it in a database. The pipeline supports both SQLite and PostgreSQL and can be executed locally or within Docker containers.

---

## Prerequisites

1. **Install Docker and Docker Compose**:
   - [Docker](https://www.docker.com/products/docker-desktop)
   - [Docker Compose](https://docs.docker.com/compose/install/)

2. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Challenge---Data-Engineer.git
   cd Challenge---Data-Engineer
   ```

3. **Create the `.env` file**:
   
   The `.env` file should contain the following environment variables:

   ### AWS S3 Credentials
   ```bash
   AWS_ACCESS_KEY_ID="Aws access"
   AWS_SECRET_ACCESS_KEY="Secret access"
   AWS_REGION="Region"
   S3_BUCKET_NAME="Bucket name"
   DOWNLOAD_PATH=/data/laliga_2009_2010_matches.json
   OBJECT_KEY=laliga_2009_2010_matches.json
   ```

   ### PostgreSQL Configuration
   ```bash
   DB_HOST=postgres
   DB_PORT=5432
   DB_NAME=laliga
   DB_USER=postgres
   DB_PASSWORD=postgres
   ```

   ### Toggle between SQLite and PostgreSQL
   ```bash
   USE_POSTGRES=true
   ```

   - **USE_POSTGRES**:
     - `true`: Use PostgreSQL as the database.
     - `false`: Use SQLite as the database.

---

## Usage Instructions

### 1. Initial Setup
- Ensure the `.env` file is configured correctly.
- If using PostgreSQL, ensure Docker is installed and running.


### 2. Run with SQLite
- Set `USE_POSTGRES=false` in the `.env` file.
- Run the pipeline locally, Ensure to be in the root of the project and use:
  ```bash
  python etl/main.py
  ```

- You can also use Docker to run the pipeline, so you need to start the container:
  ```bash
  docker-compose up --build
  ```


### 3. Run with PostgreSQL
- Set `USE_POSTGRES=true` in the `.env` file.
- Start the containers with Docker Compose:
  ```bash
  docker-compose up --build
  ```

The pipeline will automatically execute within the `etl_container`.

---

## Inspect the Database

### SQLite
- The SQLite database file is located in the `laliga.sqlite` directory.
- You can open it with tools like **DB Browser for SQLite**.

### PostgreSQL
- Connect to the PostgreSQL container:
  ```bash
  docker exec -it postgres_container psql -U postgres -d laliga
  ```
- Use SQL commands to inspect the tables:
  ```sql
  \dt
  SELECT * FROM matches LIMIT 10;
  ```

---

## Additional Notes

### Switching between SQLite and PostgreSQL
- Modify the `USE_POSTGRES` variable in the `.env` file to toggle between databases.

### Resetting the PostgreSQL database
- If you need to reset the PostgreSQL database, run:
  ```bash
  docker-compose down -v
  docker-compose up --build
  ```

### Python Dependencies
- If running the pipeline locally, install the dependencies:
  ```bash
  pip install -r requirements.txt
  ```

