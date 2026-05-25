from SPARQLWrapper import SPARQLWrapper, JSON
import urllib.error
import socket
import os
import json
import rdflib
from config import FUSEKI_URL, PREFIX

# Determinar rutas absolutas del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ONTOLOGIA_PATH = os.path.join(BASE_DIR, "data", "ontologia.ttl")

def ejecutar_query(query, timeout=15.0):
    try:
        sparql = SPARQLWrapper(FUSEKI_URL)
        sparql.setQuery(PREFIX + query)
        sparql.setReturnFormat(JSON)
        # Timeout corto para no congelar la app si Fuseki esta apagado
        socket.setdefaulttimeout(15)
        resultados = sparql.query().convert()
        return resultados
    except Exception as e:
        print(f"Modo Offline RDFLib Activado: Consultando ontologia.ttl localmente... (Detalle: {e})")
        return ejecutar_query_local_rdflib(query)

def ejecutar_update(query):
    from config import FUSEKI_UPDATE_URL
    try:
        sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
        sparql.setQuery(PREFIX + query)
        sparql.method = "POST"
        sparql.query()
        return True
    except Exception as e:
        print(f"Fuseki offline para inserciones. Usando RDFLib localmente... (Detalle: {e})")
        return ejecutar_update_local_rdflib(query)

# --- Motor Ontologico Local (RDFLib) ---

def ejecutar_query_local_rdflib(query):
    try:
        if not os.path.exists(ONTOLOGIA_PATH):
            print(f"Error: No se encontro el archivo de ontologia en {ONTOLOGIA_PATH}")
            return obtener_datos_simulados(query)
            
        g = rdflib.Graph()
        g.parse(ONTOLOGIA_PATH, format="turtle")
        
        # Combinar el prefijo global con la consulta
        q_full = PREFIX + query
        qres = g.query(q_full)
        
        # Serializar al formato estandar SPARQL JSON
        res_bytes = qres.serialize(format="json")
        return json.loads(res_bytes.decode("utf-8"))
    except Exception as e:
        print(f"Error procesando SPARQL localmente con RDFLib: {e}. Activando fallback estatico.")
        return obtener_datos_simulados(query)

def ejecutar_update_local_rdflib(query):
    try:
        if not os.path.exists(ONTOLOGIA_PATH):
            print(f"Error: No se encontro el archivo de ontologia para actualizar en {ONTOLOGIA_PATH}")
            return False
            
        g = rdflib.Graph()
        g.parse(ONTOLOGIA_PATH, format="turtle")
        
        # Combinar el prefijo global con el update
        u_full = PREFIX + query
        g.update(u_full)
        
        # Guardar los cambios de vuelta en el archivo .ttl
        g.serialize(destination=ONTOLOGIA_PATH, format="turtle")
        print(f"¡Base Ontologica .ttl actualizada exitosamente en: {ONTOLOGIA_PATH}!")
        return True
    except Exception as e:
        print(f"Error ejecutando UPDATE SPARQL con RDFLib: {e}")
        return False

# --- Fallback Estatico Terciario (Seguridad Absoluta) ---

