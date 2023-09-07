
from common.mensajeserver import MensajeServer, TipoMensajeServer

class ServerDecoder:


    @staticmethod
    def decode_mensaje(msg):
        if msg.startswith("O"):
            return MensajeServer(TipoMensajeServer.FIN_OK)
        if msg.startswith("N"):
            return MensajeServer(TipoMensajeServer.SIN_SORTEO)
        if msg.startswith("R"):
            return MensajeServer(TipoMensajeServer.CON_SORTEO)
    
    def decode_ganadores(msg):
        dnis = [msg[i:i+8] for i in range(0, len(msg), 8)]
        return dnis
