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
accent = "#FF6B6B"
bg_dark = "#10131A"
bg_card = "#19202C"
bg_card_light = "#222945"
shadow = "0 4px 20px rgba(0,0,0,0.3)"

st.set_page_config(
    page_title="Sikander - Portfolio Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

body, .stApp {{ 
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: #e0e0e0;
    font-family: 'Inter', sans-serif;
}}

.main-header {{
    font-family: 'Montserrat', sans-serif;
    font-size: 3.5rem;
    background: linear-gradient(90deg, {primary}, #00aaff, #00d4ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    padding: 1rem 0;
    letter-spacing: 3px;
    margin-bottom: 0.5rem;
    font-weight: 800;
    animation: gradientShift 8s ease infinite;
    background-size: 300% 300%;
}}

@keyframes gradientShift {{
    0% {{background-position: 0% 50%;}}
    50% {{background-position: 100% 50%;}}
    100% {{background-position: 0% 50%;}}
}}

.header-tagline {{
    font-size: 1.3rem;
    color: #a0d2c3;
    text-align: center;
    margin-bottom: 2rem;
    font-weight: 300;
    letter-spacing: 1px;
    animation: fadeIn 2s ease-in;
}}

@keyframes fadeIn {{
    from {{opacity: 0;}}
    to {{opacity: 1;}}
}}

.sidebar-card {{
    background: {bg_card};
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    border-radius: 16px;
    box-shadow: {shadow};
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid rgba(0, 212, 170, 0.2);
}}

.sidebar-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.4);
}}

.sidebar-section-title {{
    color: {primary};
    font-weight: 700;
    font-size: 1.3rem;
    letter-spacing: 1px;
    margin: 1rem 0 0.7rem 0;
    text-transform: uppercase;
    position: relative;
    padding-bottom: 0.5rem;
}}

.sidebar-section-title::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 50px;
    height: 3px;
    background: {primary};
    border-radius: 3px;
}}

