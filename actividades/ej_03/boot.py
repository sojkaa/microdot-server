# Configuracion inicial
import network

def connect_to_wifi():
    """Conecta al WiFi"""
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect('Cooperadora Alumnos', '')
        while not sta_if.isconnected():
            pass
    print('Conectado. Configuración de red:', sta_if.ifconfig())
