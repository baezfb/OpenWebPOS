const today = new Date();

function go_back() {
    window.history.back();
}

function getKeyValue(val) {
    let display = document.getElementById('display');
    display.value += val
}

function addNumber(element) {
    document.getElementById('keypadVar').value = document.getElementById('keypadVar').value + element.value;
}

function currentDate() {
    const year = today.getFullYear();
    const month = today.toLocaleString('default', {month: "long"});
    const day = today.toLocaleString('default', {day: "2-digit"});

    document.getElementById('date').innerText = month + " " + day + " " + year;
}

function currentTime() {
    function updateTime(time) {
        if (time < 10) {
            return "0" + time;
        } else {
            return time;
        }
    }

    let hour = updateTime(today.getHours());
    let min = updateTime(today.getMinutes());

    let mid_day = (hour >= 12) ? "PM" : "AM";
    hour = (hour === 0) ? 12 : ((hour > 12) ? (hour - 12) : hour);

    document.getElementById('time').innerText = hour + ":" + min + " " + mid_day;

    const t = setTimeout(function () {
        currentTime();
    }, 1000);
}

document.addEventListener('DOMContentLoaded', function () {
    M.AutoInit();
    currentTime();
    currentDate();
})