def obtener_datos_simulados(query):
    q_lower = query.lower()
    
    if "count(?venta)" in q_lower:
        return {"results": {"bindings": [{"total_ventas": {"value": "135"}}]}}
    if "count(?zapato)" in q_lower:
        return {"results": {"bindings": [{"total_zapatos": {"value": "30"}}]}}
    if "sum(?cantidad)" in q_lower:
        return {"results": {"bindings": [{"total_inventario": {"value": "450"}}]}}
    
    if "?zapato_nombre" in q_lower and "?inventario" in q_lower:
        return {"results": {"bindings": [
            {"inventario": {"value": "Inv_001"}, "zapato_nombre": {"value": "Air Max 270"}, "categoria_nombre": {"value": "Deportivo"}, "genero_nombre": {"value": "Hombre"}, "talla": {"value": "42"}, "cantidad": {"value": "15"}},
            {"inventario": {"value": "Inv_002"}, "zapato_nombre": {"value": "Classic Boot"}, "categoria_nombre": {"value": "Botas"}, "genero_nombre": {"value": "Hombre"}, "talla": {"value": "44"}, "cantidad": {"value": "8"}},
            {"inventario": {"value": "Inv_003"}, "zapato_nombre": {"value": "Suede Classic"}, "categoria_nombre": {"value": "Casual"}, "genero_nombre": {"value": "Unisex"}, "talla": {"value": "40"}, "cantidad": {"value": "30"}},
            {"inventario": {"value": "Inv_004"}, "zapato_nombre": {"value": "Ultraboost 22"}, "categoria_nombre": {"value": "Deportivo"}, "genero_nombre": {"value": "Mujer"}, "talla": {"value": "38"}, "cantidad": {"value": "10"}},
            {"inventario": {"value": "Inv_005"}, "zapato_nombre": {"value": "Chuck Taylor All Star"}, "categoria_nombre": {"value": "Casual"}, "genero_nombre": {"value": "Unisex"}, "talla": {"value": "41"}, "cantidad": {"value": "25"}},
            {"inventario": {"value": "Inv_006"}, "zapato_nombre": {"value": "Stan Smith"}, "categoria_nombre": {"value": "Casual"}, "genero_nombre": {"value": "Unisex"}, "talla": {"value": "42"}, "cantidad": {"value": "22"}},
            {"inventario": {"value": "Inv_007"}, "zapato_nombre": {"value": "Air Force 1"}, "categoria_nombre": {"value": "Casual"}, "genero_nombre": {"value": "Hombre"}, "talla": {"value": "43"}, "cantidad": {"value": "12"}},
            {"inventario": {"value": "Inv_008"}, "zapato_nombre": {"value": "Gel-Kayano 29"}, "categoria_nombre": {"value": "Deportivo"}, "genero_nombre": {"value": "Hombre"}, "talla": {"value": "42"}, "cantidad": {"value": "18"}},
            {"inventario": {"value": "Inv_009"}, "zapato_nombre": {"value": "Pegasus 40"}, "categoria_nombre": {"value": "Deportivo"}, "genero_nombre": {"value": "Mujer"}, "talla": {"value": "37"}, "cantidad": {"value": "14"}},
            {"inventario": {"value": "Inv_010"}, "zapato_nombre": {"value": "Vans Old Skool"}, "categoria_nombre": {"value": "Casual"}, "genero_nombre": {"value": "Unisex"}, "talla": {"value": "39"}, "cantidad": {"value": "40"}},
            {"inventario": {"value": "Inv_011"}, "zapato_nombre": {"value": "Dr. Martens 1460"}, "categoria_nombre": {"value": "Botas"}, "genero_nombre": {"value": "Unisex"}, "talla": {"value": "40"}, "cantidad": {"value": "5"}},
            {"inventario": {"value": "Inv_012"}, "zapato_nombre": {"value": "New Balance 574"}, "categoria_nombre": {"value": "Casual"}, "genero_nombre": {"value": "Hombre"}, "talla": {"value": "42"}, "cantidad": {"value": "16"}},
            {"inventario": {"value": "Inv_013"}, "zapato_nombre": {"value": "Cloudfoam Pure"}, "categoria_nombre": {"value": "Deportivo"}, "genero_nombre": {"value": "Mujer"}, "talla": {"value": "36"}, "cantidad": {"value": "25"}},
            {"inventario": {"value": "Inv_014"}, "zapato_nombre": {"value": "Chelsea Boots"}, "categoria_nombre": {"value": "Botas"}, "genero_nombre": {"value": "Mujer"}, "talla": {"value": "38"}, "cantidad": {"value": "9"}},
            {"inventario": {"value": "Inv_015"}, "zapato_nombre": {"value": "Oxford Leather"}, "categoria_nombre": {"value": "Formal"}, "genero_nombre": {"value": "Hombre"}, "talla": {"value": "41"}, "cantidad": {"value": "11"}},
            {"inventario": {"value": "Inv_016"}, "zapato_nombre": {"value": "Crocs Classic"}, "categoria_nombre": {"value": "Sandalias"}, "genero_nombre": {"value": "Unisex"}, "talla": {"value": "40"}, "cantidad": {"value": "50"}},
            {"inventario": {"value": "Inv_017"}, "zapato_nombre": {"value": "Birkenstock Arizona"}, "categoria_nombre": {"value": "Sandalias"}, "genero_nombre": {"value": "Unisex"}, "talla": {"value": "39"}, "cantidad": {"value": "30"}},
            {"inventario": {"value": "Inv_018"}, "zapato_nombre": {"value": "Puma RS-X"}, "categoria_nombre": {"value": "Deportivo"}, "genero_nombre": {"value": "Hombre"}, "talla": {"value": "43"}, "cantidad": {"value": "15"}},
            {"inventario": {"value": "Inv_019"}, "zapato_nombre": {"value": "Reebok Club C"}, "categoria_nombre": {"value": "Casual"}, "genero_nombre": {"value": "Mujer"}, "talla": {"value": "38"}, "cantidad": {"value": "20"}},
            {"inventario": {"value": "Inv_020"}, "zapato_nombre": {"value": "Mocasin Elegante"}, "categoria_nombre": {"value": "Formal"}, "genero_nombre": {"value": "Hombre"}, "talla": {"value": "42"}, "cantidad": {"value": "7"}}
        ]}}
        
    if "?venta" in q_lower and "?metodo_nombre" in q_lower:
        return {"results": {"bindings": [
            {"venta": {"value": "Venta_001"}, "temporada_nombre": {"value": "Verano"}, "metodo_nombre": {"value": "Tarjeta de Crédito"}},
            {"venta": {"value": "Venta_002"}, "temporada_nombre": {"value": "Invierno"}, "metodo_nombre": {"value": "Efectivo"}},
            {"venta": {"value": "Venta_003"}, "temporada_nombre": {"value": "Primavera"}, "metodo_nombre": {"value": "Transferencia"}},
            {"venta": {"value": "Venta_004"}, "temporada_nombre": {"value": "Verano"}, "metodo_nombre": {"value": "Efectivo"}},
            {"venta": {"value": "Venta_005"}, "temporada_nombre": {"value": "Otoño"}, "metodo_nombre": {"value": "Tarjeta de Débito"}}
        ]}}
        
    if "?temporada_nombre) as ?ventas" in q_lower or "?temporada_nombre) as ?ventas" in q_lower.replace(" ", ""):
        return {"results": {"bindings": [
            {"temporada_nombre": {"value": "Verano"}, "ventas": {"value": "65"}},
            {"temporada_nombre": {"value": "Invierno"}, "ventas": {"value": "40"}},
            {"temporada_nombre": {"value": "Primavera"}, "ventas": {"value": "30"}},
            {"temporada_nombre": {"value": "Otoño"}, "ventas": {"value": "25"}}
        ]}}
        
    return {"results": {"bindings": []}}

