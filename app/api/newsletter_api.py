from flask import Blueprint, request, jsonify
from sqlalchemy import func  
from app.extensions import db
from app.models import Customer, NewsletterSignup
from app.schemas.newsletter_schema import NewsletterSignupIn, NewsletterSignupOut

bp = Blueprint("newsletter", __name__)

news_letter_in_schema = NewsletterSignupIn()
news_letter_out_schema = NewsletterSignupOut()

@bp.post("/")
def subscribe():
    payload = request.get_json() or {}
    data = news_letter_in_schema.load(payload)
    email = data["email"]

    cust = Customer.query.filter_by(email=email).first()
    if cust:
        cust.newsletter_signup = True
  
    else:
        cust = Customer(name=email.split("@")[0], email=email, newsletter_signup=True)
        db.session.add(cust)
        db.session.flush()

    if not NewsletterSignup.query.filter_by(email=email).first():
        db.session.add(NewsletterSignup(email=email))

    db.session.commit()
    return jsonify({"ok": True}), 201

@bp.post("/unsubscribe")
def unsubscribe():
    """
    Unsubscribe an email from the newsletter.

    Request JSON:
      { "email": "<user@example.com>" }

    Response (200):
      { "ok": true, "removed": <int> }   # 'removed' is the number of signup rows deleted
    """
    payload = request.get_json() or {}

    # Only validate the email field; reject bad/missing email with 422
    try:
        data = news_letter_out_schema.load({"email": payload.get("email")})
    except Exception as err:
        return jsonify({"errors": err.messages}), 422

    # Normalize for case-insensitive match
    email = data["email"].strip().lower()

    # Delete any signup rows for this email (idempotent if none exist)
    signups = (
        NewsletterSignup.query
        .filter(func.lower(NewsletterSignup.email) == email)
        .all()
    )
    removed = 0
    for s in signups:
        db.session.delete(s)
        removed += 1

    # Flip the customer's newsletter flag if a customer exists
    cust = Customer.query.filter(func.lower(Customer.email) == email).first()
    if cust and cust.newsletter_signup:
        cust.newsletter_signup = False

    db.session.commit()
    return jsonify({"ok": True, "removed": removed}), 200