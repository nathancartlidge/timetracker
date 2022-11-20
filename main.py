import eel
from data_handler import DataHandler

eel.init('web')
handler = DataHandler("test")

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
    handler.delete_entry(entry_id)

@eel.expose()
def add_client(client_name):
    return handler.get_client_id(client_name)

@eel.expose()
def add_work(work_name):
    return handler.get_work_id(work_name)

@eel.expose()
def add_entry(client, worktype, date, hours, comment):
    handler.add_entry(client, worktype, date, hours, comment)

print("Server running on http://localhost:8080")
eel.start('index.html', block=True, mode=None, port=8080)
