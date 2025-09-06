import random
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from app.extensions import db
from app.models import Reservation

TOTAL_TABLES = 30

def tables_taken_at(time_slot):
    rows = db.session.query(Reservation.table_number).filter(Reservation.time_slot == time_slot).all()
    return {r[0] for r in rows}

def remaining_capacity(time_slot):
    count = db.session.query(func.count(Reservation.id)).filter(Reservation.time_slot == time_slot).scalar()
    return max(TOTAL_TABLES - int(count or 0), 0)

def assign_table_number(time_slot):
    taken = tables_taken_at(time_slot)
    free = [i for i in range(1, TOTAL_TABLES + 1) if i not in taken]
    if not free:
        return None
    return random.choice(free)

def create_with_capacity(reservation):
    # Commit with simple retry in case the DB enforces uniqueness during a race.
    for _ in range(3):
        try:
            db.session.add(reservation)
            db.session.commit()
            return reservation
        except IntegrityError:
            db.session.rollback()
    return None
