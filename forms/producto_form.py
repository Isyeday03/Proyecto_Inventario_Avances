from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    DecimalField,
    IntegerField,
    SelectField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange
)


class ProductoForm(FlaskForm):

    nombre = StringField(
        "Nombre del producto",
        validators=[
            DataRequired(message="El nombre del producto es obligatorio."),
            Length(
                min=3,
                max=100,
                message="El nombre debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    categoria = StringField(
        "Categoría",
        validators=[
            DataRequired(message="La categoría es obligatoria."),
            Length(
                min=3,
                max=80,
                message="La categoría debe tener entre 3 y 80 caracteres."
            )
        ]
    )

    precio = DecimalField(
        "Precio",
        validators=[
            DataRequired(message="El precio es obligatorio."),
            NumberRange(
                min=0.01,
                message="El precio debe ser mayor que 0."
            )
        ]
    )

    stock = IntegerField(
        "Stock",
        validators=[
            DataRequired(message="El stock es obligatorio."),
            NumberRange(
                min=0,
                message="El stock no puede ser negativo."
            )
        ]
    )

    id_proveedor = SelectField(
        "Proveedor",
        coerce=int,
        validators=[
            DataRequired(message="Debe seleccionar un proveedor.")
        ]
    )

    submit = SubmitField("Guardar producto")

class EliminarProductoForm(FlaskForm):
    submit = SubmitField("Eliminar")    