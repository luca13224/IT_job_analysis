"""
🤖 AI CRAWLER THẬT - Version đơn giản với Playwright + GPT
==========================================================
Không cần browser-use, chỉ dùng Playwright + OpenAI API trực tiếp

⚠️ YÊU CẦU:
    - OpenAI API key
    - playwright
    
🚀 USAGE:
    python src/crawler/ITViec_AI_simple_real.py --jobs 20
"""

import os
import sys
import io
import json
import asyncio
from pathlib import Path
from datetime import datetime
import logging
from dotenv import load_dotenv
import pandas as pd
import re

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

load_dotenv()


async def crawl_with_playwright_and_ai(num_jobs=20):
    """Crawl ITViec bằng Playwright + GPT để parse HTML"""
    
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    if not api_key or api_key == "sk-your-openai-api-key-here":
        logger.error("❌ Chưa có OpenAI API key trong file .env!")
        return []
    
    logger.info(f"✅ API key loaded")
    logger.info(f"🤖 Model: {model}\n")
    
    try:
        from playwright.async_api import async_playwright
        from openai import OpenAI
        
        client = OpenAI(api_key=api_key)
        
        logger.info("🌐 Đang khởi động browser...")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            logger.info("📡 Đang vào ITViec.com...")
            await page.goto("https://itviec.com/it-jobs", wait_until="networkidle")
            await page.wait_for_timeout(3000)
            
            logger.info("📸 Đang lấy HTML content...")
            content = await page.content()
            
            # Lấy job cards
            job_cards = await page.query_selector_all('[class*="job"]')
            logger.info(f"✅ Tìm thấy {len(job_cards)} job cards\n")
            
            await browser.close()
            
            # Extract một phần HTML để gửi cho GPT
            html_snippet = content[:10000]  # Lấy 10k chars đầu
            
            logger.info("🧠 Đang gửi HTML cho GPT để extract data...")
            logger.info("⏱️ Đợi ~30 giây...\n")
            
            prompt = f"""
Phân tích HTML sau từ trang ITViec.com và extract {num_jobs} jobs đầu tiên.

Với mỗi job, extract:
- job_title: Tiêu đề công việc
- company_name: Tên công ty  
- salary: Mức lương (nếu không có ghi "Negotiable")
- level: Cấp độ (fresher/junior/mid/senior)
- city: Thành phố (Hồ Chí Minh/Hà Nội/Đà Nẵng...)
- skills: Các skills yêu cầu (cách nhau bởi dấu phẩy)
- description: Mô tả ngắn

Trả về JSON array:
[
  {{
    "job_title": "...",
    "company_name": "...",
    "salary": "...",
    "level": "...",
    "city": "...",
    "skills": "...",
    "description": "..."
  }}
]

HTML:
{html_snippet}

CHỈ TRẢ VỀ JSON ARRAY, KHÔNG GHI GÌ THÊM.
"""
            
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert at extracting structured data from HTML. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            
            result = response.choices[0].message.content
            logger.info("✅ GPT đã trả về kết quả\n")
            
            # Parse JSON
            try:
                # Extract JSON từ response (có thể có ```json wrapper)
                json_start = result.find('[')
                json_end = result.rfind(']') + 1
                
                if json_start != -1 and json_end > json_start:
                    json_str = result[json_start:json_end]
                    jobs = json.loads(json_str)
                    
                    # Add metadata
                    for job in jobs:
                        job['crawled_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        job['method'] = f"Playwright + {model}"
                    
                    logger.info(f"📊 Đã extract {len(jobs)} jobs từ HTML!")
                    return jobs
                else:
                    logger.error("❌ Không tìm thấy JSON trong response")
                    return []
                    
            except json.JSONDecodeError as e:
                logger.error(f"❌ Lỗi parse JSON: {e}")
                logger.info(f"\n📝 Response từ GPT:\n{result[:500]}...")
                return []
            
    except ImportError as e:
        logger.error(f"\n❌ Thiếu thư viện: {e}")
        logger.info("\n📦 Cài đặt:")
        logger.info("   pip install playwright openai")
        logger.info("   playwright install chromium")
        return []
        
    except Exception as e:
        logger.error(f"\n❌ Lỗi: {e}")
        return []


def save_and_merge(jobs_data):
    """Save và merge vào data chính"""
    if len(jobs_data) == 0:
        logger.warning("⚠️ Không có data để lưu")
        return None
    
    df = pd.DataFrame(jobs_data)
    
    # Save to data_raw
    output_path = Path(__file__).parent.parent.parent / "data_raw" / "ITViec_AI_real.csv"
    output_path.parent.mkdir(exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    logger.info(f"\n💾 Đã lưu vào: {output_path}")
    
    # Auto merge
    try:
        main_file = Path(__file__).parent.parent.parent / "data_clean" / "clean_data.csv"
        
        if not main_file.exists():
            logger.info("⚠️ Không tìm thấy main data file")
            return df
        
        logger.info("\n🔄 Đang merge vào data chính...")
        
        # Transform
        df_processed = pd.DataFrame()
        df_processed['job_names'] = df['job_title']
        df_processed['company_names'] = df['company_name']
        df_processed['salaries'] = df['salary']
        df_processed['position_names'] = df['job_title']
        df_processed['kind_jobs'] = 'At office'
        df_processed['array_skills'] = df['skills']
        df_processed['locate_names'] = df['city']
        df_processed['exp_skills'] = df['description']
        df_processed['domain_arr'] = '[]'
        df_processed['post_dates_formatted'] = df['crawled_at']
        
        # Extract salary numeric
        def extract_sal(s):
            if pd.isna(s) or 'Negotiable' in str(s):
                return None
            nums = re.findall(r'(\d+)', str(s))
            return sum([int(n) for n in nums]) / len(nums) * 1_000_000 if nums else None
        
        df_processed['salary_numeric'] = df['salary'].apply(extract_sal)
        
        # Normalize
        city_map = {'Hồ Chí Minh': 'Ho Chi Minh', 'Hà Nội': 'Ha Noi', 'Đà Nẵng': 'Da Nang'}
        df_processed['city'] = df['city'].replace(city_map)
        df_processed['level'] = df['level']
        df_processed['job_group'] = df['job_title'].str.split().str[0]
        
        # Load and merge
        df_main = pd.read_csv(main_file)
        before = len(df_main)
        
        df_merged = pd.concat([df_main, df_processed], ignore_index=True)
        df_merged = df_merged.drop_duplicates(subset=['job_names', 'company_names'])
        
        df_merged.to_csv(main_file, index=False, encoding='utf-8-sig')
        
        logger.info(f"  ✓ Trước: {before} jobs")
        logger.info(f"  ✓ Sau: {len(df_merged)} jobs (+{len(df_merged) - before})")
        logger.info(f"  💾 Đã lưu: {main_file}")
        
    except Exception as e:
        logger.error(f"❌ Lỗi merge: {e}")
    
    return df


async def main():
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--jobs', type=int, default=20)
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("🤖 AI CRAWLER THẬT - Playwright + GPT")
    print("="*70)
    print(f"Target: {args.jobs} jobs từ ITViec.vn")
    print(f"Method: Playwright crawl HTML → GPT extract data")
    print(f"💰 Chi phí: ~$0.05-0.10")
    print("="*70 + "\n")
    
    # Crawl
    jobs = await crawl_with_playwright_and_ai(num_jobs=args.jobs)
    
    if len(jobs) == 0:
        logger.error("\n❌ Crawl thất bại")
        return
    
    # Save and merge
    df = save_and_merge(jobs)
    
    if df is not None:
        print("\n" + "="*70)
        print("📊 KẾT QUẢ CRAWL")
        print("="*70)
        print(f"\n✅ Đã crawl: {len(df)} jobs THẬT từ ITViec.vn")
        print(f"🏢 Công ty: {df['company_name'].nunique()}")
        print(f"🏙️ Thành phố: {df['city'].nunique()}")
        
        print(f"\n📋 MẪU 5 JOBS:")
        print("="*70)
        cols = ['job_title', 'company_name', 'salary', 'city']
        print(df[cols].head().to_string(index=False))
        
        print("\n" + "="*70)
        print("✅ HOÀN THÀNH!")
        print("💾 Data đã merge vào: data_clean/clean_data.csv")
        print("🔄 Refresh dashboard để xem")
        print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
