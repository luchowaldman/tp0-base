# TP0: Docker + Comunicaciones + Concurrencia


### Ejercicio N°1:
Modificar la definición del DockerCompose para agregar un nuevo cliente al proyecto.

#### Solucion

El Yaml hay una parte en donde se definen los container a crear. Es la key "services". En esta teniamos definido client1 y server. Para agregar un cliente hay que copiar client1 y ajustar la propiedad container_name y la variable de entorno CLI_ID

### Ejercicio N°1.1:
Definir un script (en el lenguaje deseado) que permita crear una definición de DockerCompose con una cantidad configurable de clientes.


#### Solucion
Cree un script en Python (make-compose-yaml.py) que toma por parametro la cantidad de clientes Y crea un objeto con las propiedades name, version, networks y services. Esta ultima con un server ya creado. Luego se recorre un for y va agregando a services tantos clientes como se solicito. Por ultimo se genera el archivo con yaml.dump(...)

Para crear, entonces, un yaml para tener 5 contenedores, hay que ejecutar:

>python3 make-compose-yaml.py 5

##### En Github: https://github.com/luchowaldman/tp0-base/commit/7a744d344f11a3f34212d33cdac02acf49ad2d43

### Ejercicio N°2:
Modificar el cliente y el servidor para lograr que realizar cambios en el archivo de configuración no requiera un nuevo build de las imágenes de Docker para que los mismos sean efectivos. La configuración a través del archivo correspondiente (`config.ini` y `config.yaml`, dependiendo de la aplicación) debe ser inyectada en el container y persistida afuera de la imagen (hint: `docker volumes`).

#### Solucion

Este ejercicio se soluciona usando la caracteristica volumes de docker. Es un mecanismo que permite persistir y compartir datos entre contenedores y el host.
Para hacer el ejercicio agregue en cada definicion de un contendor:

    volumes:
    - ./volumen:/volumen

Con esto, hago que mi carpeta ./volumen se vea en los containers como la carpeta /volumen.
A esa carpeta le agregue los archivos de configuracion y por ultimo modifique los programas para que lean sus respectivas configuraciones de la carpeta /volumen

##### En Github: https://github.com/luchowaldman/tp0-base/commit/c10f7468903249f61889088faa9d9bbba2e919a5


### Ejercicio N°3:
Crear un script que permita verificar el correcto funcionamiento del servidor utilizando el comando `netcat` para interactuar con el mismo. Dado que el servidor es un EchoServer, se debe enviar un mensaje al servidor y esperar recibir el mismo mensaje enviado. Netcat no debe ser instalado en la máquina _host_ y no se puede exponer puertos del servidor para realizar la comunicación (hint: `docker network`).

#### Solucion

Esto lo resolvi con el script bash ./testserver.sh . Este, luego de declarar algunas constantes, utiliza:


>CONTAINER_ID=$(docker ps -qf "ancestor=$IMAGE_NAME")

para obtener el container id que esta corriendo la imagen del servidor. Con la instruccion inspect de docker, obtenemos la IP de ese container

>CONTAINER_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $CONTAINER_ID)

Si efectivamente hay algo corriendo en esa IP y en el puerto que corresponde:

>if nc -z -v -w 5 "$CONTAINER_IP" "$CONTAINER_PORT"; then

Le envio un texto de prueba y guardo el resultado en un archivo

> echo -n "$TEST_STRING" | nc "$CONTAINER_IP" "$CONTAINER_PORT" > response.txt

Finalmente, valido que la respuesta sea igual a lo enviado.


##### En Github: https://github.com/luchowaldman/tp0-base/commit/4f0cf99f7131529e0a92f80f6ddfdba12b1d67ae


### Ejercicio N°4:
Modificar servidor y cliente para que ambos sistemas terminen de forma _graceful_ al recibir la signal SIGTERM. Terminar la aplicación de forma _graceful_ implica que todos los _file descriptors_ (entre los que se encuentran archivos, sockets, threads y procesos) deben cerrarse correctamente antes que el thread de la aplicación principal muera. Loguear mensajes en el cierre de cada recurso (hint: Verificar que hace el flag `-t` utilizado en el comando `docker compose down`).

#### Solucion

docker-compose stop manda una signal SIGKILL para finalizar los procesos que corren en los container. El parametro `-t X` hace que, X segundos antes de mandar la signal SIGKILL, mande la signal SIGTERM para permitir a nuestro proceso cerrar sockets y archivos, liberar memoria, etc.

Para solucionar el ejercicio, agregamos en ambas aplicaciones un handler que reciba esta signal. En el caso del servidor, asi definimos que el handler handle_sigterm se llamara cuando llega signal.SIGTERM

> signal.signal(signal.SIGTERM, self.handle_sigterm)

Esta funcion pasa a False la propiedad _running, que es la que le indica al servidor que debe seguir ejecutandose. Cuando esto ocurre, la aplicacion termina.

##### En Github: https://github.com/luchowaldman/tp0-base/commit/996433b729de616b93c39ff2020367ff4a03718f


## Parte 2: Repaso de Comunicaciones


### Ejercicio N°5:
Modificar la lógica de negocio tanto de los clientes como del servidor para nuestro nuevo caso de uso.

