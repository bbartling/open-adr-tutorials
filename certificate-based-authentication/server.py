import socket
import ssl
import random
import xml.etree.ElementTree as ET


# Server certificate and private key
server_certfile = "server_certificate.pem"
server_keyfile = "server_private_key.pem"

# Create a socket and bind it to a specific address and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 8888))
server_socket.listen(5)

print("Server is listening...")


def check_for_openadr_event():
    return random.choice([True, False])


# generate a pretend open ADR event
def generate_openadr_event():
    root = ET.Element("oadrDistributeEvent")
    event = ET.Element("oadrEvent")
    event_id = ET.Element("eventID")
    event_id.text = "1"  # Replace with your event ID
    event.append(event_id)
    root.append(event)
    tree = ET.ElementTree(root)
    xml_str = ET.tostring(root, encoding="utf-8").decode()
    return xml_str


while True:
    client_socket, client_address = server_socket.accept()
    ssl_socket = ssl.wrap_socket(
        client_socket,
        keyfile=server_keyfile,
        certfile=server_certfile,
        server_side=True,
    )

    # Receive a request from the client
    data = ssl_socket.recv(1024).decode()
    command, power_value = data.split("|")

    if command.lower() == "check_event":
        print(
            f"Received check from client {client_address[0]}:{client_address[1]} with power value: {power_value} kW"
        )

        # Simulate checking for OpenADR event
        has_event = check_for_openadr_event()

        if has_event:
            # Push the event to the client
            ssl_socket.send(generate_openadr_event().encode())
        else:
            # Notify the client that no event exists
            ssl_socket.send("No OpenADR event found.".encode())

    # Close the SSL connection
    ssl_socket.close()
