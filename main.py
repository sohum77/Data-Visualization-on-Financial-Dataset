"""
main.py
Combine .txt price files (ETFs + Stocks) into prices.csv, produce a split-adjusted CSV,
create securities.csv (metadata) and a simple fundamentals.csv (derived metrics).
"""

import os
import pandas as pd
from pathlib import Path

# --- CONFIG: change if needed ---
ROOT = Path(".")
DATA_DIR = ROOT / "data"
DATA_ETFS = DATA_DIR / "ETFs"
DATA_STOCKS = DATA_DIR / "stocks"
# also check top-level folders (some extra copies exist)
TOP_ETFS = ROOT / "ETFs"
TOP_STOCKS = ROOT / "Stocks"

OUT_DIR = DATA_DIR  # keep output inside data/
OUT_DIR.mkdir(parents=True, exist_ok=True)

# helper to find txt files in several possible folders
def gather_files(*folders):
    files = []
    for folder in folders:
        if folder and folder.exists() and folder.is_dir():
            for f in folder.iterdir():
                if f.is_file() and f.suffix.lower() in {".txt", ".csv"}:
                    files.append(f)
    return sorted(files)

# gather files from both locations
files = gather_files(DATA_ETFS, DATA_STOCKS, TOP_ETFS, TOP_STOCKS)
if not files:
    raise SystemExit("No .txt/.csv price files found in data/ETFs or data/stocks or top-level ETFs/Stocks. Check path.")

print(f"Found {len(files)} files — using first 200 (you can change limit in the code).")

# --- load and concatenate ---
dfs = []
for i, f in enumerate(files):
    if i >= 200:  # safety/limit — remove or increase for full dataset
        break
    try:
        df = pd.read_csv(f)
    except Exception as e:
        print(f"Skipping {f.name}: read error {e}")
        continue

    # Standardize column names (common variants)
    df.columns = [c.strip() for c in df.columns]
    # ensure Date exists
    if "Date" not in df.columns and "date" in df.columns:
        df = df.rename(columns={c: "Date" for c in df.columns if c.lower() == "date"})
    # add symbol from filename (strip extensions and .us if present)
    raw = f.name
    sym = raw.split(".")[0].upper()  # e.g., aaxj.us.txt -> AAXJ
    # handle patterns like AAPL.us.txt or AAPL_2010...txt
    sym = sym.split("_")[0].upper()
    sym = sym.replace(".US", "").upper()

    df["symbol"] = sym

    # ensure Date is datetime
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    else:
        # if no Date column, try first column
        df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], errors="coerce")
        df = df.rename(columns={df.columns[0]: "Date"})

    dfs.append(df)

if not dfs:
    raise SystemExit("No readable dataframes collected. Check file formatting.")

combined = pd.concat(dfs, ignore_index=True, sort=False)
# sort for tidiness
combined = combined.sort_values(by=["symbol", "Date"]).reset_index(drop=True)

# Save prices.csv
prices_path = OUT_DIR / "prices.csv"
combined.to_csv(prices_path, index=False)
print(f"Saved combined prices -> {prices_path}")

# --- Create prices-split-adjusted.csv ---
# Many source files may not include 'Adj Close'. We'll try common names then fallback.
adj_col_candidates = ["Adj Close", "Adj_Close", "AdjClose", "Adjusted Close", "adjusted_close"]
present_adj = None
for c in adj_col_candidates:
    if c in combined.columns:
        present_adj = c
        break

if present_adj:
    combined = combined.rename(columns={present_adj: "adjusted_close"})
    print(f"Using existing adjusted column: {present_adj}")
else:
    # fallback: create adjusted_close as Close (note: not truly split-adjusted)
    if "Close" in combined.columns:
        combined["adjusted_close"] = combined["Close"]
        print("No adjusted column found — created 'adjusted_close' by copying 'Close' (not split-adjusted).")
    else:
        combined["adjusted_close"] = pd.NA
        print("No Close column found — 'adjusted_close' set to NA.")

prices_adj_path = OUT_DIR / "prices-split-adjusted.csv"
combined.to_csv(prices_adj_path, index=False)
print(f"Saved split-adjusted prices -> {prices_adj_path}")

# --- Create securities.csv (simple metadata) ---
securities = []
for f in files[:200]:
    sym = f.name.split(".")[0].split("_")[0].upper().replace(".US", "")
    # determine type: check parent folder name
    parent = f.parent.name.lower()
    typ = "ETF" if "etf" in parent else ("Stock" if "stock" in parent else "Unknown")
    securities.append({"symbol": sym, "type": typ, "source_file": f.name})

securities_df = pd.DataFrame(securities).drop_duplicates(subset=["symbol"]).reset_index(drop=True)

# try to enrich using yfinance (optional)
try:
    import yfinance as yf
    print("yfinance available — attempting to fetch company name and sector for a few tickers (may be slow).")
    extra = []
    for sym in securities_df["symbol"].tolist():
        try:
            info = yf.Ticker(sym).info
            name = info.get("longName") or info.get("shortName")
            sector = info.get("sector")
            industry = info.get("industry")
            extra.append({"symbol": sym, "company_name": name, "sector": sector, "industry": industry})
        except Exception:
            extra.append({"symbol": sym, "company_name": None, "sector": None, "industry": None})
    extra_df = pd.DataFrame(extra).set_index("symbol")
    securities_df = securities_df.set_index("symbol").join(extra_df).reset_index()
except Exception:
    print("yfinance not installed or failed — securities.csv will contain basic fields only. Install yfinance to enrich data.")

securities_path = OUT_DIR / "securities.csv"
securities_df.to_csv(securities_path, index=False)
print(f"Saved securities metadata -> {securities_path}")

# --- Create a simple fundamentals.csv derived from prices (basic metrics) ---
funds = []
for sym, group in combined.groupby("symbol"):
    g = group.sort_values("Date").copy()
    # ensure numeric close
    if "Close" in g.columns:
        g["Close"] = pd.to_numeric(g["Close"], errors="coerce")
    else:
        continue
    mean_close = g["Close"].mean()
    std_close = g["Close"].std()
    # simple daily returns (pct)
    g = g.dropna(subset=["Close"])
    g["ret"] = g["Close"].pct_change()
    avg_ret = g["ret"].mean()
    vol = g["ret"].std() * (252**0.5) if not pd.isna(g["ret"].std()) else pd.NA
    max_drawdown = ((g["Close"].cummax() - g["Close"]) / g["Close"].cummax()).max() if not g["Close"].isna().all() else pd.NA
    avg_volume = pd.to_numeric(g["Volume"], errors="coerce").mean() if "Volume" in g.columns else pd.NA

    funds.append({
        "symbol": sym,
        "mean_close": mean_close,
        "std_close": std_close,
        "avg_daily_return": avg_ret,
        "annualized_volatility": vol,
        "max_drawdown": max_drawdown,
        "avg_volume": avg_volume
    })

fundamentals_df = pd.DataFrame(funds)
fundamentals_path = OUT_DIR / "fundamentals.csv"
fundamentals_df.to_csv(fundamentals_path, index=False)
print(f"Saved derived fundamentals -> {fundamentals_path}")

print("All done. You now have prices.csv, prices-split-adjusted.csv, securities.csv, fundamentals.csv in the data/ folder.")
