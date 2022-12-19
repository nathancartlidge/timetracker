MAKE_WORKTYPE_TABLE = """
CREATE TABLE IF NOT EXISTS worktype (
    work_id   INTEGER PRIMARY KEY NOT NULL,
    work_name TEXT    UNIQUE NOT NULL
)
"""

MAKE_CLIENT_TABLE = """
CREATE TABLE IF NOT EXISTS clients (
    client_id   INTEGER PRIMARY KEY NOT NULL,
    client_name TEXT    UNIQUE NOT NULL
)
"""

MAKE_TIME_TABLE = """
CREATE TABLE IF NOT EXISTS entries (
    entry_id  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    client_id INTEGER NOT NULL,
    work_id   INTEGER NOT NULL,
    date      TEXT    NOT NULL,
    hours     REAL    NOT NULL,
    addtime   INTEGER NOT NULL,
    comment   TEXT,

    FOREIGN KEY (client_id)
        REFERENCES clients (client_id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION,
    FOREIGN KEY (work_id)
        REFERENCES worktype (work_id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
)
"""

GET_ENTRIES = """
SELECT clients.client_name as client, worktype.work_name as work_type,
       entries.date as date, entries.hours as hours,
       entries.comment as comment,
       datetime(entries.addtime, 'unixepoch') as add_time,
       entries.entry_id as entry_id
    FROM entries
        INNER JOIN clients ON entries.client_id = clients.client_id
        INNER JOIN worktype ON entries.work_id = worktype.work_id
    ORDER BY entries.date ASC
"""
GET_ENTRIES_BY_ID = """
SELECT worktype.work_name as work_type, entries.date as date,
       entries.hours as hours, entries.comment as comment,
       datetime(entries.addtime, 'unixepoch') as add_time,
       entries.entry_id as entry_id
    FROM entries
        INNER JOIN worktype ON entries.work_id = worktype.work_id
    WHERE entries.client_id = ?
    ORDER BY entries.date ASC
"""

DELETE_ENTRY = "DELETE FROM clients WHERE client_id = ?"
DELETE_CLIENT = "DELETE FROM entries WHERE entry_id = ?"

GET_CLIENTS = "SELECT client_id, client_name FROM clients"
GET_WORK = "SELECT work_name FROM worktype"

GET_CLIENTID = "SELECT client_id FROM clients WHERE client_name = ?"
GET_WORKID = "SELECT work_id FROM worktype WHERE work_name = ?"

GET_TIME_BY_CLIENT = "SELECT SUM(hours) FROM entries WHERE client_id = ?"
GET_TIME_BY_CLIENT_GROUPED = """
SELECT worktype.work_name as worktype, SUM(hours) as hours
    FROM entries
        INNER JOIN worktype ON entries.work_id = worktype.work_id
    WHERE client_id = ?
    GROUP BY worktype.work_name
"""

ADD_CLIENT = "INSERT INTO clients (client_name) VALUES (?)"
ADD_WORK = "INSERT INTO worktype (work_name) VALUES (?)"
ADD_ENTRY = """
INSERT INTO entries
    (client_id, work_id, date, hours, addtime, comment)
    VALUES (?, ?, ?, ?, ?, ?)
"""