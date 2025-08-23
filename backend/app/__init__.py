import os
from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.db.base import init_db
from app.routes.auth import auth_bp
from app.routes.categorias import categoria_bp
from app.routes.presentaciones import presentacion_bp
from app.routes.productos import producto_bp

def create_app():
    app = Flask(__name__)

    # JWT
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "change-me")
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_COOKIE_SAMESITE"] = "Lax"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_SESSION_COOKIE"] = True  # la cookie de refresh se borra al cerrar el navegador

    # CORS (con credenciales y orígenes explícitos)
    CORS(
        app,
        supports_credentials=True,
        resources={
            r"/api/*": {
                "origins": [
                    "http://localhost:8080",
                    "http://127.0.0.1:8080",
                    "http://localhost:8081",     # agregado
                    "http://127.0.0.1:8081",     # agregado
                    "http://localhost:5173",
                    "http://127.0.0.1:5173",
                ],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "expose_headers": ["Content-Type", "Authorization"],
            }
        },
    )

    JWTManager(app)
    init_db()

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(presentacion_bp)
    app.register_blueprint(producto_bp)

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app
