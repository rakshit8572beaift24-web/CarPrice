"""
Comparison Routes Blueprint
Handles car comparison endpoints
"""

from flask import Blueprint, jsonify, request
import numpy as np
import pickle
import traceback

comparison_bp = Blueprint('comparison', __name__)

# Load model and preprocessing objects
def load_model():
    """Load the trained model and preprocessing objects"""
    try:
        print("[DEBUG] Loading model files for comparison...")
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        print("[DEBUG] Model loaded successfully for comparison")
        
        with open('encoders.pkl', 'rb') as f:
            encoders = pickle.load(f)
        print("[DEBUG] Encoders loaded successfully for comparison")
        
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        print("[DEBUG] Scaler loaded successfully for comparison")
        
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


def predict_single_car(car_data):
    """Helper function to predict price for a single car with robust error handling"""
    try:
        print(f"[DEBUG] Predicting car: {car_data.get('company')} {car_data.get('model')}")
        
        # Extract features with safe conversion
        try:
            company = car_data.get('company', '').strip()
            model_name = car_data.get('model', '').strip()
            year = int(car_data.get('year', 0))
            fuel_type = car_data.get('fuel_type', '').strip()
            transmission = car_data.get('transmission', '').strip()
            kilometers_driven = float(car_data.get('kilometers_driven', 0))
            owner_type = car_data.get('owner_type', '').strip()
            mileage = float(car_data.get('mileage', 0))
            engine_capacity = float(car_data.get('engine_capacity', 0))
        except (ValueError, TypeError) as e:
            print(f"[ERROR] Type conversion error: {e}")
            raise ValueError(f'Invalid data format: {str(e)}')
        
        # Validate input
        if not all([company, model_name, year, fuel_type, transmission, 
                   kilometers_driven, owner_type, mileage, engine_capacity]):
            raise ValueError('Missing required fields')
        
        # Validate ranges
        if year < 2000 or year > 2025:
            raise ValueError(f'Year must be between 2000 and 2025. Got: {year}')
        if year <= 0:
            raise ValueError(f'Year cannot be negative. Got: {year}')
        if kilometers_driven < 0:
            raise ValueError(f'Kilometers driven cannot be negative. Got: {kilometers_driven}')
        if kilometers_driven > 500000:
            raise ValueError(f'Kilometers driven must be less than 500,000. Got: {kilometers_driven}')
        if mileage < 0:
            raise ValueError(f'Mileage cannot be negative. Got: {mileage}')
        if mileage > 50:
            raise ValueError(f'Mileage must be less than 50 km/l. Got: {mileage}')
        if engine_capacity <= 0:
            raise ValueError(f'Engine capacity must be positive. Got: {engine_capacity}')
        if engine_capacity < 500 or engine_capacity > 6000:
            raise ValueError(f'Engine capacity must be between 500 and 6000 CC. Got: {engine_capacity}')
        
        # Encode categorical features with unseen label handling
        try:
            if company not in encoders['company'].classes_:
                raise ValueError(f'Invalid company: {company}. Available: {list(encoders["company"].classes_)}')
            company_encoded = encoders['company'].transform([company])[0]
            
            if model_name not in encoders['model'].classes_:
                raise ValueError(f'Invalid model: {model_name}. Available: {list(encoders["model"].classes_)}')
            model_encoded = encoders['model'].transform([model_name])[0]
            
            if fuel_type not in encoders['fuel_type'].classes_:
                raise ValueError(f'Invalid fuel type: {fuel_type}. Available: {list(encoders["fuel_type"].classes_)}')
            fuel_type_encoded = encoders['fuel_type'].transform([fuel_type])[0]
            
            if transmission not in encoders['transmission'].classes_:
                raise ValueError(f'Invalid transmission: {transmission}. Available: {list(encoders["transmission"].classes_)}')
            transmission_encoded = encoders['transmission'].transform([transmission])[0]
            
            if owner_type not in encoders['owner_type'].classes_:
                raise ValueError(f'Invalid owner type: {owner_type}. Available: {list(encoders["owner_type"].classes_)}')
            owner_type_encoded = encoders['owner_type'].transform([owner_type])[0]
            
        except ValueError as e:
            print(f"[ERROR] Encoding error: {e}")
            raise
        
        # Prepare features in exact training order
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
        
        # Scale numerical features
        numerical_cols = [0, 1, 2, 3]
        try:
            features[:, numerical_cols] = scaler.transform(features[:, numerical_cols])
        except Exception as e:
            print(f"[ERROR] Scaler error: {e}")
            raise ValueError(f'Error scaling features: {str(e)}')
        
        # Make prediction
        try:
            predicted_price = model.predict(features)[0]
            print(f"[DEBUG] Prediction successful: {predicted_price}")
            return round(predicted_price, 2)
        except Exception as e:
            print(f"[ERROR] Prediction error: {e}")
            raise ValueError(f'Error making prediction: {str(e)}')
        
    except Exception as e:
        print(f"[ERROR] Error predicting single car: {e}")
        traceback.print_exc()
        raise


