import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pickle
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StockOracle Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: #06141B;
    --bg-secondary: #0a1e2c;
    --bg-card: #0d2137;
    --bg-card-hover: #112845;
    --accent-gold: #F5B700;
    --accent-green: #00FFB2;
    --accent-red: #FF4D6D;
    --accent-cyan: #00D9FF;
    --accent-purple: #7B61FF;
    --text-primary: #EAFBFF;
    --text-secondary: #7aa5be;
    --border: rgba(0, 217, 255, 0.15);
    --glow-cyan: rgba(0, 217, 255, 0.3);
    --glow-green: rgba(0, 255, 178, 0.3);
}

/* Cyber grid background */
.stApp {
    background-color: #06141B;
    background-image:
        linear-gradient(rgba(0,217,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,217,255,0.03) 1px, transparent 1px),
        radial-gradient(ellipse at 20% 20%, rgba(0,217,255,0.06) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 80%, rgba(123,97,255,0.06) 0%, transparent 60%);
    background-size: 40px 40px, 40px 40px, 100% 100%, 100% 100%;
    font-family: 'Inter', sans-serif;
    color: var(--text-primary);
}

.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 100%;
}

/* Glassmorphism sidebar */
section[data-testid="stSidebar"] {
    background: rgba(6, 20, 27, 0.7) !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-right: 1px solid rgba(0,217,255,0.12);
    box-shadow: 4px 0 30px rgba(0,217,255,0.05);
}
section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1rem;
}

/* Hero header */
.hero-header {
    background: rgba(13, 33, 55, 0.6);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(0,217,255,0.2);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 40px rgba(0,217,255,0.08), inset 0 1px 0 rgba(255,255,255,0.05);
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%; right: -10%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(0,217,255,0.07) 0%, transparent 70%);
    pointer-events: none;
}
.hero-header::after {
    content: '';
    position: absolute;
    bottom: -30%; left: -5%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(123,97,255,0.05) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 2.8rem;
    font-weight: 900;
    font-family: 'Orbitron', sans-serif;
    background: linear-gradient(135deg, #00D9FF 0%, #00FFB2 50%, #F5B700 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    letter-spacing: 2px;
    text-shadow: none;
    filter: drop-shadow(0 0 20px rgba(0,217,255,0.3));
}
.hero-sub {
    color: var(--text-secondary);
    font-size: 1rem;
    margin-top: 0.4rem;
    font-weight: 400;
    letter-spacing: 0.5px;
}

/* Glassmorphism metric cards */
.metric-card {
    background: rgba(13, 33, 55, 0.5);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(0,217,255,0.15);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.04);
}
.metric-card:hover {
    border-color: rgba(0,217,255,0.4);
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(0,217,255,0.15), inset 0 1px 0 rgba(255,255,255,0.06);
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,217,255,0.6), rgba(0,255,178,0.4), transparent);
}
.metric-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin-bottom: 0.4rem;
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--text-primary);
    font-family: 'JetBrains Mono', monospace;
    text-shadow: 0 0 20px rgba(0,217,255,0.2);
}
.metric-delta-pos { color: var(--accent-green); font-size: 0.85rem; font-weight: 500; text-shadow: 0 0 10px rgba(0,255,178,0.4); }
.metric-delta-neg { color: var(--accent-red); font-size: 0.85rem; font-weight: 500; }

/* Section headers */
.section-header {
    font-size: 1rem;
    font-weight: 700;
    font-family: 'Orbitron', sans-serif;
    color: var(--accent-cyan);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(0,217,255,0.15);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    text-shadow: 0 0 15px rgba(0,217,255,0.4);
}

/* Prediction box */
.prediction-box {
    background: rgba(0, 255, 178, 0.04);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(0,255,178,0.25);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    margin: 1rem 0;
    box-shadow: 0 0 40px rgba(0,255,178,0.08), inset 0 1px 0 rgba(0,255,178,0.1);
}
.pred-label { font-size: 0.75rem; letter-spacing: 3px; text-transform: uppercase; color: var(--accent-green); font-weight: 600; font-family: 'Orbitron', sans-serif; }
.pred-price { font-size: 3.5rem; font-weight: 900; color: var(--accent-green); font-family: 'JetBrains Mono', monospace; margin: 0.3rem 0; text-shadow: 0 0 30px rgba(0,255,178,0.5); }
.pred-sub { font-size: 0.85rem; color: var(--text-secondary); }

/* Insight cards */
.insight-card {
    background: rgba(13, 33, 55, 0.5);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(0,217,255,0.12);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    transition: border-color 0.2s;
}
.insight-card:hover { border-color: rgba(0,217,255,0.3); }

/* Streamlit overrides */
.stSelectbox > div > div, .stNumberInput > div > div > input, .stTextInput > div > div > input {
    background: rgba(13,33,55,0.7) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(0,217,255,0.2) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
}
.stSlider > div > div > div { background: var(--accent-cyan) !important; }

/* Gradient glow button */
.stButton > button {
    background: linear-gradient(135deg, #00D9FF 0%, #00FFB2 100%) !important;
    color: #06141B !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-family: 'Orbitron', sans-serif !important;
    letter-spacing: 1px !important;
    padding: 0.6rem 2rem !important;
    transition: all 0.3s !important;
    width: 100% !important;
    box-shadow: 0 4px 20px rgba(0,217,255,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(0,217,255,0.5), 0 0 60px rgba(0,255,178,0.2) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(13,33,55,0.6) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid rgba(0,217,255,0.1) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0,217,255,0.2), rgba(0,255,178,0.15)) !important;
    color: var(--accent-cyan) !important;
    box-shadow: 0 0 15px rgba(0,217,255,0.2) !important;
}

div[data-testid="metric-container"] {
    background: rgba(13,33,55,0.5);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(0,217,255,0.12);
    border-radius: 12px;
    padding: 1rem;
}
.stDataFrame { border-radius: 12px; overflow: hidden; }
hr { border-color: rgba(0,217,255,0.1) !important; }

/* Badges */
.badge {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    font-family: 'Orbitron', sans-serif;
}
.badge-bull { background: rgba(0,255,178,0.1); color: var(--accent-green); border: 1px solid rgba(0,255,178,0.3); box-shadow: 0 0 10px rgba(0,255,178,0.15); }
.badge-bear { background: rgba(255,77,109,0.1); color: var(--accent-red); border: 1px solid rgba(255,77,109,0.3); }
.badge-neutral { background: rgba(245,183,0,0.1); color: var(--accent-gold); border: 1px solid rgba(245,183,0,0.3); }

