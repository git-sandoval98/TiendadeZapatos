import requests
import os
import time
 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ONTOLOGIA_PATH = os.path.join(BASE_DIR, "data", "ontologia.ttl")
 
 
def crear_dataset(base_url, dataset, admin_password):
    """
    Crea el dataset en Fuseki si no existe.
    Usa la API de administración de Fuseki (/$/datasets).
    """
    admin_url = f"{base_url}/$/datasets"
    try:
        # Verificar si ya existe
        r = requests.get(
            admin_url,
            auth=("admin", admin_password),
            timeout=15
        )
        if r.status_code == 200:
            datasets_existentes = r.text
            if dataset in datasets_existentes:
                print(f"[Fuseki Loader] Dataset '{dataset}' ya existe, no es necesario crearlo.")
                return True
 
        # Crear el dataset (tipo mem = en memoria, o tdb2 = persistente)
        r = requests.post(
            admin_url,
            data={"dbName": dataset, "dbType": "mem"},
            auth=("admin", admin_password),
            timeout=15
        )
        if r.status_code in (200, 201):
            print(f"[Fuseki Loader] ✅ Dataset '{dataset}' creado exitosamente.")
            return True
        else:
            print(f"[Fuseki Loader] ⚠️ No se pudo crear el dataset: {r.status_code} - {r.text[:200]}")
            return False
    except Exception as e:
        print(f"[Fuseki Loader] Error creando dataset: {e}")
        return False
 
 
def cargar_ontologia(base_url, dataset, admin_password, reintentos=5):
    """
    Sube ontologia.ttl al dataset usando POST (más compatible que PUT).
    """
    upload_url = f"{base_url}/{dataset}/data"
 
    if not os.path.exists(ONTOLOGIA_PATH):
        print(f"[Fuseki Loader] ERROR: No se encontró {ONTOLOGIA_PATH}")
        return False
 
    for intento in range(1, reintentos + 1):
        try:
            with open(ONTOLOGIA_PATH, "rb") as f:
                contenido = f.read()
 
            # Usar POST en lugar de PUT (POST añade, PUT reemplaza — ambos deben funcionar)
            # pero primero intentamos con POST que es más permisivo
            response = requests.post(
                upload_url,
                data=contenido,
                headers={"Content-Type": "text/turtle"},
                auth=("admin", admin_password),
                timeout=20
            )
 
            if response.status_code in (200, 201, 204):
                print(f"[Fuseki Loader] ✅ Ontología cargada en Fuseki (intento {intento})")
                return True
            else:
                print(f"[Fuseki Loader] ⚠️ Error al subir ontología: {response.status_code} - {response.text[:200]}")
                time.sleep(3)
 
        except requests.exceptions.ConnectionError:
            print(f"[Fuseki Loader] Fuseki no disponible (intento {intento}/{reintentos}). Reintentando en 5s...")
            time.sleep(5)
        except requests.exceptions.Timeout:
            print(f"[Fuseki Loader] Timeout (intento {intento}/{reintentos}). Reintentando en 5s...")
            time.sleep(5)
        except Exception as e:
            print(f"[Fuseki Loader] Error inesperado: {e}")
            break
 
    print("[Fuseki Loader] ❌ No se pudo cargar la ontología. Se usará RDFLib local.")
    return False
 
 
def inicializar_fuseki():
    """
    Punto de entrada desde app.py.
    1. Lee variables de entorno
    2. Crea el dataset si no existe
    3. Carga la ontología
    """
    fuseki_url_completa = os.environ.get("FUSEKI_URL", "")
    admin_password = os.environ.get("FUSEKI_ADMIN_PASSWORD", "")
 
    if not fuseki_url_completa or not admin_password:
        print("[Fuseki Loader] FUSEKI_URL o FUSEKI_ADMIN_PASSWORD no configuradas. Saltando.")
        return False
 
    # Validar que no sea localhost ni URL falsa
    if "localhost" in fuseki_url_completa or not fuseki_url_completa.startswith("http"):
        print("[Fuseki Loader] FUSEKI_URL apunta a localhost. Saltando.")
        return False
 
    # Parsear base_url y dataset desde FUSEKI_URL
    # Ejemplo: https://fuseki-tienda.onrender.com/TiendadeZapatos/query
    try:
        partes = fuseki_url_completa.rstrip("/").split("/")
        dataset = partes[-2]       # "TiendadeZapatos"
        base_url = "/".join(partes[:-2])  # "https://fuseki-tienda.onrender.com"
    except IndexError:
        print(f"[Fuseki Loader] No se pudo parsear FUSEKI_URL: {fuseki_url_completa}")
        return False
 
    print(f"[Fuseki Loader] Base URL: {base_url} | Dataset: {dataset}")
 
    # Paso 1: crear dataset
    dataset_ok = crear_dataset(base_url, dataset, admin_password)
    if not dataset_ok:
        print("[Fuseki Loader] No se pudo asegurar el dataset. Abortando carga.")
        return False
 
    # Paso 2: cargar ontología
    return cargar_ontologia(base_url, dataset, admin_password)
