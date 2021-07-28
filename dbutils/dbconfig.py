#EVENT_DB_FILEPATH = "../dbase/events.db"
EVENT_DB_FILEPATH = "C:/Users/anna2/PycharmProjects/event_bot/event_bot/dbase/events.db"
NO_TICKETS = "no tickets"

SQL_FOREIGN_KEY = """
PRAGMA foreign_key
"""
SQL_CREATE_EVENTS = """
CREATE TABLE IF NOT EXISTS events(
    id INTEGER PRIMARY KEY UNIQUE,
    event TEXT,
    date TEXT, 
    time TEXT,
    location TEXT,
    places INTEGER NOT NULL
    )
"""

SQL_CREATE_TICKETS = """
CREATE TABLE IF NOT EXISTS tickets(
    id INTEGER PRIMARY KEY UNIQUE,
    event_id INTEGER NOT NULL,
    user TEXT,
    amount INTEGER NOT NULL,
    FOREIGN KEY(event_id) REFERENCES events(id)
    )
"""

SQL_POPULATE_EVENTS = """
INSERT INTO events VALUES (NULL, ?, ?, ?, ?, ?)
"""

SQL_SELECT_TEST = """
SELECT event, date, time, location, places
FROM events
WHERE id = 3 
"""

SQL_SELECT_EVENTS = """
SELECT id, event, date, time, location, places
FROM events
"""

SQL_SELECT_EVENT_BY_ID = """
SELECT id, event, date, time, location, places
FROM events
WHERE id = ?
"""

SQL_UPDATE_EVENT = """
UPDATE events
SET places = ?
WHERE id = ?
"""

SQL_INSERT_TICKET = """
INSERT INTO tickets VALUES (NULL, ?, ?, ?) 
"""

SQL_SELECT_USER_EVENTS = """
SELECT events.event 
FROM tickets 
JOIN events 
ON tickets.event_id = events.id
WHERE tickets.user = ? 
"""

SQL_SELECT_TICKETS = """
SELECT * 
FROM tickets
"""

SQL_CLEAR_TICKETS = """
DELETE FROM tickets
"""