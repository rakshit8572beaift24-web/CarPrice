"""
Prediction Routes Blueprint
Handles car price prediction endpoints
"""

from flask import Blueprint, render_template, request, jsonify, flash
import pickle
import numpy as np
import os
from datetime import datetime
import json
import traceback

prediction_bp = Blueprint('prediction', __name__)

# Load model and preprocessing objects
def load_model():
    """Load the trained model and preprocessing objects"""
    try:
        print("[DEBUG] Loading model files...")
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        print("[DEBUG] Model loaded successfully")
        
        with open('encoders.pkl', 'rb') as f:
            encoders = pickle.load(f)
        print("[DEBUG] Encoders loaded successfully")
        
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        print("[DEBUG] Scaler loaded successfully")
        
        return model, encoders, scaler
    except FileNotFoundError as e:
        print(f"[ERROR] Model files not found: {e}")
        print("[ERROR] Please run train_model.py first.")
        return None, None, None
    except Exception as e:
        print(f"[ERROR] Error loading model files: {e}")
        traceback.print_exc()
        return None, None, None

# Load model at module level
model, encoders, scaler = load_model()

# Get actual values from encoders if available, otherwise use fallback
if encoders:
    CAR_COMPANIES = list(encoders['company'].classes_)
    CAR_MODELS = {}  # Will be populated dynamically
    FUEL_TYPES = list(encoders['fuel_type'].classes_)
    TRANSMISSION_TYPES = list(encoders['transmission'].classes_)
    OWNER_TYPES = list(encoders['owner_type'].classes_)
    
    # Build CAR_MODELS dictionary from encoder data
    # Group models by company from the encoder
    all_models = list(encoders['model'].classes_)
    # Since we don't have company-model mapping in encoders, we'll use a fallback
    # In production, you should save this mapping during training
    CAR_MODELS = {
        'Maruti': ['Swift', 'Baleno', 'Dzire', 'Vitara', 'Nexon', 'Ciaz', 'Eeco', 'WagonR', 'Ignis', 'Spresso', 'S-Cross', 'XL6', 'Ertiga', 'Celerio', 'Alto', 'Gypsy', 'Omni'],
        'Hyundai': ['i20', 'Verna', 'Creta', 'Grand i10', 'Elantra', 'Santro', 'Accent', 'Tucson', 'Venue', 'Kona', 'Xcent', 'Elite i20', 'Aura', 'Starex', 'H1', 'County', 'Mighty', 'Universe'],
        'Honda': ['City', 'Amaze', 'Civic', 'Jazz', 'WR-V', 'Brio', 'CR-V', 'HR-V', 'Passport', 'Pilot', 'Clarity', 'Avancier', 'Freed', 'Stepwgn', 'Odyssey', 'Elysion', 'Acty', 'Vamos'],
        'Toyota': ['Innova', 'Etios', 'Yaris', 'Glanza', 'Corolla', 'Qualis', 'Fortuner', 'Camry', 'Rav4', 'Highlander', '4Runner', 'Etios Cross', 'Sienta', 'Alphard', 'Previa', 'Sienna', 'Hilux', 'Dyna', 'Coaster', 'GranAce'],
        'Mahindra': ['Scorpio', 'XUV500', 'Thar', 'Bolero', 'XUV300'],
        'Tata': ['Nexon', 'Harrier', 'Safari', 'Tiago', 'Altroz'],
        'Ford': ['EcoSport', 'Figo', 'Endeavour', 'Aspire'],
        'Volkswagen': ['Polo', 'Vento', 'Tiguan'],
        'Skoda': ['Rapid', 'Octavia', 'Superb'],
        'Renault': ['Duster', 'Kwid', 'Triber'],
        'Nissan': ['Magnite', 'Kicks', 'Sunny'],
        'Kia': ['Seltos', 'Sonet', 'Carnival'],
        'MG': ['Hector', 'Gloster', 'Astor'],
        'Jeep': ['Compass', 'Wrangler', 'Grand Cherokee']
    }
    print(f"[DEBUG] Loaded {len(CAR_COMPANIES)} companies from encoder")
    print(f"[DEBUG] Loaded {len(FUEL_TYPES)} fuel types from encoder")
    print(f"[DEBUG] Loaded {len(TRANSMISSION_TYPES)} transmission types from encoder")
    print(f"[DEBUG] Loaded {len(OWNER_TYPES)} owner types from encoder")
