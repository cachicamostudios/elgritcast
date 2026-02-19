#!/usr/bin/env python3
"""
Script para convertir posts .md de blog/posts/ a HTML
y generar el índice del blog en blog/index.html
"""

import os
import re
import glob
from datetime import datetime

# ── Rutas ──────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
POSTS_DIR  = os.path.join(BASE_DIR, "blog", "posts")
BLOG_DIR   = os.path.join(BASE_DIR, "blog")

# ── Estilos compartidos con la página principal ────────────────────────────────
SHARED_STYLES = """
  <style>
    @font-face {
      font-family: 'n27regular';
      src: url('../n27-regular-webfont.ttf') format('truetype');
      font-weight: normal;
      font-style: normal;
    }
    :root {
      --color-bg: #d3d4d4;
      --color-main: #b8fc26;
      --color-dark: #373737;
      --color-white: #fff;
      --color-shadow: #373737;
    }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      font-family: 'n27regular', Arial, sans-serif;
      background: var(--color-bg);
      color: var(--color-dark);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 24px 32px 12px;
      background: var(--color-bg);
      border-bottom: 3px solid var(--color-dark);
      position: sticky;
      top: 0;
      z-index: 1000;
    }
    .logo-img { height: 60px; width: auto; }
    nav { display: flex; gap: 1.2rem; align-items: center; }
    nav a {
      text-decoration: none;
      font-size: 1.1rem;
      font-weight: bold;
      color: var(--color-dark);
      border-bottom: 2px solid transparent;
      padding: 4px 7px;
      border-radius: 8px;
      transition: background .2s;
    }
    nav a:hover { background: var(--color-main); border-bottom: 2px solid var(--color-dark); }
    footer {
      background: var(--color-bg);
      border-top: 3px solid var(--color-dark);
      text-align: center;
      padding: 22px 10px 30px;
      font-size: 1rem;
      margin-top: auto;
    }
    .dev-link {
      color: var(--color-dark);
      font-weight: bold;
      text-decoration: none;
      border-bottom: 1.5px dashed var(--color-dark);
    }
    .dev-link:hover { background: var(--color-main); }
  </style>
"""

HEADER_HTML = """
  <header>
    <a href="../index.html">
      <img class="logo-img" src="../el_grit_cast_cube_sin_fondo copia.png" alt="Logo El Grit Cast" />
    </a>
    <nav>
      <a href="../index.html">Home</a>
      <a href="../episodios/index.html">Episodios</a>
      <a href="../blog/index.html">Blog</a>
      <a href="../index.html#contacto">Contacto</a>
    </nav>
  </header>
"""

FOOTER_HTML = """
  <footer>
    <div style="margin-bottom:8px; font-weight:bold;">Copyright © El Grit Cast 2025</div>
    <div>Desarrollado por
      <a class="dev-link" href="https://www.cachicamo.studio/" target="_blank" rel="noopener">CACHICAMO STUDIOS LLC</a>
    </div>
  </footer>
"""

# ── Parser Markdown simple ─────────────────────────────────────────────────────
def parse_frontmatter(content):
    """Extrae el frontmatter YAML del markdown."""
    meta = {"titulo": "Sin título", "fecha": "", "descripcion": ""}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
            body = parts[2].strip()
    return meta, body

def md_to_html(text):
    """Convierte Markdown básico a HTML."""
    lines = text.splitlines()
    html = []
    in_list = False
    for line in lines:
        # Encabezados
        if line.startswith("### "):
            html.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("## "):
            html.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("# "):
            html.append(f"<h1>{line[2:]}</h1>")
        # Listas
        elif line.startswith("- "):
            if not in_list:
                html.append("<ul>")
                in_list = True
            html.append(f"<li>{line[2:]}</li>")
        else:
            if in_list:
                html.append("</ul>")
                in_list = False
            if line.strip() == "":
                html.append("")
            else:
                html.append(f"<p>{line}</p>")
    if in_list:
        html.append("</ul>")
    # Negritas e itálicas
    result = "\n".join(html)
    result = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", result)
    result = re.sub(r"\*(.+?)\*", r"<em>\1</em>", result)
    return result

