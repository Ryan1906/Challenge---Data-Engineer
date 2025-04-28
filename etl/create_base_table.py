import pandas as pd
import json
import sqlite3

def create_base_table(json_path):
    # Cargar JSON
    print(f"Loading JSON data from {json_path}...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Crear DataFrame
    df = pd.DataFrame(data)

    # Aplanar columnas anidadas
    df['competition_name'] = df['competition'].apply(lambda x: x.get('competition_name') if isinstance(x, dict) else None)
    df['season_name'] = df['season'].apply(lambda x: x.get('season_name') if isinstance(x, dict) else None)
    df['home_team_name'] = df['home_team'].apply(lambda x: x.get('home_team_name') if isinstance(x, dict) else None)
    df['away_team_name'] = df['away_team'].apply(lambda x: x.get('away_team_name') if isinstance(x, dict) else None)
    df['stadium_name'] = df['stadium'].apply(lambda x: x.get('name') if isinstance(x, dict) else None)
    df['referee_name'] = df['referee'].apply(lambda x: x.get('name') if isinstance(x, dict) else None)

    # Elimina columnas problemáticas originales
    df = df.drop(columns=['competition', 'season', 'home_team', 'away_team', 'stadium', 'referee', 'metadata', 'competition_stage'])

    # Guardar en SQLite
    conn = sqlite3.connect('laliga.db')
    df.to_sql('matches', conn, if_exists='replace', index=False)
    conn.close()
