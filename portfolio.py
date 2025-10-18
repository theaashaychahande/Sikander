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
            # If DataFetcher import or lookup fails, fall back to purchase price
            for asset in self.assets.values():
                asset.current_price = asset.purchase_price

    def get_portfolio_summary(self):
        self.update_prices()
        if not self.assets:
            return {}
        total_invested = sum(a.quantity * a.purchase_price for a in self.assets.values())
        total_current = sum(a.quantity * a.current_price for a in self.assets.values())
        total_pl = total_current - total_invested
        total_pl_percent = (total_pl / total_invested * 100) if total_invested > 0 else 0.0
        daily_pl = 0.0
        return {
            'total_invested': total_invested,
            'total_current_value': total_current,
            'total_pl': total_pl,
            'total_pl_percent': total_pl_percent,
            'daily_pl': daily_pl,
            'asset_count': len(self.assets),
        }
    def get_asset_allocation(self):
        self.update_prices()
        total_value = sum(a.quantity * a.current_price for a in self.assets.values())
        if total_value <= 0:
            return pd.DataFrame()
        rows = []
        for ticker, asset in self.assets.items():
            current_value = asset.quantity * asset.current_price
            weight = (current_value / total_value) * 100 if total_value > 0 else 0.0
            pl_dollar = current_value - (asset.quantity * asset.purchase_price)
            pl_percent = ((asset.current_price - asset.purchase_price) / asset.purchase_price * 100) if asset.purchase_price > 0 else 0.0
            rows.append({
                'Ticker': ticker,
                'Quantity': asset.quantity,
                'Purchase Price': round(asset.purchase_price, 2),
                'Current Price': round(asset.current_price, 2),
                'Current Value': round(current_value, 2),
                'Weight (%)': round(weight, 2),
                'P&L ($)': round(pl_dollar, 2),
                'P&L (%)': round(pl_percent, 2),
            })
        return pd.DataFrame(rows)
   
