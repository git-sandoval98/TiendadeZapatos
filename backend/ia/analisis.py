def generar_analisis_ia(categoria, genero, temporada, ventas):

    texto = f"""
    El sistema inteligente detectó que la temporada '{temporada}'
    presenta el mayor comportamiento histórico de ventas para
    zapatos de categoría '{categoria}' y género '{genero}'.

    Basado en el análisis semántico de ventas registradas,
    se recomienda aumentar pedidos e inventario antes del
    inicio de esta temporada para maximizar disponibilidad
    y oportunidades comerciales.
    """

    if ventas >= 10:
        texto += """

        📈 Se identificó una demanda ALTA para esta combinación,
        lo cual indica una fuerte tendencia comercial.
        """

    elif ventas >= 5:
        texto += """

        📊 Se identificó una demanda MEDIA con comportamiento
        comercial estable.
        """

    else:
        texto += """

        📉 Se identificó una demanda BAJA, pero con potencial
        de crecimiento según temporadas anteriores.
        """

    return texto