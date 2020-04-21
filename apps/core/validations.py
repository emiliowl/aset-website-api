from marshmallow import Schema, fields, validate

error_messages={
    "null": "campo deve ser preenchido",
    "required": "campo deve ser preenchido"
}

class CustomerSchema(Schema):
    name = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=100, error="tamanho deve ser entre {min} e {max}"),
        error_messages=error_messages
    )
    phone = fields.Str(
        required=True,
        validate=[
            validate.Length(min=14, max=15, error="tamanho deve ser entre {min} e {max}"),
            validate.Regexp("\(\d{2}\).(\d{4}|\d{5})-(\d{4})", error="formato inválido!")
        ],
        error_messages=error_messages
    )
    email = fields.Email(
        required=True,
        validate=validate.Length(min=3, max=50, error="tamanho deve ser entre {min} e {max}"),
        error_messages={**error_messages, **{"invalid": "e-mail inválido"}}
    )