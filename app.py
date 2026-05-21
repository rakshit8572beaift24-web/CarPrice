"""
Car Price Prediction Flask Application - Premium Version
Main application with blueprint organization and enhanced features
"""

import sys
import os

# UTF-8 encoding setup for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from flask import Flask, render_template

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Register blueprints
from routes.prediction_routes import prediction_bp
from routes.comparison_routes import comparison_bp
from routes.api_routes import api_bp

app.register_blueprint(prediction_bp)
app.register_blueprint(comparison_bp)
app.register_blueprint(api_bp)


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('index.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('index.html'), 500


if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('static/uploads', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    print("=" * 60)
    print("🚗 AI Car Price Predictor - Premium Edition")
    print("=" * 60)
    print("✨ Features:")
    print("  • AI-Powered Price Prediction")
    print("  • Advanced Price Analysis")
    print("  • Car Comparison")
    print("  • Interactive Dashboard")
    print("  • PDF Report Generation")
    print("  • Image Upload")
    print("=" * 60)
    print("🌐 Starting Flask application...")
    print("=" * 60)
    
    # PRODUCTION DEPLOYMENT CONFIGURATION
    # ====================================
    # This app uses a simple app.run() configuration for maximum compatibility
    # with production deployment platforms (Render, Railway, Streamlit Cloud, etc.)
    #
    # Why we removed debug=True, host='0.0.0.0', port=5000:
    # - debug=True: Enables Flask's auto-reloader which uses signal handlers
    #   Signal handlers don't work in containerized/cloud environments
    #   This causes ValueError and signal handling errors during deployment
    # - host='0.0.0.0': Production servers (Gunicorn) handle binding
    # - port=5000: Production platforms set the PORT environment variable
    # - use_reloader: Causes signal handling issues in cloud environments
    #
    # How deployment works:
    # - Production: Gunicorn (from Procfile) serves the app
    # - Gunicorn reads the 'app' object from this file and serves it
    # - Gunicorn handles host binding, port configuration, and process management
    # - This simple app.run() is ignored by Gunicorn but kept for local testing
    #
    # Local development:
    # - Run with: python app.py
    # - Access at: http://127.0.0.1:5000 (Flask defaults)
    # - For debug mode locally, you can set environment variables or use Gunicorn
    
    # Simple app.run() - production-ready and deployment-safe
    # Production servers (Gunicorn) will use the 'app' object directly
    if __name__ == "__main__":
        app.run()
