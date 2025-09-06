from datetime import datetime, date
from sqlalchemy import UniqueConstraint
from app.extensions import db

class Reservation(db.Model):
    __tablename__ = "reservations"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False, index=True)
    time_slot = db.Column(db.DateTime, nullable=False, index=True)
    table_number = db.Column(db.SmallInteger, nullable=False)
    guests = db.Column(db.SmallInteger, nullable=False, default=2)
    date = db.Column(db.Date, nullable=False, default=date.today)  # <-- Added date column
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    customer = db.relationship("Customer", back_populates="reservations")

    # Ensure no two reservations share the same table_number at a given time_slot
    __table_args__ = (
        UniqueConstraint("time_slot", "table_number", name="uq_reservation_time_table"),
    )