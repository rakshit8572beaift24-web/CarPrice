"""
Routes package for Car Price Prediction Application
"""

from flask import Blueprint

# Create main blueprint
main_bp = Blueprint('main', __name__)

# Import routes
from routes import prediction_routes, comparison_routes, api_routes

# Register blueprints
from routes.prediction_routes import prediction_bp
from routes.comparison_routes import comparison_bp
from routes.api_routes import api_bp