# --- Funciones de Negocio ---

def obtener_kpis():
    res_ventas = ejecutar_query("SELECT (COUNT(?venta) AS ?total_ventas) WHERE { ?venta a :Venta }")
    res_zapatos = ejecutar_query("SELECT (COUNT(?zapato) AS ?total_zapatos) WHERE { ?zapato a :Zapato }")
    res_inv = ejecutar_query("SELECT (SUM(?cantidad) AS ?total_inventario) WHERE { ?inv a :Inventario ; :cantidad ?cantidad }")
    
    try:
        ventas = res_ventas["results"]["bindings"][0]["total_ventas"]["value"]
    except: ventas = "0"
    
    try:
        zapatos = res_zapatos["results"]["bindings"][0]["total_zapatos"]["value"]
    except: zapatos = "0"
        
    try:
        inv = res_inv["results"]["bindings"][0]["total_inventario"]["value"]
    except: inv = "0"
        
    return {"ventas": ventas, "zapatos": zapatos, "inventario": inv}

def obtener_inventario():
    query = """
    SELECT ?inventario ?zapato_nombre ?categoria_nombre ?genero_nombre ?talla ?cantidad
    WHERE {
      ?inventario a :Inventario ;
                  :tieneZapato ?zapato ;
                  :talla ?talla ;
                  :cantidad ?cantidad .
      ?zapato :nombre ?zapato_nombre ;
              :tieneCategoria ?categoria ;
              :tieneGenero ?genero .
      ?categoria :nombre ?categoria_nombre .
      ?genero :nombre ?genero_nombre .
    } LIMIT 50
    """
    resultados = ejecutar_query(query)
    inventarios = []
    for row in resultados["results"]["bindings"]:
        inventarios.append({
            "inventario": row.get("inventario", {}).get("value", ""),
            "zapato": row.get("zapato_nombre", {}).get("value", ""),
            "categoria": row.get("categoria_nombre", {}).get("value", ""),
            "genero": row.get("genero_nombre", {}).get("value", ""),
            "talla": int(row.get("talla", {}).get("value", 0)),
            "cantidad": int(row.get("cantidad", {}).get("value", 0))
        })
    return inventarios

