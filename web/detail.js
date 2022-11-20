const heading = document.getElementById("client");
const table_headings = document.getElementById("headings");
const table_values = document.getElementById("values");
const table_entries = document.getElementById("entries");
const searchParams = new URLSearchParams(window.location.search);
const client = searchParams.get("client");

if (client == null) {
    heading.innerText = "error";
} else {
    heading.innerText = "client " + client;
    eel.add_client(client)(id => {
        eel.get_time(id, true)(group => {
            console.log(group)
            group.forEach(element => {
                if (element != null) {
                    let header = document.createElement("th");
                    header.innerText = element[0];
                    table_headings.appendChild(header);

                    let value = document.createElement("td");
                    let hours = Math.floor(element[1]);
                    let mins = Math.floor((element[1] % 1) * 60 + 0.0001);
                    let timeText = hours + ':' + String(mins).padStart(2, '0');
                    value.innerText = timeText;
                    table_values.appendChild(value);
                }
            });
        });
        eel.get_time(id, false)(time => {
            let hours = Math.floor(time);
            let mins = Math.floor((time % 1) * 60 + 0.0001);
            let timeText = hours + ':' + String(mins).padStart(2, '0');

            document.getElementById("totalTime").innerText = timeText + " total";
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
                let minsText = Math.floor((entry[2] % 1) * 60 + 0.0001);
                let timeText = Math.floor(entry[2]) + ':' + String(minsText).padStart(2, '0');
                hours.innerText = timeText;
                row.appendChild(hours);
                let note = document.createElement("td");
                note.innerText = entry[3];
                row.appendChild(note);
                let added = document.createElement("td");
                added.innerText = entry[4];
                row.appendChild(added);
                let delete_entry = document.createElement("td");
                let delete_button = document.createElement("button")
                delete_button.innerText = "x"
                delete_button.setAttribute("data-client", entry[5]);
                delete_button.setAttribute("onclick", "deleteRow(this)");
                delete_entry.appendChild(delete_button);
                row.appendChild(delete_entry);

                table_entries.appendChild(row);
            });
        });
    })
    function deleteRow(button) {
        eel.delete_entry(button.getAttribute("data-client"))(_ => {
            window.location.reload();
        })
    }
}

