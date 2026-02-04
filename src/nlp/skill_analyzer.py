"""
NLP module for skill extraction and analysis
"""
import re
import sys
from pathlib import Path
from collections import Counter
import pandas as pd
import numpy as np
from typing import List, Dict, Set

sys.path.append(str(Path(__file__).parent.parent.parent))
from config.config import SKILL_CATEGORIES


class SkillAnalyzer:
    """Analyze and extract skills from job descriptions"""
    
    def __init__(self):
        self.skill_database = self._build_skill_database()
        self.skill_frequency = Counter()
        
    def _build_skill_database(self) -> Dict[str, Set[str]]:
        """Build comprehensive skill database"""
        
        skills_db = {
            'programming_languages': {
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'golang',
                'rust', 'kotlin', 'swift', 'php', 'ruby', 'scala', 'r', 'matlab',
                'dart', 'objective-c', 'perl', 'shell', 'bash', 'powershell', 'sql',
                'html', 'css', 'html5', 'css3'
            },
            
            'frameworks': {
                # Frontend
                'react', 'reactjs', 'vue', 'vuejs', 'angular', 'angularjs', 'nextjs',
                'nuxt', 'svelte', 'ember', 'backbone', 'jquery',
                
                # Backend
                'django', 'flask', 'fastapi', 'spring', 'spring boot', 'laravel',
                'express', 'expressjs', 'nestjs', 'asp.net', '.net', '.net core',
                'rails', 'ruby on rails', 'gin', 'echo', 'fiber',
                
                # Mobile
                'react native', 'flutter', 'ionic', 'xamarin',
                
                # Testing
                'pytest', 'unittest', 'jest', 'mocha', 'jasmine', 'selenium',
                'playwright', 'cypress', 'testcafe',
            },
            
            'tools_devops': {
                'git', 'github', 'gitlab', 'bitbucket', 'svn',
                'docker', 'kubernetes', 'k8s', 'helm', 'terraform', 'ansible',
                'jenkins', 'gitlab ci', 'github actions', 'circleci', 'travis ci',
                'aws', 'azure', 'gcp', 'heroku', 'digitalocean',
                'nginx', 'apache', 'iis', 'tomcat',
                'prometheus', 'grafana', 'elk', 'splunk', 'datadog',
                'vagrant', 'chef', 'puppet', 'salt',
            },
            
            'databases': {
                'mysql', 'postgresql', 'postgres', 'oracle', 'sql server', 'mssql',
                'mongodb', 'cassandra', 'redis', 'elasticsearch', 'dynamodb',
                'neo4j', 'couchdb', 'mariadb', 'sqlite', 'firestore',
                'influxdb', 'timescaledb', 'clickhouse',
            },
            
            'data_ai_ml': {
                'machine learning', 'deep learning', 'ai', 'ml', 'nlp', 'cv',
                'computer vision', 'llm', 'generative ai', 'tensorflow', 'pytorch',
                'keras', 'scikit-learn', 'sklearn', 'pandas', 'numpy', 'scipy',
                'matplotlib', 'seaborn', 'plotly', 'tableau', 'power bi',
                'spark', 'pyspark', 'hadoop', 'kafka', 'airflow', 'mlflow',
                'data science', 'data analysis', 'data engineering', 'etl',
                'big data', 'data warehouse', 'business intelligence', 'bi',
            },
            
            'methodologies': {
                'agile', 'scrum', 'kanban', 'lean', 'devops', 'ci/cd',
                'tdd', 'bdd', 'oop', 'functional programming', 'microservices',
                'rest api', 'graphql', 'soap', 'grpc', 'websocket',
                'mvc', 'mvvm', 'solid', 'design patterns',
            },
            
            'soft_skills': {
                'leadership', 'team management', 'communication', 'problem solving',
                'critical thinking', 'collaboration', 'english', 'japanese',
                'korean', 'chinese', 'project management', 'product management',
            },
            
            'specialized': {
                'blockchain', 'web3', 'smart contracts', 'solidity', 'defi',
                'cybersecurity', 'penetration testing', 'security', 'networking',
                'iot', 'embedded', 'firmware', 'robotics', 'ar', 'vr',
                'game development', 'unity', 'unreal engine', 'godot',
                'sap', 'erp', 'crm', 'salesforce', 'oracle erp',
            }
        }
        
        return skills_db
    
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract skills from text"""
        if pd.isna(text):
            return {category: [] for category in self.skill_database.keys()}
        
        text_lower = str(text).lower()
        extracted = {}
        
        for category, skills in self.skill_database.items():
            found_skills = []
            for skill in skills:
                # Use word boundary for better matching
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text_lower):
                    found_skills.append(skill)
            extracted[category] = found_skills
        
        return extracted
    
    def analyze_skill_trends(self, df: pd.DataFrame, 
                            skill_column: str = 'array_skills') -> pd.DataFrame:
        """Analyze skill trends from job postings"""
        print("📊 Analyzing skill trends...")
        
        all_skills = []
        
        for idx, row in df.iterrows():
            skills = row.get(skill_column, [])
            if isinstance(skills, str):
                try:
                    import ast
                    skills = ast.literal_eval(skills)
                except:
                    skills = []
            
            if isinstance(skills, list):
                all_skills.extend([s.lower() for s in skills if s])
        
        # Count skill frequency
        skill_counts = Counter(all_skills)
        
        # Create DataFrame
        trend_df = pd.DataFrame([
            {'skill': skill, 'count': count, 'percentage': count / len(df) * 100}
            for skill, count in skill_counts.most_common(50)
        ])
        
        return trend_df
    
    def categorize_job_skills(self, df: pd.DataFrame) -> pd.DataFrame:
        """Categorize all skills in the dataset"""
        print("🔍 Categorizing job skills...")
        
        # Initialize new columns
        for category in self.skill_database.keys():
            df[f'{category}_extracted'] = [[] for _ in range(len(df))]
        
        # Process each job
        for idx, row in df.iterrows():
            # Combine all text fields
            text_fields = []
            for col in ['job_names', 'array_skills', 'exp_skills']:
                if col in df.columns and pd.notna(row[col]):
                    text_fields.append(str(row[col]))
            
            combined_text = ' '.join(text_fields)
            
            # Extract skills
            extracted = self.extract_skills(combined_text)
            
            # Assign to DataFrame
            for category, skills in extracted.items():
                df.at[idx, f'{category}_extracted'] = skills
        
        return df
    
    def get_skill_cooccurrence(self, df: pd.DataFrame, 
                               skill_column: str = 'array_skills',
                               top_n: int = 20) -> pd.DataFrame:
        """Analyze which skills often appear together"""
        print("🔗 Analyzing skill co-occurrence...")
        
        import ast
        from itertools import combinations
        
        cooccurrence = Counter()
        
        for idx, row in df.iterrows():
            skills = row.get(skill_column, [])
            if isinstance(skills, str):
                try:
                    skills = ast.literal_eval(skills)
                except:
                    skills = []
            
            if isinstance(skills, list) and len(skills) > 1:
                # Get all pairs of skills
                skills_lower = [s.lower() for s in skills if s]
                for pair in combinations(sorted(skills_lower), 2):
                    cooccurrence[pair] += 1
        
        # Create DataFrame
        cooccur_df = pd.DataFrame([
            {'skill_1': pair[0], 'skill_2': pair[1], 'count': count}
            for pair, count in cooccurrence.most_common(top_n)
        ])
        
        return cooccur_df
    
    def generate_skill_recommendations(self, job_group: str, 
                                      current_skills: List[str],
                                      df: pd.DataFrame) -> List[str]:
        """Recommend skills to learn based on job group and current skills"""
        print(f"💡 Generating skill recommendations for {job_group}...")
        
        # Filter jobs by group
        group_df = df[df['job_group'] == job_group]
        
        if len(group_df) == 0:
            return []
        
        # Get all skills for this job group
        all_skills = []
        for idx, row in group_df.iterrows():
            skills = row.get('array_skills', [])
            if isinstance(skills, str):
                try:
                    import ast
                    skills = ast.literal_eval(skills)
                except:
                    skills = []
            if isinstance(skills, list):
                all_skills.extend([s.lower() for s in skills if s])
        
        # Count frequency
        skill_freq = Counter(all_skills)
        
        # Remove skills already known
        current_skills_lower = [s.lower() for s in current_skills]
        recommendations = []
        
        for skill, count in skill_freq.most_common(10):
            if skill not in current_skills_lower:
                recommendations.append({
                    'skill': skill,
                    'frequency': count,
                    'percentage': count / len(group_df) * 100
                })
        
        return recommendations[:5]  # Top 5 recommendations


if __name__ == "__main__":
    # Test skill analyzer
    from config.config import CLEAN_CSV_PATH
    
    analyzer = SkillAnalyzer()
    
    # Load data
    df = pd.read_csv(CLEAN_CSV_PATH)
    print(f"Loaded {len(df)} records")
    
    # Analyze trends
    trends = analyzer.analyze_skill_trends(df)
    print("\n📈 Top Skills:")
    print(trends.head(20))
    
    # Skill co-occurrence
    cooccur = analyzer.get_skill_cooccurrence(df)
    print("\n🔗 Skill Co-occurrence:")
    print(cooccur.head(10))
