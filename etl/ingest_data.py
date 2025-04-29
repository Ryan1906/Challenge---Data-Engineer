import json
from sqlalchemy.orm import Session
from etl.models import Match
from datetime import datetime

def ingest_data(session: Session, file_path: str):
    """
    Ingresa datos desde un archivo JSON a la base de datos en la tabla 'matches'.
    :param session: Sesión activa de SQLAlchemy.
    :param file_path: Ruta del archivo JSON con los datos de los partidos.
    """
    # Leer el archivo JSON
    with open(file_path, "r", encoding="utf-8") as file:
        matches = json.load(file)

    # Insertar datos en la tabla 'matches'
    for match in matches:
        # Convertir match_date y kick_off a objetos datetime
        match_date = datetime.strptime(match["match_date"], "%Y-%m-%d").date()
        kick_off = datetime.strptime(match["kick_off"], "%H:%M:%S.%f").time()

        match_entry = Match(
            match_id=match["match_id"],
            match_date=match_date,
            kick_off=kick_off,
            home_team_id=match["home_team"]["home_team_id"],
            home_team_name=match["home_team"]["home_team_name"],
            away_team_id=match["away_team"]["away_team_id"],
            away_team_name=match["away_team"]["away_team_name"],
            home_score=match["home_score"],
            away_score=match["away_score"],
            stadium_id=match["stadium"]["id"],
            stadium_name=match["stadium"]["name"],
            referee_id=match["referee"]["id"],
            referee_name=match["referee"]["name"]
        )
        session.merge(match_entry)

    # Confirmar los cambios
    session.commit()
    print("Data ingested successfully into the matches table.")