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
    print("🌐 Access the application at: http://127.0.0.1:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
