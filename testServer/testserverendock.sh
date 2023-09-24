#!/bin/bash

# Puerto en el que se ejecuta tu servidor en el contenedor
CONTAINER_PORT=12346

TEST_STRING="Texto_de_Prueba"  

CONTAINER_IP="server"

echo "Iniciando consulta"


# Intentar conectarse al servidor en el contenedor utilizando netcat
if nc -z -v -w 5 "$CONTAINER_IP" "$CONTAINER_PORT"; then
  echo "El servidor en el contenedor Docker con la imagen '$IMAGE_NAME' ($CONTAINER_IP) está funcionando correctamente en el puerto $CONTAINER_PORT."

  # Enviar el texto de prueba al servidor
  echo -n "$TEST_STRING" | nc "$CONTAINER_IP" "$CONTAINER_PORT" > response.txt

  # Leer la respuesta del servidor
  RESPONSE=$(cat response.txt)

  # Comparar la respuesta del servidor con el texto de prueba
  if [ "$RESPONSE" == "$TEST_STRING" ]; then
    echo "El servidor devolvió la respuesta esperada: '$RESPONSE'."
    rm response.txt
    exit 0
  else
    echo "El servidor devolvió una respuesta inesperada: '$RESPONSE'."
    rm response.txt
    exit 1
  fi

else
  echo "No se pudo conectar al servidor "
  exit 1
fi