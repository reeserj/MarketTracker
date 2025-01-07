import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

def fetch_market_data():
    # Define tickers
    tickers = {
        'S&P 500': '^GSPC',
        'WTI Crude': 'CL=F',
        'Bitcoin': 'BTC-USD',
        'Ethereum': 'ETH-USD'
    }
    
    # Get end date (today) and start date (1 year ago)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    # Fetch data for all assets
    data = pd.DataFrame()
    for name, ticker in tickers.items():
        try:
            df = yf.download(ticker, start=start_date, end=end_date)['Close']
            if not df.empty:
                data[name] = df
            else:
                print(f"Warning: No data available for {name} ({ticker})")
        except Exception as e:
            print(f"Error fetching data for {name} ({ticker}): {str(e)}")
    
    return data

def normalize_data(data):
    # Normalize all assets to start at 100 for better comparison
    return data / data.iloc[0] * 100

def create_plot(data):
    fig = go.Figure()
    
    # Calculate returns for sorting
    returns = ((data.iloc[-1] - data.iloc[0]) / data.iloc[0]) * 100
    sorted_columns = returns.sort_values(ascending=False).index
    
    # Add traces in sorted order
    for column in sorted_columns:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data[column],
                name=f"{column} ({returns[column]:.1f}%)",
                mode='lines'
            )
        )
    
    fig.update_layout(
        title='Market Comparison (Normalized to 100)',
        xaxis_title='Date',
        yaxis_title='Normalized Price',
        hovermode='x unified'
    )
    
    return fig

def main():
    # Fetch data
    data = fetch_market_data()
    
    # Normalize data
    normalized_data = normalize_data(data)
    
    # Create plot
    fig = create_plot(normalized_data)
    
    # Save as HTML file
    fig.write_html('index.html', auto_open=True)

if __name__ == "__main__":
    main() 