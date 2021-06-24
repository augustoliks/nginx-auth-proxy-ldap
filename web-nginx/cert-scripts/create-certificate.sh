#!/bin/bash

# openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
openssl req -x509 -nodes \
   -days 365 \
   -newkey rsa:2048 \
   -keyout cert.key \
   -out cert.crt \
   -subj "/C=BR/ST=Sao Paulo/L=Jacarei/O=Github/OU=Tecnology/CN=localhost/emailAddress=carlos.neto.dev@gmail.com"
exit


## requirements
# httpd-tools

## doc
#    openssl: This is the basic command line tool for creating and managing OpenSSL certificates, keys, and other files.
#    req: This subcommand specifies that we want to use X.509 certificate signing request (CSR) management. The “X.509” is a public key infrastructure standard that SSL and TLS adheres to for its key and certificate management. We want to create a new X.509 cert, so we are using this subcommand.
#    -x509: This further modifies the previous subcommand by telling the utility that we want to make a self-signed certificate instead of generating a certificate signing request, as would normally happen.
#    -nodes: This tells OpenSSL to skip the option to secure our certificate with a passphrase. We need Nginx to be able to read the file, without user intervention, when the server starts up. A passphrase would prevent this from happening because we would have to enter it after every restart.
#    -days 365: This option sets the length of time that the certificate will be considered valid. We set it for one year here.
#    -newkey rsa:2048: This specifies that we want to generate a new certificate and a new key at the same time. We did not create the key that is required to sign the certificate in a previous step, so we need to create it along with the certificate. The rsa:2048 portion tells it to make an RSA key that is 2048 bits long.
#    -keyout: This line tells OpenSSL where to place the generated private key file that we are creating.
#    -out: This tells OpenSSL where to place the certificate that we are creating.
