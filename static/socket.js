const socket = io();
const chatInput = document.getElementById('input');

function entrarSala(sala){
    socket.emit("join", JSON.stringify({room: sala, username: username}));
    console.log(sala)
}

function salirSala(sala){
    socket.emit("leave", JSON.stringify({room: sala, username: username}));
}

socket.on("connect", function (){

    window.localStorage.setItem("room", "Random");
    entrarSala(window.localStorage.getItem("room"));

});

socket.on("message", function (message){
    console.log(message);
    const divMessage = document.createElement("div");
    divMessage.textContent = message.username + ": " + message.data;
    const chatDisplay = document.getElementById('chat');
    chatDisplay.append(divMessage);
});

socket.on("alerta", function (message){
    console.log(message);
    const divMessage = document.createElement("div");
    divMessage.textContent = message.username + " " + message.data;
    const chatDisplay = document.getElementById('chat');
    chatDisplay.append(divMessage);
});

function enviarMessage(){
    const message = {data: document.getElementById("input").value, username: username, room: window.localStorage.getItem('room')};
    socket.send(JSON.stringify(message));
}

document.getElementById("enviar").addEventListener("click", ()=>{
    enviarMessage();
});

chatInput.addEventListener('enviar', e => {
    e.target.elements.message.value = "";
});
