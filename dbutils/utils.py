import sqlite3
import event_bot.dbutils.dbconfig as cfg
from event_bot.data.Events import Event
from event_bot.data.Tickets import Ticket


def get_events():
    conn = sqlite3.connect(cfg.EVENT_DB_FILEPATH)
    cursor = conn.cursor()

    cursor.execute(cfg.SQL_SELECT_EVENTS)
    result = cursor.fetchall()

    events = []
    for t in result:
        events.append(Event.create_from_tuple(t))
    return events


def get_event_by_id(id):
    conn = sqlite3.connect(cfg.EVENT_DB_FILEPATH)
    cursor = conn.cursor()

    cursor.execute(cfg.SQL_SELECT_EVENT_BY_ID, [(id)])
    result = cursor.fetchall()

    if len(result) == 0:
        return Event(-1, "", "", "", "", 0)
    return Event.create_from_tuple(result[0])


def create_ticket(event_id, user, amount):
    event = get_event_by_id(event_id)

    conn = sqlite3.connect(cfg.EVENT_DB_FILEPATH)
    cursor = conn.cursor()

    if amount > event.places:
        return cfg.NO_TICKETS

    event.places = event.places - amount
    cursor.execute(cfg.SQL_UPDATE_EVENT, [event.places, event.id])
    conn.commit()

    cursor.execute(cfg.SQL_INSERT_TICKET, [event.id, user, amount])
    conn.commit()

    t = Ticket(-1, event.id, user, amount)
    return (event.id, amount, t.to_string(event))


def add_places(event_id, places):
    event = get_event_by_id(event_id)

    conn = sqlite3.connect(cfg.EVENT_DB_FILEPATH)
    cursor = conn.cursor()

    event.places = event.places + places
    cursor.execute(cfg.SQL_UPDATE_EVENT, [event.places, event.id])
    conn.commit()


def get_events_by_user(user):
    conn = sqlite3.connect(cfg.EVENT_DB_FILEPATH)
    cursor = conn.cursor()

    cursor.execute(cfg.SQL_SELECT_USER_EVENTS, [user])
    result = cursor.fetchall()
    events = []
    for t in result:
        events.append(t[0])
    return events


def get_tickets():
    conn = sqlite3.connect(cfg.EVENT_DB_FILEPATH)
    cursor = conn.cursor()

    cursor.execute(cfg.SQL_SELECT_TICKETS)
    result = cursor.fetchall()

    tickets = []
    for t in result:
        tickets.append(Ticket.create_from_tuple(t))

    return tickets


def clear_tickets():
    conn = sqlite3.connect(cfg.EVENT_DB_FILEPATH)
    cursor = conn.cursor()

    cursor.execute(cfg.SQL_CLEAR_TICKETS)
    conn.commit()
