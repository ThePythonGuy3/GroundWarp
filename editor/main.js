let id = 1;
let dimens = 0;
let tiles = [[], [], []];
let images = [[], [], []];
let pid = "ABC";

function updoot(lb) {
	lb.innerHTML = id;
}

function paint(dim, ctx, x, y, rid = -1){
	if(rid == -1) rid = id;
	tiles[dim][y][x] = rid;

	let tid = rid - 1;
	if(rid == 9) tid = 4;

	ctx.beginPath();
	ctx.rect(x * 17, y * 17, 16, 16);
	ctx.fillStyle = "white";
	ctx.fill();

	if(rid != 0) ctx.drawImage(images[dim][tid], x * 17, y * 17);
}

function saveD(data, name) {
	let blob = new Blob([data], { type: "text/plain;charset=utf-8" });
	saveAs(blob, name + ".room", { type: "text/plain;charset=utf-8" });
}

function loadTile(dim, ctx){
	for(let i = 0; i < 30; i++){
		for(let j = 0; j < 20; j++){
			let rid = tiles[dim][j][i];
			if(rid == 9) rid = 5;

			ctx.beginPath();
			ctx.rect(i * 17, j * 17, 16, 16);
			ctx.fillStyle = "white";
			ctx.fill();

			if(rid != 0) ctx.drawImage(images[dim][rid - 1], i * 17, j * 17);
		}
	}
}

function downloadDimension(dim, name) {
	let data = "";

	for(let i = 0; i < 20; i++){
		for(let j = 0; j < 30; j++){
			data += tiles[dim][i][j];
		}
		data += ";";
	}

	console.log(data.slice(0, -1));
	saveD(data.slice(0, -1), name);
}

for(let i = 0; i < 3; i++){
	for(let j = 0; j < 20; j++){
		let temp = [];
		for(let q = 0; q < 30; q++){
			temp.push(0)
		}
		tiles[i].push(temp)
	}

	for(let j = 0; j < 3; j++){
		let image = new Image();
		let tg = "";
		if(i > 0) tg = pid[i];
		image.src = "sprites/block" + tg + (j == 0 ? "" : j) + ".png";
		images[i].push(image)
	}

	let image = new Image();
	let tg = "";
	if(i > 0) tg = pid[i];
	image.src = "sprites/spoike" + tg + ".png";
	images[i].push(image)

	image = new Image();
	image.src = "sprites/begin.png";
	images[i].push(image)
}

function randint(max) {
	return Math.floor(Math.random() * max);
}

console.log(tiles);
window.onload = () => {
	let select = document.getElementById("select");

	let v0 = document.getElementById("v0");
	let v1 = document.getElementById("v1");
	let v2 = document.getElementById("v2");
	let v3 = document.getElementById("v3");
	let v4 = document.getElementById("v4");
	let v99 = document.getElementById("v99");
	let lb = document.getElementById("pp");
	let rng = document.getElementById("rng");
	let newb = document.getElementById("new");
	let save = document.getElementById("save");
	let load = document.getElementById("load");

	let chooseFile = document.getElementById("chooseFile");

	let canvas = document.getElementById("map");
	let ctx = canvas.getContext("2d");
	ctx.lineWidth = 0.5;
	let rect = canvas.getBoundingClientRect();

	ctx.beginPath();
	ctx.rect(0, 0, 509, 339);
	ctx.fillStyle = "white";
	ctx.fill();

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

	v99.onclick = () => {
		id = 9;
		updoot(lb);
	}

	select.onchange = () => {
		dimens = select.selectedIndex;
		let i = dimens;

		tag = "";
		if(i > 0){
			tag = [0, "B", "C"][i];
		}

		v1.src = "sprites/block" + tag + ".png";
		v2.src = "sprites/block" + tag + "1.png";
		v3.src = "sprites/block" + tag + "2.png";
		v4.src = "sprites/spoike" + tag + ".png";

		loadTile(dimens, ctx);
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

	for(let i = 0; i < 30; i++){
		for(let j = 0; j < 20; j++){
			ctx.beginPath();
			ctx.rect(i * 17, j * 17, 16, 16);
			ctx.fillStyle = "white";
			ctx.fill();
		}
	}

	let click = false;
	let pX = -1;
	let pY = -1;

	canvas.onmousedown = () => {
		click = true;

		let tileX = Math.trunc((event.clientX - rect.x) / 17);
		let tileY = Math.trunc((event.clientY - rect.y) / 17);
		
		if(tileX != pX || tileY != pY) {
			paint(dimens, ctx, tileX, tileY);
		}

		pX = tileX;
		pY = tileY;
	}

	canvas.onmouseup = () => {
		click = false;
	}

	canvas.onmouseleave = () => {
		click = false;
	}

	canvas.onmousemove = event => {
		if(click) {
			let tileX = Math.trunc((event.clientX - rect.x) / 17);
			let tileY = Math.trunc((event.clientY - rect.y) / 17);
			
			if(tileX != pX || tileY != pY) {
				paint(dimens, ctx, tileX, tileY);
			}

			pX = tileX;
			pY = tileY;
		}
	}

	rng.onclick = () => {
		for(let i = 0; i < 30; i++){
			for(let j = 0; j < 20; j++){
				if(randint(9) >= 8 && tiles[dimens][j][i] > 0 && tiles[dimens][j][i] <= 3){
					let nId = randint(3) + 1;
					paint(dimens, ctx, i, j, nId);
				}
			}
		}
	}

	newb.onclick = () => {
		for(let i = 0; i < 30; i++){
			for(let j = 0; j < 20; j++){
				paint(dimens, ctx, i, j, 0);
			}
		}
	}

	save.onclick = () => {
		for(let i = 0; i < 3; i++){
			downloadDimension(i, pid[i]);
		}
	}

	load.onclick = () => {
		chooseFile.click();
	}

	chooseFile.addEventListener("change", () => {
		let file = chooseFile.files[0];

		file.text().then(e => {
			let x = 0;
			let y = 0;

			for(let i = 0; i < e.length; i++){
				if(e[i] == ";"){
					x = -1;
					y += 1;
				} else {
					paint(dimens, ctx, x, y, e[i]);
				}

				x += 1;
			}
		});

		chooseFile.value = "";
	});
}