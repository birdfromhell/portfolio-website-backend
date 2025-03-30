from flask import Flask
from flask_wtf.csrf import CSRFProtect
from src.models.models import db
from src.routes.api import api
from src.routes.admin import admin
import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__,
                template_folder='src/templates',
                static_folder='src/static')
                
    # Configuration
    app.config.update(
        SQLALCHEMY_DATABASE_URI='sqlite:///portfolio.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-key-please-change'),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=1800  # 30 minutes
    )
    
    # Remove SESSION_COOKIE_SECURE for local development
    if not app.debug:
        app.config['SESSION_COOKIE_SECURE'] = True

    # Configure Cloudinary
    try:
        cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
        api_key = os.environ.get('CLOUDINARY_API_KEY')
        api_secret = os.environ.get('CLOUDINARY_API_SECRET')
        
        if not cloud_name or not api_key or not api_secret:
            print("WARNING: Missing Cloudinary credentials:")
            print(f"  CLOUDINARY_CLOUD_NAME: {'✓' if cloud_name else '✗'}")
            print(f"  CLOUDINARY_API_KEY: {'✓' if api_key else '✗'}")
            print(f"  CLOUDINARY_API_SECRET: {'✓' if api_secret else '✗'}")
        
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        print("Cloudinary configured successfully")
    except Exception as e:
        print(f"Error configuring Cloudinary: {e}")
    
    # Initialize extensions
    csrf = CSRFProtect()
    csrf.init_app(app)
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(admin, url_prefix='/admin')
    
    with app.app_context():
        db.create_all()
    
    return app  # Return the app object, not flask_app

# Create a global flask application instance for WSGI servers to use
flask_app = create_app()

if __name__ == '__main__':
    flask_app.run(debug=True)