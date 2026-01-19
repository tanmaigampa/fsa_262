"""
Main orchestrator for Financial Statement Analyzer
Coordinates ingestion, mapping, analysis, and export
"""

from pathlib import Path
from typing import Optional, Dict
import sys

from financial_analyzer.ingestion import ExcelReader, ExcelCleaner
from financial_analyzer.mapping import FinancialDataMapper
from financial_analyzer.analysis import RatioCalculator
from financial_analyzer.core import CanonicalFinancialData, StatementType


class FinancialAnalyzer:
    """
    Main class that orchestrates the entire analysis workflow
    Works with ANY company's financial statements
    """
    
    def __init__(self):
        self.canonical_model: Optional[CanonicalFinancialData] = None
        self.ratios: Optional[Dict] = None
        self.metadata: Dict = {}
        self.cleaned_data: Dict = {}
        
    def analyze(self, 
                pl_file: Optional[str] = None,
                bs_file: Optional[str] = None,
                cf_file: Optional[str] = None) -> Dict:
        """
        Analyze financial statements
        
        Args:
            pl_file: Path to P&L file
            bs_file: Path to Balance Sheet file
            cf_file: Path to Cash Flow file
            
        Returns:
            Dictionary with results
        """
        print("="*60)
        print("FINANCIAL STATEMENT ANALYZER")
        print("="*60)
        
        # Step 1: Ingest and clean files
        print("\nStep 1: Ingesting and cleaning files...")
        cleaned_data = {}
        
        if pl_file:
            print(f"  Processing P&L: {Path(pl_file).name}")
            pl_df, pl_meta = self._ingest_file(pl_file, StatementType.PROFIT_LOSS)
            cleaned_data['P&L'] = pl_df
            self.metadata.update(pl_meta)
        
        if bs_file:
            print(f"  Processing Balance Sheet: {Path(bs_file).name}")
            bs_df, bs_meta = self._ingest_file(bs_file, StatementType.BALANCE_SHEET)
            cleaned_data['Balance Sheet'] = bs_df
            if not self.metadata:  # Use BS metadata if PL not provided
                self.metadata.update(bs_meta)
        
        if cf_file:
            print(f"  Processing Cash Flow: {Path(cf_file).name}")
            cf_df, cf_meta = self._ingest_file(cf_file, StatementType.CASH_FLOW)
            cleaned_data['Cash Flow'] = cf_df
            if not self.metadata:  # Use CF metadata if others not provided
                self.metadata.update(cf_meta)
        
        if not cleaned_data:
            raise ValueError("No files provided. Please provide at least one financial statement.")
        
        self.cleaned_data = cleaned_data
        
        print(f"\n  Company: {self.metadata.get('company_name', 'Unknown')}")
        print(f"  Currency: {self.metadata.get('currency', 'Unknown')}")
        print(f"  Unit: {self.metadata.get('unit', 'Unknown')}")
        
        # Step 2: Map to canonical model
        print("\nStep 2: Mapping to canonical model...")
        mapper = FinancialDataMapper(cleaned_data, self.metadata)
        self.canonical_model = mapper.map_all_statements()
        
        mapping_summary = mapper.get_mapping_summary()
        print(f"  Total mappings: {mapping_summary['total_mappings']}")
        for stmt, mappings in mapping_summary.get('by_statement', {}).items():
            print(f"  {stmt}: {len(mappings)} fields mapped")
        
        if mapping_summary.get('unmapped_fields'):
            print(f"  Warning: {len(mapping_summary['unmapped_fields'])} fields unmapped")
        
        # Step 3: Validate canonical model
        print("\nStep 3: Validating data...")
        warnings = self.canonical_model.validate()
        if warnings:
            print("  Warnings:")
            for stmt, issues in warnings.items():
                for issue in issues:
                    print(f"    - {stmt}: {issue}")
        else:
            print("  No validation warnings")
        
        # Step 4: Calculate ratios
        print("\nStep 4: Calculating financial ratios...")
        calculator = RatioCalculator(self.canonical_model)
        self.ratios = calculator.calculate_all_ratios()
        
        ratio_summary = calculator.get_ratio_summary()
        print(f"  Total ratios defined: {ratio_summary['total_ratios']}")
        print(f"  Years analyzed: {', '.join(ratio_summary['years'])}")
        for year, count in ratio_summary['calculated_per_year'].items():
            print(f"    {year}: {count}/{ratio_summary['total_ratios']} ratios calculated")
        
        # Step 5: Summary
        print("\n" + "="*60)
        print("ANALYSIS COMPLETE")
        print("="*60)
        print(f"Company: {self.canonical_model.company_name}")
        print(f"Years: {', '.join(self.canonical_model.get_available_years())}")
        print(f"Ratios calculated: {len(self.ratios)}")
        print("="*60)
        
        return {
            'canonical_model': self.canonical_model,
            'ratios': self.ratios,
            'metadata': self.metadata,
            'mapping_summary': mapping_summary,
            'ratio_summary': ratio_summary
        }
    
    def _ingest_file(self, file_path: str, expected_type: StatementType) -> tuple:
        """
        Ingest and clean a single file
        
        Args:
            file_path: Path to file
            expected_type: Expected statement type
            
        Returns:
            Tuple of (cleaned_df, metadata)
        """
        # Read file
        reader = ExcelReader(file_path)
        raw_df = reader.read()
        metadata = reader.extract_metadata()
        
        # Verify it's the right type
        detected_type = reader.identify_statement_type()
        if detected_type != expected_type:
            print(f"    Warning: Expected {expected_type.value}, detected {detected_type.value}")
        
        # Clean
        cleaner = ExcelCleaner(raw_df, metadata)
        cleaned_df = cleaner.clean()
        
        print(f"    Rows extracted: {len(cleaned_df)}")
        print(f"    Years found: {', '.join(cleaner.get_years())}")
        
        return cleaned_df, metadata
    
    def print_ratio_table(self):
        """Print ratios in table format"""
        if not self.ratios:
            print("No ratios calculated yet. Run analyze() first.")
            return
        
        years = self.canonical_model.get_available_years()
        
        print("\n" + "="*80)
        print("FINANCIAL RATIOS")
        print("="*80)
        
        # Print header
        header = f"{'Ratio':<40}"
        for year in years:
            header += f"{year:>12}"
        print(header)
        print("-"*80)
        
        # Print ratios
        for ratio_name, values in self.ratios.items():
            row = f"{ratio_name:<40}"
            for year in years:
                value = values.get(year)
                if value is not None:
                    row += f"{value:12.2f}"
                else:
                    row += f"{'N/A':>12}"
            print(row)
        
        print("="*80)


def main():
    """
    Command-line interface
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Analyze financial statements from ANY company'
    )
    parser.add_argument('--pl', help='Path to Profit & Loss statement')
    parser.add_argument('--bs', help='Path to Balance Sheet')
    parser.add_argument('--cf', help='Path to Cash Flow statement')
    parser.add_argument('--output', help='Output Excel file path', default='financial_analysis.xlsx')
    
    args = parser.parse_args()
    
    if not (args.pl or args.bs or args.cf):
        parser.print_help()
        print("\nError: Please provide at least one financial statement file")
        sys.exit(1)
    
    # Run analysis
    analyzer = FinancialAnalyzer()
    
    try:
        results = analyzer.analyze(
            pl_file=args.pl,
            bs_file=args.bs,
            cf_file=args.cf
        )
        
        # Print ratio table
        analyzer.print_ratio_table()
        
        # TODO: Export to Excel (next step)
        print(f"\nResults ready for export to: {args.output}")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
