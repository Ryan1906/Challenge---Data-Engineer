from sqlalchemy.orm import Session
from etl.models import Match, NormalizedMatch

def create_normalized_table(session: Session):
   
 
    session.query(NormalizedMatch).delete()

    # Consult ther data from the 'matches' table
    matches = session.query(
        Match.match_id,
        Match.match_date,
        Match.home_team_id,
        Match.away_team_id,
        Match.home_score,
        Match.away_score,
        Match.stadium_id,
        Match.referee_id
    ).all()

    # Insert data into the normalized_matches table
    for match in matches:
        normalized_match = NormalizedMatch(
            match_id=match.match_id,
            match_date=match.match_date,
            home_team_id=match.home_team_id,
            away_team_id=match.away_team_id,
            home_score=match.home_score,
            away_score=match.away_score,
            stadium_id=match.stadium_id,
            referee_id=match.referee_id
        )
        session.add(normalized_match)

    # Confirm the changes to the database
    session.commit()
    print("Normalized table created successfully.")