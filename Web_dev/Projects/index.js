let start = document.getElementById("start-time");
let reset = document.getElementById("start-cycle");
let stop = document.getElementById("start-break");

let wm = document.getElementById("w_min");
let ws = document.getElementById("w_sec");

let bm = document.getElementById("b_min");
let bs = document.getElementById("b_sec");

let cycle_count = document.getElementById("cycle_count");

let startTimer;

start.addEventListener
("click", function () {
    if (startTimer === undefined) {
        startTimer = setInterval(Timer, 1000);
    } else {
        alert("Timer is already running");
    }
});


reset.addEventListener("click" , function() {
    wm.innerText = "25";
    ws.innerText = "00";

    bm.innerText =  "05"; 
    bs.innerText = "00";

    cycle_count.innerText = "0";

    stopInterval();
    startTimer = undefined;
});


stop.addEventListener("click", function() {
    stopInterval();
    startTimer = undefined;
});

function Timer(){
    // work Timer logic

    if(ws.innerText != 0){
        ws.innerText--;
    }

    else if(wm.innerText != 0 && ws.innerText == 0){
        ws.innerText = 59;
        wm.innerText--;
    }

    // break Timer Logic
    if(wm.innerText == 0 && ws.innerText == 0){
        if(bs.innerText != 0){
            bs.innerText-- ;
        }
        else if(bm.innerText != 0 && bs.innerText == 0){
            bs.innerText = 59;
            bm.innerText-- ;
        }
    }
    // increament cycle count if one cycle is completed
    if(wm.innerText == 0 && ws.innerText == 0 && bm.innerText == 0 && bs.innerText == 0){
        cycle_count.innerText++;
        wm.innerText = 25;
        ws.innerText = "00";

        bm.innerText = 5;
        bs.innerText = "00";

    }


}

function stopInterval(){
    clearInterval(startTimer);
}

