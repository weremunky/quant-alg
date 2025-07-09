import pandas as pd
import yfinance as yf
import argparse
import sys

#Download data from Yahoo Finance or load from a CSV file
def get_data(symbol="SPY", start="2015-01-01", end="2024-01-01", input_csv=None):
    if input_csv:
        try:
            data = pd.read_csv(input_csv, parse_dates=True, index_col=0)
        except Exception as e:
            print(f"Error loading {input_csv}: {e}")
            sys.exit(1)
    else:
        data = yf.download(symbol, start=start, end=end)
        if data.empty:
            print(f"No data found for {symbol} between {start} and {end}.")
            sys.exit(1)
        data.to_csv(f"{symbol}_{start[:4]}_{end[:4]}.csv")
    if "Close" not in data.columns:
        print("Input data must have a 'Close' column.")
        sys.exit(1)
    data = data.dropna(subset=["Close"])
    return data

#Calculate moving averages for strategy
def add_indicators(data, fast=20, slow=50):
    data['sma_fast'] = data['Close'].rolling(window=fast).mean()
    data['sma_slow'] = data['Close'].rolling(window=slow).mean()
    return data

#Generate trading signals based on moving average crossover
def generate_signals(data):
    data['signal'] = 0
    data.loc[data['sma_fast'] > data['sma_slow'], 'signal'] = 1
    return data

if __name__ == "__main__":
    #Argument parsing for custom runs
    parser = argparse.ArgumentParser(description="Universal Quant Trading Backtest")
    parser.add_argument("--symbol", type=str, default="SPY", help="Ticker symbol (default: SPY)")
    parser.add_argument("--start", type=str, default="2015-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default="2024-01-01", help="End date (YYYY-MM-DD)")
    parser.add_argument("--fast", type=int, default=20, help="Fast MA window (default: 20)")
    parser.add_argument("--slow", type=int, default=50, help="Slow MA window (default: 50)")
    parser.add_argument("--input_csv", type=str, default=None, help="Path to custom CSV (optional)")
    args = parser.parse_args()

    #Step 1: Data Collection
    df = get_data(symbol=args.symbol, start=args.start, end=args.end, input_csv=args.input_csv)
    print("Data loaded. First few rows:")
    print(df.head())

    #Step 2: Add indicators
    df = add_indicators(df, fast=args.fast, slow=args.slow)

    #Step 3: Generate signals
    df = generate_signals(df)

    #Preview relevant columns to confirm everything is set up
    print(df[['Close', 'sma_fast', 'sma_slow', 'signal']].tail(10))

    #Calculate daily returns for the market and strategy
    df['market_return'] = df['Close'].pct_change()
    df['strategy_return'] = df['market_return'] * df['signal'].shift(1)

    #Calculate cumulative returns
    df['market_cum'] = (1 + df['market_return']).cumprod()
    df['strategy_cum'] = (1 + df['strategy_return']).cumprod()

    print("\nCumulative returns (last 10 rows):")
    print(df[['market_cum', 'strategy_cum']].tail(10))

    #Step 6: Performance metrics
    sharpe = df['strategy_return'].mean() / df['strategy_return'].std() * (252 ** 0.5)
    win_rate = (df['strategy_return'] > 0).mean()
    print(f"\nSharpe Ratio: {sharpe:.2f}")
    print(f"Win Rate: {win_rate:.2%}")

    #Step 7: Plot the performance
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['market_cum'], label='Buy & Hold (Market)')
    plt.plot(df.index, df['strategy_cum'], label='Moving Avg Strategy')
    plt.title(f"{args.symbol} Strategy vs. Market Performance")
    
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    
    plt.legend()
    plt.tight_layout()
    plt.show()

