let tg = window.Telegram.WebApp;
tg.expand();

let item = ""

let btn1 = document.getElementById("btn1");
let btn2 = document.getElementById("btn2");
let btn3 = document.getElementById("btn3");
let btn4 = document.getElementById("btn4");

btn1.addEventListener("click", function() {
    item = "1";
    tg.sendData(item);
    print("Запрос 1")
});

btn2.addEventListener("click", function() {
    item = "2";
    tg.sendData(item);
    print("Запрос 2")
});

btn3.addEventListener("click", function() {
    item = "3";
    tg.sendData(item);
    print("Запрос 3")
});

btn4.addEventListener("click", function() {
    item = "4";
    tg.sendData(item);
    print("Запрос 4")
});

