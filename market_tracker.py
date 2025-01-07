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
        # Calculate point-by-point returns
        point_returns = ((data[column] - data[column].iloc[0]) / data[column].iloc[0]) * 100
        total_return = point_returns.iloc[-1]
        
        trace_props = {
            'x': data.index,
            'y': data[column],
            'name': f"{column} ({total_return:.1f}%)",
            'mode': 'lines',
            'hovertemplate': f"{column}<br>Value: %{{y:.1f}}<br>Return: %{{text:.1f}}%<extra></extra>",
            'text': point_returns,
            'line': {'shape': 'spline', 'smoothing': 0.8}
        }
        
        # Add extra styling for Ethereum
        if column == 'Ethereum':
            trace_props['line']['width'] = 3
            
        fig.add_trace(go.Scatter(**trace_props))
    
    fig.update_layout(
        title='Market Performance Tracker',
        xaxis_title='Date',
        yaxis_title='Normalized Price',
        hovermode='x unified',
        margin=dict(t=50, l=50, r=50, b=50),
        template='plotly_white',
        hoverlabel=dict(
            font_size=12,
            font_family="Arial"
        )
    )
    
    # Create the HTML with a refresh button
    html_content = f"""
    <html>
    <head>
        <title>Market Performance Tracker</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }}
            .button {{
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 4px;
                transition: background-color 0.3s;
            }}
            .button:hover {{
                background-color: #45a049;
            }}
            .container {{
                text-align: center;
                padding: 20px;
                background-color: #f8f9fa;
            }}
            .last-updated {{
                color: #666;
                font-style: italic;
                margin-top: 10px;
            }}
            .js-plotly-plot .js-line[data-name*="Ethereum"] {{
                animation: pulse 2s infinite;
            }}
            @keyframes pulse {{
                0% {{ opacity: 0.6; }}
                50% {{ opacity: 1; }}
                100% {{ opacity: 0.6; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <button class="button" onclick="window.location.reload();">Refresh Data</button>
            <div class="last-updated">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC</div>
        </div>
        {fig.to_html(full_html=False, include_plotlyjs=True)}
    </body>
    </html>
    """
    
    # Write the complete HTML to file
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

def main():
    # Fetch data
    data = fetch_market_data()
    
    # Normalize data
    normalized_data = normalize_data(data)
    
    # Create plot and save as HTML file
    create_plot(normalized_data)

if __name__ == "__main__":
    main() 