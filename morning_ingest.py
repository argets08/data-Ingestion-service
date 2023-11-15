import datetime
import logging
import pandas as pd
from pytz import timezone
import time

from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest,StockLatestBarRequest
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass, AssetStatus, AssetExchange
from  alpaca.trading.client import TradingClient

# Alpaca API credentials
API_KEY = ""
API_SECRET = ""
ALPACA_BASE_URL = 'https://data.alpaca.markets'

logging.getLogger("transformers").setLevel(logging.ERROR)


def fetch_financial_data(historical_data_client,symbol_list,start_date) -> pd.DataFrame:
    # Fetch financial data from Alpaca Markets API
    # Process and structure data for InfluxDB
    request_params = StockBarsRequest(symbol_or_symbols=symbol_list, timeframe='1Min', start_date=start_date)
    bars = historical_data_client.get_stock_bars(request_params)
    return bars.df


#get all nasdaq tickers that are active and tradable
def get_nasdaq_tickers(trading_client):
    search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY,status=AssetStatus.ACTIVE, exchange=AssetExchange.NASDAQ)
    assets = trading_client.get_all_assets(search_params)
    symbols = [asset.symbol for asset in assets if asset.tradable]
    return symbols


#filter out stocks that are not in <30 range
def filter_stock_list(historical_data_client, symbols_list) -> list:
    stocks = symbols_list  # List of 4617 stocks
    filtered_stocks = []
    chunk_size = 500  # Adjust based on the actual limit
    for i in range(0, len(stocks), chunk_size):
        chunk = stocks[i:i + chunk_size]
        request_params = StockLatestBarRequest(symbol_or_symbols=chunk,feed='sip')
        latest_bars = historical_data_client.get_stock_bars(request_params)
        latest_bars = pd.DataFrame(latest_bars)
        latest_bars['closing_price'] = latest_bars['bars'].apply(lambda x: x['c'])
        # Filter the DataFrame for closing prices below $30
        filtered_df = latest_bars[latest_bars['closing_price'] < 30]
        # Extract the stock symbols
        filtered_stocks.extend(filtered_df.index.tolist())
    # Flatten the list
    filtered_stocks = [stock for sublist in filtered_stocks for stock in sublist]
    return filtered_stocks
    # Now filtered_stocks contains stocks within the specified price range  


def main():
    # timez = timezone('US/Eastern')
    day_delta= 50
    historical_data_client = StockHistoricalDataClient(api_key=API_KEY,secret_key=API_SECRET)
    trading_client = TradingClient(api_key=API_KEY,secret_key=API_SECRET)
    str_date = (datetime.today() - datetime.timedelta(days=day_delta)).strftime('%Y-%m-%d')

    while True:
        symbols_list = get_nasdaq_tickers(trading_client)
        filtered_symbols = filter_stock_list(historical_data_client, symbols_list)
        data = fetch_financial_data(historical_data_client,symbol_list=filtered_symbols,start_date=str_date)
        # store_data_in_influxdb(data)
        time.sleep(60)  # Sleep for 60 seconds

if __name__ == "__main__":
    main()
