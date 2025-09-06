from datetime import datetime
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Customer, Reservation
from app.schemas.reservation_schema import ReservationCreateSchema, ReservationSchema
from app.services.reservation_service import (
    remaining_capacity, assign_table_number, create_with_capacity, TOTAL_TABLES
)
from app.utils.errors import error

bp = Blueprint("reservations", __name__)
create_schema = ReservationCreateSchema()
res_schema = ReservationSchema()

@bp.get("/")
def list_reservations():
    items = Reservation.query.order_by(Reservation.created_at.desc()).limit(100).all()
    return jsonify(ReservationSchema(many=True).dump(items))

@bp.get("/availability")
def availability():
    ts = request.args.get("time_slot")
    if not ts:
        return error("time_slot is required (ISO 8601)")

    try:
        time_slot = datetime.fromisoformat(ts.replace("Z", "+00:00")).replace(tzinfo=None)
    except Exception:
        return error("Invalid time_slot; expected ISO 8601")

    taken = TOTAL_TABLES - remaining_capacity(time_slot)
    return jsonify({
        "time_slot": time_slot.isoformat(),
        "remaining": remaining_capacity(time_slot),
        "taken": taken
    })

@bp.post("/")
def create():
    payload = request.get_json() or {}
    data = create_schema.load(payload)

    name = data["name"]; email = data["email"]
    phone = data.get("phone")
    time_slot = data["time_slot"].replace(tzinfo=None)
    guests = data.get("guests", 2)

    if remaining_capacity(time_slot) <= 0:
        return error("This time is fully booked. Please pick another time.", status=409)

    # upsert customer by email
    cust = Customer.query.filter_by(email=email).first()
    if cust:
        if name:  cust.name = name
        if phone: cust.phone = phone
    else:
        cust = Customer(name=name, email=email, phone=phone)
        db.session.add(cust)
        db.session.flush()  # get cust.id

    table_number = assign_table_number(time_slot)
    if not table_number:
        return error("This time is fully booked. Please pick another time.", status=409)

    res = Reservation(
        customer_id=cust.id, time_slot=time_slot, table_number=table_number, guests=guests
    )
    saved = create_with_capacity(res)
    if not saved:
        return error("Could not finalize reservation due to a concurrent booking. Try again.", status=409)

    return jsonify(res_schema.dump(saved)), 201

@bp.get("/<int:rid>")
def get_reservation(rid):
    res = Reservation.query.get_or_404(rid)
    return jsonify(res_schema.dump(res))

@bp.delete("/<int:rid>")
def delete_reservation(rid):
    res = Reservation.query.get_or_404(rid)
    db.session.delete(res)
    db.session.commit()
    return "", 204
