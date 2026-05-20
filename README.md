# 🚗 AI Car Price Predictor - Premium Edition

A professional, premium AI-powered web application for predicting used car prices using Machine Learning and Flask. Built with a futuristic AI dashboard style featuring advanced glassmorphism design, dark/light mode, interactive visualizations, and comprehensive analytics.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![Machine Learning](https://img.shields.io/badge/ML-Random%20Forest-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Premium Features

### Frontend - Modern AI Dashboard
- **Futuristic UI**: Premium AI dashboard style with glassmorphism cards and animated gradients
- **Dark/Light Mode**: Toggle between themes with smooth transitions and persistent storage
- **Fully Responsive**: Optimized for desktop, tablet, and mobile devices
- **Advanced Animations**: Smooth hover effects, loading spinners, scroll animations, and floating cards
- **Toast Notifications**: Real-time feedback with success, error, warning, and info notifications
- **Image Upload**: Drag-and-drop car image upload with preview functionality
- **Interactive Forms**: Dynamic dropdowns with real-time validation and error handling
- **Animated Counters**: Smooth number animations for statistics and prices
- **PDF Export**: Download professional prediction reports with one click

### Backend - Modular Architecture
- **Flask Blueprints**: Organized modular structure with separate route blueprints
- **REST API**: Clean and efficient API endpoints for all features
- **ML Model Integration**: Random Forest Regressor for accurate predictions
- **AI Price Analysis**: Fair price, depreciation, resale value, and deal status
- **Error Handling**: Comprehensive validation and error messages
- **Prediction History**: Track predictions with timestamps and detailed storage
- **Image Upload API**: Secure file upload with validation and storage

### Machine Learning
- **Random Forest Regressor**: High-accuracy prediction model (92% R² score)
- **Data Preprocessing**: Cleaning, encoding, scaling, and outlier removal
- **Model Evaluation**: MAE, RMSE, R² Score metrics with detailed reports
- **Feature Importance**: Visual understanding of price-influencing factors
- **AI Deal Analysis**: "Underpriced", "Fair Price", or "Overpriced" insights
- **Depreciation Calculation**: Automatic depreciation and resale value estimation

### Interactive Dashboard
- **Statistics Cards**: Real-time animated counters for key metrics
- **Price Trends Chart**: Interactive line chart showing prediction vs market prices
- **Status Distribution**: Doughnut chart showing deal status distribution
- **Feature Importance**: Horizontal bar chart of feature impact
- **History Table**: Detailed prediction history with timestamps and status badges
- **Comparison Analysis**: Side-by-side car comparison with detailed metrics

### Extra Features
- **Car Comparison**: Compare prices of two different cars with detailed analysis
- **Prediction History**: View, analyze, and manage past predictions
- **Statistics Dashboard**: Track average prices, popular brands, and deal counts
- **Market Analysis**: Estimated market price comparison and recommendations
- **Mobile Menu**: Responsive navigation with hamburger menu for mobile devices

## 📁 Project Structure

```
car-price-predictor/
│
├── app.py                      # Main Flask application with blueprint registration
├── train_model.py              # ML model training script with UTF-8 encoding fix
├── model.pkl                   # Trained ML model (generated after training)
├── encoders.pkl                # Label encoders (generated after training)
├── scaler.pkl                  # Feature scaler (generated after training)
├── model_metrics.txt           # Model performance metrics (generated after training)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── routes/                     # Modular Flask blueprints
│   ├── __init__.py            # Blueprint initialization
│   ├── prediction_routes.py   # Prediction and AI analysis endpoints
│   ├── comparison_routes.py    # Car comparison endpoints
│   └── api_routes.py          # General API endpoints (image upload, health)
│
├── dataset/
│   └── car_data.csv           # Sample car dataset for training
│
├── static/
│   ├── style.css              # Premium CSS with glassmorphism and animations
│   ├── script.js              # Interactive JavaScript with toast notifications
│   └── uploads/               # Uploaded car images (auto-created)
│
└── templates/
    └── index.html             # Premium HTML template with all sections
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Basic understanding of command line

### Installation Steps

1. **Clone or download the project**
   ```bash
   cd "car price prediction"
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the ML model**
   ```bash
   python train_model.py
   ```
   
   This will:
   - Load and clean the car dataset
   - Train the Random Forest model
   - Evaluate model performance
   - Save the model as `model.pkl`
   - Generate visualizations in the `visualizations/` folder

5. **Run the Flask application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   ```
   http://127.0.0.1:5000
   ```

## 📊 Model Performance

The trained model achieves the following metrics on the test set:

- **Mean Absolute Error (MAE)**: ~₹50,000
- **Root Mean Squared Error (RMSE)**: ~₹75,000
- **R² Score**: ~0.92 (92% accuracy)

## 🎯 Usage Guide

### Predicting Car Price

1. Navigate to the "Predict" section
2. Optionally upload a car image using the drag-and-drop upload area
3. Fill in the car details:
   - Car Company (e.g., Maruti, Hyundai, Toyota)
   - Car Model (auto-populated based on company)
   - Year of manufacture
   - Fuel type (Petrol, Diesel, CNG, Electric, Hybrid)
   - Transmission (Manual, Automatic)
   - Kilometers driven
   - Owner type (First, Second, Third)
   - Mileage (km/l)
   - Engine capacity (CC)
4. Click "Predict Price"
5. View the estimated price with AI analysis:
   - Predicted price with animated counter
   - Fair market price
   - Resale value
   - Depreciation percentage
   - Deal status (Underpriced, Fair Price, Overpriced)
   - AI recommendation
6. Download the prediction as a PDF report

### Comparing Cars

1. Go to the "Compare" section
2. Enter details for two different cars
3. Click "Compare Prices"
4. See detailed comparison:
   - Individual car prices
   - Price difference
   - Better deal recommendation
   - Value per year analysis
   - Savings calculation

### Viewing History & Dashboard

1. Visit the "History" section
2. View prediction statistics with animated counters
3. Browse recent predictions in the history list
4. Analyze detailed history table with timestamps
5. View interactive charts:
   - Price trends line chart
   - Status distribution doughnut chart
   - Feature importance bar chart

## 🔧 API Endpoints

### Prediction & AI Analysis
- `POST /api/predict` - Get car price prediction with AI analysis (fair price, depreciation, resale value)
- `POST /api/compare` - Compare two cars with detailed value analysis

### Data & Dropdowns
- `GET /api/companies` - Get list of car companies
- `GET /api/car-models/<company>` - Get models for a specific company
- `GET /api/fuel-types` - Get fuel types
- `GET /api/transmission-types` - Get transmission types
- `GET /api/owner-types` - Get owner types

### History & Statistics
- `GET /api/history` - Get prediction history with timestamps
- `GET /api/stats` - Get prediction statistics and status distribution
- `GET /api/model-info` - Get model performance metrics

### General API
- `POST /api/upload-image` - Upload car image with validation
- `GET /api/health` - Health check endpoint
- `GET /api/feature-metadata` - Get feature information

## 🎨 Customization

### Adding More Car Data

Edit `dataset/car_data.csv` to add more car entries. The CSV should have these columns:
- company, model, year, fuel_type, transmission, kilometers_driven, owner_type, mileage, engine_capacity, price

After adding data, retrain the model:
```bash
python train_model.py
```

### Changing the Model

Edit `train_model.py` to experiment with different models:
- Change `RandomForestRegressor` to other regressors
- Adjust hyperparameters (n_estimators, max_depth, etc.)
- Try different feature engineering techniques

### Customizing the UI

- **Colors**: Edit CSS variables in `static/style.css` (primary-color, secondary-color, etc.)
- **Layout**: Modify HTML structure in `templates/index.html`
- **Animations**: Adjust CSS animations in `static/style.css`
- **Charts**: Modify Chart.js configurations in `static/script.js`
- **Theme**: Toggle dark/light mode in the UI or edit CSS variables directly

## 🚀 Deployment

### Deploy on Render

1. Create a `Procfile` (if not exists):
   ```
   web: python app.py
   ```

2. Push your code to GitHub

3. Connect your repository to Render

4. Render will automatically detect Python and deploy

### Deploy on Railway

1. Push code to GitHub

2. Create a new project on Railway

3. Select your repository

4. Railway will deploy automatically

### Environment Variables

For production, consider setting:
- `FLASK_ENV=production`
- `FLASK_DEBUG=0`

## 📈 Model Training Details

### Data Preprocessing
- **Missing Values**: Removed rows with missing data
- **Outliers**: Removed using IQR method
- **Categorical Encoding**: Label encoding for company, model, fuel type, transmission, owner type
- **Feature Scaling**: StandardScaler for numerical features
- **UTF-8 Encoding**: Fixed encoding issues for Windows compatibility

### Features Used
1. Year of manufacture
2. Kilometers driven
3. Mileage (km/l)
4. Engine capacity (CC)
5. Car company (encoded)
6. Car model (encoded)
7. Fuel type (encoded)
8. Transmission type (encoded)
9. Owner type (encoded)

### Model Parameters
- **Algorithm**: Random Forest Regressor
- **n_estimators**: 100
- **max_depth**: 10
- **min_samples_split**: 5
- **min_samples_leaf**: 2
- **random_state**: 42

### AI Price Analysis Logic
- **Fair Price**: Calculated based on market averages and model prediction
- **Depreciation**: Estimated based on car age and mileage
- **Resale Value**: Projected future value considering depreciation trends
- **Deal Status**: Determined by comparing predicted price to market price
  - Underpriced: Predicted price > 10% below market
  - Fair Price: Within ±10% of market price
  - Overpriced: Predicted price > 10% above market

## 🐛 Troubleshooting

### Model Not Found Error
If you see "Model files not found", run:
```bash
python train_model.py
```

### Port Already in Use
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead of 5000
```

### Import Errors
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Dropdowns Not Populating
Check browser console for errors. Ensure Flask server is running and API endpoints are accessible.

### Image Upload Not Working
- Ensure the `static/uploads/` folder exists
- Check file size (max 5MB)
- Verify file type (JPEG, PNG, GIF, WebP only)
- Check browser console for errors

### Charts Not Displaying
- Ensure Chart.js is loaded properly
- Check browser console for errors
- Verify canvas elements exist in HTML

### PDF Generation Fails
- Ensure html2pdf.js library is loaded
- Check browser console for errors
- Try using a different browser (Chrome/Firefox recommended)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add more car data
- Improve the ML model
- Enhance the UI
- Fix bugs
- Add new features

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Built with ❤️ using Python, Flask, and Machine Learning.

## 🙏 Acknowledgments

- Flask web framework
- Scikit-learn for ML algorithms
- Chart.js for interactive visualizations
- html2pdf.js for PDF generation
- Font Awesome for icons
- Google Fonts for typography

## 📞 Support

For issues or questions, please open an issue on the repository or contact the maintainer.

---

**Note**: This is a premium demonstration project showcasing modern web development practices with AI/ML integration. For production use, consider:
- Adding user authentication and authorization
- Implementing a real database (PostgreSQL/MongoDB)
- Adding more comprehensive car data
- Implementing API rate limiting
- Adding comprehensive logging and monitoring
- Using a production WSGI server (Gunicorn/uWSGI)
- Setting up CI/CD pipelines
- Adding automated testing
- Implementing caching for better performance
