def generar_alerta_stock(ventas, stock_actual=5):

    if ventas > stock_actual:

        return (
            "El sistema detectó que el volumen de ventas "
            "supera el stock estimado disponible. "
            "Se recomienda generar nuevas órdenes de compra."
        )

    return None