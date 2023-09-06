import configparser
import sys
import yaml
import os
import shutil



def modificar_valor_agencia(archivo_ini, nuevo_valor_agencia):
    # Crear un objeto ConfigParser
    config = configparser.ConfigParser()

    # Leer el archivo INI
    config.read(archivo_ini)

    # Actualizar el valor de AGENCIA
    config.set('DEFAULT', 'AGENCIA', str(nuevo_valor_agencia))

    # Escribir los cambios de vuelta al archivo
    with open(archivo_ini, 'w') as configfile:
        config.write(configfile)




def crear_carpeta_y_copiar_archivos(ID_CLIENT):
    # Directorio base donde se encuentra este script
    directorio_base = os.getcwd()
    
    # Crear la carpeta en ./volumen_client{ID_CLIENT}
    carpeta_destino = os.path.join(directorio_base, f'./volumen_client{ID_CLIENT}')
    os.makedirs(carpeta_destino, exist_ok=True)
    
    
    try:
        # Copiar agency-{ID_CLIENT}.csv desde ./data        
        shutil.copy(f'./.data/agency-{ID_CLIENT}.csv', carpeta_destino)
        # Copiar config_client.ini desde ./volumen
        shutil.copy('./volumen/config_cliente.ini', carpeta_destino)
        archivo_destino = os.path.join(carpeta_destino, 'agency.csv')
        os.rename(os.path.join(carpeta_destino, f'agency-{ID_CLIENT}.csv'), archivo_destino)

        #setea el valor de agencia
        archivo_ini = f'./volumen_client{ID_CLIENT}/config_cliente.ini'        
        modificar_valor_agencia(archivo_ini, ID_CLIENT)
        
    except FileNotFoundError:
        print("No se encontraron los archivos de origen.")
    except Exception as e:
        print(f"Error al copiar archivos: {str(e)}")


def generate_docker_compose(client_count):
    docker_compose = {
        'version': '3.9',
        'name': 'tp0',
        'services': {
            'server': {
                'container_name': 'server',
                'image': 'server:latest',
                'entrypoint': 'python3 /main.py',
                'environment': [
                    'PYTHONUNBUFFERED=1',
                    'LOGGING_LEVEL=DEBUG'
                ],
                'networks': ['testing_net'],
                'volumes': ['./volumen:/volumen']
            }
        },
        'networks': {
            'testing_net': {
                'ipam': {
                    'driver': 'default',
                    'config': [
                        {'subnet': '172.25.125.0/24'}
                    ]
                }
            }
        }
    }

    for i in range(1, client_count + 1):
        crear_carpeta_y_copiar_archivos(i)
        client_name = f'client{i}'
        docker_compose['services'][client_name] = {
            'container_name': client_name,
            'image': 'client:latest',
            'entrypoint': 'python3 /main.py',
            'environment': [
                    'PYTHONUNBUFFERED=1',
                    'LOGGING_LEVEL=DEBUG'
            ],
            'networks': ['testing_net'],
            'depends_on': ['server'],
            'volumes': [f'./volumen_client{i}:/volumen']
            
        }

    return docker_compose

def write_docker_compose_yaml(docker_compose, filename='docker-compose-dev.yaml'):
    with open(filename, 'w') as yaml_file:
        yaml.dump(docker_compose, yaml_file, default_flow_style=False)

if __name__ == "__main__":
    generate_docker_compose(5)
    if len(sys.argv) != 2:
        print("Uso: python script.py <numero_de_clientes>")
        sys.exit(1)

    try:
        client_count = int(sys.argv[1])
        if client_count < 0:
            print("El número de clientes debe ser un número positivo.")
            sys.exit(1)

        docker_compose = generate_docker_compose(client_count)
        write_docker_compose_yaml(docker_compose)
        print(f"Se ha creado o actualizado el archivo 'docker-compose-dev.yaml' con {client_count} clientes.")
    except ValueError:
        print("El número de clientes debe ser un número entero.")
        sys.exit(1)
