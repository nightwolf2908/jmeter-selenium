# Mini proyecto: Selenium y JMeter

Aplicación web local para aprender pruebas funcionales con Selenium y pruebas de carga con Apache JMeter.

## Objetivo

- Automatizar una interacción en el navegador con Selenium.
- Generar solicitudes HTTP con JMeter.
- Validar respuestas mediante aserciones.
- Interpretar tiempos de respuesta, errores y rendimiento.

## Tecnologías

- Python 3.
- Selenium.
- Firefox o Chrome.
- Apache JMeter.
- Java para ejecutar JMeter.

El servidor utiliza la biblioteca estándar de Python.

## Estructura

jmeter_selenium/
├── app.py
├── test_selenium.py
├── carga.jmx
├── resultados-01.jtl
└── reporte-01/

Los archivos .jtl y las carpetas de reportes se generan al ejecutar las pruebas.

## Preparación

Crear un entorno virtual, si todavía no existe:

python -m venv venv

Activarlo:

source venv/bin/activate

Instalar Selenium:

pip install -U selenium

En Arch Linux, JMeter se instaló usando:

yay -S jmeter

## Ejecutar la aplicación

Desde la carpeta del proyecto:

python app.py

Mantener esa terminal abierta y visitar:

http://127.0.0.1:8000

La aplicación permite escribir un nombre y obtener un saludo.

### Endpoint

GET /saludo?nombre=Abdiel

Respuesta esperada:

{"mensaje": "Hola, Abdiel!"}

## Prueba funcional con Selenium

Con el servidor ejecutándose, abrir otra terminal y activar el entorno virtual:

source venv/bin/activate

Ejecutar:

python test_selenium.py

La prueba realiza estos pasos:

1. Abre el navegador.
2. Visita la aplicación.
3. Escribe Abdiel.
4. Pulsa el botón de saludo.
5. Espera a que aparezca Hola, Abdiel!.
6. Comprueba el resultado.
7. Cierra el navegador.

Resultado esperado en la terminal:

Prueba correcta: el saludo funciona.

El script utiliza Firefox. Para usar Chrome, cambiar la creación del navegador por:

driver = webdriver.Chrome()

La primera ejecución puede necesitar Internet para que Selenium Manager obtenga el controlador correspondiente.

## Plan de JMeter

Abrir la interfaz gráfica:

jmeter

El plan carga.jmx contiene:

Test Plan
└── Thread Group
    ├── Obtener saludo — HTTP Request
    │   └── Response Assertion
    └── View Results Tree

### Solicitud HTTP

| Campo | Valor |
|---|---|
| Protocol | http |
| Server Name or IP | 127.0.0.1 |
| Port Number | 8000 |
| Method | GET |
| Path | /saludo |

Parámetros:

| Name | Value |
|---|---|
| nombre | Abdiel |

### Aserción de respuesta

Configurar Response Assertion con:

| Campo | Valor |
|---|---|
| Field to Test | Text Response |
| Pattern Matching Rules | Substring |
| Patterns to Test | Hola, Abdiel! |

El texto debe coincidir, incluyendo mayúsculas, signos y espacios.

Una respuesta HTTP 200 OK puede aparecer como fallida si la aserción no se cumple.

## Verificación inicial

Antes de generar carga:

1. Configurar un usuario y una repetición.
2. Habilitar View Results Tree.
3. Ejecutar la prueba desde la interfaz.
4. Revisar el código HTTP y el contenido recibido.
5. Confirmar que la muestra aparece en verde.
6. Guardar el plan.

Para consultar una aserción fallida, expandir la solicitud roja en View Results Tree y seleccionar la aserción que aparece debajo.

## Ejecutar una prueba de carga

Mantener el servidor encendido.

Desactivar View Results Tree, guardar el plan y ejecutar JMeter desde la terminal:

jmeter -n -t carga.jmx -l resultados-01.jtl -e -o reporte-01

| Opción | Función |
|---|---|
| -n | Ejecuta sin interfaz gráfica |
| -t | Indica el archivo del plan |
| -l | Guarda los resultados |
| -e | Genera el reporte HTML al terminar |
| -o | Indica la carpeta del reporte |

Abrir el reporte:

xdg-open reporte-01/index.html

Usar nombres nuevos para cada ejecución. La carpeta del reporte debe estar vacía o no existir.

## Usuarios, repeticiones y ramp-up

### Usuarios virtuales