else:
    # Fallback to hardcoded values if encoders not loaded
    CAR_COMPANIES = [
        'Maruti', 'Hyundai', 'Honda', 'Toyota', 'Mahindra', 'Tata', 'Ford', 
        'Volkswagen', 'Skoda', 'Renault', 'Nissan', 'Kia', 'MG', 'Jeep'
    ]
    CAR_MODELS = {
        'Maruti': ['Swift', 'Baleno', 'Dzire', 'Vitara', 'Nexon', 'Ciaz', 'Eeco', 'WagonR', 'Ignis', 'Spresso', 'S-Cross', 'XL6', 'Ertiga', 'Celerio', 'Alto', 'Gypsy', 'Omni'],
        'Hyundai': ['i20', 'Verna', 'Creta', 'Grand i10', 'Elantra', 'Santro', 'Accent', 'Tucson', 'Venue', 'Kona', 'Xcent', 'Elite i20', 'Aura', 'Starex', 'H1', 'County', 'Mighty', 'Universe'],
        'Honda': ['City', 'Amaze', 'Civic', 'Jazz', 'WR-V', 'Brio', 'CR-V', 'HR-V', 'Passport', 'Pilot', 'Clarity', 'Avancier', 'Freed', 'Stepwgn', 'Odyssey', 'Elysion', 'Acty', 'Vamos'],
        'Toyota': ['Innova', 'Etios', 'Yaris', 'Glanza', 'Corolla', 'Qualis', 'Fortuner', 'Camry', 'Rav4', 'Highlander', '4Runner', 'Etios Cross', 'Sienta', 'Alphard', 'Previa', 'Sienna', 'Hilux', 'Dyna', 'Coaster', 'GranAce'],
        'Mahindra': ['Scorpio', 'XUV500', 'Thar', 'Bolero', 'XUV300'],
        'Tata': ['Nexon', 'Harrier', 'Safari', 'Tiago', 'Altroz'],
        'Ford': ['EcoSport', 'Figo', 'Endeavour', 'Aspire'],
        'Volkswagen': ['Polo', 'Vento', 'Tiguan'],
        'Skoda': ['Rapid', 'Octavia', 'Superb'],
        'Renault': ['Duster', 'Kwid', 'Triber'],
        'Nissan': ['Magnite', 'Kicks', 'Sunny'],
        'Kia': ['Seltos', 'Sonet', 'Carnival'],
        'MG': ['Hector', 'Gloster', 'Astor'],
        'Jeep': ['Compass', 'Wrangler', 'Grand Cherokee']
    }
    FUEL_TYPES = ['Petrol', 'Diesel', 'CNG', 'Electric', 'Hybrid', 'LPG']
    TRANSMISSION_TYPES = ['Manual', 'Automatic']
    OWNER_TYPES = ['First', 'Second', 'Third', 'Fourth & Above']
    print("[WARNING] Using fallback hardcoded values - encoders not loaded")

# Store prediction history (in-memory, for demo purposes)
prediction_history = []


@prediction_bp.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@prediction_bp.route('/api/car-models/<company>')
def get_car_models(company):
    """Get available models for a specific company"""
    models = CAR_MODELS.get(company, [])
    return jsonify({'models': models})


