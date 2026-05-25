import requests
import os
import time
 
# Ruta absoluta al archivo de ontología
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ONTOLOGIA_PATH = os.path.join(BASE_DIR, "data", "ontologia.ttl")
 
 
def cargar_ontologia_en_fuseki(fuseki_base_url: str, dataset: str, admin_password: str, reintentos: int = 5):
    """
    Carga el archivo data/ontologia.ttl en Fuseki al arrancar la app.
    Si Fuseki está durmiendo en Render, reintenta automáticamente.
 
    Args:
        fuseki_base_url: URL base de Fuseki, ej: https://fuseki-tienda.onrender.com
        dataset: Nombre del dataset, ej: TiendadeZapatos
        admin_password: Contraseña del admin de Fuseki (variable de entorno FUSEKI_ADMIN_PASSWORD)
        reintentos: Número de intentos si Fuseki no responde aún
    """
    if not fuseki_base_url or "localhost" in fuseki_base_url or not fuseki_base_url.startswith("http"):
        print("[Fuseki Loader] FUSEKI_URL no apunta a un servidor real. Saltando carga de ontología.")
        return False
 
    # Endpoint para subir datos (Graph Store Protocol)
    upload_url = f"{fuseki_base_url}/{dataset}/data"
 
    if not os.path.exists(ONTOLOGIA_PATH):
        print(f"[Fuseki Loader] ERROR: No se encontró el archivo {ONTOLOGIA_PATH}")
        return False
 
    print(f"[Fuseki Loader] Intentando cargar ontología en Fuseki: {upload_url}")
 
    for intento in range(1, reintentos + 1):
        try:
            with open(ONTOLOGIA_PATH, "rb") as f:
                contenido = f.read()
 
            response = requests.put(
                upload_url,
                data=contenido,
                headers={"Content-Type": "text/turtle"},
                auth=("admin", admin_password),
                timeout=20
            )
 
            if response.status_code in (200, 201, 204):
                print(f"[Fuseki Loader] ✅ Ontología cargada exitosamente en Fuseki (intento {intento})")
                return True
            else:
                print(f"[Fuseki Loader] ⚠️ Respuesta inesperada de Fuseki: {response.status_code} - {response.text[:200]}")
 
        except requests.exceptions.ConnectionError:
            print(f"[Fuseki Loader] Fuseki no disponible aún (intento {intento}/{reintentos}). Reintentando en 5s...")
            time.sleep(5)
 
        except requests.exceptions.Timeout:
            print(f"[Fuseki Loader] Timeout al conectar con Fuseki (intento {intento}/{reintentos}). Reintentando en 5s...")
            time.sleep(5)
 
        except Exception as e:
            print(f"[Fuseki Loader] Error inesperado: {e}")
            break
 
    print("[Fuseki Loader] No se pudo cargar la ontología en Fuseki tras todos los intentos. Se usará RDFLib local.")
    return False
 
 
def inicializar_fuseki():
    """
    Función principal a llamar desde app.py al arrancar.
    Lee las variables de entorno automáticamente.
    """
    fuseki_url_completa = os.environ.get("FUSEKI_URL", "")
    admin_password = os.environ.get("FUSEKI_ADMIN_PASSWORD", "")
 
    if not fuseki_url_completa or not admin_password:
        print("[Fuseki Loader] Variables FUSEKI_URL o FUSEKI_ADMIN_PASSWORD no configuradas. Saltando.")
        return False
 
    # Extraer base_url y nombre del dataset desde FUSEKI_URL
    # Ejemplo: https://fuseki-tienda.onrender.com/TiendadeZapatos/query
    # → base_url = https://fuseki-tienda.onrender.com
    # → dataset  = TiendadeZapatos
    try:
        partes = fuseki_url_completa.rstrip("/").split("/")
        # Quitar el último segmento ("query") y el penúltimo es el dataset
        dataset = partes[-2]
        base_url = "/".join(partes[:-2])
    except IndexError:
        print(f"[Fuseki Loader] No se pudo parsear FUSEKI_URL: {fuseki_url_completa}")
        return False
 
    return cargar_ontologia_en_fuseki(base_url, dataset, admin_password)