from marshmallow import Schema, fields

class AwardSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    year = fields.Int()
    quote = fields.Str()
    description = fields.Str()