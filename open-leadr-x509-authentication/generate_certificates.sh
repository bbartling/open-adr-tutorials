#!/bin/bash

# chmod +x generate_certificates.sh
# ./generate_certificates.sh

set -e

# Define the passphrase
passphrase="slipstream_openadr_testing"

echo "Generating the CA key"
openssl genrsa -des3 -passout pass:$passphrase -out ca.key 4096

echo "Generating the CA cert"
openssl req -x509 -new -subj "/C=NL/ST=Other/O=OpenLEADR Dummy CA/CN=dummy-ca.openleadr.org" -nodes -key ca.key -passin pass:$passphrase -sha256 -days 3650 -out ca.crt

echo "Generating the VTN key"
openssl genrsa -des3 -passout pass:$passphrase -out vtn_key.pem 2048

echo "Generating the VTN Certificate Signing Request"
openssl req -new -sha256 -key vtn_key.pem -passin pass:$passphrase -subj "/C=NL/ST=Other/O=OpenLEADR Dummy VTN/CN=localhost" -out vtn.csr

echo "Signing the VTN CSR, generating the VTN certificate"
openssl x509 -req -in vtn.csr -CA ca.crt -CAkey ca.key -passin pass:$passphrase -CAcreateserial -out vtn_cert.pem -days 3650 -sha256

echo "Generating the VEN key"
openssl genrsa -des3 -passout pass:$passphrase -out ven_key.pem 2048

echo "Generating the VEN Certificate Signing Request"
openssl req -new -sha256 -key ven_key.pem -passin pass:$passphrase -subj "/C=NL/ST=Other/O=OpenLEADR Dummy VEN/CN=dummy-ven.openleadr.org" -out ven.csr

echo "Signing the VTN CSR, generating the VEN certificate"
openssl x509 -req -in ven.csr -CA ca.crt -CAkey ca.key -passin pass:$passphrase -CAcreateserial -out ven_cert.pem -days 3650 -sha256

echo "Certificate generation complete. VEN and VTN certificates and keys are created."
