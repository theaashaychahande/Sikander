
import streamlit as st
import pandas as pd
import locale
import portfolio
import risk_engine
import visualization
import data_fetcher
import config
primary = "#00d4aa"
secondary = "#355C7D"
bg_card = "#171B26"
shadow = "0 4px 12px 0 rgba(0,0,0,0.25)"
st.set_page_config(
    page_title="Sikander - Portfolio Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(f"""
<style>
body, .stApp {{ background-color: #10131A; }}
h1.main-header {{
    font-family: 'Montserrat', 'Arial', sans-serif;
    font-size: 3rem;
    color: {primary};
    text-align: center;
    padding: 0.5rem 0 0.4rem 0;
    letter-spacing: 2.5px;
    margin-bottom: 0.5rem;
    font-weight: bold;
}}
.header-tagline {{
    font-size: 1.15rem;
    color: #9ed7cb;
    text-align: center;
    margin-bottom: 1.25rem;
}}
.sidebar-card {{
    background: #19202C;
    padding: 1.2rem 1.1rem;
    margin-bottom: 1.2rem;
    border-radius: 12px;
    box-shadow: {shadow};
}}
.sidebar-section-title {{
    color: {primary};
    font-weight: 600;
    font-size: 1.1rem;
    letter-spacing: .5px;
    margin: .7rem 0 .3rem 0;
}}
.kpi-card {{
    background: {bg_card};
    border-radius: 11px;
    margin-bottom: 10px;
    padding: 1.2rem 1.1rem;
    box-shadow: {shadow};
    min-height: 90px;
    text-align: center;
}}
.metric-label {{
    font-size: 1.13rem;
    color: #b1b8cf;
    margin-bottom: 0.4em;
    letter-spacing:0.2px;
}}
.metric-main {{
    font-size: 2.2rem;
    font-weight: 700;
    color: {primary};
    letter-spacing:1.3px;
}}
.metric-delta.pos {{ color: #33EEA0; }}
.metric-delta.neg {{ color: #FF6B6B; }}
.risk-positive {{ color: #33EEA0 !important; }}
.risk-negative {{ color: #FF6B6B !important; }}
.tab-header[data-baseweb="tab"] {{
    font-size:1.13rem;
    color:{secondary};
    font-weight:600;
}}
hr {{ border: 1px solid #222945; margin: 1.4em 0 1em 0; }}
.stButton>button, .stDownloadButton>button {{
    background: {primary} !important;
    color: #171B26 !important;
    border-radius: 7px !important;
    box-shadow: {shadow};
    border:none !important;
    font-weight: bold;
    transition: box-shadow 0.2s;
}}
.stButton>button:hover, .stDownloadButton>button:hover {{
    box-shadow: 0 8px 24px 0 rgba(0,0,0,0.25);
    background: #20eeba !important;
}}
</style>
""", unsafe_allow_html=True)
def format_inr(amount):
    try:
        return "₹" + locale.format_string("%0.2f", amount, grouping=True)
    except Exception:
       
        s = f"{amount:,.2f}"
        parts = s.split('.')
        n = parts[0]
        if len(n) > 3:
            n = n[:-3][::-1]
            n = ','.join([n[i:i+2] for i in range(0, len(n), 2)]).rstrip(',')[::-1] + ',' + parts[0][-3:]
        else:
            n = parts[0]
        return f"₹{n}.{parts[1]}"
def format_money(amount, inr_mode, rate):
    if inr_mode:
        amount_inr = amount * rate
        return format_inr(amount_inr)
    else:
        return f"${amount:,.2f}"
def format_metric(amount, inr_mode, rate):
    if inr_mode:
        return format_inr(amount * rate)
    else:
        return f"${amount:,.2f}"
class SikanderApp:
    def __init__(self):
        self.init_session_state()
    def init_session_state(self):
        if 'portfolio' not in st.session_state:
            st.session_state.portfolio = portfolio.Portfolio("My Portfolio")
        if 'risk_engine' not in st.session_state:
            st.session_state.risk_engine = risk_engine.RiskEngine(st.session_state.portfolio)
        if 'currency' not in st.session_state:
            st.session_state.currency = 'USD'
        if 'usd_inr_rate' not in st.session_state:
            st.session_state.usd_inr_rate = 83.0
    def render_sidebar(self):
        st.sidebar.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.sidebar.markdown('<div class="sidebar-section-title">🌏 Currency Options</div>', unsafe_allow_html=True)
        currency = st.sidebar.radio(
            "Display Portfolio In:", ["USD", "INR"], 
            index=0 if st.session_state.currency == "USD" else 1,
            key='currency', horizontal=True)
        usd_inr_rate = st.sidebar.number_input(
            "USD→INR Rate", min_value=70.0, max_value=150.0, value=st.session_state.usd_inr_rate, step=0.1, format="%.2f",
            help="Used for INR portfolio conversion", key='usd_inr_rate')
        st.sidebar.markdown('<hr>', unsafe_allow_html=True)
        st.sidebar.markdown('<div class="sidebar-section-title">🏦 Portfolio Management</div>', unsafe_allow_html=True)
        st.sidebar.text_input(
            "Portfolio Name",
            key='portfolio_name',
            value=st.session_state.portfolio.name,
            help="Set a name for your custom portfolio"
        )
        st.sidebar.markdown('<hr>', unsafe_allow_html=True)
        st.sidebar.markdown('<div class="sidebar-section-title">➕ Add New Asset</div>', unsafe_allow_html=True)
        with st.sidebar.form("add_asset_form", clear_on_submit=True):
            ticker = st.text_input("Ticker", placeholder="AAPL or BTC-USD").upper()
            quantity = st.number_input("Quantity", min_value=0.0, value=1.0, step=1.0)
            if st.session_state.currency == 'INR':
                price_label = "Purchase Price (₹) [converted to USD for logic]"
            else:
                price_label = "Purchase Price ($)"
            purchase_price = st.number_input(price_label, min_value=0.0, value=100.0, step=0.1)
            submitted = st.form_submit_button("Add Asset")
            if submitted:
                if ticker and quantity > 0 and purchase_price > 0:
                    if data_fetcher.DataFetcher.validate_ticker(ticker):
                        
                        price_usd = purchase_price if st.session_state.currency == 'USD' else purchase_price / st.session_state.usd_inr_rate
                        st.session_state.portfolio.add_asset(ticker, quantity, price_usd)
                        st.sidebar.success(f"Added {quantity} shares of {ticker}")
                    else:
                        st.sidebar.error("Invalid ticker symbol")
                else:
                    st.sidebar.error("Please fill all fields correctly.")
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
        st.sidebar.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.sidebar.markdown('<div class="sidebar-section-title">⚡ Quick Add Popular Assets</div>', unsafe_allow_html=True)
        selected_category = st.sidebar.selectbox(
            "Asset Category", list(config.POPULAR_ASSETS.keys()))
        col1, col2 = st.sidebar.columns([2,1])
        with col1:
            quick_ticker = st.selectbox("Asset", config.POPULAR_ASSETS[selected_category], key="quick_asset")
        with col2:
            quick_quantity = st.number_input("Qty", min_value=1.0, value=1.0, step=1.0, key="quick_qty")
        if st.sidebar.button("Quick Add"):
            current_price = data_fetcher.DataFetcher.get_current_price(quick_ticker)
            st.session_state.portfolio.add_asset(quick_ticker, quick_quantity, current_price)
            st.sidebar.success(f"Added {quick_quantity} shares of {quick_ticker}")
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
        st.sidebar.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.sidebar.markdown('<div class="sidebar-section-title">🧰 Portfolio Operations</div>', unsafe_allow_html=True)
        if st.sidebar.button("Clear Portfolio"):
            st.session_state.portfolio = portfolio.Portfolio(
                st.session_state.portfolio.name)
            st.session_state.risk_engine = risk_engine.RiskEngine(st.session_state.portfolio)
            st.rerun()
        st.sidebar.info("Tip: You can edit the details of assets below from the Holdings tab.")
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
    def render_dashboard(self):
        st.markdown('<h1 class="main-header">Sikander <span style="font-weight:300;font-size:2.2rem;vertical-align:middle;">📊</span></h1>', unsafe_allow_html=True)
        st.markdown('<div class="header-tagline">Modern, beautiful, and understandable portfolio risk analytics for everyone.</div>', unsafe_allow_html=True)
        self.render_portfolio_summary()
        st.markdown("<hr>", unsafe_allow_html=True)
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Overview", "⚖️ Allocation", "📊 Risk Analysis", "📋 Holdings"
        ])
        with tab1:
            self.render_overview_tab()
        with tab2:
            self.render_allocation_tab()
        with tab3:
            self.render_risk_tab()
        with tab4:
            self.render_holdings_tab()
    def render_portfolio_summary(self):
        summary = st.session_state.portfolio.get_portfolio_summary()
        if not summary:
            st.info("Your portfolio is empty. Add some assets to get started!")
            return
        kpi_cols = st.columns(5)
        inr_mode = st.session_state.currency == 'INR'
        rate = st.session_state.usd_inr_rate
        metrics = [
            ("Total Invested", format_metric(summary['total_invested'], inr_mode, rate), None),
            ("Current Value", format_metric(summary['total_current_value'], inr_mode, rate), f"{summary['total_pl_percent']:.2f}%"),
            ("Total P&L", format_metric(summary['total_pl'], inr_mode, rate), f"{summary['total_pl_percent']:.2f}%", summary['total_pl'] >= 0),
            ("Daily P&L", format_metric(summary['daily_pl'], inr_mode, rate), None),
            ("Assets", f"{summary['asset_count']}", None)
        ]
        labels = ["💸", "💰", "📈", "🔄", "📦"]
        for i, (label, value, delta, *args) in enumerate(metrics):
            with kpi_cols[i]:
                delta_str = f"<div class='metric-delta {'pos' if delta is None or args and args[0] else 'neg'}'>{delta or ''}</div>" if delta else ""
                st.markdown(f"""
                    <div class='kpi-card'>
                        <div class='metric-label'>{labels[i]} {label}</div>
                        <div class='metric-main'>{value}</div>
                        {delta_str}
                    </div>
                """, unsafe_allow_html=True)
    def render_overview_tab(self):
        col1, col2 = st.columns([2, 1])
        inr_mode = st.session_state.currency == 'INR'
        rate = st.session_state.usd_inr_rate
        with col1:
            portfolio_returns = st.session_state.risk_engine.get_portfolio_returns()
            benchmark_returns = data_fetcher.DataFetcher.get_daily_returns(st.session_state.portfolio.benchmark)
            if not portfolio_returns.empty:
                performance_chart = visualization.PortfolioVisualizer.create_performance_chart(
                    portfolio_returns, benchmark_returns
                )
                st.plotly_chart(performance_chart, use_container_width=True)
            else:
                st.info("Add more assets and wait for historical data to load.")
        with col2:
            risk_metrics = st.session_state.risk_engine.get_comprehensive_risk_metrics()
            if risk_metrics:
                st.subheader("Quick Risk Snapshot")
                metrics_data = {
                    "Annual Volatility": f"{risk_metrics['volatility_annual']:.2%}",
                    "Sharpe Ratio": f"{risk_metrics['sharpe_ratio']:.2f}",
                    "Beta (vs SPY)": f"{risk_metrics['beta']:.2f}",
                    "Max Drawdown": f"{risk_metrics['max_drawdown']:.2%}",
                    "VaR (95%)": f"{risk_metrics['var_95']:.2%}",
                    "Correlation": f"{risk_metrics['correlation']:.2f}"
                }
                for metric, value in metrics_data.items():
                    st.markdown(f"**{metric}:** <span style='color:{primary};font-size:1.3rem;font-weight:600'>{value}</span>", unsafe_allow_html=True)
    def render_allocation_tab(self):
        allocation_df = st.session_state.portfolio.get_asset_allocation()
        if allocation_df.empty:
            st.info("No assets in portfolio.")
            return
        inr_mode = st.session_state.currency == 'INR'
        rate = st.session_state.usd_inr_rate
        col1, col2 = st.columns([1, 1])
        with col1:
            pie_chart = visualization.PortfolioVisualizer.create_allocation_pie_chart(allocation_df)
            st.plotly_chart(pie_chart, use_container_width=True)
        with col2:
            st.subheader("Asset Allocation Details 🧮")
            display_df = allocation_df.copy()
            display_df['Weight (%)'] = display_df['Weight (%)'].round(2)
            display_df['P&L (%)'] = display_df['P&L (%)'].round(2)
            for colnm in ['Purchase Price','Current Price','Current Value','P&L ($)']:
                if colnm in display_df.columns:
                    display_df[colnm] = display_df[colnm].apply(lambda x: format_money(x, inr_mode, rate))
            display_df = display_df.rename(columns={
                'Purchase Price':'Purchase Price (' + ('₹' if inr_mode else '$') + ')',
                'Current Price':'Current Price (' + ('₹' if inr_mode else '$') + ')',
                'Current Value':'Current Value (' + ('₹' if inr_mode else '$') + ')',
                'P&L ($)':'P&L (' + ('₹' if inr_mode else '$') + ')'
            })
            st.dataframe(
                display_df[['Ticker', 'Weight (%)', 'Current Value ('+('₹' if inr_mode else '$')+')', 'P&L ('+('₹' if inr_mode else '$')+')', 'P&L (%)']],
                use_container_width=True
            )
    def render_risk_tab(self):
        risk_metrics = st.session_state.risk_engine.get_comprehensive_risk_metrics()
        if not risk_metrics:
            st.info("Add assets to calculate risk metrics")
            return
        col1, col2 = st.columns([1, 1])
        with col1:
            risk_gauges = visualization.PortfolioVisualizer.create_risk_metrics_gauge(risk_metrics)
            st.plotly_chart(risk_gauges, use_container_width=True)
        with col2:
            st.subheader("Risk Metrics Explanation 🧠")
            risk_explanations = {
                "Volatility": "Measures how much the portfolio value fluctuates. Higher volatility = higher risk.",
                "Sharpe Ratio": "Measures risk-adjusted return. >1 is good, >2 is excellent.",
                "Beta": "Measures sensitivity to market movements. 1 = moves with market, <1 = less volatile, >1 = more volatile.",
                "Max Drawdown": "Largest peak-to-trough decline. Shows worst-case historical loss.",
                "Value at Risk (VaR)": "Maximum expected loss over a specific time period at a given confidence level.",
                "Correlation": "How closely the portfolio moves with the benchmark."
            }
            for metric, explanation in risk_explanations.items():
                with st.expander(f"{metric}"):
                    st.write(explanation)
    def render_holdings_tab(self):
        allocation_df = st.session_state.portfolio.get_asset_allocation()
        if allocation_df.empty:
            st.info("No assets in portfolio.")
            return
        st.subheader("Current Holdings 📋")
        inr_mode = st.session_state.currency == 'INR'
        rate = st.session_state.usd_inr_rate
        for _, row in allocation_df.iterrows():
            col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])
            with col1:
                st.write(f"**{row['Ticker']}**")
            with col2:
                st.write(f"Qty: {row['Quantity']:.0f}")
            with col3:
                st.write(format_money(row['Current Price'], inr_mode, rate))
            with col4:
                pl_color = "risk-positive" if row['P&L ($)'] >= 0 else "risk-negative"
                st.markdown(f'<span class="{pl_color}">{format_money(row["P&L ($)"], inr_mode, rate)}</span>', unsafe_allow_html=True)
            with col5:
                pl_pct_color = "risk-positive" if row['P&L (%)'] >= 0 else "risk-negative"
                st.markdown(f'<span class="{pl_pct_color}">{row["P&L (%)"]:.2f}%</span>', unsafe_allow_html=True)
            with col6:
                if st.button("Remove", key=f"remove_{row['Ticker']}"):
                    st.session_state.portfolio.remove_asset(row['Ticker'])
                    st.rerun()
        st.subheader("Export Data 🚀")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Export to CSV"):
                csv = allocation_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"{st.session_state.portfolio.name}_holdings.csv",
                    mime="text/csv"
                )
        with col2:
            if st.button("Generate Report"):
                st.info("Advanced reporting feature coming soon!")
    def run(self):
        self.render_sidebar()
        self.render_dashboard()
if __name__ == "__main__":
    app = SikanderApp()
    app.run()
    st.markdown(
        """
        <style>
        .aashay-footer {
            position: fixed;
            left: 0; right: 0; bottom: 0;
            width: 100vw;
            padding: 0.36em 0 0.14em 0;
            color: #b0b7c3;
            background: rgba(0,0,0,0.00);
            font-size: 0.91em;
            letter-spacing: 0.09em;
            text-align: center;
            z-index:9999;
            pointer-events: none;
            font-family: 'Inter', 'Montserrat', sans-serif;
        }
        </style>
        <div class='aashay-footer'>Programmed and licensed by Aashay Chahande</div>
        """,
        unsafe_allow_html=True
    )
