import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import pickle
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

# ── Page configuration ────────────────────────────────────────
st.set_page_config(
    page_title="Nassau Candy — Factory Optimization",
    page_icon="🍬",
    layout="wide"
)

# ── Database connection ───────────────────────────────────────
@st.cache_resource
def get_connection():
    return sqlite3.connect("data/nassau_candy.db", check_same_thread=False)

@st.cache_data
def load_data():
    conn = get_connection()
    orders       = pd.read_sql("SELECT * FROM orders_cleaned", conn)
    factories    = pd.read_sql("SELECT * FROM factories", conn)
    products     = pd.read_sql("SELECT * FROM products", conn)
    simulation   = pd.read_sql("SELECT * FROM simulation_results", conn)
    recommend    = pd.read_sql("SELECT * FROM recommendations", conn)
    model_result = pd.read_sql("SELECT * FROM model_results", conn)
    return orders, factories, products, simulation, recommend, model_result

@st.cache_resource
def load_model():
    with open("data/best_model.pkl", "rb") as f:
        return pickle.load(f)

orders, factories, products, simulation, recommend, model_result = load_data()
model = load_model()

# ── Fix numeric columns ───────────────────────────────────────
for col in ['Sales', 'Gross Profit', 'Cost', 'Lead Time', 'Units']:
    orders[col] = pd.to_numeric(orders[col], errors='coerce').fillna(0)

# ── Dark theme for all matplotlib charts ─────────────────────
plt.rcParams.update({
    'figure.facecolor':  '#0f2040',
    'axes.facecolor':    '#0f2040',
    'axes.edgecolor':    '#c9a84c',
    'axes.labelcolor':   '#e8d5a3',
    'xtick.color':       '#e8d5a3',
    'ytick.color':       '#e8d5a3',
    'text.color':        '#e8d5a3',
    'grid.color':        '#1a2a4a',
    'grid.alpha':        0.5,
    'axes.grid':         True,
    'figure.figsize':    (8, 4),
})

# ── Helper: page header ───────────────────────────────────────
def page_header(title, subtitle, icon):
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1a2a4a 0%,#0f3460 100%);
                border:1px solid #c9a84c; border-radius:16px;
                padding:28px 36px; margin-bottom:28px;
                display:flex; align-items:center; gap:20px;
                box-shadow:0 4px 20px rgba(201,168,76,0.15);">
        <div style="font-size:40px;">{icon}</div>
        <div>
            <p style="color:#c9a84c;font-size:11px;letter-spacing:3px;
                      margin:0 0 4px 0;">NASSAU CANDY DISTRIBUTOR</p>
            <h2 style="color:#ffffff;font-family:Georgia,serif;
                       font-size:26px;margin:0 0 6px 0;">{title}</h2>
            <p style="color:#a0b4c8;font-size:13px;margin:0;">{subtitle}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Helper: section title ─────────────────────────────────────
def section_title(label, title):
    st.markdown(f"""
    <div style="margin:24px 0 16px 0;">
        <p style="color:#c9a84c;font-size:10px;letter-spacing:3px;
                  margin:0 0 4px 0;">{label}</p>
        <h3 style="color:#ffffff;font-family:Georgia,serif;
                   font-size:20px;margin:0 0 8px 0;">{title}</h3>
        <div style="width:36px;height:2px;background:#c9a84c;"></div>
    </div>
    """, unsafe_allow_html=True)

