"""
Salary Analytics Module
Analyze salary trends, distributions, and predictions
"""
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple

sys.path.append(str(Path(__file__).parent.parent.parent))
from config.config import SALARY_RANGES, OUTPUTS_DIR


class SalaryAnalyzer:
    """Analyze salary data and trends"""
    
    def __init__(self, df: pd.DataFrame = None):
        self.df = df
        self.stats = {}
        
    def load_data(self, file_path):
        """Load data from file"""
        self.df = pd.read_csv(file_path)
        return self
    
    def calculate_statistics(self) -> Dict:
        """Calculate salary statistics"""
        print("📊 Calculating salary statistics...")
        
        # Filter valid salary data
        valid_salaries = self.df[self.df['salary_numeric'].notna()]['salary_numeric']
        
        if len(valid_salaries) == 0:
            print("⚠️  No valid salary data found")
            return {}
        
        self.stats = {
            'count': len(valid_salaries),
            'mean': valid_salaries.mean(),
            'median': valid_salaries.median(),
            'std': valid_salaries.std(),
            'min': valid_salaries.min(),
            'max': valid_salaries.max(),
            'q25': valid_salaries.quantile(0.25),
            'q75': valid_salaries.quantile(0.75),
        }
        
        print(f"✓ Analyzed {self.stats['count']} salary records")
        return self.stats
    
    def salary_by_job_group(self) -> pd.DataFrame:
        """Analyze salary distribution by job group"""
        print("💼 Analyzing salary by job group...")
        
        # Filter valid data
        df_valid = self.df[self.df['salary_numeric'].notna()].copy()
        
        # Group by job group
        salary_by_group = df_valid.groupby('job_group')['salary_numeric'].agg([
            ('count', 'count'),
            ('mean', 'mean'),
            ('median', 'median'),
            ('min', 'min'),
            ('max', 'max'),
            ('std', 'std')
        ]).round(0)
        
        salary_by_group = salary_by_group.sort_values('median', ascending=False)
        
        return salary_by_group
    
    def salary_by_level(self) -> pd.DataFrame:
        """Analyze salary distribution by experience level"""
        print("📈 Analyzing salary by experience level...")
        
        # Filter valid data
        df_valid = self.df[self.df['salary_numeric'].notna()].copy()
        
        # Group by level
        salary_by_level = df_valid.groupby('level')['salary_numeric'].agg([
            ('count', 'count'),
            ('mean', 'mean'),
            ('median', 'median'),
            ('min', 'min'),
            ('max', 'max'),
        ]).round(0)
        
        # Sort by predefined level order
        level_order = ['fresher', 'junior', 'mid', 'senior', 'lead', 'manager']
        salary_by_level = salary_by_level.reindex(
            [l for l in level_order if l in salary_by_level.index]
        )
        
        return salary_by_level
    
    def salary_by_city(self) -> pd.DataFrame:
        """Analyze salary distribution by city"""
        print("🌍 Analyzing salary by city...")
        
        # Filter valid data
        df_valid = self.df[self.df['salary_numeric'].notna()].copy()
        
        # Group by city
        salary_by_city = df_valid.groupby('city')['salary_numeric'].agg([
            ('count', 'count'),
            ('mean', 'mean'),
            ('median', 'median'),
        ]).round(0)
        
        salary_by_city = salary_by_city.sort_values('median', ascending=False)
        
        return salary_by_city
    
    def salary_by_skill(self, top_n: int = 20) -> pd.DataFrame:
        """Analyze average salary by skill"""
        print(f"🔧 Analyzing salary by skill (top {top_n})...")
        
        import ast
        
        # Filter valid data
        df_valid = self.df[self.df['salary_numeric'].notna()].copy()
        
        # Collect skill-salary pairs
        skill_salaries = {}
        
        for idx, row in df_valid.iterrows():
            skills = row.get('array_skills', [])
            if isinstance(skills, str):
                try:
                    skills = ast.literal_eval(skills)
                except:
                    skills = []
            
            salary = row['salary_numeric']
            
            if isinstance(skills, list):
                for skill in skills:
                    skill_lower = str(skill).lower().strip()
                    if skill_lower not in skill_salaries:
                        skill_salaries[skill_lower] = []
                    skill_salaries[skill_lower].append(salary)
        
        # Calculate statistics
        skill_stats = []
        for skill, salaries in skill_salaries.items():
            if len(salaries) >= 3:  # At least 3 occurrences
                skill_stats.append({
                    'skill': skill,
                    'count': len(salaries),
                    'avg_salary': np.mean(salaries),
                    'median_salary': np.median(salaries),
                })
        
        # Create DataFrame
        df_skill_salary = pd.DataFrame(skill_stats)
        df_skill_salary = df_skill_salary.sort_values('avg_salary', ascending=False)
        
        return df_skill_salary.head(top_n)
    
    def plot_salary_distribution(self, save_path=None):
        """Plot salary distribution"""
        print("📊 Plotting salary distribution...")
        
        df_valid = self.df[self.df['salary_numeric'].notna()].copy()
        
        if len(df_valid) == 0:
            print("⚠️  No valid data to plot")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Histogram
        axes[0, 0].hist(df_valid['salary_numeric'] / 1_000_000, bins=30, 
                       edgecolor='black', alpha=0.7)
        axes[0, 0].set_xlabel('Salary (Million VND)')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].set_title('Salary Distribution')
        axes[0, 0].grid(alpha=0.3)
        
        # 2. Box plot by level
        level_order = ['fresher', 'junior', 'mid', 'senior', 'lead', 'manager']
        df_plot = df_valid[df_valid['level'].isin(level_order)]
        if len(df_plot) > 0:
            df_plot['salary_m'] = df_plot['salary_numeric'] / 1_000_000
            sns.boxplot(data=df_plot, x='level', y='salary_m', 
                       order=level_order, ax=axes[0, 1])
            axes[0, 1].set_xlabel('Experience Level')
            axes[0, 1].set_ylabel('Salary (Million VND)')
            axes[0, 1].set_title('Salary by Experience Level')
            axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. Top job groups by salary
        salary_by_group = self.salary_by_job_group().head(10)
        salary_by_group['median_m'] = salary_by_group['median'] / 1_000_000
        salary_by_group['median_m'].plot(kind='barh', ax=axes[1, 0], 
                                         color='skyblue', edgecolor='black')
        axes[1, 0].set_xlabel('Median Salary (Million VND)')
        axes[1, 0].set_ylabel('Job Group')
        axes[1, 0].set_title('Top 10 Job Groups by Median Salary')
        
        # 4. Salary by city
        salary_by_city = self.salary_by_city()
        if len(salary_by_city) > 0:
            salary_by_city['median_m'] = salary_by_city['median'] / 1_000_000
            salary_by_city['median_m'].plot(kind='bar', ax=axes[1, 1],
                                            color='lightgreen', edgecolor='black')
            axes[1, 1].set_xlabel('City')
            axes[1, 1].set_ylabel('Median Salary (Million VND)')
            axes[1, 1].set_title('Median Salary by City')
            axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved plot to {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_salary_trends(self, save_path=None):
        """Plot salary trends over time"""
        print("📈 Plotting salary trends...")
        
        # Check if date column exists
        if 'post_dates_formatted' not in self.df.columns:
            print("⚠️  No date column found")
            return
        
        df_valid = self.df[
            (self.df['salary_numeric'].notna()) & 
            (self.df['post_dates_formatted'].notna())
        ].copy()
        
        if len(df_valid) == 0:
            print("⚠️  No valid data to plot")
            return
        
        # Convert to datetime
        try:
            df_valid['post_date'] = pd.to_datetime(df_valid['post_dates_formatted'], 
                                                   format='%d/%m/%Y %H:%M', errors='coerce')
            df_valid = df_valid[df_valid['post_date'].notna()]
            
            # Group by month
            df_valid['year_month'] = df_valid['post_date'].dt.to_period('M')
            monthly_avg = df_valid.groupby('year_month')['salary_numeric'].mean() / 1_000_000
            
            plt.figure(figsize=(12, 6))
            monthly_avg.plot(kind='line', marker='o', linewidth=2)
            plt.xlabel('Month')
            plt.ylabel('Average Salary (Million VND)')
            plt.title('Average Salary Trend Over Time')
            plt.grid(alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"✓ Saved plot to {save_path}")
            else:
                plt.show()
            
            plt.close()
            
        except Exception as e:
            print(f"⚠️  Error plotting trends: {e}")
    
    def generate_report(self) -> str:
        """Generate text report of salary analysis"""
        print("📝 Generating salary report...")
        
        self.calculate_statistics()
        
        report = []
        report.append("=" * 70)
        report.append("SALARY ANALYSIS REPORT")
        report.append("=" * 70)
        report.append("")
        
        # Overall statistics
        report.append("📊 OVERALL STATISTICS")
        report.append("-" * 70)
        report.append(f"Total jobs with salary info: {self.stats.get('count', 0):,}")
        report.append(f"Average salary: {self.stats.get('mean', 0)/1_000_000:.2f} million VND")
        report.append(f"Median salary: {self.stats.get('median', 0)/1_000_000:.2f} million VND")
        report.append(f"Salary range: {self.stats.get('min', 0)/1_000_000:.2f} - {self.stats.get('max', 0)/1_000_000:.2f} million VND")
        report.append("")
        
        # By job group
        report.append("💼 TOP 10 JOB GROUPS BY MEDIAN SALARY")
        report.append("-" * 70)
        salary_by_group = self.salary_by_job_group().head(10)
        for job_group, row in salary_by_group.iterrows():
            report.append(f"{job_group:30s} {row['median']/1_000_000:8.2f}M VND ({int(row['count'])} jobs)")
        report.append("")
        
        # By level
        report.append("📈 SALARY BY EXPERIENCE LEVEL")
        report.append("-" * 70)
        salary_by_level = self.salary_by_level()
        for level, row in salary_by_level.iterrows():
            report.append(f"{level:15s} {row['median']/1_000_000:8.2f}M VND (range: {row['min']/1_000_000:.1f} - {row['max']/1_000_000:.1f}M)")
        report.append("")
        
        # By city
        report.append("🌍 SALARY BY CITY")
        report.append("-" * 70)
        salary_by_city = self.salary_by_city()
        for city, row in salary_by_city.iterrows():
            report.append(f"{city:20s} {row['median']/1_000_000:8.2f}M VND ({int(row['count'])} jobs)")
        report.append("")
        
        report.append("=" * 70)
        
        return "\n".join(report)


if __name__ == "__main__":
    from config.config import CLEAN_CSV_PATH
    
    # Load data
    df = pd.read_csv(CLEAN_CSV_PATH)
    
    # Create analyzer
    analyzer = SalaryAnalyzer(df)
    
    # Generate report
    report = analyzer.generate_report()
    print(report)
    
    # Create plots
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    analyzer.plot_salary_distribution(OUTPUTS_DIR / "salary_distribution.png")
    analyzer.plot_salary_trends(OUTPUTS_DIR / "salary_trends.png")
    
    print(f"\n✓ Analysis complete! Check outputs in: {OUTPUTS_DIR}")
