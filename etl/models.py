from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from etl.database import Base

class Team(Base):
    __tablename__ = "teams"
    team_id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String, unique=True, index=True)

class Stadium(Base):
    __tablename__ = "stadiums"
    stadium_id = Column(Integer, primary_key=True, index=True)
    stadium_name = Column(String, unique=True, index=True)

class Referee(Base):
    __tablename__ = "referees"
    referee_id = Column(Integer, primary_key=True, index=True)
    referee_name = Column(String, unique=True, index=True)

class Match(Base):
    __tablename__ = "matches"
    match_id = Column(Integer, primary_key=True, index=True)
    match_date = Column(Date)
    kick_off = Column(Time)
    home_team_id = Column(Integer)  
    home_team_name = Column(String)
    away_team_id = Column(Integer) 
    away_team_name = Column(String)
    home_score = Column(Integer)
    away_score = Column(Integer)
    stadium_id = Column(Integer) 
    stadium_name = Column(String)
    referee_id = Column(Integer)  
    referee_name = Column(String)

class NormalizedMatch(Base):
    __tablename__ = "normalized_matches"
    match_id = Column(Integer, primary_key=True)
    match_date = Column(Date)
    home_team_id = Column(Integer, ForeignKey("teams.team_id"))
    away_team_id = Column(Integer, ForeignKey("teams.team_id"))
    home_score = Column(Integer)
    away_score = Column(Integer)
    stadium_id = Column(Integer, ForeignKey("stadiums.stadium_id"))
    referee_id = Column(Integer, ForeignKey("referees.referee_id"))