@comparison_bp.route('/api/compare', methods=['POST'])
def compare():
    """
    API endpoint for comparing two cars
    Provides detailed comparison analysis
    """
    print("\n" + "="*60)
    print("[INFO] New comparison request received")
    print("="*60)
    
    if model is None:
        print("[ERROR] Model not loaded")
        return jsonify({'error': 'Model not loaded. Please train the model first.'}), 500
    
    try:
        data = request.get_json()
        print(f"[DEBUG] Received comparison data: {data}")
        
        if not data:
            print("[ERROR] No data received in request")
            return jsonify({'error': 'No data received'}), 400
        
        car1 = data.get('car1')
        car2 = data.get('car2')
        
        if not car1 or not car2:
            print("[ERROR] Missing car data")
            return jsonify({'error': 'Both car1 and car2 data are required'}), 400
        
        print(f"[DEBUG] Car 1: {car1.get('company')} {car1.get('model')}")
        print(f"[DEBUG] Car 2: {car2.get('company')} {car2.get('model')}")
        
        # Predict price for car 1
        print("[DEBUG] Predicting Car 1...")
        price1 = predict_single_car(car1)
        print(f"[DEBUG] Car 1 price: {price1}")
        
        # Predict price for car 2
        print("[DEBUG] Predicting Car 2...")
        price2 = predict_single_car(car2)
        print(f"[DEBUG] Car 2 price: {price2}")
        
        # Calculate difference
        difference = abs(price1 - price2)
        difference_percent = (difference / max(price1, price2)) * 100 if max(price1, price2) > 0 else 0
        
        # Determine better value
        if price1 < price2:
            better_deal = "Car 1"
            better_deal_car = car1
            other_price = price2
        else:
            better_deal = "Car 2"
            better_deal_car = car2
            other_price = price1
        
        # Calculate value for money (price per year)
        current_year = 2024
        try:
            age1 = current_year - int(car1.get('year', 2024))
            age2 = current_year - int(car2.get('year', 2024))
        except (ValueError, TypeError) as e:
            print(f"[ERROR] Error calculating age: {e}")
            age1 = 1
            age2 = 1
        
        value_per_year1 = price1 / max(1, age1)
        value_per_year2 = price2 / max(1, age2)
        
        # Calculate depreciation rate
        depreciation_rate1 = (price1 / (price1 * 1.5)) * 100 if price1 > 0 else 0
        depreciation_rate2 = (price2 / (price2 * 1.5)) * 100 if price2 > 0 else 0
        
        # Comparison analysis
        comparison_analysis = {
            'price_difference': difference,
            'price_difference_percent': round(difference_percent, 2),
            'better_deal': better_deal,
            'better_deal_price': min(price1, price2),
            'other_car_price': max(price1, price2),
            'savings': difference,
            'value_per_year': {
                'car1': round(value_per_year1, 2),
                'car2': round(value_per_year2, 2)
            },
            'depreciation_rate': {
                'car1': round(depreciation_rate1, 2),
                'car2': round(depreciation_rate2, 2)
            },
            'recommendation': f"{better_deal} offers better value with {round(difference_percent, 2)}% lower price."
        }
        
        print(f"[INFO] Comparison completed successfully")
        print(f"[INFO] Price difference: INR {difference:,.2f}")
        print(f"[INFO] Better deal: {better_deal}")
        print("="*60 + "\n")
        
        return jsonify({
            'success': True,
            'car1_price': price1,
            'car2_price': price2,
            'comparison': comparison_analysis
        })
        
    except ValueError as e:
        print(f"[ERROR] Validation error in comparison: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"[ERROR] Unexpected error in comparison: {e}")
        traceback.print_exc()
        return jsonify({'error': f'An error occurred during comparison: {str(e)}'}), 500
