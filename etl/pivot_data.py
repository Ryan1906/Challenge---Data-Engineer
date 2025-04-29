from sqlalchemy.orm import Session
from etl.models import Match
import pandas as pd

def pivot_data(session: Session):
    """
    Pivota la tabla 'matches' en un formato largo, manteniendo match_id y match_date.
    Transforma los campos home_team, away_team, home_score, away_score en una estructura variable/valor.
    :param session: Sesión activa de SQLAlchemy.
    """
    # Consult the data from the 'matches' table
    matches = session.query(
        Match.match_id,
        Match.match_date,
        Match.home_team_id,
        Match.away_team_id,
        Match.home_score,
        Match.away_score
    ).all()

    # Convert the data to a DataFrame
    data = [
        {
            "match_id": match.match_id,
            "match_date": match.match_date,
            "home_team_id": match.home_team_id,
            "away_team_id": match.away_team_id,
            "home_score": match.home_score,
            "away_score": match.away_score,
        }
        for match in matches
    ]
    df = pd.DataFrame(data)

    # Pivot the data to long format
    pivoted_df = pd.melt(
        df,
        id_vars=["match_id", "match_date"],
        value_vars=["home_team_id", "away_team_id", "home_score", "away_score"],
        var_name="variable",
        value_name="value"
    )



   
    pivoted_df.to_csv("data/laliga_longFormat_data.csv", index=False)
    print("Pivoted data saved to 'laliga_longFormat_data.csv'.")