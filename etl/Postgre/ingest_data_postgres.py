def ingest_data_postgres(conn):
    """
    Ingresa datos desde un archivo JSON a la base de datos PostgreSQL.
    :param conn: Conexión activa a la base de datos PostgreSQL.
    """
    import json

    # Leer el archivo JSON
    with open('data/laliga_2009_2010_matches.json', 'r', encoding='utf-8') as file:
        matches = json.load(file)

    cursor = conn.cursor()

    # Crear la tabla base si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            match_id SERIAL PRIMARY KEY,
            match_date DATE,
            kick_off TIME,
            home_team_id INTEGER,
            home_team_name TEXT,
            away_team_id INTEGER,
            away_team_name TEXT,
            home_score INTEGER,
            away_score INTEGER,
            stadium_id INTEGER,
            stadium_name TEXT,
            referee_id INTEGER,
            referee_name TEXT,
            FOREIGN KEY (home_team_id) REFERENCES teams (team_id),
            FOREIGN KEY (away_team_id) REFERENCES teams (team_id),
            FOREIGN KEY (stadium_id) REFERENCES stadiums (stadium_id),
            FOREIGN KEY (referee_id) REFERENCES referees (referee_id)
        )
    ''')

    # Insertar equipos en la tabla de dimensiones
    teams = set()
    for match in matches:
        teams.add(match['home_team']['home_team_name'])
        teams.add(match['away_team']['away_team_name'])

    for team in teams:
        cursor.execute('''
            INSERT INTO teams (team_name)
            VALUES (%s)
            ON CONFLICT (team_name) DO NOTHING
        ''', (team,))

    # Insertar estadios en la tabla de dimensiones
    stadiums = set(match['stadium']['name'] for match in matches)
    for stadium in stadiums:
        cursor.execute('''
            INSERT INTO stadiums (stadium_name)
            VALUES (%s)
            ON CONFLICT (stadium_name) DO NOTHING
        ''', (stadium,))

    # Insertar árbitros en la tabla de dimensiones
    referees = set(match['referee']['name'] for match in matches)
    for referee in referees:
        cursor.execute('''
            INSERT INTO referees (referee_name)
            VALUES (%s)
            ON CONFLICT (referee_name) DO NOTHING
        ''', (referee,))

    # Insertar partidos en la tabla base
    for match in matches:
        cursor.execute('''
            INSERT INTO matches (
                match_id, match_date, kick_off, home_team_id, home_team_name,
                away_team_id, away_team_name, home_score, away_score,
                stadium_id, stadium_name, referee_id, referee_name
            ) VALUES (
                %s, %s, %s,
                (SELECT team_id FROM teams WHERE team_name = %s),
                %s,
                (SELECT team_id FROM teams WHERE team_name = %s),
                %s,
                %s, %s,
                (SELECT stadium_id FROM stadiums WHERE stadium_name = %s),
                %s,
                (SELECT referee_id FROM referees WHERE referee_name = %s),
                %s
            )
            ON CONFLICT (match_id) DO NOTHING
        ''', (
            match['match_id'],
            match['match_date'],
            match['kick_off'],
            match['home_team']['home_team_name'],
            match['home_team']['home_team_name'],
            match['away_team']['away_team_name'],
            match['away_team']['away_team_name'],
            match['home_score'],
            match['away_score'],
            match['stadium']['name'],
            match['stadium']['name'],
            match['referee']['name'],
            match['referee']['name']
        ))

    conn.commit()
    cursor.close()
    print("Datos ingresados correctamente en PostgreSQL.")