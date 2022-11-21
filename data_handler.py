import sqlite3
from time import time

import pandas as pd
import numpy as np

from queries import *

class DataHandler:
    def __init__(self, file) -> None:
        self.file = file
        self.make_tables()

    def make_tables(self):
        with sqlite3.connect(f"{self.file}.db") as conn:
            cursor = conn.cursor()

            cursor.execute(MAKE_WORKTYPE_TABLE)
            cursor.execute(MAKE_CLIENT_TABLE)
            cursor.execute(MAKE_TIME_TABLE)

            cursor.close()
            conn.commit()

    def get_clients(self):
        with sqlite3.connect(f"{self.file}.db") as conn:
            cursor = conn.cursor()
            cursor.execute(GET_CLIENTS)
            return cursor.fetchall()

    def get_work(self):
        with sqlite3.connect(f"{self.file}.db") as conn:
            cursor = conn.cursor()
            cursor.execute(GET_WORK)
            return [x for x, in cursor.fetchall()]

    def get_hours(self, client_id):
        with sqlite3.connect(f"{self.file}.db") as conn:
            cursor = conn.cursor()
            cursor.execute(GET_TIME_BY_CLIENT, (client_id, ))
            return cursor.fetchone()

    def get_hours_by_client(self, client_id):
        with sqlite3.connect(f"{self.file}.db") as conn:
            cursor = conn.cursor()
            cursor.execute(GET_TIME_BY_CLIENT_GROUPED, (client_id, ))
            return cursor.fetchall()

    def get_client_id(self, name):
        with sqlite3.connect(f"{self.file}.db") as conn:
            cursor = conn.cursor()
            cursor.execute(GET_CLIENTID, (name, ))
            client_id = cursor.fetchone()

            if client_id is None:
                cursor.execute(ADD_CLIENT, (name, ))
                cursor.execute(GET_CLIENTID, (name, ))
                client_id = cursor.fetchone()

                cursor.close()
                conn.commit()

        return client_id[0]

    def delete_entry(self, entry_id):
        with sqlite3.connect(f"{self.file}.db") as conn:
            cursor = conn.cursor()
            cursor.execute(DELETE_ENTRY, (entry_id, ))
            cursor.close()
            conn.commit()

    def get_work_id(self, name):
        with sqlite3.connect(f"{self.file}.db") as conn:
            cursor = conn.cursor()
            cursor.execute(GET_WORKID, (name, ))
            work_id = cursor.fetchone()

            if work_id is None:
                cursor.execute(ADD_WORK, (name, ))
                cursor.execute(GET_WORKID, (name, ))
                work_id = cursor.fetchone()

                cursor.close()
                conn.commit()

        return work_id[0]

    def add_entry(self, client, worktype, date, hours, comment):
        client_id = self.get_client_id(client)
        work_id = self.get_work_id(worktype)
        datetime = int(time())

        hours, minutes = map(int, hours.split(":"))
        e_time = hours + (minutes / 60)

        with sqlite3.connect(f"{self.file}.db") as conn:
            cursor = conn.cursor()
            cursor.execute(ADD_ENTRY, (client_id, work_id, date, e_time, datetime, comment))
            cursor.close()
            conn.commit()

    def get_pandas(self, client_id=None):
        with sqlite3.connect(f"{self.file}.db") as conn:
            if client_id is None:
                data = pd.read_sql_query(GET_ENTRIES, conn)
            else:
                data = pd.read_sql_query(GET_ENTRIES, conn, params=(client_id, ))

            data["time"] = np.round(data["hours"], 6)

            data["minutes"] = np.floor(60 * ((data["hours"] + 0.0001) % 1))
            data["minutes"] = data["minutes"].astype(int)

            data["hours"] = np.floor(data["hours"] + 0.0001)
            data["hours"] = data["hours"].astype(int)

            if client_id is None:
                data = data[["date", "client", "worktype", "time", "hours",
                             "minutes", "comment", "addtime"]]
                data.to_csv("web/data/all.csv", index=False)
                return f"all.csv"

            else:
                data = data[["date", "worktype", "time", "hours",
                             "minutes", "comment", "addtime"]]
                data.to_csv(f"web/data/client_{client_id}.csv", index=False)
                return f"client_{client_id}.csv"


    def get_entries(self, client_id=None):
        with sqlite3.connect(f"{self.file}.db") as conn:
            cursor = conn.cursor()
            if client_id is None:
                cursor.execute(GET_ENTRIES)
            else:
                cursor.execute(GET_ENTRIES_BY_ID, (client_id, ))
            return cursor.fetchall()