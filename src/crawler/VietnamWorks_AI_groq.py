"""
🚀 AI Crawler VietnamWorks với Groq API - DỄ HƠN ITVIEC!
=========================================================
VietnamWorks HTML đơn giản hơn, dễ parse hơn ITViec

⚠️ YÊU CẦU:
    - Groq API key (FREE): https://console.groq.com
    - pip install groq playwright

🚀 USAGE:
    python src/crawler/VietnamWorks_AI_groq.py --jobs 20

💰 CHI PHÍ: MIỄN PHÍ (free tier: 30 req/min)
⏱️ THỜI GIAN: ~1-2 phút (nhanh!)
"""

import os
import sys
import io
import json
import asyncio
from pathlib import Path
from datetime import datetime
import logging
import pandas as pd
import re
from dotenv import load_dotenv

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

load_dotenv()


async def crawl_vietnamworks(num_jobs=20):
    """Crawl VietnamWorks bằng Playwright + Groq API"""
    
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        logger.error("❌ Chưa có Groq API key!")
        logger.info("\n📝 Lấy API key miễn phí:")
        logger.info("   1. Vào: https://console.groq.com")
        logger.info("   2. Sign up (miễn phí)")
        logger.info("   3. Tạo API key")
        logger.info("   4. Thêm vào .env: GROQ_API_KEY=gsk_...")
        return []
    
    logger.info(f"✅ API key loaded")
    logger.info(f"🚀 Model: Llama 3.3 70B (qua Groq - cực nhanh!)\n")
    
    try:
        from playwright.async_api import async_playwright
        from groq import Groq
        
        client = Groq(api_key=api_key)
        
        jobs = []  # Initialize early
        
        logger.info("🌐 Đang khởi động browser...")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,
                args=['--disable-blink-features=AutomationControlled']
            )
            
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            page = await context.new_page()
            
            logger.info("📡 Đang vào VietnamWorks.com...")
            await page.goto("https://www.vietnamworks.com/it-software-jobs-i35-en", wait_until='domcontentloaded')
            
            logger.info("⏳ Đợi jobs load (5s)...")
            await page.wait_for_timeout(5000)
            
            # Scroll to load more
            logger.info("📜 Đang scroll để load jobs...")
            for i in range(3):
                await page.evaluate(f"window.scrollTo(0, {(i+1) * 800})")
                await page.wait_for_timeout(1000)
            
            logger.info("📸 Đang lấy HTML content...")
            content = await page.content()
            
            logger.info(f"📏 HTML length: {len(content):,} characters")
            
            # Extract HTML first before closing
            html_snippet = content[:25000]
            
            # Close browser early to avoid issues
            try:
                await page.close()
                await context.close()
                await browser.close()
                logger.info("✅ Browser closed")
            except:
                pass  # Ignore close errors
            
            logger.info("🧠 Đang gửi HTML cho Groq AI...")
            logger.info("⏱️ Đợi ~20 giây...\n")
            
            prompt = f"""Extract {num_jobs} IT jobs from this VietnamWorks HTML.

Look for job cards/listings with:
- Job titles (usually in <h2>, <h3>, or class with "job-title")
- Company names (class with "company")
- Salary/wage information
- Location/city
- Tech skills, programming languages

For EACH job found, extract these fields:
- job_title: The position name
- company_name: Hiring company
- salary: Salary info or "Negotiable" if not shown
- level: Try to determine from title (fresher/junior/mid/senior) or use "mid"
- city: Work location (Ho Chi Minh/Ha Noi/Da Nang etc)
- skills: List of technologies (Python, Java, React, etc)
- description: Brief job summary if available

Return valid JSON array with {num_jobs} objects:
[
  {{
    "job_title": "Backend Developer",
    "company_name": "FPT Software",
    "salary": "$800-1500",
    "level": "mid",
    "city": "Ho Chi Minh",
    "skills": "Python, Django, MySQL",
    "description": "Develop backend APIs"
  }},
  ...
]

HTML content:
{html_snippet}

IMPORTANT: Return ONLY the JSON array, no other text or explanation."""
            
            # Call Groq API
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at extracting structured job data from HTML. Return only valid JSON arrays."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=4000
            )
            
            result = response.choices[0].message.content
            logger.info("✅ Groq đã trả về kết quả!")
            logger.info(f"📝 Response length: {len(result)} chars")
            
            # Parse JSON
            try:
                # Find JSON array in response
                json_start = result.find('[')
                json_end = result.rfind(']') + 1
                
                if json_start != -1 and json_end > json_start:
                    json_str = result[json_start:json_end]
                    jobs = json.loads(json_str)
                    
                    # Add metadata
                    for job in jobs:
                        job['crawled_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        job['method'] = "Playwright + Groq Llama 3.3"
                        job['source'] = "VietnamWorks"
                    
                    logger.info(f"📊 Đã extract {len(jobs)} jobs từ VietnamWorks!")
                    
                    # Show preview
                    if len(jobs) > 0:
                        logger.info(f"\n📋 SAMPLE JOB:")
                        logger.info(f"  • {jobs[0].get('job_title', 'N/A')}")
                        logger.info(f"  • Company: {jobs[0].get('company_name', 'N/A')}")
                        logger.info(f"  • Salary: {jobs[0].get('salary', 'N/A')}")
                else:
                    logger.error("❌ Không tìm thấy JSON array trong response")
                    logger.info(f"\n📝 Raw response:\n{result[:500]}...")
                    
            except json.JSONDecodeError as e:
                logger.error(f"❌ Lỗi parse JSON: {e}")
                logger.info(f"\n📝 Response:\n{result[:500]}...")
        
        return jobs  # Return outside async context
            
    except ImportError as e:
        logger.error(f"\n❌ Thiếu thư viện: {e}")
        logger.info("\n📦 Cài đặt:")
        logger.info("   pip install groq playwright")
        logger.info("   playwright install chromium")
        return []
        
    except Exception as e:
        logger.error(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
        return []


def save_and_merge(jobs_data):
    """Save và merge vào data chính"""
    if len(jobs_data) == 0:
        logger.warning("⚠️ Không có data để save")
        return None
    
    df = pd.DataFrame(jobs_data)
    
    # Save raw data
    output_path = Path(__file__).parent.parent.parent / "data_raw" / "VietnamWorks_AI_groq.csv"
    output_path.parent.mkdir(exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    logger.info(f"\n💾 Đã lưu raw data: {output_path}")
    
    # Transform and merge
    try:
        main_file = Path(__file__).parent.parent.parent / "data_clean" / "clean_data.csv"
        
        if not main_file.exists():
            logger.warning("⚠️ Chưa có clean_data.csv, skip merge")
            return df
        
        logger.info("\n🔄 Đang transform và merge...")
        
        # Transform to match schema
        df_processed = pd.DataFrame()
        df_processed['job_names'] = df['job_title']
        df_processed['company_names'] = df['company_name']
        df_processed['salaries'] = df['salary']
        df_processed['position_names'] = df['job_title']
        df_processed['kind_jobs'] = 'At office'
        df_processed['array_skills'] = df['skills']
        df_processed['locate_names'] = df['city']
        df_processed['exp_skills'] = df.get('description', 'N/A')
        df_processed['domain_arr'] = '[]'
        df_processed['post_dates_formatted'] = df['crawled_at']
        
        # Extract salary numeric
        def extract_sal(s):
            if pd.isna(s) or 'Negotiable' in str(s) or 'Thoả' in str(s):
                return None
            nums = re.findall(r'(\d+)', str(s))
            return sum([int(n) for n in nums]) / len(nums) * 1_000_000 if nums else None
        
        df_processed['salary_numeric'] = df['salary'].apply(extract_sal)
        
        # Standardize cities
        city_map = {
            'Hồ Chí Minh': 'Ho Chi Minh',
            'HCM': 'Ho Chi Minh',
            'Hà Nội': 'Ha Noi',
            'Hanoi': 'Ha Noi',
            'Đà Nẵng': 'Da Nang',
            'Danang': 'Da Nang'
        }
        df_processed['city'] = df['city'].replace(city_map)
        df_processed['level'] = df.get('level', 'mid')
        df_processed['job_group'] = df['job_title'].str.split().str[0]
        
        # Merge with existing data
        df_main = pd.read_csv(main_file)
        before = len(df_main)
        
        df_merged = pd.concat([df_main, df_processed], ignore_index=True)
        df_merged = df_merged.drop_duplicates(subset=['job_names', 'company_names'], keep='last')
        
        df_merged.to_csv(main_file, index=False, encoding='utf-8-sig')
        
        logger.info(f"  ✓ Trước merge: {before} jobs")
        logger.info(f"  ✓ Sau merge: {len(df_merged)} jobs")
        logger.info(f"  ✓ Thêm mới: +{len(df_merged) - before} jobs")
        
    except Exception as e:
        logger.error(f"❌ Lỗi merge: {e}")
        import traceback
        traceback.print_exc()
    
    return df


async def main():
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--jobs', type=int, default=20, help='Số lượng jobs cần crawl')
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("🚀 AI CRAWLER VIETNAMWORKS với GROQ - DỄ HƠN ITVIEC!")
    print("="*70)
    print(f"🎯 Target: {args.jobs} jobs từ VietnamWorks.com")
    print(f"🤖 AI: Llama 3.3 70B qua Groq (miễn phí + nhanh)")
    print(f"💰 Chi phí: $0 (MIỄN PHÍ)")
    print(f"⏱️ Thời gian: ~1-2 phút")
    print("="*70 + "\n")
    
    # Crawl
    jobs = await crawl_vietnamworks(num_jobs=args.jobs)
    
    if len(jobs) == 0:
        logger.error("\n❌ Crawl thất bại hoặc không tìm thấy jobs")
        logger.info("\n💡 Troubleshooting:")
        logger.info("   1. Check API key: https://console.groq.com")
        logger.info("   2. Check internet connection")
        logger.info("   3. VietnamWorks có thể thay đổi layout")
        return
    
    # Save
    df = save_and_merge(jobs)
    
    if df is not None:
        print("\n" + "="*70)
        print("📊 KẾT QUẢ CRAWL VIETNAMWORKS")
        print("="*70)
        print(f"\n✅ Crawled: {len(df)} jobs THẬT từ VietnamWorks")
        print(f"🚀 API: Groq (miễn phí)")
        print(f"🏢 Companies: {df['company_name'].nunique()}")
        print(f"🌆 Cities: {', '.join(df['city'].unique()[:5])}")
        
        print(f"\n📋 TOP 5 JOBS:")
        cols = ['job_title', 'company_name', 'city', 'salary']
        print(df[cols].head().to_string(index=False))
        
        print("\n" + "="*70)
        print("✅ HOÀN THÀNH - CRAWL VIETNAMWORKS THÀNH CÔNG!")
        print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
