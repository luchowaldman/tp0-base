from enum import Enum

class TipoMensajeServer(Enum):
    FIN_OK = 1
    SIN_SORTEO = 2
    CON_SORTEO = 3

class MensajeServer:
    def __init__(self, tipo):
        if tipo not in TipoMensajeServer:
            raise ValueError("El tipo de mensaje no es válido")
        
        self.tipo = tipo