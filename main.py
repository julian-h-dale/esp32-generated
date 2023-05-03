import network
import usocket as socket
import uos

# Read the WiFi network credentials from the environment variables
ssid = uos.environ.get('SSID')
password = uos.environ.get('PASSWORD')

# Set up the WiFi network
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

# Wait for the connection to be established
while not station.isconnected():
    pass

# Define the HTML content to be displayed on the homepage
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>ESP32 Web Server</title>
    </head>
    <body>
        <h1>Julian Dale</h1>
    </body>
</html>
"""


# Define the function that handles incoming client requests
def handle_client(client_socket):
    # Receive the client's HTTP request
    request = client_socket.recv(1024)

    # Send the HTTP response with the HTML content
    response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + html
    client_socket.send(response)

    # Close the client socket
    client_socket.close()


# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 80))
server_socket.listen(1)

# Wait for incoming client requests
while True:
    client_socket, addr = server_socket.accept()
    handle_client(client_socket)
