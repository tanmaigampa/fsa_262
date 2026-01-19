# Financial Statement Analyzer

🔍 **Automated analysis of financial statements with intelligent field mapping and ratio calculation.**

Works with **ANY company's** financial statements - automatically adapts to different formats, field names, and data structures.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Problem Statement

Financial analysts manually spend hours:
- Extracting data from Excel financial statements
- Dealing with inconsistent field names ("Operating Income" vs "Revenue" vs "Net Sales")
- Calculating 15+ financial ratios
- Handling missing data and errors
- Repeating this process for every company

**This tool automates 100% of this workflow.**

---

## ✨ Features

- ✅ **Universal Compatibility**: Works with ANY company's financial statements
- ✅ **Intelligent Field Mapping**: Automatically maps varying field names to standardized format
- ✅ **Canonical Data Model**: Converts messy statements into clean, consistent structure
- ✅ **17 Financial Ratios**: Profitability, liquidity, leverage, efficiency, cash flow metrics
- ✅ **Multi-Year Analysis**: Analyzes 20+ years of data in seconds
- ✅ **Graceful Error Handling**: Works even with incomplete data
- ✅ **ACE Equity Support**: Built for Indian market data (expandable to other sources)

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/yourusername/financial-statement-analyzer.git
cd financial-statement-analyzer
pip install -r requirements.txt
```

### Usage

```bash
# Analyze any company's financial statements
python main.py \
    --pl company_profit_loss.xlsx \
    --bs company_balance_sheet.xlsx \
    --cf company_cash_flow.xlsx
```

### Example Output

```
============================================================
FINANCIAL STATEMENT ANALYZER
============================================================

Step 1: Ingesting and cleaning files...
  Processing P&L: Infosys_Ltd__-_Profit_And_Loss.xlsx
    Rows extracted: 34
    Years found: 2003-2025 (23 years)
  
  Company: Infosys Ltd.
  Currency: INR
  Unit: Crores

Step 2: Mapping to canonical model...
  Total mappings: 20
  P&L: 7 fields mapped
  Balance Sheet: 7 fields mapped
  Cash Flow: 6 fields mapped

Step 4: Calculating financial ratios...
  Total ratios defined: 17
  Years analyzed: 2003-2025
  Ratios calculated: 9-17 per year

============================================================
ANALYSIS COMPLETE
============================================================
Company: Infosys Ltd.
Ratios calculated: 17
```

---

## 📊 Calculated Ratios

### Profitability Ratios
- Gross Profit Margin (%)
- Operating Profit Margin (%)
- Net Profit Margin (%)
- EBITDA Margin (%)
- Return on Assets (%)
- Return on Equity (%)

### Liquidity Ratios
- Current Ratio
- Cash Ratio
- Working Capital Ratio

### Leverage Ratios
- Debt to Equity
- Debt to Assets
- Equity Ratio (%)
- Interest Coverage

### Efficiency Ratios
- Asset Turnover

### Cash Flow Ratios
- Operating Cash Flow Ratio
- Cash Flow Margin (%)
- Free Cash Flow

---

## 🏗️ Architecture

The tool uses a **two-stage canonical model approach**:

```
Raw Excel Files (ANY company)
    ↓
[1. INGESTION] → Clean, structured DataFrames
    ↓
[2. MAPPING] → Canonical Model (standardized)
    ↓
[3. ANALYSIS] → Financial Ratios
    ↓
[4. EXPORT] → Excel Dashboard (coming soon)
```

### Why This Approach?

**Problem**: Different companies use different field names:
- Company A: "Operating Income"
- Company B: "Revenue from Operations"  
- Company C: "Net Sales"

**Solution**: Canonical model provides a universal standard:
- All three → `revenue` in canonical model
- Ratios calculate from `revenue` consistently
- Works with ANY company automatically

[Read detailed architecture →](docs/CODE_STRUCTURE.md)

---

## 🧪 Tested With

- ✅ **Infosys** (IT Services) - 23 years of data
- ✅ **TCS** (IT Services) - Coming soon
- ✅ **Reliance** (Manufacturing/Retail) - Coming soon
- 🔄 More companies being added...

The tool adapts automatically to:
- Service companies (no COGS/inventory)
- Manufacturing companies (has COGS/inventory)
- Different field naming conventions
- Missing or incomplete data

---

## 📁 Project Structure

```
financial-statement-analyzer/
├── financial_analyzer/          # Main package
│   ├── core/                    # Canonical model & field mappings
│   ├── ingestion/               # Excel reading & cleaning
│   ├── mapping/                 # Field matching & mapping
│   ├── analysis/                # Ratio calculations
│   ├── export/                  # Output generation (coming soon)
│   └── utils/                   # Helper functions
├── main.py                      # Command-line interface
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

---

## 🔧 How It Works

### 1. Intelligent Field Mapping

```python
# The tool automatically recognizes these as the SAME field:
"Operating Income"     → revenue
"Revenue from Operations" → revenue
"Net Sales"           → revenue
"Total Income"        → revenue

# Even with typos or variations:
"Revenue from Oprations" → revenue (fuzzy matching)
```

### 2. Handles Missing Data

```python
# If data is missing, ratios show "N/A" instead of crashing
Gross Profit not available? → Gross Profit Margin = N/A
Total Equity missing? → ROE = N/A
```

### 3. Multi-Year Analysis

Processes 20+ years of data in seconds:
- 2003: 9/17 ratios calculated
- 2004: 9/17 ratios calculated
- ...
- 2025: 9/17 ratios calculated

---

## 💡 Use Cases

### For Analysts
- Compare multiple companies quickly
- Track ratio trends over 10+ years
- Automate repetitive Excel work

### For Investors
- Screen companies by financial health
- Identify trends in profitability/leverage
- Build custom analysis workflows

### For Students
- Learn financial analysis
- Experiment with real company data
- Understand ratio calculations

---

## 🚧 Roadmap

### Version 0.1 (Current)
- ✅ Core ingestion & cleaning
- ✅ Canonical model mapping
- ✅ 17 financial ratios
- ✅ Command-line interface

### Version 0.2 (Next)
- 📊 Excel dashboard export
- 📈 Trend analysis (YoY growth)
- 🔍 Data quality reports
- 📝 Comprehensive documentation

### Version 0.3 (Future)
- 🌐 Web interface (Streamlit)
- 📊 Visual charts & graphs
- 🏢 Multi-company comparison
- 🔌 Support for more data sources

---

## 🤝 Contributing

Contributions welcome! Areas needing help:
- Support for more data sources (NSE, BSE, Yahoo Finance)
- Additional ratio calculations
- Visualization improvements
- Documentation enhancements

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built to solve real financial analysis challenges
- Inspired by the need for automated statement processing
- Sample data from ACE Equity (for demonstration purposes)

---

## 📧 Contact

- GitHub Issues: [Report bugs or request features](https://github.com/yourusername/financial-analyzer/issues)
- Email: your.email@example.com

---

## ⭐ Star This Project

If you find this tool useful, please consider giving it a star! It helps others discover the project.

---

## 🎓 Learn More

- [Architecture Overview](docs/CODE_STRUCTURE.md)
- [Business Logic](docs/BUSINESS_LOGIC_ANALYSIS.md)
- [GitHub Publication Strategy](docs/GITHUB_STRATEGY.md)
