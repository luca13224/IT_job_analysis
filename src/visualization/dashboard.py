"""
Interactive Dashboard using Streamlit
"""
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from collections import Counter
import ast

sys.path.append(str(Path(__file__).parent.parent.parent))
from config.config import CLEAN_CSV_PATH
from src.analysis.salary_analytics import SalaryAnalyzer
from src.nlp.skill_analyzer import SkillAnalyzer


# Page config
st.set_page_config(
    page_title="Vietnam IT Job Market Analytics",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load and cache data"""
    try:
        df = pd.read_csv(CLEAN_CSV_PATH)
        return df
    except FileNotFoundError:
        st.error(f"Data file not found: {CLEAN_CSV_PATH}")
        st.info("Please run the data processing pipeline first: python src/data_processing/processor.py")
        st.stop()


def parse_list_field(field):
    """Parse string representation of list"""
    if pd.isna(field):
        return []
    if isinstance(field, list):
        return field
    try:
        return ast.literal_eval(field)
    except:
        return []


def main():
    # Header
    st.markdown('<p class="main-header">🇻🇳 Vietnam IT Job Market Analytics Dashboard</p>', 
                unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading data..."):
        df = load_data()
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Job group filter
    job_groups = ['All'] + sorted(df['job_group'].unique().tolist())
    selected_job_group = st.sidebar.selectbox("Job Group", job_groups)
    
    # Level filter
    levels = ['All'] + sorted(df['level'].unique().tolist())
    selected_level = st.sidebar.selectbox("Experience Level", levels)
    
    # City filter
    cities = ['All'] + sorted(df['city'].unique().tolist())
    selected_city = st.sidebar.selectbox("City", cities)
    
    # Apply filters
    filtered_df = df.copy()
    if selected_job_group != 'All':
        filtered_df = filtered_df[filtered_df['job_group'] == selected_job_group]
    if selected_level != 'All':
        filtered_df = filtered_df[filtered_df['level'] == selected_level]
    if selected_city != 'All':
        filtered_df = filtered_df[filtered_df['city'] == selected_city]
    
    # Overview metrics
    st.header("📊 Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Jobs", f"{len(filtered_df):,}")
    
    with col2:
        st.metric("Job Groups", f"{filtered_df['job_group'].nunique()}")
    
    with col3:
        st.metric("Companies", f"{filtered_df['company_names'].nunique()}")
    
    with col4:
        jobs_with_salary = filtered_df['salary_numeric'].notna().sum()
        st.metric("Jobs with Salary", f"{jobs_with_salary:,}")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💰 Salary Analysis", 
        "📈 Job Market Trends",
        "🔧 Skills Analysis",
        "🌍 Geographic Distribution",
        "🎯 Job Recommendations"
    ])
    
    # Tab 1: Salary Analysis
    with tab1:
        st.subheader("💰 Salary Analysis")
        
        analyzer = SalaryAnalyzer(filtered_df)
        
        # Salary statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("#### Overall Statistics")
            stats = analyzer.calculate_statistics()
            if stats:
                st.write(f"**Average Salary:** {stats['mean']/1_000_000:.2f}M VND")
                st.write(f"**Median Salary:** {stats['median']/1_000_000:.2f}M VND")
                st.write(f"**Min - Max:** {stats['min']/1_000_000:.2f}M - {stats['max']/1_000_000:.2f}M VND")
                st.write(f"**Jobs with Salary:** {stats['count']:,}")
        
        with col2:
            st.write("#### By Experience Level")
            salary_by_level = analyzer.salary_by_level()
            if not salary_by_level.empty:
                st.dataframe(
                    salary_by_level[['median', 'count']].rename(columns={
                        'median': 'Median Salary (VND)',
                        'count': 'Job Count'
                    }),
                    use_container_width=True
                )
        
        # Salary distribution plot
        st.write("#### Salary Distribution")
        df_with_salary = filtered_df[filtered_df['salary_numeric'].notna()].copy()
        
        if len(df_with_salary) > 0:
            df_with_salary['salary_m'] = df_with_salary['salary_numeric'] / 1_000_000
            
            fig = px.histogram(
                df_with_salary,
                x='salary_m',
                nbins=30,
                title="Salary Distribution",
                labels={'salary_m': 'Salary (Million VND)'},
                color_discrete_sequence=['#1f77b4']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Box plot by job group
            if selected_job_group == 'All':
                top_groups = df_with_salary['job_group'].value_counts().head(10).index
                df_top_groups = df_with_salary[df_with_salary['job_group'].isin(top_groups)]
                
                fig2 = px.box(
                    df_top_groups,
                    x='job_group',
                    y='salary_m',
                    title="Salary Distribution by Job Group (Top 10)",
                    labels={'salary_m': 'Salary (Million VND)', 'job_group': 'Job Group'}
                )
                fig2.update_xaxes(tickangle=45)
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No salary data available for current filters")
        
        # Top paying skills
        st.write("#### Top Paying Skills")
        salary_by_skill = analyzer.salary_by_skill(top_n=15)
        if not salary_by_skill.empty:
            fig3 = px.bar(
                salary_by_skill,
                x='avg_salary',
                y='skill',
                orientation='h',
                title="Average Salary by Skill (Top 15)",
                labels={'avg_salary': 'Average Salary (VND)', 'skill': 'Skill'},
                color='avg_salary',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig3, use_container_width=True)
    
    # Tab 2: Job Market Trends
    with tab2:
        st.subheader("📈 Job Market Trends")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Job distribution by group
            st.write("#### Job Distribution by Group")
            job_counts = filtered_df['job_group'].value_counts().head(10)
            fig = px.bar(
                x=job_counts.values,
                y=job_counts.index,
                orientation='h',
                title="Top 10 Job Groups",
                labels={'x': 'Number of Jobs', 'y': 'Job Group'},
                color=job_counts.values,
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Level distribution
            st.write("#### Experience Level Distribution")
            level_counts = filtered_df['level'].value_counts()
            fig = px.pie(
                values=level_counts.values,
                names=level_counts.index,
                title="Experience Level Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Work mode analysis
        if 'kind_jobs' in filtered_df.columns:
            st.write("#### Work Mode Distribution")
            work_mode = filtered_df['kind_jobs'].value_counts()
            fig = px.pie(
                values=work_mode.values,
                names=work_mode.index,
                title="Work Mode Distribution",
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 3: Skills Analysis
    with tab3:
        st.subheader("🔧 Skills Analysis")
        
        # Top skills
        all_skills = []
        for idx, row in filtered_df.iterrows():
            skills = parse_list_field(row.get('array_skills', []))
            all_skills.extend([s.lower() for s in skills if s])
        
        skill_counts = Counter(all_skills)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("#### Most In-Demand Skills")
            top_skills = dict(skill_counts.most_common(20))
            
            fig = px.bar(
                x=list(top_skills.values()),
                y=list(top_skills.keys()),
                orientation='h',
                title="Top 20 Skills",
                labels={'x': 'Frequency', 'y': 'Skill'},
                color=list(top_skills.values()),
                color_continuous_scale='Teal'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("#### Skill Breakdown")
            
            # Categorize skills
            programming_langs = ['python', 'java', 'javascript', 'c++', 'c#', 'go', 'php', 'typescript']
            frameworks = ['react', 'vue', 'angular', 'django', 'spring', 'laravel', 'flask', '.net']
            
            lang_count = sum(skill_counts.get(lang, 0) for lang in programming_langs)
            framework_count = sum(skill_counts.get(fw, 0) for fw in frameworks)
            other_count = sum(skill_counts.values()) - lang_count - framework_count
            
            fig = px.pie(
                values=[lang_count, framework_count, other_count],
                names=['Programming Languages', 'Frameworks', 'Other Skills'],
                title="Skill Categories"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Skill co-occurrence
        st.write("#### Skill Co-occurrence (What skills go together?)")
        
        skill_pairs = Counter()
        for idx, row in filtered_df.iterrows():
            skills = parse_list_field(row.get('array_skills', []))
            skills = [s.lower() for s in skills if s]
            if len(skills) > 1:
                from itertools import combinations
                for pair in combinations(sorted(skills), 2):
                    skill_pairs[pair] += 1
        
        top_pairs = skill_pairs.most_common(15)
        if top_pairs:
            pair_df = pd.DataFrame([
                {'Skill 1': pair[0], 'Skill 2': pair[1], 'Count': count}
                for pair, count in top_pairs
            ])
            st.dataframe(pair_df, use_container_width=True)
    
    # Tab 4: Geographic Distribution
    with tab4:
        st.subheader("🌍 Geographic Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Jobs by city
            st.write("#### Jobs by City")
            city_counts = filtered_df['city'].value_counts()
            fig = px.bar(
                x=city_counts.index,
                y=city_counts.values,
                title="Job Distribution by City",
                labels={'x': 'City', 'y': 'Number of Jobs'},
                color=city_counts.values,
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Salary by city
            st.write("#### Average Salary by City")
            df_with_salary = filtered_df[filtered_df['salary_numeric'].notna()]
            if len(df_with_salary) > 0:
                city_salary = df_with_salary.groupby('city')['salary_numeric'].mean() / 1_000_000
                fig = px.bar(
                    x=city_salary.index,
                    y=city_salary.values,
                    title="Average Salary by City",
                    labels={'x': 'City', 'y': 'Average Salary (Million VND)'},
                    color=city_salary.values,
                    color_continuous_scale='Greens'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Top companies
        st.write("#### Top Hiring Companies")
        top_companies = filtered_df['company_names'].value_counts().head(15)
        fig = px.bar(
            x=top_companies.values,
            y=top_companies.index,
            orientation='h',
            title="Top 15 Hiring Companies",
            labels={'x': 'Number of Jobs', 'y': 'Company'},
            color=top_companies.values,
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 5: Recommendations
    with tab5:
        st.subheader("🎯 Career Path Recommendations")
        
        st.write("#### Find Your Career Path")
        
        col1, col2 = st.columns(2)
        
        with col1:
            target_role = st.selectbox(
                "Target Job Role",
                sorted(df['job_group'].unique())
            )
        
        with col2:
            target_level = st.selectbox(
                "Target Experience Level",
                ['fresher', 'junior', 'mid', 'senior', 'lead']
            )
        
        if st.button("Get Recommendations", type="primary"):
            # Filter by role and level
            role_df = df[
                (df['job_group'] == target_role) & 
                (df['level'] == target_level)
            ]
            
            if len(role_df) > 0:
                st.success(f"Found {len(role_df)} {target_level} {target_role} positions")
                
                # Top skills for this role
                role_skills = []
                for idx, row in role_df.iterrows():
                    skills = parse_list_field(row.get('array_skills', []))
                    role_skills.extend([s.lower() for s in skills if s])
                
                skill_freq = Counter(role_skills)
                top_skills = skill_freq.most_common(10)
                
                st.write("#### Most Important Skills")
                for i, (skill, count) in enumerate(top_skills, 1):
                    pct = count / len(role_df) * 100
                    st.write(f"{i}. **{skill.title()}** - {count} jobs ({pct:.1f}%)")
                
                # Salary expectations
                role_with_salary = role_df[role_df['salary_numeric'].notna()]
                if len(role_with_salary) > 0:
                    avg_salary = role_with_salary['salary_numeric'].mean() / 1_000_000
                    med_salary = role_with_salary['salary_numeric'].median() / 1_000_000
                    min_salary = role_with_salary['salary_numeric'].min() / 1_000_000
                    max_salary = role_with_salary['salary_numeric'].max() / 1_000_000
                    
                    st.write("#### Expected Salary Range")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Minimum", f"{min_salary:.2f}M VND")
                    col2.metric("Average", f"{avg_salary:.2f}M VND")
                    col3.metric("Maximum", f"{max_salary:.2f}M VND")
                
                # Top companies hiring
                st.write("#### Top Companies Hiring")
                top_companies = role_df['company_names'].value_counts().head(5)
                for company, count in top_companies.items():
                    st.write(f"• {company}: {count} positions")
            else:
                st.warning(f"No {target_level} {target_role} positions found")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>Vietnam IT Job Market Analytics Dashboard</p>
        <p>Data source: ITviec | Last updated: February 2026</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
