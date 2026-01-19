"""
Excel file reader for financial statements
Handles reading and initial identification of statement types
"""

import pandas as pd
from typing import Optional, Dict
from pathlib import Path

from ..core import StatementType
from ..utils import extract_currency_and_unit


class ExcelReader:
    """
    Reads Excel financial statement files and extracts basic metadata
    Works with files from ANY company
    """
    
    def __init__(self, file_path: str):
        """
        Initialize reader
        
        Args:
            file_path: Path to Excel file
        """
        self.file_path = Path(file_path)
        self.raw_df: Optional[pd.DataFrame] = None
        self.metadata: Dict = {}
        
    def read(self) -> pd.DataFrame:
        """
        Read Excel file
        
        Returns:
            Raw DataFrame
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file cannot be read
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        try:
            # Read first sheet with openpyxl engine
            self.raw_df = pd.read_excel(
                self.file_path, 
                sheet_name=0,
                engine='openpyxl',
                header=None  # Don't assume header row
            )
            
            return self.raw_df
            
        except Exception as e:
            raise ValueError(f"Error reading Excel file {self.file_path}: {e}")
    
    def identify_statement_type(self) -> StatementType:
        """
        Identify the type of financial statement based on filename and content
        
        Returns:
            Statement type
        """
        if self.raw_df is None:
            self.read()
        
        # Check filename first
        filename_lower = self.file_path.name.lower()
        
        if any(keyword in filename_lower for keyword in ['p&l', 'profit', 'loss', 'income', 'p_and_l', 'pl']):
            return StatementType.PROFIT_LOSS
        
        if any(keyword in filename_lower for keyword in ['balance', 'b/s', 'bs', 'b_s']):
            return StatementType.BALANCE_SHEET
        
        if any(keyword in filename_lower for keyword in ['cash', 'flow', 'cf', 'c_f', 'cashflow']):
            return StatementType.CASH_FLOW
        
        # Check content - look in first few rows for keywords
        content_str = ' '.join(
            self.raw_df.astype(str).values.flatten()[:50]
        ).lower()
        
        # P&L indicators
        pl_keywords = ['revenue', 'net profit', 'ebitda', 'operating income', 'expenditure']
        if sum(1 for kw in pl_keywords if kw in content_str) >= 2:
            return StatementType.PROFIT_LOSS
        
        # Balance Sheet indicators
        bs_keywords = ['total assets', 'equity', 'liabilities', 'shareholders']
        if sum(1 for kw in bs_keywords if kw in content_str) >= 2:
            return StatementType.BALANCE_SHEET
        
        # Cash Flow indicators
        cf_keywords = ['operating activities', 'investing activities', 'financing activities']
        if sum(1 for kw in cf_keywords if kw in content_str) >= 2:
            return StatementType.CASH_FLOW
        
        # Default: try to infer from structure
        # P&L usually has "profit" related items
        if 'profit' in content_str and 'tax' in content_str:
            return StatementType.PROFIT_LOSS
        
        # Fallback: Return based on filename keywords if possible
        raise ValueError(
            f"Could not determine statement type for {self.file_path.name}. "
            f"Please ensure filename contains 'pl', 'bs', or 'cf' keywords."
        )
    
    def extract_metadata(self) -> Dict:
        """
        Extract metadata from the Excel file
        - Company name
        - Currency
        - Unit
        
        Returns:
            Dictionary with metadata
        """
        if self.raw_df is None:
            self.read()
        
        metadata = {
            'company_name': 'Unknown Company',
            'currency': 'INR',
            'unit': 'Crores',
            'file_name': self.file_path.name
        }
        
        # Company name is usually in first row, first column
        if not self.raw_df.empty:
            first_cell = self.raw_df.iloc[0, 0]
            if pd.notna(first_cell):
                first_cell_str = str(first_cell)
                
                # Extract company name (before first '-' or ' - ')
                if ' - ' in first_cell_str:
                    company_name = first_cell_str.split(' - ')[0].strip()
                    metadata['company_name'] = company_name
                elif '-' in first_cell_str and len(first_cell_str) < 100:
                    company_name = first_cell_str.split('-')[0].strip()
                    metadata['company_name'] = company_name
                else:
                    # Just use the whole text if it's reasonable length
                    if 5 < len(first_cell_str) < 100:
                        metadata['company_name'] = first_cell_str.strip()
                
                # Extract currency and unit from first row
                currency, unit = extract_currency_and_unit(first_cell_str)
                metadata['currency'] = currency
                metadata['unit'] = unit
        
        self.metadata = metadata
        return metadata
    
    def get_raw_dataframe(self) -> pd.DataFrame:
        """
        Get the raw DataFrame
        
        Returns:
            Raw DataFrame
        """
        if self.raw_df is None:
            self.read()
        
        return self.raw_df
