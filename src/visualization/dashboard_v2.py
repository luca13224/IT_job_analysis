"""
Enhanced Interactive Dashboard with Job Recommendations
Improved UI/UX with modern design
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
from src.ml_models.job_recommender import JobRecommender
from src.visualization.demo_scenarios import show_demo_scenarios
from src.visualization.career_simulator import show_career_simulator
from src.visualization.compare_tool import show_compare_tool
from src.visualization.export_tools import show_export_tools
from src.visualization.chatbot import show_chatbot


# Page config
st.set_page_config(
    page_title="Phân tích thị trường việc làm IT Việt Nam",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
<style>
    /* Main theme */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem 0;
    }
    
    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #667eea;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Job cards */
    .job-card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        transition: transform 0.2s;
    }
    
    .job-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .job-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .job-company {
        font-size: 1.1rem;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .job-details {
        color: #718096;
        font-size: 0.95rem;
    }
    
    .skill-tag {
        display: inline-block;
        background: #e6f0ff;
        color: #667eea;
        padding: 0.3rem 0.8rem;
        border-radius: 1rem;
        margin: 0.2rem;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Info boxes */
    .info-box {
        background: #e6f0ff;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=1)  # Cache 1 giây - force reload
def load_data():
    """Load and cache data"""
    try:
        df = pd.read_csv(CLEAN_CSV_PATH)
        
        # Normalize city names (chuẩn hóa tên thành phố)
        city_mapping = {
            'Hà Nội': 'Ha Noi',
            'Hồ Chí Minh': 'Ho Chi Minh',
            'Đà Nẵng': 'Da Nang',
            'Cần Thơ': 'Can Tho',
            'Hải Phòng': 'Hai Phong'
        }
        df['city'] = df['city'].replace(city_mapping)
        
        return df
    except FileNotFoundError:
        st.error(f"❌ Không tìm thấy dữ liệu: {CLEAN_CSV_PATH}")
        st.info("💡 File cần: data/processed/clean_data.csv")
        st.info("🔄 Chạy: `python src/crawler/ITViec_AI_demo.py` để tạo data")
        st.stop()
    except Exception as e:
        st.error(f"❌ Lỗi đọc dữ liệu: {e}")
        st.info(f"📁 Path: {CLEAN_CSV_PATH}")
        st.info(f"📊 Exists: {CLEAN_CSV_PATH.exists()}")
        st.stop()


@st.cache_resource
def load_recommender():
    """Load and cache recommender"""
    try:
        recommender = JobRecommender()
        recommender.load_data()
        recommender.build_features()
        return recommender
    except:
        return None


def parse_skills(field):
    """Parse skills field"""
    if pd.isna(field):
        return []
    if isinstance(field, list):
        return field
    try:
        return ast.literal_eval(field)
    except:
        return []


def format_salary(salary):
    """Format salary display"""
    if pd.isna(salary):
        return "💰 Thỏa thuận"
    return f"💰 {salary/1_000_000:.1f}M VND"


def create_metric_card(label, value, icon="📊"):
    """Create a metric card"""
    return f"""
    <div class="metric-card">
        <div class="metric-label">{icon} {label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """


def display_job_card(job, show_match=False):
    """Display a job card"""
    skills = parse_skills(job.get('array_skills', '[]'))
    skills_html = ''.join([f'<span class="skill-tag">{s}</span>' for s in skills[:8]])
    
    match_html = ""
    if show_match and 'similarity' in job:
        match_score = job['similarity'] * 100
        match_html = f'<div style="color: #667eea; font-weight: 600;">🎯 Match: {match_score:.0f}%</div>'
    
    st.markdown(f"""
    <div class="job-card">
        <div class="job-title">💼 {job['job_names']}</div>
        <div class="job-company">🏢 {job['company_names']}</div>
        {match_html}
        <div class="job-details">
            📍 {job['city']} | 
            📊 {job['level']} | 
            🎯 {job['job_group']} | 
            {format_salary(job.get('salary_numeric'))}
        </div>
        <div style="margin-top: 1rem;">
            {skills_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


def main():
    # Header
    st.markdown("""
    <div class="main-header">
        💼 Phân tích thị trường việc làm IT Việt Nam
    </div>
    <p style="text-align: center; color: #718096; font-size: 1.1rem; margin-bottom: 2rem;">
        Khai thác dữ liệu tuyển dụng IT với phân tích thông minh
    </p>
    """, unsafe_allow_html=True)
    
    # Load data
    with st.spinner("🔄 Đang tải dữ liệu..."):
        df = load_data()
        recommender = load_recommender()
    
    # Sidebar
    st.sidebar.image("https://img.icons8.com/fluency/96/analytics.png", width=80)
    st.sidebar.title("🎯 Bộ lọc & Cài đặt")
    
    # Navigation
    page = st.sidebar.radio(
        "📋 Điều hướng",
        ["🏠 Tổng quan", "📊 Phân tích thị trường", "🔍 Gợi ý việc làm", "💰 Phân tích lương", 
         "🎓 Phân tích kỹ năng", "🎬 Kịch bản Demo", "🚀 Mô phỏng lộ trình", "⚖️ Công cụ so sánh", 
         "📥 Xuất báo cáo", "🤖 Trợ lý AI"],
        label_visibility="visible"
    )
    
    # Filters
    with st.sidebar.expander("🔍 Tùy chọn lọc", expanded=True):
        job_groups = ['All'] + sorted(df['job_group'].unique().tolist())
        selected_job_group = st.selectbox("Nhóm nghề", job_groups, key="job_group")
        
        levels = ['All'] + sorted(df['level'].unique().tolist())
        selected_level = st.selectbox("Cấp độ kinh nghiệm", levels, key="level")
        
        cities = ['All'] + sorted(df['city'].unique().tolist())
        selected_city = st.selectbox("Thành phố", cities, key="city")
    
    # Apply filters
    filtered_df = df.copy()
    if selected_job_group != 'All':
        filtered_df = filtered_df[filtered_df['job_group'] == selected_job_group]
    if selected_level != 'All':
        filtered_df = filtered_df[filtered_df['level'] == selected_level]
    if selected_city != 'All':
        filtered_df = filtered_df[filtered_df['city'] == selected_city]
    
    # Page routing
    if page == "🏠 Tổng quan":
        show_overview(df, filtered_df)
    elif page == "📊 Phân tích thị trường":
        show_market_analysis(filtered_df)
    elif page == "🔍 Gợi ý việc làm":
        show_job_recommendations(df, recommender)
    elif page == "💰 Phân tích lương":
        show_salary_insights(filtered_df)
    elif page == "🎓 Phân tích kỹ năng":
        show_skills_analysis(filtered_df)
    elif page == "🎬 Kịch bản Demo":
        show_demo_scenarios(df, recommender)
    elif page == "🚀 Mô phỏng lộ trình":
        show_career_simulator(df)
    elif page == "⚖️ Công cụ so sánh":
        show_compare_tool(df)
    elif page == "📥 Xuất báo cáo":
        show_export_tools(df)
    elif page == "🤖 Trợ lý AI":
        show_chatbot(df)


def show_overview(df, filtered_df):
    """Overview page"""
    st.markdown('<h2 class="sub-header">📊 Tổng quan thị trường</h2>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card("Tổng số việc", f"{len(filtered_df):,}", "💼"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card("Công ty", f"{filtered_df['company_names'].nunique():,}", "🏢"), unsafe_allow_html=True)
    
    with col3:
        avg_salary = filtered_df['salary_numeric'].mean() / 1_000_000
        st.markdown(create_metric_card("Lương TB", f"{avg_salary:.1f}M", "💰"), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_metric_card("Thành phố", f"{filtered_df['city'].nunique()}", "📍"), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Việc theo nhóm nghề")
        job_dist = filtered_df['job_group'].value_counts().head(10)
        fig = px.bar(
            x=job_dist.values, 
            y=job_dist.index,
            orientation='h',
            color=job_dist.values,
            color_continuous_scale='Blues',
            labels={'x': 'Số lượng việc', 'y': 'Nhóm nghề'}
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Cấp độ kinh nghiệm")
        level_dist = filtered_df['level'].value_counts()
        fig = px.pie(
            values=level_dist.values,
            names=level_dist.index,
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Charts row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📍 Phân bố địa lý")
        city_dist = filtered_df['city'].value_counts().head(10)
        fig = px.bar(
            x=city_dist.index,
            y=city_dist.values,
            color=city_dist.values,
            color_continuous_scale='Viridis',
            labels={'x': 'Thành phố', 'y': 'Số lượng việc'}
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 💰 Phân bố lương")
        salary_data = filtered_df[filtered_df['salary_numeric'].notna()]['salary_numeric'] / 1_000_000
        fig = px.histogram(
            salary_data,
            nbins=30,
            labels={'value': 'Lương (triệu VND)', 'count': 'Tần suất'},
            color_discrete_sequence=['#667eea']
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)


def show_market_analysis(filtered_df):
    """Market analysis page"""
    st.markdown('<h2 class="sub-header">📊 Xu hướng & phân tích thị trường</h2>', unsafe_allow_html=True)
    
    # Salary by job group
    st.markdown("### 💰 Lương theo nhóm nghề")
    salary_by_group = filtered_df[filtered_df['salary_numeric'].notna()].groupby('job_group').agg({
        'salary_numeric': ['mean', 'median', 'count']
    }).reset_index()
    salary_by_group.columns = ['Job Group', 'Mean Salary', 'Median Salary', 'Count']
    salary_by_group = salary_by_group[salary_by_group['Count'] >= 5].sort_values('Mean Salary', ascending=False)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=salary_by_group['Job Group'],
        x=salary_by_group['Mean Salary'] / 1_000_000,
        name='Mean',
        orientation='h',
        marker=dict(color='#667eea')
    ))
    fig.add_trace(go.Bar(
        y=salary_by_group['Job Group'],
        x=salary_by_group['Median Salary'] / 1_000_000,
        name='Median',
        orientation='h',
        marker=dict(color='#764ba2')
    ))
    fig.update_layout(
        barmode='group',
        xaxis_title="Lương (triệu VND)",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Salary by level
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Lương theo cấp độ")
        salary_by_level = filtered_df[filtered_df['salary_numeric'].notna()].groupby('level')['salary_numeric'].mean().sort_values(ascending=False)
        fig = px.bar(
            x=salary_by_level.index,
            y=salary_by_level.values / 1_000_000,
            color=salary_by_level.values,
            color_continuous_scale='Blues',
            labels={'x': 'Cấp độ', 'y': 'Lương TB (triệu VND)'}
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🏢 Công ty tuyển nhiều")
        top_companies = filtered_df['company_names'].value_counts().head(10)
        fig = px.bar(
            x=top_companies.values,
            y=top_companies.index,
            orientation='h',
            color=top_companies.values,
            color_continuous_scale='Purples',
            labels={'x': 'Tin tuyển', 'y': 'Công ty'}
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)


def show_job_recommendations(df, recommender):
    """Job recommendations page"""
    st.markdown('<h2 class="sub-header">🔍 Gợi ý việc làm bằng AI</h2>', unsafe_allow_html=True)
    
    if recommender is None:
        st.error("❌ Hệ thống gợi ý chưa sẵn sàng")
        return
    
    st.markdown("""
    <div class="info-box">
        💡 <strong>Cách hoạt động:</strong> Nhập kỹ năng và tiêu chí của bạn, AI sẽ gợi ý 
        các việc phù hợp nhất dựa trên mức độ tương đồng kỹ năng.
    </div>
    """, unsafe_allow_html=True)
    
    # User input
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Skills input
        all_skills = set()
        for idx, row in df.iterrows():
            skills = parse_skills(row.get('array_skills', '[]'))
            all_skills.update([s.lower() for s in skills])
        
        popular_skills = ['python', 'javascript', 'java', 'react', 'nodejs', 'docker', 
                         'kubernetes', 'aws', 'sql', 'mongodb', 'django', 'spring']
        
        user_skills_input = st.multiselect(
            "🎯 Chọn kỹ năng của bạn",
            options=sorted(list(all_skills)),
            default=['python', 'django'] if 'python' in all_skills else [],
            help="Chọn các kỹ năng bạn đang có"
        )
        
        # Or manual input
        manual_skills = st.text_input(
            "Hoặc nhập kỹ năng thủ công (cách nhau bằng dấu phẩy)",
            placeholder="vd: python, django, postgresql, docker"
        )
        
        if manual_skills:
            user_skills = [s.strip().lower() for s in manual_skills.split(',')]
        else:
            user_skills = user_skills_input
    
    with col2:
        st.markdown("### ⚙️ Ưu tiên")
        pref_level = st.selectbox("Cấp độ", ['Any'] + sorted(df['level'].unique().tolist()))
        pref_city = st.selectbox("Thành phố", ['Any'] + sorted(df['city'].unique().tolist()))
        pref_min_salary = st.number_input("Lương tối thiểu (triệu VND)", min_value=0, value=0, step=5)
        num_results = st.slider("Số lượng kết quả", 5, 20, 10)
    
    # Search button
    if st.button("🔍 Tìm việc phù hợp", use_container_width=True):
        if not user_skills:
            st.warning("⚠️ Vui lòng nhập ít nhất 1 kỹ năng")
            return
        
        with st.spinner("🤖 AI đang phân tích việc làm..."):
            # Get recommendations
            recommendations = recommender.recommend_by_skills(
                user_skills=user_skills,
                top_n=num_results,
                level=None if pref_level == 'Any' else pref_level,
                city=None if pref_city == 'Any' else pref_city,
                min_salary=pref_min_salary * 1_000_000 if pref_min_salary > 0 else None
            )
            
            if len(recommendations) == 0:
                st.warning("😕 Không tìm thấy việc phù hợp. Hãy điều chỉnh bộ lọc.")
                return
            
            # Display results
            st.markdown(f"""
            <div class="info-box">
                ✅ Tìm thấy <strong>{len(recommendations)}</strong> việc phù hợp với hồ sơ của bạn
            </div>
            """, unsafe_allow_html=True)
            
            # Show skills summary
            st.markdown(f"**Kỹ năng của bạn:** {', '.join(user_skills)}")
            
            # Display jobs
            for idx, (_, job) in enumerate(recommendations.iterrows(), 1):
                display_job_card(job, show_match=True)


def show_salary_insights(filtered_df):
    """Salary insights page"""
    st.markdown('<h2 class="sub-header">💰 Phân tích lương & ước tính</h2>', unsafe_allow_html=True)
    
    # Salary calculator
    st.markdown("### 🧮 Ước tính lương")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        calc_job_group = st.selectbox("Nhóm nghề", filtered_df['job_group'].unique())
    with col2:
        calc_level = st.selectbox("Cấp độ", filtered_df['level'].unique())
    with col3:
        calc_city = st.selectbox("Thành phố", filtered_df['city'].unique())
    
    # Calculate salary range
    calc_df = filtered_df[
        (filtered_df['job_group'] == calc_job_group) &
        (filtered_df['level'] == calc_level) &
        (filtered_df['city'] == calc_city) &
        (filtered_df['salary_numeric'].notna())
    ]
    
    if len(calc_df) > 0:
        min_sal = calc_df['salary_numeric'].min() / 1_000_000
        max_sal = calc_df['salary_numeric'].max() / 1_000_000
        avg_sal = calc_df['salary_numeric'].mean() / 1_000_000
        median_sal = calc_df['salary_numeric'].median() / 1_000_000
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📉 Thấp nhất", f"{min_sal:.1f}M")
        with col2:
            st.metric("📊 Trung bình", f"{avg_sal:.1f}M")
        with col3:
            st.metric("📈 Trung vị", f"{median_sal:.1f}M")
        with col4:
            st.metric("🚀 Cao nhất", f"{max_sal:.1f}M")
        
        # Salary range visualization
        fig = go.Figure()
        fig.add_trace(go.Box(
            y=calc_df['salary_numeric'] / 1_000_000,
            name='Salary Range',
            marker_color='#667eea',
            boxmean='sd'
        ))
        fig.update_layout(
            yaxis_title="Lương (triệu VND)",
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📊 Chưa có dữ liệu lương cho lựa chọn này")
    
    # Salary trends
    st.markdown("---")
    st.markdown("### 📈 Xu hướng lương theo nhóm")
    
    tab1, tab2, tab3 = st.tabs(["Theo nhóm nghề", "Theo cấp độ", "Theo thành phố"])
    
    with tab1:
        salary_by_group = filtered_df[filtered_df['salary_numeric'].notna()].groupby('job_group')['salary_numeric'].agg(['mean', 'median', 'count'])
        salary_by_group = salary_by_group[salary_by_group['count'] >= 3].sort_values('mean', ascending=False)
        
        fig = px.bar(
            salary_by_group,
            y=salary_by_group.index,
            x='mean',
            orientation='h',
            color='mean',
            color_continuous_scale='Blues',
            labels={'mean': 'Lương TB (VND)', 'index': 'Nhóm nghề'}
        )
        fig.update_traces(x=salary_by_group['mean'] / 1_000_000)
        fig.update_layout(xaxis_title="Lương TB (triệu VND)", height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        salary_by_level = filtered_df[filtered_df['salary_numeric'].notna()].groupby('level')['salary_numeric'].mean()
        fig = px.bar(
            x=salary_by_level.index,
            y=salary_by_level.values / 1_000_000,
            color=salary_by_level.values,
            color_continuous_scale='Purples',
            labels={'x': 'Cấp độ', 'y': 'Lương TB (triệu VND)'}
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        salary_by_city = filtered_df[filtered_df['salary_numeric'].notna()].groupby('city')['salary_numeric'].mean().sort_values(ascending=False)
        fig = px.bar(
            x=salary_by_city.index,
            y=salary_by_city.values / 1_000_000,
            color=salary_by_city.values,
            color_continuous_scale='Greens',
            labels={'x': 'Thành phố', 'y': 'Lương TB (triệu VND)'}
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)


def show_skills_analysis(filtered_df):
    """Skills analysis page"""
    st.markdown('<h2 class="sub-header">🎓 Phân tích kỹ năng</h2>', unsafe_allow_html=True)
    
    # Extract all skills
    all_skills = []
    for idx, row in filtered_df.iterrows():
        skills = parse_skills(row.get('array_skills', '[]'))
        all_skills.extend([s.lower() for s in skills])
    
    skill_counts = pd.Series(all_skills).value_counts()
    
    # Top skills
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Kỹ năng được tuyển nhiều")
        top_20 = skill_counts.head(20)
        fig = px.bar(
            x=top_20.values,
            y=top_20.index,
            orientation='h',
            color=top_20.values,
            color_continuous_scale='Blues',
            labels={'x': 'Tin tuyển', 'y': 'Kỹ năng'}
        )
        fig.update_layout(showlegend=False, height=600)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Nhóm kỹ năng")
        
        # Categorize skills (simplified)
        categories = {
            'Ngôn ngữ lập trình': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'swift'],
            'Framework': ['react', 'angular', 'vue', 'django', 'spring', 'nodejs', 'laravel', 'flutter'],
            'Cơ sở dữ liệu': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'elasticsearch'],
            'Cloud & DevOps': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform', 'ansible'],
            'Data & AI': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'data analysis', 'pandas', 'numpy']
        }
        
        category_counts = {}
        for category, keywords in categories.items():
            count = sum(skill_counts.get(skill, 0) for skill in keywords if skill in skill_counts)
            category_counts[category] = count
        
        fig = px.pie(
            values=list(category_counts.values()),
            names=list(category_counts.keys()),
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Trending skills
        st.markdown("### 🔥 Kỹ năng nổi bật")
        trending = skill_counts.head(15)
        for skill, count in trending.items():
            percentage = (count / len(filtered_df)) * 100
            st.markdown(f"""
            <div style="margin: 0.5rem 0;">
                <strong>{skill.capitalize()}</strong><br>
                <div style="background: #e6f0ff; border-radius: 1rem; height: 8px; margin-top: 0.3rem;">
                    <div style="background: linear-gradient(90deg, #667eea, #764ba2); width: {min(percentage*2, 100)}%; height: 100%; border-radius: 1rem;"></div>
                </div>
                <small style="color: #718096;">{count} jobs ({percentage:.1f}%)</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Skill combinations
    st.markdown("---")
    st.markdown("### 🔗 Tổ hợp kỹ năng phổ biến")
    
    st.info("💡 Các kỹ năng thường xuất hiện cùng nhau trong tin tuyển dụng")
    
    # Find common pairs (simplified)
    from itertools import combinations
    pairs = []
    for idx, row in filtered_df.head(200).iterrows():
        skills = parse_skills(row.get('array_skills', '[]'))
        skills_lower = [s.lower() for s in skills]
        for pair in combinations(skills_lower, 2):
            pairs.append(tuple(sorted(pair)))
    
    pair_counts = pd.Series(pairs).value_counts().head(15)
    
    pair_df = pd.DataFrame([
        {'Kỹ năng 1': pair[0].capitalize(), 'Kỹ năng 2': pair[1].capitalize(), 'Số lượng': count}
        for pair, count in pair_counts.items()
    ])
    
    st.dataframe(pair_df, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
