import network

shown_message = False

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)
sta_if.active(True)

def try_connect():
    if not sta_if.isconnected()
        sta_if.connect("Lee's Wi-Fi Network", 'Ramborox21')
    elif not shown_message:
        print('\nnetwork config:', sta_if.ifconfig())

        shown_message = True