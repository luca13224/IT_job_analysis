"""
Demo Scenarios - Pre-configured use cases for presentation
Các kịch bản demo có sẵn để trình bày
"""
import streamlit as st
import pandas as pd
from datetime import datetime


def show_demo_scenarios(df, recommender):
    """Display demo scenarios page"""
    
    st.markdown('<h2 class="sub-header">🎬 Kịch bản Demo</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        💡 <strong>Hướng dẫn:</strong> Chọn kịch bản bên dưới để demo nhanh các tính năng chính của hệ thống
    </div>
    """, unsafe_allow_html=True)
    
    # Scenario selector
    scenario = st.selectbox(
        "🎯 Chọn kịch bản demo",
        [
            "1. Sinh viên mới tốt nghiệp tìm việc",
            "2. Developer 2 năm kinh nghiệm muốn chuyển việc",
            "3. HR phân tích mức lương thị trường",
            "4. Nhà tuyển dụng tìm kỹ năng hot",
            "5. Người học lập trình chọn hướng đi"
        ]
    )
    
    st.markdown("---")
    
    if "1. Sinh viên" in scenario:
        demo_fresh_graduate(df, recommender)
    elif "2. Developer" in scenario:
        demo_experienced_dev(df, recommender)
    elif "3. HR" in scenario:
        demo_hr_analysis(df)
    elif "4. Nhà tuyển dụng" in scenario:
        demo_recruiter(df)
    elif "5. Người học" in scenario:
        demo_learner(df)


def demo_fresh_graduate(df, recommender):
    """Demo: Fresh graduate looking for first job"""
    
    st.markdown("### 🎓 Kịch bản: Sinh viên mới tốt nghiệp")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Hồ sơ:**
        - 👤 Tên: Nguyễn Văn A
        - 🎓 Vừa tốt nghiệp Công nghệ thông tin
        - 💼 Chưa có kinh nghiệm làm việc
        - 🎯 Mục tiêu: Tìm vị trí Junior/Fresher
        - 📍 Khu vực: Hồ Chí Minh
        """)
        
        st.markdown("**Kỹ năng đã học:**")
        skills = ['python', 'java', 'sql', 'git', 'html', 'css']
        st.write(", ".join(skills))
    
    with col2:
        st.metric("Mức lương mong đợi", "8-12M VND")
        st.metric("Vị trí phù hợp", f"{len(df[df['level']=='fresher'])}")
    
    st.markdown("---")
    st.markdown("#### 🔍 Kết quả gợi ý:")
    
    if recommender:
        recommendations = recommender.recommend_by_skills(
            user_skills=skills,
            level='fresher',
            city='Hồ Chí Minh',
            top_n=5
        )
        
        for idx, (_, job) in enumerate(recommendations.iterrows(), 1):
            with st.expander(f"#{idx} - {job['job_titles']}", expanded=(idx==1)):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"🏢 **Công ty:** {job['company_names']}")
                with col2:
                    st.write(f"📍 **Địa điểm:** {job['city']}")
                with col3:
                    match = job.get('similarity', 0) * 100
                    st.write(f"🎯 **Độ phù hợp:** {match:.0f}%")
                
                if pd.notna(job.get('salary_numeric')):
                    st.write(f"💰 **Lương:** {job['salary_numeric']/1_000_000:.1f}M VND")
    
    st.markdown("---")
    st.info("💡 **Insight:** Fresher nên tập trung vào các công ty có văn hóa đào tạo tốt và cơ hội thăng tiến rõ ràng")


