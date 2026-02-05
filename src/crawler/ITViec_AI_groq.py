"""
🚀 AI Crawler với Groq API - MIỄN PHÍ + CỰC NHANH
=================================================
Groq = API miễn phí, nhanh hơn GPT-4, không cần download gì!

⚠️ YÊU CẦU:
    - Groq API key (FREE): https://console.groq.com
    - pip install groq

🚀 USAGE:
    python src/crawler/ITViec_AI_groq.py --jobs 20

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


def extract_json_array(text):
    """Extract JSON array from LLM response (handles code fences)."""
    if not text:
        return None

    # Strip code fences if present
    if "```" in text:
        parts = text.split("```")
        # Prefer the first fenced block content
        if len(parts) >= 2:
            text = parts[1]
            # Remove optional language tag
            if text.strip().startswith("json"):
                text = text.strip()[4:]

    # Try to locate JSON array
    start = text.find('[')
    end = text.rfind(']') + 1
    if start == -1 or end <= start:
        return None

    try:
        return json.loads(text[start:end])
    except Exception:
        return None


async def crawl_with_groq(num_jobs=20):
    """Crawl ITViec bằng Playwright + Groq API"""
    
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
    logger.info(f"🚀 Model: Llama 3 70B (qua Groq - cực nhanh!)\n")
    
    try:
        from playwright.async_api import async_playwright
        from groq import Groq
        
        client = Groq(api_key=api_key)
        
        logger.info("🌐 Đang khởi động browser...")
        
        async with async_playwright() as p:
            # Launch with stealth mode
            browser = await p.chromium.launch(
                headless=False,  # Show browser để bypass detection
                args=['--disable-blink-features=AutomationControlled']
            )
            
            # Create page with real user agent
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            
            # Hide automation
            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """)
            
            logger.info("📡 Đang vào ITViec.com...")
            await page.goto("https://itviec.com/it-jobs", wait_until='domcontentloaded', timeout=30000)
            
            # Wait a bit for page to load
            await page.wait_for_timeout(3000)
            
            # Scroll slowly like human
            logger.info("📜 Đang scroll như người thật...")
            for i in range(3):
                await page.evaluate(f"window.scrollTo(0, {(i+1) * 500})")
                await page.wait_for_timeout(500)
            
            logger.info("📸 Đang lấy HTML content...")
            content = await page.content()
            
            # Debug: print HTML length
            logger.info(f"📏 HTML length: {len(content):,} characters")
            
            await browser.close()
            
            # Extract HTML snippet (larger for better context)
            html_snippet = content[:20000]  # 20K chars for better job extraction
            
            logger.info("🧠 Đang gửi HTML cho Groq AI...")
            logger.info("⏱️ Đợi ~30 giây (Groq siêu nhanh)...\n")
            
            prompt = f"""You are a web scraping expert. Extract up to {num_jobs} jobs from this ITViec.com HTML.

FIND job listings in the HTML - they usually have:
- Job titles (h3, h2, or class="job-title")
- Company names (class="company-name" or similar)
- Salary information
- Location/city

For EACH job you find, extract:
- job_title: The position name
- company_name: Company hiring
- salary: Salary range or "Negotiable"
- level: junior/mid/senior/fresher (or guess from title)
- city: Work location
- skills: Programming languages/tech mentioned
- description: Brief job summary

Return a JSON array with up to {num_jobs} jobs. If you find fewer jobs, return what you found.

Format:
[
  {{
    "job_title": "Backend Developer",
    "company_name": "VNG Corporation",
    "salary": "$1000-2000",
    "level": "mid",
    "city": "Ho Chi Minh",
    "skills": "Python, Django, PostgreSQL",
    "description": "Develop and maintain backend services"
  }}
]

HTML:
{html_snippet}

RETURN ONLY THE RAW JSON ARRAY. DO NOT WRAP WITH CODE FENCES OR EXTRA TEXT."""
            
            # Call Groq API
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Latest free model
                messages=[
                    {
                        "role": "system",
                        "content": "You extract structured data from HTML. Return only valid JSON."
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
            
            # Parse JSON with better error handling
            jobs = extract_json_array(result)
            if not jobs:
                logger.error("❌ Không tìm thấy JSON")
                logger.info(f"Response: {result[:500]}")
                return []
            
            if isinstance(jobs, list) and len(jobs) > 0:
                # Add metadata
                for job in jobs:
                    job['crawled_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    job['method'] = "Playwright + Groq Llama 3.1 70B"
                
                logger.info(f"📊 Đã extract {len(jobs)} jobs!")
                return jobs
            else:
                logger.error("❌ Không tìm thấy JSON")
                return []
                    
    except json.JSONDecodeError as e:
        logger.error(f"❌ Lỗi parse JSON: {e}")
        logger.info(f"\n📝 Response:\n{result[:500]}...")
        return []
            
    except ImportError as e:
        logger.error(f"\n❌ Thiếu thư viện: {e}")
        logger.info("\n📦 Cài đặt:")
        logger.info("   pip install groq playwright")
        logger.info("   playwright install chromium")
        return []
        
    except Exception as e:
        logger.error(f"\n❌ Lỗi: {e}")
        logger.info("\n💡 Kiểm tra:")
        logger.info("   - API key đúng chưa?")
        logger.info("   - Đã sign up Groq chưa?")
        return []


def save_and_merge(jobs_data):
    """Save và merge vào data chính"""
    if len(jobs_data) == 0:
        logger.warning("⚠️ Không có data")
        return None
    
    df = pd.DataFrame(jobs_data)
    
    # Save
    output_path = Path(__file__).parent.parent.parent / "data" / "raw" / "ITViec_AI_groq.csv"
    output_path.parent.mkdir(exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    logger.info(f"\n💾 Đã lưu: {output_path}")

    # Sync into main raw file (append + dedupe)
    try:
        raw_main = Path(__file__).parent.parent.parent / "data" / "raw" / "ITViec_data.csv"

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

        if raw_main.exists():
            df_raw = pd.read_csv(raw_main)
            before_raw = len(df_raw)
            df_raw_merged = pd.concat([df_raw, df_processed], ignore_index=True)
            df_raw_merged = df_raw_merged.drop_duplicates(subset=['job_names', 'company_names'])
            df_raw_merged.to_csv(raw_main, index=False, encoding='utf-8-sig')
            logger.info("\n🔄 Đã cập nhật data/raw/ITViec_data.csv")
            logger.info(f"  ✓ Trước: {before_raw} jobs")
            logger.info(f"  ✓ Sau: {len(df_raw_merged)} jobs (+{len(df_raw_merged) - before_raw})")
        else:
            df_processed.to_csv(raw_main, index=False, encoding='utf-8-sig')
            logger.info("\n💾 Tạo mới data/raw/ITViec_data.csv")
            logger.info(f"  ✓ Tổng: {len(df_processed)} jobs")
    except Exception as e:
        logger.error(f"❌ Lỗi cập nhật raw data: {e}")
    
    # Merge
    try:
        main_file = Path(__file__).parent.parent.parent / "data" / "processed" / "clean_data.csv"
        
        if not main_file.exists():
            return df
        
        logger.info("\n🔄 Đang merge...")
        
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
        
        def extract_sal(s):
            if pd.isna(s) or 'Negotiable' in str(s):
                return None
            nums = re.findall(r'(\d+)', str(s))
            return sum([int(n) for n in nums]) / len(nums) * 1_000_000 if nums else None
        
        df_processed['salary_numeric'] = df['salary'].apply(extract_sal)
        
        city_map = {'Hồ Chí Minh': 'Ho Chi Minh', 'Hà Nội': 'Ha Noi', 'Đà Nẵng': 'Da Nang'}
        df_processed['city'] = df['city'].replace(city_map)
        df_processed['level'] = df['level']
        df_processed['job_group'] = df['job_title'].str.split().str[0]
        
        df_main = pd.read_csv(main_file)
        before = len(df_main)
        
        df_merged = pd.concat([df_main, df_processed], ignore_index=True)
        df_merged = df_merged.drop_duplicates(subset=['job_names', 'company_names'])
        
        df_merged.to_csv(main_file, index=False, encoding='utf-8-sig')
        
        logger.info(f"  ✓ Trước: {before} jobs")
        logger.info(f"  ✓ Sau: {len(df_merged)} jobs (+{len(df_merged) - before})")
        
    except Exception as e:
        logger.error(f"❌ Lỗi merge: {e}")
    
    return df


async def main():
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--jobs', type=int, default=20)
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("🚀 AI CRAWLER với GROQ API - MIỄN PHÍ + CỰC NHANH!")
    print("="*70)
    print(f"Target: {args.jobs} jobs từ ITViec.vn")
    print(f"AI: Llama 3.1 70B qua Groq (nhanh hơn GPT-4)")
    print(f"💰 Chi phí: $0 (MIỄN PHÍ)")
    print(f"⏱️ Thời gian: ~1-2 phút")
    print("="*70 + "\n")
    
    # Crawl in batches to avoid token limits
    target = args.jobs
    batch_size = 20
    all_jobs = []
    attempts = 0

    while len(all_jobs) < target and attempts < 5:
        remaining = target - len(all_jobs)
        batch = min(batch_size, remaining)
        attempts += 1

        jobs = await crawl_with_groq(num_jobs=batch)
        if not jobs:
            break

        all_jobs.extend(jobs)

        # Deduplicate by title + company
        seen = set()
        unique = []
        for job in all_jobs:
            key = (str(job.get('job_title', '')).strip().lower(),
                   str(job.get('company_name', '')).strip().lower())
            if key in seen:
                continue
            seen.add(key)
            unique.append(job)
        all_jobs = unique

        if len(all_jobs) < target:
            await asyncio.sleep(6)
    
    if len(all_jobs) == 0:
        logger.error("\n❌ Crawl thất bại")
        logger.info("\n💡 Lấy API key miễn phí:")
        logger.info("   https://console.groq.com")
        return
    
    # Save
    df = save_and_merge(all_jobs)
    
    if df is not None:
        print("\n" + "="*70)
        print("📊 KẾT QUẢ")
        print("="*70)
        print(f"\n✅ Crawled: {len(df)} jobs THẬT")
        print(f"🚀 API: Groq (miễn phí, nhanh)")
        print(f"🏢 Companies: {df['company_name'].nunique()}")
        
        print(f"\n📋 SAMPLE:")
        cols = ['job_title', 'company_name', 'city']
        print(df[cols].head().to_string(index=False))
        
        print("\n" + "="*70)
        print("✅ HOÀN THÀNH - KHÔNG TỐN TIỀN + CỰC NHANH!")
        print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
