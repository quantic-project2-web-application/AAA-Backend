from app import create_app
from app.extensions import db
from app.models import MenuCategory, MenuItem, Award, GalleryImage

app = create_app()

with app.app_context():
    starters = MenuCategory(name="Starters", sort_order=1)
    mains = MenuCategory(name="Mains", sort_order=2)
    desserts = MenuCategory(name="Desserts", sort_order=3)
    db.session.add_all([starters, mains, desserts])
    db.session.flush()


    db.session.add_all([
        Award(title="Best New Restaurant", organization="City Magazine", year=2024, quote="A must-try."),
    ])


    db.session.commit()
    print("Seeded!")
