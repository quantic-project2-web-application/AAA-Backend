import os
from flask import Flask, jsonify
from .extensions import db, migrate, cors

def create_app(config_object=None):
    app = Flask(__name__)

    if config_object:
        app.config.from_object(config_object)
    else:
        env = os.environ.get("FLASK_ENV", "development").lower()
        cfg = {
            "development": "app.config.DevelopmentConfig",
            "testing": "app.config.TestingConfig",
            "production": "app.config.ProductionConfig",
        }.get(env, "app.config.DevelopmentConfig")
        app.config.from_object(cfg)

    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprints
    from .api.customers_api import bp as customers_bp
    from .api.reservations_api import bp as reservations_bp
    from .api.newsletter_api import bp as newsletter_bp

    app.register_blueprint(customers_bp,   url_prefix="/api/customers")
    app.register_blueprint(reservations_bp, url_prefix="/api/reservations")
    app.register_blueprint(newsletter_bp,  url_prefix="/api/newsletter-signups")


    @app.get("/health")
    def health():
        return {"status": "ok"}, 200
    
    @app.get("/")
    def welcome():
        html = """
        <!doctype html>
        <html lang="en">
        <head><meta charset="utf-8"><title>Welcome</title></head>
        <body style="font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;">
            <h1>Welcome to CafeFuse BAckend API 👋</h1>
            <p>Health check: <a href="/health">/health</a></p>
            <h2>Assignment 2</h2>
            <table border="1" cellpadding="6" style="border-collapse:collapse;">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Ahmed Hassan Saad Tqloo</td>
                        <td>ahmedhassan.op9@gmail.com</td>
                    </tr>
                    <tr>
                        <td>Abubakarr Bangura</td>
                        <td>abangura9@gmail.com</td>
                    </tr>
                    <tr>
                        <td>Alvaro Candela</td>
                        <td>acandela.ripoll@gmail.com</td>
                    </tr>
                </tbody>
            </table>
            <h2>Endpoints</h2>
            <ul>
                <li>
                    <strong>Customers:</strong>
                    <code>GET /api/customers/</code>,
                    <code>POST /api/customers/</code>,
                    <code>GET /api/customers/&lt;id&gt;</code>,
                    <code>PATCH /api/customers/&lt;id&gt;</code>,
                    <code>DELETE /api/customers/&lt;id&gt;</code>
                </li>
                <li>
                    <strong>Reservations:</strong>
                    <code>GET /api/reservations/</code>,
                    <code>POST /api/reservations/</code>,
                    <code>GET /api/reservations/&lt;id&gt;</code>,
                    <code>DELETE /api/reservations/&lt;id&gt;</code>,
                    <code>GET /api/reservations/availability?time_slot=...</code>
                </li>
                <li>
                    <strong>Newsletter:</strong>
                    <code>POST /api/newsletter-signups/</code>,
                    <code>POST /api/newsletter-signups/unsubscribe</code>
                </li>
            </ul>
        </body>
        </html>
        """
        return html, 200, {"Content-Type": "text/html; charset=utf-8"}

    @app.errorhandler(400)
    def _400(e): return jsonify(error="Bad request"), 400

    @app.errorhandler(404)
    def _404(e): return jsonify(error="Not found"), 404

    @app.errorhandler(500)
    def _500(e): return jsonify(error="Internal server error"), 500

    return app
