import os
from flask import Flask
from models import db
from routes import routes
from config import Config
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    
    # Crear tablas al arrancar
    with app.app_context():
        try:
            db.create_all()
            print("Tablas creadas exitosamente")
        except Exception as e:
            print(f"Error creando tablas: {e}")
    
    app.register_blueprint(routes)
    return app

# Crear la aplicación
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    debug = os.environ.get("FLASK_ENV") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)