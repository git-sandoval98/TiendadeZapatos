from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from backend.services import (
    obtener_kpis, obtener_tendencias, obtener_ventas,
    obtener_inventario, generar_alertas_basicas, obtener_resumen_negocio,
    agregar_producto_fuseki, eliminar_producto_fuseki
)
from ai_service import obtener_respuesta_ia
from auth import login_required, admin_required
from database import guardar_mensaje_chat, obtener_historial_chat, listar_usuarios

main_bp = Blueprint("main", __name__)

# --- Rutas Generales (Protegidas) ---

@main_bp.route("/")
@login_required
def index():
    return render_template("index.html")

@main_bp.route("/dashboard")
@login_required
def dashboard():
    kpis = obtener_kpis()
    alertas = generar_alertas_basicas()
    return render_template(
        "dashboard.html",
        total_ventas=kpis["ventas"],
        total_zapatos=kpis["zapatos"],
        total_inventario=kpis["inventario"],
        total_alertas=len(alertas)
    )

@main_bp.route("/tendencias")
@login_required
def tendencias():
    datos = obtener_tendencias()
    return render_template("tendencias.html", tendencias=datos)

@main_bp.route("/ventas")
@login_required
def ventas():
    datos = obtener_ventas()
    return render_template("ventas.html", ventas=datos)

@main_bp.route("/inventario")
@login_required
def inventario():
    datos = obtener_inventario()
    return render_template("inventario.html", inventarios=datos)

@main_bp.route("/alertas")
@login_required
def alertas():
    datos = generar_alertas_basicas()
    return render_template("alertas.html", alertas=datos)

# --- Rutas de Asistente IA ---

@main_bp.route("/asistente")
@login_required
def asistente():
    user_id = session.get("user_id")
    historial = obtener_historial_chat(user_id)
    return render_template("asistente.html", historial=historial)

@main_bp.route("/api/chat", methods=["POST"])
@login_required
def api_chat():
    data = request.get_json()
    mensaje_usuario = data.get("mensaje", "").strip()
    
    if not mensaje_usuario:
        return jsonify({"success": False, "error": "Mensaje vacio"})
        
    user_id = session.get("user_id")
    
    # 1. Guardar mensaje del usuario
    guardar_mensaje_chat(user_id, "user", mensaje_usuario)
    
    # 2. Obtener contexto y consultar a OpenRouter
    contexto = obtener_resumen_negocio()
    historial = obtener_historial_chat(user_id, limite=10) # pasar los ultimos 10 msg
    
    res = obtener_respuesta_ia(mensaje_usuario, contexto, historial)
    
    # 3. Guardar respuesta del asistente
    if res["success"]:
        guardar_mensaje_chat(user_id, "assistant", res["respuesta"])
        
    return jsonify(res)


# --- Rutas de Administracion ---

@main_bp.route("/admin/usuarios")
@admin_required
def admin_usuarios():
    usuarios = listar_usuarios()
    return render_template("admin_usuarios.html", usuarios=usuarios)

@main_bp.route("/admin/inventario")
@admin_required
def admin_inventario():
    datos = obtener_inventario()
    return render_template("admin_inventario.html", inventarios=datos)

@main_bp.route("/admin/inventario/agregar", methods=["POST"])
@admin_required
def admin_inventario_agregar():
    nombre = request.form.get("nombre")
    precio = request.form.get("precio")
    talla = request.form.get("talla")
    cantidad = request.form.get("cantidad")
    marca = request.form.get("marca")
    categoria = request.form.get("categoria")
    genero = request.form.get("genero")
    
    # Insertar en Fuseki
    if agregar_producto_fuseki(nombre, precio, talla, cantidad, marca, categoria, genero):
        flash("Producto agregado exitosamente a la base de datos semántica.", "success")
    else:
        flash("No se pudo agregar el producto. ¿Está encendido Fuseki?", "danger")
        
    return redirect(url_for("main.admin_inventario"))

@main_bp.route("/admin/inventario/eliminar")
@admin_required
def admin_inventario_eliminar():
    inv_id = request.args.get("id")
    if inv_id:
        if eliminar_producto_fuseki(inv_id):
            flash("Registro de inventario eliminado.", "success")
        else:
            flash("Error al eliminar.", "danger")
    return redirect(url_for("main.admin_inventario"))