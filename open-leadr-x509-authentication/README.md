# open-leadr-x509-authentication-tutorial


[!snip](/images/x509-openleadr-auth-snip.JPG)

# Writeup
* [linkdedin story](https://www.linkedin.com/posts/ben-bartling-510a0961_demandresponse-energymanagement-openadr-activity-7134285763650748416-7Ux3?utm_source=share&utm_medium=member_desktop)

# Generate Certs

* Make sure you come up with some `passphrase` string which is also stored on the server as well.

```bash
#!/bin/bash

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
```

Set correct permissions to run the bash script:
```bash
chmod +x generate_certificates.sh
```

Run the bash script with:
```bash
./generate_certificates.sh
```

# VEN APP
On the openleadr client and server scripts which are in the same directory as the bash script output x509 files make sure the client is defined like:
```python
async def main():
    client = OpenADRClient(ven_name='ven_id_123',
                        vtn_url='https://localhost:8080/OpenADR2/Simple/2.0b',
                        cert='ven_cert.pem',
                        key='ven_key.pem',
                        passphrase='slipstream_openadr_testing',
                        ca_file='ca.crt')
```
When the client app starts copy the output of the VEN `fingerprint` which is used in the server app setup.
# VTN APP
One the server openleadr app make sure its defined like:
```python
 Create the server object with X.509 certificate and private key
server = OpenADRServer(vtn_id='BensVTN',
                       http_cert='vtn_cert.pem',
                       http_key='vtn_key.pem',
                       http_ca_file='ca.crt',
                       http_port=8080,
                       http_host='0.0.0.0',
                       http_path_prefix='/OpenADR2/Simple/2.0b',
                       requested_poll_freq=timedelta(seconds=10),
                       ven_lookup=ven_lookup)
```

As well as putting the VEN fingerprint inside a `ven_lookup` function which is a requirement by `OPENleadr` like this:
```python
def ven_lookup(ven_id):

    if ven_id == 'ven_id_123':
        return {'ven_id': 'ven_id_123',
                'ven_name': 'MyVEN',
                'fingerprint': '28:36:73:32:53:6C:84:C7:89:95',
                'registration_id': 'reg_id_123'}
    else:
        return None  # Return None if the VEN is not found
```

