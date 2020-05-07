const socket = io("http://localhost:8080");

function sendMsg() {
  socket.emit("message", "HELLO WORLD");
}

socket.on("message", function(data) {
  console.log(data);
});