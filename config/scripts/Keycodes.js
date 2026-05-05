// Contains all the keycodes and their respective letters [Code] : "Char"
const Keycodes = {
	0x04: "A",
	0x05: "B",
	0x06: "C",
	0x07: "D",
	0x08: "E",
	0x09: "F",
	0x0A: "G",
	0x0B: "H",
	0x0C: "I",
	0x0D: "J",
	0x0E: "K",
	0x0F: "L",
	0x10: "M",
	0x11: "N",
	0x12: "O",
	0x13: "P",
	0x14: "Q",
	0x15: "R",
	0x16: "S",
	0x17: "T",
	0x18: "U",
	0x19: "V",
	0x1A: "W",
	0x1B: "X",
	0x1C: "Y",
	0x1D: "Z",
	0x1E: "1",
	0x1F: "2",
	0x20: "3",
	0x21: "4",
	0x22: "5",
	0x23: "6",
	0x24: "7",
	0x25: "8",
	0x26: "9",
	0x27: "0",
	0x28: "Ent",
	0x29: "Esc",
	0x2A: "Bck",
	0x2B: "Tab",
	0x2C: "Spa",
	0x2D: "-",
	0x2E: "=",
	0x2F: "[",
	0x30: "]",
	0x31: "\\",
	0x32: "#",
	0x33: ";",
	0x34: "'",
	0x35: "`",
	0x36: ",",
	0x37: ".",
	0x38: "/",
	0x39: "CLck",
	0x3A: "F1",
	0x3B: "F2",
	0x3C: "F3",
	0x3D: "F4",
	0x3E: "F5",
	0x3F: "F6",
	0x40: "F7",
	0x41: "F8",
	0x42: "F9",
	0x43: "F10",
	0x44: "F11",
	0x45: "F12",
	0x46: "Prnt",
	0x47: "SLck",
	0x48: "Paus",
	0x49: "Ins",
	0x4A: "Home",
	0x4B: "PgUp",
	0x4C: "Del",
	0x4D: "End",
	0x4E: "PgDw",
	0x4F: "RArr",
	0x50: "LArr",
	0x51: "DArr",
	0x52: "UArr",
	0x53: "NLck",
	0x54: "K/",
	0x55: "K*",
	0x56: "K-",
	0x57: "K+",
	0x58: "KEnt",
	0x59: "K1",
	0x5A: "K2",
	0x5B: "K3",
	0x5C: "K4",
	0x5D: "K5",
	0x5E: "K6",
	0x5F: "K7",
	0x60: "K8",
	0x61: "K9",
	0x62: "K0",
	0x63: "K.",
	0x64: "K\\",
	0x65: "Menu",
	0x66: "Pwr",
	0x67: "K=",
	0x68: "F13",
	0x69: "F14",
	0x6A: "F15",
	0x6B: "F16",
	0x6C: "F17",
	0x6D: "F18",
	0x6E: "F19",
	0x6F: "F20",
	0x70: "F21",
	0x71: "F22",
	0x72: "F23",
	0x73: "F24",
	0xE0: "LCtr",
	0xE1: "LShf",
	0xE2: "LAlt",
	0xE3: "LMet",
	0xE4: "RCtr",
	0xE5: "RShf",
	0xE6: "RAlt",
	0xE7: "RMet" 
}

// Contains all the letters and their respective keycodes "Char" = [Code]
const Codes = {
}

// Invert Keycodes into Codes
for (Value in Keycodes){
	const Index = Keycodes[Value]
	Codes[Index] = Value
}

// Checks if a given keycode is valid
function IsKeyValid(Keycode){
	return Keycodes[Keycode] != undefined
}

// Turns a keycode into text, turning corrupted keys into ???
function KeycodeToText(Keycode){
	if (IsKeyValid(Keycode)){
		return Keycodes[Keycode]
	} else {
		return "???"
	}
}

// Turns improper/corrupted keys into "?", allowing the rest to pass
function FilterKeycode(Keycode){
	if (IsKeyValid(Keycode)){
		return Keycode
	} else {
		return 0x38
	}
}

// Creates a set of Option elements and adds them to the provided selector
function LoadKeycodeSelector(Selector){
	for (Index in Keycodes){
		const OptionElement = document.createElement("option")
		OptionElement.value = Index
		OptionElement.innerHTML = Keycodes[Index]

		Selector.appendChild(OptionElement);
	}
}

function LoadAllSelectors(){
	const Selectors = document.getElementsByClassName("combo-key")

	for(let Index = 0; Index < Selectors.length; Index++){
		LoadKeycodeSelector(Selectors.item(Index))
	}
}

LoadAllSelectors()

const tipo = document.getElementById("tipo");

const keyConfig = document.getElementById("key-config");
const textConfig = document.getElementById("text-config");
const comboConfig = document.getElementById("combo-config");

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
    `;

	const NewSelect = document.createElement("select")
	NewSelect.className="combo-combo"

	wrapper.appendChild(NewSelect)

	LoadKeycodeSelector(NewSelect)

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