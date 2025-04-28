import pandas as pd
import os

def pivot_data(conn):
    """
    Pivotar los datos de la tabla 'matches' y guardarlos en un archivo CSV.
    :param conn: Conexión activa a la base de datos SQLite.
    """
    # Consulta para obtener los datos
    query = "SELECT match_id, match_date, home_team_name, away_team_name, home_score, away_score FROM matches"
    df = pd.read_sql_query(query, conn)

    # Pivotar los datos
    df_long = df.melt(
        id_vars=['match_id', 'match_date'], 
        value_vars=['home_team_name', 'away_team_name', 'home_score', 'away_score'],
        var_name='variable', 
        value_name='value'
    )

    # Guardar el resultado en un archivo CSV
    output_path = os.path.join('data', 'matches_long_format.csv')
    df_long.to_csv(output_path, index=False)
    print(f"Datos pivotados guardados en: {output_path}")