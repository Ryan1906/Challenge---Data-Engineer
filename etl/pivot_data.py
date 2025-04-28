import pandas as pd
import sqlite3
from etl.config import DB_PATH
import os

def pivot_data():
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect(DB_PATH)
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

    # Cerrar la conexión
    conn.close()