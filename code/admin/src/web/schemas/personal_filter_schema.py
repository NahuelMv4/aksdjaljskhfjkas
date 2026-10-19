from marshmallow import Schema, fields, validate

class PersonalFilterSchema(Schema):
    dni = fields.Str(allow_none=True)
    nombre = fields.Str(allow_none=True)
    apellido = fields.Str(allow_none=True)
    sector_id = fields.Int(allow_none=True)
    tipo_personal_id = fields.Int(allow_none=True)
    activo = fields.Boolean(load_default=True)
    page = fields.Int(load_default=1)
    per_page = fields.Int(load_default=25, validate=validate.Range(min=1, max=25))

personal_filter_schema = PersonalFilterSchema()