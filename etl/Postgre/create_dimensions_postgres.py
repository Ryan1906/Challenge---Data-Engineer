def create_dimensions_postgres(conn):

    cursor = conn.cursor()

    # Create table for teams
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            team_id SERIAL PRIMARY KEY,
            team_name TEXT UNIQUE
        )
    ''')

    # Create table for stadiums
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stadiums (
            stadium_id SERIAL PRIMARY KEY,
            stadium_name TEXT UNIQUE
        )
    ''')

    # Crear tabla de árbitros
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS referees (
            referee_id SERIAL PRIMARY KEY,
            referee_name TEXT UNIQUE
        )
    ''')

    # Insert the unique data into the dimension tables from the matches table
    cursor.execute('''
        INSERT INTO teams (team_name)
        SELECT DISTINCT home_team_name
        FROM matches
        ON CONFLICT (team_name) DO NOTHING
    ''')

    cursor.execute('''
        INSERT INTO teams (team_name)
        SELECT DISTINCT away_team_name
        FROM matches
        ON CONFLICT (team_name) DO NOTHING
    ''')

    cursor.execute('''
        INSERT INTO stadiums (stadium_name)
        SELECT DISTINCT stadium_name
        FROM matches
        ON CONFLICT (stadium_name) DO NOTHING
    ''')

    cursor.execute('''
        INSERT INTO referees (referee_name)
        SELECT DISTINCT referee_name
        FROM matches
        ON CONFLICT (referee_name) DO NOTHING
    ''')

    conn.commit()
    cursor.close()
    print("Dimensional tables created and populated successfully in PostgreSQL.")