def obtener_ventas():
    query = """
    SELECT ?venta ?temporada_nombre ?metodo_nombre
    WHERE {
      ?venta a :Venta ;
             :perteneceATemporada ?temporada ;
             :tieneMetodoPago ?metodo .
      ?temporada :nombreTemporada ?temporada_nombre .
      ?metodo :nombre ?metodo_nombre .
    } ORDER BY DESC(?venta) LIMIT 50
    """
    resultados = ejecutar_query(query)
    ventas = []
    for row in resultados["results"]["bindings"]:
        ventas.append({
            "venta": row.get("venta", {}).get("value", ""),
            "temporada": row.get("temporada_nombre", {}).get("value", ""),
            "metodo": row.get("metodo_nombre", {}).get("value", "")
        })
    return ventas

def obtener_tendencias():
    query = """
    SELECT ?temporada_nombre (COUNT(?venta) AS ?ventas)
    WHERE {
      ?venta a :Venta ;
             :perteneceATemporada ?temporada .
      ?temporada :nombreTemporada ?temporada_nombre .
    } GROUP BY ?temporada_nombre
    """
    resultados = ejecutar_query(query)
    tendencias = []
    for row in resultados["results"]["bindings"]:
        tendencias.append({
            "temporada": row.get("temporada_nombre", {}).get("value", ""),
            "ventas": int(row.get("ventas", {}).get("value", 0))
        })
    return tendencias

def generar_alertas_basicas():
    return [
        {"categoria": "Deportivo", "genero": "Hombre", "ventas": 55, "nivel": "ALTA", "mensaje": "Stock rotando rapido, reabastecer."},
        {"categoria": "Botas", "genero": "Hombre", "ventas": 5, "nivel": "BAJA", "mensaje": "Stock estancado. Considerar promocion."},
        {"categoria": "Casual", "genero": "Unisex", "ventas": 25, "nivel": "MEDIA", "mensaje": "Flujo normal."}
    ]

def obtener_resumen_negocio():
    kpis = obtener_kpis()
    tends = obtener_tendencias()
    inventario_detalle = obtener_inventario()
    
    # Calcular cantidades por genero y categoria
    generos = {}
    categorias = {}
    detalle_zapatos = []
    
    for item in inventario_detalle:
        gen = item["genero"]
        cat = item["categoria"]
        cant = item["cantidad"]
        zap = item["zapato"]
        talla = item["talla"]
        
        generos[gen] = generos.get(gen, 0) + cant
        categorias[cat] = categorias.get(cat, 0) + cant
        detalle_zapatos.append(f"  * {zap} (Cat: {cat}, Gen: {gen}, Talla: {talla}): {cant} unidades")
        
    resumen = f"- Total ventas historicas: {kpis['ventas']}\n"
    resumen += f"- Total unidades en inventario: {kpis['inventario']}\n"
    resumen += f"- Modelos de zapatos en catalogo: {kpis['zapatos']}\n"
    
    resumen += "- Distribucion de Stock por GENERO:\n"
    for g, c in generos.items():
        resumen += f"  * {g}: {c} unidades en total\n"
        
    resumen += "- Distribucion de Stock por CATEGORIA:\n"
    for cat, c in categorias.items():
        resumen += f"  * {cat}: {c} unidades en total\n"
        
    resumen += "- Ventas por Temporada:\n"
    for t in tends:
        resumen += f"  * {t['temporada']}: {t['ventas']} ventas registradas\n"
        
    resumen += "- Detalle Completo de Inventario (Primeros 25 items):\n"
    resumen += "\n".join(detalle_zapatos[:25])
    
    return resumen

# --- CRUD RDF ---
def agregar_producto_fuseki(nombre, precio, talla, cantidad, marca_id, categoria_id, genero_id):
    import time
    timestamp = int(time.time())
    zap_id = f"Zap_{timestamp}"
    inv_id = f"Inv_{timestamp}"
    
    query = f"""
    INSERT DATA {{
      :{zap_id} a :Zapato ;
                :nombre "{nombre}" ;
                :precio {precio} ;
                :tieneMarca :{marca_id} ;
                :tieneCategoria :{categoria_id} ;
                :tieneGenero :{genero_id} .
                
      :{inv_id} a :Inventario ;
                :tieneZapato :{zap_id} ;
                :talla {talla} ;
                :cantidad {cantidad} .
    }}
    """
    return ejecutar_update(query)

def eliminar_producto_fuseki(inv_id):
    query = f"""
    DELETE WHERE {{
      :{inv_id} ?p ?o .
    }}
    """
    return ejecutar_update(query)