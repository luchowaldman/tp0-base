from enum import Enum

class TipoMensaje(Enum):
    ENVIA_APUESTAS = 1
    FIN_ENVIO = 2
    CONSULTA_GANADOR = 3

class Mensaje:
    def __init__(self, tipo, id_agencia):
        if tipo not in TipoMensaje:
            raise ValueError("El tipo de mensaje no es válido")
        
        self.tipo = tipo
        self.id_agencia = id_agencia
