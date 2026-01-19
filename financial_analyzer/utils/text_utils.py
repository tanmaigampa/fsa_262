"""
Text utility functions for string manipulation
"""
import re
from typing import Optional


def normalize_text(text: str) -> str:
    """
    Normalize text: lowercase, trim, remove special chars
    
    Args:
        text: Input text
        
    Returns:
        Normalized text
    """
    if not text:
        return ""
    
    # Convert to string if not already
    text = str(text).strip().lower()
    
    # Remove special characters but keep spaces
    text = re.sub(r'[:\(\)\[\]\{\}\*#]', '', text)
    
    # Replace multiple spaces with single space
    text = ' '.join(text.split())
    
    return text


def extract_year_from_text(text: str) -> Optional[str]:
    """
    Extract 4-digit year from text
    
    Examples:
        'Mar-2025' -> '2025'
        'FY2024' -> '2024'
        '31-Mar-2023' -> '2023'
        
    Args:
        text: Input text containing year
        
    Returns:
        Year as string or None
    """
    if not text:
        return None
    
    # Look for 4-digit year pattern (19xx or 20xx)
    match = re.search(r'(19|20)\d{2}', str(text))
    
    if match:
        year = match.group()
        # Validate it's a reasonable year
        if 1990 <= int(year) <= 2030:
            return year
    
    return None


def extract_numeric_from_text(text: str) -> Optional[float]:
    """
    Extract numeric value from text
    
    Examples:
        '123.45 Cr' -> 123.45
        'INR 1,234.56' -> 1234.56
        '(123.45)' -> -123.45
        
    Args:
        text: Input text
        
    Returns:
        Numeric value or None
    """
    if not text:
        return None
    
    text = str(text).strip()
    
    # Handle bracketed negatives: (123.45) -> -123.45
    is_negative = False
    if text.startswith('(') and text.endswith(')'):
        text = text[1:-1]
        is_negative = True
    
    # Remove commas and currency symbols
    text = re.sub(r'[,₹$€£]', '', text)
    
    # Extract first number found
    match = re.search(r'-?\d+\.?\d*', text)
    
    if match:
        value = float(match.group())
        return -value if is_negative else value
    
    return None


def clean_field_name(field_name: str) -> str:
    """
    Clean field name for display
    
    Args:
        field_name: Raw field name
        
    Returns:
        Cleaned field name
    """
    if not field_name:
        return ""
    
    # Convert underscores to spaces
    cleaned = field_name.replace('_', ' ')
    
    # Title case
    cleaned = cleaned.title()
    
    return cleaned


def extract_currency_and_unit(text: str) -> tuple[str, str]:
    """
    Extract currency and unit from header text
    
    Examples:
        '[INR-Crores]' -> ('INR', 'Crores')
        '[USD-Millions]' -> ('USD', 'Millions')
        
    Args:
        text: Header text
        
    Returns:
        Tuple of (currency, unit)
    """
    # Default values
    currency = 'INR'
    unit = 'Crores'
    
    if not text:
        return currency, unit
    
    text = str(text).upper()
    
    # Extract currency
    if 'USD' in text:
        currency = 'USD'
    elif 'EUR' in text:
        currency = 'EUR'
    elif 'INR' in text:
        currency = 'INR'
    
    # Extract unit
    if 'CRORE' in text:
        unit = 'Crores'
    elif 'LAKH' in text:
        unit = 'Lakhs'
    elif 'MILLION' in text:
        unit = 'Millions'
    elif 'THOUSAND' in text:
        unit = 'Thousands'
    
    return currency, unit


def is_category_header(text: str) -> bool:
    """
    Check if text is a category header (not actual data)
    
    Category headers are lines like:
    - 'INCOME :'
    - 'EXPENDITURE :'
    - 'ASSETS'
    - 'LIABILITIES'
    
    Args:
        text: Field name text
        
    Returns:
        True if category header
    """
    if not text:
        return False
    
    text = str(text).strip().upper()
    
    # Common category headers
    category_keywords = [
        'INCOME', 'EXPENDITURE', 'ASSETS', 'LIABILITIES',
        'EQUITY AND LIABILITIES', 'NON-CURRENT ASSETS',
        'CURRENT ASSETS', 'OPERATING ACTIVITIES',
        'INVESTING ACTIVITIES', 'FINANCING ACTIVITIES',
        'PARTICULARS', 'DESCRIPTION', 'ITEM'
    ]
    
    # Check if text is exactly one of these headers
    for keyword in category_keywords:
        if text == keyword or text == keyword + ' :' or text == keyword + ':':
            return True
    
    # Also check if it ends with colon (common pattern)
    if text.endswith(':') and len(text) < 30:
        return True
    
    return False


def similarity_score(text1: str, text2: str) -> float:
    """
    Calculate simple similarity score between two texts (0-1)
    Uses character overlap for quick fuzzy matching
    
    Args:
        text1: First text
        text2: Second text
        
    Returns:
        Similarity score between 0 and 1
    """
    if not text1 or not text2:
        return 0.0
    
    text1 = normalize_text(text1)
    text2 = normalize_text(text2)
    
    if text1 == text2:
        return 1.0
    
    # Check if one contains the other
    if text1 in text2 or text2 in text1:
        shorter = min(len(text1), len(text2))
        longer = max(len(text1), len(text2))
        return shorter / longer
    
    # Count common words
    words1 = set(text1.split())
    words2 = set(text2.split())
    
    if not words1 or not words2:
        return 0.0
    
    common = words1 & words2
    total = words1 | words2
    
    return len(common) / len(total) if total else 0.0
