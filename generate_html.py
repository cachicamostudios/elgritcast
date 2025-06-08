import os
import pandas as pd
from datetime import datetime

# Crear carpeta /episodios si no existe
os.makedirs("episodios", exist_ok=True)

# Leer el archivo CSV con separador de columnas '|'
df = pd.read_csv("episodios.csv", sep="|")

# Mostrar columnas detectadas por seguridad
print("🔎 Columnas leídas:", df.columns.tolist())

# Arreglar posibles espacios o BOM invisibles en encabezados
df.columns = df.columns.str.strip()

# Encabezado HTML
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
      background-color: rgba(30, 30, 30, 0.85);
      border-radius: 10px;
    }
    h2 {
      color: #B8FC26;
      margin-bottom: 0.3rem;
    }
    audio {
      width: 100%;
      margin-top: 0.5rem;
    }
    p {
      margin: 0.4rem 0;
    }
  </style>
</head>
<body>
  <a href="../index.html" class="volver">⬅ Volver al Inicio</a>
  <h1>🎧 Todos los Episodios de El Grit Cast</h1>
  <input type="text" id="busqueda" placeholder="Buscar episodio por título, invitado o tema...">
  <div id="episodios">
"""

# Generar cada bloque de episodio
episodes_html = ""
for _, row in df.iterrows():
    num_raw = row.get("número") or row.get("\ufeffnúmero")  # Manejo de BOM
    num = str(num_raw).zfill(3)
    invitado = row["invitado"]
    titulo = row["título"]
    fecha_str = row["fecha"]
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").strftime("%d/%m/%Y")
    except:
        fecha = fecha_str
    url = row["url_mp3"]
    temas = row["temas"]

    episode_block = f"""
    <section>
      <h2>🎙️ Episodio {num}: {titulo}</h2>
      <p><strong>Invitado:</strong> {invitado}</p>
      <p><strong>Fecha:</strong> {fecha}</p>
      <p><strong>Temas:</strong> {temas}</p>
      <audio controls preload="none">
        <source src="{url}" type="audio/mpeg">
        Tu navegador no soporta audio.
      </audio>
    </section>
    """
    episodes_html += episode_block

# Script para buscar episodios + cierre HTML
html_end = """
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

# Guardar archivo HTML generado
with open("episodios/index.html", "w", encoding="utf-8") as f:
    f.write(html_head + episodes_html + html_end)

print("✅ Página generada correctamente en episodios/index.html")