# ── Generar HTML de cada post ─────────────────────────────────────────────────
def generate_post_html(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    meta, body = parse_frontmatter(content)
    body_html = md_to_html(body)
    slug = os.path.splitext(os.path.basename(md_path))[0]
    out_path = os.path.join(BLOG_DIR, f"{slug}.html")

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{meta['titulo']} - El Grit Cast Blog</title>
  <meta name="description" content="{meta['descripcion']}" />
  <link rel="icon" href="../el_grit_cast_cube_sin_fondo copia.png" type="image/png">
{SHARED_STYLES}
  <style>
    .post-container {{
      max-width: 780px;
      margin: 60px auto;
      padding: 0 24px;
      flex: 1;
    }}
    .post-header {{
      background: var(--color-main);
      border: 3px solid var(--color-dark);
      border-radius: 18px;
      box-shadow: 10px 10px 0 var(--color-dark);
      padding: 32px 36px;
      margin-bottom: 40px;
    }}
    .post-header h1 {{
      font-size: 2.2rem;
      margin: 0 0 10px 0;
      text-transform: uppercase;
      letter-spacing: .05em;
    }}
    .post-fecha {{
      font-size: .95rem;
      color: var(--color-dark);
      opacity: .7;
    }}
    .post-body {{
      background: #fff;
      border: 3px solid var(--color-dark);
      border-radius: 18px;
      box-shadow: 8px 8px 0 var(--color-dark);
      padding: 36px;
      line-height: 1.7;
      font-size: 1.08rem;
    }}
    .post-body h2 {{
      font-size: 1.4rem;
      border-bottom: 3px solid var(--color-main);
      padding-bottom: 6px;
      margin-top: 32px;
    }}
    .post-body h3 {{ font-size: 1.15rem; margin-top: 24px; }}
    .back-link {{
      display: inline-block;
      margin: 30px 0 0 0;
      padding: 10px 24px;
      background: var(--color-dark);
      color: var(--color-main);
      border-radius: 10px;
      text-decoration: none;
      font-weight: bold;
      box-shadow: 4px 4px 0 var(--color-main);
      transition: background .2s, color .2s;
    }}
    .back-link:hover {{ background: var(--color-main); color: var(--color-dark); }}
  </style>
</head>
<body>
{HEADER_HTML}
  <div class="post-container">
    <div class="post-header">
      <h1>{meta['titulo']}</h1>
      <span class="post-fecha">{meta['fecha']}</span>
    </div>
    <div class="post-body">
      {body_html}
    </div>
    <a class="back-link" href="index.html">← Volver al Blog</a>
  </div>
{FOOTER_HTML}
</body>
</html>"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  ✓ Generado: blog/{slug}.html")
    return {"slug": slug, "titulo": meta["titulo"], "fecha": meta["fecha"], "descripcion": meta["descripcion"]}

# ── Generar blog/index.html ───────────────────────────────────────────────────
def generate_blog_index(posts):
    # Ordenar por fecha descendente
    posts_sorted = sorted(posts, key=lambda x: x["fecha"], reverse=True)

    cards = ""
    for p in posts_sorted:
        cards += f"""
    <article style="background:#fff; border:3px solid var(--color-dark); border-radius:18px;
      box-shadow:8px 8px 0 var(--color-dark); padding:28px 32px; margin-bottom:32px;">
      <h2 style="margin:0 0 8px 0; font-size:1.5rem; text-transform:uppercase;">{p['titulo']}</h2>
      <p style="margin:0 0 6px 0; opacity:.65; font-size:.93rem;">{p['fecha']}</p>
      <p style="margin:0 0 20px 0;">{p['descripcion']}</p>
      <a href="{p['slug']}.html" style="display:inline-block; padding:10px 24px;
        background:var(--color-dark); color:var(--color-main); border-radius:10px;
        text-decoration:none; font-weight:bold; box-shadow:4px 4px 0 var(--color-main);">
        Leer más →
      </a>
    </article>"""

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Blog - El Grit Cast</title>
  <meta name="description" content="Artículos, reflexiones y herramientas del podcast El Grit Cast." />
  <link rel="icon" href="../el_grit_cast_cube_sin_fondo copia.png" type="image/png">
{SHARED_STYLES}
  <style>
    .blog-container {{ max-width: 780px; margin: 60px auto; padding: 0 24px; flex: 1; }}
    .blog-titulo {{
      background: var(--color-main);
      border: 3px solid var(--color-dark);
      border-radius: 18px;
      box-shadow: 10px 10px 0 var(--color-dark);
      padding: 28px 36px;
      margin-bottom: 40px;
    }}
    .blog-titulo h1 {{
      margin: 0;
      font-size: 2.4rem;
      text-transform: uppercase;
      letter-spacing: .06em;
    }}
  </style>
</head>
<body>
{HEADER_HTML}
  <div class="blog-container">
    <div class="blog-titulo">
      <h1>📝 Blog</h1>
    </div>
    {cards}
  </div>
{FOOTER_HTML}
</body>
</html>"""

    out_path = os.path.join(BLOG_DIR, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("  ✓ Generado: blog/index.html")

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    md_files = glob.glob(os.path.join(POSTS_DIR, "*.md"))
    if not md_files:
        print("No se encontraron archivos .md en blog/posts/")
        exit(0)

    print(f"Procesando {len(md_files)} post(s)...")
    posts = []
    for md_file in md_files:
        post_meta = generate_post_html(md_file)
        posts.append(post_meta)

    generate_blog_index(posts)
    print("✅ Blog generado correctamente.")
