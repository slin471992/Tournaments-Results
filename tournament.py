#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    # delete all rows in matches table
    c.execute("DELETE FROM matches")
    DB.commit()

    # delete all rows in player_matches table
    c.execute("DELETE FROM player_matches")
    DB.commit()

    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    # delete all rows in players table
    c.execute("DELETE FROM players")
    DB.commit()

    # delete all rows in player_matches table
    c.execute("DELETE FROM player_matches")
    DB.commit()

    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("SELECT count(*) as num FROM players")
    row = c.fetchone()
    count = row[0]
    DB.close()
    return int(count)


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.
    (This should be handled by your SQL database schema,
        not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    name = bleach.clean(name)
    c.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    # return all rows from the view player_standings
    c.execute("SELECT * FROM player_standings")
    rows = c.fetchall()
    DB.close()
    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    winner = bleach.clean(winner)
    loser = bleach.clean(loser)
    # insert a new row to the matches table
    c.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)",
              (winner, loser,))

    # get the winner's and loser's previous wins, looses, and matches number
    # winner
    c.execute("""SELECT matches, wins
                 FROM player_matches
                 WHERE player_id = %s""", (int(winner),))
    rec = c.fetchone()
    # if no record
    if rec is None:
        # insert new row to player_matches table
        c.execute("""INSERT INTO player_matches (player_id, matches, wins, looses)
                     VALUES (%s, %s, %s, %s)""",
                  (winner, 1, 1, 0,))
        DB.commit()

    # has record
    else:
        winner_matches = rec[0] + 1
        winner_wins = rec[1] + 1
        # update matches and wins numbers
        c.execute("""UPDATE player_matches
                 SET matches = winner_matches, wins = winner_wins
                 WHERE player_id = %s""", (int(winner),))
        DB.commit()

    # loser
    c.execute("""SELECT matches, looses
                 FROM player_matches
                 WHERE player_id = %s""", (int(loser),))
    rec = c.fetchone()
    # if no record
    if rec is None:
        # insert new row to player_matches table
        c.execute("""INSERT INTO player_matches (player_id, matches, wins, looses)
                     VALUES (%s, %s, %s, %s)""",
                  (loser, 1, 0, 1,))
        DB.commit()

    # has record
    else:
        loser_matches = rec[0] + 1
        loser_looses = rec[1] + 1
        # update matches and looses numbers
        c.execute("""UPDATE player_matches
                 SET matches = loser_matches, looses = loser_looses
                 WHERE player_id = %s""", (int(loser),))
        DB.commit()

    DB.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()

    # count how many players to pair
    c.execute("SELECT COUNT(*) as num FROM player_standings")
    row = c.fetchone()
    num = int(row[0])

    # get players id and name to pair
    c.execute("SELECT id, name FROM player_standings")

    result = []

    i = 0
    # get the query result one by one
    while i < num / 2:
        pairings = []

        row = c.fetchone()
        pairings.append(int(row[0]))
        pairings.append(str(row[1]))

        row = c.fetchone()
        pairings.append(int(row[0]))
        pairings.append(str(row[1]))

        result.append(pairings)
        i += 1

    return result
