#!/usr/bin/env python3

from configparser import ConfigParser
from common.transmicioncontroller import TransmicionController
from common.client import Client
import logging
import os

def initialize_config():
    """ Parse env variables or config file to find program config params

    Function that search and parse program configuration parameters in the
    program environment variables first and the in a config file. 
    If at least one of the config parameters is not found a KeyError exception 
    is thrown. If a parameter could not be parsed, a ValueError is thrown. 
    If parsing succeeded, the function returns a ConfigParser object 
    with config parameters
    """

    config = ConfigParser(os.environ)
    # If config.ini does not exists original config object is not modified
    config.read("/volumen/config_cliente.ini")

    config_params = {}
    try:
        config_params["port"] = int(os.getenv('SERVER_PORT', config["DEFAULT"]["SERVER_PORT"]))
        config_params["listen_backlog"] = int(os.getenv('SERVER_LISTEN_BACKLOG', config["DEFAULT"]["SERVER_LISTEN_BACKLOG"]))
        config_params["logging_level"] = os.getenv('LOGGING_LEVEL', config["DEFAULT"]["LOGGING_LEVEL"])
        config_params["server_ip"] = os.getenv('SERVER_IP', config["DEFAULT"]["SERVER_IP"])


        config_params["agencia"] = int(os.getenv('AGENCIA', config["DEFAULT"]["AGENCIA"]))
        config_params["archivo_apuestas"] = os.getenv('ARCHIVO_APUESTAS', config["DEFAULT"]["ARCHIVO_APUESTAS"])
        config_params["apuestas_por_envio"] = int(os.getenv('APUESTAS_POR_ENVIO)', config["DEFAULT"]["APUESTAS_POR_ENVIO"]))
    except KeyError as e:
        raise KeyError("Key was not found. Error: {} .Aborting server".format(e))
    except ValueError as e:
        raise ValueError("Key could not be parsed. Error: {}. Aborting server".format(e))

    return config_params


def main():
    config_params = initialize_config()
    server_ip = config_params["server_ip"]
    port = config_params["port"]
    logging_level = config_params["logging_level"]

    initialize_log(logging_level)

    # Log config parameters at the beginning of the program to verify the configuration
    # of the component
    logging.debug(f"action: config | result: success | port: {port} | "
                  f"logging_level: {logging_level} | server ip: {server_ip}")

    # Initialize client
    agencia = config_params["agencia"]
    client = Client(server_ip, port, agencia)
    archivo_apuestas = config_params["archivo_apuestas"]
    apuestas_por_envio = config_params["apuestas_por_envio"]
    controlador = TransmicionController(client)
    controlador.TrasmitirArchivo(archivo_apuestas, apuestas_por_envio)
    controlador.VerificarGanadores()

    

        


def initialize_log(logging_level):
    """
    Python custom logging initialization

    Current timestamp is added to be able to identify in docker
    compose logs the date when the log has arrived
    """
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging_level,
        datefmt='%Y-%m-%d %H:%M:%S',
    )


if __name__ == "__main__":
    main()
