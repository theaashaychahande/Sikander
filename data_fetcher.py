class DataFetcher:
    _price_database = {
        'AAPL': 175.50,
        'GOOGL': 2800.30,
        'MSFT': 330.45,
        'AMZN': 3200.10,
        'TSLA': 220.75,
        'META': 310.20,
        'SPY': 430.80,
        'IVV': 435.60,
        'VOO': 380.90,
        'QQQ': 390.25,
        'BTC-USD': 35000.00,
        'ETH-USD': 1800.50
    }
    
    @staticmethod
    def get_current_price(ticker):
        return DataFetcher._price_database.get(ticker.upper(), 100.0)
    
    @staticmethod
    def validate_ticker(ticker):
        if not ticker or len(ticker) < 1 or len(ticker) > 10:
            return False
        return True
    
    @staticmethod
    def get_daily_returns(ticker):
        import pandas as pd
        import numpy as np
        
        dates = pd.date_range(end=pd.Timestamp.today(), periods=90)
        
        if 'BTC' in ticker.upper() or 'ETH' in ticker.upper():
            returns = np.random.normal(0.002, 0.04, size=len(dates))
        elif ticker.upper() in ['SPY', 'QQQ', 'IVV', 'VOO']:
            returns = np.random.normal(0.0005, 0.015, size=len(dates))
        else:
            returns = np.random.normal(0.001, 0.02, size=len(dates))
        
        df = pd.DataFrame({'date': dates, 'returns': returns})
        df.set_index('date', inplace=True)
        return df
