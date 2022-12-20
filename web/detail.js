const heading = document.getElementById("client");
const table_headings = document.getElementById("headings");
const table_values = document.getElementById("values");
const table_entries = document.getElementById("entries");
const searchParams = new URLSearchParams(window.location.search);
const client = searchParams.get("client");

if (client == null) {
    heading.innerText = "error getting client";
} else {
    heading.innerText = "client " + client;
    eel.add_client(client)(id => {
        eel.get_time(id, true)(group => {
            if (group.length != 0) {
                document.querySelectorAll(".hide").forEach(el => {
                    el.classList.remove("hide");
                })
            }
            group.forEach(element => {
                if (element != null) {
                    let header = document.createElement("th");
                    header.innerText = element[0];
                    table_headings.appendChild(header);

                    let value = document.createElement("td");
                    let hours = Math.floor(element[1] + 0.0001);
                    let mins = Math.floor(((element[1] + 0.0001) % 1) * 60);
                    let timeText = hours + ':' + String(mins).padStart(2, '0');
                    value.innerText = timeText;
                    table_values.appendChild(value);
                }
            });
        });
        eel.get_time(id, false)(time => {
            let hours = Math.floor(time[0] + 0.0001);
            let mins = Math.floor(((time[0] + 0.0001) % 1) * 60);
            let timeText = hours + "h" + String(mins).padStart(2, '0') + "m";

            heading.innerText += ": " + timeText;
        });
        eel.get_entries(id)(entries => {
            console.log(entries);
            entries.forEach(entry => {
                let row = document.createElement("tr");

                let cat = document.createElement("td");
                cat.innerText = entry[0];
                row.appendChild(cat);
                let date = document.createElement("td");
                date.innerText = entry[1];
                row.appendChild(date);
                let hours = document.createElement("td");
                let minsText = Math.floor(((entry[2] + 0.0001) % 1) * 60);
                let timeText = Math.floor(entry[2] + 0.0001) + ':' + String(minsText).padStart(2, '0');
                hours.innerText = timeText;
                row.appendChild(hours);
                let note = document.createElement("td");
                note.innerText = entry[3];
                row.appendChild(note);
                // let added = document.createElement("td");
                // added.innerText = entry[4];
                // row.appendChild(added);
                let delete_entry = document.createElement("td");
                let delete_button = document.createElement("button")
                delete_button.innerText = "x"
                delete_button.setAttribute("data-client", entry[5]);
                delete_button.setAttribute("onclick", "deleteRow(this)");
                delete_button.classList.add("warn");
                delete_entry.appendChild(delete_button);
                row.appendChild(delete_entry);

                table_entries.appendChild(row);
            });
        });
        document.getElementById("download").setAttribute("onclick", "getData(" + id + ")")
        document.getElementById("delete").setAttribute("onclick", "deleteClient(" + id + ")");
    })
    function deleteRow(button) {
        eel.delete_entry(button.getAttribute("data-client"))(_ => {
            window.location.reload();
        })
    }
    function deleteClient(client_id) {
        del = confirm("Are you sure you wish to delete this client? This action is not reversible!");
        if (del == true) {
            eel.delete_client(client_id);
            window.location = "index.html";
        }
    }
}

function getData(client) {
    eel.make_csv(client)(fn => {
        let anchor = document.createElement('a');
        anchor.href = "/data/" + fn;
        anchor.target = '_blank';
        anchor.download = fn;
        anchor.click();
    })
}

function addEntry() {
    if (client != null) {
        window.location = "entry.html?client=" + client
    } else {
        window.location = "entry.html"
    }
}