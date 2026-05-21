<div align="center">

# 📉 Stock Price Prediction
### Machine Learning · Time Series · Quantitative Finance

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.x-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-Regressor-189AB4?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

<br/>

> **Predicting next-day stock closing prices using correlated multi-stock signals,
> temporal lag features, and rolling market statistics.**
> Four ML models benchmarked. Best model persisted for production inference.

<br/>

```
  STOCK_1(t) + STOCK_2..5(t) + LAG(t-1,t-2) + MA(5d) + VOLATILITY(5d)
                              ↓
                    [ ML Pipeline ]
                              ↓
                  PREDICTED PRICE → STOCK_1(t+1)
```

</div>

![Stock Price Prediction Demo](assets/stock_price_dash.gif)
---

## 📁 Repository Structure

```
stock-price-prediction/
│
├── 📓 Stock_Price_Prediction.ipynb              # End-to-end ML pipeline
├── 📊 stock_data.csv                            # Raw dataset · 365 days · 5 stocks
│
├── 🤖 Linear_Regression_StockPrice_Prediction.pkl   # Best model artifact
├── ⚖️  scaler.pkl                               # Fitted StandardScaler
├── 🗂️  columns.pkl                              # Feature column registry (14 cols)
│
└── 📄 README.md
```

---

## 📊 Dataset Overview

| Property | Value |
|----------|-------|
| **Total Records** | 365 daily observations |
| **Date Range** | 2020-01-01 → 2020-12-31 |
| **Input Signals** | Stock_1 · Stock_2 · Stock_3 · Stock_4 · Stock_5 |
| **Target Variable** | `Stock_1` closing price — next trading day |
| **Train / Test Split** | 80% / 20% · chronological (no shuffle) |
| **Preprocessing** | StandardScaler · bfill NaN · int casting |

---

## ⚙️ Feature Engineering Pipeline

> **14 final features** engineered from raw OHLC-style signals across 5 correlated stocks.

### Primary Stock (Stock_1)
| Feature | Type | Window | Description |
|---------|------|--------|-------------|
| `Stock_1` | Raw | — | Current day closing price |
| `MA_5` | Rolling Mean | 5-day | Short-term price trend |
| `Volatility_5` | Rolling Std | 5-day | Intraday risk proxy |
| `Daily_Return` | Pct Change | 1-day | Momentum signal |

### Cross-Asset Signals (Stock_2)
| Feature | Type | Window | Description |
|---------|------|--------|-------------|
| `Stock_2` | Raw | — | Correlated asset price |
| `Stock_2_Lag_1` | Lag | t-1 | Yesterday's Stock_2 price |
| `Stock_2_MA_5` | Rolling Mean | 5-day | Stock_2 trend |
| `Stock_2_Volatility` | Rolling Std | 5-day | Stock_2 risk signal |
| `Stock_2_Return` | Pct Change | 1-day | Stock_2 momentum |

### Temporal & Multi-Stock
| Feature | Description |
|---------|-------------|
| `Stock_3`, `Stock_4`, `Stock_5` | Raw correlated asset prices |
| `Months`, `Day` | Calendar-based seasonality features |

---

## 🤖 Model Benchmarking

All models trained on identical scaled features. Evaluated on held-out 20% test set.

| # | Model | Type | Verdict |
|---|-------|------|---------|
| 1 | **Linear Regression** | Parametric | ✅ **Best — saved to production** |
| 2 | **Random Forest Regressor** | Ensemble / Bagging | Robust · non-linear |
| 3 | **SVR** | Support Vector Regression | Strong on small scaled sets |
| 4 | **XGBoost Regressor** | Gradient Boosting | High capacity · tabular SOTA |

**Evaluation Metrics:** `MAE` · `MSE` · `RMSE` · `R² Score`

> Linear Regression outperformed ensemble methods — a strong signal that
> **well-engineered temporal features matter more than model complexity**
> on clean, low-noise financial time series.

---

## 🔧 Tech Stack

| Layer | Tools |
|-------|-------|
| **Language** | Python 3.10+ |
| **ML / Modeling** | Scikit-learn · XGBoost |
| **Data Wrangling** | Pandas · NumPy |
| **Visualization** | Plotly · Seaborn · Matplotlib |
| **Persistence** | Joblib (`.pkl` artifacts) |
| **Environment** | Jupyter Notebook |

---

## 🚀 Quickstart

### 1 · Clone & Install

```bash
git clone https://github.com/your-username/stock-price-prediction.git
cd stock-price-prediction
pip install pandas numpy scikit-learn xgboost plotly seaborn matplotlib joblib
```

### 2 · Run Full Pipeline

```bash
jupyter notebook Stock_Price_Prediction.ipynb
```

### 3 · Inference with Saved Model

```python
import joblib
import pandas as pd

# Load artifacts
model   = joblib.load('Linear_Regression_StockPrice_Prediction.pkl')
scaler  = joblib.load('scaler.pkl')
columns = joblib.load('columns.pkl')

# Construct feature vector (14 features — must match columns.pkl order)
X_new = pd.DataFrame([your_feature_dict], columns=columns)
X_scaled = scaler.transform(X_new)

# Predict
predicted_price = model.predict(X_scaled)
print(f"📈 Predicted next-day price: {predicted_price[0]:.2f}")
```

---

## 💡 Key Findings

```
📌  Lag features dominate — yesterday's price is the #1 predictor of tomorrow's.
📌  5-day MA adds strong directional context to raw price signals.
📌  Cross-stock signals (Stock_2 return + volatility) contribute meaningful alpha.
📌  Linear Regression > ensembles — on clean financial series, simplicity wins.
```

---

## 📦 Saved Artifacts

| Artifact | Description |
|----------|-------------|
| `Linear_Regression_StockPrice_Prediction.pkl` | Production-ready trained model |
| `scaler.pkl` | StandardScaler fitted on training split only |
| `columns.pkl` | Ordered list of 14 feature column names |

> ⚠️ Always use the saved `scaler.pkl` to transform new data before inference.
> Fitting a new scaler on unseen data causes train-test leakage.

---

## 📜 License

Distributed under the **MIT License** — free to use, modify, and distribute with attribution.

---

<div align="center">

**Built with 🧠 · Python · Scikit-learn · XGBoost**

*If this helped you, drop a ⭐ on the repo!*

</div>
