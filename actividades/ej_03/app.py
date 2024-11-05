# Aplicacion del servidor
import machine
import onewire
import ds18x20
import microdot
from boot import do_connect

# Configuración de pines
BUZZER_PIN = 14
DS_PIN = 19

# Inicialización de pines y sensores
buzzer = machine.Pin(BUZZER_PIN, machine.Pin.OUT)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(machine.Pin(DS_PIN)))

# Conexión a WiFi
do_connect()

# Creación de la aplicación web
app = microdot.Microdot()

@app.route('/')
async def index(request):
    return send_file('index.html')

@app.route('/<dir>/<file>')
async def static(request, dir, file):
    return send_file("/{}/{}".format(dir, file))

@app.route('/sensors/ds18b20/read')
async def temperature_measuring(request):
    ds_sensor.convert_temp()
    machine.sleep_ms(1)
    temperature_celsius = ds_sensor.read_temp(ds_sensor.scan()[0])
    return {'temperature': temperature_celsius}

@app.route('/setpoint/set/<int:value>')
async def setpoint_calculation(request, value):
    if value >= ds_sensor.read_temp(ds_sensor.scan()[0]):
        buzzer.on()
        return {'buzzer': 'On'}
    else:
        buzzer.off()
        return {'buzzer': 'Off'}

if __name__ == '__main__':
    app.run(port=80)
