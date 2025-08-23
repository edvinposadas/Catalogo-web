
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity,
    set_refresh_cookies, unset_jwt_cookies
)
from app.db.base import SessionLocal
from app.models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()
    if not username or not password:
        return jsonify({"error": "Usuario y contraseña son requeridos"}), 400
    db = SessionLocal()
    try:
        u = User(username=username)
        u.set_password(password)
        db.add(u); db.commit(); db.refresh(u)
        return jsonify({"message": "Usuario creado", "user": {"id": u.id, "username": u.username}}), 201
    except IntegrityError:
        db.rollback()
        return jsonify({"error": "El usuario ya existe"}), 409
    finally:
        db.close()

@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()
    if not username or not password:
        return jsonify({"error": "Usuario y contraseña son requeridos"}), 400
    db = SessionLocal()
    try:
        u = db.query(User).filter(User.username == username).first()
        if not u or not u.check_password(password):
            return jsonify({"error": "Credenciales inválidas"}), 401

        access = create_access_token(identity=str(u.id), additional_claims={"username": u.username})
        refresh = create_refresh_token(identity=str(u.id))

        resp = jsonify({"message": "ok", "access_token": access, "user": {"id": u.id, "username": u.username}})
        set_refresh_cookies(resp, refresh)
        return resp, 200
    finally:
        db.close()

@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access = create_access_token(identity=str(user_id))
    return jsonify({"access_token": access}), 200

@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    db = SessionLocal()
    try:
        u = db.get(User, int(user_id))
        if not u:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify({"id": u.id, "username": u.username}), 200
    finally:
        db.close()

@auth_bp.post("/logout")
def logout():
    resp = jsonify({"message": "Sesión cerrada"})
    unset_jwt_cookies(resp)
    return resp, 200
