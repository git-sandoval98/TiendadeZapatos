from flask import Flask
from config import SECRET_KEY
from database import init_db
from backend.routes import main_bp
from auth import auth_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)