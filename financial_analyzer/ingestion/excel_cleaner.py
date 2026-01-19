"""
Excel data cleaner
Cleans and structures raw Excel data into usable format
"""

import pandas as pd
import numpy as np
from typing import List, Tuple, Optional
import re

from ..utils import (
    extract_year_from_text,
    extract_numeric_from_text,
    is_category_header,
    normalize_text
)


class ExcelCleaner:
    """
    Cleans raw Excel DataFrames into structured format
    Handles data from ANY company's financial statements
    """
    
    def __init__(self, raw_df: pd.DataFrame, metadata: dict):
        """
        Initialize cleaner
        
        Args:
            raw_df: Raw DataFrame from Excel
            metadata: Metadata dict with company info
        """
        self.raw_df = raw_df
        self.metadata = metadata
        self.cleaned_df: Optional[pd.DataFrame] = None
        self.years: List[str] = []
        self.header_row_idx: int = 0
        
    def find_header_row(self) -> int:
        """
        Find the row containing year headers
        
        Returns:
            Row index of header
        """
        # Look in first 15 rows for year patterns
        for idx in range(min(15, len(self.raw_df))):
            row = self.raw_df.iloc[idx]
            
            # Count how many year-like values in this row
            year_count = 0
            for val in row:
                if pd.notna(val):
                    year = extract_year_from_text(str(val))
                    if year:
                        year_count += 1
            
            # If we found 2+ years, this is likely the header row
            if year_count >= 2:
                self.header_row_idx = idx
                return idx
        
        # Default to row 0 if not found
        return 0
    
    def extract_years(self) -> List[str]:
        """
        Extract fiscal years from the header row
        
        Returns:
            List of year strings (e.g., ['2023', '2024', '2025'])
        """
        header_row = self.raw_df.iloc[self.header_row_idx]
        years = []
        
        for val in header_row:
            if pd.notna(val):
                year = extract_year_from_text(str(val))
                if year and year not in years:
                    years.append(year)
        
        self.years = years
        return years
    
    def clean_numeric_value(self, value) -> Optional[float]:
        """
        Clean and convert numeric value
        
        Args:
            value: Raw value from Excel
            
        Returns:
            Float value or None
        """
        if pd.isna(value):
            return None
        
        # Already a number
        if isinstance(value, (int, float)):
            return float(value) if not np.isnan(value) else None
        
        # String number
        if isinstance(value, str):
            # Try to extract numeric value
            numeric = extract_numeric_from_text(value)
            return numeric
        
        return None
    
    def remove_empty_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove rows where all year values are empty
        
        Args:
            df: DataFrame to clean
            
        Returns:
            Cleaned DataFrame
        """
        if df.empty:
            return df
        
        # Get year columns (all except 'Particulars')
        year_cols = [col for col in df.columns if col != 'Particulars']
        
        if not year_cols:
            return df
        
        # Keep rows where at least one year has data
        df = df.dropna(subset=year_cols, how='all')
        
        return df
    
    def remove_category_headers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove category header rows
        
        Args:
            df: DataFrame to clean
            
        Returns:
            Cleaned DataFrame
        """
        if df.empty:
            return df
        
        # Filter out category headers
        mask = df['Particulars'].apply(lambda x: not is_category_header(str(x)) if pd.notna(x) else False)
        
        return df[mask]
    
    def clean(self) -> pd.DataFrame:
        """
        Main cleaning method - creates structured DataFrame
        
        Returns:
            Cleaned DataFrame with structure:
            | Particulars | 2023 | 2024 | 2025 |
        """
        # Find header row and extract years
        self.find_header_row()
        self.extract_years()
        
        if not self.years:
            raise ValueError("No years found in the file. Cannot process.")
        
        # Build mapping of year to column index
        year_to_col = {}
        header_row = self.raw_df.iloc[self.header_row_idx]
        
        for col_idx, val in enumerate(header_row):
            if pd.notna(val):
                year = extract_year_from_text(str(val))
                if year:
                    year_to_col[year] = col_idx
        
        # Extract data rows (start after header)
        data_start_idx = self.header_row_idx + 1
        
        cleaned_rows = []
        
        for idx in range(data_start_idx, len(self.raw_df)):
            row = self.raw_df.iloc[idx]
            
            # Get field name from first non-empty cell
            field_name = None
            for val in row:
                if pd.notna(val) and str(val).strip():
                    field_name = str(val).strip()
                    break
            
            if not field_name:
                continue
            
            # Skip if category header
            if is_category_header(field_name):
                continue
            
            # Build row data
            row_data = {'Particulars': field_name}
            
            # Extract values for each year
            for year in self.years:
                if year in year_to_col:
                    col_idx = year_to_col[year]
                    if col_idx < len(row):
                        raw_value = row.iloc[col_idx]
                        cleaned_value = self.clean_numeric_value(raw_value)
                        row_data[year] = cleaned_value
                    else:
                        row_data[year] = None
                else:
                    row_data[year] = None
            
            cleaned_rows.append(row_data)
        
        # Create DataFrame
        columns = ['Particulars'] + sorted(self.years)
        df = pd.DataFrame(cleaned_rows, columns=columns)
        
        # Remove empty rows
        df = self.remove_empty_rows(df)
        
        # Remove duplicate field names (keep first occurrence)
        df = df.drop_duplicates(subset=['Particulars'], keep='first')
        
        # Reset index
        df = df.reset_index(drop=True)
        
        self.cleaned_df = df
        return df
    
    def get_cleaned_dataframe(self) -> pd.DataFrame:
        """
        Get cleaned DataFrame (run clean() if not already done)
        
        Returns:
            Cleaned DataFrame
        """
        if self.cleaned_df is None:
            self.clean()
        
        return self.cleaned_df
    
    def get_years(self) -> List[str]:
        """
        Get extracted years
        
        Returns:
            List of year strings
        """
        if not self.years:
            self.find_header_row()
            self.extract_years()
        
        return sorted(self.years)
