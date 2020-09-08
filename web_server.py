import usocket as socket
import uselect as select
import gc

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

def server_connect(server_socket):
    r, _, __, = select.select((server_socket,), (), (), 0)
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

                    response_header = b"HTTP/1.0 200 OK\nContent-Type: application/javascript\n\n"
                elif "style.css" in request:
                    try:
                        with open("style.css", 'rb') as infile:
                            response_body = infile.read()
                    except OSError:
                        response_body = b"body { background: blue; height: 100vh; width: 100vw; }"

                    response_header = b"HTTP/1.0 200 OK\nContent-Type: text/css\n\n"
                else:
                    try:
                        with open("index.html", 'rb') as infile:
                            response_body = infile.read()
                    except OSError:
                        response_body = b"No index file found..."
                    
                    response_header = b"HTTP/1.0 200 OK\nContent-Type: text/html\n\n"

                

                client.send(response_header)
                client.sendall(response_body)
                client.close()
            
            except OSError:
                pass