import plotly.graph_objects as go
import plotly.express as px

class PortfolioVisualizer:
    @staticmethod
    def create_performance_chart(portfolio_returns, benchmark_returns):
        fig = go.Figure()
        
        if not portfolio_returns.empty:
            portfolio_cumulative = (1 + portfolio_returns['returns']).cumprod()
            fig.add_trace(go.Scatter(
                x=portfolio_returns.index,
                y=portfolio_cumulative,
                mode='lines',
                name='Portfolio',
                line=dict(width=4, color='#00d4aa'),
                fill='tonexty',
                fillcolor='rgba(0, 212, 170, 0.1)',
                hovertemplate=
                '<b>Portfolio</b><br>'+\
                'Date: %{x}<br>'+\
                'Value: %{y:.3f}<br>'+\
                '<extra></extra>'
            ))
        
        if not benchmark_returns.empty:
            benchmark_cumulative = (1 + benchmark_returns['returns']).cumprod()
            fig.add_trace(go.Scatter(
                x=benchmark_returns.index,
                y=benchmark_cumulative,
                mode='lines',
                name='Benchmark (SPY)',
                line=dict(width=3, color='#355C7D', dash='dot'),
                hovertemplate=
                '<b>Benchmark (SPY)</b><br>'+\
                'Date: %{x}<br>'+\
                'Value: %{y:.3f}<br>'+\
                '<extra></extra>'
            ))
        
        fig.update_layout(
            title=dict(
                text='Portfolio vs Benchmark Performance',
                x=0.5,
                xanchor='center',
                font=dict(size=20, color='#00d4aa')
            ),
            xaxis=dict(
                title='Date',
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(255, 255, 255, 0.1)',
                zeroline=False
            ),
            yaxis=dict(
                title='Cumulative Return',
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(255, 255, 255, 0.1)',
                zeroline=False
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            hovermode='x unified',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1,
                bgcolor='rgba(0,0,0,0)'
            ),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        return fig

    @staticmethod
    def create_allocation_pie_chart(allocation_df):
        if allocation_df.empty:
            labels, values = [], []
        else:
            labels = allocation_df['Ticker']
            values = allocation_df['Current Value']
        
        colors = ['#00d4aa', '#355C7D', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(colors=colors),
            textinfo='label+percent',
            textfont=dict(size=14),
            hovertemplate=
            '<b>%{label}</b><br>'+\
            'Value: $%{value:.2f}<br>'+\
            'Percentage: %{percent}<br>'+\
            '<extra></extra>'
        )])
        
        fig.update_layout(
            title=dict(
                text='Asset Allocation',
                x=0.5,
                xanchor='center',
                font=dict(size=20, color='#00d4aa')
            ),
            annotations=[dict(
                text='Allocation', 
                x=0.5, y=0.5, 
                font_size=16, 
                showarrow=False
            )],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        return fig

    @staticmethod
    def create_risk_metrics_gauge(risk_metrics):
        if not risk_metrics:
            return go.Figure()
        
        from plotly.subplots import make_subplots
        
        fig = make_subplots(
            rows=2, cols=3,
            specs=[[{'type': 'indicator'}]*3, [{'type': 'indicator'}]*3],
            subplot_titles=('Annual Volatility', 'Sharpe Ratio', 'Beta', 
                           'Max Drawdown', 'VaR (95%)', 'Correlation')
        )
        
        fig.add_trace(go.Indicator(
            mode='gauge+number',
            value=risk_metrics.get('volatility_annual', 0),
            title={'text': 'Volatility', 'font': {'size': 16}},
            gauge={
                'axis': {'range': [0, 0.5], 'tickwidth': 1, 'tickcolor': '#e0e0e0'},
                'bar': {'color': '#00d4aa'},
                'bgcolor': 'rgba(0,0,0,0)',
                'borderwidth': 2,
                'bordercolor': '#355C7D',
                'steps': [
                    {'range': [0, 0.15], 'color': '#33EEA0'},
                    {'range': [0.15, 0.3], 'color': '#FFEAA7'},
                    {'range': [0.3, 0.5], 'color': '#FF6B6B'}],
                'threshold': {
                    'line': {'color': 'white', 'width': 4},
                    'thickness': 0.75,
                    'value': risk_metrics.get('volatility_annual', 0)}
            }
        ), row=1, col=1)
        
        fig.add_trace(go.Indicator(
            mode='gauge+number',
            value=risk_metrics.get('sharpe_ratio', 0),
            title={'text': 'Sharpe Ratio', 'font': {'size': 16}},
            gauge={
                'axis': {'range': [-1, 3], 'tickwidth': 1, 'tickcolor': '#e0e0e0'},
                'bar': {'color': '#00d4aa'},
                'bgcolor': 'rgba(0,0,0,0)',
                'borderwidth': 2,
                'bordercolor': '#355C7D',
                'steps': [
                    {'range': [-1, 0], 'color': '#FF6B6B'},
                    {'range': [0, 1], 'color': '#FFEAA7'},
                    {'range': [1, 3], 'color': '#33EEA0'}],
                'threshold': {
                    'line': {'color': 'white', 'width': 4},
                    'thickness': 0.75,
                    'value': risk_metrics.get('sharpe_ratio', 0)}
            }
        ), row=1, col=2)
        
        fig.add_trace(go.Indicator(
            mode='gauge+number',
            value=risk_metrics.get('beta', 0),
            title={'text': 'Beta', 'font': {'size': 16}},
            gauge={
                'axis': {'range': [0, 2], 'tickwidth': 1, 'tickcolor': '#e0e0e0'},
                'bar': {'color': '#00d4aa'},
                'bgcolor': 'rgba(0,0,0,0)',
                'borderwidth': 2,
                'bordercolor': '#355C7D',
                'steps': [
                    {'range': [0, 0.8], 'color': '#33EEA0'},
                    {'range': [0.8, 1.2], 'color': '#FFEAA7'},
                    {'range': [1.2, 2], 'color': '#FF6B6B'}],
                'threshold': {
                    'line': {'color': 'white', 'width': 4},
                    'thickness': 0.75,
                    'value': risk_metrics.get('beta', 0)}
            }
        ), row=1, col=3)
        
        fig.add_trace(go.Indicator(
            mode='gauge+number',
            value=risk_metrics.get('max_drawdown', 0),
            title={'text': 'Drawdown', 'font': {'size': 16}},
            gauge={
                'axis': {'range': [0, 0.5], 'tickwidth': 1, 'tickcolor': '#e0e0e0'},
                'bar': {'color': '#FF6B6B'},
                'bgcolor': 'rgba(0,0,0,0)',
                'borderwidth': 2,
                'bordercolor': '#355C7D',
                'steps': [
                    {'range': [0, 0.1], 'color': '#33EEA0'},
                    {'range': [0.1, 0.25], 'color': '#FFEAA7'},
                    {'range': [0.25, 0.5], 'color': '#FF6B6B'}],
                'threshold': {
                    'line': {'color': 'white', 'width': 4},
                    'thickness': 0.75,
                    'value': risk_metrics.get('max_drawdown', 0)}
            }
        ), row=2, col=1)
        
        fig.add_trace(go.Indicator(
            mode='gauge+number',
            value=risk_metrics.get('var_95', 0),
            title={'text': 'VaR', 'font': {'size': 16}},
            gauge={
                'axis': {'range': [0, 0.2], 'tickwidth': 1, 'tickcolor': '#e0e0e0'},
                'bar': {'color': '#FF6B6B'},
                'bgcolor': 'rgba(0,0,0,0)',
                'borderwidth': 2,
                'bordercolor': '#355C7D',
                'steps': [
                    {'range': [0, 0.05], 'color': '#33EEA0'},
                    {'range': [0.05, 0.1], 'color': '#FFEAA7'},
                    {'range': [0.1, 0.2], 'color': '#FF6B6B'}],
                'threshold': {
                    'line': {'color': 'white', 'width': 4},
                    'thickness': 0.75,
                    'value': risk_metrics.get('var_95', 0)}
            }
        ), row=2, col=2)
        
        fig.add_trace(go.Indicator(
            mode='gauge+number',
            value=risk_metrics.get('correlation', 0),
            title={'text': 'Correlation', 'font': {'size': 16}},
            gauge={
                'axis': {'range': [-1, 1], 'tickwidth': 1, 'tickcolor': '#e0e0e0'},
                'bar': {'color': '#00d4aa'},
                'bgcolor': 'rgba(0,0,0,0)',
                'borderwidth': 2,
                'bordercolor': '#355C7D',
                'steps': [
                    {'range': [-1, -0.5], 'color': '#FF6B6B'},
                    {'range': [-0.5, 0.5], 'color': '#FFEAA7'},
                    {'range': [0.5, 1], 'color': '#33EEA0'}],
                'threshold': {
                    'line': {'color': 'white', 'width': 4},
                    'thickness': 0.75,
                    'value': risk_metrics.get('correlation', 0)}
            }
        ), row=2, col=3)
        
        fig.update_layout(
            title=dict(
                text='Risk Metrics Dashboard',
                x=0.5,
                xanchor='center',
                font=dict(size=24, color='#00d4aa')
            ),
            grid={'rows': 2, 'columns': 3},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            margin=dict(l=50, r=50, t=100, b=50)
        )
        
        return fig

