const clientList = document.getElementById("clientList");
const clientCount = document.getElementById("clientCount");

eel.get_clients()(clients => {
    if (clients.length != 0) {
        document.querySelectorAll(".hide").forEach(el => {
            el.classList.remove("hide");
        })
    }

    clients.forEach(client => {
        let row = document.createElement("tr");

        let name = document.createElement("td");
        name.innerText = client.name;

        let timeText = document.createElement("td");
        let timeTextSpan = document.createElement("span");
        eel.get_time(client.id)(time => {
            hours = Math.floor(time[0] + 0.0001);
            mins = Math.floor(((time[0] + 0.0001) % 1) * 60);
            timeText = hours + ':' + String(mins).padStart(2, '0');
            timeTextSpan.innerHTML = timeText;
        })
        timeText.appendChild(timeTextSpan);

        let details = document.createElement("td");
        let detailsButton = document.createElement("button")
        detailsButton.setAttribute("data-client", client.name);
        detailsButton.setAttribute("onclick", "getTime(this)");
        detailsButton.innerHTML = "→"

        details.appendChild(detailsButton);

        row.appendChild(name);
        row.appendChild(timeText);
        row.appendChild(details)
        clientList.appendChild(row);
    });

    clientCount.innerText = clients.length + ((clients.length == 1) ? " client" : " clients")
})

function getTime(button) {
    window.location.href = "/detail.html?client=" + button.getAttribute("data-client");
}

function getData() {
    eel.make_csv()(fn => {
        let anchor = document.createElement('a');
        anchor.href = "/data/" + fn;
        anchor.target = '_blank';
        anchor.download = fn;
        anchor.click();
    })
}