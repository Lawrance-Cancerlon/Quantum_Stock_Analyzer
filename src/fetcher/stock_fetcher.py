import yfinance as yf
import numpy as np
import pandas as pd
import logging
from typing import Optional


class StockFetcher:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def fetch_data(self, symbol: str, days: int = 30) -> Optional[pd.DataFrame]:
        """Fetch stock data from Yahoo Finance"""

        try:
            if not symbol.endswith('.JK'):
                symbol += '.JK'
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=f'{days}d')

            if data.empty:
                self.logger.warning(f"Not found: fetching data for {symbol}")
                return None
            
            data['Returns'] = data['Close'].pct_change()
            data['SMA_5'] = data['Close'].rolling(window=5).mean()
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            data['Volatility'] = data['Returns'].rolling(window=10).std()

            self.logger.info(f"Success: fetched {len(data)} data for {symbol}")
            return data
    
        except Exception as e:
            self.logger.error(f"Failed: fetching data for {symbol} - {str(e)}")
            return None
        
    def get_current_price(self, symbol: str) -> Optional[float]:
        """Get the current stock price"""

        try:
            if not symbol.endswith('.JK'):
                symbol += '.JK'
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d')

            if not data.empty:
                return float(data['Close'].iloc[-1])
            return None
        
        except Exception as e:
            self.logger.error(f"Failed: getting current price for {symbol} - {str(e)}")
            return None
        
    def validate_symbol(self, symbol: str) -> bool:
        """Validate the stock symbol"""
        try:
            data = self.fetch_data(symbol, 1)
            return data is not None and not data.empty
        except:
            return False