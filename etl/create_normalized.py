import sqlite3
from etl.config import DB_PATH
def create_normalized_table(conn):
    """
    Crea una tabla normalizada en la base de datos SQLite.
    :param conn: Conexión activa a la base de datos SQLite.
    """
    cursor = conn.cursor()

    # Crear tabla normalizada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS normalized_matches (
            match_id INTEGER PRIMARY KEY,
            match_date TEXT,
            team_id INTEGER,
            team_name TEXT,
            score INTEGER,
            stadium_id INTEGER,
            stadium_name TEXT,
            referee_id INTEGER,
            referee_name TEXT,
            FOREIGN KEY (team_id) REFERENCES teams (team_id),
            FOREIGN KEY (stadium_id) REFERENCES stadiums (stadium_id),
            FOREIGN KEY (referee_id) REFERENCES referees (referee_id)
        )
    ''')

    # Insertar datos normalizados
    cursor.execute('''
        INSERT OR IGNORE INTO normalized_matches
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
    cursor.execute('''
        INSERT OR IGNORE INTO normalized_matches
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
    print("Tabla normalizada creada correctamente.")