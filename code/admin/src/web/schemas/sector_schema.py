from marshmallow import Schema, fields, validate


class SectorSchema(Schema):
    id = fields.Integer(dump_only=True)
    activo = fields.Boolean(dump_only=True)
    creado_en = fields.DateTime(dump_only=True)
    actualizado_en = fields.DateTime(dump_only=True)

    nombre = fields.String(required=True, validate=validate.Length(min=1, max=100),)
    descripcion = fields.String(required=True, validate=validate.Length(max=255),)

sector_schema = SectorSchema()
lista_sectores_schema = SectorSchema(many=True)

