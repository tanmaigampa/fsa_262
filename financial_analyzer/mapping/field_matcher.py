"""
Field matcher for mapping source field names to canonical fields
"""

from typing import Optional, List, Tuple
from ..core import FIELD_MAPPINGS, normalize_field_name
from ..utils import similarity_score


class FieldMatcher:
    """
    Matches source field names to canonical field names
    Uses exact matching, fuzzy matching, and keyword matching
    """
    
    def __init__(self, field_mappings: dict = None):
        """
        Initialize matcher
        
        Args:
            field_mappings: Custom field mappings (uses default if None)
        """
        self.field_mappings = field_mappings or FIELD_MAPPINGS
        
        # Create reverse mapping for faster lookup
        self._reverse_mapping = {}
        for canonical_field, variations in self.field_mappings.items():
            for variation in variations:
                normalized = normalize_field_name(variation)
                self._reverse_mapping[normalized] = canonical_field
    
    def find_canonical_field(self, source_field: str, threshold: float = 0.8) -> Optional[str]:
        """
        Find canonical field name for a source field
        
        Args:
            source_field: Source field name from statement
            threshold: Similarity threshold for fuzzy matching (0-1)
            
        Returns:
            Canonical field name or None if no match
        """
        if not source_field:
            return None
        
        normalized_source = normalize_field_name(source_field)
        
        # Try exact match first
        if normalized_source in self._reverse_mapping:
            return self._reverse_mapping[normalized_source]
        
        # Try fuzzy matching
        best_match = None
        best_score = 0.0
        
        for canonical_field, variations in self.field_mappings.items():
            for variation in variations:
                normalized_variation = normalize_field_name(variation)
                score = similarity_score(normalized_source, normalized_variation)
                
                if score > best_score and score >= threshold:
                    best_score = score
                    best_match = canonical_field
        
        return best_match
    
    def get_match_confidence(self, source_field: str, canonical_field: str) -> float:
        """
        Get confidence score for a match
        
        Args:
            source_field: Source field name
            canonical_field: Canonical field name
            
        Returns:
            Confidence score (0-1)
        """
        if not source_field or canonical_field not in self.field_mappings:
            return 0.0
        
        normalized_source = normalize_field_name(source_field)
        
        # Check against all variations
        max_score = 0.0
        for variation in self.field_mappings[canonical_field]:
            normalized_variation = normalize_field_name(variation)
            score = similarity_score(normalized_source, normalized_variation)
            max_score = max(max_score, score)
        
        return max_score
    
    def suggest_mappings(self, unmapped_fields: List[str], top_n: int = 3) -> dict:
        """
        Suggest possible canonical fields for unmapped fields
        
        Args:
            unmapped_fields: List of field names that didn't match
            top_n: Number of suggestions per field
            
        Returns:
            Dict mapping source field to list of (canonical_field, score) tuples
        """
        suggestions = {}
        
        for source_field in unmapped_fields:
            if not source_field:
                continue
            
            normalized_source = normalize_field_name(source_field)
            scores = []
            
            for canonical_field, variations in self.field_mappings.items():
                max_score = 0.0
                for variation in variations:
                    normalized_variation = normalize_field_name(variation)
                    score = similarity_score(normalized_source, normalized_variation)
                    max_score = max(max_score, score)
                
                if max_score > 0.3:  # Only suggest if some similarity
                    scores.append((canonical_field, max_score))
            
            # Sort by score and take top N
            scores.sort(key=lambda x: x[1], reverse=True)
            suggestions[source_field] = scores[:top_n]
        
        return suggestions
    
    def get_all_canonical_fields(self) -> List[str]:
        """
        Get list of all canonical field names
        
        Returns:
            List of canonical field names
        """
        return list(self.field_mappings.keys())
