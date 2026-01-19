"""
Financial Statement Analyzer - Streamlit Web App
Upload any company's financial statements and get instant analysis
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import io

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from financial_analyzer.ingestion import ExcelReader, ExcelCleaner
from financial_analyzer.mapping import FinancialDataMapper
from financial_analyzer.analysis import RatioCalculator
from financial_analyzer.core import StatementType
from financial_analyzer.utils import format_percentage, format_ratio


# Page configuration
st.set_page_config(
    page_title="Financial Statement Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application"""
    
    # Header
    st.markdown('<div class="main-header">📊 Financial Statement Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Upload any company\'s financial statements and get instant analysis with 17+ financial ratios</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📁 Upload Files")
        st.markdown("Upload financial statements from **any company**")
        st.markdown("---")
        
        pl_file = st.file_uploader(
            "Profit & Loss Statement",
            type=['xlsx', 'xls'],
            help="Upload P&L / Income Statement"
        )
        
        bs_file = st.file_uploader(
            "Balance Sheet",
            type=['xlsx', 'xls'],
            help="Upload Balance Sheet"
        )
        
        cf_file = st.file_uploader(
            "Cash Flow Statement",
            type=['xlsx', 'xls'],
            help="Upload Cash Flow Statement"
        )
        
        st.markdown("---")
        
        analyze_button = st.button("🚀 Analyze", type="primary", use_container_width=True)
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.info("""
        This tool automatically:
        - Maps varying field names
        - Calculates 17+ ratios
        - Handles missing data
        - Works with ANY company
        """)
    
    # Main content area
    if not analyze_button:
        show_landing_page()
    else:
        if not (pl_file or bs_file or cf_file):
            st.error("⚠️ Please upload at least one financial statement file")
            return
        
        # Run analysis
        run_analysis(pl_file, bs_file, cf_file)


def show_landing_page():
    """Show landing page with instructions"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### ✨ Features")
        st.markdown("""
        - ✅ Works with **any company**
        - ✅ Intelligent field mapping
        - ✅ 17+ financial ratios
        - ✅ Multi-year analysis
        - ✅ Handles missing data
        """)
    
    with col2:
        st.markdown("### 📊 Calculated Ratios")
        st.markdown("""
        **Profitability**
        - Net Profit Margin
        - ROE, ROA
        
        **Liquidity**
        - Current Ratio
        - Cash Ratio
        
        **Leverage**
        - Debt to Equity
        - Interest Coverage
        """)
    
    with col3:
        st.markdown("### 🚀 How to Use")
        st.markdown("""
        1. Upload P&L, Balance Sheet, Cash Flow
        2. Click **Analyze** button
        3. View instant results
        4. Download analysis
        """)
    
    st.markdown("---")
    
    # Example
    with st.expander("📖 See Example Output"):
        st.markdown("""
        ### Sample Analysis: Infosys Ltd.
        
        **Company**: Infosys Ltd.  
        **Years**: 2003-2025 (23 years)  
        **Ratios Calculated**: 17
        
        | Ratio | 2023 | 2024 | 2025 |
        |-------|------|------|------|
        | Net Profit Margin (%) | 16.43 | 17.08 | 16.41 |
        | ROE (%) | - | - | - |
        | Current Ratio | 1.81 | 2.31 | 2.27 |
        | Free Cash Flow (Cr) | 25,046 | 27,411 | 37,931 |
        """)


def run_analysis(pl_file, bs_file, cf_file):
    """Run the financial analysis"""
    
    st.markdown("## 🔄 Processing...")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Ingest files
        status_text.text("📥 Step 1/4: Reading and cleaning files...")
        progress_bar.progress(25)
        
        cleaned_data = {}
        metadata = {}
        
        if pl_file:
            pl_df, pl_meta = ingest_file(pl_file, StatementType.PROFIT_LOSS)
            cleaned_data['P&L'] = pl_df
            metadata.update(pl_meta)
        
        if bs_file:
            bs_df, bs_meta = ingest_file(bs_file, StatementType.BALANCE_SHEET)
            cleaned_data['Balance Sheet'] = bs_df
            if not metadata:
                metadata.update(bs_meta)
        
        if cf_file:
            cf_df, cf_meta = ingest_file(cf_file, StatementType.CASH_FLOW)
            cleaned_data['Cash Flow'] = cf_df
            if not metadata:
                metadata.update(cf_meta)
        
        # Step 2: Map to canonical model
        status_text.text("🗺️ Step 2/4: Mapping to canonical model...")
        progress_bar.progress(50)
        
        mapper = FinancialDataMapper(cleaned_data, metadata)
        canonical_model = mapper.map_all_statements()
        
        # Step 3: Calculate ratios
        status_text.text("🧮 Step 3/4: Calculating financial ratios...")
        progress_bar.progress(75)
        
        calculator = RatioCalculator(canonical_model)
        ratios = calculator.calculate_all_ratios()
        
        # Step 4: Display results
        status_text.text("✅ Step 4/4: Generating results...")
        progress_bar.progress(100)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        # Display results
        display_results(canonical_model, ratios, mapper)
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        import traceback
        with st.expander("🔍 See error details"):
            st.code(traceback.format_exc())


def ingest_file(file, statement_type):
    """Ingest a single file"""
    
    # Save uploaded file temporarily
    temp_path = f"/tmp/{file.name}"
    with open(temp_path, "wb") as f:
        f.write(file.getbuffer())
    
    # Read and clean
    reader = ExcelReader(temp_path)
    raw_df = reader.read()
    metadata = reader.extract_metadata()
    
    cleaner = ExcelCleaner(raw_df, metadata)
    cleaned_df = cleaner.clean()
    
    return cleaned_df, metadata


def display_results(canonical_model, ratios, mapper):
    """Display analysis results"""
    
    st.markdown("## ✅ Analysis Complete!")
    
    # Company info
    st.markdown(f'<div class="success-box">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Company", canonical_model.company_name)
    with col2:
        st.metric("Years Analyzed", len(canonical_model.get_available_years()))
    with col3:
        st.metric("Ratios Calculated", len(ratios))
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Ratios", "📈 Trends", "🗺️ Mapping", "📋 Raw Data"])
    
    with tab1:
        display_ratios(canonical_model, ratios)
    
    with tab2:
        display_trends(canonical_model, ratios)
    
    with tab3:
        display_mapping_info(mapper)
    
    with tab4:
        display_raw_data(canonical_model)


def display_ratios(canonical_model, ratios):
    """Display financial ratios"""
    
    st.markdown("### 📊 Financial Ratios")
    
    years = canonical_model.get_available_years()
    
    # Group ratios by category
    categories = {
        'Profitability': [
            'Gross Profit Margin (%)',
            'Operating Profit Margin (%)',
            'Net Profit Margin (%)',
            'EBITDA Margin (%)',
            'Return on Assets (%)',
            'Return on Equity (%)'
        ],
        'Liquidity': [
            'Current Ratio',
            'Cash Ratio',
            'Working Capital Ratio'
        ],
        'Leverage': [
            'Debt to Equity',
            'Debt to Assets',
            'Equity Ratio (%)',
            'Interest Coverage'
        ],
        'Efficiency': [
            'Asset Turnover'
        ],
        'Cash Flow': [
            'Operating CF Ratio',
            'Cash Flow Margin (%)',
            'Free Cash Flow'
        ]
    }
    
    for category, ratio_list in categories.items():
        st.markdown(f"#### {category}")
        
        # Create DataFrame for this category
        category_data = {}
        for ratio_name in ratio_list:
            if ratio_name in ratios:
                category_data[ratio_name] = ratios[ratio_name]
        
        if category_data:
            df = pd.DataFrame(category_data).T
            df.columns = years
            
            # Format based on ratio type - simplified without background gradient
            try:
                # Try with background gradient
                st.dataframe(
                    df.style.format("{:.2f}", na_rep="N/A")
                          .background_gradient(cmap='RdYlGn', axis=1),
                    use_container_width=True
                )
            except ImportError:
                # Fallback: simple formatting without gradient
                st.dataframe(
                    df.style.format("{:.2f}", na_rep="N/A"),
                    use_container_width=True
                )
        else:
            st.info(f"No {category.lower()} ratios available (missing required data)")
        
        st.markdown("---")


def display_trends(canonical_model, ratios):
    """Display trend analysis"""
    
    st.markdown("### 📈 Trend Analysis")
    
    years = canonical_model.get_available_years()
    
    if len(years) < 2:
        st.warning("Need at least 2 years of data for trend analysis")
        return
    
    # Select recent years for display
    recent_years = years[-5:] if len(years) >= 5 else years
    
    # Key metrics to track
    key_metrics = [
        'Net Profit Margin (%)',
        'Return on Assets (%)',
        'Current Ratio',
        'Asset Turnover'
    ]
    
    for metric in key_metrics:
        if metric in ratios:
            values = [ratios[metric].get(year) for year in recent_years]
            
            if any(v is not None for v in values):
                df = pd.DataFrame({
                    'Year': recent_years,
                    metric: values
                })
                
                st.markdown(f"#### {metric}")
                st.line_chart(df.set_index('Year'))


def display_mapping_info(mapper):
    """Display mapping information"""
    
    st.markdown("### 🗺️ Field Mapping Summary")
    
    mapping_summary = mapper.get_mapping_summary()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Fields Mapped", mapping_summary['total_mappings'])
    
    with col2:
        st.metric("Unmapped Fields", len(mapping_summary.get('unmapped_fields', [])))
    
    # Show mappings by statement
    st.markdown("#### Mapped Fields by Statement")
    
    for stmt_type, mappings in mapping_summary.get('by_statement', {}).items():
        with st.expander(f"{stmt_type} ({len(mappings)} fields)"):
            for mapping in mappings:
                st.text(mapping)
    
    # Show unmapped fields
    if mapping_summary.get('unmapped_fields'):
        with st.expander(f"⚠️ Unmapped Fields ({len(mapping_summary['unmapped_fields'])})"):
            st.info("These fields were found but couldn't be automatically mapped. This is normal - not all fields are needed for ratio calculations.")
            for field in mapping_summary['unmapped_fields'][:20]:  # Show first 20
                st.text(field)


def display_raw_data(canonical_model):
    """Display raw canonical data"""
    
    st.markdown("### 📋 Canonical Data Model")
    
    years = canonical_model.get_available_years()
    
    # P&L data
    st.markdown("#### Income Statement (P&L)")
    pl_fields = ['revenue', 'gross_profit', 'ebit', 'net_profit', 'depreciation_amortization', 'interest_expense']
    pl_data = {}
    for field in pl_fields:
        pl_data[field.replace('_', ' ').title()] = [canonical_model.get_value(field, year) for year in years]
    
    if any(any(values) for values in pl_data.values()):
        df_pl = pd.DataFrame(pl_data, index=years)
        st.dataframe(df_pl.style.format("{:,.2f}", na_rep="-"), use_container_width=True)
    else:
        st.info("No P&L data available")
    
    # Balance Sheet data
    st.markdown("#### Balance Sheet")
    bs_fields = ['total_assets', 'current_assets', 'total_equity', 'total_liabilities', 'current_liabilities']
    bs_data = {}
    for field in bs_fields:
        bs_data[field.replace('_', ' ').title()] = [canonical_model.get_value(field, year) for year in years]
    
    if any(any(values) for values in bs_data.values()):
        df_bs = pd.DataFrame(bs_data, index=years)
        st.dataframe(df_bs.style.format("{:,.2f}", na_rep="-"), use_container_width=True)
    else:
        st.info("No Balance Sheet data available")


if __name__ == "__main__":
    main()
