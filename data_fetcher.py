class DataFetcher:
    @staticmethod
    def get_current_price(ticker):
        return 100.0
    @staticmethod
    def validate_ticker(ticker):
        return bool(ticker)
    @staticmethod
    def get_daily_returns(ticker):
        import pandas as pd
        import numpy as np
        dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
        returns = np.random.normal(0.001, 0.01, size=len(dates))
        df = pd.DataFrame({'date': dates, 'returns': returns})
        df.set_index('date', inplace=True)
        return df

