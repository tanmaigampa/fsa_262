"""
Financial Ratio Calculator
Calculates financial ratios and metrics from canonical model
Works with ANY company's data
"""

from typing import Dict, Optional
from ..core import CanonicalFinancialData
from ..utils import safe_divide, safe_percentage


class RatioCalculator:
    """
    Calculates financial ratios from canonical financial data
    All ratios work universally regardless of company or industry
    """
    
    def __init__(self, canonical_model: CanonicalFinancialData):
        """
        Initialize calculator
        
        Args:
            canonical_model: Populated canonical financial data
        """
        self.model = canonical_model
        self.ratios: Dict[str, Dict[str, Optional[float]]] = {}
    
    # ===================
    # PROFITABILITY RATIOS
    # ===================
    
    def gross_profit_margin(self, year: str) -> Optional[float]:
        """Gross Profit Margin (%) = (Gross Profit / Revenue) × 100"""
        gross_profit = self.model.get_value('gross_profit', year)
        revenue = self.model.get_value('revenue', year)
        return safe_percentage(gross_profit, revenue)
    
    def operating_profit_margin(self, year: str) -> Optional[float]:
        """Operating Profit Margin (%) = (EBIT / Revenue) × 100"""
        ebit = self.model.get_value('ebit', year)
        revenue = self.model.get_value('revenue', year)
        return safe_percentage(ebit, revenue)
    
    def net_profit_margin(self, year: str) -> Optional[float]:
        """Net Profit Margin (%) = (Net Profit / Revenue) × 100"""
        net_profit = self.model.get_value('net_profit', year)
        revenue = self.model.get_value('revenue', year)
        return safe_percentage(net_profit, revenue)
    
    def return_on_assets(self, year: str) -> Optional[float]:
        """Return on Assets (%) = (Net Profit / Total Assets) × 100"""
        net_profit = self.model.get_value('net_profit', year)
        total_assets = self.model.get_value('total_assets', year)
        return safe_percentage(net_profit, total_assets)
    
    def return_on_equity(self, year: str) -> Optional[float]:
        """Return on Equity (%) = (Net Profit / Total Equity) × 100"""
        net_profit = self.model.get_value('net_profit', year)
        total_equity = self.model.get_value('total_equity', year)
        return safe_percentage(net_profit, total_equity)
    
    def ebitda_margin(self, year: str) -> Optional[float]:
        """EBITDA Margin (%) = (EBITDA / Revenue) × 100"""
        ebitda = self.model.get_value('ebitda', year)
        revenue = self.model.get_value('revenue', year)
        return safe_percentage(ebitda, revenue)
    
    # ===================
    # LIQUIDITY RATIOS
    # ===================
    
    def current_ratio(self, year: str) -> Optional[float]:
        """Current Ratio = Current Assets / Current Liabilities"""
        current_assets = self.model.get_value('current_assets', year)
        current_liabilities = self.model.get_value('current_liabilities', year)
        return safe_divide(current_assets, current_liabilities)
    
    def cash_ratio(self, year: str) -> Optional[float]:
        """Cash Ratio = Cash / Current Liabilities"""
        cash = self.model.get_value('cash_ending', year)
        current_liabilities = self.model.get_value('current_liabilities', year)
        return safe_divide(cash, current_liabilities)
    
    def working_capital_ratio(self, year: str) -> Optional[float]:
        """Working Capital Ratio = Working Capital / Total Assets"""
        working_capital = self.model.get_value('working_capital', year)
        total_assets = self.model.get_value('total_assets', year)
        return safe_divide(working_capital, total_assets)
    
    # ===================
    # LEVERAGE RATIOS
    # ===================
    
    def debt_to_equity(self, year: str) -> Optional[float]:
        """Debt to Equity = Total Debt / Total Equity"""
        total_debt = self.model.get_value('total_debt', year)
        total_equity = self.model.get_value('total_equity', year)
        return safe_divide(total_debt, total_equity)
    
    def debt_to_assets(self, year: str) -> Optional[float]:
        """Debt to Assets = Total Debt / Total Assets"""
        total_debt = self.model.get_value('total_debt', year)
        total_assets = self.model.get_value('total_assets', year)
        return safe_divide(total_debt, total_assets)
    
    def equity_ratio(self, year: str) -> Optional[float]:
        """Equity Ratio (%) = (Total Equity / Total Assets) × 100"""
        total_equity = self.model.get_value('total_equity', year)
        total_assets = self.model.get_value('total_assets', year)
        return safe_percentage(total_equity, total_assets)
    
    def interest_coverage(self, year: str) -> Optional[float]:
        """Interest Coverage = EBIT / Interest Expense"""
        ebit = self.model.get_value('ebit', year)
        interest = self.model.get_value('interest_expense', year)
        return safe_divide(ebit, interest)
    
    # ===================
    # EFFICIENCY RATIOS
    # ===================
    
    def asset_turnover(self, year: str) -> Optional[float]:
        """Asset Turnover = Revenue / Total Assets"""
        revenue = self.model.get_value('revenue', year)
        total_assets = self.model.get_value('total_assets', year)
        return safe_divide(revenue, total_assets)
    
    def revenue_per_employee(self, year: str) -> Optional[float]:
        """Revenue per Employee = Revenue / Employee Count"""
        revenue = self.model.get_value('revenue', year)
        employees = self.model.get_value('employee_count', year)
        return safe_divide(revenue, employees)
    
    # ===================
    # CASH FLOW RATIOS
    # ===================
    
    def operating_cash_flow_ratio(self, year: str) -> Optional[float]:
        """Operating Cash Flow Ratio = Operating CF / Current Liabilities"""
        ocf = self.model.get_value('operating_cash_flow', year)
        current_liabilities = self.model.get_value('current_liabilities', year)
        return safe_divide(ocf, current_liabilities)
    
    def free_cash_flow(self, year: str) -> Optional[float]:
        """Free Cash Flow = Operating Cash Flow - CapEx"""
        ocf = self.model.get_value('operating_cash_flow', year)
        capex = self.model.get_value('capex', year)
        
        if ocf is None:
            return None
        
        if capex is None:
            return ocf
        
        return ocf - capex
    
    def cash_flow_margin(self, year: str) -> Optional[float]:
        """Cash Flow Margin (%) = (Operating CF / Revenue) × 100"""
        ocf = self.model.get_value('operating_cash_flow', year)
        revenue = self.model.get_value('revenue', year)
        return safe_percentage(ocf, revenue)
    
    # ===================
    # COMPREHENSIVE CALCULATION
    # ===================
    
    def calculate_all_ratios(self) -> Dict[str, Dict[str, Optional[float]]]:
        """
        Calculate all available ratios for all years
        
        Returns:
            Dict of {ratio_name: {year: value}}
        """
        years = self.model.get_available_years()
        
        # Define all ratio functions
        ratio_functions = {
            # Profitability
            'Gross Profit Margin (%)': self.gross_profit_margin,
            'Operating Profit Margin (%)': self.operating_profit_margin,
            'Net Profit Margin (%)': self.net_profit_margin,
            'EBITDA Margin (%)': self.ebitda_margin,
            'Return on Assets (%)': self.return_on_assets,
            'Return on Equity (%)': self.return_on_equity,
            
            # Liquidity
            'Current Ratio': self.current_ratio,
            'Cash Ratio': self.cash_ratio,
            'Working Capital Ratio': self.working_capital_ratio,
            
            # Leverage
            'Debt to Equity': self.debt_to_equity,
            'Debt to Assets': self.debt_to_assets,
            'Equity Ratio (%)': self.equity_ratio,
            'Interest Coverage': self.interest_coverage,
            
            # Efficiency
            'Asset Turnover': self.asset_turnover,
            
            # Cash Flow
            'Operating CF Ratio': self.operating_cash_flow_ratio,
            'Cash Flow Margin (%)': self.cash_flow_margin,
        }
        
        results = {}
        
        # Calculate each ratio for each year
        for ratio_name, ratio_func in ratio_functions.items():
            results[ratio_name] = {}
            for year in years:
                try:
                    results[ratio_name][year] = ratio_func(year)
                except Exception:
                    results[ratio_name][year] = None
        
        # Add Free Cash Flow as absolute value
        results['Free Cash Flow'] = {}
        for year in years:
            try:
                results['Free Cash Flow'][year] = self.free_cash_flow(year)
            except Exception:
                results['Free Cash Flow'][year] = None
        
        self.ratios = results
        return results
    
    def get_ratio_summary(self) -> Dict:
        """
        Get summary of calculated ratios
        
        Returns:
            Summary dictionary
        """
        if not self.ratios:
            self.calculate_all_ratios()
        
        total_ratios = len(self.ratios)
        years = self.model.get_available_years()
        
        # Count how many ratios were successfully calculated per year
        calculated_counts = {}
        for year in years:
            count = sum(
                1 for ratio_dict in self.ratios.values()
                if ratio_dict.get(year) is not None
            )
            calculated_counts[year] = count
        
        return {
            'total_ratios': total_ratios,
            'years': years,
            'calculated_per_year': calculated_counts,
            'company': self.model.company_name
        }
