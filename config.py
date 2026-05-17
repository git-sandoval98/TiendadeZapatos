import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Flask
SECRET_KEY = os.environ.get("SECRET_KEY", "zapatosstore-secret-key-2026")

# SQLite (datos sensibles)
SQLITE_DB = os.path.join(os.path.dirname(__file__), "tienda.db")

# Apache Jena Fuseki (datos de negocio)
FUSEKI_URL = os.environ.get("FUSEKI_URL", "http://localhost:3030/TiendadeZapatos/query")
FUSEKI_UPDATE_URL = os.environ.get("FUSEKI_UPDATE_URL", "http://localhost:3030/TiendadeZapatos/update")

# Prefijo SPARQL
PREFIX = """
PREFIX : <http://www.semanticweb.org/Sergio/OntologiaTiendaZapatos#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""

# OpenRouter (IA)
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_URL = os.environ.get("OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions")
OPENROUTER_MODEL = os.environ.get("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free")