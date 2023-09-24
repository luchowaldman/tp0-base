# Usa una imagen base de Linux, por ejemplo, Ubuntu
FROM ubuntu:latest

# Instala netcat
RUN apt-get update && apt-get install -y netcat

COPY /testServer/testserverendock.sh /testserver.sh

RUN chmod +x /testserver.sh

