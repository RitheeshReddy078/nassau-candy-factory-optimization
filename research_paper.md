# Factory Reallocation & Shipping Optimization Recommendation System
## Nassau Candy Distributor — Research Paper

**Author:** A. Ritheesh  
**Project Type:** Data Science & Decision Intelligence  
**Organization:** Nassau Candy Distributor  
**Date:** May 2026

---

## Abstract

Nassau Candy Distributor currently assigns products to factories using 
static rules and legacy processes, leading to suboptimal shipping distances, 
high lead times for certain regions, and margin erosion due to logistics 
inefficiencies. This research introduces a decision intelligence system that 
predicts shipping outcomes under different configurations, recommends which 
products should be reassigned to alternative factories, and balances shipping 
efficiency with profitability. The system combines exploratory data analysis, 
machine learning modeling, scenario simulation, and an interactive Streamlit 
dashboard to deliver actionable factory reallocation recommendations.

---

## 1. Introduction

### 1.1 Background
Nassau Candy Distributor operates a network of 5 factories across the 
United States, supplying 15 products across 4 major regions — Atlantic, 
Gulf, Interior, and Pacific. The current factory-product assignment follows 
static rules that were established historically and have not been 
systematically reviewed for efficiency.

### 1.2 Problem Statement
The existing system leads to:
- Suboptimal shipping distances between factories and customer regions
- High lead times for certain product-region combinations
- Margin erosion due to logistics inefficiencies
- No mechanism to simulate or quantify the impact of reassignment before execution

### 1.3 Objectives
1. Analyze existing shipping patterns using exploratory data analysis
2. Build machine learning models to predict shipping lead times
3. Simulate factory reassignment scenarios for all products
4. Generate data-driven factory reallocation recommendations
5. Deliver a live interactive dashboard for decision makers

---

## 2. Dataset Description

The dataset contains 10,194 order records with 18 fields covering the 
period January 2024 to December 2025.

| Field | Description |
|---|---|
| Row ID | Unique row identifier |
| Order ID | Unique order identifier |
| Order Date | Date of order placement |
| Ship Date | Date of shipment |
| Ship Mode | Shipping method used |
| Customer ID | Unique customer identifier |
| Country/Region | Customer country or region |
| City | Customer city |
| State/Province | Customer state or province |
| Postal Code | Customer postal code |
| Division | Product division (Chocolate, Sugar, Other) |
| Region | Customer region (Atlantic, Gulf, Interior, Pacific) |
| Product ID | Unique product identifier |
| Product Name | Full product name |
| Sales | Total sales value of order |
| Units | Total units in order |
| Gross Profit | Sales minus cost |
| Cost | Manufacturing cost |

### 2.1 Data Quality
- Zero null values across all 18 columns
- Lead time derived as Ship Date minus Order Date
- Numeric columns validated and cleaned before modeling

### 2.2 Key Statistics
- Total Orders: 10,194
- Total Products: 15
- Active Factories: 5
- Total Revenue: $141,784
- Total Gross Profit: $93,443
- Profit Margin: 65.9%

---

## 3. Exploratory Data Analysis

### 3.1 Division Analysis
Chocolate division dominates with 9,844 orders (96.6% of total), 
followed by Other division with 316 orders (3.1%), and Sugar division 
with only 30 orders (0.3%). This heavy concentration in Chocolate 
indicates high dependency on a single product category.

### 3.2 Shipping Mode Analysis
Standard Class is the most frequently used shipping mode with the 
shortest average lead time. First Class, despite being a premium option, 
recorded the longest average lead time — indicating inefficiencies in 
premium shipping operations.

### 3.3 Regional Lead Time Analysis
Gulf region recorded the shortest average lead time while Interior region 
recorded the longest. This is consistent with the geographic positioning 
of factories relative to customer regions.

### 3.4 Financial Analysis
- Chocolate division generates 92.9% of total revenue ($131,693)
- Other division contributes 6.8% ($9,663)
- Sugar division contributes only 0.3% ($427)
- Overall profit margin stands at 65.9%

---

## 4. Analytical Methodology

### 4.1 Data Preparation
The raw dataset was loaded from a SQLite database and processed as follows:
- Date columns converted to datetime format
- Lead time computed as the difference between Ship Date and Order Date
- Categorical features encoded using Label Encoding
- Numeric features validated and null values filled

### 4.2 Feature Engineering
The following features were selected for model training:
- Division (encoded)
- Region (encoded)
- Ship Mode (encoded)
- Product Name (encoded)
- Units
- Cost

Target variable: Lead Time (days)

### 4.3 Machine Learning Models
Three regression models were trained and evaluated:

#### Model 1: Linear Regression (Baseline)
A simple linear model used as a baseline to understand the linear 
relationship between features and lead time.

#### Model 2: Random Forest Regressor
An ensemble model using 100 decision trees to capture non-linear 
relationships in the data.

#### Model 3: Gradient Boosting Regressor
A sequential ensemble model using 100 estimators to minimize prediction 
error through boosting.

### 4.4 Model Evaluation

