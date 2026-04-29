const Container = document.getElementById('estrellas-container');

function CreateBaseStar() {
    const div = document.createElement('div');
    div.classList.add('estrella');
    div.addEventListener('animationend', () => {
        div.remove();
    });
    return div
}

function CreateFollower() {
	const BaseBlock = document.createElement("div")
	BaseBlock.className = "AbsBlock"
	BaseBlock.id = "Follower"
	if (document.body != null){
		document.body.appendChild(BaseBlock)
	}
	return BaseBlock
}

function CreateBackgroundStar() {
    const ModifierMaster = Math.random()*100
    
    var Modifier = ModifierMaster < 33 
    ? 1/5 
    : ModifierMaster < 66
        ? 1/2
        : 1

    const div = CreateBaseStar();
    div.style.left = `${Math.random() * 100}%`;
    div.style.animationDuration = `${(Math.random() * 5 + 2)*(1/Modifier)}s`;
    const size = Math.random() * 15 + 10;
    div.style.width = `${size*Modifier}px`;
    div.style.height = `${size*Modifier}px`;
    div.style.animationName= "moverArriba";
    Container.appendChild(div);
}

window.addEventListener("DOMContentLoaded", () => {
    setInterval(CreateBackgroundStar, 200);
});

var Ticks = 0;

document.onmousemove = function(Event) {
	const XPos = `${(Event.clientX*100)/window.innerWidth}%`
	const YPos = `${(Event.clientY*100)/window.innerHeight}%`
	var Follower = document.getElementById("Follower")
	
	if (Follower == null){
		Follower = CreateFollower()
	}

	Ticks++

    if (Ticks % 2 == 0){
        const Star = CreateBaseStar()
        Star.style.backgroundColor = "rgba(255, 255, 255, 0.73)"
        Star.style.rotate = `${360 * Math.random()}deg`
        Star.style.left = XPos
        Star.style.top = YPos
        Star.style.animationDuration = "500ms"
        Star.style.animationName = "Fade"
        const size = Math.random() * 15 + 10;
        Star.style.width = `${size}px`
        Star.style.height = `${size}px`
        Container.appendChild(Star)
        Ticks = 0
    }

	Follower.style.left = XPos
	Follower.style.top = YPos
}