from config import PREFIX

def consulta_categorias():
    return PREFIX + """
    SELECT DISTINCT ?categoria
    WHERE {
      ?zapato a :Zapato ;
              :tieneCategoria ?categoria .
    }
    ORDER BY ?categoria
    """

def consulta_generos():
    return PREFIX + """
    SELECT DISTINCT ?genero
    WHERE {
      ?zapato a :Zapato ;
              :tieneGenero ?genero .
    }
    ORDER BY ?genero
    """

def consulta_top_temporadas(categoria, genero):
    return PREFIX + f"""
    SELECT ?nombreTemporada (COUNT(?venta) AS ?totalVentas)
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

def consulta_top_marcas(categoria, genero):
    return PREFIX + f"""
    SELECT ?marca (COUNT(?venta) AS ?totalVentas)
    WHERE {{
      ?venta a :Venta ;
             :contieneDetalleVenta ?detalle .

      ?detalle :correspondeAInventario ?inventario .
      ?inventario :tieneZapato ?zapato .

      ?zapato :tieneCategoria ?categoria ;
              :tieneGenero ?genero ;
              :tieneMarca ?marca .

      FILTER(LCASE(STR(?categoria)) = LCASE("{categoria}"))
      FILTER(LCASE(STR(?genero)) = LCASE("{genero}"))
    }}
    GROUP BY ?marca
    ORDER BY DESC(?totalVentas)
    LIMIT 3
    """

def consulta_rango_precios(categoria, genero):
    return PREFIX + f"""
    SELECT (MIN(?precio) AS ?precioMin) (MAX(?precio) AS ?precioMax) (AVG(?precio) AS ?precioPromedio)
    WHERE {{
      ?zapato a :Zapato ;
              :tieneCategoria ?categoria ;
              :tieneGenero ?genero ;
              :tienePrecio ?precio .

      FILTER(LCASE(STR(?categoria)) = LCASE("{categoria}"))
      FILTER(LCASE(STR(?genero)) = LCASE("{genero}"))
    }}
    """