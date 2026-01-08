# Stock Decision Dashboard

A decision-oriented stock analysis dashboard built using Python and Streamlit.  
The project focuses on **exploratory financial analysis and risk assessment**, allowing users to analyze any stock’s historical performance using multiple metrics — without relying on prediction models or machine learning.

---

## 🖼️ Dashboard Preview

### Main Dashboard
![Main Dashboard](Assets/1.png)

### Stock Analysis & Visualization
![Stock Analysis](Assets/2.png)

Live demo:
URL Link for dashboard:



## Project Objective

The goal of this project is to make **stock analysis intuitive and decision-focused** by:

- Transforming raw stock price data into meaningful financial metrics
- Allowing users to explore **returns, volatility, and drawdowns** interactively
- Presenting insights in a clean, professional dashboard suitable for real-world use

This project is intentionally **analysis-driven**, not prediction-driven.

---

## Features

- Stock selection using Yahoo Finance ticker symbols  
- Time-range selection (1Y, 3Y, 5Y, MAX)  
- Metric-based analysis with toggleable views:
  - Closing Price
  - Cumulative Returns
  - Daily Returns
  - Volatility (20-day rolling)
  - Drawdown
- KPI summary for quick decision-making:
  - Latest Price
  - Total Return
  - Average Daily Return
  - Annualized Volatility
  - Maximum Drawdown
- Metric-specific, data-driven observations
- Clean and professional UI with custom styling

---

## Analysis Approach

Instead of focusing on predictions, the dashboard emphasizes **financial behavior and risk**:

- **Daily Returns**  
  Captures short-term price movements and market noise.

- **Cumulative Returns**  
  Shows long-term investment growth through compounding.

- **Volatility**  
  Measures risk intensity and uncertainty over time.

- **Drawdown**  
  Highlights peak-to-trough losses, representing downside risk and investor pain.

This approach aligns with how analysts and investors evaluate stocks in practice.

---

## Tech Stack

- **Python**
- **Streamlit** — interactive dashboard
- **Pandas** — data manipulation & time-series analysis
- **NumPy** — numerical computations
- **Matplotlib** — controlled, publication-style visualizations
- **yFinance** — historical market data source

---

## How to Run the Project

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd stock-dashboard

## 2. Clone the repository
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows

### 3. Install dependencies
 pip install -r requirements.txt

### 4. Run the dashboard
streamlit run app.py

###Key Takeaways

Demonstrates strong understanding of financial metrics and risk analysis

Shows ability to build end-to-end data products

Emphasizes clean architecture, validation, and user experience

Suitable for internship portfolios, interviews, and GitHub showcases

### Future Enhancements
Future Enhancements

Benchmark comparison (Stock vs Index)

Sector-wise analysis

Exportable reports

Portfolio-level analysis

KPI tooltips and metric explanations

Stock Predictions

### Author
Built by a B.Tech Computer Science (Data Science) student as a portfolio project focused on realistic financial data analysis and dashboard design.




