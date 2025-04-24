"""
Flask application initialization.
"""

import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

from app.config import config

bootstrap = Bootstrap()
csrf = CSRFProtect()

def create_app(config_name=None):
    """Create and configure the Flask application."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config[config_name])

    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
    app.config['OUTPUT_FOLDER'] = os.path.join(app.root_path, 'static', 'output')

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

    bootstrap.init_app(app)
    csrf.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    register_error_handlers(app)

    register_template_filters(app)
    
    return app

def register_error_handlers(app):
    """Register error handlers with the Flask application."""
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

def register_template_filters(app):
    """Register custom template filters with the Flask application."""
    
    @app.template_filter('datetime')
    def format_datetime(value, format='%Y-%m-%d %H:%M:%S'):
        """Format a datetime object."""
        if value is None:
            return ""
        return value.strftime(format)
    
    @app.context_processor
    def utility_processor():
        """Add utility functions to template context."""
        def now(format_string="%Y"):
            """Get current year or date based on format string."""
            from datetime import datetime
            return datetime.now().strftime(format_string)
        
        return dict(now=now)