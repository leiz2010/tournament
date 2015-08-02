#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM MATCH;")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM PLAYER;")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM PLAYER;")
    rows = c.fetchall()
    count = len(rows)
    conn.close()
    return count

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO PLAYER(NAME) VALUES(%s)", (name,))
    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT P.PLAYER_ID, P.NAME, " \
                "SUM(CASE WHEN M.OUTCOME = 'WIN' THEN 1 ELSE 0 END) AS WINS, " \
                "COUNT(M.MATCH_NUMBER) AS MATCHES " \
                "FROM PLAYER AS P LEFT JOIN MATCH AS M " \
                "ON P.PLAYER_ID = M.PLAYER_ID " \
                "GROUP BY P.PLAYER_ID, P.NAME " \
                "ORDER BY WINS DESC;")
    results = c.fetchall()
    conn.close()
    return results

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    # get the max MATCH_NUMBER then increase it's value by 1
    # to be used for this match
    c.execute("SELECT MAX(MATCH_NUMBER) FROM MATCH")
    max_id = c.fetchone()[0]
    if max_id is None:
        max_id = 0
    max_id += 1
    c.execute("INSERT INTO MATCH (MATCH_NUMBER, PLAYER_ID, OUTCOME) " \
            "VALUES  (%s, %s, %s)", (max_id,  winner, 'WIN', ))
    c.execute("INSERT INTO MATCH (MATCH_NUMBER, PLAYER_ID, OUTCOME) " \
            "VALUES (%s, %s, %s)", (max_id, loser, 'LOSE',))
    conn.commit()
    conn.close()

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
    results = []
    # get player statndings
    player_standings = playerStandings()
    # loop through all players to create pairs
    c = 0
    while c < len(player_standings):
        c += 1
        # only pair when c is event
        if c % 2 != 0:
            pid1 = player_standings[c-1][0]
            pname1 = player_standings[c-1][1]
            pid2 = player_standings[c][0]
            pname2 = player_standings[c][1]
            pair = (pid1, pname1, pid2, pname2)
            results.append(pair)
    return results
