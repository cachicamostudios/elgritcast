name: Generar episodios.html

on:
  push:
    paths:
      - 'episodios.csv'
      - 'generate_html.py'

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Clonar repositorio
      uses: actions/checkout@v3

    - name: Configurar Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: Instalar dependencias
      run: pip install pandas

    - name: Ejecutar script
      run: python generate_html.py

    - name: Commit y push de cambios
      run: |
        git config user.name "github-actions"
        git config user.email "github-actions@github.com"
        git add episodios.html
        git commit -m "Actualizar episodios.html automáticamente" || echo "No hay cambios"
        git push
