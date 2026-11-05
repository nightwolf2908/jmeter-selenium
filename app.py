from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from urllib.parse import parse_qs, urlparse
import json

PAGINA = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Mini proyecto</title>
</head>
<body>
    <h1>Saludador</h1>

    <form id="formulario">
        <input id="nombre" placeholder="Escribe tu nombre" required>
        <button type="submit">Saludar</button>
    </form>

    <p id="resultado"></p>

    <script>
        document.querySelector("#formulario")
            .addEventListener("submit", async (evento) => {
                evento.preventDefault();

                const nombre = document.querySelector("#nombre").value;
                const respuesta = await fetch(
                    "/saludo?nombre=" + encodeURIComponent(nombre)
                );
                const datos = await respuesta.json();

                document.querySelector("#resultado").textContent =
                    datos.mensaje;
            });
    </script>
</body>
</html>
"""


class Manejador(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)

        if url.path == "/":
            contenido = PAGINA.encode("utf-8")
            tipo = "text/html; charset=utf-8"

        elif url.path == "/saludo":
            parametros = parse_qs(url.query)
            nombre = parametros.get("nombre", ["visitante"])[0]

            contenido = json.dumps(
                {"mensaje": f"Hola, {nombre}!"},
                ensure_ascii=False,
            ).encode("utf-8")
            tipo = "application/json; charset=utf-8"

        else:
            self.send_error(404)
            return

        self.send_response(200)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(contenido)))
        self.end_headers()
        self.wfile.write(contenido)


if __name__ == "__main__":
    servidor = ThreadingHTTPServer(("127.0.0.1", 8000), Manejador)
    print("Servidor disponible en http://127.0.0.1:8000")
    servidor.serve_forever()
