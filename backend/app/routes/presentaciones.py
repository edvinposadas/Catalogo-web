
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from app.db.base import SessionLocal
from app.models.presentacion import Presentacion

presentacion_bp = Blueprint("presentaciones", __name__, url_prefix="/api/presentaciones")

@presentacion_bp.get("")
@presentacion_bp.get("/")
@jwt_required()
def list_presentaciones():
    db = SessionLocal()
    try:
        page = int((request.args.get("page") or 1))
        per_page = int((request.args.get("per_page") or request.args.get("size") or 10))
        q = (request.args.get("q") or request.args.get("search") or "").strip()
        qry = db.query(Presentacion)
        if q:
            qry = qry.filter(func.lower(Presentacion.nombre).contains(q.lower()))
        total = qry.count()
        items = (qry.order_by(Presentacion.id.desc())
                   .offset((page-1)*per_page)
                   .limit(per_page).all())
        return jsonify({
            "total": total, "page": page, "per_page": per_page,
            "items": [{"id": p.id, "nombre": p.nombre, "descripcion": p.descripcion} for p in items]
        })
    finally:
        db.close()

@presentacion_bp.post("")
@presentacion_bp.post("/")
@jwt_required()
def create_presentacion():
    data = request.get_json() or {}
    nombre = (data.get("nombre") or "").strip()
    descripcion = (data.get("descripcion") or "").strip() or None
    if not nombre:
        return jsonify({"error": "El nombre es obligatorio"}), 400
    db = SessionLocal()
    try:
        p = Presentacion(nombre=nombre, descripcion=descripcion)
        db.add(p); db.commit(); db.refresh(p)
        return jsonify({"id": p.id, "nombre": p.nombre, "descripcion": p.descripcion}), 201
    finally:
        db.close()

@presentacion_bp.put("/<int:pid>")
@jwt_required()
def update_presentacion(pid):
    data = request.get_json() or {}
    db = SessionLocal()
    try:
        p = db.get(Presentacion, pid)
        if not p:
            return jsonify({"error": "No encontrado"}), 404
        if "nombre" in data: p.nombre = (data["nombre"] or "").strip()
        if "descripcion" in data: p.descripcion = (data["descripcion"] or "").strip() or None
        db.commit()
        return jsonify({"id": p.id, "nombre": p.nombre, "descripcion": p.descripcion})
    finally:
        db.close()

@presentacion_bp.delete("/<int:pid>")
@jwt_required()
def delete_presentacion(pid):
    db = SessionLocal()
    try:
        p = db.get(Presentacion, pid)
        if not p:
            return jsonify({"error": "No encontrado"}), 404
        db.delete(p); db.commit()
        return jsonify({"message": "Eliminado"})
    finally:
        db.close()
