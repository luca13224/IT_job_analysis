"""
Data processing and cleaning module
"""
import os
import sys
import ast
import re
import pandas as pd
import numpy as np
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from config.config import CSV_PATH, CLEAN_CSV_PATH, SALARY_RANGES


class DataProcessor:
    """Process and clean job market data"""
    
    def __init__(self, input_path=None, output_path=None):
        self.input_path = input_path or CSV_PATH
        self.output_path = output_path or CLEAN_CSV_PATH
        self.df = None
        
    def load_data(self):
        """Load raw data from CSV"""
        print(f"📂 Loading data from {self.input_path}")
        self.df = pd.read_csv(self.input_path)
        print(f"✓ Loaded {len(self.df)} records")
        return self
    
    def clean_salary(self):
        """Clean and parse salary information"""
        print("💰 Cleaning salary data...")
        
        def parse_salary(salary_str):
            """Parse salary string to numeric value (USD/month)"""
            if pd.isna(salary_str) or salary_str == "Unknown":
                return None
            
            # Extract numbers from string
            numbers = re.findall(r'\d+', salary_str)
            if not numbers:
                return None
            
            # Get first number (usually the base or "Up to" value)
            value = int(numbers[0])
            
            # Convert to VND if in USD (assuming 1 USD = 24,000 VND)
            if "$" in salary_str:
                value = value * 24_000
            elif "K" in salary_str or "k" in salary_str:
                value = value * 1_000_000
                
            return value
        
        self.df['salary_numeric'] = self.df['salaries'].apply(parse_salary)
        print(f"✓ Parsed {self.df['salary_numeric'].notna().sum()} salary values")
        return self
    
    def categorize_skills(self):
        """Categorize skills into different types"""
        print("🔧 Categorizing skills...")
        
        def safe_eval(x):
            """Safely evaluate string representation of list"""
            try:
                return ast.literal_eval(x) if isinstance(x, str) else []
            except:
                return []
        
        # Process skills columns
        skill_columns = ['array_skills', 'programming_languages', 'frameworks', 
                        'tools', 'libraries', 'languages']
        
        for col in skill_columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].apply(safe_eval)
        
        print("✓ Skills categorized")
        return self
    
    def extract_job_groups(self):
        """Extract and normalize job groups from job names"""
        print("👥 Extracting job groups...")
        
        job_keywords = {
            'Backend Developer': ['backend', 'back-end', 'server'],
            'Frontend Developer': ['frontend', 'front-end'],
            'Fullstack Developer': ['fullstack', 'full-stack', 'full stack'],
            'Mobile Developer': ['mobile', 'ios', 'android'],
            'Data / AI': ['data scientist', 'data engineer', 'machine learning', 'ai', 'ml engineer'],
            'DevOps / Cloud': ['devops', 'cloud', 'sre', 'infrastructure'],
            'QA / Tester': ['tester', 'qa', 'quality assurance', 'test'],
            'UX/UI Designer': ['ux', 'ui', 'designer', 'design'],
            'Manager / Lead': ['manager', 'lead', 'director', 'head', 'cto', 'cio'],
            'Security': ['security', 'cybersecurity', 'infosec'],
            'Database': ['dba', 'database administrator'],
            'Embedded / Firmware': ['embedded', 'firmware', 'iot'],
            'Game': ['game developer', 'game designer', 'unity'],
            'ERP / Enterprise': ['erp', 'sap', 'oracle erp'],
        }
        
        def classify_job(job_name):
            if pd.isna(job_name):
                return 'Other'
            
            job_name_lower = job_name.lower()
            for group, keywords in job_keywords.items():
                if any(keyword in job_name_lower for keyword in keywords):
                    return group
            return 'Other'
        
        self.df['job_group'] = self.df['job_names'].apply(classify_job)
        print(f"✓ Identified {self.df['job_group'].nunique()} job groups")
        return self
    
    def extract_experience_level(self):
        """Extract experience level from job requirements"""
        print("📊 Extracting experience levels...")
        
        def get_level(row):
            """Determine experience level from job data"""
            # Check if level column exists
            if 'position_names' in row and pd.notna(row['position_names']):
                pos = str(row['position_names']).lower()
                if any(x in pos for x in ['fresher', 'intern', 'entry']):
                    return 'fresher'
                elif any(x in pos for x in ['junior', 'jr']):
                    return 'junior'
                elif any(x in pos for x in ['senior', 'sr']):
                    return 'senior'
                elif any(x in pos for x in ['lead', 'principal', 'staff']):
                    return 'lead'
                elif any(x in pos for x in ['manager', 'director', 'head']):
                    return 'manager'
            
            # Check from job name
            job_name = str(row.get('job_names', '')).lower()
            if any(x in job_name for x in ['senior', 'sr.']):
                return 'senior'
            elif any(x in job_name for x in ['junior', 'jr.']):
                return 'junior'
            elif any(x in job_name for x in ['lead', 'principal']):
                return 'lead'
            elif any(x in job_name for x in ['manager', 'head', 'director']):
                return 'manager'
            else:
                return 'mid'
        
        self.df['level'] = self.df.apply(get_level, axis=1)
        print(f"✓ Experience levels: {self.df['level'].value_counts().to_dict()}")
        return self
    
    def clean_location(self):
        """Standardize location names"""
        print("🌍 Cleaning location data...")
        
        def standardize_city(location):
            if pd.isna(location):
                return 'Unknown'
            
            location = str(location).lower()
            if 'ho chi minh' in location or 'hcm' in location or 'saigon' in location:
                return 'Ho Chi Minh'
            elif 'ha noi' in location or 'hanoi' in location:
                return 'Ha Noi'
            elif 'da nang' in location or 'danang' in location:
                return 'Da Nang'
            elif 'can tho' in location:
                return 'Can Tho'
            elif 'hai phong' in location:
                return 'Hai Phong'
            else:
                return 'Other'
        
        if 'locate_names' in self.df.columns:
            self.df['city'] = self.df['locate_names'].apply(standardize_city)
        elif 'city' not in self.df.columns:
            self.df['city'] = 'Unknown'
            
        print(f"✓ Cities: {self.df['city'].value_counts().to_dict()}")
        return self
    
    def remove_duplicates(self):
        """Remove duplicate job postings"""
        print("🔄 Removing duplicates...")
        before = len(self.df)
        self.df = self.df.drop_duplicates(subset=['job_names', 'company_names'], keep='first')
        after = len(self.df)
        print(f"✓ Removed {before - after} duplicates")
        return self
    
    def save_cleaned_data(self):
        """Save cleaned data to CSV"""
        print(f"💾 Saving cleaned data to {self.output_path}")
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.df.to_csv(self.output_path, index=False, encoding='utf-8-sig')
        print(f"✓ Saved {len(self.df)} records")
        return self
    
    def process_pipeline(self):
        """Run complete data processing pipeline"""
        print("\n" + "="*60)
        print("🚀 STARTING DATA PROCESSING PIPELINE")
        print("="*60 + "\n")
        
        (self.load_data()
            .remove_duplicates()
            .clean_salary()
            .categorize_skills()
            .extract_job_groups()
            .extract_experience_level()
            .clean_location()
            .save_cleaned_data())
        
        print("\n" + "="*60)
        print("✅ DATA PROCESSING COMPLETED")
        print("="*60 + "\n")
        
        return self
    
    def get_summary(self):
        """Get summary statistics of cleaned data"""
        if self.df is None:
            print("⚠️  No data loaded")
            return
        
        print("\n📊 DATA SUMMARY")
        print("-" * 60)
        print(f"Total records: {len(self.df)}")
        print(f"Columns: {len(self.df.columns)}")
        print(f"Date range: {self.df.get('post_dates_formatted', pd.Series()).min()} to {self.df.get('post_dates_formatted', pd.Series()).max()}")
        print(f"\nJob groups: {self.df['job_group'].nunique()}")
        print(self.df['job_group'].value_counts().head(10))
        print(f"\nCities: {self.df['city'].nunique()}")
        print(self.df['city'].value_counts())
        print(f"\nSalary data: {self.df['salary_numeric'].notna().sum()} records with salary info")
        print("-" * 60)


if __name__ == "__main__":
    # Run processing pipeline
    processor = DataProcessor()
    processor.process_pipeline()
    processor.get_summary()
