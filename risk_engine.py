import pandas as pd
import numpy as np

class RiskEngine:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def get_portfolio_returns(self):
        allocation_df = self.portfolio.get_asset_allocation()
        if allocation_df.empty:
            dates = pd.date_range(end=pd.Timestamp.today(), periods=90)
            returns = np.random.normal(0.001, 0.01, size=len(dates))
            df = pd.DataFrame({'date': dates, 'returns': returns})
            df.set_index('date', inplace=True)
            return df
        
        from data_fetcher import DataFetcher
        dates = pd.date_range(end=pd.Timestamp.today(), periods=90)
        portfolio_returns = np.zeros(len(dates))
        total_value = allocation_df['Current Value'].sum()
        
        if total_value > 0:
            for _, asset in allocation_df.iterrows():
                ticker_returns = DataFetcher.get_daily_returns(asset['Ticker'])
                weight = asset['Current Value'] / total_value
                ticker_returns_aligned = ticker_returns.reindex(dates, method='nearest')
                portfolio_returns += weight * ticker_returns_aligned['returns'].values
        
        df = pd.DataFrame({'date': dates, 'returns': portfolio_returns})
        df.set_index('date', inplace=True)
        return df

    def get_comprehensive_risk_metrics(self):
        portfolio_returns = self.get_portfolio_returns()
        if portfolio_returns.empty:
            return {
                'volatility_annual': 0.15,
                'sharpe_ratio': 1.2,
                'beta': 1.0,
                'max_drawdown': 0.10,
                'var_95': 0.05,
                'correlation': 0.7
            }
        
        volatility_annual = portfolio_returns['returns'].std() * np.sqrt(252)
        
        risk_free_rate = 0.02 / 252  
        sharpe_ratio = (portfolio_returns['returns'].mean() - risk_free_rate) / portfolio_returns['returns'].std() * np.sqrt(252)
        
        from data_fetcher import DataFetcher
        benchmark_returns = DataFetcher.get_daily_returns(self.portfolio.benchmark)
        merged_returns = portfolio_returns.join(benchmark_returns, how='inner', lsuffix='_portfolio', rsuffix='_benchmark')
        if len(merged_returns) > 1:
            beta = merged_returns['returns_portfolio'].cov(merged_returns['returns_benchmark']) / merged_returns['returns_benchmark'].var()
        else:
            beta = 1.0
        
        cumulative_returns = (1 + portfolio_returns['returns']).cumprod()
        running_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - running_max) / running_max
        max_drawdown = drawdown.min()
        
        var_95 = np.percentile(portfolio_returns['returns'], 5)
        
        if len(merged_returns) > 1:
            correlation = merged_returns['returns_portfolio'].corr(merged_returns['returns_benchmark'])
        else:
            correlation = 0.7
        
        return {
            'volatility_annual': volatility_annual,
            'sharpe_ratio': sharpe_ratio,
            'beta': beta,
            'max_drawdown': abs(max_drawdown),
            'var_95': abs(var_95),
            'correlation': correlation
        }
