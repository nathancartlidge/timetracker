import eel
import logging
from data_handler import DataHandler

PORT = 8081

logging.basicConfig(level=logging.INFO)
handler = DataHandler("/data/times")

eel.init("web")

@eel.expose()
def get_clients():
    return [
        {"id": c_id, "name": c_name}
        for (c_id, c_name)
        in handler.get_clients()
    ]

@eel.expose()
def get_worktypes():
    return handler.get_work()

@eel.expose()
def get_entries(filter=None):
    return handler.get_entries(filter)

@eel.expose()
def make_csv(filter=None):
    return handler.get_pandas(filter)

@eel.expose()
def get_time(client_id, grouped: bool = False):
    if grouped:
        return handler.get_hours_by_client(client_id)

    else:
        hours = handler.get_hours(client_id)
        if hours is None:
            return 0
        return hours

@eel.expose()
def delete_entry(entry_id):
    handler.delete_entry(int(entry_id))

@eel.expose()
def delete_client(client_id):
    handler.delete_client(int(client_id))

@eel.expose()
def add_client(client_name):
    return handler.get_client_id(client_name)

@eel.expose()
def add_work(work_name):
    return handler.get_work_id(work_name)

@eel.expose()
def add_entry(client, worktype, date, hours, comment):
    handler.add_entry(client, worktype, date, hours, comment)

logging.info(f"Server running on http://localhost:{PORT}")
eel.start("index.html", host="0.0.0.0", block=True, mode=None, port=PORT,
          shutdown_delay=86400)

logging.info("Shutdown due to inactivity")