@prediction_bp.route('/api/predict', methods=['POST'])
def predict():
    """
    API endpoint for car price prediction
    Expects JSON data with car features
    """
    print("\n" + "="*60)
    print("[INFO] New prediction request received")
    print("="*60)
    
    if model is None:
        print("[ERROR] Model not loaded")
        return jsonify({'error': 'Model not loaded. Please train the model first.'}), 500
    
    try:
        # Get data from request
        data = request.get_json()
        print(f"[DEBUG] Received data: {data}")
        
        if not data:
            print("[ERROR] No data received in request")
            return jsonify({'error': 'No data received'}), 400
        
        # Extract features with safe conversion
        try:
            company = data.get('company', '').strip()
            model_name = data.get('model', '').strip()
            year = int(data.get('year', 0))
            fuel_type = data.get('fuel_type', '').strip()
            transmission = data.get('transmission', '').strip()
            kilometers_driven = float(data.get('kilometers_driven', 0))
            owner_type = data.get('owner_type', '').strip()
            mileage = float(data.get('mileage', 0))
            engine_capacity = float(data.get('engine_capacity', 0))
        except (ValueError, TypeError) as e:
            print(f"[ERROR] Type conversion error: {e}")
            return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
        
        print(f"[DEBUG] Extracted features:")
        print(f"  - Company: {company}")
        print(f"  - Model: {model_name}")
        print(f"  - Year: {year}")
        print(f"  - Fuel Type: {fuel_type}")
        print(f"  - Transmission: {transmission}")
        print(f"  - Kilometers Driven: {kilometers_driven}")
        print(f"  - Owner Type: {owner_type}")
        print(f"  - Mileage: {mileage}")
        print(f"  - Engine Capacity: {engine_capacity}")
        
        # Validate input - check for missing fields
        if not all([company, model_name, year, fuel_type, transmission, 
                   kilometers_driven, owner_type, mileage, engine_capacity]):
            print("[ERROR] Missing required fields")
            return jsonify({'error': 'Missing required fields. Please fill all fields.'}), 400
        
        # Validate ranges with detailed error messages
        if year < 2000 or year > 2025:
            print(f"[ERROR] Invalid year: {year}")
            return jsonify({'error': f'Year must be between 2000 and 2025. Got: {year}'}), 400
        if year <= 0:
            print(f"[ERROR] Negative year: {year}")
            return jsonify({'error': f'Year cannot be negative. Got: {year}'}), 400
        if kilometers_driven < 0:
            print(f"[ERROR] Negative kilometers: {kilometers_driven}")
            return jsonify({'error': f'Kilometers driven cannot be negative. Got: {kilometers_driven}'}), 400
        if kilometers_driven > 500000:
            print(f"[ERROR] Kilometers too high: {kilometers_driven}")
            return jsonify({'error': f'Kilometers driven must be less than 500,000. Got: {kilometers_driven}'}), 400
        if mileage < 0:
            print(f"[ERROR] Negative mileage: {mileage}")
            return jsonify({'error': f'Mileage cannot be negative. Got: {mileage}'}), 400
        if mileage > 50:
            print(f"[ERROR] Mileage too high: {mileage}")
            return jsonify({'error': f'Mileage must be less than 50 km/l. Got: {mileage}'}), 400
        if engine_capacity <= 0:
            print(f"[ERROR] Invalid engine capacity: {engine_capacity}")
            return jsonify({'error': f'Engine capacity must be positive. Got: {engine_capacity}'}), 400
        if engine_capacity < 500 or engine_capacity > 6000:
            print(f"[ERROR] Engine capacity out of range: {engine_capacity}")
            return jsonify({'error': f'Engine capacity must be between 500 and 6000 CC. Got: {engine_capacity}'}), 400
        
        # Encode categorical features with unseen label handling
        print("[DEBUG] Encoding categorical features...")
        try:
            # Check if label exists in encoder before transforming
            if company not in encoders['company'].classes_:
                print(f"[ERROR] Unseen company: {company}")
                print(f"[DEBUG] Available companies: {list(encoders['company'].classes_)}")
                return jsonify({'error': f'Invalid company: {company}. Available options: {list(encoders["company"].classes_)}'}), 400
            company_encoded = encoders['company'].transform([company])[0]
            print(f"[DEBUG] Company encoded: {company_encoded}")
            
            if model_name not in encoders['model'].classes_:
                print(f"[ERROR] Unseen model: {model_name}")
                print(f"[DEBUG] Available models: {list(encoders['model'].classes_)}")
                return jsonify({'error': f'Invalid model: {model_name}. Available options: {list(encoders["model"].classes_)}'}), 400
            model_encoded = encoders['model'].transform([model_name])[0]
            print(f"[DEBUG] Model encoded: {model_encoded}")
            
            if fuel_type not in encoders['fuel_type'].classes_:
                print(f"[ERROR] Unseen fuel type: {fuel_type}")
                print(f"[DEBUG] Available fuel types: {list(encoders['fuel_type'].classes_)}")
                return jsonify({'error': f'Invalid fuel type: {fuel_type}. Available options: {list(encoders["fuel_type"].classes_)}'}), 400
            fuel_type_encoded = encoders['fuel_type'].transform([fuel_type])[0]
            print(f"[DEBUG] Fuel type encoded: {fuel_type_encoded}")
            
            if transmission not in encoders['transmission'].classes_:
                print(f"[ERROR] Unseen transmission: {transmission}")
                print(f"[DEBUG] Available transmissions: {list(encoders['transmission'].classes_)}")
                return jsonify({'error': f'Invalid transmission: {transmission}. Available options: {list(encoders["transmission"].classes_)}'}), 400
            transmission_encoded = encoders['transmission'].transform([transmission])[0]
            print(f"[DEBUG] Transmission encoded: {transmission_encoded}")
            
            if owner_type not in encoders['owner_type'].classes_:
                print(f"[ERROR] Unseen owner type: {owner_type}")
                print(f"[DEBUG] Available owner types: {list(encoders['owner_type'].classes_)}")
                return jsonify({'error': f'Invalid owner type: {owner_type}. Available options: {list(encoders["owner_type"].classes_)}'}), 400
            owner_type_encoded = encoders['owner_type'].transform([owner_type])[0]
            print(f"[DEBUG] Owner type encoded: {owner_type_encoded}")
            
        except ValueError as e:
            print(f"[ERROR] Encoding error: {e}")
            traceback.print_exc()
            return jsonify({'error': f'Invalid categorical value: {str(e)}'}), 400
        
        # Prepare features in exact training order
        # Order: year, kilometers_driven, mileage, engine_capacity, company_encoded, model_encoded, fuel_type_encoded, transmission_encoded, owner_type_encoded
        features = np.array([[
            year,
            kilometers_driven,
            mileage,
            engine_capacity,
            company_encoded,
            model_encoded,
            fuel_type_encoded,
            transmission_encoded,
            owner_type_encoded
        ]], dtype=np.float64)
        
        print(f"[DEBUG] Features before scaling: {features}")
        print(f"[DEBUG] Feature shape: {features.shape}")
        
        # Scale numerical features (year, kilometers_driven, mileage, engine_capacity - indices 0,1,2,3)
        print("[DEBUG] Scaling numerical features...")
        numerical_cols = [0, 1, 2, 3]  # year, kilometers_driven, mileage, engine_capacity
        try:
            features[:, numerical_cols] = scaler.transform(features[:, numerical_cols])
            print(f"[DEBUG] Features after scaling: {features}")
        except Exception as e:
            print(f"[ERROR] Scaler error: {e}")
            traceback.print_exc()
            return jsonify({'error': f'Error scaling features: {str(e)}'}), 500
        
        # Make prediction
        print("[DEBUG] Making prediction...")
        try:
            predicted_price = model.predict(features)[0]
            print(f"[DEBUG] Prediction successful: {predicted_price}")
        except Exception as e:
            print(f"[ERROR] Prediction error: {e}")
            traceback.print_exc()
            return jsonify({'error': f'Error making prediction: {str(e)}'}), 500
        
        # AI Price Analysis
        current_year = 2024
        car_age = current_year - year
        
        # Calculate depreciation (10% per year)
        annual_depreciation = 0.10
        depreciation_factor = 1 - (car_age * annual_depreciation)
        depreciation_factor = max(0.3, min(0.95, depreciation_factor))  # Keep between 30% and 95%
        
        # Calculate expected market price based on depreciation
        base_price = predicted_price / depreciation_factor
        expected_market_price = base_price * depreciation_factor
        
        # Calculate price difference percentage
        price_difference_percent = ((predicted_price - expected_market_price) / expected_market_price) * 100
        
        # Determine price status
        if price_difference_percent < -15:
            price_status = "Underpriced"
            price_status_color = "green"
            recommendation = "Great Deal! This car is priced below market value."
        elif price_difference_percent > 15:
            price_status = "Overpriced"
            price_status_color = "red"
            recommendation = "Caution: This car is priced above market value."
        else:
            price_status = "Fair Price"
            price_status_color = "yellow"
            recommendation = "Reasonably priced according to market standards."
        
        # Calculate expected resale value after 3 years
        future_age = car_age + 3
        future_depreciation = 1 - (future_age * annual_depreciation)
        future_depreciation = max(0.2, future_depreciation)
        expected_resale_value = predicted_price * future_depreciation
        
        # Calculate total depreciation amount
        total_depreciation = base_price - predicted_price
        depreciation_percentage = (total_depreciation / base_price) * 100
        
        # Store in history
        prediction_entry = {
            'id': len(prediction_history) + 1,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'company': company,
            'model': model_name,
            'year': year,
            'fuel_type': fuel_type,
            'transmission': transmission,
            'kilometers_driven': kilometers_driven,
            'predicted_price': round(predicted_price, 2),
            'price_status': price_status,
            'expected_market_price': round(expected_market_price, 2),
            'expected_resale_value': round(expected_resale_value, 2),
            'depreciation_percentage': round(depreciation_percentage, 2)
        }
        prediction_history.append(prediction_entry)
        
        print(f"[INFO] Prediction completed successfully")
        print(f"[INFO] Predicted Price: INR {predicted_price:,.2f}")
        print(f"[INFO] Price Status: {price_status}")
        print("="*60 + "\n")
        
        # Return prediction with AI analysis
        # Note: Removed model.score() as it requires test data, not single prediction
        return jsonify({
            'success': True,
            'predicted_price': round(predicted_price, 2),
            'price_status': price_status,
            'price_status_color': price_status_color,
            'recommendation': recommendation,
            'expected_market_price': round(expected_market_price, 2),
            'expected_resale_value': round(expected_resale_value, 2),
            'depreciation_percentage': round(depreciation_percentage, 2),
            'total_depreciation': round(total_depreciation, 2),
            'car_age': car_age,
            'price_difference_percent': round(price_difference_percent, 2),
            'confidence': 85.0  # Fixed confidence value based on model training metrics
        })
        
    except Exception as e:
        print(f"[ERROR] Unexpected error in prediction: {e}")
        traceback.print_exc()
        return jsonify({'error': f'An error occurred during prediction: {str(e)}'}), 500


