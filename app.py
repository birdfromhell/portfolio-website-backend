from flask import Flask
from flask_wtf.csrf import CSRFProtect
from src.models.models import db
from src.routes.api import api
from src.routes.admin import admin
import os

def create_app():
    app = Flask(__name__,
                template_folder='src/templates',
                static_folder='src/static')
                
    # Configuration
    app.config.update(
        SQLALCHEMY_DATABASE_URI='sqlite:///portfolio.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-key-please-change'),
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=1800  # 30 minutes
    )
    
    # Initialize extensions
    csrf = CSRFProtect()
    csrf.init_app(app)
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(admin, url_prefix='/admin')
    
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)