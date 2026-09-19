from flask import Flask, render_template, redirect, url_for, flash

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import generate_password_hash, check_password_hash

from conexion.conexion import obtener_conexion

from models import Usuario

from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm
from forms.producto_form import ProductoForm, EliminarProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm


app = Flask(__name__)

app.config["SECRET_KEY"] = "semana14-clave-secreta"


# ==================================================
# FLASK-LOGIN
# ==================================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

login_manager.login_message = (
    "Debe iniciar sesión para acceder a esta página."
)

login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT id, usuario, password
        FROM usuarios
        WHERE id = %s
        """,
        (int(user_id),)
    )

    fila = cursor.fetchone()

    cursor.close()
    conexion.close()

    if fila:

        return Usuario(
            id=fila[0],
            usuario=fila[1],
            password=fila[2]
        )

    return None


# ==================================================
# DATOS TEMPORALES DE OTROS MÓDULOS
# ==================================================

clientes = [
    {
        "id": 1,
        "nombre": "Carlos Mendoza",
        "correo": "carlos@example.com",
        "telefono": "0991112233"
    },
    {
        "id": 2,
        "nombre": "María Torres",
        "correo": "maria@example.com",
        "telefono": "0982223344"
    },
    {
        "id": 3,
        "nombre": "Luis Herrera",
        "correo": "luis@example.com",
        "telefono": "0973334455"
    }
]


proveedores_temporales = [
    {
        "id": 1,
        "empresa": "Distribuidora Andina",
        "contacto": "Ana Ruiz",
        "telefono": "0994567812"
    },
    {
        "id": 2,
        "empresa": "Herramientas del Sur",
        "contacto": "Jorge León",
        "telefono": "0987654321"
    },
    {
        "id": 3,
        "empresa": "Pinturas Ecuador",
        "contacto": "Daniela Mora",
        "telefono": "0976543210"
    }
]


facturas = [
    {
        "numero": "F-001",
        "cliente": "Carlos Mendoza",
        "fecha": "2026-08-10",
        "total": 102.40,
        "estado": "Pagada"
    },
    {
        "numero": "F-002",
        "cliente": "María Torres",
        "fecha": "2026-08-12",
        "total": 48.75,
        "estado": "Pendiente"
    },
    {
        "numero": "F-003",
        "cliente": "Luis Herrera",
        "fecha": "2026-08-14",
        "total": 135.00,
        "estado": "Pagada"
    }
]


# ==================================================
# PÁGINA PRINCIPAL
# ==================================================

@app.route("/")
def inicio():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM productos"
    )

    total_productos = cursor.fetchone()[0]

    cursor.close()
    conexion.close()

    return render_template(
        "index.html",
        total_productos=total_productos,
        total_clientes=len(clientes),
        total_proveedores=len(proveedores_temporales),
        total_facturas=len(facturas)
    )


# ==================================================
# REGISTRO DE USUARIOS
# ==================================================

@app.route("/registro", methods=["GET", "POST"])
def registro():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = UsuarioForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Comprobar que el usuario no exista
        cursor.execute(
            """
            SELECT id
            FROM usuarios
            WHERE usuario = %s
            """,
            (form.usuario.data,)
        )

        usuario_existente = cursor.fetchone()

        if usuario_existente:

            cursor.close()
            conexion.close()

            flash(
                "Ese nombre de usuario ya está registrado.",
                "danger"
            )

            return render_template(
                "registro.html",
                form=form
            )

        # Generar hash de la contraseña
        password_hash = generate_password_hash(
            form.password.data
        )

        # Guardar usuario
        cursor.execute(
            """
            INSERT INTO usuarios
            (usuario, password)
            VALUES (%s, %s)
            """,
            (
                form.usuario.data,
                password_hash
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Usuario registrado correctamente. "
            "Ahora puede iniciar sesión.",
            "success"
        )

        return redirect(url_for("login"))

    return render_template(
        "registro.html",
        form=form
    )


# ==================================================
# LOGIN
# ==================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = LoginForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT id, usuario, password
            FROM usuarios
            WHERE usuario = %s
            """,
            (form.usuario.data,)
        )

        fila = cursor.fetchone()

        cursor.close()
        conexion.close()

        if fila:

            password_correcta = check_password_hash(
                fila[2],
                form.password.data
            )

            if password_correcta:

                usuario = Usuario(
                    id=fila[0],
                    usuario=fila[1],
                    password=fila[2]
                )

                login_user(usuario)

                flash(
                    "Inicio de sesión correcto.",
                    "success"
                )

                return redirect(
                    url_for("dashboard")
                )

        flash(
            "Usuario o contraseña incorrectos.",
            "danger"
        )

    return render_template(
        "login.html",
        form=form
    )


# ==================================================
# DASHBOARD
# ==================================================

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html"
    )


# ==================================================
# LOGOUT
# ==================================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Sesión cerrada correctamente.",
        "success"
    )

    return redirect(url_for("login"))


# ==================================================
# PRODUCTOS - SELECT + JOIN
# ==================================================

