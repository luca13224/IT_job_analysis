"""
AI Chatbot Assistant - Interactive Q&A about job market
Answer questions about jobs, salaries, skills, and career advice
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime


def show_chatbot(df):
    """AI Chatbot assistant page"""
    
    st.markdown('<h2 class="sub-header">🤖 Trợ lý AI</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        💡 <strong>Hỏi đáp thông minh:</strong> Đặt câu hỏi về thị trường việc làm IT,
        lương bổng, kỹ năng cần thiết, và lộ trình phát triển sự nghiệp.
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": "Xin chào! Tôi là trợ lý AI phân tích thị trường việc làm IT. Bạn có thể hỏi tôi về:\n\n"
                          "- 💰 Mức lương của các vị trí\n"
                          "- 🎯 Kỹ năng cần thiết cho công việc\n"
                          "- 📊 Xu hướng tuyển dụng\n"
                          "- 🚀 Lộ trình phát triển sự nghiệp\n"
                          "- 🏢 So sánh công ty, thành phố\n\n"
                          "Hãy đặt câu hỏi của bạn!"
            }
        ]
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Quick questions
    st.markdown("### ⚡ Câu hỏi nhanh")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💰 Lương Backend Dev?", use_container_width=True):
            handle_quick_question(df, "Lương trung bình của Backend Developer là bao nhiêu?")
    
    with col2:
        if st.button("🎯 Kỹ năng hot nhất?", use_container_width=True):
            handle_quick_question(df, "Những kỹ năng nào đang được yêu cầu nhiều nhất?")
    
    with col3:
        if st.button("📊 HCM vs Hà Nội?", use_container_width=True):
            handle_quick_question(df, "So sánh thị trường IT giữa TP.HCM và Hà Nội?")
    
    # Chat input
    if prompt := st.chat_input("Đặt câu hỏi của bạn..."):
        # Add user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Đang phân tích..."):
                response = generate_response(df, prompt)
                st.markdown(response)
        
        # Add assistant message
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })
        
        st.rerun()


def handle_quick_question(df, question):
    """Handle quick question button clicks"""
    st.session_state.chat_history.append({
        "role": "user",
        "content": question
    })
    
    response = generate_response(df, question)
    
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response
    })
    
    st.rerun()


def generate_response(df, question):
    """Generate AI response based on question"""
    
    question_lower = question.lower()
    
    # Salary questions
    if any(word in question_lower for word in ['lương', 'salary', 'tiền', 'thu nhập']):
        return generate_salary_response(df, question_lower)
    
    # Skills questions
    elif any(word in question_lower for word in ['kỹ năng', 'skill', 'học', 'công nghệ']):
        return generate_skills_response(df, question_lower)
    
    # Job market questions
    elif any(word in question_lower for word in ['thị trường', 'xu hướng', 'tuyển dụng', 'cơ hội']):
        return generate_market_response(df, question_lower)
    
    # Comparison questions
    elif any(word in question_lower for word in ['so sánh', 'compare', 'vs', 'hay', 'hơn']):
        return generate_comparison_response(df, question_lower)
    
    # Career path questions
    elif any(word in question_lower for word in ['lộ trình', 'career', 'phát triển', 'fresher', 'junior']):
        return generate_career_response(df, question_lower)
    
    # Company questions
    elif any(word in question_lower for word in ['công ty', 'company', 'firm', 'doanh nghiệp']):
        return generate_company_response(df, question_lower)
    
    # Default response
    else:
        return generate_general_response(df)


def generate_salary_response(df, question):
    """Generate response about salary"""
    
    response = []
    response.append("## 💰 Phân tích lương\n")
    
    # Detect job type
    job_keywords = {
        'backend': 'Backend Developer',
        'frontend': 'Frontend Developer',
        'fullstack': 'Fullstack Developer',
        'data': 'Data / AI',
        'mobile': 'Mobile Developer',
        'devops': 'DevOps / Cloud'
    }
    
    detected_job = None
    for keyword, job_name in job_keywords.items():
        if keyword in question:
            detected_job = job_name
            break
    
    if detected_job:
        job_data = df[df['job_group'] == detected_job]
        salary_data = job_data[job_data['salary_numeric'].notna()]['salary_numeric']
        
        if len(salary_data) > 0:
            response.append(f"**{detected_job}:**\n")
            response.append(f"- Lương trung bình: **{salary_data.mean()/1_000_000:.1f}M VND**")
            response.append(f"- Lương trung vị: **{salary_data.median()/1_000_000:.1f}M VND**")
            response.append(f"- Khoảng lương: {salary_data.quantile(0.25)/1_000_000:.1f}M - {salary_data.quantile(0.75)/1_000_000:.1f}M")
            response.append(f"- Số mẫu: {len(salary_data):,} tin tuyển\n")
            
            # By level
            response.append("**Theo cấp độ:**")
            for level in ['fresher', 'junior', 'mid', 'senior']:
                level_salary = job_data[
                    (job_data['level'] == level) & 
                    (job_data['salary_numeric'].notna())
                ]['salary_numeric']
                
                if len(level_salary) > 0:
                    response.append(f"- {level.capitalize()}: {level_salary.mean()/1_000_000:.1f}M VND")
        else:
            response.append(f"Không có đủ dữ liệu lương cho {detected_job}")
    else:
        # General salary overview
        salary_data = df[df['salary_numeric'].notna()]['salary_numeric']
        response.append(f"**Tổng quan thị trường:**\n")
        response.append(f"- Lương trung bình: **{salary_data.mean()/1_000_000:.1f}M VND**")
        response.append(f"- Lương trung vị: **{salary_data.median()/1_000_000:.1f}M VND**")
        response.append(f"- Khoảng lương: {salary_data.min()/1_000_000:.1f}M - {salary_data.max()/1_000_000:.1f}M\n")
        
        response.append("**Top 5 nghề lương cao:**")
        salary_by_group = df[df['salary_numeric'].notna()].groupby('job_group')['salary_numeric'].mean().sort_values(ascending=False)
        for i, (job, salary) in enumerate(salary_by_group.head(5).items(), 1):
            response.append(f"{i}. {job}: {salary/1_000_000:.1f}M VND")
    
    return "\n".join(response)


def generate_skills_response(df, question):
    """Generate response about skills"""
    import ast
    from collections import Counter
    
    response = []
    response.append("## 🎯 Phân tích kỹ năng\n")
    
    # Extract all skills
    all_skills = []
    for _, row in df.iterrows():
        try:
            skills = ast.literal_eval(str(row.get('array_skills', '[]')))
            if isinstance(skills, list):
                all_skills.extend([s.lower() for s in skills if s])
        except:
            pass
    
    skill_counts = Counter(all_skills)
    
    response.append("**Top 15 kỹ năng được yêu cầu nhiều nhất:**\n")
    for i, (skill, count) in enumerate(skill_counts.most_common(15), 1):
        pct = (count / len(df)) * 100
        response.append(f"{i}. **{skill.capitalize()}** - {count:,} tin ({pct:.1f}%)")
    
    response.append("\n**💡 Khuyến nghị:**")
    response.append("- Học các kỹ năng phổ biến để tăng cơ hội xin việc")
    response.append("- Kết hợp nhiều kỹ năng để trở thành Fullstack")
    response.append("- Cập nhật công nghệ mới thường xuyên")
    
    return "\n".join(response)


def generate_market_response(df, question):
    """Generate response about job market"""
    
    response = []
    response.append("## 📊 Phân tích thị trường\n")
    
    response.append(f"**Tổng quan:**")
    response.append(f"- Tổng tin tuyển: **{len(df):,}**")
    response.append(f"- Số công ty tuyển: **{df['company_names'].nunique():,}**")
    response.append(f"- Thành phố: **{df['city'].nunique()}**\n")
    
    response.append("**Top 5 nghề nghiệp hot nhất:**")
    job_counts = df['job_group'].value_counts()
    for i, (job, count) in enumerate(job_counts.head(5).items(), 1):
        pct = (count / len(df)) * 100
        response.append(f"{i}. {job}: {count:,} tin ({pct:.1f}%)")
    
    response.append("\n**Phân bố theo cấp độ:**")
    level_counts = df['level'].value_counts()
    for level, count in level_counts.items():
        pct = (count / len(df)) * 100
        response.append(f"- {level.capitalize()}: {count:,} ({pct:.1f}%)")
    
    response.append("\n**💡 Xu hướng:**")
    response.append("- Backend và Frontend vẫn là 2 nghề được tuyển nhiều nhất")
    response.append("- Nhu cầu Middle/Senior cao hơn Fresher")
    response.append("- TP.HCM và Hà Nội chiếm > 80% thị trường")
    
    return "\n".join(response)


def generate_comparison_response(df, question):
    """Generate comparison response"""
    
    response = []
    response.append("## ⚖️ So sánh\n")
    
    if 'hcm' in question or 'hồ chí minh' in question or 'sài gòn' in question:
        # Compare cities
        hcm_data = df[df['city'].str.contains('Hồ Chí Minh', case=False, na=False)]
        hn_data = df[df['city'].str.contains('Hà Nội', case=False, na=False)]
        
        response.append("**TP.HCM vs Hà Nội:**\n")
        response.append(f"- **Số tin tuyển:** HCM {len(hcm_data):,} vs HN {len(hn_data):,}")
        
        hcm_salary = hcm_data[hcm_data['salary_numeric'].notna()]['salary_numeric'].mean()
        hn_salary = hn_data[hn_data['salary_numeric'].notna()]['salary_numeric'].mean()
        response.append(f"- **Lương TB:** HCM {hcm_salary/1_000_000:.1f}M vs HN {hn_salary/1_000_000:.1f}M")
        response.append(f"- **Công ty:** HCM {hcm_data['company_names'].nunique():,} vs HN {hn_data['company_names'].nunique():,}")
    
    elif 'backend' in question and 'frontend' in question:
        # Compare Backend vs Frontend
        be_data = df[df['job_group'] == 'Backend Developer']
        fe_data = df[df['job_group'] == 'Frontend Developer']
        
        response.append("**Backend vs Frontend:**\n")
        response.append(f"- **Số tin:** Backend {len(be_data):,} vs Frontend {len(fe_data):,}")
        
        be_salary = be_data[be_data['salary_numeric'].notna()]['salary_numeric'].mean()
        fe_salary = fe_data[fe_data['salary_numeric'].notna()]['salary_numeric'].mean()
        response.append(f"- **Lương TB:** Backend {be_salary/1_000_000:.1f}M vs Frontend {fe_salary/1_000_000:.1f}M")
    
    else:
        response.append("Vui lòng chỉ rõ bạn muốn so sánh gì? (VD: Backend vs Frontend, HCM vs Hà Nội)")
    
    return "\n".join(response)


def generate_career_response(df, question):
    """Generate career path response"""
    
    response = []
    response.append("## 🚀 Lộ trình phát triển\n")
    
    if 'fresher' in question:
        response.append("**Lộ trình từ Fresher:**\n")
        response.append("**Năm 1-2 (Fresher → Junior):**")
        response.append("- Học các kỹ năng nền tảng: Git, coding conventions")
        response.append("- Làm việc với framework chính của công ty")
        response.append("- Lương: 8-15M VND\n")
        
        response.append("**Năm 2-3 (Junior → Middle):**")
        response.append("- Độc lập xử lý tasks, review code")
        response.append("- Học database, caching, testing")
        response.append("- Lương: 15-25M VND\n")
        
        response.append("**Năm 4-5 (Middle → Senior):**")
        response.append("- Lead projects, mentor juniors")
        response.append("- System design, architecture")
        response.append("- Lương: 25-40M VND")
    
    else:
        response.append("**Các cấp độ phổ biến:**\n")
        for level in ['fresher', 'junior', 'mid', 'senior']:
            level_data = df[df['level'] == level]
            salary = level_data[level_data['salary_numeric'].notna()]['salary_numeric'].mean()
            
            response.append(f"**{level.capitalize()}:**")
            response.append(f"- Số tin: {len(level_data):,}")
            if not pd.isna(salary):
                response.append(f"- Lương TB: {salary/1_000_000:.1f}M VND")
            response.append("")
    
    return "\n".join(response)


def generate_company_response(df, question):
    """Generate company response"""
    
    response = []
    response.append("## 🏢 Phân tích công ty\n")
    
    response.append("**Top 10 công ty tuyển nhiều nhất:**\n")
    top_companies = df['company_names'].value_counts().head(10)
    
    for i, (company, count) in enumerate(top_companies.items(), 1):
        response.append(f"{i}. **{company}** - {count} tin tuyển")
    
    return "\n".join(response)


def generate_general_response(df):
    """Generate general response"""
    
    return """## 👋 Xin chào!

Tôi có thể giúp bạn về:

**💰 Lương:**
- "Lương Backend Developer là bao nhiêu?"
- "Fresher thường được trả bao nhiêu?"

**🎯 Kỹ năng:**
- "Kỹ năng nào đang hot?"
- "Nên học gì để trở thành Frontend?"

**📊 Thị trường:**
- "Nghề nào đang được tuyển nhiều?"
- "Thị trường IT hiện tại thế nào?"

**⚖️ So sánh:**
- "HCM vs Hà Nội?"
- "Backend hay Frontend?"

Hãy đặt câu hỏi cụ thể nhé! 😊"""
