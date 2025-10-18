import pandas as pd


class Asset:
    def __init__(self, ticker, quantity, purchase_price):
        self.ticker = ticker
        self.quantity = quantity
        self.purchase_price = purchase_price
        self.current_price = purchase_price


class Portfolio:
    """Simple, import-safe Portfolio implementation.
    Avoids importing Streamlit or other app modules at top-level to prevent circular imports.
    DataFetcher is imported inside update_prices() where needed.
    """
    def __init__(self, name="My Portfolio"):
        self.name = name
        self.assets = {}
        self.benchmark = "SPY"
    def add_asset(self, ticker, quantity, purchase_price):
        ticker = ticker.upper()
        quantity = float(quantity)
        purchase_price = float(purchase_price)
        if ticker in self.assets:
            existing = self.assets[ticker]
            total_qty = existing.quantity + quantity
            if total_qty <= 0:
                return False
            total_cost = existing.quantity * existing.purchase_price + quantity * purchase_price
            existing.quantity = total_qty
            existing.purchase_price = total_cost / total_qty
        else:
            self.assets[ticker] = Asset(ticker, quantity, purchase_price)
        return True
    def remove_asset(self, ticker):
        ticker = ticker.upper()
        if ticker in self.assets:
            del self.assets[ticker]
            return True
        return False
    def update_prices(self):
        try:
            from data_fetcher import DataFetcher
            for ticker, asset in self.assets.items():
                try:
                    price = DataFetcher.get_current_price(ticker)
                    asset.current_price = float(price) if price and price > 0 else asset.purchase_price
                except Exception:
                    asset.current_price = asset.purchase_price
        except Exception:
            for asset in self.assets.values():
                asset.current_price = asset.purchase_price
   
