from datetime import datetime
from app.extensions import db

class NewsletterSignup(db.Model):
    __tablename__ = "newsletter_signups"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # customer = db.relationship(
    #     "Customer", backref=db.backref("newsletter_signup_record", uselist=False)
    # )
