import usocket as socket
import uselect as select
import ure
import gc
from utime import ticks_ms

light_options = {
    "quickselect": ["white", "yellow", "red", "blue", "green", "fade"],
    "brightness": [i for i in range(1, 101)],
    "fade_speed": [i for i in range(1, 10)]
}

def start_server():
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

def parse_request(request):
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

def return_homepage():
    try:
        with open("index.html", 'rb') as infile:
            response_body = infile.read()
    except OSError:
        response_body = b"No index file found..."

    return response_body

def server_connect(server_socket):
    r, _, __, = select.select((server_socket,), (), (), 0.02)
    if r:
        for _ in r:
            client, client_addr = server_socket.accept()
            try:
                request_return = None

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

                    response_header = b"HTTP/1.1 200 OK\nContent-Type: application/javascript\r\n\r\n"
                elif "style.css" in request:
                    try:
                        with open("style.css", 'rb') as infile:
                            response_body = infile.read()
                    except OSError:
                        response_body = b"body { background: blue; height: 100vh; width: 100vw; }"

                    response_header = b"HTTP/1.1 200 OK\nContent-Type: text/css\r\n\r\n"
                elif "GET /?" in request:
                    # response_body = b"Ok, all good."
                    request_return = parse_request(request)
                    response_body = return_homepage()
                    response_header = b"HTTP/1.1 200 OK\nContent-Type: text/html\r\n\r\n"                    
                else:
                    response_body = return_homepage()
                    response_header = b"HTTP/1.1 200 OK\nContent-Type: text/html\r\n\r\n"

                

                # print(response_header + response_body)
                client.send(response_header)
                client.sendall(response_body)
                client.close()

                return request_return

            
            except OSError as e:
                print(e)
    else:
        return None