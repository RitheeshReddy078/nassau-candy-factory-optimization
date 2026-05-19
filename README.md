# Nassau Candy — Factory Reallocation & Shipping Optimization System

A decision intelligence platform that elevates Nassau Candy Distributor 
from static logistics to data-driven factory assignment decisions.

## Project Overview
This system predicts shipping lead times, simulates factory reassignment 
scenarios, and recommends optimal factory-product assignments using 
Machine Learning.

## Features
- Exploratory Data Analysis (EDA) with interactive charts
- Machine Learning models (Linear Regression, Random Forest, Gradient Boosting)
- Factory Reassignment Simulation Engine
- What-If Scenario Analysis
- Recommendations Dashboard
- Risk & Impact Panel
- SQLite Database Backend
- Professional Streamlit Web Interface

## Tech Stack
- Python
- Streamlit
- SQLite
- Pandas & NumPy
- Scikit-learn
- Matplotlib & Seaborn

## Project Structure
nassau_candy_project/
├── data/
│   ├── Nassau_Candy_Distributor.csv
│   ├── nassau_candy.db
│   └── best_model.pkl
├── 00_database_setup.py
├── 01_data_preparation.py
├── 02_eda.py
├── 03_ml_models.py
├── 04_simulation.py
├── 05_streamlit_app.py
├── requirements.txt
└── README.md

## How to Run
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run database setup: `python 00_database_setup.py`
4. Launch dashboard: `streamlit run 05_streamlit_app.py`

## Dataset
10,194 orders across 15 products and 5 factories.

## Deliverables
- Live Streamlit Dashboard
- Research Paper
- Executive Summary