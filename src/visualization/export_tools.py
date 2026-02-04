"""
Export Tools - Export reports to PDF and Excel
Generate downloadable reports and data exports
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import io


def show_export_tools(df):
    """Export tools page"""
    
    st.markdown('<h2 class="sub-header">📥 Xuất báo cáo</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        💡 <strong>Tải về:</strong> Xuất dữ liệu và báo cáo phân tích để sử dụng offline,
        đính kèm vào luận văn, hoặc chia sẻ với đồng nghiệp.
    </div>
    """, unsafe_allow_html=True)
    
    # Export options
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Xuất dữ liệu")
        
        export_type = st.radio(
            "Chọn loại dữ liệu:",
            ["Toàn bộ dữ liệu", "Dữ liệu đã lọc", "Chỉ có lương", "Top 100"],
            key="data_export"
        )
        
        export_format = st.selectbox(
            "Định dạng:",
            ["Excel (.xlsx)", "CSV (.csv)", "JSON (.json)"]
        )
        
        if st.button("📥 Tải dữ liệu", use_container_width=True):
            export_data(df, export_type, export_format)
    
    with col2:
        st.markdown("### 📄 Báo cáo phân tích")
        
        report_type = st.radio(
            "Chọn loại báo cáo:",
            ["Báo cáo tổng quan", "Báo cáo lương", "Báo cáo kỹ năng", "Báo cáo tùy chỉnh"],
            key="report_export"
        )
        
        include_charts = st.checkbox("Bao gồm biểu đồ", value=True)
        
        if st.button("📥 Tạo báo cáo", use_container_width=True):
            generate_report(df, report_type, include_charts)
    
    # Quick stats for export
    st.markdown("---")
    st.markdown("### 📊 Thống kê nhanh")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Tổng tin tuyển", f"{len(df):,}")
    
    with col2:
        st.metric("Có thông tin lương", f"{df['salary_numeric'].notna().sum():,}")
    
    with col3:
        st.metric("Công ty", f"{df['company_names'].nunique():,}")
    
    with col4:
        st.metric("Thành phố", f"{df['city'].nunique()}")


def export_data(df, export_type, export_format):
    """Export data to file"""
    
    # Filter data based on type
    if export_type == "Toàn bộ dữ liệu":
        data = df
    elif export_type == "Dữ liệu đã lọc":
        data = df  # Would use filtered data from session state
    elif export_type == "Chỉ có lương":
        data = df[df['salary_numeric'].notna()]
    else:  # Top 100
        data = df.head(100)
    
    # Create file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if "Excel" in export_format:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            data.to_excel(writer, index=False, sheet_name='Data')
            
            # Add summary sheet
            summary = pd.DataFrame({
                'Metric': ['Total Jobs', 'Jobs with Salary', 'Companies', 'Cities'],
                'Value': [len(data), data['salary_numeric'].notna().sum(), 
                         data['company_names'].nunique(), data['city'].nunique()]
            })
            summary.to_excel(writer, index=False, sheet_name='Summary')
        
        buffer.seek(0)
        
        st.download_button(
            label="📥 Tải Excel",
            data=buffer,
            file_name=f"job_data_{timestamp}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        st.success("✅ File Excel đã sẵn sàng tải về!")
    
    elif "CSV" in export_format:
        csv = data.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 Tải CSV",
            data=csv,
            file_name=f"job_data_{timestamp}.csv",
            mime="text/csv"
        )
        st.success("✅ File CSV đã sẵn sàng tải về!")
    
    else:  # JSON
        json = data.to_json(orient='records', force_ascii=False)
        st.download_button(
            label="📥 Tải JSON",
            data=json,
            file_name=f"job_data_{timestamp}.json",
            mime="application/json"
        )
        st.success("✅ File JSON đã sẵn sàng tải về!")