.ticker-bar {
    background: rgba(13,33,55,0.6);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(0,217,255,0.12);
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--text-secondary);
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── MODEL LOADING ──────────────────────────────────────────────────────────────
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))



@st.cache_resource
def load_models():
    try:
        with open(os.path.join(BASE_DIR, "columns.pkl"), "rb") as f:
            columns = pickle.load(f)
        with open(os.path.join(BASE_DIR, "scaler.pkl"), "rb") as f:
            scaler = pickle.load(f)
        with open(os.path.join(BASE_DIR, "Linear_Regression_StockPrice_Prediction.pkl"), "rb") as f:
            model = pickle.load(f)
        return model, scaler, columns, True
    except Exception as e:
        
        return None, None, None, False

model, scaler, columns, model_loaded = load_models()

# ─── DATA FETCHING ──────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch_stock(ticker, period="1y"):
    try:
        tk = yf.Ticker(ticker)
        df = tk.history(period=period)
        info = tk.info
        return df, info
    except:
        return pd.DataFrame(), {}

def compute_technicals(df):
    if df.empty:
        return df
    df = df.copy()
    # Moving Averages
    df["SMA_20"] = df["Close"].rolling(20).mean()
    df["SMA_50"] = df["Close"].rolling(50).mean()
    df["SMA_200"] = df["Close"].rolling(200).mean()
    df["EMA_12"] = df["Close"].ewm(span=12, adjust=False).mean()
    df["EMA_26"] = df["Close"].ewm(span=26, adjust=False).mean()
    # MACD
    df["MACD"] = df["EMA_12"] - df["EMA_26"]
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_Hist"] = df["MACD"] - df["Signal"]
    # RSI
    delta = df["Close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / (loss + 1e-9)
    df["RSI"] = 100 - 100 / (1 + rs)
    # Bollinger Bands
    df["BB_Mid"] = df["Close"].rolling(20).mean()
    bb_std = df["Close"].rolling(20).std()
    df["BB_Upper"] = df["BB_Mid"] + 2 * bb_std
    df["BB_Lower"] = df["BB_Mid"] - 2 * bb_std
    # Stochastic
    low14 = df["Low"].rolling(14).min()
    high14 = df["High"].rolling(14).max()
    df["Stoch_K"] = 100 * (df["Close"] - low14) / (high14 - low14 + 1e-9)
    df["Stoch_D"] = df["Stoch_K"].rolling(3).mean()
    # ATR
    df["ATR"] = pd.concat([
        df["High"] - df["Low"],
        (df["High"] - df["Close"].shift()).abs(),
        (df["Low"] - df["Close"].shift()).abs()
    ], axis=1).max(axis=1).rolling(14).mean()
    # Volume indicators
    df["Vol_SMA"] = df["Volume"].rolling(20).mean()
    df["Returns"] = df["Close"].pct_change()
    df["Volatility"] = df["Returns"].rolling(20).std() * np.sqrt(252)
    return df

# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; margin-bottom:1.5rem;">
        <div style="font-size:2.2rem;">📈</div>
        <div style="font-size:1.3rem; font-weight:800; background:linear-gradient(135deg,#00b4d8,#7b2ff7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">StockOracle Pro</div>
        <div style="font-size:0.7rem;color:#8ba7c7;letter-spacing:2px;text-transform:uppercase;">AI-Powered Analytics</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">🔍 Stock Selection</div>', unsafe_allow_html=True)

    POPULAR = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "NFLX",
               "AMD", "INTC", "JPM", "GS", "BAC", "WMT", "TGT", "RELIANCE.NS",
               "TCS.NS", "INFY.NS", "HDFCBANK.NS", "WIPRO.NS"]
    ticker_input = st.selectbox("Select Ticker", POPULAR, index=0)
    custom_ticker = st.text_input("Or enter custom ticker", placeholder="e.g. BABA, SHOP...")
    ticker = custom_ticker.upper().strip() if custom_ticker.strip() else ticker_input

    period_map = {"1 Month": "1mo", "3 Months": "3mo", "6 Months": "6mo",
                  "1 Year": "1y", "2 Years": "2y", "5 Years": "5y"}
    period_label = st.selectbox("Time Period", list(period_map.keys()), index=3)
    period = period_map[period_label]

    st.markdown("---")
    st.markdown('<div class="section-header">🤖 ML Prediction</div>', unsafe_allow_html=True)

    if model_loaded:
        st.success("✅ Model Loaded")
        st.markdown(f"<div style='font-size:0.75rem;color:#8ba7c7;'>Features: {len(columns) if columns else 'N/A'}</div>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Place pkl files in same directory")

    st.markdown("---")
    st.markdown('<div class="section-header">⚙️ Chart Settings</div>', unsafe_allow_html=True)
    chart_theme = st.selectbox("Theme", ["Dark (Default)", "Midnight Blue", "Deep Purple"])
    show_volume = st.toggle("Show Volume", True)
    show_bb = st.toggle("Bollinger Bands", True)
    show_sma = st.toggle("Moving Averages", True)

    st.markdown("---")
    run_btn = st.button("🚀 Analyze Stock", use_container_width=True)

# ─── INIT SESSION STATE ─────────────────────────────────────────────────────────
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()
if "info" not in st.session_state:
    st.session_state.info = {}
if "ticker" not in st.session_state:
    st.session_state.ticker = "AAPL"

if run_btn:
    with st.spinner(f"Fetching {ticker} data..."):
        df_raw, info = fetch_stock(ticker, period)
        if not df_raw.empty:
            st.session_state.df = compute_technicals(df_raw)
            st.session_state.info = info
            st.session_state.ticker = ticker
            st.session_state.analyzed = True
        else:
            st.error(f"Could not fetch data for {ticker}. Check ticker symbol.")

# ─── HERO HEADER ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
        <div>
            <div class="hero-title">StockOracle Pro 📊</div>
            <div class="hero-sub">AI-Powered Stock Price Prediction & Market Intelligence Platform</div>
        </div>
        <div style="text-align:right;">
            <div style="font-size:0.7rem;letter-spacing:2px;text-transform:uppercase;color:#8ba7c7;">POWERED BY</div>
            <div style="font-size:0.95rem;font-weight:700;color:#00b4d8;">Linear Regression ML Model</div>
            <div style="font-size:0.7rem;color:#8ba7c7;">+ Real-time Yahoo Finance Data</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── MAIN CONTENT ───────────────────────────────────────────────────────────────
