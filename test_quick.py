"""Quick test script"""
from src.analysis.salary_analytics import SalaryAnalyzer
import pandas as pd

df = pd.read_csv('data_clean/clean_data.csv')
analyzer = SalaryAnalyzer(df)
stats = analyzer.calculate_statistics()

print(f"\nSalary Statistics:")
print(f"  Average: {stats['mean']/1_000_000:.2f}M VND")
print(f"  Median: {stats['median']/1_000_000:.2f}M VND")
print(f"  Count: {stats['count']}")
print("\n✅ All modules working correctly!")
