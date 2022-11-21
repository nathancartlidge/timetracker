const clientList = document.getElementById("clientList");
const clientCount = document.getElementById("clientCount");

eel.get_clients()(clients => {
    clients.forEach(client => {
        let row = document.createElement("tr");

        let name = document.createElement("td");
        name.innerText = client.name;

        let getTime = document.createElement("td");
        let getTimeButton = document.createElement("button");
        eel.get_time(client.id)(time => {
            hours = Math.floor(time[0] + 0.0001);
            mins = Math.floor(((time[0] + 0.0001) % 1) * 60);
            timeText = hours + ':' + String(mins).padStart(2, '0');
            getTimeButton.innerHTML = timeText;
        })
        getTimeButton.setAttribute("data-client", client.name);
        getTimeButton.setAttribute("onclick", "getTime(this)");
        getTime.appendChild(getTimeButton);

        row.appendChild(name);
        row.appendChild(getTime);
        clientList.appendChild(row);
    });

    clientCount.innerText = clients.length + " clients"
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