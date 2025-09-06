from marshmallow import Schema, fields, validate
from .base import StrictSchema

class ReservationCreateSchema(StrictSchema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(load_default=None)
    time_slot = fields.DateTime(required=True)
    guests = fields.Int(load_default=2, validate=validate.Range(min=1, max=12))

class ReservationSchema(StrictSchema):
    id = fields.Int()
    time_slot = fields.DateTime()
    table_number = fields.Int()
    guests = fields.Int()
    created_at = fields.DateTime()
    customer = fields.Nested("CustomerOut")
