DROP TABLE IF EXISTS matches CASCADE;
DROP TABLE IF EXISTS teams CASCADE;
DROP TABLE IF EXISTS stadiums CASCADE;
DROP TABLE IF EXISTS referees CASCADE;

-- Crear tabla de equipos
CREATE TABLE IF NOT EXISTS teams (
    team_id SERIAL PRIMARY KEY,
    team_name TEXT UNIQUE
);

-- Crear tabla de estadios
CREATE TABLE IF NOT EXISTS stadiums (
    stadium_id SERIAL PRIMARY KEY,
    stadium_name TEXT UNIQUE
);

-- Crear tabla de árbitros
CREATE TABLE IF NOT EXISTS referees (
    referee_id SERIAL PRIMARY KEY,
    referee_name TEXT UNIQUE
);

-- Crear tabla de partidos
CREATE TABLE IF NOT EXISTS matches (
    match_id SERIAL PRIMARY KEY,
    match_date DATE,
    kick_off TIME,
    home_team_id INTEGER,
    home_team_name TEXT,
    away_team_id INTEGER,
    away_team_name TEXT,
    home_score INTEGER,
    away_score INTEGER,
    stadium_id INTEGER,
    stadium_name TEXT,
    referee_id INTEGER,
    referee_name TEXT
);