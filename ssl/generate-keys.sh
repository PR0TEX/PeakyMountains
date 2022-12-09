#!/bin/sh

mkdir -p keys

openssl req \
  -x509 \
  -nodes \
  -new \
  -sha256 \
  -days 1024 \
  -newkey rsa:2048 \
  -keyout keys/RootCA.key \
  -out keys/RootCA.pem \
  -subj "/C=US/CN=Example-Root-CA"

openssl x509 \
  -outform pem \
  -in keys/RootCA.pem \
  -out keys/RootCA.crt

openssl req \
  -new \
  -nodes \
  -newkey rsa:2048 \
  -keyout keys/localhost.key \
  -out keys/localhost.csr \
  -subj "/C=US/ST=YourState/L=YourCity/O=Example-Certificates/CN=localhost.local"

openssl x509 \
  -req \
  -sha256 \
  -days 1024 \
  -in keys/localhost.csr \
  -CA keys/RootCA.pem \
  -CAkey keys/RootCA.key \
  -CAcreateserial \
  -extfile domains.ext \
  -out keys/localhost.crt
