from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from app.db.base import SessionLocal
from app.models.producto import Producto

producto_bp = Blueprint("productos", __name__, url_prefix="/api/productos")

# ------------------------------
# LISTAR (paginado + filtros)
# ------------------------------
@producto_bp.get("")
@producto_bp.get("/")
@jwt_required()
def list_productos():
    db = SessionLocal()
    try:
        page = int(request.args.get("page") or 1)
        per_page = int(request.args.get("per_page") or request.args.get("size") or 10)
        q = (request.args.get("q") or request.args.get("search") or "").strip()
        categoria_id = request.args.get("categoria_id")
        presentacion_id = request.args.get("presentacion_id")

        qry = db.query(Producto)
        if q:
            qry = qry.filter(func.lower(Producto.nombre).contains(q.lower()))
        if categoria_id:
            qry = qry.filter(Producto.categoria_id == int(categoria_id))
        if presentacion_id:
            qry = qry.filter(Producto.presentacion_id == int(presentacion_id))

        total = qry.count()
        items = (
            qry.order_by(Producto.id.desc())
               .offset((page - 1) * per_page)
               .limit(per_page)
               .all()
        )

        return jsonify({
            "total": total,
            "page": page,
            "per_page": per_page,
            "items": [{
                "id": p.id,
                "nombre": p.nombre,
                "precio": float(p.precio),
                "categoria_id": p.categoria_id,
                "presentacion_id": p.presentacion_id,
                "activo": p.activo
            } for p in items]
        })
    finally:
        db.close()

# ------------------------------
# CREAR
# ------------------------------
@producto_bp.post("")
@producto_bp.post("/")
@jwt_required()
def create_producto():
    data = request.get_json() or {}
    required = ["nombre", "precio", "categoria_id", "presentacion_id"]
    if any(k not in data or data[k] in [None, ""] for k in required):
        return jsonify({"error": "Campos requeridos: nombre, precio, categoria_id, presentacion_id"}), 400

    # Normalizar/castear
    nombre = (data.get("nombre") or "").strip()
    try:
        precio = float(data.get("precio"))
        categoria_id = int(data.get("categoria_id"))
        presentacion_id = int(data.get("presentacion_id"))
    except (TypeError, ValueError):
        return jsonify({"error": "Tipos inválidos en precio/categoria_id/presentacion_id"}), 400
    activo = bool(data.get("activo", True))

    db = SessionLocal()
    try:
        # Evitar duplicados por nombre (case-insensitive)
        dup = db.query(Producto).filter(func.lower(Producto.nombre) == nombre.lower()).first()
        if dup:
            return jsonify({"error": "Ya existe un producto con ese nombre"}), 409

        p = Producto(
            nombre=nombre,
            precio=precio,
            categoria_id=categoria_id,
            presentacion_id=presentacion_id,
            activo=activo,
        )
        db.add(p)
        db.commit()
        db.refresh(p)
        return jsonify({
            "id": p.id,
            "nombre": p.nombre,
            "precio": float(p.precio),
            "categoria_id": p.categoria_id,
            "presentacion_id": p.presentacion_id,
            "activo": p.activo
        }), 201
    except IntegrityError as e:
        db.rollback()
        # Mensaje amigable para FK/UNIQUE
        msg = str(e.orig).lower()
        if "foreign key" in msg and "categoria" in msg:
            return jsonify({"error": "La categoría indicada no existe"}), 400
        if "foreign key" in msg and "presentacion" in msg:
            return jsonify({"error": "La presentación indicada no existe"}), 400
        if "unique" in msg or "duplic" in msg:
            return jsonify({"error": "Ya existe un producto con ese nombre"}), 409
        return jsonify({"error": "Error de integridad en BD"}), 400
    finally:
        db.close()

# ------------------------------
# ACTUALIZAR
# ------------------------------
@producto_bp.put("/<int:pid>")
@jwt_required()
def update_producto(pid):
    data = request.get_json() or {}

    db = SessionLocal()
    try:
        p = db.get(Producto, pid)
        if not p:
            return jsonify({"error": "No encontrado"}), 404

        # Si viene nombre, validar duplicado contra otros
        if "nombre" in data and data["nombre"] is not None:
            nuevo_nombre = (str(data["nombre"]).strip())
            if nuevo_nombre and nuevo_nombre.lower() != (p.nombre or "").lower():
                dup = (
                    db.query(Producto)
                      .filter(func.lower(Producto.nombre) == nuevo_nombre.lower(), Producto.id != pid)
                      .first()
                )
                if dup:
                    return jsonify({"error": "Ya existe un producto con ese nombre"}), 409
                p.nombre = nuevo_nombre

        if "precio" in data and data["precio"] is not None:
            try:
                p.precio = float(data["precio"])
            except (TypeError, ValueError):
                return jsonify({"error": "Precio inválido"}), 400

        if "categoria_id" in data and data["categoria_id"] is not None:
            try:
                p.categoria_id = int(data["categoria_id"])
            except (TypeError, ValueError):
                return jsonify({"error": "categoria_id inválido"}), 400

        if "presentacion_id" in data and data["presentacion_id"] is not None:
            try:
                p.presentacion_id = int(data["presentacion_id"])
            except (TypeError, ValueError):
                return jsonify({"error": "presentacion_id inválido"}), 400

        if "activo" in data:
            p.activo = bool(data["activo"])

        db.commit()
        db.refresh(p)
        return jsonify({
            "id": p.id,
            "nombre": p.nombre,
            "precio": float(p.precio),
            "categoria_id": p.categoria_id,
            "presentacion_id": p.presentacion_id,
            "activo": p.activo
        })
    except IntegrityError as e:
        db.rollback()
        msg = str(e.orig).lower()
        if "foreign key" in msg and "categoria" in msg:
            return jsonify({"error": "La categoría indicada no existe"}), 400
        if "foreign key" in msg and "presentacion" in msg:
            return jsonify({"error": "La presentación indicada no existe"}), 400
        if "unique" in msg or "duplic" in msg:
            return jsonify({"error": "Ya existe un producto con ese nombre"}), 409
        return jsonify({"error": "Error de integridad en BD"}), 400
    finally:
        db.close()

# ------------------------------
# ELIMINAR
# ------------------------------
@producto_bp.delete("/<int:pid>")
@jwt_required()
def delete_producto(pid):
    db = SessionLocal()
    try:
        p = db.get(Producto, pid)
        if not p:
            return jsonify({"error": "No encontrado"}), 404
        db.delete(p)
        db.commit()
        return jsonify({"message": "Eliminado"})
    finally:
        db.close()
