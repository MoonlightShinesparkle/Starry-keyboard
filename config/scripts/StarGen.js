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
    div.backgroundColor = `rgba(255, 255, 255, ${1/(Modifier)/5})`
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

// Funciones principales
//flechitas
let posicion = 0;

function mover(direccion) {
    const input = document.getElementById("aparador");

    if (input.scrollWidth <= input.clientWidth) {
        return; // no hace nada si cabe completo
    }

    posicion += direccion * 20; // velocidad más realista en px

    // límites reales de scroll
    const maxScroll = input.scrollWidth - input.clientWidth;

    if (posicion < 0) posicion = 0;
    if (posicion > maxScroll) posicion = maxScroll;

    input.scrollLeft = posicion;
}


const tipo = document.getElementById("tipo");

const keyConfig = document.getElementById("key-config");
const textConfig = document.getElementById("text-config");
const comboConfig = document.getElementById("combo-config");

function actualizarVista() {

    //  ocultar TODO primero
    keyConfig.style.display = "none";
    textConfig.style.display = "none";
    comboConfig.style.display = "none";


    // =========================
    // mostrar key (default)
    // =========================
    if (tipo.value === "key") {
        keyConfig.style.display = "flex";
    }


    // =========================
    // mostrar text
    // =========================
    else if (tipo.value === "text") {
        textConfig.style.display = "flex";
    }


    // =========================
    // mostrar combo
    // =========================
    else if (tipo.value === "combo") {
        comboConfig.style.display = "block";
    }
}


//  estado inicial (al cargar la página)
actualizarVista();

//  cambio dinámico
tipo.addEventListener("change", actualizarVista);

//sumar al combo
const comboContainer = document.getElementById("combo-keys");
const btnAgregar = document.getElementById("agregar-key");
const btnQuitar = document.getElementById("quitar-key");

let totalKeys = 0;
const MIN_KEYS = 2;
const MAX_KEYS = 8;

// crear un bloque combo
function crearCombo() {
    const wrapper = document.createElement("div");
    wrapper.classList.add("combo-item");

    wrapper.innerHTML = `
        <input type="text" class="input-combo" maxlength="2" placeholder="00">

        <select class="combo-combo">
            <option value="letters">Letras</option>
            <option value="numbers">Números</option>
            <option value="symbols">Símbolos</option>
            <option value="all">Todo</option>
        </select>
    `;

    comboContainer.appendChild(wrapper);
    totalKeys++;
    actualizarBotones();
}

// eliminar último
function eliminarCombo() {
    if (totalKeys <= MIN_KEYS) return;

    comboContainer.lastElementChild.remove();
    totalKeys--;
    actualizarBotones();
}

// control de botones
function actualizarBotones() {
    // ocultar - si hay mínimo
    btnQuitar.style.display = (totalKeys <= MIN_KEYS) ? "none" : "inline-block";

    // desactivar + si llega al máximo
    btnAgregar.disabled = (totalKeys >= MAX_KEYS);
}

// inicial → 2 combos
for (let i = 0; i < MIN_KEYS; i++) {
    crearCombo();
}

// eventos
btnAgregar.addEventListener("click", () => {
    if (totalKeys < MAX_KEYS) crearCombo();
});

btnQuitar.addEventListener("click", eliminarCombo);