if not st.session_state.analyzed:
    # Landing state
    st.markdown("""
    <div style="text-align:center;padding:3rem;background:rgba(13,31,60,0.5);border:1px solid rgba(0,180,216,0.1);border-radius:20px;">
        <div style="font-size:4rem;margin-bottom:1rem;">🔮</div>
        <div style="font-size:1.5rem;font-weight:700;color:#e8f4f8;margin-bottom:0.5rem;">Select a Stock & Click Analyze</div>
        <div style="color:#8ba7c7;max-width:500px;margin:0 auto;line-height:1.6;">
            Choose any ticker from the sidebar, set your time period, and unlock professional-grade 
            analytics powered by machine learning and real-time market data.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Feature showcase
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    features = [
        ("📊", "3D Price Surface", "Interactive 3D volatility & price landscape"),
        ("🤖", "ML Predictions", "Linear regression price forecasting"),
        ("📉", "Technical Analysis", "RSI, MACD, Bollinger Bands & more"),
        ("🌐", "Live Market Data", "Real-time Yahoo Finance integration"),
    ]
    for col, (icon, title, desc) in zip([c1,c2,c3,c4], features):
        col.markdown(f"""
        <div class="metric-card" style="text-align:center;padding:1.5rem 1rem;">
            <div style="font-size:2rem;margin-bottom:0.5rem;">{icon}</div>
            <div style="font-weight:700;font-size:0.95rem;color:#e8f4f8;margin-bottom:0.3rem;">{title}</div>
            <div style="font-size:0.78rem;color:#8ba7c7;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

else:
    df = st.session_state.df
    info = st.session_state.info
    tkr = st.session_state.ticker

    # ── KPI METRICS ────────────────────────────────────────────────────────────
    last = df["Close"].iloc[-1]
    prev = df["Close"].iloc[-2]
    chg = last - prev
    chg_pct = chg / prev * 100
    high52 = df["Close"].rolling(min(252, len(df))).max().iloc[-1]
    low52 = df["Close"].rolling(min(252, len(df))).min().iloc[-1]
    avg_vol = df["Volume"].mean()
    current_vol = df["Volume"].iloc[-1]
    vol_ratio = current_vol / avg_vol if avg_vol > 0 else 1
    rsi_val = df["RSI"].iloc[-1] if "RSI" in df.columns and not np.isnan(df["RSI"].iloc[-1]) else 50
    atr_val = df["ATR"].iloc[-1] if "ATR" in df.columns and not np.isnan(df["ATR"].iloc[-1]) else 0
    
    name = info.get("longName", tkr)
    sector = info.get("sector", "—")
    market_cap = info.get("marketCap", 0)
    cap_str = f"${market_cap/1e9:.1f}B" if market_cap >= 1e9 else f"${market_cap/1e6:.0f}M" if market_cap else "—"
    
    chg_class = "metric-delta-pos" if chg >= 0 else "metric-delta-neg"
    chg_arrow = "▲" if chg >= 0 else "▼"
    
    # Sentiment badge
    if rsi_val > 70:
        sentiment = "OVERBOUGHT"; badge_cls = "badge-bear"
    elif rsi_val < 30:
        sentiment = "OVERSOLD"; badge_cls = "badge-bull"
    elif chg_pct > 1:
        sentiment = "BULLISH"; badge_cls = "badge-bull"
    elif chg_pct < -1:
        sentiment = "BEARISH"; badge_cls = "badge-bear"
    else:
        sentiment = "NEUTRAL"; badge_cls = "badge-neutral"

    # Top info row
    col_info1, col_info2 = st.columns([3,1])
    with col_info1:
        st.markdown(f"""
        <div style="margin-bottom:1rem;">
            <div style="display:flex;align-items:center;gap:1rem;flex-wrap:wrap;">
                <span style="font-size:2rem;font-weight:900;color:#e8f4f8;">{tkr}</span>
                <span style="font-size:1rem;color:#8ba7c7;">{name}</span>
                <span class="badge {badge_cls}">{sentiment}</span>
                <span style="font-size:0.8rem;color:#8ba7c7;">📌 {sector}</span>
                <span style="font-size:0.8rem;color:#8ba7c7;">💰 {cap_str}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # KPI cards
    k1,k2,k3,k4,k5,k6 = st.columns(6)
    kpis = [
        ("LAST PRICE", f"${last:.2f}", f"{chg_arrow} {abs(chg):.2f} ({abs(chg_pct):.2f}%)", chg >= 0),
        ("52W HIGH", f"${high52:.2f}", f"{((last/high52-1)*100):.1f}% from high", None),
        ("52W LOW", f"${low52:.2f}", f"{((last/low52-1)*100):+.1f}% from low", None),
        ("RSI (14)", f"{rsi_val:.1f}", "Overbought >70 / Oversold <30", None),
        ("ATR", f"${atr_val:.2f}", "Average True Range (14)", None),
        ("VOL RATIO", f"{vol_ratio:.2f}x", "Current vs 20D Avg Volume", vol_ratio > 1),
    ]
    for col, (label, val, sub, positive) in zip([k1,k2,k3,k4,k5,k6], kpis):
        if positive is True:
            delta_cls = "metric-delta-pos"
        elif positive is False:
            delta_cls = "metric-delta-neg"
        else:
            delta_cls = "metric-delta-pos" if "+" in sub or ("from low" in sub) else "metric-delta-neg" if ("-" in sub and "from high" not in sub) else ""

        col.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="font-size:1.3rem;">{val}</div>
            <div class="{delta_cls}" style="font-size:0.72rem;margin-top:0.2rem;">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── TABS ───────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊  Price Chart", "🤖  ML Prediction", "📉  Technical Analysis",
        "🌋  3D Visualizations", "📋  Data & Statistics"
    ])

    # ─── TAB 1: PRICE CHART ────────────────────────────────────────────────────
    with tab1:
        fig = make_subplots(
            rows=2, cols=1,
            row_heights=[0.75, 0.25],
            shared_xaxes=True,
            vertical_spacing=0.03,
        )
        # Candlestick
        fig.add_trace(go.Candlestick(
            x=df.index, open=df["Open"], high=df["High"],
            low=df["Low"], close=df["Close"],
            name="OHLC",
            increasing=dict(line=dict(color="#00d4aa"), fillcolor="rgba(0,212,170,0.7)"),
            decreasing=dict(line=dict(color="#ff4757"), fillcolor="rgba(255,71,87,0.7)"),
        ), row=1, col=1)

        # MAs
        if show_sma and "SMA_20" in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df["SMA_20"], name="SMA 20",
                line=dict(color="#f5a623", width=1.5), opacity=0.85), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df["SMA_50"], name="SMA 50",
                line=dict(color="#00b4d8", width=1.5), opacity=0.85), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df["SMA_200"], name="SMA 200",
                line=dict(color="#7b2ff7", width=1.5, dash="dot"), opacity=0.85), row=1, col=1)

        # Bollinger Bands
        if show_bb and "BB_Upper" in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df["BB_Upper"], name="BB Upper",
                line=dict(color="rgba(0,180,216,0.4)", width=1, dash="dash"),
                fill=None), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df["BB_Lower"], name="BB Lower",
                line=dict(color="rgba(0,180,216,0.4)", width=1, dash="dash"),
                fill="tonexty", fillcolor="rgba(0,180,216,0.04)"), row=1, col=1)

        # Volume
        if show_volume:
            colors = ["rgba(0,212,170,0.6)" if c >= o else "rgba(255,71,87,0.6)"
                      for c, o in zip(df["Close"], df["Open"])]
            fig.add_trace(go.Bar(x=df.index, y=df["Volume"], name="Volume",
                marker_color=colors, showlegend=False), row=2, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df["Vol_SMA"], name="Vol SMA20",
                line=dict(color="#f5a623", width=1.5), showlegend=False), row=2, col=1)

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(5,11,24,0.8)",
            font=dict(family="Inter, sans-serif", color="#8ba7c7"),
            xaxis_rangeslider_visible=False,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                       bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
            margin=dict(l=10, r=10, t=30, b=10),
            height=600,
            xaxis=dict(gridcolor="rgba(0,180,216,0.06)", showgrid=True),
            yaxis=dict(gridcolor="rgba(0,180,216,0.06)", showgrid=True,
                      tickprefix="$", tickformat=".2f"),
            yaxis2=dict(gridcolor="rgba(0,180,216,0.06)", showgrid=True),
            title=dict(text=f"<b>{tkr}</b> Price Chart — {period_label}",
                      font=dict(size=16, color="#e8f4f8"), x=0.01),
        )
        fig.update_xaxes(showspikes=True, spikecolor="#00b4d8", spikethickness=1)
        fig.update_yaxes(showspikes=True, spikecolor="#00b4d8", spikethickness=1)
        st.plotly_chart(fig, use_container_width=True)

    # ─── TAB 2: ML PREDICTION ──────────────────────────────────────────────────
    with tab2:
        col_pred, col_input = st.columns([1.2, 1])
        with col_input:
            st.markdown('<div class="section-header">🎛️ Input Features</div>', unsafe_allow_html=True)

            if model_loaded and columns is not None:
                inputs = {}
                with st.form("prediction_form"):
                    for col_name in columns:
                        if "open" in col_name.lower() or "Open" in col_name:
                            default_val = float(df["Open"].iloc[-1]) if not df.empty else 100.0
                        elif "high" in col_name.lower():
                            default_val = float(df["High"].iloc[-1]) if not df.empty else 105.0
                        elif "low" in col_name.lower():
                            default_val = float(df["Low"].iloc[-1]) if not df.empty else 95.0
                        elif "volume" in col_name.lower():
                            default_val = float(df["Volume"].iloc[-1]) if not df.empty else 1000000.0
                        elif "rsi" in col_name.lower():
                            default_val = float(rsi_val)
                        else:
                            default_val = float(df["Close"].iloc[-1]) if not df.empty else 100.0
                        inputs[col_name] = st.number_input(
                            f"{col_name}", value=round(default_val, 4),
                            format="%.4f", key=col_name
                        )
                    predict_btn = st.form_submit_button("🔮 Predict Price", use_container_width=True)
            else:
                st.markdown("""
                <div class="insight-card">
                    <div style="font-weight:600;color:#f5a623;margin-bottom:0.4rem;">Manual Input Mode</div>
                    <div style="font-size:0.82rem;color:#8ba7c7;">Place columns.pkl, scaler.pkl, and model.pkl in the same directory to enable ML predictions with your trained model.</div>
                </div>
                """, unsafe_allow_html=True)

                with st.form("manual_pred_form"):
                    open_p = st.number_input("Open Price ($)", value=float(df["Open"].iloc[-1]) if not df.empty else 100.0, format="%.2f")
                    high_p = st.number_input("High Price ($)", value=float(df["High"].iloc[-1]) if not df.empty else 105.0, format="%.2f")
                    low_p = st.number_input("Low Price ($)", value=float(df["Low"].iloc[-1]) if not df.empty else 95.0, format="%.2f")
                    vol_p = st.number_input("Volume", value=float(df["Volume"].iloc[-1]) if not df.empty else 1000000.0, format="%.0f")
                    predict_btn = st.form_submit_button("🔮 Predict Price", use_container_width=True)

        with col_pred:
            st.markdown('<div class="section-header">🎯 Prediction Result</div>', unsafe_allow_html=True)

            if "predict_btn" in dir() and predict_btn:
                if model_loaded and columns is not None:
                    try:
                        feat_arr = np.array([[inputs[c] for c in columns]])
                        feat_scaled = scaler.transform(feat_arr)
                        predicted = model.predict(feat_scaled)[0]
                        actual = df["Close"].iloc[-1]
                        diff = predicted - actual
                        diff_pct = diff / actual * 100
                        col_class = "#00d4aa" if diff >= 0 else "#ff4757"

                        st.markdown(f"""
                        <div class="prediction-box">
                            <div class="pred-label">ML Predicted Price</div>
                            <div class="pred-price" style="color:{col_class};">${predicted:.2f}</div>
                            <div class="pred-sub">Current: ${actual:.2f} &nbsp;|&nbsp; 
                            <span style="color:{col_class};">{"▲" if diff>=0 else "▼"} {abs(diff):.2f} ({abs(diff_pct):.2f}%)</span></div>
                        </div>
                        """, unsafe_allow_html=True)

                        # Gauge
                        conf = min(100, max(0, 100 - abs(diff_pct) * 5))
                        fig_gauge = go.Figure(go.Indicator(
                            mode="gauge+number+delta",
                            value=predicted,
                            delta={"reference": actual, "prefix": "$", "valueformat": ".2f"},
                            title={"text": "Predicted vs Actual", "font": {"color": "#8ba7c7", "size": 13}},
                            number={"prefix": "$", "valueformat": ".2f", "font": {"color": "#e8f4f8", "size": 28}},
                            gauge={
                                "axis": {"range": [actual * 0.85, actual * 1.15], "tickcolor": "#8ba7c7"},
                                "bar": {"color": col_class},
                                "bgcolor": "rgba(13,31,60,0.8)",
                                "bordercolor": "rgba(0,180,216,0.2)",
                                "steps": [
                                    {"range": [actual * 0.85, actual * 0.95], "color": "rgba(255,71,87,0.15)"},
                                    {"range": [actual * 0.95, actual * 1.05], "color": "rgba(245,166,35,0.1)"},
                                    {"range": [actual * 1.05, actual * 1.15], "color": "rgba(0,212,170,0.15)"},
                                ],
                                "threshold": {"line": {"color": "#f5a623", "width": 3}, "thickness": 0.8, "value": actual},
                            },
                        ))
                        fig_gauge.update_layout(
                            paper_bgcolor="rgba(0,0,0,0)",
                            font=dict(family="Inter", color="#8ba7c7"),
                            height=260, margin=dict(l=20,r=20,t=30,b=20),
                        )
                        st.plotly_chart(fig_gauge, use_container_width=True)
                    except Exception as e:
                        st.error(f"Prediction error: {e}")
                else:
                    # Fallback linear estimate
                    est = (open_p + high_p + low_p) / 3 * 1.001
                    st.markdown(f"""
                    <div class="prediction-box">
                        <div class="pred-label">Estimated Price (VWAP)</div>
                        <div class="pred-price">${est:.2f}</div>
                        <div class="pred-sub">Based on OHLC pivot — load pkl files for ML prediction</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align:center;padding:3rem;opacity:0.5;">
                    <div style="font-size:3rem;">🔮</div>
                    <div style="font-size:1rem;color:#8ba7c7;margin-top:0.5rem;">Fill inputs & click Predict</div>
                </div>
                """, unsafe_allow_html=True)

            # Model info card
            st.markdown("""
            <div class="insight-card">
                <div style="font-size:0.75rem;font-weight:700;color:#00b4d8;letter-spacing:1px;text-transform:uppercase;margin-bottom:0.5rem;">Model Architecture</div>
                <div style="font-size:0.82rem;color:#8ba7c7;line-height:1.6;">
                    <b style="color:#e8f4f8;">Algorithm:</b> Linear Regression<br>
                    <b style="color:#e8f4f8;">Scaling:</b> StandardScaler (z-score normalization)<br>
                    <b style="color:#e8f4f8;">Features:</b> OHLCV + Technical Indicators<br>
                    <b style="color:#e8f4f8;">Framework:</b> scikit-learn
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Prediction horizon chart
        st.markdown("---")
        st.markdown('<div class="section-header">📅 Price Projection (Monte Carlo Simulation)</div>', unsafe_allow_html=True)

        last_price = df["Close"].iloc[-1]
        daily_ret = df["Returns"].dropna()
        mu = daily_ret.mean()
        sigma = daily_ret.std()
        n_days = 30
        n_sims = 200
        np.random.seed(42)
        
        fig_mc = go.Figure()
        sim_ends = []
        for i in range(n_sims):
            prices = [last_price]
            for _ in range(n_days):
                prices.append(prices[-1] * np.exp(mu + sigma * np.random.randn()))
            sim_ends.append(prices[-1])
            fig_mc.add_trace(go.Scatter(
                x=list(range(n_days + 1)), y=prices,
                mode="lines", line=dict(width=0.7, color="rgba(0,180,216,0.08)"),
                showlegend=False, hoverinfo="skip"
            ))
        
        # Percentile bands
        all_paths = []
        for _ in range(1000):
            prices = [last_price]
            for _ in range(n_days):
                prices.append(prices[-1] * np.exp(mu + sigma * np.random.randn()))
            all_paths.append(prices)
        all_paths = np.array(all_paths)
        p10 = np.percentile(all_paths, 10, axis=0)
        p50 = np.percentile(all_paths, 50, axis=0)
        p90 = np.percentile(all_paths, 90, axis=0)
        
        fig_mc.add_trace(go.Scatter(x=list(range(n_days+1)), y=p90, name="P90",
            line=dict(color="rgba(0,212,170,0.8)", width=2, dash="dash")))
        fig_mc.add_trace(go.Scatter(x=list(range(n_days+1)), y=p50, name="Median",
            line=dict(color="#f5a623", width=2.5),
            fill="tonexty", fillcolor="rgba(0,212,170,0.04)"))
        fig_mc.add_trace(go.Scatter(x=list(range(n_days+1)), y=p10, name="P10",
            line=dict(color="rgba(255,71,87,0.8)", width=2, dash="dash"),
            fill="tonexty", fillcolor="rgba(255,71,87,0.04)"))
        
        fig_mc.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(5,11,24,0.8)",
            title=dict(text=f"<b>30-Day Monte Carlo Simulation</b> ({n_sims} paths shown)",
                      font=dict(size=14, color="#e8f4f8"), x=0.01),
            xaxis=dict(title="Days Ahead", gridcolor="rgba(0,180,216,0.06)"),
            yaxis=dict(title="Price ($)", tickprefix="$", gridcolor="rgba(0,180,216,0.06)"),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
            height=350, margin=dict(l=10,r=10,t=40,b=10),
            font=dict(family="Inter", color="#8ba7c7"),
        )
        st.plotly_chart(fig_mc, use_container_width=True)
        
        mc1, mc2, mc3 = st.columns(3)
        mc1.markdown(f"""<div class="metric-card"><div class="metric-label">P10 Target (30D)</div><div class="metric-value" style="font-size:1.3rem;">${p10[-1]:.2f}</div><div class="metric-delta-neg">Bear case ({((p10[-1]/last_price-1)*100):+.1f}%)</div></div>""", unsafe_allow_html=True)
        mc2.markdown(f"""<div class="metric-card"><div class="metric-label">Median Target (30D)</div><div class="metric-value" style="font-size:1.3rem;">${p50[-1]:.2f}</div><div class="metric-delta-pos">Base case ({((p50[-1]/last_price-1)*100):+.1f}%)</div></div>""", unsafe_allow_html=True)
        mc3.markdown(f"""<div class="metric-card"><div class="metric-label">P90 Target (30D)</div><div class="metric-value" style="font-size:1.3rem;">${p90[-1]:.2f}</div><div class="metric-delta-pos">Bull case ({((p90[-1]/last_price-1)*100):+.1f}%)</div></div>""", unsafe_allow_html=True)

    # ─── TAB 3: TECHNICAL ANALYSIS ─────────────────────────────────────────────
    with tab3:
        # RSI
        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(x=df.index, y=df["RSI"], name="RSI",
            line=dict(color="#00b4d8", width=2),
            fill="tozeroy", fillcolor="rgba(0,180,216,0.05)"))
        fig_rsi.add_hline(y=70, line_dash="dash", line_color="rgba(255,71,87,0.5)", annotation_text="Overbought (70)")
        fig_rsi.add_hline(y=30, line_dash="dash", line_color="rgba(0,212,170,0.5)", annotation_text="Oversold (30)")
        fig_rsi.add_hline(y=50, line_dash="dot", line_color="rgba(245,166,35,0.3)")
        fig_rsi.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(5,11,24,0.8)",
            title=dict(text="<b>RSI — Relative Strength Index (14)</b>", font=dict(size=14, color="#e8f4f8"), x=0.01),
            yaxis=dict(range=[0,100], gridcolor="rgba(0,180,216,0.06)"),
            xaxis=dict(gridcolor="rgba(0,180,216,0.06)"),
            height=250, margin=dict(l=10,r=10,t=40,b=10),
            font=dict(family="Inter", color="#8ba7c7"),
        )
        st.plotly_chart(fig_rsi, use_container_width=True)

        # MACD
        fig_macd = make_subplots(rows=2, cols=1, row_heights=[0.6,0.4], shared_xaxes=True, vertical_spacing=0.04)
        fig_macd.add_trace(go.Scatter(x=df.index, y=df["MACD"], name="MACD",
            line=dict(color="#00b4d8", width=2)), row=1, col=1)
        fig_macd.add_trace(go.Scatter(x=df.index, y=df["Signal"], name="Signal",
            line=dict(color="#f5a623", width=2)), row=1, col=1)
        colors_hist = ["rgba(0,212,170,0.7)" if v >= 0 else "rgba(255,71,87,0.7)" for v in df["MACD_Hist"]]
        fig_macd.add_trace(go.Bar(x=df.index, y=df["MACD_Hist"], name="Histogram",
            marker_color=colors_hist), row=2, col=1)
        fig_macd.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(5,11,24,0.8)",
            title=dict(text="<b>MACD — Moving Average Convergence Divergence</b>", font=dict(size=14, color="#e8f4f8"), x=0.01),
            height=350, margin=dict(l=10,r=10,t=40,b=10),
            xaxis=dict(gridcolor="rgba(0,180,216,0.06)"),
            yaxis=dict(gridcolor="rgba(0,180,216,0.06)"),
            yaxis2=dict(gridcolor="rgba(0,180,216,0.06)"),
            font=dict(family="Inter", color="#8ba7c7"),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig_macd, use_container_width=True)

        # Stochastic
        col_stoch, col_atr = st.columns(2)
        with col_stoch:
            fig_stoch = go.Figure()
            fig_stoch.add_trace(go.Scatter(x=df.index, y=df["Stoch_K"], name="%K",
                line=dict(color="#7b2ff7", width=2)))
            fig_stoch.add_trace(go.Scatter(x=df.index, y=df["Stoch_D"], name="%D",
                line=dict(color="#f5a623", width=1.5, dash="dash")))
            fig_stoch.add_hline(y=80, line_dash="dash", line_color="rgba(255,71,87,0.4)")
            fig_stoch.add_hline(y=20, line_dash="dash", line_color="rgba(0,212,170,0.4)")
            fig_stoch.update_layout(
                template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(5,11,24,0.8)",
                title=dict(text="<b>Stochastic Oscillator</b>", font=dict(size=13, color="#e8f4f8"), x=0.01),
                yaxis=dict(range=[0,100], gridcolor="rgba(0,180,216,0.06)"),
                xaxis=dict(gridcolor="rgba(0,180,216,0.06)"),
                height=280, margin=dict(l=10,r=10,t=40,b=10),
                font=dict(family="Inter", color="#8ba7c7"),
                legend=dict(bgcolor="rgba(0,0,0,0)"),
            )
            st.plotly_chart(fig_stoch, use_container_width=True)

        with col_atr:
            fig_atr = go.Figure()
            fig_atr.add_trace(go.Scatter(x=df.index, y=df["ATR"], name="ATR (14)",
                line=dict(color="#00d4aa", width=2),
                fill="tozeroy", fillcolor="rgba(0,212,170,0.05)"))
            fig_atr.update_layout(
                template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(5,11,24,0.8)",
                title=dict(text="<b>ATR — Average True Range (14)</b>", font=dict(size=13, color="#e8f4f8"), x=0.01),
                yaxis=dict(tickprefix="$", gridcolor="rgba(0,180,216,0.06)"),
                xaxis=dict(gridcolor="rgba(0,180,216,0.06)"),
                height=280, margin=dict(l=10,r=10,t=40,b=10),
                font=dict(family="Inter", color="#8ba7c7"),
            )
            st.plotly_chart(fig_atr, use_container_width=True)

        # Rolling volatility
        fig_vol = go.Figure()
        fig_vol.add_trace(go.Scatter(x=df.index, y=df["Volatility"] * 100, name="Ann. Volatility",
            line=dict(color="#f5a623", width=2),
            fill="tozeroy", fillcolor="rgba(245,166,35,0.06)"))
        fig_vol.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(5,11,24,0.8)",
            title=dict(text="<b>Annualized Rolling Volatility (20-Day)</b>", font=dict(size=14, color="#e8f4f8"), x=0.01),
            yaxis=dict(ticksuffix="%", gridcolor="rgba(0,180,216,0.06)"),
            xaxis=dict(gridcolor="rgba(0,180,216,0.06)"),
            height=250, margin=dict(l=10,r=10,t=40,b=10),
            font=dict(family="Inter", color="#8ba7c7"),
        )
        st.plotly_chart(fig_vol, use_container_width=True)

    # ─── TAB 4: 3D VISUALIZATIONS ──────────────────────────────────────────────
    with tab4:
        st.markdown('<div class="section-header">🌋 3D Price & Volatility Landscape</div>', unsafe_allow_html=True)

        col_3d1, col_3d2 = st.columns(2)

        with col_3d1:
            # 3D Surface: Price vs Volume vs RSI
            df_3d = df[["Close","Volume","RSI","Volatility"]].dropna().tail(120)
            fig_3d = go.Figure(data=[go.Scatter3d(
                x=df_3d["RSI"],
                y=df_3d["Volatility"] * 100,
                z=df_3d["Close"],
                mode="markers",
                marker=dict(
                    size=5,
                    color=df_3d["Close"],
                    colorscale="Viridis",
                    opacity=0.85,
                    showscale=True,
                    colorbar=dict(title="Price $", tickprefix="$"),
                    line=dict(color="rgba(255,255,255,0.1)", width=0.5),
                ),
                text=[f"Date: {i.date()}<br>Price: ${c:.2f}<br>RSI: {r:.1f}<br>Vol: {v:.1f}%"
                      for i,(c,r,v) in zip(df_3d.index, zip(df_3d["Close"],df_3d["RSI"],df_3d["Volatility"]*100))],
                hovertemplate="%{text}<extra></extra>",
                name="",
            )])
            fig_3d.update_layout(
                template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                scene=dict(
                    xaxis=dict(title="RSI", backgroundcolor="rgba(5,11,24,0.8)", gridcolor="rgba(0,180,216,0.1)", showbackground=True),
                    yaxis=dict(title="Volatility %", backgroundcolor="rgba(5,11,24,0.8)", gridcolor="rgba(0,180,216,0.1)", showbackground=True),
                    zaxis=dict(title="Price $", backgroundcolor="rgba(5,11,24,0.8)", gridcolor="rgba(0,180,216,0.1)", showbackground=True),
                    camera=dict(eye=dict(x=1.5, y=1.5, z=0.8)),
                ),
                title=dict(text="<b>3D: Price vs RSI vs Volatility</b>", font=dict(size=14, color="#e8f4f8"), x=0.01),
                height=500, margin=dict(l=0,r=0,t=40,b=0),
                font=dict(family="Inter", color="#8ba7c7"),
            )
            st.plotly_chart(fig_3d, use_container_width=True)

        with col_3d2:
            # 3D Surface: Bollinger Band width over time
            df_surf = df[["Close","BB_Upper","BB_Lower","Volume"]].dropna().tail(90)
            bb_width = df_surf["BB_Upper"] - df_surf["BB_Lower"]
            
            fig_3d2 = go.Figure(data=[go.Scatter3d(
                x=list(range(len(df_surf))),
                y=df_surf["Close"].values,
                z=bb_width.values,
                mode="lines+markers",
                line=dict(color=df_surf["Close"].values, colorscale="Plasma", width=4),
                marker=dict(size=4, color=df_surf["Close"].values, colorscale="Plasma",
                           showscale=True, colorbar=dict(title="Price $", tickprefix="$", x=1.05)),
                text=[f"Day {i}<br>Price: ${p:.2f}<br>BB Width: ${w:.2f}"
                      for i,(p,w) in enumerate(zip(df_surf["Close"],bb_width))],
                hovertemplate="%{text}<extra></extra>",
            )])
            fig_3d2.update_layout(
                template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                scene=dict(
                    xaxis=dict(title="Day", backgroundcolor="rgba(5,11,24,0.8)", gridcolor="rgba(0,180,216,0.1)", showbackground=True),
                    yaxis=dict(title="Price $", backgroundcolor="rgba(5,11,24,0.8)", gridcolor="rgba(0,180,216,0.1)", showbackground=True),
                    zaxis=dict(title="BB Width $", backgroundcolor="rgba(5,11,24,0.8)", gridcolor="rgba(0,180,216,0.1)", showbackground=True),
                    camera=dict(eye=dict(x=1.5, y=-1.5, z=0.8)),
                ),
                title=dict(text="<b>3D: Price Path & Bollinger Band Width</b>", font=dict(size=14, color="#e8f4f8"), x=0.01),
                height=500, margin=dict(l=0,r=0,t=40,b=0),
                font=dict(family="Inter", color="#8ba7c7"),
            )
            st.plotly_chart(fig_3d2, use_container_width=True)

        # 3D Candlestick-style surface
        st.markdown('<div class="section-header">🏔️ OHLCV 3D Heatmap Surface</div>', unsafe_allow_html=True)
        df_heat = df[["Open","High","Low","Close","Volume"]].dropna().tail(60)
        n = len(df_heat)
        
        # Create surface data: day × OHLC position
        z_surface = np.array([
            df_heat["Low"].values,
            df_heat["Open"].values,
            df_heat["Close"].values,
            df_heat["High"].values,
        ])
        
        fig_surf = go.Figure(data=[go.Surface(
            z=z_surface,
            x=list(range(n)),
            y=["Low","Open","Close","High"],
            colorscale="RdYlGn",
            opacity=0.85,
            showscale=True,
            colorbar=dict(title="Price $", tickprefix="$"),
            contours=dict(z=dict(show=True, usecolormap=True, project_z=True, width=2)),
        )])
        fig_surf.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            scene=dict(
                xaxis=dict(title="Day (recent 60)", backgroundcolor="rgba(5,11,24,0.8)", gridcolor="rgba(0,180,216,0.1)", showbackground=True),
                yaxis=dict(title="OHLC Level", backgroundcolor="rgba(5,11,24,0.8)", gridcolor="rgba(0,180,216,0.1)", showbackground=True),
                zaxis=dict(title="Price ($)", backgroundcolor="rgba(5,11,24,0.8)", gridcolor="rgba(0,180,216,0.1)", showbackground=True),
                camera=dict(eye=dict(x=1.8, y=-1.2, z=0.7)),
            ),
            title=dict(text="<b>3D OHLC Price Surface (Last 60 Days)</b>", font=dict(size=14, color="#e8f4f8"), x=0.01),
            height=520, margin=dict(l=0,r=0,t=40,b=0),
            font=dict(family="Inter", color="#8ba7c7"),
        )
        st.plotly_chart(fig_surf, use_container_width=True)

        # Returns distribution
        col_dist1, col_dist2 = st.columns(2)
        with col_dist1:
            returns_pct = df["Returns"].dropna() * 100
            fig_dist = go.Figure()
            fig_dist.add_trace(go.Histogram(
                x=returns_pct, nbinsx=60, name="Daily Returns",
                marker=dict(color="rgba(0,180,216,0.6)", line=dict(color="rgba(0,180,216,0.3)", width=0.5)),
            ))
            fig_dist.add_vline(x=returns_pct.mean(), line_dash="dash", line_color="#f5a623",
                              annotation_text=f"Mean: {returns_pct.mean():.2f}%")
            fig_dist.add_vline(x=0, line_dash="dot", line_color="rgba(255,255,255,0.3)")
            fig_dist.update_layout(
                template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(5,11,24,0.8)",
                title=dict(text="<b>Returns Distribution</b>", font=dict(size=14, color="#e8f4f8"), x=0.01),
                xaxis=dict(title="Daily Return %", gridcolor="rgba(0,180,216,0.06)"),
                yaxis=dict(title="Frequency", gridcolor="rgba(0,180,216,0.06)"),
                height=320, margin=dict(l=10,r=10,t=40,b=10),
                font=dict(family="Inter", color="#8ba7c7"),
            )
            st.plotly_chart(fig_dist, use_container_width=True)

        with col_dist2:
            # Waterfall / Heatmap of monthly returns
            df_ret = df[["Returns"]].copy()
            df_ret.index = pd.to_datetime(df_ret.index)
            df_ret["Month"] = df_ret.index.month
            df_ret["Year"] = df_ret.index.year
            monthly = df_ret.groupby(["Year","Month"])["Returns"].sum() * 100
            monthly_df = monthly.reset_index()
            pivot = monthly_df.pivot(index="Year", columns="Month", values="Returns")
            pivot.columns = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][:len(pivot.columns)]
            
            fig_heat = go.Figure(data=go.Heatmap(
                z=pivot.values,
                x=pivot.columns,
                y=pivot.index.astype(str),
                colorscale=[[0,"rgba(255,71,87,0.9)"],[0.5,"rgba(30,30,30,0.9)"],[1,"rgba(0,212,170,0.9)"]],
                zmid=0,
                text=[[f"{v:.1f}%" if not np.isnan(v) else "" for v in row] for row in pivot.values],
                texttemplate="%{text}",
                textfont=dict(size=10, color="white"),
                hoverongaps=False,
                colorbar=dict(title="%", ticksuffix="%"),
            ))
            fig_heat.update_layout(
                template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(5,11,24,0.8)",
                title=dict(text="<b>Monthly Returns Heatmap</b>", font=dict(size=14, color="#e8f4f8"), x=0.01),
                height=320, margin=dict(l=10,r=10,t=40,b=10),
                font=dict(family="Inter", color="#8ba7c7", size=11),
                xaxis=dict(side="bottom"),
            )
            st.plotly_chart(fig_heat, use_container_width=True)

    # ─── TAB 5: DATA & STATISTICS ──────────────────────────────────────────────
    with tab5:
        col_stat1, col_stat2 = st.columns([1, 1])

        with col_stat1:
            st.markdown('<div class="section-header">📊 Descriptive Statistics</div>', unsafe_allow_html=True)
            stats_df = df[["Open","High","Low","Close","Volume","RSI","MACD","Volatility"]].describe().T
            stats_df.columns = ["Count","Mean","Std","Min","25%","50%","75%","Max"]
            stats_df = stats_df.round(3)
            st.dataframe(stats_df.style.background_gradient(cmap="Blues", axis=1), use_container_width=True)

            st.markdown('<div class="section-header" style="margin-top:1.5rem;">🔗 Correlation Matrix</div>', unsafe_allow_html=True)
            corr_cols = ["Close","Volume","RSI","MACD","ATR","Volatility"]
            corr = df[corr_cols].dropna().corr()
            fig_corr = px.imshow(
                corr, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
                title="Feature Correlation Matrix",
            )
            fig_corr.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(5,11,24,0.8)",
                font=dict(family="Inter", color="#8ba7c7", size=11),
                height=380, margin=dict(l=10,r=10,t=40,b=10),
                title=dict(font=dict(size=13, color="#e8f4f8"), x=0.01),
            )
            st.plotly_chart(fig_corr, use_container_width=True)

        with col_stat2:
            st.markdown('<div class="section-header">📋 Recent Price Data</div>', unsafe_allow_html=True)
            show_df = df[["Open","High","Low","Close","Volume","RSI","MACD","Volatility"]].tail(20).copy()
            show_df = show_df.round(3)
            show_df.index = pd.to_datetime(show_df.index).strftime("%Y-%m-%d")
            st.dataframe(show_df[::-1], use_container_width=True, height=320)

            st.markdown('<div class="section-header" style="margin-top:1.5rem;">📦 Company Info</div>', unsafe_allow_html=True)
            info_keys = [
                ("longName","Company"), ("sector","Sector"), ("industry","Industry"),
                ("country","Country"), ("exchange","Exchange"), ("currency","Currency"),
                ("marketCap","Market Cap"), ("fiftyTwoWeekHigh","52W High"),
                ("fiftyTwoWeekLow","52W Low"), ("dividendYield","Dividend Yield"),
                ("beta","Beta"), ("forwardPE","Forward P/E"),
            ]
            info_data = []
            for key, label in info_keys:
                val = info.get(key, "—")
                if key == "marketCap" and isinstance(val, (int, float)):
                    val = f"${val/1e9:.2f}B" if val >= 1e9 else f"${val/1e6:.0f}M"
                elif key == "dividendYield" and isinstance(val, float):
                    val = f"{val*100:.2f}%"
                elif isinstance(val, float):
                    val = f"{val:.4f}"
                info_data.append({"Field": label, "Value": str(val)})
            st.dataframe(pd.DataFrame(info_data).set_index("Field"), use_container_width=True, height=350)

        # Volume profile
        st.markdown('<div class="section-header">📊 Volume Profile</div>', unsafe_allow_html=True)
        price_bins = pd.cut(df["Close"], bins=30)
        vol_profile = df.groupby(price_bins, observed=True)["Volume"].sum().reset_index()
        vol_profile["Price"] = vol_profile["Close"].apply(lambda x: x.mid)
        vol_profile["Color"] = vol_profile["Price"].apply(
            lambda p: "rgba(0,212,170,0.7)" if p >= last_price else "rgba(255,71,87,0.7)")
        
        fig_vp = go.Figure()
        fig_vp.add_trace(go.Bar(
            y=vol_profile["Price"], x=vol_profile["Volume"], orientation="h",
            marker_color=vol_profile["Color"], name="Volume at Price",
        ))
        fig_vp.add_hline(y=last_price, line_dash="dash", line_color="#f5a623",
                        annotation_text=f"Current: ${last_price:.2f}", annotation_position="right")
        fig_vp.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(5,11,24,0.8)",
            title=dict(text="<b>Volume Profile at Price Level</b>", font=dict(size=14, color="#e8f4f8"), x=0.01),
            xaxis=dict(title="Total Volume", gridcolor="rgba(0,180,216,0.06)"),
            yaxis=dict(title="Price ($)", tickprefix="$", gridcolor="rgba(0,180,216,0.06)"),
            height=380, margin=dict(l=10,r=10,t=40,b=10),
            font=dict(family="Inter", color="#8ba7c7"),
        )
        st.plotly_chart(fig_vp, use_container_width=True)

# ─── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;padding:1rem;color:#8ba7c7;font-size:0.75rem;">
    <span style="color:#00b4d8;font-weight:600;">StockOracle Pro</span> &nbsp;|&nbsp; 
    Powered by Linear Regression ML · Plotly · Yahoo Finance &nbsp;|&nbsp;
    <span style="color:#f5a623;">⚠️ For educational purposes only. Not financial advice.</span>
</div>
""", unsafe_allow_html=True)