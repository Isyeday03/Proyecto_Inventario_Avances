from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ProveedorForm(FlaskForm):
    empresa = StringField(
        "Empresa",
        validators=[
            DataRequired(message="El nombre de la empresa es obligatorio."),
            Length(min=3, max=100, message="El nombre debe tener entre 3 y 100 caracteres.")
        ]
    )

    contacto = StringField(
        "Persona de contacto",
        validators=[
            DataRequired(message="El contacto es obligatorio."),
            Length(min=3, max=100, message="El contacto debe tener entre 3 y 100 caracteres.")
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(message="El teléfono es obligatorio."),
            Length(min=10, max=10, message="El teléfono debe contener 10 dígitos.")
        ]
    )

    submit = SubmitField("Guardar proveedor")