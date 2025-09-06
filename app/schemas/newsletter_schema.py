from marshmallow import fields
from .base import StrictSchema

class NewsletterSignupIn(StrictSchema):
    email = fields.Email(required=True)
    name = fields.Str(load_default=None)

class NewsletterSignupOut(StrictSchema):
    id = fields.Int()
    email = fields.Email()
    customer_id = fields.Int()
    created_at = fields.DateTime()
