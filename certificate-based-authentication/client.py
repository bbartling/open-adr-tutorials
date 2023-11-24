import socket
import ssl
import time
import random

# Client certificate and private key
client_certfile = "client_certificate.pem"
client_keyfile = "client_private_key.pem"

while True:
    try:
        # Generate a random power value
        power_value = round(random.uniform(100, 200))

        # Create a new socket and connect to the server for each request
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 8888))

        # Wrap the socket in SSL
        ssl_socket = ssl.wrap_socket(
            client_socket,
            keyfile=client_keyfile,
            certfile=client_certfile,
            cert_reqs=ssl.CERT_REQUIRED,
            ca_certs="server_certificate.pem",
        )

        # Send a check event request along with the power value to the server
        message = f"check_event|{power_value}"
        ssl_socket.send(message.encode())

        # Print the power value sent to the server
        print("Sending report value of power meter in report: ", power_value)

        # Receive the server's response
        response = ssl_socket.recv(1024).decode()

        if not response.lower() == "no openadr event found.":
            print("Received ADR Server Response:", response)

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        # Close the SSL connection
        ssl_socket.close()

    # Wait for 10 seconds before checking again
    time.sleep(10)
