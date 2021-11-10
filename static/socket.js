const socket = io();

function entrarSala(){
    socket.emit("join", JSON.stringify({room: "chatroom", username: username}));
}

function salirSala(){
    socket.emit("leave", JSON.stringify({room: "chatroom", username: username}));
}

socket.on("connect", function (){
    entrarSala();
});

socket.on("message", function (message){
    console.log(message);
    const divMessage = document.createElement("div");
    divMessage.textContent = message.username + " " + message.data;
    const chatDisplay = document.getElementById('chat');
    chatDisplay.append(divMessage);
});

function enviarMessage(){
    const message = {data: document.getElementById("input").value, username: username, room: "chatroom"};
    socket.send(JSON.stringify(message));
}

document.getElementById("enviar").addEventListener("click", ()=>{
    enviarMessage();
});
