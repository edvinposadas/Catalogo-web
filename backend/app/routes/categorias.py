
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from app.db.base import SessionLocal
from app.models.categoria import Categoria

categoria_bp = Blueprint("categorias", __name__, url_prefix="/api/categorias")

@categoria_bp.get("")
@categoria_bp.get("/")
@jwt_required()
def list_categorias():
    db = SessionLocal()
    try:
        page = int((request.args.get("page") or 1))
        per_page = int((request.args.get("per_page") or request.args.get("size") or 10))
        q = (request.args.get("q") or request.args.get("search") or "").strip()
        qry = db.query(Categoria)
        if q:
            qry = qry.filter(func.lower(Categoria.nombre).contains(q.lower()))
        total = qry.count()
        items = (qry.order_by(Categoria.id.desc())
                   .offset((page-1)*per_page)
                   .limit(per_page).all())
        return jsonify({
            "total": total, "page": page, "per_page": per_page,
            "items": [{"id": c.id, "nombre": c.nombre, "descripcion": c.descripcion} for c in items]
        })
    finally:
        db.close()

@categoria_bp.post("")
@categoria_bp.post("/")
@jwt_required()
def create_categoria():
    data = request.get_json() or {}
    nombre = (data.get("nombre") or "").strip()
    descripcion = (data.get("descripcion") or "").strip() or None
    if not nombre:
        return jsonify({"error": "El nombre es obligatorio"}), 400
    db = SessionLocal()
    try:
        c = Categoria(nombre=nombre, descripcion=descripcion)
        db.add(c); db.commit(); db.refresh(c)
        return jsonify({"id": c.id, "nombre": c.nombre, "descripcion": c.descripcion}), 201
    finally:
        db.close()

@categoria_bp.put("/<int:cid>")
@jwt_required()
def update_categoria(cid):
    data = request.get_json() or {}
    db = SessionLocal()
    try:
        c = db.get(Categoria, cid)
        if not c:
            return jsonify({"error": "No encontrado"}), 404
        if "nombre" in data: c.nombre = (data["nombre"] or "").strip()
        if "descripcion" in data: c.descripcion = (data["descripcion"] or "").strip() or None
        db.commit()
        return jsonify({"id": c.id, "nombre": c.nombre, "descripcion": c.descripcion})
    finally:
        db.close()

@categoria_bp.delete("/<int:cid>")
@jwt_required()
def delete_categoria(cid):
    db = SessionLocal()
    try:
        c = db.get(Categoria, cid)
        if not c:
            return jsonify({"error": "No encontrado"}), 404
        db.delete(c); db.commit()
        return jsonify({"message": "Eliminado"})
    finally:
        db.close()
