import os
from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
from database.database import init_db
from database.models import db

import warnings
warnings.filterwarnings("ignore", category=UserWarning)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per minute"],
        storage_uri="memory://",
    )

    init_db(app)

    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
            "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
            "connect-src 'self'; "
            "img-src 'self' data:; "
        )
        return response

    from routes.chat import chat_bp
    from routes.dashboard import dashboard_bp
    from routes.alerts import alerts_bp

    app.register_blueprint(chat_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(alerts_bp)

    @app.route("/")
    def index():
        return render_template("fan.html")

    @app.route("/dashboard")
    def dashboard():
        return render_template("dashboard.html")

    @app.route("/health")
    def health():
        return {"status": "healthy", "service": "ArenaShield AI"}

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
