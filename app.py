from flask import Flask
from flask_cors import CORS
from routes.api import api_bp
import config

def create_app():
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Load configuration
    app.config.from_object(config.Config)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/')
    def health_check():
        return {"status": "healthy", "message": "Biological Insights API is running"}
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)