def demo_experienced_dev(df, recommender):
    """Demo: Experienced developer changing job"""
    
    st.markdown("### 💼 Kịch bản: Developer có kinh nghiệm")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Hồ sơ:**
        - 👤 Tên: Trần Thị B
        - 💼 2 năm kinh nghiệm Backend Developer
        - 🎯 Mục tiêu: Tìm vị trí Mid-level, lương cao hơn
        - 📍 Khu vực: Hà Nội hoặc remote
        - 💰 Lương hiện tại: 18M, mong muốn: 25M+
        """)
        
        st.markdown("**Kỹ năng hiện tại:**")
        skills = ['python', 'django', 'postgresql', 'redis', 'docker', 'aws']
        st.write(", ".join(skills))
    
    with col2:
        st.metric("Lương TB thị trường", "25M VND")
        st.metric("Số việc phù hợp", f"{len(df[(df['level']=='mid') & (df['salary_numeric']>=25_000_000)])}")
    
    st.markdown("---")
    st.markdown("#### 📊 So sánh lương:")
    
    # Salary comparison
    salary_data = df[(df['job_group']=='Backend Developer') & (df['level']=='mid') & (df['salary_numeric'].notna())]
    
    if len(salary_data) > 0:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Min", f"{salary_data['salary_numeric'].min()/1_000_000:.0f}M")
        with col2:
            st.metric("Trung bình", f"{salary_data['salary_numeric'].mean()/1_000_000:.0f}M")
        with col3:
            st.metric("Trung vị", f"{salary_data['salary_numeric'].median()/1_000_000:.0f}M")
        with col4:
            st.metric("Max", f"{salary_data['salary_numeric'].max()/1_000_000:.0f}M")
    
    st.markdown("---")
    st.success("✅ **Kết luận:** Với kỹ năng hiện tại, mức lương 25-30M là hợp lý cho vị trí Mid-level")


def demo_hr_analysis(df):
    """Demo: HR analyzing market salary"""
    
    st.markdown("### 📊 Kịch bản: HR phân tích thị trường")
    
    st.markdown("""
    **Tình huống:**
    - 🏢 Công ty đang tuyển Backend Developer (Mid-level)
    - 🎯 Cần xác định mức lương cạnh tranh
    - 📍 Vị trí: Hồ Chí Minh
    - ❓ Câu hỏi: Nên trả bao nhiêu để cạnh tranh?
    """)
    
    st.markdown("---")
    st.markdown("#### 📈 Phân tích thị trường:")
    
    # Filter data
    target_jobs = df[
        (df['job_group'] == 'Backend Developer') & 
        (df['level'] == 'mid') & 
        (df['city'] == 'Hồ Chí Minh') &
        (df['salary_numeric'].notna())
    ]
    
    if len(target_jobs) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**💰 Mức lương thống kê:**")
            stats = {
                "Thấp nhất": f"{target_jobs['salary_numeric'].min()/1_000_000:.1f}M",
                "25% percentile": f"{target_jobs['salary_numeric'].quantile(0.25)/1_000_000:.1f}M",
                "Trung vị": f"{target_jobs['salary_numeric'].median()/1_000_000:.1f}M",
                "75% percentile": f"{target_jobs['salary_numeric'].quantile(0.75)/1_000_000:.1f}M",
                "Cao nhất": f"{target_jobs['salary_numeric'].max()/1_000_000:.1f}M",
                "Trung bình": f"{target_jobs['salary_numeric'].mean()/1_000_000:.1f}M"
            }
            for k, v in stats.items():
                st.write(f"- **{k}:** {v}")
        
        with col2:
            st.markdown("**🎯 Đề xuất:**")
            median_sal = target_jobs['salary_numeric'].median() / 1_000_000
            
            st.info(f"**Mức cạnh tranh:** {median_sal:.0f}M - {median_sal*1.2:.0f}M VND")
            st.write(f"""
            - **Mức thấp (50%):** {median_sal*0.9:.0f}M - có thể khó tuyển
            - **Mức trung bình (60-70%):** {median_sal:.0f}M - {median_sal*1.1:.0f}M - cạnh tranh vừa
            - **Mức cao (80%+):** {median_sal*1.2:.0f}M+ - thu hút ứng viên tốt
            """)
    
    st.markdown("---")
    st.warning("⚠️ **Lưu ý:** Ngoài lương còn cần xem xét benefits, văn hóa công ty, cơ hội phát triển")


def demo_recruiter(df):
    """Demo: Recruiter finding trending skills"""
    
    st.markdown("### 🔍 Kịch bản: Tìm kỹ năng hot")
    
    st.markdown("""
    **Tình huống:**
    - 👔 Nhà tuyển dụng muốn biết kỹ năng nào đang được tuyển nhiều
    - 🎯 Để điều chỉnh JD và chiến lược tuyển dụng
    - 📊 Phân tích top 15 kỹ năng được yêu cầu nhiều nhất
    """)
    
    st.markdown("---")
    st.markdown("#### 🏆 Top kỹ năng được yêu cầu:")
    
    # Extract skills
    all_skills = []
    for idx, row in df.iterrows():
        try:
            import ast
            skills = ast.literal_eval(str(row.get('array_skills', '[]')))
            if isinstance(skills, list):
                all_skills.extend([s.lower() for s in skills if s])
        except:
            pass
    
    skill_counts = pd.Series(all_skills).value_counts().head(15)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        import plotly.express as px
        fig = px.bar(
            x=skill_counts.values,
            y=skill_counts.index,
            orientation='h',
            title="Top 15 kỹ năng được tuyển nhiều nhất",
            color=skill_counts.values,
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            xaxis_title="Số lượng tin tuyển",
            yaxis_title="Kỹ năng",
            showlegend=False,
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**📋 Danh sách:**")
        for idx, (skill, count) in enumerate(skill_counts.items(), 1):
            pct = (count / len(df)) * 100
            st.write(f"{idx}. **{skill.capitalize()}** - {count} tin ({pct:.1f}%)")
    
    st.markdown("---")
    st.success("✅ **Insight:** Python, JavaScript, Java là 3 kỹ năng được yêu cầu nhiều nhất. Nên ưu tiên trong JD.")


def demo_learner(df):
    """Demo: Student choosing learning path"""
    
    st.markdown("### 🎓 Kịch bản: Chọn hướng học")
    
    st.markdown("""
    **Tình huống:**
    - 👨‍🎓 Sinh viên năm 2 muốn chọn chuyên ngành
    - 🤔 Đang phân vân giữa: Frontend, Backend, hay Data
    - 📊 Phân tích để chọn hướng đi phù hợp
    """)
    
    st.markdown("---")
    st.markdown("#### 📊 So sánh 3 hướng:")
    
    # Compare paths
    paths = {
        'Frontend Developer': df[df['job_group'] == 'Frontend Developer'],
        'Backend Developer': df[df['job_group'] == 'Backend Developer'],
        'Data / AI': df[df['job_group'] == 'Data / AI']
    }
    
    comparison = []
    for path_name, path_data in paths.items():
        salary_data = path_data[path_data['salary_numeric'].notna()]
        comparison.append({
            'Hướng đi': path_name,
            'Số việc': len(path_data),
            'Lương TB (M)': f"{salary_data['salary_numeric'].mean()/1_000_000:.1f}" if len(salary_data) > 0 else "N/A",
            'Lương Max (M)': f"{salary_data['salary_numeric'].max()/1_000_000:.1f}" if len(salary_data) > 0 else "N/A"
        })
    
    comparison_df = pd.DataFrame(comparison)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("#### 🎯 Kỹ năng cần học:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Frontend:**")
        st.write("- JavaScript")
        st.write("- React/Vue")
        st.write("- HTML/CSS")
        st.write("- TypeScript")
    
    with col2:
        st.markdown("**Backend:**")
        st.write("- Python/Java")
        st.write("- SQL/NoSQL")
        st.write("- Docker")
        st.write("- APIs")
    
    with col3:
        st.markdown("**Data/AI:**")
        st.write("- Python")
        st.write("- Machine Learning")
        st.write("- Pandas/NumPy")
        st.write("- TensorFlow")
    
    st.markdown("---")
    st.info("💡 **Gợi ý:** Nếu thích UI/UX → Frontend. Thích logic/hệ thống → Backend. Thích toán/phân tích → Data")
