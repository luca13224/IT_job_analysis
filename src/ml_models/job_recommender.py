"""
Job Recommendation System
Content-based filtering using TF-IDF and cosine similarity
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
from config.config import CLEAN_CSV_PATH


class JobRecommender:
    """Recommend jobs based on user skills and preferences"""
    
    def __init__(self):
        self.df = None
        self.tfidf_matrix = None
        self.vectorizer = None
        
    def load_data(self, file_path=None):
        """Load job data"""
        file_path = file_path or CLEAN_CSV_PATH
        self.df = pd.read_csv(file_path)
        print(f"✓ Loaded {len(self.df)} jobs")
        return self
    
    def build_features(self):
        """Build TF-IDF features from job skills"""
        # Extract skills text
        skills_text = []
        for idx, row in self.df.iterrows():
            try:
                skills = ast.literal_eval(str(row.get('array_skills', '[]')))
                if isinstance(skills, list):
                    skills_text.append(' '.join([str(s).lower() for s in skills if s]))
                else:
                    skills_text.append('')
            except:
                skills_text.append('')
        
        self.df['skills_text'] = skills_text
        
        # Build TF-IDF matrix
        self.vectorizer = TfidfVectorizer(
            max_features=200,
            stop_words='english'
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['skills_text'])
        
        print(f"✓ Built TF-IDF matrix: {self.tfidf_matrix.shape}")
        return self
    
    def recommend_by_skills(self, user_skills, top_n=10, level=None, city=None, min_salary=None):
        """Recommend jobs based on user skills"""
        # Convert user skills to TF-IDF vector
        user_skills_text = ' '.join([s.lower() for s in user_skills])
        user_vector = self.vectorizer.transform([user_skills_text])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(user_vector, self.tfidf_matrix).flatten()
        
        # Add similarity scores to dataframe
        self.df['similarity'] = similarities
        
        # Filter by preferences
        filtered_df = self.df.copy()
        
        if level:
            filtered_df = filtered_df[filtered_df['level'] == level]
        
        if city:
            filtered_df = filtered_df[filtered_df['city'] == city]
        
        if min_salary:
            filtered_df = filtered_df[
                (filtered_df['salary_numeric'].notna()) & 
                (filtered_df['salary_numeric'] >= min_salary)
            ]
        
        # Sort by similarity
        recommendations = filtered_df.nlargest(top_n, 'similarity')
        
        return recommendations[[
            'job_titles', 'company_names', 'job_group', 'level', 
            'city', 'salary_numeric', 'similarity', 'array_skills'
        ]]
    
    def get_skill_match(self, user_skills, job_skills_str):
        """Calculate skill match percentage"""
        try:
            job_skills = ast.literal_eval(str(job_skills_str))
            if not isinstance(job_skills, list):
                return 0
            
            job_skills_lower = [s.lower() for s in job_skills if s]
            user_skills_lower = [s.lower() for s in user_skills]
            
            matched = len(set(user_skills_lower) & set(job_skills_lower))
            total = len(job_skills_lower)
            
            return (matched / total * 100) if total > 0 else 0
        except:
            return 0


def main():
    """Demo recommendation system"""
    recommender = JobRecommender()
    recommender.load_data()
    recommender.build_features()
    
    # Example: Recommend jobs for a Python developer
    user_skills = ['python', 'django', 'postgresql', 'docker']
    
    print(f"\n{'='*70}")
    print(f"Job Recommendations for skills: {', '.join(user_skills)}")
    print(f"{'='*70}\n")
    
    recommendations = recommender.recommend_by_skills(
        user_skills=user_skills,
        top_n=5,
        level='mid',
        city='Hồ Chí Minh'
    )
    
    for idx, row in recommendations.iterrows():
        print(f"\n{idx+1}. {row['job_titles']}")
        print(f"   Company: {row['company_names']}")
        print(f"   Level: {row['level']} | City: {row['city']}")
        print(f"   Salary: {row['salary_numeric']/1_000_000:.1f}M VND" if pd.notna(row['salary_numeric']) else "   Salary: Negotiable")
        print(f"   Match: {row['similarity']*100:.1f}%")


if __name__ == "__main__":
    main()
