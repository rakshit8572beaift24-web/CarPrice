"""
Car Price Prediction Model Training Script
This script trains a Random Forest Regressor model to predict car prices
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
import os
import warnings
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

warnings.filterwarnings('ignore')

# Set style for visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


def load_data(filepath):
    """
    Load the car dataset from CSV file
    """
    print("Loading dataset...")
    df = pd.read_csv(filepath)
    print(f"Dataset loaded with shape: {df.shape}")
    return df


def explore_data(df):
    """
    Perform exploratory data analysis
    """
    print("\n" + "="*50)
    print("EXPLORATORY DATA ANALYSIS")
    print("="*50)
    
    print("\nDataset Info:")
    print(df.info())
    
    print("\nFirst 5 rows:")
    print(df.head())
    
    print("\nStatistical Summary:")
    print(df.describe())
    
    print("\nMissing Values:")
    print(df.isnull().sum())
    
    print("\nData Types:")
    print(df.dtypes)
    
    # Create visualizations directory
    if not os.path.exists('visualizations'):
        os.makedirs('visualizations')
    
    # Price distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df['price'], bins=30, kde=True)
    plt.title('Distribution of Car Prices')
    plt.xlabel('Price (INR)')
    plt.ylabel('Frequency')
    plt.savefig('visualizations/price_distribution.png')
    plt.close()
    
    # Price by year
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='year', y='price', data=df)
    plt.title('Car Price by Year')
    plt.xticks(rotation=45)
    plt.savefig('visualizations/price_by_year.png')
    plt.close()
    
    # Price by fuel type
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='fuel_type', y='price', data=df)
    plt.title('Car Price by Fuel Type')
    plt.savefig('visualizations/price_by_fuel.png')
    plt.close()
    
    # Price by transmission
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='transmission', y='price', data=df)
    plt.title('Car Price by Transmission')
    plt.savefig('visualizations/price_by_transmission.png')
    plt.close()
    
    # Correlation heatmap
    plt.figure(figsize=(12, 8))
    numeric_df = df.select_dtypes(include=[np.number])
    correlation_matrix = numeric_df.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Heatmap')
    plt.savefig('visualizations/correlation_heatmap.png')
    plt.close()
    
    print("\nVisualizations saved in 'visualizations' directory")


def clean_data(df):
    """
    Clean and preprocess the data
    """
    print("\n" + "="*50)
    print("DATA CLEANING")
    print("="*50)
    
    # Remove duplicates
    initial_rows = len(df)
    df = df.drop_duplicates()
    print(f"Removed {initial_rows - len(df)} duplicate rows")
    
    # Handle missing values (if any)
    df = df.dropna()
    print(f"Removed rows with missing values. Remaining rows: {len(df)}")
    
    # Convert numeric columns to proper types
    numeric_columns = ['year', 'kilometers_driven', 'mileage', 'engine_capacity', 'price']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Remove outliers using IQR method for price
    Q1 = df['price'].quantile(0.25)
    Q3 = df['price'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    df = df[(df['price'] >= lower_bound) & (df['price'] <= upper_bound)]
    print(f"Removed outliers. Remaining rows: {len(df)}")
    
    return df


def encode_categorical_features(df):
    """
    Encode categorical features using Label Encoding
    """
    print("\n" + "="*50)
    print("FEATURE ENCODING")
    print("="*50)
    
    # Create label encoders for categorical columns
    categorical_columns = ['company', 'model', 'fuel_type', 'transmission', 'owner_type']
    
    encoders = {}
    
    for col in categorical_columns:
        le = LabelEncoder()
        df[col + '_encoded'] = le.fit_transform(df[col])
        encoders[col] = le
        print(f"Encoded {col}: {dict(zip(le.classes_, le.transform(le.classes_)))}")
    
    # Save encoders for later use
    with open('encoders.pkl', 'wb') as f:
        pickle.dump(encoders, f)
    
    print("\nEncoders saved as 'encoders.pkl'")
    
    return df, encoders


def prepare_features(df):
    """
    Prepare features for model training
    """
    print("\n" + "="*50)
    print("FEATURE PREPARATION")
    print("="*50)
    
    # Select features for training
    feature_columns = [
        'year',
        'kilometers_driven',
        'mileage',
        'engine_capacity',
        'company_encoded',
        'model_encoded',
        'fuel_type_encoded',
        'transmission_encoded',
        'owner_type_encoded'
    ]
    
    X = df[feature_columns]
    y = df['price']
    
    print(f"Features shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    
    # Scale numerical features
    scaler = StandardScaler()
    numerical_cols = ['year', 'kilometers_driven', 'mileage', 'engine_capacity']
    X[numerical_cols] = scaler.fit_transform(X[numerical_cols])
    
    # Save scaler for later use
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    print("Scaler saved as 'scaler.pkl'")
    
    return X, y, feature_columns


def train_model(X, y):
    """
    Train Random Forest Regressor model
    """
    print("\n" + "="*50)
    print("MODEL TRAINING")
    print("="*50)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")
    
    # Initialize and train the model
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2
    )
    
    print("\nTraining Random Forest Regressor...")
    model.fit(X_train, y_train)
    print("Model training completed!")
    
    return model, X_train, X_test, y_train, y_test


def evaluate_model(model, X_test, y_test):
    """
    Evaluate the model performance
    """
    print("\n" + "="*50)
    print("MODEL EVALUATION")
    print("="*50)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nMean Absolute Error (MAE): INR {mae:,.2f}")
    print(f"Root Mean Squared Error (RMSE): INR {rmse:,.2f}")
    print(f"R² Score: {r2:.4f} ({r2*100:.2f}%)")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'Feature': X_test.columns,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print("\nFeature Importance:")
    print(feature_importance)
    
    # Plot feature importance
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Importance', y='Feature', data=feature_importance)
    plt.title('Feature Importance')
    plt.xlabel('Importance')
    plt.tight_layout()
    plt.savefig('visualizations/feature_importance.png')
    plt.close()
    
    # Actual vs Predicted plot
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual Price')
    plt.ylabel('Predicted Price')
    plt.title('Actual vs Predicted Prices')
    plt.savefig('visualizations/actual_vs_predicted.png')
    plt.close()
    
    # Residual plot
    residuals = y_test - y_pred
    plt.figure(figsize=(10, 6))
    plt.scatter(y_pred, residuals, alpha=0.5)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel('Predicted Price')
    plt.ylabel('Residuals')
    plt.title('Residual Plot')
    plt.savefig('visualizations/residual_plot.png')
    plt.close()
    
    return {
        'mae': mae,
        'rmse': rmse,
        'r2': r2,
        'feature_importance': feature_importance
    }


def save_model(model, metrics):
    """
    Save the trained model and metrics
    """
    print("\n" + "="*50)
    print("SAVING MODEL")
    print("="*50)
    
    # Save the model
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print("Model saved as 'model.pkl'")
    
    # Save metrics
    with open('model_metrics.txt', 'w', encoding='utf-8') as f:
        f.write("Car Price Prediction Model Metrics\n")
        f.write("="*50 + "\n\n")
        f.write(f"Mean Absolute Error (MAE): INR {metrics['mae']:,.2f}\n")
        f.write(f"Root Mean Squared Error (RMSE): INR {metrics['rmse']:,.2f}\n")
        f.write(f"R² Score: {metrics['r2']:.4f} ({metrics['r2']*100:.2f}%)\n\n")
        f.write("Feature Importance:\n")
        f.write(str(metrics['feature_importance']))
    
    print("Metrics saved as 'model_metrics.txt'")


def main():
    """
    Main function to run the entire training pipeline
    """
    print("\n" + "="*50)
    print("CAR PRICE PREDICTION MODEL TRAINING")
    print("="*50)
    
    # Load data
    df = load_data('dataset/car_data.csv')
    
    # Explore data
    explore_data(df)
    
    # Clean data
    df = clean_data(df)
    
    # Encode categorical features
    df, encoders = encode_categorical_features(df)
    
    # Prepare features
    X, y, feature_columns = prepare_features(df)
    
    # Train model
    model, X_train, X_test, y_train, y_test = train_model(X, y)
    
    # Evaluate model
    metrics = evaluate_model(model, X_test, y_test)
    
    # Save model
    save_model(model, metrics)
    
    print("\n" + "="*50)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("="*50)
    print("\nFiles created:")
    print("- model.pkl (trained model)")
    print("- encoders.pkl (label encoders)")
    print("- scaler.pkl (feature scaler)")
    print("- model_metrics.txt (model performance)")
    print("- visualizations/ (data analysis plots)")


if __name__ == "__main__":
    main()