| Model | RMSE | MAE | R² |
|---|---|---|---|
| Linear Regression | 266.07 | 215.00 | -0.0010 |
| Gradient Boosting | 267.33 | 215.61 | -0.0105 |
| Random Forest | 277.20 | 225.02 | -0.0866 |

**Best Model: Linear Regression** — selected based on lowest RMSE and 
closest R² to zero.

Note: The negative R² values indicate that lead time in this dataset does 
not follow a strongly learnable pattern from the available features, which 
is consistent with the synthetic nature of the Ship Dates. However, the 
relative comparison between factory assignments remains valid and useful 
for the recommendation engine.

---

## 5. Scenario Simulation Engine

### 5.1 Haversine Distance Formula
Factory-to-region distances were calculated using the Haversine formula, 
which computes the great-circle distance between two geographic coordinates 
on Earth's surface.

### 5.2 Factory Coordinates

| Factory | Latitude | Longitude |
|---|---|---|
| Lot's O' Nuts | 32.881893 | -111.768036 |
| Wicked Choccy's | 32.076176 | -81.088371 |
| Sugar Shack | 48.119140 | -96.181150 |
| Secret Factory | 41.446333 | -90.565487 |
| The Other Factory | 35.117500 | -89.971107 |

### 5.3 Simulation Process
For each of the 15 products, all 5 factories were evaluated against all 
4 regions, producing 300 total simulation scenarios. For each scenario:
1. Haversine distance from factory to region was calculated
2. Lead time was predicted using the best ML model
3. Results were stored in the SQLite database

### 5.4 Recommendation Logic
For each product-region combination, the factory with the shortest 
distance was selected as the optimal assignment. This produced 60 
final recommendations (15 products × 4 regions).

---

## 6. Key Findings & Recommendations

### 6.1 Regional Factory Recommendations

| Region | Recommended Factory | Distance |
|---|---|---|
| Atlantic | Wicked Choccy's | 719 km |
| Gulf | The Other Factory | 680 km |
| Interior | Secret Factory | 210 km |
| Pacific | Lot's O' Nuts | 591 km |

### 6.2 Key Insights
1. **Secret Factory** is the most strategically located for Interior 
   region shipments at only 210 km — the shortest distance of any 
   factory-region combination.
2. **Wicked Choccy's** in Georgia is the best option for Atlantic 
   coast customers.
3. **The Other Factory** in Tennessee serves Gulf region customers 
   most efficiently.
4. **Lot's O' Nuts** in Arizona is geographically closest to Pacific 
   coast customers.
5. Several products currently assigned to distant factories could 
   reduce shipping distance by over 1,400 km through reassignment.

### 6.3 Risk Assessment
- No product-region combinations exceed the 2,000 km high-risk threshold
- All recommended assignments are within operationally safe distances
- Profit margin of 65.9% provides sufficient buffer for reassignment costs

---

## 7. System Architecture

### 7.1 Database Design
A SQLite relational database with 7 tables:

| Table | Rows | Purpose |
|---|---|---|
| orders | 10,194 | Raw order data |
| orders_cleaned | 10,194 | Cleaned data with Lead Time |
| factories | 5 | Factory coordinates |
| products | 15 | Product-factory mapping |
| simulation_results | 300 | All simulated scenarios |
| recommendations | 60 | Optimal assignments |
| model_results | 3 | ML model performance |

### 7.2 Technology Stack
- **Language:** Python 3.13
- **Database:** SQLite
- **ML Framework:** Scikit-learn
- **Dashboard:** Streamlit
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Deployment:** Streamlit Cloud

### 7.3 Dashboard Modules
1. **Home** — KPIs, project overview, financial summary
2. **EDA Dashboard** — 6 interactive charts
3. **Factory Simulator** — product vs factory comparison
4. **What-If Analysis** — current vs recommended assignments
5. **Recommendations** — filterable recommendation table
6. **Risk & Impact** — profit alerts and risk flags

---

## 8. Conclusion

This project successfully elevates Nassau Candy Distributor from 
descriptive analytics to intelligent decision-making. By combining 
predictive modeling with geographic optimization logic, the system 
provides actionable factory reallocation recommendations that can 
reduce shipping distances by up to 1,436 km for certain product-region 
combinations.

The live Streamlit dashboard enables business stakeholders to explore 
scenarios interactively, compare current vs recommended assignments, 
and download recommendations for operational use — without requiring 
any technical knowledge.

### 8.1 Future Enhancements
- Integration with real-time shipping APIs (FedEx, UPS)
- Capacity constraint modeling for each factory
- Seasonal demand forecasting
- Cost optimization beyond distance (fuel, tolls, handling)

---

## 9. References

1. Scikit-learn Documentation — Machine Learning in Python
2. Streamlit Documentation — Build and share data apps
3. SQLite Documentation — Serverless Database Engine
4. Haversine Formula — Geographic Distance Calculation
5. Nassau Candy Distributor — Internal Dataset (2024–2025)

---

*This research paper was prepared as part of the Nassau Candy Distributor 
Factory Optimization Project — May 2026*