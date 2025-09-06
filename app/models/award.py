from app.extensions import db

class Award(db.Model):
    __tablename__ = "awards"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    year = db.Column(db.Integer)
    quote = db.Column(db.Text)
