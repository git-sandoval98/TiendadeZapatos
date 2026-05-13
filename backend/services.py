import requests

from backend.ia.analisis import generar_analisis_ia
from backend.ia.alertas import generar_alerta_stock

FUSEKI_URL = "http://localhost:3030/TiendadeZapatos/query"

PREFIX = """
PREFIX : <http://www.semanticweb.org/Sergio/OntologiaTiendaZapatos#>
"""

def ejecutar_query(query):

    response = requests.post(

        FUSEKI_URL,

        data={"query": query},

        headers={
            "Accept": "application/sparql-results+json"
        }

    )

    return response.json()

def obtener_categorias():

    query = PREFIX + """

    SELECT DISTINCT ?categoria
    WHERE {

        ?zapato :tieneCategoria ?categoria .

    }

    ORDER BY ?categoria
    """

    data = ejecutar_query(query)

    categorias = []

    for item in data["results"]["bindings"]:

        categorias.append(
            item["categoria"]["value"]
        )

    return categorias

def obtener_generos():

    query = PREFIX + """

    SELECT DISTINCT ?genero
    WHERE {

        ?zapato :tieneGenero ?genero .

    }

    ORDER BY ?genero
    """

    data = ejecutar_query(query)

    generos = []

    for item in data["results"]["bindings"]:

        generos.append(
            item["genero"]["value"]
        )

    return generos

def obtener_top_temporadas(categoria, genero):

    query = PREFIX + f"""

    SELECT ?nombreTemporada
           (COUNT(?venta) AS ?totalVentas)

    WHERE {{

        ?venta a :Venta ;
               :perteneceATemporada ?temporada ;
               :contieneDetalleVenta ?detalle .

        ?detalle :correspondeAInventario ?inventario .

        ?inventario :tieneZapato ?zapato .

        ?zapato :tieneCategoria ?categoria ;
                :tieneGenero ?genero .

        ?temporada :tieneNombreTemporada ?nombreTemporada .

        FILTER(LCASE(STR(?categoria)) = LCASE("{categoria}"))
        FILTER(LCASE(STR(?genero)) = LCASE("{genero}"))

    }}

    GROUP BY ?nombreTemporada

    ORDER BY DESC(?totalVentas)

    LIMIT 3
    """

    data = ejecutar_query(query)

    resultados = []

    for item in data["results"]["bindings"]:

        resultados.append({

            "temporada":
                item["nombreTemporada"]["value"],

            "ventas":
                int(item["totalVentas"]["value"])

        })

    return resultados

def obtener_rango_precios(categoria, genero):

    query = PREFIX + f"""

    SELECT
        (MIN(?precio) AS ?precioMin)
        (MAX(?precio) AS ?precioMax)
        (AVG(?precio) AS ?precioPromedio)

    WHERE {{

        ?zapato :tieneCategoria ?categoria ;
                :tieneGenero ?genero ;
                :tienePrecio ?precio .

        FILTER(LCASE(STR(?categoria)) = LCASE("{categoria}"))
        FILTER(LCASE(STR(?genero)) = LCASE("{genero}"))

    }}
    """

    data = ejecutar_query(query)

    bindings = data["results"]["bindings"]

    if not bindings:
        return None

    item = bindings[0]

    precio_min = item.get("precioMin")
    precio_max = item.get("precioMax")
    precio_promedio = item.get("precioPromedio")

    return {

        "min":
            round(float(precio_min["value"]), 2)
            if precio_min else 0,

        "max":
            round(float(precio_max["value"]), 2)
            if precio_max else 0,

        "promedio":
            round(float(precio_promedio["value"]), 2)
            if precio_promedio else 0

    }

def generar_recomendacion(categoria, genero):

    top_temporadas = obtener_top_temporadas(
        categoria,
        genero
    )

    if not top_temporadas:

        return {
            "mensaje":
                "No se encontraron ventas registradas para esa combinación.",
            "top_temporadas": [],
            "precios": None,
            "analisis_ia": None,
            "alerta_stock": None
        }

    mejor = top_temporadas[0]

    temporada = mejor["temporada"]

    ventas = mejor["ventas"]

    recomendacion = (
        f"La mejor temporada para aumentar pedidos de zapatos "
        f"{categoria.lower()} para {genero.lower()} es "
        f"{temporada}, ya que presenta "
        f"{ventas} ventas registradas."
    )

    analisis_ia = generar_analisis_ia(

        categoria,
        genero,
        temporada,
        ventas

    )

    alerta = generar_alerta_stock(ventas)

    precios = obtener_rango_precios(
        categoria,
        genero
    )

    return {

        "mensaje":
            recomendacion,

        "top_temporadas":
            top_temporadas,

        "precios":
            precios,

        "analisis_ia":
            analisis_ia,

        "alerta_stock":
            alerta

    }

def obtener_total_ventas():

    query = PREFIX + """

    SELECT (COUNT(?venta) AS ?total)

    WHERE {

        ?venta a :Venta .

    }
    """

    data = ejecutar_query(query)

    return int(
        data["results"]["bindings"][0]["total"]["value"]
    )

def obtener_total_zapatos():

    query = PREFIX + """

    SELECT (COUNT(?zapato) AS ?total)

    WHERE {

        ?zapato a :Zapato .

    }
    """

    data = ejecutar_query(query)

    return int(
        data["results"]["bindings"][0]["total"]["value"]
    )

def obtener_total_inventario():

    query = PREFIX + """

    SELECT (COUNT(?inventario) AS ?total)

    WHERE {

        ?inventario a :Inventario .

    }
    """

    data = ejecutar_query(query)

    return int(
        data["results"]["bindings"][0]["total"]["value"]
    )

