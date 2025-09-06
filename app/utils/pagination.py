from sqlalchemy import select
from app.extensions import db

def paginate_model(model, schema, page, per_page=20, order_by=None, filters=None):
    stmt = select(model)
    if filters:
        stmt = stmt.filter_by(**filters)
    if order_by is not None:
        stmt = stmt.order_by(order_by)
    per_page = min(int(per_page), 100)
    page_obj = db.paginate(stmt, page=page, per_page=per_page, error_out=False)
    return {
        "items": schema.dump(page_obj.items, many=True),
        "page": page_obj.page,
        "per_page": page_obj.per_page,
        "total": page_obj.total,
        "pages": page_obj.pages,
    }
