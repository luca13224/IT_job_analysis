"""
Career Path Simulator - Mô phỏng lộ trình nghề nghiệp
Simulate career progression from Fresher to Senior
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta


def show_career_simulator(df):
    """Career path simulation page"""
    
    st.markdown('<h2 class="sub-header">🚀 Mô phỏng lộ trình nghề nghiệp</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        💡 <strong>Công cụ này giúp bạn:</strong> Dự đoán lộ trình phát triển nghề nghiệp trong 3-5 năm tới,
        bao gồm cấp độ, lương, và kỹ năng cần học theo từng giai đoạn.
    </div>
    """, unsafe_allow_html=True)
    
    # Input section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        job_group = st.selectbox(
            "🎯 Chọn nghề nghiệp",
            ['Backend Developer', 'Frontend Developer', 'Fullstack Developer', 
             'Data / AI', 'Mobile Developer', 'DevOps / Cloud']
        )
    
    with col2:
        current_level = st.selectbox(
            "📊 Cấp độ hiện tại",
            ['fresher', 'junior', 'mid', 'senior']
        )
    
    with col3:
        years = st.slider("⏱️ Thời gian dự đoán (năm)", 1, 10, 5)
    
    if st.button("🚀 Mô phỏng lộ trình", use_container_width=True):
        simulate_career_path(df, job_group, current_level, years)


