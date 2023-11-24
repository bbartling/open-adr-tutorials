# certificate-based-authentication-tutorial
This hands-on exploration and tutorial guide covers client and server authentication techniques employed in demand response applications, specifically within OpenADR. It focuses on a client application (OpenADR VEN) situated within a building, which communicates with a cloud-based server or OpenADR VTN for authentication purposes.

In this guide, we'll walk you through the process of creating client and server certificate and private key files for simulating secure communication in OpenADR or similar applications. These certificates will enable secure authentication and communication between a client (VEN - Virtual End Node) and a server (VTN - Virtual Top Node).

[snip](/images/cert-based-auth-snip.JPG)

# Prerequisites
1. **OpenSSL**: Ensure that OpenSSL is installed on your system. If it's not installed, you can download it from the official OpenSSL website or use your system's package manager to install it.

2. **Generate a Certificate Authority (CA)**
Before creating client and server certificates, you need to establish a Certificate Authority (CA) to issue and sign these certificates. You can either use a trusted public CA or set up your own CA for testing purposes. For this guide, we'll create a self-signed CA certificate and private key:

```bash
# Generate a CA private key
openssl genpkey -algorithm RSA -out ca_private_key.pem

# Create a self-signed CA certificate
openssl req -new -key ca_private_key.pem -x509 -out ca_certificate.pem
```

3. **Create the Server Certificate and Private Key**
Now, let's generate a server certificate and private key for the VTN (Virtual Top Node):
```bash
# Generate a private key for the server
openssl genpkey -algorithm RSA -out server_private_key.pem

# Create a Certificate Signing Request (CSR) for the server
openssl req -new -key server_private_key.pem -out server_csr.pem

# Sign the server CSR with your CA to create the server certificate
openssl x509 -req -in server_csr.pem -CA ca_certificate.pem -CAkey ca_private_key.pem -CAcreateserial -out server_certificate.pem
```

4. **Create the Client Certificate and Private Key**
Similarly, generate a client certificate and private key for the VEN (Virtual End Node):
```bash
# Generate a private key for the client
openssl genpkey -algorithm RSA -out client_private_key.pem

# Create a CSR for the client
openssl req -new -key client_private_key.pem -out client_csr.pem

# Sign the client CSR with your CA to create the client certificate
openssl x509 -req -in client_csr.pem -CA ca_certificate.pem -CAkey ca_private_key.pem -CAcreateserial -out client_certificate.pem
```
The file outputs should look like this:
```bash
$ ls
ca_certificate.pem  client_certificate.pem  client.py               server_private_key.pem
ca_certificate.srl  client_csr.pem          server_certificate.pem  server.py
ca_private_key.pem  client_private_key.pem  server_csr.pem
```

# Usage
With the generated certificate and private key files, you can simulate secure communication between the VTN (server) and VEN (client) in your OpenADR or similar application. Use these certificates to establish secure connections and implement authentication mechanisms as needed. First start the simulated VTN server in one SSH terminal:

```bash
$ python server.py
```

Which should then print:
```bash
Server is listening...
```
One a different terminal simulate the building side open ADR client app:
```bash
$ python server.py
```

# X.509 Certificate Overview
X.509 is a widely used standard for defining the format of public key certificates. In this simulation, X.509 certificates are used to enable secure communication between the client and server. Each entity (client and server) possesses its certificate and private key. The certificates are used for authentication, ensuring that the communicating parties can trust each other's identity. The client and server scripts utilize the OpenSSL library in Python to establish secure SSL/TLS connections, which rely on these certificates for encryption and authentication. The provided scripts demonstrate a basic client-server interaction, but in a real-world OpenADR scenario, they would be part of a more comprehensive demand response system.

# Security Note
In a production environment, follow best practices for certificate management and security. Consider using trusted CAs for real-world applications and automate certificate issuance and renewal.

Please customize the certificate details (e.g., common name, organization) and paths as needed for your specific use case. This guide provides a basic overview of certificate generation for educational purposes.

# Web app tutorial issues
When you use a web framework like Flask or Django to simulate open ADR which is actually used in the wild, the web framework typically relies on external libraries like OpenSSL and urllib3 to handle HTTPS connections. 
These libraries are more strict in their certificate verification, conforming to modern security standards and best practices. 
As a result, they are more likely to raise certificate verification errors, especially if your certificates are missing required fields like commonName or subjectAltName.

Most likely some error will pop up like an SSL certificate verification error in a web app-based implementation is due to these stricter verification checks. 
To make the web app work, you should update your certificates to include the necessary Subject Alternative Names (SANs) or modify your client code to match the hostname specified in your certificates, 
as mentioned in a previous response.

For learning purposes in summary, the socket-based implementation may be less strict in certificate verification compared to libraries used by web frameworks, which adhere to more rigorous security standards. 
It's essential to ensure that your certificates meet the necessary requirements for secure communication when using these libraries.