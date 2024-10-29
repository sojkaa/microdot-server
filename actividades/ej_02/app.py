from boot import do_connect
from microdot import Microdot, send_file
import machine
import neopixel

do_connect()
app = Microdot()

# Usar una tupla para los pines LED, más eficiente que una lista
leds = (machine.Pin(32, machine.Pin.OUT),
        machine.Pin(33, machine.Pin.OUT),
        machine.Pin(25, machine.Pin.OUT))

np = neopixel.NeoPixel(machine.Pin(27), 8)

@app.route('/')
def index(request):  # No es necesario async para archivos estáticos
    return send_file('index.html')

@app.route('/<path>') # Maneja todas las rutas estáticas con una sola regla
def static_file(request, path):
    return send_file(f"/{path}")

@app.route('/led')
def led_control(request): # No es necesario async aquí
    led_num = int(request.args.get('led'))
    state = request.args.get('state') == 'true'
    print(f"Controlando LED {led_num}, su condición es: {state}")

    # Acceder a los LEDs por índice en la tupla
    led = leds[led_num - 1]
    led.value(state) # Usar led.value() es más eficiente

    return f'LED {led_num} {"Andando" if state else "Apagado"}'


@app.route('/color')
def color_control(request): # No es necesario async aquí
    # Conversión a entero más eficiente
    r = int(request.args['r'])
    g = int(request.args['g'])
    b = int(request.args['b'])

    print(f"Estableciendo color de tira LED: Rojo:{r}, Verde:{g}, Azul:{b}")

    np.fill((r, g, b))
    np.write()

    return f'Color establecido a Rojo:{r}, Verde:{g}, Azul:{b}'


app.run(port=80)# Aplicacion del servidor
