def create_dimensions_postgres(conn):
    """
    Crear y llenar las tablas de dimensiones en PostgreSQL.
    :param conn: Conexión activa a la base de datos PostgreSQL.
    """
    cursor = conn.cursor()

    # Crear tabla de equipos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            team_id SERIAL PRIMARY KEY,
            team_name TEXT UNIQUE
        )
    ''')

    # Crear tabla de estadios
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

    # Insertar datos únicos en las tablas de dimensiones desde la tabla matches
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
    print("Tablas dimensionales creadas y llenadas correctamente en PostgreSQL.")