import sqlite3
from etl.config import DB_PATH

def create_normalized_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Crear tabla normalizada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS normalized_matches (
            match_id INTEGER PRIMARY KEY,
            match_date TEXT,
            kick_off TEXT,
            home_team_id INTEGER,
            away_team_id INTEGER,
            home_score INTEGER,
            away_score INTEGER,
            stadium_id INTEGER,
            referee_id INTEGER,
            FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
            FOREIGN KEY (away_team_id) REFERENCES teams(team_id),
            FOREIGN KEY (stadium_id) REFERENCES stadiums(stadium_id),
            FOREIGN KEY (referee_id) REFERENCES referees(referee_id)
        )
    ''')

    # Insertar datos normalizados
    cursor.execute('''
        INSERT OR IGNORE INTO normalized_matches (
            match_id, match_date, kick_off, home_team_id, away_team_id,
            home_score, away_score, stadium_id, referee_id
        )
        SELECT
            m.match_id, m.match_date, m.kick_off,
            t1.team_id AS home_team_id,
            t2.team_id AS away_team_id,
            m.home_score, m.away_score,
            s.stadium_id, r.referee_id
        FROM matches m
        JOIN teams t1 ON m.home_team_id = t1.team_id
        JOIN teams t2 ON m.away_team_id = t2.team_id
        JOIN stadiums s ON m.stadium_id = s.stadium_id
        JOIN referees r ON m.referee_id = r.referee_id
    ''')

    conn.commit()
    conn.close()
    print("Tabla normalizada creada correctamente.")