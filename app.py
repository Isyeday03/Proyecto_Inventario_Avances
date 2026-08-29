from flask import Flask, render_template, redirect, url_for, flash

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm


app = Flask(__name__)
app.config["SECRET_KEY"] = "semana11-clave-secreta"


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
        total_facturas=len(facturas)
    )


@app.route("/productos")
def ver_productos():
    return render_template("productos.html", productos=productos)


@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():
    form = ProductoForm()

    if form.validate_on_submit():
        nuevo = {
            "id": len(productos) + 1,
            "nombre": form.nombre.data,
            "categoria": form.categoria.data,
            "precio": float(form.precio.data),
            "stock": form.stock.data
        }

        productos.append(nuevo)

        flash("Producto registrado correctamente.", "success")
        return redirect(url_for("ver_productos"))

    return render_template("formulario_producto.html", form=form)


@app.route("/clientes")
def ver_clientes():
    return render_template("clientes.html", clientes=clientes)


@app.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():
    form = ClienteForm()

    if form.validate_on_submit():
        nuevo = {
            "id": len(clientes) + 1,
            "nombre": form.nombre.data,
            "correo": form.correo.data,
            "telefono": form.telefono.data
        }

        clientes.append(nuevo)

        flash("Cliente registrado correctamente.", "success")
        return redirect(url_for("ver_clientes"))

    return render_template("formulario_cliente.html", form=form)


@app.route("/proveedores")
def ver_proveedores():
    return render_template("proveedores.html", proveedores=proveedores)


@app.route("/proveedores/nuevo", methods=["GET", "POST"])
def nuevo_proveedor():
    form = ProveedorForm()

    if form.validate_on_submit():
        nuevo = {
            "id": len(proveedores) + 1,
            "empresa": form.empresa.data,
            "contacto": form.contacto.data,
            "telefono": form.telefono.data
        }

        proveedores.append(nuevo)

        flash("Proveedor registrado correctamente.", "success")
        return redirect(url_for("ver_proveedores"))

    return render_template("formulario_proveedor.html", form=form)


@app.route("/facturacion")
def ver_facturacion():
    return render_template("facturacion.html", facturas=facturas)


@app.route("/facturacion/nueva", methods=["GET", "POST"])
def nueva_factura():
    form = FacturacionForm()

    if form.validate_on_submit():
        nueva = {
            "numero": f"F-{len(facturas) + 1:03d}",
            "cliente": form.cliente.data,
            "fecha": "2026-08-28",
            "total": float(form.total.data),
            "estado": form.estado.data
        }

        facturas.append(nueva)

        flash("Factura registrada correctamente.", "success")
        return redirect(url_for("ver_facturacion"))

    return render_template("formulario_facturacion.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)