# ── Helper: metric card ───────────────────────────────────────
def metric_card(col, icon, label, value, sub, border="#c9a84c"):
    with col:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1a2a4a 0%,#0f3460 100%);
                    border:1px solid {border}; border-top:3px solid {border};
                    border-radius:14px; padding:24px 12px; text-align:center;
                    box-shadow:0 4px 15px rgba(0,0,0,0.3); margin-bottom:8px;
                    min-height:160px; display:flex; flex-direction:column;
                    align-items:center; justify-content:center;">
            <div style="font-size:24px;margin-bottom:10px;">{icon}</div>
            <p style="color:#a0b4c8;font-size:10px;letter-spacing:2px;
                      margin:0 0 8px 0;white-space:nowrap;">{label}</p>
            <p style="color:{border};font-size:26px;font-weight:700;
                      margin:0 0 6px 0;font-family:Georgia,serif;
                      line-height:1;white-space:nowrap;">{value}</p>
            <p style="color:#e8d5a3;font-size:11px;margin:0;">{sub}</p>
        </div>
        """, unsafe_allow_html=True)

# ── Global styles ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);
}
.stApp {
    background: linear-gradient(135deg,#0d1117 0%,#0d1b2e 50%,#0f2040 100%);
}
.stApp p, .stApp h1, .stApp h2, .stApp h3 { color: #e8e8e8; }
div[data-testid="stSidebar"] .stButton button {
    width:100%;
    background:linear-gradient(135deg,#2c3e6b 0%,#1a2a4a 100%);
    color:#e8d5a3; border:1px solid #c9a84c; border-radius:8px;
    padding:10px 16px; font-size:14px; font-weight:500;
    text-align:left; margin-bottom:6px; transition:all 0.3s ease;
}
div[data-testid="stSidebar"] .stButton button:hover {
    background:linear-gradient(135deg,#c9a84c 0%,#a07830 100%);
    color:#ffffff; border-color:#e8d5a3; transform:translateX(4px);
}
div[data-testid="stSidebar"] .stButton button:focus {
    background:linear-gradient(135deg,#c9a84c 0%,#a07830 100%);
    color:#ffffff;
}
[data-testid="stSidebar"] p      { color:#e8d5a3; }
[data-testid="stSidebar"] hr     { border-color:#c9a84c; opacity:0.4; }
[data-testid="stSidebar"] .stSuccess {
    background:rgba(201,168,76,0.15); border:1px solid #c9a84c;
}
[data-testid="stDataFrame"]      { border-radius:10px; overflow:hidden; }
[data-testid="stSelectbox"] label {
    color:#c9a84c !important; font-size:12px; letter-spacing:1px;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center;padding:20px 0 10px 0;'>
    <span style='font-family:Georgia,serif;font-size:22px;
    font-weight:700;color:#c9a84c;letter-spacing:3px;'>NASSAU CANDY</span>
    <br><br>
    <span style='font-family:Georgia,serif;font-size:10px;
    color:#e8d5a3;letter-spacing:2px;'>Specialty Confections & Fine Foods</span>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown(
    "<p style='text-align:center;color:#c9a84c;font-size:10px;"
    "letter-spacing:2px;'>FACTORY OPTIMIZATION SYSTEM</p>",
    unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown(
    "<p style='color:#e8d5a3;font-size:11px;font-weight:600;"
    "letter-spacing:2px;'>NAVIGATE</p>",
    unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = "🏠 Home"

pages = [
    ("🏠  Home",              "🏠 Home"),
    ("📊  EDA Dashboard",     "📊 EDA Dashboard"),
    ("🏭  Factory Simulator", "🏭 Factory Simulator"),
    ("🔄  What-If Analysis",  "🔄 What-If Analysis"),
    ("🏆  Recommendations",   "🏆 Recommendations"),
    ("⚠️  Risk & Impact",     "⚠️ Risk & Impact"),
]
for btn_label, page_key in pages:
    if st.sidebar.button(btn_label):
        st.session_state.page = page_key

page = st.session_state.page

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<p style='color:#e8d5a3;font-size:11px;font-weight:600;"
    "letter-spacing:2px;'>DATABASE STATUS</p>",
    unsafe_allow_html=True)
st.sidebar.success(f"✅ {len(orders):,} orders loaded")
st.sidebar.success(f"✅ {len(products)} products tracked")
st.sidebar.success(f"✅ {len(factories)} factories connected")

# ══════════════════════════════════════════════════════════════
# PAGE 1 — HOME
# ══════════════════════════════════════════════════════════════
if page == "🏠 Home":

    st.markdown("""
    <div style="background:linear-gradient(135deg,#1a2a4a 0%,#0f3460 60%,#1a1a2e 100%);
                border:1px solid #c9a84c; border-radius:20px;
                padding:50px 40px; text-align:center; margin-bottom:32px;
                box-shadow:0 8px 32px rgba(201,168,76,0.15);">
        <p style="color:#c9a84c;font-size:11px;letter-spacing:4px;margin-bottom:12px;">
            DECISION INTELLIGENCE PLATFORM</p>
        <h1 style="font-family:Georgia,serif;color:#ffffff;font-size:46px;
                   font-weight:700;letter-spacing:2px;margin:0 0 8px 0;">
            Nassau Candy Distributor</h1>
        <div style="width:80px;height:2px;background:#c9a84c;margin:16px auto;"></div>
        <p style="color:#a0b4c8;font-size:15px;letter-spacing:1px;margin:0;">
            Factory Reallocation & Shipping Optimization System</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    metric_card(col1, "📦", "TOTAL ORDERS",    f"{len(orders):,}",                   "orders processed")
    metric_card(col2, "🍬", "TOTAL PRODUCTS",  f"{len(products)}",                   "unique products")
    metric_card(col3, "🏭", "TOTAL FACTORIES", f"{len(factories)}",                  "active factories")
    metric_card(col4, "⏱", "AVG LEAD TIME",   f"{orders['Lead Time'].mean():.0f}d", "days average")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 0.9])
    with col1:
        # ── ALL points hardcoded inside one HTML block ────────
        st.markdown("""
        <div style="background:linear-gradient(135deg,#1a2a4a 0%,#0f3460 100%);
                    border:1px solid rgba(201,168,76,0.5); border-radius:16px;
                    padding:32px; box-shadow:0 4px 15px rgba(0,0,0,0.3);">
            <p style="color:#c9a84c;font-size:10px;letter-spacing:3px;margin-bottom:6px;">
                ABOUT THIS SYSTEM</p>
            <h3 style="color:#ffffff;font-family:Georgia,serif;
                       font-size:22px;margin-bottom:16px;">Project Overview</h3>
            <div style="width:36px;height:2px;background:#c9a84c;margin-bottom:20px;"></div>
            <p style="color:#a0b4c8;font-size:13px;line-height:1.9;margin-bottom:20px;">
                This intelligent platform elevates Nassau Candy Distributor from static
                logistics to <strong style="color:#e8d5a3;">data-driven decision making</strong>,
                combining predictive modeling with optimization logic.
            </p>
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
                <span style="background:#c9a84c;color:#1a1a2e;border-radius:50%;
                             width:26px;height:26px;display:flex;align-items:center;
                             justify-content:center;font-size:11px;font-weight:700;
                             flex-shrink:0;">1</span>
                <span style="color:#e8d5a3;font-size:13px;">
                    Analyze shipping patterns across all regions</span>
            </div>
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
                <span style="background:#c9a84c;color:#1a1a2e;border-radius:50%;
                             width:26px;height:26px;display:flex;align-items:center;
                             justify-content:center;font-size:11px;font-weight:700;
                             flex-shrink:0;">2</span>
                <span style="color:#e8d5a3;font-size:13px;">
                    Predict lead times using Machine Learning models</span>
            </div>
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
                <span style="background:#c9a84c;color:#1a1a2e;border-radius:50%;
                             width:26px;height:26px;display:flex;align-items:center;
                             justify-content:center;font-size:11px;font-weight:700;
                             flex-shrink:0;">3</span>
                <span style="color:#e8d5a3;font-size:13px;">
                    Simulate factory reassignment scenarios at scale</span>
            </div>
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
                <span style="background:#c9a84c;color:#1a1a2e;border-radius:50%;
                             width:26px;height:26px;display:flex;align-items:center;
                             justify-content:center;font-size:11px;font-weight:700;
                             flex-shrink:0;">4</span>
                <span style="color:#e8d5a3;font-size:13px;">
                    Recommend optimal factory-product assignments</span>
            </div>
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
                <span style="background:#c9a84c;color:#1a1a2e;border-radius:50%;
                             width:26px;height:26px;display:flex;align-items:center;
                             justify-content:center;font-size:11px;font-weight:700;
                             flex-shrink:0;">5</span>
                <span style="color:#e8d5a3;font-size:13px;">
                    Quantify profit impact before execution</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#1a2a4a 0%,#0f3460 100%);
                    border:1px solid rgba(201,168,76,0.5); border-radius:16px;
                    padding:32px; box-shadow:0 4px 15px rgba(0,0,0,0.3);">
            <p style="color:#c9a84c;font-size:10px;letter-spacing:3px;margin-bottom:6px;">
                FACTORY NETWORK</p>
            <h3 style="color:#ffffff;font-family:Georgia,serif;
                       font-size:22px;margin-bottom:16px;">Our Factories</h3>
            <div style="width:36px;height:2px;background:#c9a84c;margin-bottom:20px;"></div>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(factories, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)

    total_sales   = orders['Sales'].sum()
    total_profit  = orders['Gross Profit'].sum()
    total_cost    = orders['Cost'].sum()
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0

    section_title("FINANCIAL SUMMARY", "Business Performance")
    col1, col2, col3, col4 = st.columns(4)
    metric_card(col1, "💰", "TOTAL REVENUE",  f"${total_sales:,.0f}",  "gross revenue",  "#2ecc71")
    metric_card(col2, "📈", "GROSS PROFIT",   f"${total_profit:,.0f}", "after costs",    "#c9a84c")
    metric_card(col3, "💸", "TOTAL COST",     f"${total_cost:,.0f}",   "manufacturing",  "#e74c3c")
    metric_card(col4, "🎯", "PROFIT MARGIN",  f"{profit_margin:.1f}%", "overall margin", "#3498db")

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("INVENTORY", "Product Catalogue")
    st.dataframe(products, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════
# PAGE 2 — EDA DASHBOARD
# ══════════════════════════════════════════════════════════════
elif page == "📊 EDA Dashboard":
    page_header("EDA Dashboard",
                "Exploratory analysis of orders, shipping, and financials", "📊")

    col1, col2 = st.columns(2)
    with col1:
        section_title("DISTRIBUTION", "Orders by Division")
        div_counts = orders['Division'].value_counts()
        fig, ax = plt.subplots()
        bars = ax.bar(div_counts.index, div_counts.values,
                      color=['#c9a84c','#3498db','#2ecc71'],
                      edgecolor='#0f2040', linewidth=0.5)
        ax.set_xlabel("Division")
        ax.set_ylabel("Number of Orders")
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 50,
                    f'{int(bar.get_height()):,}',
                    ha='center', va='bottom', fontsize=10, color='#e8d5a3')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        section_title("DISTRIBUTION", "Orders by Ship Mode")
        ship_counts = orders['Ship Mode'].value_counts()
        fig, ax = plt.subplots()
        bars = ax.bar(ship_counts.index, ship_counts.values,
                      color=['#3498db','#c9a84c','#2ecc71','#e74c3c'],
                      edgecolor='#0f2040', linewidth=0.5)
        ax.set_xlabel("Ship Mode")
        ax.set_ylabel("Number of Orders")
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 20,
                    f'{int(bar.get_height()):,}',
                    ha='center', va='bottom', fontsize=10, color='#e8d5a3')
        plt.xticks(rotation=15)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        section_title("PERFORMANCE", "Avg Lead Time by Ship Mode")
        lead_ship = orders.groupby('Ship Mode')['Lead Time'].mean().sort_values()
        fig, ax = plt.subplots()
        bars = ax.barh(lead_ship.index, lead_ship.values,
                       color='#e74c3c', edgecolor='#0f2040', linewidth=0.5)
        ax.set_xlabel("Average Lead Time (days)")
        for bar in bars:
            ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                    f'{bar.get_width():.0f}d',
                    va='center', fontsize=10, color='#e8d5a3')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        section_title("PERFORMANCE", "Avg Lead Time by Region")
        lead_region = orders.groupby('Region')['Lead Time'].mean().sort_values()
        fig, ax = plt.subplots()
        bars = ax.barh(lead_region.index, lead_region.values,
                       color='#8172B2', edgecolor='#0f2040', linewidth=0.5)
        ax.set_xlabel("Average Lead Time (days)")
        for bar in bars:
            ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                    f'{bar.get_width():.0f}d',
                    va='center', fontsize=10, color='#e8d5a3')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("FINANCIALS", "Sales vs Gross Profit by Division")
    div_finance = orders.groupby('Division')[['Sales', 'Gross Profit']].sum()
    fig, ax = plt.subplots(figsize=(10, 4))
    x = range(len(div_finance))
    width = 0.35
    bars1 = ax.bar([i - width/2 for i in x], div_finance['Sales'],
                   width, color='#3498db', label='Sales', edgecolor='#0f2040')
    bars2 = ax.bar([i + width/2 for i in x], div_finance['Gross Profit'],
                   width, color='#c9a84c', label='Gross Profit', edgecolor='#0f2040')
    ax.set_xticks(list(x))
    ax.set_xticklabels(div_finance.index)
    ax.set_ylabel("Amount ($)")
    ax.legend(facecolor='#1a2a4a', edgecolor='#c9a84c', labelcolor='#e8d5a3')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("DATA", "Raw Data Viewer (first 100 rows)")
    st.dataframe(orders.head(100), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════
# PAGE 3 — FACTORY SIMULATOR
# ══════════════════════════════════════════════════════════════
elif page == "🏭 Factory Simulator":
    page_header("Factory Simulator",
                "Select a product and compare performance across all 5 factories", "🏭")

    col1, col2 = st.columns(2)
    with col1:
        selected_product = st.selectbox("SELECT PRODUCT",
                                        sorted(orders['Product Name'].unique()))
    with col2:
        selected_region = st.selectbox("SELECT REGION",
                                       ["Atlantic", "Gulf", "Interior", "Pacific"])

    filtered = simulation[
        (simulation['Product'] == selected_product) &
        (simulation['Region']  == selected_region)
    ].sort_values('Distance (km)')

    best_factory  = filtered.iloc[0]['Factory']
    best_distance = filtered.iloc[0]['Distance (km)']
    best_lead     = filtered.iloc[0]['Predicted Lead Time']

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    metric_card(col1, "🏆", "BEST FACTORY",      best_factory,          "recommended",    "#2ecc71")
    metric_card(col2, "📍", "SHORTEST DISTANCE", f"{best_distance} km", "to region",      "#c9a84c")
    metric_card(col3, "⏱", "PREDICTED LEAD",    f"{best_lead:.0f}d",   "estimated days", "#3498db")

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("COMPARISON", f"{selected_product} → {selected_region}")

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    colors_dist = ['#2ecc71' if f == best_factory else '#2c3e6b'
                   for f in filtered['Factory']]
    axes[0].bar(filtered['Factory'], filtered['Distance (km)'],
                color=colors_dist, edgecolor='#0f2040', linewidth=0.5)
    axes[0].set_title("Distance to Region (km)", color='#c9a84c', fontsize=12)
    axes[0].set_xlabel("Factory")
    axes[0].set_ylabel("Distance (km)")
    axes[0].tick_params(axis='x', rotation=15)
    for i, (_, row) in enumerate(filtered.iterrows()):
        axes[0].text(i, row['Distance (km)'] + 20,
                     f"{row['Distance (km)']:.0f}",
                     ha='center', fontsize=9, color='#e8d5a3')

    colors_lead = ['#2ecc71' if f == best_factory else '#2c3e6b'
                   for f in filtered['Factory']]
    axes[1].bar(filtered['Factory'], filtered['Predicted Lead Time'],
                color=colors_lead, edgecolor='#0f2040', linewidth=0.5)
    axes[1].set_title("Predicted Lead Time (days)", color='#c9a84c', fontsize=12)
    axes[1].set_xlabel("Factory")
    axes[1].set_ylabel("Lead Time (days)")
    axes[1].tick_params(axis='x', rotation=15)

    plt.suptitle("Green = Best Factory", color='#2ecc71', fontsize=10, y=1.02)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("DATA", "Detailed Factory Comparison")
    st.dataframe(filtered.reset_index(drop=True),
                 use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════
# PAGE 4 — WHAT-IF ANALYSIS
# ══════════════════════════════════════════════════════════════
elif page == "🔄 What-If Analysis":
    page_header("What-If Analysis",
                "Compare current factory assignment vs AI-recommended assignment", "🔄")

    col1, col2, col3 = st.columns(3)
    with col1:
        wi_product  = st.selectbox("SELECT PRODUCT",
                                   sorted(orders['Product Name'].unique()))
    with col2:
        wi_region   = st.selectbox("SELECT REGION",
                                   ["Atlantic", "Gulf", "Interior", "Pacific"])
    with col3:
        wi_shipmode = st.selectbox("SELECT SHIP MODE",
                                   sorted(orders['Ship Mode'].unique()))

    st.markdown("""
    <div style="background:rgba(201,168,76,0.1);border:1px solid #c9a84c;
                border-left:4px solid #c9a84c;border-radius:8px;
                padding:12px 16px;margin:16px 0;">
        <p style="color:#e8d5a3;font-size:13px;margin:0;">
            ℹ️ Ship Mode affects shipping cost but not factory distance.
            Distance-based recommendations remain consistent across all ship modes.
        </p>
    </div>
    """, unsafe_allow_html=True)

    current_factory = products[products['Product'] == wi_product]['Factory'].values
    current_factory = current_factory[0] if len(current_factory) > 0 else "Unknown"

    rec_row      = recommend[(recommend['Product'] == wi_product) &
                             (recommend['Region']  == wi_region)]
    rec_factory  = rec_row['Best Factory'].values[0]        if len(rec_row) > 0 else "Unknown"
    rec_distance = rec_row['Distance (km)'].values[0]       if len(rec_row) > 0 else 0
    rec_leadtime = rec_row['Predicted Lead Time'].values[0]  if len(rec_row) > 0 else 0

    cur_row      = simulation[(simulation['Product'] == wi_product) &
                              (simulation['Region']  == wi_region) &
                              (simulation['Factory'] == current_factory)]
    cur_distance = cur_row['Distance (km)'].values[0]       if len(cur_row) > 0 else 0
    cur_leadtime = cur_row['Predicted Lead Time'].values[0]  if len(cur_row) > 0 else 0

    dist_improvement = cur_distance - rec_distance
    lead_improvement = cur_leadtime - rec_leadtime

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("SCENARIO", "Current vs Recommended Assignment")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#2d1515 0%,#1a0f0f 100%);
                    border:1px solid #e74c3c;border-top:3px solid #e74c3c;
                    border-radius:14px;padding:28px;">
            <p style="color:#e74c3c;font-size:10px;letter-spacing:3px;margin-bottom:16px;">
                CURRENT ASSIGNMENT</p>
            <div style="margin-bottom:16px;">
                <p style="color:#a0b4c8;font-size:11px;margin:0 0 4px 0;">FACTORY</p>
                <p style="color:#ffffff;font-size:22px;font-weight:700;
                          font-family:Georgia,serif;margin:0;">{current_factory}</p>
            </div>
            <div style="margin-bottom:16px;">
                <p style="color:#a0b4c8;font-size:11px;margin:0 0 4px 0;">DISTANCE</p>
                <p style="color:#e74c3c;font-size:28px;font-weight:700;margin:0;">
                    {cur_distance} km</p>
            </div>
            <div>
                <p style="color:#a0b4c8;font-size:11px;margin:0 0 4px 0;">LEAD TIME</p>
                <p style="color:#e74c3c;font-size:28px;font-weight:700;margin:0;">
                    {cur_leadtime:.0f} days</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0d2d1a 0%,#0a1f12 100%);
                    border:1px solid #2ecc71;border-top:3px solid #2ecc71;
                    border-radius:14px;padding:28px;">
            <p style="color:#2ecc71;font-size:10px;letter-spacing:3px;margin-bottom:16px;">
                RECOMMENDED ASSIGNMENT</p>
            <div style="margin-bottom:16px;">
                <p style="color:#a0b4c8;font-size:11px;margin:0 0 4px 0;">FACTORY</p>
                <p style="color:#ffffff;font-size:22px;font-weight:700;
                          font-family:Georgia,serif;margin:0;">{rec_factory}</p>
            </div>
            <div style="margin-bottom:16px;">
                <p style="color:#a0b4c8;font-size:11px;margin:0 0 4px 0;">DISTANCE</p>
                <p style="color:#2ecc71;font-size:28px;font-weight:700;margin:0;">
                    {rec_distance} km
                    <span style="font-size:14px;color:#a0b4c8;">
                        ↓ {dist_improvement} km saved</span></p>
            </div>
            <div>
                <p style="color:#a0b4c8;font-size:11px;margin:0 0 4px 0;">LEAD TIME</p>
                <p style="color:#2ecc71;font-size:28px;font-weight:700;margin:0;">
                    {rec_leadtime:.0f} days
                    <span style="font-size:14px;color:#a0b4c8;">
                        ↓ {lead_improvement:.0f}d saved</span></p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("VISUALIZATION", "Side-by-Side Comparison")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, vals, title, ylabel in [
        (axes[0], [cur_distance, rec_distance],
         "Distance Comparison (km)", "Distance (km)"),
        (axes[1], [cur_leadtime, rec_leadtime],
         "Lead Time Comparison (days)", "Lead Time (days)")
    ]:
        bars = ax.bar(["Current", "Recommended"], vals,
                      color=['#e74c3c', '#2ecc71'],
                      edgecolor='#0f2040', linewidth=0.5, width=0.5)
        ax.set_title(title, color='#c9a84c', fontsize=12)
        ax.set_ylabel(ylabel)
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + (max(vals) * 0.01),
                    f'{bar.get_height():.0f}',
                    ha='center', va='bottom', fontsize=11,
                    color='#e8d5a3', fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ══════════════════════════════════════════════════════════════
# PAGE 5 — RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════
elif page == "🏆 Recommendations":
    page_header("Recommendations",
                "Optimal factory assignments for every product and region", "🏆")

    col1, col2 = st.columns(2)
    with col1:
        filter_region  = st.selectbox("FILTER BY REGION",
                                      ["All"] + list(recommend['Region'].unique()))
    with col2:
        filter_product = st.selectbox("FILTER BY PRODUCT",
                                      ["All"] + sorted(recommend['Product'].unique()))

    filtered_rec = recommend.copy()
    if filter_region  != "All":
        filtered_rec = filtered_rec[filtered_rec['Region']  == filter_region]
    if filter_product != "All":
        filtered_rec = filtered_rec[filtered_rec['Product'] == filter_product]

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    metric_card(col1, "📋", "RECOMMENDATIONS", str(len(filtered_rec)),
                "total results", "#c9a84c")
    metric_card(col2, "📍", "AVG DISTANCE",
                f"{filtered_rec['Distance (km)'].mean():.0f} km",
                "average", "#3498db")
    metric_card(col3, "⏱", "AVG LEAD TIME",
                f"{filtered_rec['Predicted Lead Time'].mean():.0f}d",
                "estimated", "#2ecc71")

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("ANALYSIS", "Most Recommended Factories")

    factory_counts = filtered_rec['Best Factory'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 4))
    colors_rec = ['#c9a84c','#3498db','#2ecc71','#e74c3c','#8172B2']
    bars = ax.bar(factory_counts.index, factory_counts.values,
                  color=colors_rec[:len(factory_counts)],
                  edgecolor='#0f2040', linewidth=0.5)
    ax.set_xlabel("Factory")
    ax.set_ylabel("Number of Recommendations")
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.1,
                str(int(bar.get_height())),
                ha='center', va='bottom',
                fontsize=11, color='#e8d5a3', fontweight='bold')
    plt.xticks(rotation=15)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("DATA", "Full Recommendations Table")
    st.dataframe(filtered_rec.reset_index(drop=True),
                 use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    csv = filtered_rec.to_csv(index=False)
    st.download_button(
        label="⬇️ Download Recommendations as CSV",
        data=csv,
        file_name="nassau_candy_recommendations.csv",
        mime="text/csv"
    )

# ══════════════════════════════════════════════════════════════
# PAGE 6 — RISK & IMPACT
# ══════════════════════════════════════════════════════════════
elif page == "⚠️ Risk & Impact":
    page_header("Risk & Impact Panel",
                "Profit impact alerts and high-risk reassignment warnings", "⚠️")

    total_sales   = orders['Sales'].sum()
    total_profit  = orders['Gross Profit'].sum()
    total_cost    = orders['Cost'].sum()
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    metric_card(col1, "💰", "TOTAL SALES",   f"${total_sales:,.0f}",  "revenue",       "#2ecc71")
    metric_card(col2, "📈", "GROSS PROFIT",  f"${total_profit:,.0f}", "after costs",   "#c9a84c")
    metric_card(col3, "🎯", "PROFIT MARGIN", f"{profit_margin:.1f}%", "overall",       "#3498db")
    metric_card(col4, "💸", "TOTAL COST",    f"${total_cost:,.0f}",   "manufacturing", "#e74c3c")

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("FINANCIALS", "Profit by Division")
    div_profit = orders.groupby('Division')[['Sales','Gross Profit','Cost']].sum()
    st.dataframe(div_profit, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("ALERTS", "Risk Flags")
    high_risk = recommend[recommend['Distance (km)'] > 2000]
    if len(high_risk) > 0:
        st.markdown(f"""
        <div style="background:rgba(231,76,60,0.1);border:1px solid #e74c3c;
                    border-left:4px solid #e74c3c;border-radius:8px;
                    padding:12px 16px;margin-bottom:16px;">
            <p style="color:#e74c3c;font-size:13px;margin:0;font-weight:600;">
                ⚠️ {len(high_risk)} product-region combinations have distances
                over 2,000 km — consider urgent reassignment
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(high_risk, use_container_width=True, hide_index=True)
    else:
        st.markdown("""
        <div style="background:rgba(46,204,113,0.1);border:1px solid #2ecc71;
                    border-left:4px solid #2ecc71;border-radius:8px;
                    padding:12px 16px;">
            <p style="color:#2ecc71;font-size:13px;margin:0;font-weight:600;">
                ✅ No high distance risk flags found — all assignments within safe range
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("MODELS", "ML Model Performance")
    st.dataframe(model_result, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("ANALYSIS", "Gross Profit by Product")
    prod_profit = orders.groupby('Product Name')[['Sales','Gross Profit']].sum()
    prod_profit = prod_profit.sort_values('Gross Profit', ascending=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    colors_prod = ['#c9a84c' if v == prod_profit['Gross Profit'].max()
                   else '#2c3e6b' for v in prod_profit['Gross Profit']]
    bars = ax.barh(prod_profit.index, prod_profit['Gross Profit'],
                   color=colors_prod, edgecolor='#0f2040', linewidth=0.5)
    ax.set_xlabel("Gross Profit ($)")
    for bar in bars:
        ax.text(bar.get_width() + 100,
                bar.get_y() + bar.get_height()/2,
                f'${bar.get_width():,.0f}',
                va='center', fontsize=9, color='#e8d5a3')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()