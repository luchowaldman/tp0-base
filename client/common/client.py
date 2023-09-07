import socket
import logging
import signal
import sys
from common.mensajeserver import TipoMensajeServer
from common.serverdecoder import ServerDecoder
from common.encoder import ApuestaEncoder
from common.apuesta import Apuesta


class Client:
    def __init__(self, servidor_host, servidor_puerto, agencia):
        self.servidor_host = servidor_host
        self.servidor_puerto = servidor_puerto
        self.agencia = agencia
        self.ganadores = []
        self.cliente_socket = None

    def conectar(self):
        try:
            # Conexión al servidor
            self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.cliente_socket.connect((self.servidor_host, self.servidor_puerto))
        except ConnectionRefusedError:
            logging.error("Error: No se pudo conectar al servidor.")
            exit(1)
        except Exception as e:
            logging.error(f"Error: {e}")
            exit(1)

    def enviar_finapuestas(self):
        mensaje = ApuestaEncoder.encode_finapuestas(self.agencia)
        try:
            logging.debug(f"action: send-fin-apuestas  {mensaje}")
            # Envío del mensaje al servidor
            self.cliente_socket.sendall(mensaje.encode())


            # Recepción de la confirmación del servidor
            respuesta = self.LeerDatos(1)
            logging.debug(f"action: recepcion respuesta  {respuesta}")
            mensajeservidor = ServerDecoder.decode_mensaje(respuesta)
            return mensajeservidor.tipo == TipoMensajeServer.FIN_OK

        except Exception as e:
            logging.error(f"Error al enviar mensaje: {e}")
            return None

    def LeerDatos(self, caracteres):
        datos = self.cliente_socket.recv(caracteres).decode('utf-8')
        while (len(datos) < caracteres):                        
            datos  = datos + self.cliente_socket.recv(caracteres - len(datos)).decode('utf-8')
        return datos
  
    def get_ganadores(self):
        return self.ganadores
    
    def leer_ganadores(self):
        total_ganadores_str = self.LeerDatos(5)
        self.ganadores = ServerDecoder.decode_ganadores(self.LeerDatos(int(total_ganadores_str) * 8))
        

    def enviar_consultaganador(self):
        mensaje = ApuestaEncoder.encode_consultaganador(self.agencia)
        try:
            logging.debug(f"action: send-consulta ganador  {mensaje}")
            # Envío del mensaje al servidor
            self.cliente_socket.sendall(mensaje.encode())


            # Recepción de la respuesta del servidor
            respuesta = self.LeerDatos(1)
            logging.debug(f"action: recepcion respuesta  {respuesta}")
            mensajeservidor = ServerDecoder.decode_mensaje(respuesta)
            if mensajeservidor.tipo == TipoMensajeServer.CON_SORTEO:
                self.leer_ganadores()
            return mensajeservidor.tipo == TipoMensajeServer.CON_SORTEO

        except Exception as e:
            logging.error(f"Error al enviar mensaje: {e}")
            return None



    def enviar_apuestas(self, apuesta: Apuesta):
        mensaje = ApuestaEncoder.encode_vector(apuesta, self.agencia)
        try:
            # Envío del mensaje al servidor
            self.cliente_socket.sendall(mensaje.encode())

        except Exception as e:
            print(f"Error al enviar la apuesta: {e}")
            return None

    def cerrar_conexion(self):
        # Cierre del socket
        self.cliente_socket.close()