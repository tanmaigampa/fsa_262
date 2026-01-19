"""Utility functions for financial analysis"""

from .numeric_utils import (
    safe_divide,
    safe_percentage,
    round_safe,
    is_positive,
    is_negative,
    format_currency,
    format_percentage,
    format_ratio
)

from .text_utils import (
    normalize_text,
    extract_year_from_text,
    extract_numeric_from_text,
    clean_field_name,
    extract_currency_and_unit,
    is_category_header,
    similarity_score
)

__all__ = [
    'safe_divide',
    'safe_percentage',
    'round_safe',
    'is_positive',
    'is_negative',
    'format_currency',
    'format_percentage',
    'format_ratio',
    'normalize_text',
    'extract_year_from_text',
    'extract_numeric_from_text',
    'clean_field_name',
    'extract_currency_and_unit',
    'is_category_header',
    'similarity_score'
]
