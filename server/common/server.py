from codecs import getencoder
import socket
import logging
import signal
import sys
import threading
from common.decoder import Bet, BetDecoder
from common.utils import has_won, load_bets, store_bets
from common.mensaje import TipoMensaje
from common.betencoder import BetEncoder


class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)
        self._running = True
        self._mensajeganadores = ""
        self.clientes_sinapuestas = listen_backlog
        self.lock_archivo = threading.Lock()
        self.lock_clientes_sinapuestas = threading.Lock()
        self._active_threads = []
                
        # Register a signal handler for SIGTERM
        signal.signal(signal.SIGTERM, self.handle_sigterm)



    def run(self):
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """

        # TODO: Modify this program to handle signal to graceful shutdown
        # the server
        try:
            while self._running:
                self.__cleanup_threads()
                client_sock = self.__accept_new_connection()
                hilo = threading.Thread(target=self.__handle_client_connection,
                                        args=(client_sock,))
                hilo.start()
                self._active_threads.append(hilo)
        except OSError as e:
            if e.errno == 9:
                logging.log(f'Salida GRACEFUL')
            else:
                # Manejar otros casos de OSError si es necesario
                raise e
        except Exception as ex:
            # Captura otras excepciones generales si es necesario
            raise ex

        self._server_socket.close()


    def __cleanup_threads(self):
        # Verificar los hilos que han terminado y unirlos
        threads_to_remove = []
        for thread in self._active_threads:
            if not thread.is_alive():
                thread.join()
                threads_to_remove.append(thread)

        # Eliminar los hilos terminados de la lista
        for thread in threads_to_remove:
            self._active_threads.remove(thread)

    def LeerDatos(self, client_sock, caracteres):
        datos = client_sock.recv(caracteres).decode('utf-8')
        while (len(datos) < caracteres):                        
            datos  = datos + client_sock.recv(caracteres - len(datos)).decode('utf-8')
        return datos
                    

    def EscribirDatos(self, client_sock, mensaje):
        mensaje_codificado = mensaje.encode('utf-8')
        total_enviado = 0

        while total_enviado < len(mensaje_codificado):
            bytes_enviados = client_sock.send(mensaje_codificado[total_enviado:])            
            total_enviado += bytes_enviados


    def __handle_client_connection(self, client_sock):
        """
        Read message from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        try:
            com_terminada = False
            
            while not com_terminada:
                msg = self.LeerDatos(client_sock, 6)
                mensaje = BetDecoder.decode_mensaje(msg)
                if mensaje.tipo == TipoMensaje.ENVIA_APUESTAS:
                    agencia = int(msg[1:])
                    # leo 5 caracteres para saber cuantas apuestas se van a enviar
                    total = self.LeerDatos(client_sock, 5)
                    cantidad = int(total)
                    tamano_apuesta = (cantidad * BetDecoder.tamanio_apuesta())
                    apuestas_recibidas = self.LeerDatos(client_sock, tamano_apuesta)
                    apuestas = BetDecoder.decode_vector(apuestas_recibidas, agencia)
                    with self.lock_archivo:
                        store_bets(apuestas)
                elif mensaje.tipo == TipoMensaje.FIN_ENVIO:
                    # Termino de enviar apuestas
                    with self.lock_clientes_sinapuestas:
                        self.clientes_sinapuestas = self.clientes_sinapuestas - 1
                    com_terminada = True
                    self.EscribirDatos(client_sock, BetEncoder.FinApuestasOk())
                elif mensaje.tipo == TipoMensaje.CONSULTA_GANADOR:
                    # Termino de enviar apuestas
                    com_terminada = True
                    with self.lock_clientes_sinapuestas:
                        sinsorteo = self.clientes_sinapuestas > 0
                    if (sinsorteo):
                        self.EscribirDatos(client_sock, BetEncoder.SinSorteo())
                    else:
                        with self.lock_archivo:
                            bets = load_bets()
                        bets_winner = []
                        for bet in bets:
                            if has_won(bet):
                                if bet.agency == mensaje.id_agencia:
                                    bets_winner.append(bet)
                        self.EscribirDatos(client_sock, BetEncoder.ConSorteo(bets_winner))

        except OSError as e:
            logging.error("action: receive_message | result: fail | error: {e}")
        finally:
            client_sock.close()

    def handle_sigterm(self, signum, frame):
        """
        Signal handler for SIGTERM

        This method will be called when the server receives a SIGTERM signal.
        It sets the _running flag to False, which will gracefully terminate the server.
        """
        logging.info("Received SIGTERM signal. Gracefully shutting down...")
        self._running = False
        self._server_socket.close()

    def __accept_new_connection(self):
        """
        Accept new connections

        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

        # Connection arrived
        logging.info('action: accept_connections | result: in_progress')
        c, addr = self._server_socket.accept()
        logging.info(f'action: accept_connections | result: success | ip: {addr[0]}')
        return c
