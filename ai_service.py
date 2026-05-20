import requests
from config import OPENROUTER_API_KEY, OPENROUTER_URL, OPENROUTER_MODEL


def obtener_respuesta_ia(mensaje_usuario, contexto_negocio, historial=None):
    if historial is None:
        historial = []

    system_prompt = f"""Eres el asistente comercial inteligente de ZapatosStore, una tienda de zapatos.
Tienes acceso a los siguientes datos reales de inventario y ventas de la tienda:

{contexto_negocio}

Instrucciones de comportamiento para ti:
1. Responde preguntas específicas sobre las cantidades, KPIs, ventas y stock del negocio utilizando EXCLUSIVAMENTE los datos del contexto de arriba. No inventes números de stock, ventas o modelos que no estén especificados allí.
2. Si te preguntan sobre géneros, categorías o tallas en mayor o menor cantidad, realiza el cálculo mental en base al bloque "Distribucion de Stock" provisto arriba.
3. Si el usuario te hace preguntas generales o te pide sugerencias sobre tendencias de moda, marketing digital, estrategias de venta, o consejos de negocio, tienes TOTAL LIBERTAD de responder con tu amplio conocimiento general sobre calzado y comercio.
4. Combina los datos de la tienda con tu conocimiento general de forma fluida. (Ejemplo: "Veo que tienes X unidades de Deportivo Unisex. Esta categoría es muy popular en verano porque...").
5. Si no tienes datos suficientes para responder algo específico del negocio, dilo honestamente diciendo: "No dispongo de ese dato exacto en el inventario actual, pero...".
6. Responde siempre en español, de forma profesional, elegante y concisa, utilizando formato Markdown claro (viñetas, negritas) para facilitar la lectura."""

    messages = [{"role": "system", "content": system_prompt}]

    for msg in historial[-10:]:
        messages.append({
            "role": msg["rol_mensaje"],
            "content": msg["contenido"]
        })

    messages.append({"role": "user", "content": mensaje_usuario})

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": OPENROUTER_MODEL,
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.7
            },
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "respuesta": data["choices"][0]["message"]["content"]
            }
        else:
            # Logs detallados para depuración
            print(f"[IA ERROR {response.status_code}]", flush=True)
            print(f"[BODY]: {response.text}", flush=True)
            return {
                "success": False,
                "respuesta": f"Error del servicio de IA (codigo {response.status_code}). Intenta de nuevo en unos momentos."
            }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "respuesta": "El servicio de IA tardo demasiado en responder. Intenta de nuevo."
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "respuesta": "No se pudo conectar al servicio de IA. Verifica tu conexion a internet."
        }
    except Exception as e:
        return {
            "success": False,
            "respuesta": f"Error inesperado: {str(e)}"
        }