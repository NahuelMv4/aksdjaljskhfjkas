from marshmallow import Schema, fields

class PersonalSchema(Schema):
    id = fields.Integer(dump_only=True)
    activo = fields.Boolean(dump_only=True)
    creado_en = fields.DateTime(dump_only=True)
    actualizado_en = fields.DateTime(dump_only=True)

    nombre = fields.String(required=True)
    apellido = fields.String(required=True)
    dni = fields.String(required=True)

    tipo_personal_id = fields.Integer(required=True)
    sector_id = fields.Integer(required=False, allow_none=True)
    tipo_menu_id = fields.Integer(required=True)


personal_schema = PersonalSchema()
lista_personal_schema = PersonalSchema(many=True)