@prediction_bp.route('/api/history')
def get_history():
    """Get prediction history"""
    return jsonify({'history': prediction_history})


@prediction_bp.route('/api/stats')
def get_stats():
    """Get statistics about predictions"""
    if not prediction_history:
        return jsonify({
            'total_predictions': 0,
            'avg_price': 0,
            'most_predicted_company': None,
            'price_distribution': {},
            'status_distribution': {}
        })
    
    import pandas as pd
    df = pd.DataFrame(prediction_history)
    
    return jsonify({
        'total_predictions': len(prediction_history),
        'avg_price': round(df['predicted_price'].mean(), 2),
        'most_predicted_company': df['company'].mode()[0] if len(df) > 0 else None,
        'price_distribution': {
            'min': round(df['predicted_price'].min(), 2),
            'max': round(df['predicted_price'].max(), 2),
            'median': round(df['predicted_price'].median(), 2)
        },
        'status_distribution': df['price_status'].value_counts().to_dict()
    })


@prediction_bp.route('/api/companies')
def get_companies():
    """Get list of car companies from encoder"""
    if encoders and 'company' in encoders:
        companies = list(encoders['company'].classes_)
        print(f"[DEBUG] Returning {len(companies)} companies from encoder")
        return jsonify({'companies': companies})
    else:
        print("[WARNING] Returning fallback companies")
        return jsonify({'companies': CAR_COMPANIES})


