let id = 1;

function updoot(lb) {
	lb.innerHTML = id;
}

window.onload = () => {
	let select = document.getElementById("select");

	let v0 = document.getElementById("v0");
	let v1 = document.getElementById("v1");
	let v2 = document.getElementById("v2");
	let v3 = document.getElementById("v3");
	let v4 = document.getElementById("v4");
	let lb = document.getElementById("pp");

	let ctx = document.getElementById("map").getContext("2d");

	v0.onclick = () => {
		id = 0;
		updoot(lb);
	}
	v1.onclick = () => {
		id = 1;
		updoot(lb);
	}

	v2.onclick = () => {
		id = 2;
		updoot(lb);
	}

	v3.onclick = () => {
		id = 3;
		updoot(lb);
	}

	v4.onclick = () => {
		id = 4;
		updoot(lb);
	}


	select.onchange = () => {
		let i = select.selectedIndex;

		tag = ""
		if(i > 0){
			tag = [0, "B", "C"][i]
		}

		v1.src = "sprites/block" + tag + ".png";
		v2.src = "sprites/block" + tag + "1.png";
		v3.src = "sprites/block" + tag + "2.png";
		v4.src = "sprites/spoike" + tag + ".png";
	}

	for(let i = 1; i < 30; i++){
		ctx.beginPath();
		ctx.moveTo(i * 17, 0);
		ctx.lineTo(i * 17, 339);
		ctx.stroke();
	}

	for(let i = 1; i < 20; i++){
		ctx.beginPath();
		ctx.moveTo(0, i * 17);
		ctx.lineTo(509, i * 17);
		ctx.stroke();
	}
}