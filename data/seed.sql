CREATE TABLE matches (
    match_id SERIAL PRIMARY KEY,
    match_date DATE NOT NULL,
    home_team VARCHAR(255),
    away_team VARCHAR(255),
    home_score INT,
    away_score INT
);