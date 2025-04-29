import pandas as pd
import os

def pivot_data(conn):

    # Consult to obtain the data
    query = "SELECT match_id, match_date, home_team_name, away_team_name, home_score, away_score FROM matches"
    df = pd.read_sql_query(query, conn)

    # Pivot the data to long format
    df_long = df.melt(
        id_vars=['match_id', 'match_date'], 
        value_vars=['home_team_name', 'away_team_name', 'home_score', 'away_score'],
        var_name='variable', 
        value_name='value'
    )

    # Save the pivoted data to a CSV file
    output_path = os.path.join('data', 'matches_long_format.csv')
    df_long.to_csv(output_path, index=False)
    print(f"Pivoted data in: {output_path}")