# 📊 Data Visualization on Financial Dataset

This project analyzes and visualizes **financial data of multiple ETFs (Exchange-Traded Funds)** using Python.  
It explores trends in prices, volatility, returns, and sector performance through **20+ professional visualizations**.

---

## 🎯 Objective
The goal of this project is to perform a detailed analysis and create meaningful visualizations from a financial dataset consisting of multiple ETFs.  
It aims to uncover insights into **stock performance, volatility, sector behavior, and risk-return relationships** through visual analytics.

---

## 💼 Real-world Use Cases
- **Portfolio Analysis:** Identify ETFs with better risk-return profiles for investment decisions.  
- **Market Research:** Analyze sector trends and investor behavior across years.  
- **Financial Education:** Demonstrate how data visualization helps interpret stock market dynamics.  
- **Business Intelligence:** Assist asset managers and financial analysts in creating visual dashboards.

---

## 🧩 Key Features
- Performed **data preprocessing, cleaning**, and handled missing values  
- Created **20+ different visualizations** for trend, risk, and performance analysis  
- Explored relationships between **trading volume, returns, and volatility**  
- Evaluated **sector distribution** and identified performance consistency over time  
- Generated visuals for **cumulative return, moving average, correlation, and drawdown**

---

## ⚙️ How to Run the Project

1. **Clone or download** the project folder:
   ```bash
   git clone <your_repo_link>
   ```

2. **Create or activate the environment** used for this project:  
   The notebook was developed in a Conda environment named **`dv`** (Python 3.10.18).  
   You can recreate it with:
   ```bash
   conda create -n dv python=3.10
   conda activate dv
   ```

3. **Install required Python libraries:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate the dataset:**
   Run the file:
   ```bash
   python main.py
   ```
   This script converts raw financial data into a CSV file automatically saved as:
   ```
   data/prices.csv
   ```

5. **Open the Jupyter Notebook:**
   ```bash
   jupyter notebook visualization.ipynb
   ```
   When prompted, select the **`dv (Python 3.10.18)`** kernel to ensure compatibility.

6. **Run all cells sequentially** to generate all visualizations:
   - Price and return trends  
   - Volatility and drawdown charts  
   - Sector and volume analysis  
   - Correlation heatmaps and risk-return visuals  

7. All insights and charts will be displayed automatically after execution.

---

## 📁 Project Folder Structure

```
D:\Data Science Projects\Data Visualization on Financial Dataset

│
├── Data/                            
│   ├── ETFs/
│   │   ├── aadr.us
│   │   ├── aaxj.us
│   │   └── zsl.us
│   │
│   ├── Stocks/
│   │   ├── a.us
│   │   ├── aa.us
│   │   └── zyne.us
│   │
│   ├── fundamentals.csv
│   ├── prices.csv
│   ├── prices-split-adjusted.csv
│   └── securities.csv 
│
├── ETFs/                            
│   ├── aadr.us
│   ├── aaxj.us
│   └── zsl.us
│
├── Screenshots/                            
│   ├── AGG Closing Price Over Time (1).png
│   ├── Top 3 Stocks Closing Price Trends (2).png
│   ├── Top 15 Stocks by Average Closing Price (3).png
│   ├── Top 15 Stocks by Average Trading Volume (4).png
│   ├── Distribution of Daily Returns (5).png
│   ├── Daily Return Distribution - Top 6 Symbols (6).png
│   ├── Relationship Between Trading Volume and Closing Price (7).png
│   ├── Correlation Heatmap - Fundamental Metrics (8).png
│   ├── Moving Averages (20 & 100 days) -  AGG (9).png
│   ├── Cumulative Return Over Time - AGG (10).png
│   ├── Sector Distribution (Excluding Unknown) (11).png
│   ├── Distribution of Annualized Volatility (12).png
│   ├── Top 15 Stocks by Max Drawdown (13).png
│   ├── Adjusted Close vs Close (Skipped) (14).png
│   ├── Missing Values % by Column (15).png
│   ├── Average Trading Volume by Sector (Top 8) (16).png
│   ├── Risk vs Average Price (17).png
│   ├── 30-Day Rolling Annualized Volatility (AGG) (18).png
│   ├── Risk vs Return (Average Daily Return vs Volatility) (19).png
│   └── AGG Average Monthly Returns (Year × Month Heatmap) (20).png
│
├── Stocks/                            
│   ├── a.us
│   ├── aa.us
│   └── zyne.us
│
├── .gitignore                         
├── main.py                 
├── README.md
├── Requirements.txt                    
└── visualization.ipynb
```

---

## 📂 Dataset Source
The dataset used in this project was downloaded from Kaggle:  
[Price and Volume Data for All US Stocks & ETFs](https://www.kaggle.com/datasets/borismarjanovic/price-volume-data-for-all-us-stocks-etfs)

It contains historical **price and trading volume data** for U.S. stocks and ETFs from **2010 onwards**.

---

## 🧰 Tools and Technologies
- **Python 3.10.18 (`dv` Conda environment)**  
- **Pandas**, **NumPy**  
- **Matplotlib**, **Seaborn**  
- **Scipy**, **Jupyter Notebook**

---

## 📈 Key Insights
- **AGG** shows consistent long-term growth with low volatility  
- **DIA** and **AMLP** are highly traded ETFs, showing strong market interest  
- The **risk-return relationship** across ETFs is weak, emphasizing diversification  
- **Financial and Technology sectors** dominate in trading activity  
- **2008–09** marked the highest volatility spike across all instruments  

---

## 🏁 Conclusion
This project provides a **visual and statistical understanding** of ETF market behavior over time, demonstrating the importance of **data visualization in financial analytics and portfolio evaluation**.

---

## 👨‍💻 Author
**Sohum Patil**  
Project Title: *Data Visualization on Financial Dataset*

---

### 📬 Feedback
💌 For suggestions or collaboration:  
**sohum7even@gmail.com**
