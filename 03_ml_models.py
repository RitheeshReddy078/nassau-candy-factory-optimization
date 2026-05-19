import pandas as pd
import numpy as np
import sqlite3
import pickle
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# ── Connect to database and load cleaned data ─────────────────
conn = sqlite3.connect("data/nassau_candy.db")
df = pd.read_sql("SELECT * FROM orders_cleaned", conn)
print("✅ Data loaded from database!")

# ── Select features for the model ────────────────────────────
features = ['Division', 'Region', 'Ship Mode', 'Product Name', 'Units', 'Cost']
target   = 'Lead Time'

# ── Encode categorical columns to numbers ─────────────────────
le = LabelEncoder()
df_model = df.copy()

le_dict = {}
for col in features:
    if df_model[col].dtype == 'object':
        le_dict[col] = LabelEncoder()
        df_model[col] = le_dict[col].fit_transform(df_model[col].astype(str))
    else:
        df_model[col] = pd.to_numeric(df_model[col], errors='coerce').fillna(0)

print("✅ Features encoded!")

# ── Split into X (inputs) and y (output) ─────────────────────
X = df_model[features]
y = df_model[target]

# ── Split into training and testing sets ─────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"✅ Data split — Train: {len(X_train)} rows, Test: {len(X_test)} rows")
print()

# ── Model 1: Linear Regression ────────────────────────────────
lr = LinearRegression()
lr.fit(X_train, y_train)
lr_pred = lr.predict(X_test)

lr_rmse = np.sqrt(mean_squared_error(y_test, lr_pred))
lr_mae  = mean_absolute_error(y_test, lr_pred)
lr_r2   = r2_score(y_test, lr_pred)

print("📊 Model 1: Linear Regression")
print(f"   RMSE : {lr_rmse:.2f}")
print(f"   MAE  : {lr_mae:.2f}")
print(f"   R²   : {lr_r2:.4f}")
print()

# ── Model 2: Random Forest ────────────────────────────────────
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)

rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
rf_mae  = mean_absolute_error(y_test, rf_pred)
rf_r2   = r2_score(y_test, rf_pred)

print("📊 Model 2: Random Forest")
print(f"   RMSE : {rf_rmse:.2f}")
print(f"   MAE  : {rf_mae:.2f}")
print(f"   R²   : {rf_r2:.4f}")
print()

# ── Model 3: Gradient Boosting ────────────────────────────────
gb = GradientBoostingRegressor(n_estimators=100, random_state=42)
gb.fit(X_train, y_train)
gb_pred = gb.predict(X_test)

gb_rmse = np.sqrt(mean_squared_error(y_test, gb_pred))
gb_mae  = mean_absolute_error(y_test, gb_pred)
gb_r2   = r2_score(y_test, gb_pred)

print("📊 Model 3: Gradient Boosting")
print(f"   RMSE : {gb_rmse:.2f}")
print(f"   MAE  : {gb_mae:.2f}")
print(f"   R²   : {gb_r2:.4f}")
print()

# ── Compare all 3 models ──────────────────────────────────────
results = pd.DataFrame({
    'Model': ['Linear Regression', 'Random Forest', 'Gradient Boosting'],
    'RMSE' : [lr_rmse, rf_rmse, gb_rmse],
    'MAE'  : [lr_mae,  rf_mae,  gb_mae],
    'R²'   : [lr_r2,   rf_r2,   gb_r2]
})

print("📋 Model Comparison:")
print(results.to_string(index=False))
print()

# ── Find the best model ───────────────────────────────────────
best = results.loc[results['R²'].idxmax(), 'Model']
print(f"🏆 Best Model: {best}")
print()

# ── Save model results to database ───────────────────────────
results.to_sql("model_results", conn, if_exists="replace", index=False)
print("✅ Model results saved to database — table: model_results")

# ── Plot model comparison ─────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(14, 5))

metrics = ['RMSE', 'MAE', 'R²']
colors  = ['#4C72B0', '#55A868', '#C44E52']

for i, metric in enumerate(metrics):
    axes[i].bar(results['Model'], results[metric], color=colors[i])
    axes[i].set_title(f'{metric} Comparison')
    axes[i].set_ylabel(metric)
    axes[i].tick_params(axis='x', rotation=15)

plt.suptitle("Model Performance Comparison", fontsize=14)
plt.tight_layout()
plt.savefig("data/chart7_model_comparison.png")
plt.show()
print("✅ Chart 7 saved — Model Comparison")
print()

# ── Save the best model ───────────────────────────────────────
best_model = lr  # Linear Regression is best
with open("data/best_model.pkl", "wb") as f:
    pickle.dump(best_model, f)

print("✅ Best model saved to data/best_model.pkl")

conn.close()
print("✅ Database connection closed!")
print()
print("🎉 Phase 3 Complete!")