"""
Compare Tool - So sánh vị trí, thành phố, công ty
Side-by-side comparison for jobs, cities, companies
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def show_compare_tool(df):
    """Comparison tool page"""
    
    st.markdown('<h2 class="sub-header">⚖️ Công cụ so sánh</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        💡 <strong>So sánh chi tiết:</strong> Đưa ra quyết định sáng suốt bằng cách so sánh 
        các vị trí, thành phố hoặc công ty trực tiếp.
    </div>
    """, unsafe_allow_html=True)
    
    # Compare type selector
    compare_type = st.radio(
        "Chọn loại so sánh:",
        ["🎯 Vị trí công việc", "📍 Thành phố", "🏢 Công ty"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if compare_type == "🎯 Vị trí công việc":
        compare_jobs(df)
    elif compare_type == "📍 Thành phố":
        compare_cities(df)
    else:
        compare_companies(df)


def compare_jobs(df):
    """Compare two job positions"""
    
    st.markdown("### So sánh 2 vị trí")
    
    job_groups = sorted(df['job_group'].unique().tolist())
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Vị trí 1**")
        job1 = st.selectbox("Chọn vị trí", job_groups, key='job1')
        level1 = st.selectbox("Cấp độ", sorted(df['level'].unique()), key='level1')
    
    with col2:
        st.markdown("**Vị trí 2**")
        job2 = st.selectbox("Chọn vị trí", job_groups, key='job2', 
                           index=min(1, len(job_groups)-1))
        level2 = st.selectbox("Cấp độ", sorted(df['level'].unique()), key='level2')
    
    if st.button("🔍 So sánh ngay", use_container_width=True):
        # Filter data
        data1 = df[(df['job_group'] == job1) & (df['level'] == level1)]
        data2 = df[(df['job_group'] == job2) & (df['level'] == level2)]
        
        st.markdown("---")
        
        # Metrics comparison
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📊 Số lượng việc")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric(job1, len(data1))
            with col_b:
                st.metric(job2, len(data2))
        
        with col2:
            st.markdown("### 💰 Lương trung bình")
            salary1 = data1[data1['salary_numeric'].notna()]['salary_numeric'].mean()
            salary2 = data2[data2['salary_numeric'].notna()]['salary_numeric'].mean()
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric(job1, f"{salary1/1_000_000:.1f}M" if not pd.isna(salary1) else "N/A")
            with col_b:
                delta = ((salary2 - salary1) / salary1 * 100) if not pd.isna(salary1) and not pd.isna(salary2) else 0
                st.metric(job2, f"{salary2/1_000_000:.1f}M" if not pd.isna(salary2) else "N/A",
                         delta=f"{delta:+.0f}%" if delta != 0 else None)
        
        with col3:
            st.markdown("### 🏢 Số công ty")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric(job1, data1['company_names'].nunique())
            with col_b:
                st.metric(job2, data2['company_names'].nunique())
        
        # Salary distribution comparison
        st.markdown("---")
        st.markdown("### 💰 Phân bố lương")
        
        fig = go.Figure()
        
        salary1_data = data1[data1['salary_numeric'].notna()]['salary_numeric'] / 1_000_000
        salary2_data = data2[data2['salary_numeric'].notna()]['salary_numeric'] / 1_000_000
        
        if len(salary1_data) > 0:
            fig.add_trace(go.Box(y=salary1_data, name=job1, marker_color='#667eea'))
        if len(salary2_data) > 0:
            fig.add_trace(go.Box(y=salary2_data, name=job2, marker_color='#764ba2'))
        
        fig.update_layout(
            yaxis_title="Lương (triệu VND)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Skills comparison
        st.markdown("---")
        st.markdown("### 🎯 So sánh kỹ năng")
        
        skills1 = extract_top_skills(data1, 10)
        skills2 = extract_top_skills(data2, 10)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**{job1}**")
            for skill, count in skills1:
                st.markdown(f"- {skill.capitalize()} ({count})")
        
        with col2:
            st.markdown(f"**{job2}**")
            for skill, count in skills2:
                st.markdown(f"- {skill.capitalize()} ({count})")
        
        # Recommendation
        st.markdown("---")
        st.markdown("### 💡 Kết luận")
        
        if not pd.isna(salary1) and not pd.isna(salary2):
            if salary1 > salary2:
                st.success(f"✅ **{job1}** có mức lương cao hơn {((salary1-salary2)/salary2*100):.0f}%")
            else:
                st.success(f"✅ **{job2}** có mức lương cao hơn {((salary2-salary1)/salary1*100):.0f}%")
        
        if len(data1) > len(data2):
            st.info(f"📊 **{job1}** có nhiều cơ hội việc làm hơn ({len(data1)} vs {len(data2)})")
        else:
            st.info(f"📊 **{job2}** có nhiều cơ hội việc làm hơn ({len(data2)} vs {len(data1)})")


def compare_cities(df):
    """Compare two cities"""
    
    st.markdown("### So sánh 2 thành phố")
    
    cities = sorted(df['city'].unique().tolist())
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Thành phố 1**")
        city1 = st.selectbox("Chọn thành phố", cities, key='city1')
    
    with col2:
        st.markdown("**Thành phố 2**")
        city2 = st.selectbox("Chọn thành phố", cities, key='city2',
                            index=min(1, len(cities)-1))
    
    if st.button("🔍 So sánh ngay", use_container_width=True):
        data1 = df[df['city'] == city1]
        data2 = df[df['city'] == city2]
        
        st.markdown("---")
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Tổng việc làm", f"{len(data1):,}", delta=f"{len(data1)-len(data2):+,}")
        
        with col2:
            salary1 = data1[data1['salary_numeric'].notna()]['salary_numeric'].mean()
            salary2 = data2[data2['salary_numeric'].notna()]['salary_numeric'].mean()
            st.metric(f"Lương TB - {city1}", f"{salary1/1_000_000:.1f}M" if not pd.isna(salary1) else "N/A")
        
        with col3:
            st.metric(f"Lương TB - {city2}", f"{salary2/1_000_000:.1f}M" if not pd.isna(salary2) else "N/A")
        
        with col4:
            companies = data1['company_names'].nunique()
            st.metric("Công ty", companies)
        
        # Job groups comparison
        st.markdown("---")
        st.markdown("### 🎯 Phân bố nghề nghiệp")
        
        job_dist1 = data1['job_group'].value_counts().head(10)
        job_dist2 = data2['job_group'].value_counts().head(10)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name=city1, x=job_dist1.index, y=job_dist1.values, marker_color='#667eea'))
        fig.add_trace(go.Bar(name=city2, x=job_dist2.index, y=job_dist2.values, marker_color='#764ba2'))
        
        fig.update_layout(
            barmode='group',
            xaxis_title="Nghề nghiệp",
            yaxis_title="Số lượng việc",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)


def compare_companies(df):
    """Compare two companies"""
    
    st.markdown("### So sánh 2 công ty")
    
    # Get top companies
    top_companies = df['company_names'].value_counts().head(50).index.tolist()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Công ty 1**")
        company1 = st.selectbox("Chọn công ty", top_companies, key='comp1')
    
    with col2:
        st.markdown("**Công ty 2**")
        company2 = st.selectbox("Chọn công ty", top_companies, key='comp2',
                               index=min(1, len(top_companies)-1))
    
    if st.button("🔍 So sánh ngay", use_container_width=True):
        data1 = df[df['company_names'] == company1]
        data2 = df[df['company_names'] == company2]
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Số việc đang tuyển", len(data1), delta=f"{len(data1)-len(data2):+}")
        
        with col2:
            salary1 = data1[data1['salary_numeric'].notna()]['salary_numeric'].mean()
            st.metric(f"{company1}", f"{salary1/1_000_000:.1f}M" if not pd.isna(salary1) else "N/A")
        
        with col3:
            salary2 = data2[data2['salary_numeric'].notna()]['salary_numeric'].mean()
            st.metric(f"{company2}", f"{salary2/1_000_000:.1f}M" if not pd.isna(salary2) else "N/A")
        
        # Job groups
        st.markdown("---")
        st.markdown("### 🎯 Vị trí đang tuyển")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**{company1}**")
            jobs1 = data1['job_group'].value_counts()
            for job, count in jobs1.items():
                st.markdown(f"- {job}: {count}")
        
        with col2:
            st.markdown(f"**{company2}**")
            jobs2 = data2['job_group'].value_counts()
            for job, count in jobs2.items():
                st.markdown(f"- {job}: {count}")


def extract_top_skills(data, top_n=10):
    """Extract top N skills from job data"""
    import ast
    from collections import Counter
    
    all_skills = []
    for _, row in data.iterrows():
        try:
            skills = ast.literal_eval(str(row.get('array_skills', '[]')))
            if isinstance(skills, list):
                all_skills.extend([s.lower() for s in skills if s])
        except:
            pass
    
    return Counter(all_skills).most_common(top_n)
