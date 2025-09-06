from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.extensions import db
from app.models import Customer
from app.schemas.customer_schema import CustomerInCreate, CustomerInUpdate, CustomerOut
from app.utils.pagination import paginate_model
from app.utils.errors import error

bp = Blueprint("customers", __name__)
create_in = CustomerInCreate()
update_in = CustomerInUpdate()
cust_out = CustomerOut()

@bp.get("/")
def list_customers():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))
    data = paginate_model(Customer, CustomerOut(), page, per_page, order_by=Customer.created_at.desc())
    return jsonify(data)

@bp.post("/")
def create_customer():
    payload = request.get_json() or {}
    # StrictSchema will raise on any unknown keys
    data = create_in.load(payload)

    # ✅ Explicit, whitelisted construction
    cust = Customer(
        name=data["name"],
        email=data["email"],
        phone=data.get("phone"),
        newsletter_signup=data.get("newsletter_signup", False),
    )
    db.session.add(cust)
    db.session.commit()
    return jsonify(cust_out.dump(cust)), 201

@bp.get("/<int:cid>")
def get_customer(cid):
    cust = Customer.query.get_or_404(cid)
    return jsonify(cust_out.dump(cust))

@bp.patch("/<int:cid>")
def update_customer(cid):
    cust = Customer.query.get_or_404(cid)
    payload = request.get_json() or {}

    # Still rejects unknown keys; partial=True lets you omit fields
    data = update_in.load(payload, partial=True)

    # ✅ Whitelist assignments (no for k,v in data.items())
    for field in ("name", "phone", "newsletter_signup"):   # add "email" if allowed
        if field in data:
            setattr(cust, field, data[field])

    db.session.commit()
    return jsonify(cust_out.dump(cust))

@bp.delete("/<int:cid>")
def delete_customer(cid):
    cust = Customer.query.get_or_404(cid)
    db.session.delete(cust)
    db.session.commit()
    return "", 204
