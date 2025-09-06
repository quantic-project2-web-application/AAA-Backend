from marshmallow import Schema, RAISE

class StrictSchema(Schema):
    class Meta:
        # Be explicit: reject ANY key not declared in the schema
        unknown = RAISE
