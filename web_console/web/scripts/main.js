window.onload = _=> {
	const socket = io();
	socket.on('connect', _=>{
		document.querySelector("#console").innerHTML = ""
		socket.emit('get_history', data=>{
			data.forEach(item=>{
				log(item)
			})
		})
	});
	socket.on('new_log', data=>{
		log(data)
	});
}

function log(data){
	let div = document.createElement("div")
	div.classList.add("log", data.level)
	let code = document.createElement("code")
	if (data.message === null){
		code.innerHTML = "None"
		code.setAttribute("type", "none")
	}
	else if (typeof data.message === "boolean"){
		code.innerHTML = data.message ? "True": "False"
		code.setAttribute("type", "bool")
	}
	else if (typeof data.message === "number"){
		code.textContent = data.message
		code.setAttribute("type", "int")
	}
	else if (typeof data.message === "string"){
		code.textContent = data.message
		code.setAttribute("type", "str")

		const urlPattern = /https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)/;
		code.innerHTML = code.innerHTML.replace(urlPattern, (url) => {
			return `<a href="${url}" target="_blank">${url}</a>`;
		})
	}
	else if (typeof data.message === "object"){
		code.classList.add("tree")
		code.appendChild(buildTree(data.message))
	}
	else {
		code.textContent = data.message
	}
	let link = document.createElement("a")
	link.className = "caller"
	link.innerHTML = `${data.filename}:${data.line}`
	div.appendChild(link)
	div.appendChild(code)
	document.querySelector("#console").appendChild(div)
}
