import os
import pandas as pd
from datetime import datetime

# Crear carpeta /episodios si no existe
os.makedirs("episodios", exist_ok=True)

# Leer el archivo CSV con los episodios
df = pd.read_csv("episodios.csv")

# Encabezado HTML con fondo, estilos y botón de volver
html_head = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>El Grit Cast - Episodios</title>
  <style>
    body {
      background: url('../assets/fondo-episodios.jpg') no-repeat center center fixed;
      background-size: cover;
      color: #fff;
      font-family: sans-serif;
      padding: 2rem;
    }

    h1 {
      color: #B8FC26;
      margin-bottom: 1rem;
    }

    .volver {
      display: inline-block;
      margin-bottom: 2rem;
      padding: 10px 20px;
      background-color: #B8FC26;
      color: #000;
      border-radius: 8px;
      text-decoration: none;
      font-weight: bold;
    }

    input[type='text'] {
      width: 100%;
      padding: 10px;
      font-size: 1rem;
      margin-bottom: 2rem;
      border: none;
      border-radius: 8px;
    }

    section {
      margin-bottom: 2rem;
      padding: 1rem;
      background-color: rgba(30, 30, 30, 0.8);
      border-radius: 10px;
    }

    h2 {
      color: #B8FC26;
      margin-bottom: 0.5rem;
    }

    audio {
      width: 100%;
      margin-top: 0.5rem;
    }

    p {
      margin: 0.5rem 0;
    }
  </style>
</head>
<body>
  <a href="../index.html" class="volver">⬅ Volver al Inicio</a>
  <h1>🎙️ Todos los Episodios de El Grit Cast</h1>
  <input type="text" id="busqueda" placeholder="Buscar episodio por título, invitado o tema...">
  <div id="episodios">
"""

# Script para filtrar episodios con la barra de búsqueda
html_script = """
  </div>
  <script>
    const input = document.getElementById("busqueda");
    const episodios = document.querySelectorAll("#episodios section");
    input.addEventListener("input", function () {
      const texto = input.value.toLowerCase();
      episodios.forEach((ep) => {
        const contenido = ep.textContent.toLowerCase();
        ep.style.display = contenido.includes(texto) ? "block" : "none";
      });
    });
  </script>
</body>
</html>
"""

# Generar HTML para cada episodio
episodes_html = ""
for _, row in df.iterrows():
    num = str(row["número"]).zfill(3)
    titulo = row["título"] or f"Episodio {num}"
    fecha = datetime.strptime(row["fecha"], "%Y-%m-%d").strftime("%d/%m/%Y")
    episodio = f"""
    <section>
      <h2>Episodio {num}: {titulo}</h2>
      <p><strong>Invitado:</strong> {row["invitado"]}</p>
      <p><strong>Fecha:</strong> {fecha}</p>
      <p><strong>Temas:</strong> {row["temas"]}</p>
      <audio controls preload="none">
        <source src="{row["url_mp3"]}" type="audio/mpeg">
        Tu navegador no soporta el reproductor de audio.
      </audio>
    </section>
    """
    episodes_html += episodio

# Guardar en episodios/index.html
with open("episodios/index.html", "w", encoding="utf-8") as f:
    f.write(html_head + episodes_html + html_script)
