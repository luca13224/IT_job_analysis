"""
🤖 AI CRAWLER THẬT - Crawl data thật từ ITViec.vn bằng AI
==========================================================
Sử dụng GPT-4 + Browser automation để tự động crawl

⚠️ YÊU CẦU:
    - OpenAI API key (trong file .env)
    - Python 3.11+
    - browser-use, langchain-openai

🚀 CÁCH DÙNG:
    python src/crawler/ITViec_AI_real.py --jobs 50
    python src/crawler/ITViec_AI_real.py --jobs 100
    python src/crawler/ITViec_AI_real.py --quick  # 20 jobs

💰 CHI PHÍ:
    ~$0.50 cho 100 jobs (GPT-3.5-turbo)
    ~$2.00 cho 100 jobs (GPT-4)

⏱️ THỜI GIAN:
    ~10-15 phút cho 100 jobs
"""

import os
import sys
import io
import asyncio
import pandas as pd
from datetime import datetime
from pathlib import Path
import logging
import re
from dotenv import load_dotenv

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class RealAICrawler:
    """AI crawler thật sử dụng GPT-4 + Browser automation"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.jobs_data = []
        
        if not self.api_key or self.api_key == "sk-your-openai-api-key-here":
            raise ValueError(
                "❌ Chưa có OpenAI API key!\n"
                "📝 Hướng dẫn:\n"
                "   1. Mở file .env\n"
                "   2. Lấy API key từ: https://platform.openai.com/api-keys\n"
                "   3. Thay thế OPENAI_API_KEY=sk-your-key\n"
            )
        
        logger.info(f"✅ Đã load API key")
        logger.info(f"🤖 Sử dụng model: {self.model}")
        
    async def setup_browser_agent(self):
        """Setup browser-use agent với GPT"""
        try:
            from browser_use import Agent
            from langchain_openai import ChatOpenAI
            
            logger.info("🌐 Đang khởi tạo AI browser agent...")
            
            # Initialize LLM
            llm = ChatOpenAI(
                model=self.model,
                openai_api_key=self.api_key,
                temperature=0.1  # Low temperature for consistent extraction
            )
            
            # Create browser agent
            self.agent = Agent(
                task="Navigate to ITViec.com and extract IT job listings",
                llm=llm
            )
            
            logger.info("✅ Browser agent sẵn sàng!")
            return True
            
        except ImportError:
            logger.error("❌ Chưa cài browser-use!")
            logger.info("\n📦 Cài đặt:")
            logger.info("   pip install browser-use langchain-openai playwright")
            logger.info("   playwright install chromium")
            return False
            
        except Exception as e:
            logger.error(f"❌ Lỗi setup: {e}")
            return False
    
    async def crawl_with_ai(self, num_jobs=50):
        """Sử dụng AI để crawl thật từ ITViec.vn"""
        logger.info(f"\n🤖 AI đang vào ITViec.vn và crawl {num_jobs} jobs...")
        logger.info("⏱️ Thời gian ước tính: 10-15 phút")
        logger.info("💰 Chi phí ước tính: $0.25-0.50\n")
        
        try:
            from browser_use import Agent
            from langchain_openai import ChatOpenAI
            
            # Create LLM
            llm = ChatOpenAI(
                model=self.model,
                openai_api_key=self.api_key,
                temperature=0.1
            )
            
            # Create agent with detailed task
            task = f"""
Vào trang https://itviec.com/it-jobs và crawl {num_jobs} công việc IT.

Với mỗi công việc, trích xuất:
1. job_title (tiêu đề công việc)
2. company_name (tên công ty)
3. salary (mức lương, nếu không có ghi "Negotiable")
4. level (cấp độ: fresher, junior, mid, senior...)
5. city (thành phố: Hồ Chí Minh, Hà Nội, Đà Nẵng...)
6. skills (các kỹ năng yêu cầu, ngăn cách bởi dấu phẩy)
7. description (mô tả ngắn về công việc)

Scroll xuống để load thêm jobs nếu cần.
Click "Load more" hoặc "Xem thêm" nếu có.

