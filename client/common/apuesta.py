class Apuesta:
    def __init__(self, agencia: str, nombre: str, apellido: str, dni: str, nacimiento: str, numero: str):
        self.agencia = int(agencia)
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.nacimiento = nacimiento
        self.numero = numero
