import pandas as pd
import sqlite3
import os

# ── Connect to SQLite database ────────────────────────────────
# This will create a new file called nassau_candy.db
conn = sqlite3.connect("data/nassau_candy.db")
cursor = conn.cursor()
print("✅ Database created!")

# ── Load the original CSV ─────────────────────────────────────
df = pd.read_csv("data/Nassau_Candy_Distributor.csv")
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Ship Date']  = pd.to_datetime(df['Ship Date'],  dayfirst=True)
df['Lead Time']  = (df['Ship Date'] - df['Order Date']).dt.days
print("✅ CSV loaded and Lead Time calculated!")

# ── Save orders table ─────────────────────────────────────────
df.to_sql("orders", conn, if_exists="replace", index=False)
print(f"✅ Orders table created — {len(df)} rows inserted!")

# ── Save factories table ──────────────────────────────────────
factories_df = pd.DataFrame([
    {"Factory": "Lot's O' Nuts",     "Latitude": 32.881893, "Longitude": -111.768036},
    {"Factory": "Wicked Choccy's",   "Latitude": 32.076176, "Longitude": -81.088371},
    {"Factory": "Sugar Shack",       "Latitude": 48.119140, "Longitude": -96.181150},
    {"Factory": "Secret Factory",    "Latitude": 41.446333, "Longitude": -90.565487},
    {"Factory": "The Other Factory", "Latitude": 35.117500, "Longitude": -89.971107},
])
factories_df.to_sql("factories", conn, if_exists="replace", index=False)
print("✅ Factories table created — 5 factories inserted!")

# ── Save products table ───────────────────────────────────────
products_df = pd.DataFrame([
    {"Product": "Wonka Bar - Nutty Crunch Surprise",   "Division": "Chocolate", "Factory": "Lot's O' Nuts"},
    {"Product": "Wonka Bar - Fudge Mallows",           "Division": "Chocolate", "Factory": "Lot's O' Nuts"},
    {"Product": "Wonka Bar -Scrumdiddlyumptious",      "Division": "Chocolate", "Factory": "Lot's O' Nuts"},
    {"Product": "Wonka Bar - Milk Chocolate",          "Division": "Chocolate", "Factory": "Wicked Choccy's"},
    {"Product": "Wonka Bar - Triple Dazzle Caramel",   "Division": "Chocolate", "Factory": "Wicked Choccy's"},
    {"Product": "Laffy Taffy",                         "Division": "Sugar",     "Factory": "Sugar Shack"},
    {"Product": "SweeTARTS",                           "Division": "Sugar",     "Factory": "Sugar Shack"},
    {"Product": "Nerds",                               "Division": "Sugar",     "Factory": "Sugar Shack"},
    {"Product": "Fun Dip",                             "Division": "Sugar",     "Factory": "Sugar Shack"},
    {"Product": "Fizzy Lifting Drinks",                "Division": "Other",     "Factory": "Sugar Shack"},
    {"Product": "Everlasting Gobstopper",              "Division": "Sugar",     "Factory": "Secret Factory"},
    {"Product": "Hair Toffee",                         "Division": "Sugar",     "Factory": "The Other Factory"},
    {"Product": "Lickable Wallpaper",                  "Division": "Other",     "Factory": "Secret Factory"},
    {"Product": "Wonka Gum",                           "Division": "Other",     "Factory": "Secret Factory"},
    {"Product": "Kazookles",                           "Division": "Other",     "Factory": "The Other Factory"},
])
products_df.to_sql("products", conn, if_exists="replace", index=False)
print("✅ Products table created — 15 products inserted!")

# ── Save recommendations table ────────────────────────────────
rec_df = pd.read_csv("data/recommendations.csv")
rec_df.to_sql("recommendations", conn, if_exists="replace", index=False)
print("✅ Recommendations table created!")

# ── Verify all tables ─────────────────────────────────────────
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print()
print("📋 Tables in database:")
for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
    count = cursor.fetchone()[0]
    print(f"   {table[0]} — {count} rows")

conn.close()
print()
print("🎉 Database setup complete! — data/nassau_candy.db")