#### Solucion
Para este ejercicio cree un cliente igual al que teniamos pero en Python. 
Cree una clase Agencia con las propiedades a mandar. Esta se completa en el inicio con los valores del config. Luego el cliente se conecta con el servidor y le manda la apuesta codificada por ApuestaEncoder.encode(). Espera una respuesta cualquiera y se desconecta.
El servidor, cuando recibe un mensaje lo decodifica con BetDecoder.decode y lo guarda con store_bets
Para transmitir, elegi mensajes de bloques fijos en que cada dato de la apuesta ocupa una cantidad fija de caracteres.

##### En Github: https://github.com/luchowaldman/tp0-base/commit/60ab2d6cc3f6760b9b74458f56f8955f994129c8


### Ejercicio N°6:
Modificar los clientes para que envíen varias apuestas a la vez (modalidad conocida como procesamiento por _chunks_ o _batchs_). La información de cada agencia será simulada por la ingesta de su archivo numerado correspondiente, provisto por la cátedra dentro de `.data/datasets.zip`.
Los _batchs_ permiten que el cliente registre varias apuestas en una misma consulta, acortando tiempos de transmisión y procesamiento. La cantidad de apuestas dentro de cada _batch_ debe ser configurable. Realizar una implementación genérica, pero elegir un valor por defecto de modo tal que los paquetes no excedan los 8kB. El servidor, por otro lado, deberá responder con éxito solamente si todas las apuestas del _batch_ fueron procesadas correctamente.

#### Solucion

El primer problema que me encontre al intentar resolver este ejercicio, es que ahora cada cliente debia leer de un archivo distinto.
Para ello modifique el script de make-compose-yaml.py para que, a medida que va creando los clientes, genere un directorio ./volumen_client{ID_CLIENT}. y copie ./data/agency-{ID_CLIENT}.csv (el archivo provisto por la catedra debe descomprimirse) con el nombre agency.csv y, copia config_cliente.ini, modificando el valor `agencia`  por el que corresponda.
Ademas, defini un protocolo, pues el cliente debe mandar 2 tipos de mensajes. O un chunk de apuestas O un mensaje diciendo que ya no va a mandar apuestas.
Entonces el primer caracter de un mensaje va a indicar el tipo de mensaje, y los siguientes 4 la agencia que lo mando.

`A` = CHUNK DE APUESTAS

`F` = FIN DE ENVIO

De este modo, el mensaje `F0012` significa que la agencia 12 dejo de transmitir.
En el caso del chunk de apuestas, al mensaje se le agregan 5 caracteres para indicar su tamaño y luego todas las apuestas concatenadas. 
Cada apuesta ocupa 82 Bytes, como quiero que por default ningun paquete supere los 8Kb, elijo un tamaño defult de 99 apuestas por paquete.

En resumen, el cliente comienza a leer el archivo y cuando alcanza el tamaño del chunck manda las apuestas y sigue hasta terminar el archivo. Cuando termina, envia un fin de envio, espera la respuesta y termina.

El servidor, cuando le llega una nueva conexion, empieza a recibir mensajes. mientras lleguen chunck de apuestas las procesa, en cuanto llega un fin de apuesta, cierra la conexion y envia un 'OK' a modo de ACK



##### En Github: https://github.com/luchowaldman/tp0-base/tree/ej6


### Ejercicio N°7:
Modificar los clientes para que notifiquen al servidor al finalizar con el envío de todas las apuestas y así proceder con el sorteo.
Inmediatamente después de la notificacion, los clientes consultarán la lista de ganadores del sorteo correspondientes a su agencia.

#### Solucion

Aqui, tuve que agregar un nuevo tipo de mensajes a mi protocolo. 

`C` = CONSULTA GANADOR

De este modo, el mensaje `C0012` significa que la agencia 12 quiere saber sus ganadores.

El servidor, que ahora cuenta los fines de archivo recibidos, puede responder este mensaje de dos maneras:


`N` = AUN NO SE REALIZO EL SORTEO

`R{tot_ganadores}{concatenated_dniss}` = YA SE REALIZO EL SORTEO.

Al ultimo mensaje, le siguen el total de ganadores y la lista de los DNIs, ocupando 8 caracteres cada uno.

El cliente cuando termina de mandar sus apuestas cierra la conexion. Inmediatamente despues abre una nueva y verifica si ya hay ganadores. Si los hay, los decodifica y muestra el total por pantalla. 
Si no los hay, espera un tiempo (que va creciendo exponencialmente) y vuelve a intentar la operacion.

Aqui es clave que el cliente despues de enviar sus apuestas cierre la conexion y la vuelva a abir. Como el servidor no maneja concurrencia, solo va a atender de a una conexion a la vez, entonces quedaria el primer cliente preguntando por siempre, pues los otros no podrian transmitir sus apuestas.

##### En Github: https://github.com/luchowaldman/tp0-base/tree/Ej7


## Parte 3: Repaso de Concurrencia

### Ejercicio N°8:
Modificar el servidor para que permita aceptar conexiones y procesar mensajes en paralelo.
En este ejercicio es importante considerar los mecanismos de sincronización a utilizar para el correcto funcionamiento de la persistencia.


#### Solucion

Modifique el servidor para que, al recibir una nueva conexion, el manejo de esta se haga en un hilo separado que va a existir mientras dure la comunicacion.
Ademas, cree dos locks: uno para los archivos y otro para el total de clientes que ya mandaron sus apuestas.
Entonces, una seccion critica para mi es la lectura y escritura del archivo de apuestas y una segunda es cuando se modifica el valor de clientes que faltan apostar y cuando se consulta.

##### En Github: https://github.com/luchowaldman/tp0-base/tree/Ej8
