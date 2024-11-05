// Constantes
const TEMPERATURE_INTERVAL = 500;
const TEMPERATURE_URL = '/sensors/ds18b20/read';
const SETPOINT_URL = '/setpoint/set/';
const TEMPERATURE_ELEMENT = document.getElementById('temperature-value');
const BUZZER_ELEMENT = document.getElementById('buzzer-state');
const SETPOINT_ELEMENT = document.getElementById('setpoint-value');
const SETPOINT_SLIDER = document.getElementById('setpoint-slider');

// Función para leer la temperatura
async function readTemperature() {
  try {
    const response = await fetch(TEMPERATURE_URL);
    const json = await response.json();
    TEMPERATURE_ELEMENT.innerText = json.temperature;
  } catch (error) {
    console.error('Error leyendo temperatura:', error);
  }
}

// Función para enviar el setpoint
async function sendSetpoint(value) {
  try {
    const response = await fetch(`${SETPOINT_URL}${value}`);
    const json = await response.json();
    BUZZER_ELEMENT.innerText = json.buzzer;
  } catch (error) {
    console.error('Error enviando setpoint:', error);
  }
}

// Función para actualizar el valor del setpoint
function updateSetpointValue(value) {
  SETPOINT_ELEMENT.innerText = value;
  sendSetpoint(value);
}

// Inicialización
setInterval(readTemperature, TEMPERATURE_INTERVAL);
SETPOINT_SLIDER.addEventListener('input', (e) => updateSetpointValue(e.target.value));
