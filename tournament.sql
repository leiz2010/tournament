-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
CREATE DATABASE tournament;
\c tournament;

CREATE TYPE RESULT AS ENUM('WIN', 'LOSE', 'TIE', 'BYE');

CREATE TABLE PLAYER(
    PLAYER_ID SERIAL PRIMARY KEY,
    NAME      VARCHAR(200)        NOT NULL
);

CREATE TABLE MATCH(
    MATCH_NUMBER INTEGER,
    PLAYER_ID    INTEGER REFERENCES PLAYER(PLAYER_ID),
    OUTCOME      RESULT,
    PRIMARY KEY(MATCH_NUMBER, PLAYER_ID)
);
