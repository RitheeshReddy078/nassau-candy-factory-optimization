import pandas as pd
import numpy as np
import sqlite3

# ── Connect to database ───────────────────────────────────────
conn = sqlite3.connect("data/nassau_candy.db")
print("✅ Connected to database!")

# ── Load the dataset from database ───────────────────────────
df = pd.read_sql("SELECT * FROM orders", conn)

print("✅ Dataset loaded from database!")
print(f"   Rows: {len(df)}")
print(f"   Columns: {len(df.columns)}")
print()

df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date']  = pd.to_datetime(df['Ship Date'])

print("✅ Dates converted!")
print()

# ── Create Lead Time column ───────────────────────────────────
df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days

print("✅ Lead Time column created!")
print(f"   Min:  {df['Lead Time'].min()} days")
print(f"   Max:  {df['Lead Time'].max()} days")
print(f"   Mean: {df['Lead Time'].mean():.1f} days")
print()

# ── Check for nulls ───────────────────────────────────────────
nulls = df.isnull().sum().sum()
print(f"✅ Null values: {nulls} (should be 0)")
print()

# ── Save cleaned data back to database ───────────────────────
df.to_sql("orders_cleaned", conn, if_exists="replace", index=False)
print("✅ Cleaned data saved to database — table: orders_cleaned")

conn.close()
print("✅ Database connection closed!")