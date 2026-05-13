from flask import Blueprint
from flask import render_template
from flask import request

from backend.services import (
    obtener_categorias,
    obtener_generos,
    generar_recomendacion
)

main_bp = Blueprint(
    "main",
    __name__
)

# =========================
# INICIO
# =========================

@main_bp.route("/", methods=["GET", "POST"])
def index():

    categorias = obtener_categorias()

    generos = obtener_generos()

    resultado = None

    recomendacion = None

    categoria_seleccionada = ""

    genero_seleccionado = ""

    if request.method == "POST":

        categoria_seleccionada = request.form["categoria"]

        genero_seleccionado = request.form["genero"]

        resultado = generar_recomendacion(

            categoria_seleccionada,
            genero_seleccionado

        )

        recomendacion = resultado["mensaje"]

    return render_template(

        "index.html",

        categorias=categorias,

        generos=generos,

        resultado=resultado,

        recomendacion=recomendacion,

        categoria_seleccionada=categoria_seleccionada,

        genero_seleccionado=genero_seleccionado,

        total_temporadas=4,

        total_categorias=len(categorias),

        total_generos=len(generos)

    )

# =========================
# DASHBOARD
# =========================

@main_bp.route("/dashboard")
def dashboard():

    from backend.services import (

        obtener_total_ventas,
        obtener_total_zapatos,
        obtener_total_inventario,
        obtener_total_alertas

    )

    total_ventas = obtener_total_ventas()

    total_zapatos = obtener_total_zapatos()

    total_inventario = obtener_total_inventario()

    total_alertas = obtener_total_alertas()

    return render_template(

        "dashboard.html",

        total_ventas=total_ventas,

        total_zapatos=total_zapatos,

        total_inventario=total_inventario,

        total_alertas=total_alertas

    )

# =========================
# IA
# =========================

@main_bp.route("/ia")
def ia():

    from backend.services import (
        obtener_analisis_ia
    )

    analisis = obtener_analisis_ia()

    return render_template(

        "ia.html",

        analisis=analisis

    )

# =========================
# TENDENCIAS
# =========================

@main_bp.route("/tendencias")
def tendencias():

    from backend.services import (
        obtener_tendencias
    )

    tendencias = obtener_tendencias()

    return render_template(

        "tendencias.html",

        tendencias=tendencias

    )

# =========================
# VENTAS
# =========================

@main_bp.route("/ventas")
def ventas():

    from backend.services import (
        obtener_ventas
    )

    ventas = obtener_ventas()

    return render_template(

        "ventas.html",

        ventas=ventas

    )

# =========================
# INVENTARIO
# =========================

@main_bp.route("/inventario")
def inventario():

    from backend.services import (
        obtener_inventario
    )

    inventarios = obtener_inventario()

    return render_template(

        "inventario.html",

        inventarios=inventarios

    )

# =========================
# ALERTAS
# =========================

@main_bp.route("/alertas")
def alertas():

    from backend.services import (
        obtener_alertas
    )

    alertas = obtener_alertas()

    return render_template(

        "alertas.html",

        alertas=alertas

    )