def simulate_career_path(df, job_group, current_level, years):
    """Generate and display career path simulation"""
    
    # Define career levels hierarchy
    levels = ['fresher', 'junior', 'mid', 'senior', 'lead', 'manager']
    current_idx = levels.index(current_level)
    
    # Calculate progression
    progression = []
    for year in range(years + 1):
        # Estimate level progression (avg 2-3 years per level)
        level_idx = min(current_idx + (year // 2), len(levels) - 1)
        level = levels[level_idx]
        
        # Get salary data
        salary_data = df[
            (df['job_group'] == job_group) & 
            (df['level'] == level) &
            (df['salary_numeric'].notna())
        ]
        
        if len(salary_data) > 0:
            avg_salary = salary_data['salary_numeric'].mean()
            min_salary = salary_data['salary_numeric'].quantile(0.25)
            max_salary = salary_data['salary_numeric'].quantile(0.75)
        else:
            # Estimate based on previous level
            avg_salary = 15_000_000 * (1.3 ** level_idx)
            min_salary = avg_salary * 0.8
            max_salary = avg_salary * 1.2
        
        progression.append({
            'year': year,
            'level': level,
            'level_display': level.capitalize(),
            'avg_salary': avg_salary,
            'min_salary': min_salary,
            'max_salary': max_salary
        })
    
    # Display timeline
    st.markdown("---")
    st.markdown("### 📈 Lộ trình phát triển")
    
    # Create timeline visualization
    fig = go.Figure()
    
    # Salary range area
    fig.add_trace(go.Scatter(
        x=[p['year'] for p in progression],
        y=[p['max_salary']/1_000_000 for p in progression],
        fill=None,
        mode='lines',
        line=dict(color='rgba(102, 126, 234, 0.2)'),
        showlegend=False,
        name='Max'
    ))
    
    fig.add_trace(go.Scatter(
        x=[p['year'] for p in progression],
        y=[p['min_salary']/1_000_000 for p in progression],
        fill='tonexty',
        mode='lines',
        line=dict(color='rgba(102, 126, 234, 0.2)'),
        fillcolor='rgba(102, 126, 234, 0.2)',
        name='Khoảng lương'
    ))
    
    # Average salary line
    fig.add_trace(go.Scatter(
        x=[p['year'] for p in progression],
        y=[p['avg_salary']/1_000_000 for p in progression],
        mode='lines+markers',
        name='Lương trung bình',
        line=dict(color='#667eea', width=3),
        marker=dict(size=10, color='#667eea')
    ))
    
    fig.update_layout(
        title="Dự đoán lương theo thời gian",
        xaxis_title="Năm",
        yaxis_title="Lương (triệu VND)",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed roadmap
    st.markdown("### 🗓️ Kế hoạch chi tiết")
    
    for i, step in enumerate(progression):
        if i == 0:
            continue  # Skip current year
        
        with st.expander(f"📅 Năm {step['year']} - {step['level_display']}", expanded=(i==1)):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Cấp độ:** {step['level_display']}")
                st.markdown(f"**Lương dự kiến:** {step['avg_salary']/1_000_000:.1f}M VND")
                st.markdown(f"**Khoảng lương:** {step['min_salary']/1_000_000:.1f}M - {step['max_salary']/1_000_000:.1f}M")
                
                # Skills to learn
                skills = get_skills_for_level(job_group, step['level'], df)
                if skills:
                    st.markdown("**🎯 Kỹ năng cần có:**")
                    for skill in skills[:8]:
                        st.markdown(f"- {skill.capitalize()}")
            
            with col2:
                # Progress visualization
                progress = (i / len(progression)) * 100
                st.metric("Tiến độ", f"{progress:.0f}%")
                st.progress(progress / 100)
                
                # Salary increase
                if i > 1:
                    prev_salary = progression[i-1]['avg_salary']
                    increase = ((step['avg_salary'] - prev_salary) / prev_salary) * 100
                    st.metric("Tăng lương", f"+{increase:.0f}%")
    
    # Summary
    st.markdown("---")
    st.markdown("### 📊 Tóm tắt lộ trình")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Thời gian", f"{years} năm")
    
    with col2:
        start_salary = progression[0]['avg_salary'] / 1_000_000
        st.metric("Lương bắt đầu", f"{start_salary:.1f}M")
    
    with col3:
        end_salary = progression[-1]['avg_salary'] / 1_000_000
        st.metric("Lương dự kiến", f"{end_salary:.1f}M")
    
    with col4:
        total_increase = ((progression[-1]['avg_salary'] - progression[0]['avg_salary']) / progression[0]['avg_salary']) * 100
        st.metric("Tổng tăng trưởng", f"+{total_increase:.0f}%")
    
    # Learning path
    st.markdown("---")
    st.markdown("### 📚 Lộ trình học tập")
    
    learning_path = generate_learning_path(job_group, current_level, years)
    
    for phase in learning_path:
        st.markdown(f"**{phase['period']}**")
        cols = st.columns(len(phase['skills']))
        for col, skill in zip(cols, phase['skills']):
            with col:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                     padding: 1rem; border-radius: 0.5rem; text-align: center; color: white;">
                    <strong>{skill}</strong>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("")


def get_skills_for_level(job_group, level, df):
    """Get common skills for a job group and level"""
    import ast
    
    jobs = df[(df['job_group'] == job_group) & (df['level'] == level)]
    
    all_skills = []
    for _, row in jobs.iterrows():
        try:
            skills = ast.literal_eval(str(row.get('array_skills', '[]')))
            if isinstance(skills, list):
                all_skills.extend([s.lower() for s in skills if s])
        except:
            pass
    
    from collections import Counter
    skill_counts = Counter(all_skills)
    return [skill for skill, _ in skill_counts.most_common(10)]


def generate_learning_path(job_group, current_level, years):
    """Generate learning path based on career progression"""
    
    paths = {
        'Backend Developer': [
            {'period': 'Năm 1-2: Nền tảng', 'skills': ['Python/Java', 'SQL', 'Git', 'REST API']},
            {'period': 'Năm 3-4: Nâng cao', 'skills': ['Docker', 'Redis', 'Microservices', 'AWS']},
            {'period': 'Năm 5+: Chuyên sâu', 'skills': ['Kubernetes', 'System Design', 'Team Lead', 'Architecture']}
        ],
        'Frontend Developer': [
            {'period': 'Năm 1-2: Nền tảng', 'skills': ['HTML/CSS', 'JavaScript', 'React/Vue', 'Git']},
            {'period': 'Năm 3-4: Nâng cao', 'skills': ['TypeScript', 'State Management', 'Testing', 'Performance']},
            {'period': 'Năm 5+: Chuyên sâu', 'skills': ['Architecture', 'UI/UX', 'Team Lead', 'Mentoring']}
        ],
        'Data / AI': [
            {'period': 'Năm 1-2: Nền tảng', 'skills': ['Python', 'Pandas', 'SQL', 'Statistics']},
            {'period': 'Năm 3-4: Nâng cao', 'skills': ['Machine Learning', 'Deep Learning', 'TensorFlow', 'Spark']},
            {'period': 'Năm 5+: Chuyên sâu', 'skills': ['MLOps', 'Research', 'Team Lead', 'Product']}
        ]
    }
    
    return paths.get(job_group, paths['Backend Developer'])
