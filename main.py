import machine
import network
from utime import ticks_ms
import usocket as socket
import uselect as select
import gc

# from web_server import start_server, server_connect
from light_effects import FadeAlong


# fade_along = FadeAlong([[255, 0, 0], [0, 255, 0], [0, 0, 255]])

class Main:
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.ifconfig(("10.0.1.120", "255.255.255.0", "10.0.1.1", "10.0.1.1"))

    light_options = {
        "quickselect": {
            "white": [255, 255, 255],
            "yellow": [255, 255, 0],
            "red": [255, 0, 0],
            "blue": [0, 0, 255],
            "green": [0, 255, 0],
            "purple": [255, 0, 255]
            },
        "brightness": 50,
        "fadealong": [[255, 0, 0], [0, 0, 255]],
        "fadespeed": [1000, 800, 650, 500, 300, 100, 50, 20, 5, 1]
    }

    quickselect = {
        "white": [255, 255, 255],
        "yellow": [255, 255, 0],
        "red": [255, 0, 0],
        "blue": [0, 0, 255],
        "green": [0, 255, 0],
        "purple": [255, 0, 255]
    }

    # light_options = {
    # "quickselect": ["white", "yellow", "red", "blue", "green", "fade"],
    # "brightness": [i for i in range(1, 101)],
    # "fade_speed": [i for i in range(1, 10)]
    # }

    def __init__(self):
        self.socket = self.start_server()

        self.fade_along = FadeAlong([[255, 0, 0], [0, 0, 255]])

        self.fade = True
        self.fade_along_offset = 0
        self.fade_along.cycle_lights()
        self.fade_speed = 8

        self.try_connect_counter = 0
        self.fade_start_time = ticks_ms()
        self.fade_counter_start_time = ticks_ms()
        self.connect_start_time = ticks_ms()

        gc.collect()


    def start_server(self):
        """
        Starts a simple socket server that will listen at the hosts ip address on
        port 8800.
        """
        server_port = 8800
        incoming_addr = ""
        address = (incoming_addr, server_port)

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SO_REUSEADDR)
        server_socket.bind(address)
        server_socket.listen(5)

        print("\nServer Listening\n")
        return server_socket


    def parse_request(self, request):
        """
        Takes an http request and parses the options it includes returning them as
        a dict with the options as keys and their values in lists.
        """
        request = str(request)
        str_start = request.find("GET /?")
        str_end = request.find("HTTP")
        str_full = request[str_start + 6:str_end - 1]

        options = {}
        temp_option = []
        temp_selector = ""

        for i, letter in enumerate(str_full):
            if letter == "=":
                options["".join(temp_option)] = []
                temp_selector = "".join(temp_option)
                temp_option = []
            elif letter == "&":
                options[temp_selector] = "".join(temp_option)
                temp_selector = ""
                temp_option = []
            elif i + 1 >= len(str_full):
                temp_option.append(letter)
                options[temp_selector] = "".join(temp_option)
            else:
                temp_option.append(letter)

        return options


    def set_options(self, parsed_request):
        """
        Takes a parsed_request as a dict and adjusts light options based on the
        arguments in the request.
        """
        if "quickselect" in parsed_request or parsed_request["fadespeed"] == "0":
            self.fade = False

            request_quickselect_option = parsed_request["quickselect"]
            request_brightness = int(parsed_request["brightness"]) / 100
            color = [int(value * request_brightness) for value in Main.quickselect[request_quickselect_option]]
            colors = [color for i in range(2)]
            print("\nrequest_option: {}, request_brightness: {}, color: {}".format(request_quickselect_option, request_brightness, color))

            self.fade_along.set_incremental_colors(colors)
            self.fade_along.cycle_lights()
        # else:
        #     self.fade = True
        #     self.fade_speed = int(parsed_request["fadespeed"])


    def return_homepage(self):
        try:
            with open("index.html", 'rb') as infile:
                response_body = infile.read()
        except OSError:
            response_body = b"No index file found..."

        return response_body


    def server_connect(self, server_socket):
        r, _, __, = select.select((server_socket,), (), (), 0.02)
        if r:
            for _ in r:
                client, client_addr = server_socket.accept()
                try:
                    print("\nConnected to client at {}".format(client_addr))
                    request = client.recv(4096)
                    print(request)
                    print()

                    if "app.js" in request:
                        try:
                            with open("app.js", 'rb') as infile:
                                response_body = infile.read()
                        except OSError:
                            response_body = b"alert('No JS found')"

                        response_header = b"HTTP/1.0 200 OK\nContent-Type: application/javascript\r\n\r\n"
                    elif "style.css" in request:
                        try:
                            with open("style.css", 'rb') as infile:
                                response_body = infile.read()
                        except OSError:
                            response_body = b"body { background: blue; height: 100vh; width: 100vw; }"

                        response_header = b"HTTP/1.0 200 OK\nContent-Type: text/css\r\n\r\n"
                    elif "GET /?" in request:
                        self.set_options(self.parse_request(request))

                        response_body = self.return_homepage()
                        response_header = b"HTTP/1.0 302 OK\nContent-Type: text/html\r\n\r\n"                    
                    else:
                        response_body = self.return_homepage()
                        response_header = b"HTTP/1.0 200 OK\nContent-Type: text/html\r\n\r\n"

                    # print(response_header + response_body)
                    client.send(response_header)
                    client.sendall(response_body)
                    client.close()                
                except OSError as e:
                    print(e)


    def do_connect(self):        
        Main.sta_if.connect("Lee's Wi-Fi Network", "Ramborox21")
        if Main.sta_if.isconnected():
            print("\nConnected to wifi:")
            print("\n{}\n".format(Main.sta_if.ifconfig()))


    def main(self):
        try:
            while True:
                gc.collect()

                # Responsible for trying to connect to wifi
                if ticks_ms() - self.connect_start_time >= 500:
                    if self.try_connect_counter <= 5 and not Main.sta_if.isconnected():
                        print("\nATTTEMPTing to connect to wifi")
                        self.do_connect()
                        self.try_connect_counter += 1

                    self.connect_start_time = ticks_ms()

                self.server_connect(self.socket)
                        


                # Responsible for moving the fade colors along the ball
                if self.fade and ticks_ms() - self.fade_start_time >= Main.light_options["fadespeed"][self.fade_speed % 9]:
                    self.fade_along_offset += 1
                    self.fade_along.cycle_lights(self.fade_along_offset)

                    self.fade_start_time = ticks_ms()

                # if ticks_ms() - fade_counter_start_time >= 3000:
                #     fade_speed += 1
                #     fade_counter_start_time = ticks_ms()
                #     print("\nFade Speed: {}".format(fade_speed))
        except KeyboardInterrupt:
            self.socket.close()


main = Main()
main.main()