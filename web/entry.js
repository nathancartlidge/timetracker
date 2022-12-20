const clientSelect = document.getElementById("client");
const workSelect = document.getElementById("worktype");
const date = document.getElementById("date");
const hours = document.getElementById("time");
const comment = document.getElementById("note");
const searchParams = new URLSearchParams(window.location.search);
const selectClient = searchParams.get("client");

eel.get_clients()(clients => {
    clients.forEach(client => {
        let entry = document.createElement("option");
        entry.text = client.name;
        entry.value = client.name;
        if (selectClient == client.name) {
            entry.selected = true;
        }
        clientSelect.appendChild(entry);
    });
});

eel.get_worktypes()(types => {
    types.forEach(type => {
        let entry = document.createElement("option");
        entry.text = type;
        entry.value = type;
        workSelect.appendChild(entry);
    });
});

document.getElementById("date").value = new Date().toISOString().split('T')[0]

function addClient() {
    if (clientSelect.selectedIndex == 0 ||
        workSelect.selectedIndex == 0) {
        alert("bad selection!");
        return;
    }

    if (time.value == "00:00") {
        alert("bad time!");
        return;
    }

    eel.add_entry(
        clientSelect.value,
        workSelect.value,
        date.value,
        time.value,
        comment.value
    )(_ => {
        window.location.href = "/index.html"
    });
}