Trả về kết quả dưới dạng JSON array:
[
  {{
    "job_title": "Backend Developer",
    "company_name": "VNG Corporation",
    "salary": "30-40 triệu VND",
    "level": "mid",
    "city": "Hồ Chí Minh",
    "skills": "Python, Django, PostgreSQL, Docker",
    "description": "Develop scalable backend systems"
  }},
  ...
]
"""

            logger.info("🧠 AI đang phân tích trang web...")
            agent = Agent(task=task, llm=llm)
            
            # Run agent
            result = await agent.run()
            
            logger.info("✅ AI đã hoàn thành crawl!")
            
            # Parse result
            self.jobs_data = self._parse_ai_result(result)
            
            if len(self.jobs_data) > 0:
                logger.info(f"📊 Đã crawl được {len(self.jobs_data)} jobs thật từ web")
            else:
                logger.warning("⚠️ Không parse được data. Thử lại với model khác (gpt-4)")
                
            return self.jobs_data
            
        except ImportError:
            logger.error("\n❌ Thiếu thư viện! Cài đặt:")
            logger.info("   pip install browser-use langchain-openai playwright")
            logger.info("   playwright install chromium")
            return []
            
        except Exception as e:
            logger.error(f"❌ Lỗi crawl: {e}")
            logger.info("\n💡 Thử:")
            logger.info("   1. Check API key trong .env")
            logger.info("   2. Đổi model sang gpt-4 trong .env")
            logger.info("   3. Check balance: https://platform.openai.com/usage")
            return []
    
    def _parse_ai_result(self, result):
        """Parse kết quả từ AI"""
        import json
        
        # Try to extract JSON from result
        result_str = str(result)
        
        # Find JSON array
        start_idx = result_str.find('[')
        end_idx = result_str.rfind(']') + 1
        
        if start_idx != -1 and end_idx > start_idx:
            json_str = result_str[start_idx:end_idx]
            try:
                jobs = json.loads(json_str)
                
                # Add metadata
                for job in jobs:
                    job['crawled_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    job['method'] = f"AI-Powered Real ({self.model})"
                
                return jobs
            except json.JSONDecodeError:
                logger.warning("⚠️ Không parse được JSON từ AI response")
                return []
        
        return []
    
    def save_results(self):
        """Save crawled data"""
        if len(self.jobs_data) == 0:
            logger.warning("⚠️ Không có data để lưu")
            return None
        
        # Convert to DataFrame
        df = pd.DataFrame(self.jobs_data)
        
        # Save to data_raw/
        output_path = Path(__file__).parent.parent.parent / "data_raw" / "ITViec_AI_real.csv"
        output_path.parent.mkdir(exist_ok=True)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        logger.info(f"\n💾 Đã lưu vào: {output_path}")
        return df
    
    def auto_merge_to_main(self):
        """Tự động gộp vào data_clean/clean_data.csv"""
        try:
            project_root = Path(__file__).parent.parent.parent
            ai_file = project_root / "data_raw" / "ITViec_AI_real.csv"
            main_file = project_root / "data_clean" / "clean_data.csv"
            
            if not ai_file.exists():
                logger.info("⚠️ Không tìm thấy file AI data để merge")
                return
            
            logger.info("\n🔄 Tự động gộp data AI vào data chính...")
            
            # Load AI data
            df_ai = pd.read_csv(ai_file)
            
            # Transform to standard format
            df_processed = pd.DataFrame()
            df_processed['job_names'] = df_ai['job_title']
            df_processed['company_names'] = df_ai['company_name']
            df_processed['salaries'] = df_ai['salary']
            df_processed['position_names'] = df_ai['job_title']
            df_processed['kind_jobs'] = 'At office'
            df_processed['array_skills'] = df_ai['skills']
            df_processed['locate_names'] = df_ai['city']
            df_processed['exp_skills'] = df_ai['description']
            df_processed['domain_arr'] = '[]'
            df_processed['post_dates_formatted'] = df_ai['crawled_at']
            
            # Extract salary_numeric
            def extract_salary_num(s):
                if pd.isna(s) or s == 'Negotiable' or 'Negotiable' in str(s):
                    return None
                nums = re.findall(r'(\d+)', str(s))
                if nums:
                    return sum([int(n) for n in nums]) / len(nums) * 1_000_000
                return None
            
            df_processed['salary_numeric'] = df_ai['salary'].apply(extract_salary_num)
            
            # Normalize cities
            city_map = {
                'Hồ Chí Minh': 'Ho Chi Minh',
                'Hà Nội': 'Ha Noi',
                'Đà Nẵng': 'Da Nang',
                'Cần Thơ': 'Can Tho',
                'Hải Phòng': 'Hai Phong'
            }
            df_processed['city'] = df_ai['city'].replace(city_map)
            df_processed['level'] = df_ai['level']
            df_processed['job_group'] = df_ai['job_title'].str.split(' ').str[0]
            
            # Load existing data
            if main_file.exists():
                df_main = pd.read_csv(main_file)
                logger.info(f"  ✓ Data hiện có: {len(df_main)} jobs")
                
                # Merge
                df_merged = pd.concat([df_main, df_processed], ignore_index=True)
                df_merged = df_merged.drop_duplicates(subset=['job_names', 'company_names'], keep='first')
                
                logger.info(f"  ✓ Tổng sau gộp: {len(df_merged)} jobs (thêm {len(df_merged) - len(df_main)} jobs mới)")
            else:
                df_merged = df_processed
                logger.info(f"  ✓ Tạo mới data: {len(df_merged)} jobs")
            
            # Save
            df_merged.to_csv(main_file, index=False, encoding='utf-8-sig')
            logger.info(f"  💾 Đã lưu: {main_file}")
            logger.info("  🎯 Dashboard sẽ tự động dùng data mới!")
            
        except Exception as e:
            logger.error(f"❌ Lỗi khi merge: {e}")


async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Crawler THẬT - Crawl từ ITViec.vn')
    parser.add_argument('--jobs', type=int, default=50, 
                       help='Số lượng jobs cần crawl (default: 50)')
    parser.add_argument('--quick', action='store_true', 
                       help='Demo nhanh với 20 jobs')
    args = parser.parse_args()
    
    num_jobs = 20 if args.quick else args.jobs
    
    print("\n" + "="*70)
    print("🤖 AI CRAWLER THẬT - CRAWL DATA THỰC TỪ WEB")
    print("="*70)
    print(f"Mục tiêu: Crawl {num_jobs} jobs THẬT từ ITViec.vn")
    print(f"Phương thức: AI tự vào web, tự điều hướng, tự trích xuất")
    print(f"⏱️ Thời gian: ~10-15 phút")
    print(f"💰 Chi phí: ~${0.005 * num_jobs:.2f}")
    print("="*70 + "\n")
    
    try:
        # Initialize crawler
        crawler = RealAICrawler()
        
        # Crawl with AI
        jobs = await crawler.crawl_with_ai(num_jobs=num_jobs)
        
        if len(jobs) == 0:
            logger.error("\n❌ Không crawl được data")
            logger.info("\n💡 Nguyên nhân có thể:")
            logger.info("   1. API key hết hạn/không hợp lệ")
            logger.info("   2. Model không đủ mạnh (thử gpt-4)")
            logger.info("   3. Website thay đổi cấu trúc")
            logger.info("   4. Thiếu thư viện browser-use")
            return
        
        # Save results
        df = crawler.save_results()
        
        # Auto merge
        crawler.auto_merge_to_main()
        
        # Show statistics
        print("\n" + "="*70)
        print("📊 THỐNG KÊ DỮ LIỆU (DATA THẬT TỪ WEB)")
        print("="*70)
        
        print(f"\n🔢 Tổng quan:")
        print(f"   • Tổng jobs crawled: {len(df)}")
        print(f"   • Công ty: {df['company_name'].nunique()}")
        print(f"   • Thành phố: {df['city'].nunique()}")
        
        print(f"\n🏙️ Top 5 Cities:")
        for city, count in df['city'].value_counts().head(5).items():
            print(f"   • {city}: {count} jobs")
        
        print(f"\n🏢 Top 5 Companies:")
        for company, count in df['company_name'].value_counts().head(5).items():
            print(f"   • {company}: {count} jobs")
        
        # Show sample
        print(f"\n📋 MẪU 5 JOBS ĐẦU TIÊN (DATA THẬT):")
        print("="*70)
        sample_cols = ['job_title', 'company_name', 'salary', 'level', 'city']
        print(df[sample_cols].head().to_string(index=False))
        
        print("\n" + "="*70)
        print("✅ HOÀN THÀNH CRAWL THẬT!")
        print("="*70)
        print(f"📊 Đã crawl: {len(df)} jobs THẬT từ ITViec.vn")
        print(f"💾 Data đã gộp vào: data_clean/clean_data.csv")
        print(f"🔄 Refresh dashboard để xem data mới")
        print()
        
    except ValueError as e:
        logger.error(f"\n{e}")
    except Exception as e:
        logger.error(f"\n❌ Lỗi: {e}")
        logger.info("\n📝 Debug:")
        logger.info("   1. Check .env có OPENAI_API_KEY chưa")
        logger.info("   2. Cài: pip install browser-use langchain-openai playwright")
        logger.info("   3. playwright install chromium")


if __name__ == "__main__":
    asyncio.run(main())
