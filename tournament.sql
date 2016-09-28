-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- connet to the tournament database
\c tournament

-- create players table to store players' id as primary key and players' name
CREATE TABLE players (id serial,
                      name text,
                      PRIMARY KEY(id));

-- create matches table to store matches' id as primary key
-- and winner, loser of each match
CREATE TABLE matches (id serial,
                      winner integer references players(id),
                      loser integer references players(id),
                      PRIMARY KEY(id));

-- create player_matches table to store players' wins and looses
CREATE TABLE player_matches(player_id integer references players(id),
                            matches integer,
                            wins integer,
                            looses integer,
                            PRIMARY KEY(player_id));

-- create player_standings view to store players' id, name, number of matches and wins
CREATE VIEW player_standings AS
SELECT players.id, players.name, COALESCE(player_matches.wins, 0) as wins, COALESCE(player_matches.matches, 0) as matches
FROM players LEFT JOIN player_matches ON players.id = player_matches.player_id
ORDER BY player_matches.wins DESC