@app.route("/productos")
@login_required
def ver_productos():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT
            p.id_producto AS id,
            p.nombre,
            p.categoria,
            p.precio,
            p.stock,
            pr.nombre AS proveedor
        FROM productos p
        LEFT JOIN proveedores pr
            ON p.id_proveedor = pr.id_proveedor
        ORDER BY p.id_producto
        """
    )

    filas = cursor.fetchall()

    productos = []

    for fila in filas:

        productos.append({
            "id": fila[0],
            "nombre": fila[1],
            "categoria": fila[2],
            "precio": float(fila[3]),
            "stock": fila[4],
            "proveedor": fila[5]
        })

    cursor.close()
    conexion.close()

    eliminar_form = EliminarProductoForm()

    return render_template(
        "productos.html",
        productos=productos,
        eliminar_form=eliminar_form
    )


# ==================================================
# PRODUCTOS - AGREGAR
# ==================================================

@app.route(
    "/productos/nuevo",
    methods=["GET", "POST"]
)
@login_required
def nuevo_producto():

    form = ProductoForm()

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT id_proveedor, nombre
        FROM proveedores
        ORDER BY nombre
        """
    )

    proveedores = cursor.fetchall()

    form.id_proveedor.choices = [
        (proveedor[0], proveedor[1])
        for proveedor in proveedores
    ]

    if form.validate_on_submit():

        cursor.execute(
            """
            INSERT INTO productos
            (
                nombre,
                categoria,
                precio,
                stock,
                id_proveedor
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                form.nombre.data,
                form.categoria.data,
                form.precio.data,
                form.stock.data,
                form.id_proveedor.data
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Producto registrado correctamente.",
            "success"
        )

        return redirect(
            url_for("ver_productos")
        )

    cursor.close()
    conexion.close()

    return render_template(
        "formulario_producto.html",
        form=form
    )


# ==================================================
# PRODUCTOS - EDITAR
# ==================================================

@app.route(
    "/productos/editar/<int:id_producto>",
    methods=["GET", "POST"]
)
@login_required
def editar_producto(id_producto):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT
            id_producto,
            nombre,
            categoria,
            precio,
            stock,
            id_proveedor
        FROM productos
        WHERE id_producto = %s
        """,
        (id_producto,)
    )

    producto = cursor.fetchone()

    if producto is None:

        cursor.close()
        conexion.close()

        flash(
            "Producto no encontrado.",
            "danger"
        )

        return redirect(
            url_for("ver_productos")
        )

    form = ProductoForm()

    cursor.execute(
        """
        SELECT id_proveedor, nombre
        FROM proveedores
        ORDER BY nombre
        """
    )

    proveedores = cursor.fetchall()

    form.id_proveedor.choices = [
        (proveedor[0], proveedor[1])
        for proveedor in proveedores
    ]

    if form.validate_on_submit():

        cursor.execute(
            """
            UPDATE productos
            SET
                nombre = %s,
                categoria = %s,
                precio = %s,
                stock = %s,
                id_proveedor = %s
            WHERE id_producto = %s
            """,
            (
                form.nombre.data,
                form.categoria.data,
                form.precio.data,
                form.stock.data,
                form.id_proveedor.data,
                id_producto
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Producto actualizado correctamente.",
            "success"
        )

        return redirect(
            url_for("ver_productos")
        )

    if not form.is_submitted():

        form.nombre.data = producto[1]
        form.categoria.data = producto[2]
        form.precio.data = producto[3]
        form.stock.data = producto[4]
        form.id_proveedor.data = producto[5]

    cursor.close()
    conexion.close()

    return render_template(
        "formulario_producto.html",
        form=form
    )


# ==================================================
# PRODUCTOS - ELIMINAR
# ==================================================

@app.route(
    "/productos/eliminar/<int:id_producto>",
    methods=["POST"]
)
@login_required
def eliminar_producto(id_producto):

    form = EliminarProductoForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            DELETE FROM productos
            WHERE id_producto = %s
            """,
            (id_producto,)
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Producto eliminado correctamente.",
            "success"
        )

    else:

        flash(
            "No se pudo eliminar el producto.",
            "danger"
        )

    return redirect(
        url_for("ver_productos")
    )


# ==================================================
# CLIENTES
# ==================================================

@app.route("/clientes")
@login_required
def ver_clientes():

    return render_template(
        "clientes.html",
        clientes=clientes
    )


@app.route(
    "/clientes/nuevo",
    methods=["GET", "POST"]
)
@login_required
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

        flash(
            "Cliente registrado correctamente.",
            "success"
        )

        return redirect(
            url_for("ver_clientes")
        )

    return render_template(
        "formulario_cliente.html",
        form=form
    )


# ==================================================
# PROVEEDORES
# ==================================================

@app.route("/proveedores")
@login_required
def ver_proveedores():

    return render_template(
        "proveedores.html",
        proveedores=proveedores_temporales
    )


@app.route(
    "/proveedores/nuevo",
    methods=["GET", "POST"]
)
@login_required
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        nuevo = {
            "id": len(proveedores_temporales) + 1,
            "empresa": form.empresa.data,
            "contacto": form.contacto.data,
            "telefono": form.telefono.data
        }

        proveedores_temporales.append(nuevo)

        flash(
            "Proveedor registrado correctamente.",
            "success"
        )

        return redirect(
            url_for("ver_proveedores")
        )

    return render_template(
        "formulario_proveedor.html",
        form=form
    )


# ==================================================
# FACTURACIÓN
# ==================================================

@app.route("/facturacion")
@login_required
def ver_facturacion():

    return render_template(
        "facturacion.html",
        facturas=facturas
    )


@app.route(
    "/facturacion/nueva",
    methods=["GET", "POST"]
)
@login_required
def nueva_factura():

    form = FacturacionForm()

    if form.validate_on_submit():

        nueva = {
            "numero": f"F-{len(facturas) + 1:03d}",
            "cliente": form.cliente.data,
            "fecha": "2026-09-19",
            "total": float(form.total.data),
            "estado": form.estado.data
        }

        facturas.append(nueva)

        flash(
            "Factura registrada correctamente.",
            "success"
        )

        return redirect(
            url_for("ver_facturacion")
        )

    return render_template(
        "formulario_facturacion.html",
        form=form
    )


# ==================================================
# EJECUTAR APLICACIÓN
# ==================================================

if __name__ == "__main__":
    app.run(debug=True)