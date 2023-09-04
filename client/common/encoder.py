class ApuestaEncoder:
    @staticmethod
    def encode(apuesta):
        # Verificar y ajustar la longitud de cada campo
        agencia = str(apuesta.agencia).zfill(5)[:5]
        nombre = apuesta.nombre[:10].ljust(10)
        apellido = apuesta.apellido[:10].ljust(10)
        dni = apuesta.dni.zfill(8)[:8]
        nacimiento = apuesta.nacimiento[:10].ljust(10)
        numero = apuesta.numero.zfill(4)[:4]

        # Combinar los campos en una cadena codificada
        encoded_apuesta = f"{agencia}{nombre}{apellido}{dni}{nacimiento}{numero}"

        return encoded_apuesta
