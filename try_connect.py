import network

shown_message = False

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)
sta_if.active(True)

def try_connect():
    print(sta_if.ifconfig())
    sta_if.ifconfig(("10.0.1.17", "255.255.255.0", "10.0.1.1", "10.0.1.1"))
    if sta_if.isconnected() and not shown_message:
        print('\nnetwork config: {}'.format(sta_if.ifconfig()))
        shown_message = True
    else:
        sta_if.connect("Lee's Wi-Fi Network", 'Ramborox21')
        