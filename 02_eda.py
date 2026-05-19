import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# ── Connect to database and load cleaned data ─────────────────
conn = sqlite3.connect("data/nassau_candy.db")
df = pd.read_sql("SELECT * FROM orders_cleaned", conn)
conn.close()

print("✅ Data loaded from database!")
print(f"   Rows: {len(df)}")
print()

# ── Set plot style ────────────────────────────────────────────
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 5)

# ── Chart 1: Orders by Division ───────────────────────────────
division_counts = df['Division'].value_counts()

plt.figure()
sns.barplot(x=division_counts.index, y=division_counts.values, palette="Blues_d",
            hue=division_counts.index, legend=False)
plt.title("Number of Orders by Division")
plt.xlabel("Division")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.savefig("data/chart1_orders_by_division.png")
plt.show()
print("✅ Chart 1 saved — Orders by Division")

# ── Chart 2: Orders by Ship Mode ─────────────────────────────
ship_counts = df['Ship Mode'].value_counts()

plt.figure()
sns.barplot(x=ship_counts.index, y=ship_counts.values, palette="Greens_d",
            hue=ship_counts.index, legend=False)
plt.title("Number of Orders by Ship Mode")
plt.xlabel("Ship Mode")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.savefig("data/chart2_orders_by_shipmode.png")
plt.show()
print("✅ Chart 2 saved — Orders by Ship Mode")

# ── Chart 3: Average Lead Time by Ship Mode ───────────────────
lead_ship = df.groupby('Ship Mode')['Lead Time'].mean().sort_values()

plt.figure()
sns.barplot(x=lead_ship.index, y=lead_ship.values, palette="Oranges_d",
            hue=lead_ship.index, legend=False)
plt.title("Average Lead Time by Ship Mode")
plt.xlabel("Ship Mode")
plt.ylabel("Average Lead Time (days)")
plt.tight_layout()
plt.savefig("data/chart3_leadtime_by_shipmode.png")
plt.show()
print("✅ Chart 3 saved — Avg Lead Time by Ship Mode")

# ── Chart 4: Average Lead Time by Region ─────────────────────
lead_region = df.groupby('Region')['Lead Time'].mean().sort_values()

plt.figure()
sns.barplot(x=lead_region.index, y=lead_region.values, palette="Purples_d",
            hue=lead_region.index, legend=False)
plt.title("Average Lead Time by Region")
plt.xlabel("Region")
plt.ylabel("Average Lead Time (days)")
plt.tight_layout()
plt.savefig("data/chart4_leadtime_by_region.png")
plt.show()
print("✅ Chart 4 saved — Avg Lead Time by Region")

# ── Chart 5: Top 10 Products by Orders ───────────────────────
product_counts = df['Product Name'].value_counts().head(10)

plt.figure(figsize=(12, 5))
sns.barplot(x=product_counts.values, y=product_counts.index, palette="Blues_d",
            hue=product_counts.index, legend=False)
plt.title("Top Products by Number of Orders")
plt.xlabel("Number of Orders")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig("data/chart5_top_products.png")
plt.show()
print("✅ Chart 5 saved — Top Products by Orders")

# ── Chart 6: Sales vs Gross Profit by Division ────────────────
div_finance = df.groupby('Division')[['Sales', 'Gross Profit']].sum()

plt.figure()
div_finance.plot(kind='bar', color=['#4C72B0', '#55A868'], rot=0)
plt.title("Total Sales vs Gross Profit by Division")
plt.xlabel("Division")
plt.ylabel("Amount ($)")
plt.tight_layout()
plt.savefig("data/chart6_sales_profit_division.png")
plt.show()
print("✅ Chart 6 saved — Sales vs Gross Profit by Division")

print()
print("🎉 EDA Complete! All 6 charts saved in the data/ folder")