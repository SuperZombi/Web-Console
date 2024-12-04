function buildNode(json_data){
	function makeKey(val){
		let item_key = document.createElement("span")
		item_key.className = "key"
		item_key.innerHTML = val
		setDataType(val, item_key)
		return item_key
	}
	function parseValue(val) {
		if (val === null){ return "None" }
		else if (val === true){ return "True" }
		else if (val === false){ return "False" }
		return JSON.stringify(val)
	}
	function setDataType(val, el){
		if (val === null){
			el.setAttribute("type", "none")
		}
		else if (typeof val === "boolean"){
			el.setAttribute("type", "bool")
		}
		else if (typeof val === "string"){
			el.setAttribute("type", "str")
		}
		else if (typeof val === "number"){
			el.setAttribute("type", "int")
		}
	}

	let list = document.createElement("ul")
	for (const [key, value] of Object.entries(json_data)) {
		let item = document.createElement("li")

		if (typeof value === "object" && value !== null){
			let details = document.createElement("details")
			let summary = document.createElement("summary")
			if (value.constructor.name === "Array"){
				details.setAttribute("type", "array")
			}

			summary.appendChild(makeKey(key))
			let empty_val = document.createElement("span")
			empty_val.className = "value"
			summary.appendChild(empty_val)

			details.appendChild(summary)
			details.appendChild(buildNode(value))
			item.appendChild(details)
		}
		else {
			item.appendChild(makeKey(key))
			item.classList.add("line")

			let item_value = document.createElement("span")
			item_value.className = "value"
			item_value.innerHTML = parseValue(value)
			setDataType(value, item_value)
			item.appendChild(item_value)
		}
		list.appendChild(item)
	}
	return list
}