def generate_report(df, report_type, include_charts):
    """Generate analysis report"""
    
    st.markdown("---")
    st.markdown("### 📄 Nội dung báo cáo")
    
    # Generate report content
    report_content = []
    
    report_content.append("# BÁO CÁO PHÂN TÍCH THỊ TRƯỜNG VIỆC LÀM IT VIỆT NAM")
    report_content.append(f"\nNgày tạo: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    report_content.append(f"\nLoại báo cáo: {report_type}")
    report_content.append("\n---\n")
    
    if report_type == "Báo cáo tổng quan":
        report_content.extend(generate_overview_report(df))
    elif report_type == "Báo cáo lương":
        report_content.extend(generate_salary_report(df))
    elif report_type == "Báo cáo kỹ năng":
        report_content.extend(generate_skills_report(df))
    else:
        report_content.extend(generate_custom_report(df))
    
    # Display report
    report_text = "\n".join(report_content)
    st.markdown(report_text)
    
    # Download button
    st.download_button(
        label="📥 Tải báo cáo (Text)",
        data=report_text.encode('utf-8'),
        file_name=f"report_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain"
    )
    
    st.success("✅ Báo cáo đã được tạo!")


def generate_overview_report(df):
    """Generate overview report content"""
    
    content = []
    content.append("## TỔNG QUAN THỊ TRƯỜNG\n")
    
    content.append(f"**Tổng số tin tuyển:** {len(df):,}")
    content.append(f"**Số công ty:** {df['company_names'].nunique():,}")
    content.append(f"**Số thành phố:** {df['city'].nunique()}")
    content.append(f"**Tin có thông tin lương:** {df['salary_numeric'].notna().sum():,}\n")
    
    content.append("### Phân bố theo nghề nghiệp\n")
    job_dist = df['job_group'].value_counts().head(10)
    for job, count in job_dist.items():
        pct = (count / len(df)) * 100
        content.append(f"- {job}: {count:,} ({pct:.1f}%)")
    
    content.append("\n### Phân bố theo cấp độ\n")
    level_dist = df['level'].value_counts()
    for level, count in level_dist.items():
        pct = (count / len(df)) * 100
        content.append(f"- {level.capitalize()}: {count:,} ({pct:.1f}%)")
    
    content.append("\n### Phân bố theo thành phố\n")
    city_dist = df['city'].value_counts().head(5)
    for city, count in city_dist.items():
        pct = (count / len(df)) * 100
        content.append(f"- {city}: {count:,} ({pct:.1f}%)")
    
    return content


def generate_salary_report(df):
    """Generate salary report content"""
    
    content = []
    content.append("## PHÂN TÍCH LƯƠNG\n")
    
    salary_data = df[df['salary_numeric'].notna()]['salary_numeric']
    
    content.append(f"**Số mẫu:** {len(salary_data):,}")
    content.append(f"**Lương trung bình:** {salary_data.mean()/1_000_000:.1f}M VND")
    content.append(f"**Lương trung vị:** {salary_data.median()/1_000_000:.1f}M VND")
    content.append(f"**Lương thấp nhất:** {salary_data.min()/1_000_000:.1f}M VND")
    content.append(f"**Lương cao nhất:** {salary_data.max()/1_000_000:.1f}M VND\n")
    
    content.append("### Lương theo nhóm nghề\n")
    salary_by_group = df[df['salary_numeric'].notna()].groupby('job_group')['salary_numeric'].agg(['mean', 'count'])
    salary_by_group = salary_by_group[salary_by_group['count'] >= 5].sort_values('mean', ascending=False)
    
    for job, row in salary_by_group.head(10).iterrows():
        content.append(f"- {job}: {row['mean']/1_000_000:.1f}M VND ({int(row['count'])} mẫu)")
    
    content.append("\n### Lương theo cấp độ\n")
    salary_by_level = df[df['salary_numeric'].notna()].groupby('level')['salary_numeric'].mean().sort_values(ascending=False)
    
    for level, salary in salary_by_level.items():
        content.append(f"- {level.capitalize()}: {salary/1_000_000:.1f}M VND")
    
    return content


def generate_skills_report(df):
    """Generate skills report content"""
    import ast
    from collections import Counter
    
    content = []
    content.append("## PHÂN TÍCH KỸ NĂNG\n")
    
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
    
    content.append(f"**Tổng số kỹ năng:** {len(skill_counts)}")
    content.append(f"**Kỹ năng xuất hiện nhiều nhất:** {skill_counts.most_common(1)[0][0]}\n")
    
    content.append("### Top 20 kỹ năng được yêu cầu\n")
    for skill, count in skill_counts.most_common(20):
        pct = (count / len(df)) * 100
        content.append(f"{skill.capitalize()}: {count:,} ({pct:.1f}%)")
    
    return content


def generate_custom_report(df):
    """Generate custom report"""
    return ["## BÁO CÁO TÙY CHỈNH\n", "\n(Nội dung tùy chỉnh theo yêu cầu)"]
