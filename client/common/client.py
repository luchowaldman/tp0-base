import socket
import logging
import signal
import sys
from common.encoder import ApuestaEncoder
from common.apuesta import Apuesta


class Client:
    def __init__(self, servidor_host, servidor_puerto):
        self.servidor_host = servidor_host
        self.servidor_puerto = servidor_puerto
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def conectar(self):
        try:
            # Conexión al servidor
            self.cliente_socket.connect((self.servidor_host, self.servidor_puerto))
        except ConnectionRefusedError:
            print("Error: No se pudo conectar al servidor.")
            exit(1)
        except Exception as e:
            print(f"Error: {e}")
            exit(1)

    
    def enviar_apuesta(self, apuesta: Apuesta):
        
        
        mensaje = ApuestaEncoder.encode(apuesta)
        try:
            logging.debug(f"action: send-message  {mensaje}")

            # Envío del mensaje al servidor
            self.cliente_socket.sendall(mensaje.encode())

            # Recepción de la confirmación del servidor
            respuesta = self.cliente_socket.recv(1024)
            logging.debug(f"action: recepcion respuesta Ok  {respuesta}")
            return respuesta.decode()
        except Exception as e:
            print(f"Error al enviar la apuesta: {e}")
            return None

    def cerrar_conexion(self):
        # Cierre del socket
        self.cliente_socket.close()