def obtener_total_alertas():

    query = PREFIX + """

    SELECT (COUNT(?detalle) AS ?total)

    WHERE {

        ?detalle a :DetalleVenta .

    }
    """

    data = ejecutar_query(query)

    total = int(
        data["results"]["bindings"][0]["total"]["value"]
    )

    if total >= 20:
        return 5

    elif total >= 10:
        return 3

    return 1

def obtener_inventario():

    query = PREFIX + """

    SELECT ?inventario ?zapato ?categoria ?genero

    WHERE {

        ?inventario a :Inventario ;
                    :tieneZapato ?zapato .

        ?zapato :tieneCategoria ?categoria ;
                :tieneGenero ?genero .

    }

    LIMIT 50
    """

    data = ejecutar_query(query)

    resultados = []

    for item in data["results"]["bindings"]:

        resultados.append({

            "inventario":
                item["inventario"]["value"].split("#")[-1],

            "zapato":
                item["zapato"]["value"].split("#")[-1],

            "categoria":
                item["categoria"]["value"],

            "genero":
                item["genero"]["value"]

        })

    return resultados

def obtener_ventas():

    query = PREFIX + """

    SELECT ?venta ?temporada ?metodoPago

    WHERE {

        ?venta a :Venta ;
               :perteneceATemporada ?temp ;
               :tieneMetodoPago ?metodoPago .

        ?temp :tieneNombreTemporada ?temporada .

    }

    LIMIT 50
    """

    data = ejecutar_query(query)

    resultados = []

    for item in data["results"]["bindings"]:

        resultados.append({

            "venta":
                item["venta"]["value"].split("#")[-1],

            "temporada":
                item["temporada"]["value"],

            "metodo":
                item["metodoPago"]["value"]

        })

    return resultados

def obtener_tendencias():

    query = PREFIX + """

    SELECT ?temporada
           (COUNT(?venta) AS ?totalVentas)

    WHERE {

        ?venta a :Venta ;
               :perteneceATemporada ?temp .

        ?temp :tieneNombreTemporada ?temporada .

    }

    GROUP BY ?temporada

    ORDER BY DESC(?totalVentas)
    """

    data = ejecutar_query(query)

    resultados = []

    for item in data["results"]["bindings"]:

        resultados.append({

            "temporada":
                item["temporada"]["value"],

            "ventas":
                int(item["totalVentas"]["value"])

        })

    return resultados

def obtener_alertas():

    query = PREFIX + """

    SELECT ?categoria ?genero
           (COUNT(?venta) AS ?ventas)

    WHERE {

        ?venta a :Venta ;
               :contieneDetalleVenta ?detalle .

        ?detalle :correspondeAInventario ?inventario .

        ?inventario :tieneZapato ?zapato .

        ?zapato :tieneCategoria ?categoria ;
                :tieneGenero ?genero .

    }

    GROUP BY ?categoria ?genero

    ORDER BY DESC(?ventas)
    """

    data = ejecutar_query(query)

    alertas = []

    for item in data["results"]["bindings"]:

        categoria = item["categoria"]["value"]

        genero = item["genero"]["value"]

        ventas = int(item["ventas"]["value"])

        nivel = ""
        mensaje = ""

        if ventas >= 10:

            nivel = "ALTA"

            mensaje = (
                f"Alta demanda detectada para "
                f"{categoria} - {genero}. "
                f"Se recomienda aumentar inventario."
            )

        elif ventas >= 5:

            nivel = "MEDIA"

            mensaje = (
                f"Demanda estable para "
                f"{categoria} - {genero}."
            )

        else:

            nivel = "BAJA"

            mensaje = (
                f"Baja rotación para "
                f"{categoria} - {genero}."
            )

        alertas.append({

            "categoria": categoria,

            "genero": genero,

            "ventas": ventas,

            "nivel": nivel,

            "mensaje": mensaje

        })

    return alertas

def obtener_analisis_ia():

    query = PREFIX + """

    SELECT ?categoria ?genero
           (COUNT(?venta) AS ?ventas)

    WHERE {

        ?venta a :Venta ;
               :contieneDetalleVenta ?detalle ;
               :perteneceATemporada ?temp .

        ?detalle :correspondeAInventario ?inventario .

        ?inventario :tieneZapato ?zapato .

        ?zapato :tieneCategoria ?categoria ;
                :tieneGenero ?genero .

    }

    GROUP BY ?categoria ?genero

    ORDER BY DESC(?ventas)
    """

    data = ejecutar_query(query)

    resultados = []

    for item in data["results"]["bindings"]:

        categoria = item["categoria"]["value"]

        genero = item["genero"]["value"]

        ventas = int(item["ventas"]["value"])

        prioridad = ""
        recomendacion = ""
        impacto = ""

        if ventas >= 10:

            prioridad = "ALTA"

            impacto = "ALTO"

            recomendacion = (
                f"La inteligencia comercial detectó una "
                f"alta demanda para zapatos {categoria.lower()} "
                f"dirigidos al género {genero.lower()}. "
                f"Se recomienda aumentar inventario y "
                f"priorizar campañas comerciales."
            )

        elif ventas >= 5:

            prioridad = "MEDIA"

            impacto = "MEDIO"

            recomendacion = (
                f"El sistema detectó estabilidad comercial "
                f"en productos {categoria.lower()} "
                f"para {genero.lower()}."
            )

        else:

            prioridad = "BAJA"

            impacto = "BAJO"

            recomendacion = (
                f"Se detectó baja rotación comercial "
                f"en zapatos {categoria.lower()} "
                f"para {genero.lower()}."
            )

        resultados.append({

            "categoria": categoria,

            "genero": genero,

            "ventas": ventas,

            "prioridad": prioridad,

            "impacto": impacto,

            "recomendacion": recomendacion

        })

    return resultados