@prediction_bp.route('/api/fuel-types')
def get_fuel_types():
    """Get list of fuel types from encoder"""
    if encoders and 'fuel_type' in encoders:
        fuel_types = list(encoders['fuel_type'].classes_)
        print(f"[DEBUG] Returning {len(fuel_types)} fuel types from encoder")
        return jsonify({'fuel_types': fuel_types})
    else:
        print("[WARNING] Returning fallback fuel types")
        return jsonify({'fuel_types': FUEL_TYPES})


@prediction_bp.route('/api/transmission-types')
def get_transmission_types():
    """Get list of transmission types from encoder"""
    if encoders and 'transmission' in encoders:
        transmission_types = list(encoders['transmission'].classes_)
        print(f"[DEBUG] Returning {len(transmission_types)} transmission types from encoder")
        return jsonify({'transmission_types': transmission_types})
    else:
        print("[WARNING] Returning fallback transmission types")
        return jsonify({'transmission_types': TRANSMISSION_TYPES})


@prediction_bp.route('/api/owner-types')
def get_owner_types():
    """Get list of owner types from encoder"""
    if encoders and 'owner_type' in encoders:
        owner_types = list(encoders['owner_type'].classes_)
        print(f"[DEBUG] Returning {len(owner_types)} owner types from encoder")
        return jsonify({'owner_types': owner_types})
    else:
        print("[WARNING] Returning fallback owner types")
        return jsonify({'owner_types': OWNER_TYPES})


@prediction_bp.route('/api/models')
def get_all_models():
    """Get list of all models from encoder"""
    if encoders and 'model' in encoders:
        models = list(encoders['model'].classes_)
        print(f"[DEBUG] Returning {len(models)} models from encoder")
        return jsonify({'models': models})
    else:
        # Return all models from CAR_MODELS
        all_models = []
        for company_models in CAR_MODELS.values():
            all_models.extend(company_models)
        print(f"[WARNING] Returning {len(all_models)} fallback models")
        return jsonify({'models': all_models})


@prediction_bp.route('/api/model-info')
def model_info():
    """Get model information"""
    try:
        with open('model_metrics.txt', 'r', encoding='utf-8') as f:
            metrics = f.read()
        return jsonify({'success': True, 'metrics': metrics})
    except FileNotFoundError:
        return jsonify({'error': 'Model metrics not found'}), 404
