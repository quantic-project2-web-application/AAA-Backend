from marshmallow import fields, validate
from .base import StrictSchema

class CustomerInCreate(StrictSchema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    phone = fields.Str(load_default=None)
    newsletter_signup = fields.Bool(load_default=False)

class CustomerInUpdate(StrictSchema):
    # Whitelist ONLY the fields you want PATCH to update.
    name = fields.Str(validate=validate.Length(min=1))
    phone = fields.Str()
    newsletter_signup = fields.Bool()
    # If you want to allow changing email, uncomment carefully:
    # email = fields.Email()

class CustomerOut(StrictSchema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    email = fields.Email()
    phone = fields.Str()
    newsletter_signup = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
