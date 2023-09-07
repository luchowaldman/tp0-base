import logging
import time
from common.apuesta import Apuesta
import signal

class TransmicionController:
    def __init__(self, client):
        self.client = client
        self.ganadores = []
        self._running = True

        # Register a signal handler for SIGTERM
        signal.signal(signal.SIGTERM, self.handle_sigterm)


    def handle_sigterm(self, signum, frame):
        """
        Signal handler for SIGTERM

        This method will be called when the server receives a SIGTERM signal.
        It sets the _running flag to False, which will gracefully terminate the server.
        """
        logging.info("Received SIGTERM signal. Gracefully shutting down...")
        self._running = False

    def TrasmitirArchivo(self, archivo_apuestas, apuestas_por_envio):
        self.client.conectar()
        apuestas = []
        resultado_finapuestas = ""
        apuestas_enviadas = 0

        try:

            with open(archivo_apuestas, 'r') as archivo:
                for linea in archivo:
                    partes = linea.strip().split(',')
                    if len(partes) == 5:
                        apuesta = Apuesta(partes[0], partes[1], partes[2], partes[3], partes[4])
                        apuestas.append(apuesta)
                        apuestas_enviadas = apuestas_enviadas + 1
                        if len(apuestas) >= apuestas_por_envio:
                            self.client.enviar_apuestas(apuestas)
                            apuestas = []  # Vaciar el vector de apuestas después de enviarlas
                    if not self._running:
                        break            
                if not self._running:    
                    self.client.enviar_apuestas(apuestas)
            resultado_finapuestas = self.client.enviar_finapuestas()
        except Exception as e:
            logging.error(e)
        finally:
            self.client.cerrar_conexion()

        if (not resultado_finapuestas):
            logging.error("El archivo no se trasmitio correctamiente")
            exit(1)
        else:
            logging.info(f"{apuestas_enviadas} Apuestas transmitidos correctamente")
    
    def VerificarGanadores(self):
        #Voy a buscar ganadores. Si aun no estan espero un tiempo expotencial hasta que esten
        tiempo_espera = 1
        resultado_obtenido = False
        while not resultado_obtenido and self._running:
            self.client.conectar()
            resultado_obtenido = self.client.enviar_consultaganador()
            self.client.cerrar_conexion()
            if not resultado_obtenido:
                logging.debug(f"Esperando el resultado del sorteo por {tiempo_espera} segundos")
                time.sleep(tiempo_espera)
                tiempo_espera = tiempo_espera * 2
            
        ganadores = self.client.get_ganadores()
        logging.info(f"action: consulta_ganadores | result: success | cant_ganadores: {len(ganadores)}")


                
            

            

        