.kpi-card {{
    background: {bg_card};
    border-radius: 16px;
    margin-bottom: 15px;
    padding: 1.5rem;
    box-shadow: {shadow};
    min-height: 120px;
    text-align: center;
    transition: all 0.3s ease;
    border: 2px solid transparent;
    background: linear-gradient({bg_dark}, {bg_dark}) padding-box,
                linear-gradient(90deg, {primary}, #00aaff) border-box;
}}

.kpi-card:hover {{
    transform: scale(1.03);
    box-shadow: 0 8px 25px rgba(0, 212, 170, 0.2);
}}

.metric-label {{
    font-size: 1.2rem;
    color: #b1b8cf;
    margin-bottom: 0.5em;
    letter-spacing: 0.5px;
    font-weight: 500;
}}

.metric-main {{
    font-size: 2.5rem;
    font-weight: 800;
    color: {primary};
    letter-spacing: 1.5px;
    text-shadow: 0 0 10px rgba(0, 212, 170, 0.3);
}}

.metric-delta.pos {{ 
    color: #33EEA0; 
    font-weight: 600;
}}

.metric-delta.neg {{ 
    color: {accent}; 
    font-weight: 600;
}}

.risk-positive {{ color: #33EEA0 !important; }}
.risk-negative {{ color: {accent} !important; }}

.stTabs [data-baseweb="tab-list"] {{
    gap: 10px;
    background: {bg_card_light};
    padding: 10px;
    border-radius: 12px;
}}

.stTabs [data-baseweb="tab"] {{
    background: {bg_card};
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 1.1rem;
    transition: all 0.3s ease;
}}

.stTabs [data-baseweb="tab"]:hover {{
    background: linear-gradient(90deg, {primary}, #00aaff);
    color: {bg_dark} !important;
}}

.stTabs [aria-selected="true"] {{
    background: linear-gradient(90deg, {primary}, #00aaff) !important;
    color: {bg_dark} !important;
}}

.stButton>button, .stDownloadButton>button {{
    background: linear-gradient(90deg, {primary}, #00aaff) !important;
    color: {bg_dark} !important;
    border-radius: 12px !important;
    box-shadow: {shadow};
    border: none !important;
    font-weight: 700;
    font-size: 1rem;
    padding: 0.7rem 1.5rem;
    transition: all 0.3s ease;
    letter-spacing: 0.5px;
}}

.stButton>button:hover, .stDownloadButton>button:hover {{
    box-shadow: 0 10px 30px rgba(0, 212, 170, 0.4);
    transform: translateY(-3px);
}}

.stSelectbox, .stTextInput, .stNumberInput {{
    background: {bg_card_light} !important;
    border-radius: 12px !important;
}}

@keyframes pulse {{
    0% {{ transform: scale(1); }}
    50% {{ transform: scale(1.05); }}
    100% {{ transform: scale(1); }}
}}

.pulse {{
    animation: pulse 2s infinite;
}}

::-webkit-scrollbar {{
    width: 10px;
}}

::-webkit-scrollbar-track {{
    background: {bg_dark};
}}

::-webkit-scrollbar-thumb {{
    background: {primary};
    border-radius: 5px;
}}

hr {{ 
    border: 1px solid {bg_card_light}; 
    margin: 2em 0 1.5em 0; 
}}

.aashay-footer {{
    position: fixed;
    left: 0; right: 0; bottom: 0;
    width: 100vw;
    padding: 0.5em 0 0.2em 0;
    color: #b0b7c3;
    background: rgba(0,0,0,0.3);
    font-size: 0.95em;
    letter-spacing: 1px;
    text-align: center;
    z-index:9999;
    pointer-events: none;
    font-family: 'Inter', 'Montserrat', sans-serif;
    backdrop-filter: blur(5px);
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
            "Asset Category", list(config.POPULAR_ASSETS.keys()),
            help="Select a category of popular assets")
        col1, col2 = st.sidebar.columns([2,1])
        with col1:
            quick_ticker = st.selectbox("Asset", config.POPULAR_ASSETS[selected_category], key="quick_asset",
                                       help="Select an asset to quickly add to your portfolio")
        with col2:
            quick_quantity = st.number_input("Qty", min_value=1.0, value=1.0, step=1.0, key="quick_qty",
                                            help="Enter the quantity of assets to add")
        if st.sidebar.button("🚀 Quick Add", use_container_width=True):
            current_price = data_fetcher.DataFetcher.get_current_price(quick_ticker)
            st.session_state.portfolio.add_asset(quick_ticker, quick_quantity, current_price)
            st.sidebar.success(f"✅ Added {quick_quantity} shares of {quick_ticker}")
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
        st.sidebar.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.sidebar.markdown('<div class="sidebar-section-title">🧰 Portfolio Operations</div>', unsafe_allow_html=True)
        if st.sidebar.button("🗑️ Clear Portfolio", use_container_width=True, 
                            help="Remove all assets from your portfolio"):
            st.session_state.portfolio = portfolio.Portfolio(
                st.session_state.portfolio.name)
            st.session_state.risk_engine = risk_engine.RiskEngine(st.session_state.portfolio)
            st.rerun()
        st.sidebar.info("💡 Tip: You can edit the details of assets below from the Holdings tab.")
        st.sidebar.markdown('</div>', unsafe_allow_html=True)

    def render_dashboard(self):
        st.markdown('''
        <div style="text-align:center; margin-bottom:10px;">
            <h1 class="main-header pulse">Sikander <span style="font-weight:300;font-size:2.5rem;vertical-align:middle;">📊</span></h1>
            <div class="header-tagline">Modern, beautiful, and understandable portfolio risk analytics for everyone.</div>
            <div style="display:flex; justify-content:center; gap:20px; margin-top:15px;">
                <span style="font-size:2rem; animation: pulse 2s infinite;">📈</span>
                <span style="font-size:2rem; animation: pulse 2.5s infinite;">💰</span>
                <span style="font-size:2rem; animation: pulse 3s infinite;">📊</span>
                <span style="font-size:2rem; animation: pulse 2.2s infinite;">💼</span>
                <span style="font-size:2rem; animation: pulse 2.8s infinite;">🏦</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
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
        icons = ["arrow-down-circle", "arrow-up-circle", "bar-chart-2", "trending-up", "package"]
        for i, (label, value, delta, *args) in enumerate(metrics):
            with kpi_cols[i]:
                delta_str = f"<div class='metric-delta {'pos' if delta is None or args and args[0] else 'neg'}'>{delta or ''}</div>" if delta else ""
                animation_class = "pulse" if label == "Total P&L" and summary['total_pl'] >= 0 else ""
                card_style = "border: 2px solid #FF6B6B;" if label == "Total P&L" and summary['total_pl'] < 0 else ""
                st.markdown(f"""
                    <div class='kpi-card {animation_class}' style='{card_style}'>
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
