
let data;
data = {
	"firstName": "John",
	"lastName": "Smith",
	"isAlive": true,
	"age": 25,
	"company": null,
	"height_cm": 167.64,
	"address": {
		"streetAddress": "21 2nd Street",
		"city": "New York",
		"state": "NY",
		"postalCode": "10021-3100"
	},
	"phoneNumbers": [
		{
			"type": "home",
			"number": "212 555-1234"
		},
		{
			"type": "fax",
			"number": "646 555-4567",
			"other": ["1234", "4567", "7894"],
			"other2": {
				"text": {
					"hello": {
						"world": "Main"
					}
				}
			}
		}
	]
}

window.onload = _=> {
	document.querySelector("#root").appendChild(buildNode(data))

	const socket = io();
	
	socket.on('connect', _=>{
		socket.emit('get_history', data=>{
			console.log(data)
		})
	});
	socket.on('new_log', data=>{
		console.log(data);
	});
}
