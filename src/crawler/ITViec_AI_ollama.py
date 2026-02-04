"""
🤖 AI Crawler với Ollama (Local LLM) - MIỄN PHÍ 100%
===================================================
Sử dụng Llama 3 local thay vì GPT-4 - KHÔNG TỐN TIỀN!

⚠️ YÊU CẦU:
    - Ollama installed (https://ollama.ai)
    - RAM: 8GB+ (16GB recommended)
    - Chạy: ollama pull llama3

🚀 USAGE:
    python src/crawler/ITViec_AI_ollama.py --jobs 20

💰 CHI PHÍ: MIỄN PHÍ (chạy local)
⏱️ THỜI GIAN: ~5-10 phút (chậm hơn GPT)
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

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


async def crawl_with_ollama(num_jobs=20):
    """Crawl ITViec bằng Playwright + Ollama (Local LLM)"""
    
    try:
        from playwright.async_api import async_playwright
        import ollama
        
        logger.info("🌐 Đang khởi động browser...")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            logger.info("📡 Đang vào ITViec.com...")
            await page.goto("https://itviec.com/it-jobs", wait_until="networkidle")
            await page.wait_for_timeout(3000)
            
            logger.info("📸 Đang lấy HTML content...")
            content = await page.content()
            
            await browser.close()
            
            # Extract HTML snippet
            html_snippet = content[:8000]  # 8k chars
            
            logger.info("🧠 Đang gửi HTML cho Llama 3 (local AI)...")
            logger.info("⏱️ Đợi ~1-2 phút (AI đang chạy trên máy bạn)...\n")
            
            prompt = f"""Extract {num_jobs} jobs from this ITViec HTML.

For each job, extract:
- job_title
- company_name  
- salary (or "Negotiable")
- level (fresher/junior/mid/senior)
- city
- skills (comma-separated)
- description (brief)

Return ONLY valid JSON array:
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

RETURN ONLY JSON, NO OTHER TEXT."""
            
            # Call Ollama (local)
            response = ollama.chat(
                model='llama3',
                messages=[
                    {
                        'role': 'system',
                        'content': 'You extract structured data from HTML. Return only valid JSON.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            )
            
            result = response['message']['content']
            logger.info("✅ Llama 3 đã trả về kết quả\n")
            
            # Parse JSON
            try:
                json_start = result.find('[')
                json_end = result.rfind(']') + 1
                
                if json_start != -1 and json_end > json_start:
                    json_str = result[json_start:json_end]
                    jobs = json.loads(json_str)
                    
                    # Add metadata
                    for job in jobs:
                        job['crawled_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        job['method'] = "Playwright + Llama3 (Local)"
                    
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
        logger.info("   1. Cài Ollama: https://ollama.ai/download")
        logger.info("   2. Chạy: ollama pull llama3")
        logger.info("   3. pip install ollama playwright")
        logger.info("   4. playwright install chromium")
        return []
        
    except Exception as e:
        logger.error(f"\n❌ Lỗi: {e}")
        logger.info("\n💡 Kiểm tra:")
        logger.info("   - Ollama đã chạy chưa? (ollama serve)")
        logger.info("   - Đã pull model? (ollama pull llama3)")
        return []


def save_and_merge(jobs_data):
    """Save và merge vào data chính"""
    if len(jobs_data) == 0:
        logger.warning("⚠️ Không có data")
        return None
    
    df = pd.DataFrame(jobs_data)
    
    # Save
    output_path = Path(__file__).parent.parent.parent / "data_raw" / "ITViec_AI_ollama.csv"
    output_path.parent.mkdir(exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    logger.info(f"\n💾 Đã lưu: {output_path}")
    
    # Merge
    try:
        main_file = Path(__file__).parent.parent.parent / "data_clean" / "clean_data.csv"
        
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
    print("🤖 AI CRAWLER với OLLAMA (Local LLM) - MIỄN PHÍ!")
    print("="*70)
    print(f"Target: {args.jobs} jobs từ ITViec.vn")
    print(f"AI: Llama 3 (chạy local trên máy bạn)")
    print(f"💰 Chi phí: $0 (MIỄN PHÍ)")
    print(f"⏱️ Thời gian: ~5-10 phút")
    print("="*70 + "\n")
    
    # Check Ollama
    try:
        import ollama
        models = ollama.list()
        logger.info(f"✅ Ollama đã cài\n")
    except:
        logger.error("❌ Chưa cài Ollama!")
        logger.info("\n📦 Cài đặt:")
        logger.info("   1. Tải Ollama: https://ollama.ai/download")
        logger.info("   2. Cài đặt và chạy")
        logger.info("   3. Chạy: ollama pull llama3")
        logger.info("   4. pip install ollama")
        return
    
    # Crawl
    jobs = await crawl_with_ollama(num_jobs=args.jobs)
    
    if len(jobs) == 0:
        logger.error("\n❌ Crawl thất bại")
        return
    
    # Save
    df = save_and_merge(jobs)
    
    if df is not None:
        print("\n" + "="*70)
        print("📊 KẾT QUẢ")
        print("="*70)
        print(f"\n✅ Crawled: {len(df)} jobs THẬT")
        print(f"🤖 AI: Llama 3 (local, miễn phí)")
        print(f"🏢 Companies: {df['company_name'].nunique()}")
        
        print(f"\n📋 SAMPLE:")
        cols = ['job_title', 'company_name', 'city']
        print(df[cols].head().to_string(index=False))
        
        print("\n" + "="*70)
        print("✅ HOÀN THÀNH - KHÔNG TỐN TIỀN!")
        print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
