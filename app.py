from flask import Flask, render_template

app = Flask(__name__)

# Datos demostrativos para esta semana.
# No se utiliza base de datos todavía.
productos = [
    {"id": 1, "nombre": "Taladro inalámbrico", "categoria": "Herramientas", "precio": 89.90, "stock": 12},
    {"id": 2, "nombre": "Martillo", "categoria": "Herramientas", "precio": 12.50, "stock": 28},
    {"id": 3, "nombre": "Caja de tornillos", "categoria": "Ferretería", "precio": 6.75, "stock": 45},
    {"id": 4, "nombre": "Pintura blanca 1 galón", "categoria": "Pinturas", "precio": 24.00, "stock": 16},
]

clientes = [
    {"id": 1, "nombre": "Carlos Mendoza", "correo": "carlos@example.com", "telefono": "0991112233"},
    {"id": 2, "nombre": "María Torres", "correo": "maria@example.com", "telefono": "0982223344"},
    {"id": 3, "nombre": "Luis Herrera", "correo": "luis@example.com", "telefono": "0973334455"},
]

proveedores = [
    {"id": 1, "empresa": "Distribuidora Andina", "contacto": "Ana Ruiz", "telefono": "0994567812"},
    {"id": 2, "empresa": "Herramientas del Sur", "contacto": "Jorge León", "telefono": "0987654321"},
    {"id": 3, "empresa": "Pinturas Ecuador", "contacto": "Daniela Mora", "telefono": "0976543210"},
]

facturas = [
    {"numero": "F-001", "cliente": "Carlos Mendoza", "fecha": "2026-08-10", "total": 102.40, "estado": "Pagada"},
    {"numero": "F-002", "cliente": "María Torres", "fecha": "2026-08-12", "total": 48.75, "estado": "Pendiente"},
    {"numero": "F-003", "cliente": "Luis Herrera", "fecha": "2026-08-14", "total": 135.00, "estado": "Pagada"},
]


@app.route("/")
def inicio():
    return render_template(
        "index.html",
        total_productos=len(productos),
        total_clientes=len(clientes),
        total_proveedores=len(proveedores),
        total_facturas=len(facturas),
    )


@app.route("/productos")
def ver_productos():
    return render_template("productos.html", productos=productos)


@app.route("/clientes")
def ver_clientes():
    return render_template("clientes.html", clientes=clientes)


@app.route("/proveedores")
def ver_proveedores():
    return render_template("proveedores.html", proveedores=proveedores)


@app.route("/facturacion")
def ver_facturacion():
    return render_template("facturacion.html", facturas=facturas)


if __name__ == "__main__":
    app.run(debug=True)
