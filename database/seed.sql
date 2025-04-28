CREATE TABLE teams (
    team_id SERIAL PRIMARY KEY,
    team_name TEXT UNIQUE NOT NULL
);

CREATE TABLE stadiums (
    stadium_id SERIAL PRIMARY KEY,
    stadium_name TEXT UNIQUE NOT NULL
);

CREATE TABLE referees (
    referee_id SERIAL PRIMARY KEY,
    referee_name TEXT UNIQUE NOT NULL
);

CREATE TABLE matches (
    match_id SERIAL PRIMARY KEY,
    match_date DATE NOT NULL,
    kick_off TIME NOT NULL,
    home_team_id INTEGER REFERENCES teams(team_id),
    away_team_id INTEGER REFERENCES teams(team_id),
    stadium_id INTEGER REFERENCES stadiums(stadium_id),
    referee_id INTEGER REFERENCES referees(referee_id),
    home_score INTEGER,
    away_score INTEGER
);