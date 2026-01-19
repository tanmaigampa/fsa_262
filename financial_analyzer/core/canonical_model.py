"""
Canonical Financial Model
Defines the standardized internal structure for financial data.
Works with ANY company's financial statements.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, List
from enum import Enum


class StatementType(Enum):
    """Types of financial statements"""
    PROFIT_LOSS = "P&L"
    BALANCE_SHEET = "Balance Sheet"
    CASH_FLOW = "Cash Flow"


@dataclass
class CanonicalFinancialData:
    """
    Standardized financial data structure.
    All amounts in the reporting currency (typically in millions/thousands as per source).
    Years are stored as strings (e.g., "2023", "2024").
    """
    
    # Metadata
    company_name: str = ""
    currency: str = "INR"
    unit: str = "millions"  # millions, thousands, etc.
    fiscal_years: List[str] = field(default_factory=list)
    
    # Income Statement (P&L) - key items by year
    revenue: Dict[str, Optional[float]] = field(default_factory=dict)
    cost_of_goods_sold: Dict[str, Optional[float]] = field(default_factory=dict)
    gross_profit: Dict[str, Optional[float]] = field(default_factory=dict)
    operating_expenses: Dict[str, Optional[float]] = field(default_factory=dict)
    ebitda: Dict[str, Optional[float]] = field(default_factory=dict)
    depreciation_amortization: Dict[str, Optional[float]] = field(default_factory=dict)
    ebit: Dict[str, Optional[float]] = field(default_factory=dict)
    interest_expense: Dict[str, Optional[float]] = field(default_factory=dict)
    profit_before_tax: Dict[str, Optional[float]] = field(default_factory=dict)
    tax_expense: Dict[str, Optional[float]] = field(default_factory=dict)
    net_profit: Dict[str, Optional[float]] = field(default_factory=dict)
    
    # Balance Sheet - key items by year
    current_assets: Dict[str, Optional[float]] = field(default_factory=dict)
    non_current_assets: Dict[str, Optional[float]] = field(default_factory=dict)
    total_assets: Dict[str, Optional[float]] = field(default_factory=dict)
    
    current_liabilities: Dict[str, Optional[float]] = field(default_factory=dict)
    non_current_liabilities: Dict[str, Optional[float]] = field(default_factory=dict)
    total_liabilities: Dict[str, Optional[float]] = field(default_factory=dict)
    
    share_capital: Dict[str, Optional[float]] = field(default_factory=dict)
    reserves_surplus: Dict[str, Optional[float]] = field(default_factory=dict)
    total_equity: Dict[str, Optional[float]] = field(default_factory=dict)
    
    # Debt items
    short_term_debt: Dict[str, Optional[float]] = field(default_factory=dict)
    long_term_debt: Dict[str, Optional[float]] = field(default_factory=dict)
    total_debt: Dict[str, Optional[float]] = field(default_factory=dict)
    
    # Cash Flow - key items by year
    operating_cash_flow: Dict[str, Optional[float]] = field(default_factory=dict)
    investing_cash_flow: Dict[str, Optional[float]] = field(default_factory=dict)
    financing_cash_flow: Dict[str, Optional[float]] = field(default_factory=dict)
    net_cash_flow: Dict[str, Optional[float]] = field(default_factory=dict)
    cash_beginning: Dict[str, Optional[float]] = field(default_factory=dict)
    cash_ending: Dict[str, Optional[float]] = field(default_factory=dict)
    
    # Additional useful metrics
    capex: Dict[str, Optional[float]] = field(default_factory=dict)
    working_capital: Dict[str, Optional[float]] = field(default_factory=dict)
    
    def get_value(self, field_name: str, year: str) -> Optional[float]:
        """Get value for a specific field and year"""
        field_dict = getattr(self, field_name, {})
        return field_dict.get(year)
    
    def set_value(self, field_name: str, year: str, value: Optional[float]):
        """Set value for a specific field and year"""
        field_dict = getattr(self, field_name, {})
        field_dict[year] = value
        
    def get_available_years(self) -> List[str]:
        """Get list of years with data"""
        return sorted(self.fiscal_years)
    
    def validate(self) -> Dict[str, List[str]]:
        """
        Validate the canonical model and return warnings about missing data
        Returns dict of statement_type -> list of missing fields
        """
        warnings = {
            "P&L": [],
            "Balance Sheet": [],
            "Cash Flow": []
        }
        
        years = self.get_available_years()
        if not years:
            return {"General": ["No fiscal years found"]}
        
        # Check P&L critical fields
        pl_fields = ['revenue', 'net_profit']
        for field in pl_fields:
            if not any(self.get_value(field, year) is not None for year in years):
                warnings["P&L"].append(f"Missing {field}")
        
        # Check Balance Sheet critical fields
        bs_fields = ['total_assets', 'total_equity']
        for field in bs_fields:
            if not any(self.get_value(field, year) is not None for year in years):
                warnings["Balance Sheet"].append(f"Missing {field}")
        
        # Check Cash Flow critical fields
        cf_fields = ['operating_cash_flow']
        for field in cf_fields:
            if not any(self.get_value(field, year) is not None for year in years):
                warnings["Cash Flow"].append(f"Missing {field}")
        
        # Remove empty warnings
        warnings = {k: v for k, v in warnings.items() if v}
        
        return warnings


# Field name mappings - maps common variations to canonical field names
FIELD_MAPPINGS = {
    # Revenue variations
    'revenue': [
        'revenue', 'total revenue', 'net revenue', 'sales', 'net sales', 
        'total sales', 'income from operations', 'operating income', 
        'turnover', 'net turnover', 'revenue from operations', 'gross sales'
    ],
    
    # Cost variations
    'cost_of_goods_sold': [
        'cost of goods sold', 'cogs', 'cost of sales', 'cost of revenue',
        'direct costs', 'cost of materials', 'raw material consumed', 'raw materials consumed'
    ],
    
    # Profit variations
    'gross_profit': [
        'gross profit', 'gross margin', 'gross income'
    ],
    
    'ebitda': [
        'ebitda', 'operating profit before depreciation', 'pbdt',
        'profit before depreciation and tax', 'profit before depreciation & tax'
    ],
    
    'ebit': [
        'ebit', 'operating profit', 'operating income', 'profit from operations',
        'earnings before interest and tax', 'operating profit (excl oi)',
        'operating profit excl oi'
    ],
    
    'net_profit': [
        'net profit', 'net income', 'profit after tax', 'pat', 'net earnings',
        'profit for the year', 'profit attributable to shareholders',
        'net profit after tax', 'total comprehensive income'
    ],
    
    'profit_before_tax': [
        'profit before tax', 'pbt', 'earnings before tax', 'income before tax',
        'profit before income tax'
    ],
    
    # Assets
    'total_assets': [
        'total assets', 'assets', 'total asset'
    ],
    
    'current_assets': [
        'current assets', 'total current assets'
    ],
    
    'non_current_assets': [
        'non-current assets', 'non current assets', 'fixed assets', 
        'total non-current assets', 'total non current assets'
    ],
    
    # Liabilities
    'total_liabilities': [
        'total liabilities', 'liabilities', 'total liability'
    ],
    
    'current_liabilities': [
        'current liabilities', 'total current liabilities'
    ],
    
    'non_current_liabilities': [
        'non-current liabilities', 'non current liabilities',
        'total non-current liabilities', 'total non current liabilities',
        'long term liabilities', 'long-term liabilities'
    ],
    
    # Equity
    'total_equity': [
        "shareholders' equity", 'shareholders equity', 'total equity',
        'equity', 'net worth', "stockholders' equity", 
        'equity attributable to shareholders', 'shareholders funds',
        'total shareholders funds', "shareholder's funds", 'shareholders funds'
    ],
    
    'share_capital': [
        'share capital', 'equity share capital', 'common stock',
        'paid up capital', 'capital stock'
    ],
    
    'reserves_surplus': [
        'reserves and surplus', 'reserves & surplus', 'retained earnings',
        'accumulated surplus', 'other reserves'
    ],
    
    # Debt
    'total_debt': [
        'total debt', 'total borrowings', 'borrowings', 'debt'
    ],
    
    'short_term_debt': [
        'short-term debt', 'short term debt', 'current borrowings',
        'short-term borrowings', 'current debt', 'short term borrowings'
    ],
    
    'long_term_debt': [
        'long-term debt', 'long term debt', 'non-current borrowings',
        'long-term borrowings', 'non current borrowings', 'secured loans',
        'unsecured loans'
    ],
    
    # Cash Flow
    'operating_cash_flow': [
        'cash flow from operating activities', 'operating cash flow',
        'net cash from operating activities', 'cash from operations',
        'operating activities'
    ],
    
    'investing_cash_flow': [
        'cash flow from investing activities', 'investing cash flow',
        'net cash from investing activities', 'cash from investing',
        'investing activities'
    ],
    
    'financing_cash_flow': [
        'cash flow from financing activities', 'financing cash flow',
        'net cash from financing activities', 'cash from financing',
        'financing activities'
    ],
    
    'cash_ending': [
        'cash and cash equivalents', 'cash at end', 'closing cash',
        'cash and bank balances', 'cash balance', 'cash and bank', 'cash & bank'
    ],
    
    # Other
    'depreciation_amortization': [
        'depreciation and amortization', 'depreciation & amortization',
        'depreciation', 'amortization'
    ],
    
    'interest_expense': [
        'interest expense', 'finance costs', 'interest cost',
        'financial expenses', 'borrowing costs'
    ],
    
    'tax_expense': [
        'tax expense', 'income tax', 'provision for tax',
        'current tax', 'tax provision'
    ],
    
    'capex': [
        'capital expenditure', 'capex', 'purchase of fixed assets',
        'additions to fixed assets', 'capital expenditures'
    ]
}


def normalize_field_name(field_name: str) -> str:
    """
    Normalize a field name by removing special characters and converting to lowercase
    """
    if not field_name:
        return ""
    
    # Convert to lowercase and strip
    normalized = str(field_name).lower().strip()
    
    # Remove common special characters
    for char in [':', '(', ')', '[', ']', '{', '}', '*', '#']:
        normalized = normalized.replace(char, '')
    
    # Replace multiple spaces with single space
    normalized = ' '.join(normalized.split())
    
    return normalized


def map_to_canonical_field(field_name: str) -> Optional[str]:
    """
    Map a field name from source data to canonical field name
    Returns None if no mapping found
    """
    normalized = normalize_field_name(field_name)
    
    for canonical_field, variations in FIELD_MAPPINGS.items():
        if normalized in [normalize_field_name(v) for v in variations]:
            return canonical_field
    
    return None
