import pandas as pd
import numpy as np
import sqlite3
import pickle
from sklearn.preprocessing import LabelEncoder

# ── Connect to database ───────────────────────────────────────
conn = sqlite3.connect("data/nassau_candy.db")
print("✅ Connected to database!")

# ── Load cleaned data from database ──────────────────────────
df = pd.read_sql("SELECT * FROM orders_cleaned", conn)
print("✅ Data loaded from database!")

# ── Load the saved best model ─────────────────────────────────
with open("data/best_model.pkl", "rb") as f:
    model = pickle.load(f)
print("✅ Best model loaded!")

# ── Load factories from database ─────────────────────────────
factories_df = pd.read_sql("SELECT * FROM factories", conn)
factories = {
    row['Factory']: {"lat": row['Latitude'], "lon": row['Longitude']}
    for _, row in factories_df.iterrows()
}

# ── Define region center coordinates ─────────────────────────
regions = {
    "Atlantic":  {"lat": 37.000, "lon": -76.000},
    "Gulf":      {"lat": 29.000, "lon": -90.000},
    "Interior":  {"lat": 41.000, "lon": -93.000},
    "Pacific":   {"lat": 34.000, "lon": -118.000},
}

print("✅ Factories loaded from database!")
print("✅ Regions defined!")
print()

# ── Haversine distance formula ────────────────────────────────
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return R * c

# ── Test distance function ────────────────────────────────────
test_dist = haversine(
    factories["Lot's O' Nuts"]["lat"],
    factories["Lot's O' Nuts"]["lon"],
    regions["Atlantic"]["lat"],
    regions["Atlantic"]["lon"]
)
print(f"✅ Distance function works!")
print(f"   Example: Lot's O' Nuts → Atlantic = {test_dist:.0f} km")
print()

# ── Encode features ───────────────────────────────────────────
products  = df['Product Name'].unique()
divisions = df.groupby('Product Name')['Division'].first()

le_division = LabelEncoder().fit(df['Division'].astype(str))
le_region   = LabelEncoder().fit(df['Region'].astype(str))
le_shipmode = LabelEncoder().fit(df['Ship Mode'].astype(str))
le_product  = LabelEncoder().fit(df['Product Name'].astype(str))

# ── Simulate factory reassignment for every product ───────────
results = []

for product in products:
    for factory_name, factory_coords in factories.items():
        for region_name, region_coords in regions.items():

            # Calculate distance from factory to region
            distance = haversine(
                factory_coords["lat"], factory_coords["lon"],
                region_coords["lat"],  region_coords["lon"]
            )

            # Get average units and cost for this product
            avg_units = df[df['Product Name'] == product]['Units'].mean()
            avg_cost  = df[df['Product Name'] == product]['Cost'].mean()

            # Prepare input for model
            X_input = pd.DataFrame([{
                'Division'    : le_division.transform([divisions[product]])[0],
                'Region'      : le_region.transform([region_name])[0],
                'Ship Mode'   : le_shipmode.transform(['Standard Class'])[0],
                'Product Name': le_product.transform([product])[0],
                'Units'       : avg_units,
                'Cost'        : avg_cost
            }])

            # Predict lead time
            predicted_lead_time = model.predict(X_input)[0]

            results.append({
                'Product'             : product,
                'Factory'             : factory_name,
                'Region'              : region_name,
                'Distance (km)'       : round(distance),
                'Predicted Lead Time' : round(predicted_lead_time, 1)
            })

results_df = pd.DataFrame(results)
print("✅ Simulation complete!")
print(f"   Total scenarios simulated: {len(results_df)}")
print()

# ── Generate recommendations ──────────────────────────────────
recommendations = []

for product in products:
    for region_name in regions.keys():

        # Filter simulation results for this product+region
        subset = results_df[
            (results_df['Product'] == product) &
            (results_df['Region']  == region_name)
        ].copy()

        # Sort by distance — shortest = best
        subset = subset.sort_values('Distance (km)')
        best   = subset.iloc[0]

        recommendations.append({
            'Product'             : product,
            'Region'              : region_name,
            'Best Factory'        : best['Factory'],
            'Distance (km)'       : best['Distance (km)'],
            'Predicted Lead Time' : best['Predicted Lead Time']
        })

recommendations_df = pd.DataFrame(recommendations)
print("✅ Recommendations generated!")
print()
print("📋 Top Factory Recommendations:")
print(recommendations_df.to_string(index=False))
print()

# ── Save results to database ──────────────────────────────────
results_df.to_sql("simulation_results", conn, if_exists="replace", index=False)
recommendations_df.to_sql("recommendations", conn, if_exists="replace", index=False)

print("✅ Simulation results saved to database — table: simulation_results")
print("✅ Recommendations saved to database — table: recommendations")

conn.close()
print("✅ Database connection closed!")
print()
print("🎉 Phase 4 Complete!")