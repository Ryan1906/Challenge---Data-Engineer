import sqlite3
from etl.config import DB_PATH
def create_dimensions(conn):
    """
    Crea las tablas dimensionales en la base de datos SQLite.
    :param conn: Conexión activa a la base de datos SQLite.
    """
    cursor = conn.cursor()

    # Create team table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            team_id INTEGER PRIMARY KEY,
            team_name TEXT UNIQUE
        )
    ''')

    # Create stadium table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stadiums (
            stadium_id INTEGER PRIMARY KEY,
            stadium_name TEXT UNIQUE
        )
    ''')

    # Create referee table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS referees (
            referee_id INTEGER PRIMARY KEY,
            referee_name TEXT UNIQUE
        )
    ''')

    # Insert unique data into the dimension tables from the matches table
    cursor.execute('INSERT OR IGNORE INTO teams SELECT DISTINCT home_team_id, home_team_name FROM matches')
    cursor.execute('INSERT OR IGNORE INTO teams SELECT DISTINCT away_team_id, away_team_name FROM matches')
    cursor.execute('INSERT OR IGNORE INTO stadiums SELECT DISTINCT stadium_id, stadium_name FROM matches')
    cursor.execute('INSERT OR IGNORE INTO referees SELECT DISTINCT referee_id, referee_name FROM matches')

    conn.commit()
    cursor.close()
    print("Dimensional tables created and populated successfully in SQLite.")