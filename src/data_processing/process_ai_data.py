"""
Process AI Crawler Data to Standard Format
Chuyển đổi data từ AI crawler sang format chuẩn để dashboard sử dụng
"""
import pandas as pd
import ast
import re
from datetime import datetime
from pathlib import Path

def extract_salary_numeric(salary_str):
    """Extract numeric salary from string"""
    if pd.isna(salary_str) or salary_str == 'Negotiable':
        return None
    
    # Extract numbers from string like "30-40 triệu VND"
    numbers = re.findall(r'(\d+)', str(salary_str))
    if numbers:
        # If range, take average
        nums = [int(n) for n in numbers]
        avg = sum(nums) / len(nums)
        return avg * 1_000_000  # Convert to VND
    return None

def classify_job_group(job_title):
    """Classify job into groups"""
    title_lower = str(job_title).lower()
    
    if 'backend' in title_lower or 'back-end' in title_lower:
        return 'Backend Developer'
    elif 'frontend' in title_lower or 'front-end' in title_lower:
        return 'Frontend Developer'
    elif 'fullstack' in title_lower or 'full-stack' in title_lower:
        return 'Fullstack Developer'
    elif 'mobile' in title_lower or 'ios' in title_lower or 'android' in title_lower:
        return 'Mobile Developer'
    elif 'data' in title_lower or 'ai' in title_lower or 'ml' in title_lower:
        return 'Data / AI'
    elif 'devops' in title_lower or 'infrastructure' in title_lower:
        return 'DevOps / Cloud'
    elif 'qa' in title_lower or 'test' in title_lower:
        return 'QA / Tester'
    else:
        return 'Other'

def process_ai_data(input_file, output_file):
    """
    Process AI crawler data to standard format
    
    Args:
        input_file: Path to AI demo CSV (e.g., data_raw/ITViec_AI_demo.csv)
        output_file: Path to output CSV (e.g., data_clean/clean_data_ai.csv)
    """
    print(f"📥 Đọc dữ liệu AI từ: {input_file}")
    df = pd.read_csv(input_file)
    
    print(f"✓ Đã load {len(df)} jobs từ AI crawler")
    
    # Rename columns to match standard format
    df_processed = pd.DataFrame()
    
    # Basic fields (rename from AI format to standard format)
    df_processed['job_names'] = df['job_title']
    df_processed['company_names'] = df['company_name']
    df_processed['salaries'] = df['salary']
    df_processed['level'] = df['level']
    df_processed['city'] = df['city']
    
    # Skills: convert string representation to proper format
    df_processed['array_skills'] = df['skills']
    
    # Additional fields
    df_processed['position_names'] = df['job_title'].apply(lambda x: x.split(' - ')[0] if ' - ' in str(x) else x)
    df_processed['kind_jobs'] = 'At office'  # Default for AI demo
    df_processed['locate_names'] = df['city']
    df_processed['exp_skills'] = df['description']
    df_processed['domain_arr'] = '[]'
    df_processed['post_dates_formatted'] = df['crawled_at']
    
    # Calculate numeric salary
    df_processed['salary_numeric'] = df['salary'].apply(extract_salary_numeric)
    
    # Classify job group
    df_processed['job_group'] = df['job_title'].apply(classify_job_group)
    
    print("\n📊 Thống kê sau xử lý:")
    print(f"  • Tổng jobs: {len(df_processed)}")
    print(f"  • Job groups: {df_processed['job_group'].value_counts().to_dict()}")
    print(f"  • Levels: {df_processed['level'].value_counts().to_dict()}")
    print(f"  • Cities: {df_processed['city'].value_counts().to_dict()}")
    
    # Save to output file
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df_processed.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✅ Đã lưu data xử lý tại: {output_file}")
    
    return df_processed

def merge_ai_with_existing(ai_file, existing_file, output_file):
    """
    Merge AI data with existing cleaned data
    
    Args:
        ai_file: AI demo CSV
        existing_file: Existing clean_data.csv
        output_file: Output merged file
    """
    print("🔄 Gộp dữ liệu AI với dữ liệu hiện có...")
    
    # Process AI data
    df_ai = process_ai_data(ai_file, "temp_ai.csv")
    
    # Load existing data
    df_existing = pd.read_csv(existing_file)
    print(f"  • Dữ liệu hiện có: {len(df_existing)} jobs")
    print(f"  • Dữ liệu AI: {len(df_ai)} jobs")
    
    # Combine
    df_merged = pd.concat([df_existing, df_ai], ignore_index=True)
    
    # Remove duplicates based on job_names + company_names
    df_merged = df_merged.drop_duplicates(subset=['job_names', 'company_names'], keep='first')
    
    print(f"\n✅ Tổng sau gộp: {len(df_merged)} jobs (đã loại trùng)")
    
    # Save
    df_merged.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"💾 Đã lưu tại: {output_file}")
    
    return df_merged

if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    # Get project root
    project_root = Path(__file__).parent.parent.parent
    
    ai_data = project_root / "data_raw" / "ITViec_AI_demo.csv"
    clean_data = project_root / "data_clean" / "clean_data.csv"
    
    print("="*70)
    print("🤖 XỬ LÝ DỮ LIỆU AI CRAWLER")
    print("="*70)
    print("\nLựa chọn:")
    print("1. Chỉ xử lý data AI (tạo file mới)")
    print("2. Gộp data AI với data hiện có")
    
    choice = input("\nNhập lựa chọn (1 hoặc 2): ").strip()
    
    if choice == "1":
        output = project_root / "data_clean" / "clean_data_ai.csv"
        process_ai_data(ai_data, output)
        
        print("\n" + "="*70)
        print("✅ HOÀN THÀNH!")
        print("="*70)
        print(f"\nĐể dùng data AI cho dashboard, sửa file:")
        print(f"  config/config.py")
        print(f"\nThay đổi:")
        print(f"  CLEAN_CSV_PATH = DATA_CLEAN_DIR / 'clean_data_ai.csv'")
        
    elif choice == "2":
        output = project_root / "data_clean" / "clean_data_merged.csv"
        merge_ai_with_existing(ai_data, clean_data, output)
        
        print("\n" + "="*70)
        print("✅ HOÀN THÀNH!")
        print("="*70)
        print(f"\nĐể dùng data merged cho dashboard, sửa file:")
        print(f"  config/config.py")
        print(f"\nThay đổi:")
        print(f"  CLEAN_CSV_PATH = DATA_CLEAN_DIR / 'clean_data_merged.csv'")
    
    else:
        print("❌ Lựa chọn không hợp lệ!")