Cada usuario ejecuta el flujo configurado en el grupo.

Sin pausas y con repeticiones continuas, cada usuario envía una solicitud, espera su respuesta y comienza la siguiente.

La cantidad de usuarios no equivale a las solicitudes por segundo.

### Loop Count

Indica cuántas veces cada usuario repite el flujo.

Por ejemplo:

10 usuarios × 20 repeticiones × 1 solicitud = 200 solicitudes

### Ramp-up

Es el tiempo utilizado para iniciar todos los usuarios.

Con 50 usuarios y 20 segundos de ramp-up:

20 segundos / 50 usuarios = 0.4 segundos entre inicios

JMeter inicia aproximadamente un usuario cada 0.4 segundos.

El ramp-up no es una pausa entre solicitudes ni la duración total de la prueba.

### Duración

Para una prueba de duración fija:

- Marcar Infinite en Loop Count.
- Activar Specify Thread lifetime o Scheduler.
- Establecer Duration, por ejemplo, en 120 segundos.

El ramp-up está incluido en esa duración.

## Interpretación del reporte

| Métrica | Significado |
|---|---|
| Samples | Total de solicitudes ejecutadas |
| FAIL | Solicitudes fallidas |
| Error % | Porcentaje de fallos |
| Average | Tiempo promedio de respuesta |
| Min / Max | Menor y mayor tiempo de respuesta |
| Median | El 50 % respondió en ese tiempo o menos |
| P95 | El 95 % respondió en ese tiempo o menos |
| P99 | El 99 % respondió en ese tiempo o menos |
| Transactions/s | Solicitudes completadas por segundo, en promedio |

El promedio puede ocultar solicitudes lentas. Conviene revisar también los percentiles y los errores.

El gráfico verde indica que las solicitudes pasaron las comprobaciones; no garantiza que todas hayan sido rápidas.

## Resultados obtenidos

### Prueba inicial

| Métrica | Resultado |
|---|---:|
| Solicitudes | 200 |
| Fallos | 0 |
| Error % | 0 % |
| Promedio | 2.02 ms |
| P95 | 3 ms |
| Solicitudes/s | 45.26 |

### Prueba con 50 usuarios

Configuración confirmada:

- Usuarios: 50.
- Ramp-up: 20 segundos.

| Métrica | Resultado |
|---|---:|
| Solicitudes | 169,146 |
| Fallos | 0 |
| Error % | 0 % |
| Promedio | 32.59 ms |
| Mediana | 5 ms |
| P95 | 7 ms |
| P99 | 1,053.99 ms |
| Máximo | 4,286 ms |
| Solicitudes/s | 1,399.17 |

La mayoría de las respuestas fue rápida, pero algunas presentaron demoras superiores a un segundo.

Estos resultados no establecen todavía el límite máximo del servidor.

## Explorar el límite de carga

Para este ejercicio se proponen estos criterios:

- Errores menores al 1 %.
- P95 menor a 500 ms.

Son criterios de práctica, no requisitos universales.

Ejecutar pruebas de 120 segundos aumentando gradualmente los usuarios:

| Prueba | Usuarios | Ramp-up |
|---|---:|---:|
| 1 | 10 | 10 s |
| 2 | 20 | 10 s |
| 3 | 50 | 20 s |
| 4 | 100 | 30 s |
| 5 | 200 | 30 s |

Registrar solicitudes/s, P95, P99 y errores de cada ejecución.

Si una configuración cumple y la siguiente falla, probar valores intermedios. Después, repetir la última configuración aceptable durante cinco minutos.

Una señal de saturación es que aumenten las esperas sin que crezcan las solicitudes por segundo.

## Limitaciones

- JMeter y el servidor comparten los recursos de la misma computadora.
- El servidor es una aplicación de aprendizaje.
- La escritura de registros en la terminal puede afectar el rendimiento.
- JMeter llama al endpoint directamente; no ejecuta el JavaScript de la página.
- Selenium comprueba la interacción en un navegador real.
- Los resultados dependen del equipo, el servidor y el patrón de solicitudes.

## Documentación

- Primeros pasos con Selenium (https://www.selenium.dev/documentation/webdriver/getting_started/first_script/)
- Planes de pruebas web en JMeter (https://jmeter.apache.org/usermanual/build-web-test-plan)
- Ejecución de JMeter (https://jmeter.apache.org/usermanual/get-started.html)
