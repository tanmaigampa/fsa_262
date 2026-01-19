"""
Financial Statement Analyzer
Automated analysis of financial statements with intelligent field mapping
Works with ANY company's financial statements
"""

__version__ = '0.1.0'

from .core import CanonicalFinancialData, StatementType
from .ingestion import ExcelReader, ExcelCleaner
from .mapping import FieldMatcher, FinancialDataMapper
from .analysis import RatioCalculator

__all__ = [
    'CanonicalFinancialData',
    'StatementType',
    'ExcelReader',
    'ExcelCleaner',
    'FieldMatcher',
    'FinancialDataMapper',
    'RatioCalculator',
]
