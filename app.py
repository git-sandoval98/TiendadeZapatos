from flask import Flask
from config import SECRET_KEY
from database import init_db
from backend.routes import main_bp
from auth import auth_bp
from fuseki_loader import inicializar_fuseki
 
app = Flask(__name__)
app.secret_key = SECRET_KEY
 
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
 
with app.app_context():
    init_db()
 
# Cargar ontología en Fuseki al arrancar (si está configurado)
inicializar_fuseki()
 
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)