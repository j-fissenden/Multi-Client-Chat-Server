# Multi-Client-Chat-Server
This project is a Python server that operates on local host and has clients that can connect, message, private message and all content is encrypted.
The purpose of this is for fun, and learning in a  practical aspect from two of my university modules on network communications and cryptography.

## Bash to generate server.key and server.crt
> openssl genpkey -algorithm RSA -out server.key -aes256

> openssl req -new -key server.key -out server.crt
