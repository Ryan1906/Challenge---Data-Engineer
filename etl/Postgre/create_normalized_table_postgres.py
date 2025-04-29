def create_normalized_table_postgres(conn):

    cursor = conn.cursor()

    # Create the normalized_matches table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS normalized_matches (
            match_id INTEGER,
            match_date DATE,
            team_id INTEGER,
            team_name TEXT,
            score INTEGER,
            stadium_id INTEGER,
            stadium_name TEXT,
            referee_id INTEGER,
            referee_name TEXT,
            PRIMARY KEY (match_id, team_id),
            FOREIGN KEY (team_id) REFERENCES teams (team_id),
            FOREIGN KEY (stadium_id) REFERENCES stadiums (stadium_id),
            FOREIGN KEY (referee_id) REFERENCES referees (referee_id)
        )
    ''')

    # Insert data for home teams
    cursor.execute('''
        INSERT INTO normalized_matches (
            match_id, match_date, team_id, team_name, score,
            stadium_id, stadium_name, referee_id, referee_name
        )
        SELECT
            match_id,
            match_date,
            home_team_id AS team_id,
            home_team_name AS team_name,
            home_score AS score,
            stadium_id,
            stadium_name,
            referee_id,
            referee_name
        FROM matches
    ''')

    # Insert data for away teams
    cursor.execute('''
        INSERT INTO normalized_matches (
            match_id, match_date, team_id, team_name, score,
            stadium_id, stadium_name, referee_id, referee_name
        )
        SELECT
            match_id,
            match_date,
            away_team_id AS team_id,
            away_team_name AS team_name,
            away_score AS score,
            stadium_id,
            stadium_name,
            referee_id,
            referee_name
        FROM matches
    ''')

    conn.commit()
    cursor.close()
    print("Normalized table created and data inserted successfully in PostgreSQL.")