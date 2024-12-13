# Energy Demand Forecasting Project

This repository provides a comprehensive solution for forecasting energy demand and prices using historical data on energy production, consumption, and weather conditions. The project combines Python-based machine learning models with a modern web interface powered by Next.js and TailwindCSS.

## Features
- **Data Processing**: Handles missing values, outliers, and performs feature engineering.
- **Model Development**: Utilizes RandomForest and XGBoost models with hyperparameter tuning.
- **Time Series Analysis**: Includes SARIMA for seasonal decomposition and forecasting.
- **Deployment**: Provides a FastAPI-based RESTful API for live predictions.
- **Web Application**: An intuitive and sleek user interface for interacting with prediction models.

## Project Structure
```
.
├── data
│   ├── raw               # Raw energy and weather datasets
│   ├── processed         # Processed datasets
├── models                # Saved models
├── scripts               # Backend Python scripts
│   ├── preprocess.py     # Data cleaning and feature engineering
│   ├── train.py          # Training and saving models
│   ├── test.py           # Testing trained models
│   ├── app.py            # FastAPI application
├── energy-prediction-app # Frontend Next.js application
│   ├── src/app           # Next.js pages and components
│   ├── public            # Static assets
│   ├── styles            # Global CSS and Tailwind configuration
├── encoders              # Saved encoders and scalers
├── README.md             # Project documentation
└── LICENSE               # License file
```

## Installation

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repository/energy-demand-forecasting.git
   cd energy-demand-forecasting
   ```

2. Set up a Python virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Prepare the dataset:
   - Place raw datasets in the `data/raw` directory.
   - Run `preprocess.py` to clean and process the data.

4. Train models:
   ```bash
   python scripts/train.py
   ```

5. Start the FastAPI backend:
   ```bash
   uvicorn scripts.app:app --reload
   ```

6. Access the API at `http://127.0.0.1:8000/docs`.

### Frontend Setup
1. Navigate to the `energy-prediction-app` directory:
   ```bash
   cd energy-prediction-app
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the Next.js development server:
   ```bash
   npm run dev
   ```

4. Access the web application at `http://localhost:3000`.

## Usage
### API Endpoints
- `GET /` - Home page of the API.
- `POST /predict` - Predicts energy demand using the provided input.

### Example Input
```json
{
    "generation_biomass": 200,
    "generation_fossil_brown_coal_lignite": 400,
    "generation_fossil_coal_derived_gas": 0,
    "generation_fossil_gas": 5000,
    "generation_fossil_hard_coal": 4800,
    "generation_fossil_oil": 150,
    "generation_geothermal": 800,
    "generation_hydro_pumped_storage_consumption": 1000,
    "generation_hydro_run_of_river_and_poundage": 1200,
    "generation_hydro_water_reservoir": 2500,
    "generation_solar": 300,
    "generation_wind_onshore": 6000,
    "forecast_solar_day_ahead": 200,
    "forecast_wind_onshore_day_ahead": 5500,
    "total_load_forecast": 26000,
    "hour": 15,
    "day_of_week": 2,
    "month": 12,
    "is_weekend": 0,
    "season": 3
}
```

### Example Response
```json
{
    "prediction": 26500.3
}
```

### Frontend
The web application provides:
1. **Home Page**: Introduction to the energy forecasting tool.
2. **Prediction Form**: Interactive form for submitting data to generate predictions.
3. **Results Display**: Displays the prediction result or errors in a user-friendly manner.

## Contributing
Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss your ideas.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
