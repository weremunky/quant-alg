# Quantitative Trading Strategy: Moving Average Crossover

A Python implementation of a classic quantitative trading strategy using moving average crossovers on SPY (S&P 500 ETF) data. Built to demonstrate a systematic trading approach with backtesting and performance analysis.

---

## What This Does

This project implements a simple but effective trading strategy that **buys when a short-term moving average crosses above a long-term moving average**, and stays in cash otherwise. I used 9 years of SPY data (2015–2024) to test whether this approach can beat a basic buy-and-hold strategy.

---

## Key Features

- **Real market data:** Uses yfinance to pull actual SPY price history
- **Moving average signals:** 20-day and 50-day simple moving averages
- **Performance comparison:** Strategy returns vs. buy-and-hold benchmark
- **Risk metrics:** Sharpe ratio and win rate calculations
- **Visual analysis:** Equity curve plots to see performance over time

---

## Setup & Installation

You'll need Python 3.7+ and a few libraries.  
Install dependencies with:

```bash
pip3 install pandas yfinance matplotlib 
```

That’s it. No API keys or paid data feeds required.
---

## How to Run

Just run the main script:

```bash
python3 main.py
```

The program will:

    Download SPY data from Yahoo Finance (2015–2024)

    Calculate moving averages and generate trading signals

    Simulate the strategy and compare to buy-and-hold

    Print performance metrics and show a plot

---

## Understanding the Results

The output gives you three key metrics:

    Sharpe Ratio: Risk-adjusted returns (higher is better, >1.0 is generally good)

    Win Rate: Percentage of profitable trading days

    Equity Curves: Visual comparison of strategy vs. market performance

The strategy generates a “signal” of 1 (invested) when the 20-day MA is above the 50-day MA, and 0 (cash) otherwise. It’s a trend-following approach that tries to capture sustained upward moves while avoiding some downturns.

---

## What I Learned

This was my first real dive into quantitative finance, and it taught me a lot about:

    Working with financial time series data

    The importance of proper backtesting methodology

    How simple strategies can sometimes be surprisingly effective

    The trade-offs between returns and risk management

The moving average crossover isn’t groundbreaking, but it’s a solid foundation for understanding systematic trading approaches.

---

## Next Steps & Improvements

Some ideas I’m considering for future versions:

    Transaction costs: Add realistic brokerage fees and slippage

    Multiple timeframes: Test different MA periods (10/30, 50/200, etc.)

    Additional filters: Volume confirmation, volatility adjustments

    More assets: Extend beyond SPY to other ETFs or individual stocks

    Risk management: Stop-losses, position sizing, drawdown limits

This project gave me hands-on experience with the kind of systematic analysis that’s common in quantitative finance roles, and I’m excited to build on it.

---

Ian Angel, 2024
