def create_normalized_table_postgres(conn):

    cursor = conn.cursor()

    # Crear tabla normalizada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS normalized_matches (
            match_id INTEGER,
            match_date DATE,
            team_id INTEGER,
            score INTEGER,
            stadium_id INTEGER,
            referee_id INTEGER,
            PRIMARY KEY (match_id, team_id),
            FOREIGN KEY (team_id) REFERENCES teams (team_id),
            FOREIGN KEY (stadium_id) REFERENCES stadiums (stadium_id),
            FOREIGN KEY (referee_id) REFERENCES referees (referee_id)
        )
    ''')

    # Insertar datos normalizados para equipos locales
    cursor.execute('''
        INSERT INTO normalized_matches (
            match_id, match_date, team_id, score, stadium_id, referee_id
        )
        SELECT
            match_id,
            match_date,
            home_team_id AS team_id,
            home_score AS score,
            stadium_id,
            referee_id
        FROM matches
        ON CONFLICT (match_id, team_id) DO NOTHING
    ''')

    # Insertar datos normalizados para equipos visitantes
    cursor.execute('''
        INSERT INTO normalized_matches (
            match_id, match_date, team_id, score, stadium_id, referee_id
        )
        SELECT
            match_id,
            match_date,
            away_team_id AS team_id,
            away_score AS score,
            stadium_id,
            referee_id
        FROM matches
        ON CONFLICT (match_id, team_id) DO NOTHING
    ''')

    conn.commit()
    cursor.close()
    print("Normalized table created successfully in PostgreSQL.")