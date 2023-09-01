#!/bin/bash

# Nombre de la imagen del contenedor
IMAGE_NAME="server"  # Cambia esto al nombre de tu imagen Docker

# Puerto en el que se ejecuta tu servidor en el contenedor
CONTAINER_PORT=12346

# Buscar el contenedor por el nombre de la imagen
CONTAINER_ID=$(docker ps -qf "ancestor=$IMAGE_NAME")

# Verificar si se encontró el contenedor
if [ -z "$CONTAINER_ID" ]; then
  echo "No se encontró ningún contenedor Docker con la imagen '$IMAGE_NAME' en ejecución."
  exit 1
else
  echo "Si encontro" $CONTAINER_ID
fi

# Obtener la dirección IP del contenedor
CONTAINER_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $CONTAINER_ID)

# Verificar si el contenedor Docker está en ejecución
if [ -z "$CONTAINER_IP" ]; then
  echo "No se pudo obtener la dirección IP del contenedor Docker."
  exit 1
else
  echo "Servidor corriendo en" $CONTAINER_IP
fi



# Intentar conectarse al servidor en el contenedor utilizando netcat
if nc -z -v -w 5 $CONTAINER_IP $CONTAINER_PORT; then
  echo "El servidor en el contenedor Docker con la imagen '$IMAGE_NAME' ($CONTAINER_IP) está funcionando correctamente en el puerto $CONTAINER_PORT."
  exit 0
else
  echo "No se pudo conectar al servidor en el contenedor Docker con la imagen '$IMAGE_NAME' ($CONTAINER_IP) en el puerto $CONTAINER_PORT."
  exit 1
fi