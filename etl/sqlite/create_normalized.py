import sqlite3
from etl.config import DB_PATH
def create_normalized_table(conn):

    cursor = conn.cursor()

    # Create the normalized_matches table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS normalized_matches (
            match_id INTEGER PRIMARY KEY,
            match_date TEXT,
            home_team_id INTEGER,
            away_team_id INTEGER,
            home_score INTEGER,
            away_score INTEGER,
            stadium_id INTEGER,
            referee_id INTEGER,
            FOREIGN KEY (home_team_id) REFERENCES teams (team_id),
            FOREIGN KEY (away_team_id) REFERENCES teams (team_id),
            FOREIGN KEY (stadium_id) REFERENCES stadiums (stadium_id),
            FOREIGN KEY (referee_id) REFERENCES referees (referee_id)
        )
    ''')

    # Insert data into the normalized_matches table
    cursor.execute('''
        INSERT OR IGNORE INTO normalized_matches (
            match_id, match_date, home_team_id, away_team_id, home_score,
            away_score, stadium_id, referee_id
        )
        SELECT
            m.match_id,
            m.match_date,
            t1.team_id AS home_team_id,
            t2.team_id AS away_team_id,
            m.home_score,
            m.away_score,
            s.stadium_id,
            r.referee_id
        FROM matches m
        LEFT JOIN teams t1 ON m.home_team_name = t1.team_name
        LEFT JOIN teams t2 ON m.away_team_name = t2.team_name
        LEFT JOIN stadiums s ON m.stadium_name = s.stadium_name
        LEFT JOIN referees r ON m.referee_name = r.referee_name
    ''')

    conn.commit()
    cursor.close()
    print("Normalized table created and data inserted successfully.")