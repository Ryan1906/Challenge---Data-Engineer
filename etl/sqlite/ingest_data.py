import json
import sqlite3
from etl.config import DB_PATH
def ingest_data(conn):
    """
    Ingresa datos desde un archivo JSON a la base de datos.
    :param conn: Conexión activa a la base de datos SQLite.
    """
    import json

    # Leer el archivo JSON
    with open('data/laliga_2009_2010_matches.json', 'r', encoding='utf-8') as file:
        matches = json.load(file)

    cursor = conn.cursor()

    # Create the base table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            match_id INTEGER PRIMARY KEY,
            match_date TEXT,
            kick_off TEXT,
            home_team_id INTEGER,
            home_team_name TEXT,
            away_team_id INTEGER,
            away_team_name TEXT,
            home_score INTEGER,
            away_score INTEGER,
            stadium_id INTEGER,
            stadium_name TEXT,
            referee_id INTEGER,
            referee_name TEXT
        )
    ''')

    # Insert teams into the dimension table
    for match in matches:
        cursor.execute('''
            INSERT OR IGNORE INTO matches (
                match_id, match_date, kick_off, home_team_id, home_team_name,
                away_team_id, away_team_name, home_score, away_score,
                stadium_id, stadium_name, referee_id, referee_name
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            match['match_id'],
            match['match_date'],
            match['kick_off'],
            match['home_team']['home_team_id'],
            match['home_team']['home_team_name'],
            match['away_team']['away_team_id'],
            match['away_team']['away_team_name'],
            match['home_score'],
            match['away_score'],
            match['stadium']['id'],
            match['stadium']['name'],
            match['referee']['id'],
            match['referee']['name']
        ))

    conn.commit()
    cursor.close()
    print("Data ingested successfully into the matches table.")