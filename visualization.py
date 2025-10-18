import plotly.graph_objects as go

class PortfolioVisualizer:
    @staticmethod
    def create_performance_chart(portfolio_returns, benchmark_returns):
        fig = go.Figure()
        if not portfolio_returns.empty:
            fig.add_trace(go.Scatter(
                x=portfolio_returns.index,
                y=(1 + portfolio_returns['returns']).cumprod(),
                mode='lines',
                name='Portfolio'))
        if not benchmark_returns.empty:
            fig.add_trace(go.Scatter(
                x=benchmark_returns.index,
                y=(1 + benchmark_returns['returns']).cumprod(),
                mode='lines',
                name='Benchmark'))
        fig.update_layout(title='Portfolio vs Benchmark Performance')
        return fig

    @staticmethod
    def create_allocation_pie_chart(allocation_df):
        if allocation_df.empty:
            labels, values = [], []
        else:
            labels = allocation_df['Ticker']
            values = allocation_df['Current Value']
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_layout(title='Asset Allocation')
        return fig

    @staticmethod
    def create_risk_metrics_gauge(risk_metrics):
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode='gauge+number',
            value=risk_metrics.get('volatility_annual', 0),
            title={'text': 'Annual Volatility'}
        ))
        fig.update_layout(title='Risk Metrics Gauges')
        return fig
