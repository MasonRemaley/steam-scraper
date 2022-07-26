// Original code, lightly changed: https://gist.github.com/petersvp/270f7d5d7d548448f4897586a0d389c0
// # Usage
// 1. Load the query CD key page (you must be signed in): https://partner.steamgames.com/querycdkey/
// 2. Fill in the keys below
// 3. Paste this code into the console, results will be printed to console

var keys = `
// Paste keys here, separated by newlines
`;

keys.split("\n").forEach(key => {
	if (key == "") { return; }

	let req = new XMLHttpRequest();
	function response_listener() {
		let body = this.responseText;
		let result = body.split("<h2>Activation Details</h2>")[1];
		if (!result) {
			console.log("Failed to query " + key);
			return;
		}
		result = result.split("</table>")[0];
		result = result.match(/<td>.*<\/td>/g);
		result = result.map(line => line.replace(/<[^>]*>/g, ""));
		let activated = (result[0] === "Activated");
		if (activated) {
			let line = [key, '"' + result[1] + '"'].join("\t");
			console.log(line);
		}
	}
	req.addEventListener("load", response_listener);
	req.open("GET", "https://partner.steamgames.com/querycdkey/cdkey?cdkey=" + key + "&method=Query");
	req.send();
});
