import pandas as pd
import yfinance as yf

#Download SPY (S&P 500 ETF) daily data from Yahoo Finance (2015-2024)
def get_data(symbol="SPY", start="2015-01-01", end="2024-01-01"):
    data = yf.download(symbol, start=start, end=end)
    data.to_csv(f"{symbol}_{start[:4]}_{end[:4]}.csv")
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
    #Step 1: Data Collection
    df = get_data()
    print("Data downloaded. First few rows:")
    print(df.head())

    #Step 2: Add indicators
    df = add_indicators(df)

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
    plt.title('Strategy vs. Market Performance (2015–2024)')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.tight_layout()
    plt.show()