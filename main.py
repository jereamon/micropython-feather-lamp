import machine
import network
from utime import ticks_ms
import gc

from web_server import start_server, server_connect
from light_effects import FadeAlong


ap_if = network.WLAN(network.AP_IF)
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

print("ap_if ifconfig: {}".format(ap_if.ifconfig()))

try_connect_counter = 0


socket = start_server()

fade_along = FadeAlong()
fade_speeds = [1000, 800, 650, 500, 300, 100, 50, 20, 5, 1]
fade_speed = 5

def do_connect():
    sta_if.connect("Lee's Wi-Fi Network", "Ramborox21")
    if sta_if.isconnected():
        print("\nConnected to wifi:")
        print("\n{}\n".format(sta_if.ifconfig()))
    
fade_start_time = ticks_ms()
fade_counter_start_time = ticks_ms()
connect_start_time = ticks_ms()
gc.collect()
while True:
    gc.collect()
    if ticks_ms() - connect_start_time >= 500:
        if try_connect_counter <= 5 and sta_if.isconnected() == False:
            print("\nATTTEMPIng to connect to wifi")
            do_connect()
            try_connect_counter += 1

        connect_start_time = ticks_ms()

    server_connect(socket)

    if ticks_ms() - fade_start_time >= fade_speeds[fade_speed % 9]:
        fade_along.cycle_lights()

        fade_start_time = ticks_ms()

    if ticks_ms() - fade_counter_start_time >= 3000:
        fade_speed += 1
        fade_counter_start_time = ticks_ms()
        # print("\nFade Speed: {}".format(fade_speed))
