"""
API Routes Blueprint
Handles general API endpoints and utilities
"""

from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
import os
from datetime import datetime

api_bp = Blueprint('api', __name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api_bp.route('/api/upload-image', methods=['POST'])
def upload_image():
    """
    Handle car image upload
    Returns the uploaded image URL
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed types: png, jpg, jpeg, gif, webp'}), 400
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        return jsonify({'error': 'File too large. Maximum size is 5MB'}), 400
    
    try:
        # Generate secure filename with timestamp
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        
        # Save file
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(filepath)
        
        # Return the URL
        image_url = f"/static/uploads/{unique_filename}"
        
        return jsonify({
            'success': True,
            'image_url': image_url,
            'filename': unique_filename
        })
        
    except Exception as e:
        return jsonify({'error': f'Error uploading file: {str(e)}'}), 500


@api_bp.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Car Price Prediction API'
    })


@api_bp.route('/api/features', methods=['GET'])
def get_features():
    """Get feature information for the model"""
    features = [
        {
            'name': 'year',
            'label': 'Year of Manufacture',
            'type': 'number',
            'description': 'The year the car was manufactured',
            'min': 2000,
            'max': 2025
        },
        {
            'name': 'kilometers_driven',
            'label': 'Kilometers Driven',
            'type': 'number',
            'description': 'Total distance the car has been driven',
            'min': 0,
            'max': 500000
        },
        {
            'name': 'mileage',
            'label': 'Mileage',
            'type': 'number',
            'description': 'Fuel efficiency in kilometers per liter',
            'min': 0,
            'max': 50
        },
        {
            'name': 'engine_capacity',
            'label': 'Engine Capacity',
            'type': 'number',
            'description': 'Engine size in cubic centimeters (CC)',
            'min': 500,
            'max': 6000
        },
        {
            'name': 'company',
            'label': 'Car Company',
            'type': 'select',
            'description': 'Manufacturer of the car'
        },
        {
            'name': 'model',
            'label': 'Car Model',
            'type': 'select',
            'description': 'Specific model of the car'
        },
        {
            'name': 'fuel_type',
            'label': 'Fuel Type',
            'type': 'select',
            'description': 'Type of fuel the car uses'
        },
        {
            'name': 'transmission',
            'label': 'Transmission',
            'type': 'select',
            'description': 'Type of transmission'
        },
        {
            'name': 'owner_type',
            'label': 'Owner Type',
            'type': 'select',
            'description': 'Number of previous owners'
        }
    ]
    
    return jsonify({'features': features})
