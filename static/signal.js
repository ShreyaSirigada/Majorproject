let signals = {
    'North': 'Red',
    'South': 'Red',
    'East': 'Red',
    'West': 'Red'
};

function updateSignalDisplay() {
    fetch('/predict_traffic', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            document.getElementById('signal_status').innerText = `Next minute vehicle count: ${data.prediction}`;
            if (data.prediction > 10) {
                signals = {'North': 'Green', 'South': 'Red', 'East': 'Red', 'West': 'Red'};
            } else {
                signals = {'North': 'Red', 'South': 'Green', 'East': 'Red', 'West': 'Red'};
            }
            displayTrafficSignal();
        });
}

function displayTrafficSignal() {
    let signalInfo = '';
    for (let direction in signals) {
        signalInfo += `${direction}: ${signals[direction]}<br>`;
    }
    document.getElementById('signal_status').innerHTML = signalInfo;
}

setInterval(updateSignalDisplay, 5000);  // Update every 5 seconds
