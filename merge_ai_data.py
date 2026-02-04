"""
Auto Process AI Data - Merge with existing data
Tự động gộp data AI vào data hiện có
"""
import pandas as pd
import re
from pathlib import Path

def extract_salary_numeric(salary_str):
    """Extract numeric salary"""
    if pd.isna(salary_str) or salary_str == 'Negotiable':
        return None
    
    numbers = re.findall(r'(\d+)', str(salary_str))
    if numbers:
        nums = [int(n) for n in numbers]
        avg = sum(nums) / len(nums)
        return avg * 1_000_000
    return None

def classify_job_group(job_title):
    """Classify job group"""
    title_lower = str(job_title).lower()
    
    if 'backend' in title_lower:
        return 'Backend Developer'
    elif 'frontend' in title_lower:
        return 'Frontend Developer'
    elif 'fullstack' in title_lower:
        return 'Fullstack Developer'
    elif 'mobile' in title_lower or 'ios' in title_lower or 'android' in title_lower:
        return 'Mobile Developer'
    elif 'data' in title_lower or 'ai' in title_lower:
        return 'Data / AI'
    elif 'devops' in title_lower:
        return 'DevOps / Cloud'
    else:
        return 'Backend Developer'  # Default

# Paths
project_root = Path(__file__).parent
ai_file = project_root / "data_raw" / "ITViec_AI_demo.csv"
existing_file = project_root / "data_clean" / "clean_data.csv"
output_file = project_root / "data_clean" / "clean_data.csv"  # Overwrite existing

print("="*70)
print("🤖 TỰ ĐỘNG GỘP DATA AI VÀO DATA HIỆN CÓ")
print("="*70)

# Check if AI data exists
if not ai_file.exists():
    print(f"\n❌ Không tìm thấy file: {ai_file}")
    print("Vui lòng chạy: python src/crawler/ITViec_AI_demo.py")
    exit(1)

# Load AI data
print(f"\n📥 Đọc data AI: {ai_file}")
df_ai = pd.read_csv(ai_file)
print(f"  ✓ {len(df_ai)} jobs từ AI crawler")

# Process AI data to standard format
df_ai_processed = pd.DataFrame()
df_ai_processed['job_names'] = df_ai['job_title']
df_ai_processed['company_names'] = df_ai['company_name']
df_ai_processed['salaries'] = df_ai['salary']
df_ai_processed['position_names'] = df_ai['job_title']
df_ai_processed['kind_jobs'] = 'At office'
df_ai_processed['array_skills'] = df_ai['skills']
df_ai_processed['locate_names'] = df_ai['city']
df_ai_processed['exp_skills'] = df_ai['description']
df_ai_processed['domain_arr'] = '[]'
df_ai_processed['post_dates_formatted'] = df_ai['crawled_at']
df_ai_processed['salary_numeric'] = df_ai['salary'].apply(extract_salary_numeric)
df_ai_processed['job_group'] = df_ai['job_title'].apply(classify_job_group)
df_ai_processed['level'] = df_ai['level']
df_ai_processed['city'] = df_ai['city']

# Load existing data
print(f"\n📥 Đọc data hiện có: {existing_file}")
df_existing = pd.read_csv(existing_file)
print(f"  ✓ {len(df_existing)} jobs hiện có")

# Merge
print(f"\n🔄 Gộp data...")
df_merged = pd.concat([df_existing, df_ai_processed], ignore_index=True)

# Remove duplicates
before_dedup = len(df_merged)
df_merged = df_merged.drop_duplicates(subset=['job_names', 'company_names'], keep='first')
after_dedup = len(df_merged)
print(f"  ✓ Đã loại {before_dedup - after_dedup} jobs trùng lặp")

# Save
df_merged.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n✅ HOÀN THÀNH!")
print(f"  • Tổng jobs: {len(df_merged)}")
print(f"  • File output: {output_file}")

print("\n📊 Thống kê:")
print(f"  • Job groups: {df_merged['job_group'].value_counts().to_dict()}")
print(f"  • Cities: {df_merged['city'].value_counts().to_dict()}")

print("\n🎯 Dashboard sẽ tự động dùng data mới này!")
print("   Refresh trang dashboard để thấy data AI")
