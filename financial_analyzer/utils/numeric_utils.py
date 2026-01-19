"""
Numeric utility functions for safe mathematical operations
"""
from typing import Optional


def safe_divide(numerator: Optional[float], 
                denominator: Optional[float], 
                default: Optional[float] = None) -> Optional[float]:
    """
    Safely divide two numbers, handling None and zero division
    
    Args:
        numerator: The numerator value
        denominator: The denominator value
        default: Value to return if division not possible
        
    Returns:
        Result of division or default value
    """
    if numerator is None or denominator is None:
        return default
    
    if denominator == 0:
        return default
    
    return numerator / denominator


def safe_percentage(part: Optional[float], 
                    whole: Optional[float],
                    default: Optional[float] = None) -> Optional[float]:
    """
    Calculate percentage safely: (part / whole) * 100
    
    Args:
        part: The part value
        whole: The whole value
        default: Value to return if calculation not possible
        
    Returns:
        Percentage value or default
    """
    result = safe_divide(part, whole, default)
    return result * 100 if result is not None else default


def round_safe(value: Optional[float], decimals: int = 2) -> Optional[float]:
    """
    Round a number safely, handling None
    
    Args:
        value: Value to round
        decimals: Number of decimal places
        
    Returns:
        Rounded value or None
    """
    if value is None:
        return None
    
    return round(value, decimals)


def is_positive(value: Optional[float]) -> bool:
    """Check if value is positive"""
    return value is not None and value > 0


def is_negative(value: Optional[float]) -> bool:
    """Check if value is negative"""
    return value is not None and value < 0


def format_currency(value: Optional[float], 
                   currency: str = 'INR',
                   unit: str = 'Cr',
                   decimals: int = 2) -> str:
    """
    Format value as currency string
    
    Args:
        value: Numeric value
        currency: Currency code
        unit: Unit (Cr, Lakhs, etc.)
        decimals: Decimal places
        
    Returns:
        Formatted string
    """
    if value is None:
        return '-'
    
    formatted = f"{value:,.{decimals}f}"
    return f"{currency} {formatted} {unit}"


def format_percentage(value: Optional[float], decimals: int = 2) -> str:
    """
    Format value as percentage string
    
    Args:
        value: Numeric value (already in percentage form)
        decimals: Decimal places
        
    Returns:
        Formatted string with % sign
    """
    if value is None:
        return '-'
    
    return f"{value:.{decimals}f}%"


def format_ratio(value: Optional[float], decimals: int = 2) -> str:
    """
    Format value as ratio string
    
    Args:
        value: Numeric value
        decimals: Decimal places
        
    Returns:
        Formatted string with 'x' suffix
    """
    if value is None:
        return '-'
    
    return f"{value:.{decimals}f}x"
