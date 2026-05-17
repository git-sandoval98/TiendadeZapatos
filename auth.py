from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from database import obtener_usuario_por_email, crear_usuario, actualizar_ultimo_acceso

auth_bp = Blueprint("auth", __name__)


# --- Decoradores de proteccion ---

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        if session.get("user_rol") != "administrador":
            flash("Acceso denegado. Se requieren permisos de administrador.", "danger")
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)
    return decorated


# --- Rutas ---

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = obtener_usuario_por_email(email)

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["user_nombre"] = user["nombre"]
            session["user_apellido"] = user["apellido"]
            session["user_email"] = user["email"]
            session["user_rol"] = user["rol"]
            actualizar_ultimo_acceso(user["id"])
            return redirect(url_for("main.index"))
        else:
            flash("Correo o contrasena incorrectos.", "danger")

    return render_template("login.html")


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if "user_id" in session:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not all([nombre, apellido, email, password]):
            flash("Todos los campos son obligatorios.", "danger")
        elif len(password) < 6:
            flash("La contrasena debe tener al menos 6 caracteres.", "danger")
        else:
            password_hash = generate_password_hash(password)
            success = crear_usuario(nombre, apellido, email, password_hash, "usuario")
            if success:
                flash("Cuenta creada exitosamente. Inicia sesion.", "success")
                return redirect(url_for("auth.login"))
            else:
                flash("El correo ya esta registrado.", "danger")

    return render_template("registro.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
