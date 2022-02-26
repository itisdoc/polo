// --- CHAT JAVASCRIPT --- \\

var socket = io.connect();


socket.on("connect", ()=> {
	document.getElementById('status').classList.add('online');
})
socket.on("disconnect", ()=> {
	document.getElementById('status').classList.remove('online');
})
socket.on('broadcast', (data)=> {
	var today = new Date();
	var time = today.getHours() + ":" + today.getMinutes()
	var el = document.createElement('div');
	el.classList.add('message')
	el.classList.add('left')
	el.innerHTML = `<div class='container'><p><span class='username'>${data["username"]}</span>${data["message"]}<p><p class='timeStamp left'>${time}</p></div>`;
	document.getElementById('messages').appendChild(el);
})

document.addEventListener('keyup', (event)=> {
	if (event.keyCode == 13) {
		sendMessage();
	}
})


function sendMessage() {
	message = document.getElementById('message').value;
	document.getElementById('message').value = "";

	if (message && message != "" && message != "\n") {
		json = {
			message:message,
		}
		socket.emit("send", json);
		var today = new Date();
		var time = today.getHours() + ":" + today.getMinutes()
		var el = document.createElement('div');
		el.classList.add('message')
		el.classList.add('right')
		el.innerHTML = `<div class='container'><p>${message}<p><p class='timeStamp right'>${time}</p></div>`;
		document.getElementById('messages').appendChild(el);
	}
}
