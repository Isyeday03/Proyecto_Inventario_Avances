# Proyecto Integrador U3 - Avance 9/16

Aplicación web de inventario desarrollada con Python, Flask, Jinja2, HTML, CSS,
JavaScript y Bootstrap.

## Estructura principal

- `app.py`: aplicación Flask y definición de rutas.
- `templates/`: plantillas HTML utilizadas por Flask.
- `static/css/`: estilos CSS.
- `static/js/`: archivos JavaScript.
- `static/img/`: imágenes del proyecto.
- `index.html`: portada estática destinada a GitHub Pages.

## Rutas Flask

- `/`
- `/productos`
- `/clientes`
- `/proveedores`
- `/facturacion`

## Ejecución local

### 1. Crear entorno virtual

Windows:

```bash
python -m venv venv
```

### 2. Activar entorno virtual

PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

CMD:

```cmd
venv\Scripts\activate
```

### 3. Instalar Flask

```bash
pip install -r requirements.txt
```

### 4. Ejecutar

```bash
python app.py
```

Abrir en el navegador:

`http://127.0.0.1:5000`

## GitHub Pages

GitHub Pages solo muestra archivos estáticos y no ejecuta Python/Flask.
Por esa razón, el archivo `index.html` ubicado en la raíz se utiliza como
frontend demostrativo para GitHub Pages. La aplicación Flask se encuentra
completa dentro del repositorio y se ejecuta localmente.
