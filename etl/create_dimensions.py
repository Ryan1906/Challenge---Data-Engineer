from sqlalchemy.orm import Session
from etl.models import Team, Stadium, Referee, Match

def get_or_create(session: Session, model, **kwargs):
    
    instance = session.query(model).filter_by(**kwargs).first()
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        session.refresh(instance)
    return instance

def create_dimensions(session: Session):
    
    # Insert teams
    for match in session.query(Match).all():
        get_or_create(session, Team, team_id=match.home_team_id, team_name=match.home_team_name)
        get_or_create(session, Team, team_id=match.away_team_id, team_name=match.away_team_name)

    # Insert stadiums
    for match in session.query(Match).all():
        get_or_create(session, Stadium, stadium_id=match.stadium_id, stadium_name=match.stadium_name)

    # Insert referees
    for match in session.query(Match).all():
        get_or_create(session, Referee, referee_id=match.referee_id, referee_name=match.referee_name)

    session.commit()
    print("Dimensions created successfully.")