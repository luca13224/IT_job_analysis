"""
🎭 AI Crawler Demo (Enhanced Mock Version - Nhiều data realistic hơn)
===================================================================
Mô phỏng AI crawl với 50-200 jobs từ 50+ công ty, 6 job types

🚀 CÁCH DÙNG:
    python src/crawler/ITViec_AI_demo_v2.py             # 100 jobs (mặc định)
    python src/crawler/ITViec_AI_demo_v2.py --jobs 200  # 200 jobs
    python src/crawler/ITViec_AI_demo_v2.py --quick     # 10 jobs (demo nhanh)

💾 OUTPUT:
    - data_raw/ITViec_AI_demo.csv
    - Tự động gộp vào data_clean/clean_data.csv
"""

import pandas as pd
from datetime import datetime
import time
import random
import logging
import re
from pathlib import Path
import sys
import io

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class AIJobCrawler:
    """AI-powered crawler với nhiều data realistic"""
    
    def __init__(self):
        self.jobs_data = []
        self.setup_data_sources()
        
    def setup_data_sources(self):
        """Setup danh sách công ty, skills, cities..."""
        # 50+ công ty nổi tiếng VN
        self.companies = [
            "VNG Corporation", "FPT Software", "Viettel Solutions", "MOMO", "Tiki",
            "Shopee Vietnam", "Grab Vietnam", "Zalo", "VinID", "TechComBank",
            "VPBank Digital", "Be Group", "Sendo", "Teko", "The Gioi Di Dong",
            "VinBrain", "VinBigData", "Sun Asterisk", "KMS Technology", "NashTech",
            "CMC Corporation", "FPT Telecom", "Viettel Post", "GHN Express", "Ninja Van",
            "GoViet", "Foody", "Lozi", "Chotot", "5giay.vn",
            "VNLife", "VNPay", "Moca", "AirPay", "ShopeePay",
            "Lazada", "Adayroi", "Vatgia", "123job", "CareerLink",
            "Samsung Vietnam", "LG Electronics", "Bosch Vietnam", "Siemens",
            "BKAV", "Kaspersky Vietnam", "FPT IS", "Viettel Cyber Security",
            "Shopee Vietnam", "TikTok Vietnam", "Meta Vietnam"
        ]
        
        # 6 job types với skills riêng
        self.job_templates = {
            "Backend Developer": {
                "skills": [
                    ["Python", "Django", "PostgreSQL", "Docker", "AWS"],
                    ["Java", "Spring Boot", "MySQL", "Kubernetes", "Git"],
                    ["Node.js", "Express", "MongoDB", "Redis", "CI/CD"],
                    ["Go", "Microservices", "gRPC", "Kafka", "Docker"],
                    ["PHP", "Laravel", "MySQL", "Redis", "Linux"],
                    ["C#", ".NET Core", "SQL Server", "Azure", "Docker"],
                ],
                "specializations": ["Product", "Platform", "Core", "API", "Service", "Cloud"]
            },
            "Frontend Developer": {
                "skills": [
                    ["React", "TypeScript", "Redux", "Webpack", "Git"],
                    ["Vue.js", "Vuex", "JavaScript", "Sass", "NPM"],
                    ["Angular", "TypeScript", "RxJS", "NgRx", "Git"],
                    ["HTML5", "CSS3", "JavaScript", "Bootstrap", "jQuery"],
                ],
                "specializations": ["UI", "Web", "Product", "Platform"]
            },
            "Fullstack Developer": {
                "skills": [
                    ["React", "Node.js", "MongoDB", "Docker", "Git"],
                    ["Vue.js", "Python", "PostgreSQL", "Redis", "Linux"],
                    ["Angular", "Java", "MySQL", "Kubernetes", "CI/CD"],
                ],
                "specializations": ["Product", "Web", "Platform", "SaaS"]
            },
            "Mobile Developer": {
                "skills": [
                    ["React Native", "JavaScript", "Redux", "Firebase", "Git"],
                    ["Flutter", "Dart", "Firebase", "REST API", "Git"],
                    ["iOS", "Swift", "SwiftUI", "CoreData", "Xcode"],
                    ["Android", "Kotlin", "Jetpack", "Room", "Git"],
                ],
                "specializations": ["iOS", "Android", "App", "Native", "Hybrid"]
            },
            "Data Engineer": {
                "skills": [
                    ["Python", "Pandas", "NumPy", "SQL", "Jupyter"],
                    ["Spark", "Scala", "Hadoop", "Hive", "Kafka"],
                    ["R", "ggplot2", "dplyr", "Shiny", "SQL"],
                    ["TensorFlow", "PyTorch", "Scikit-learn", "Keras", "Python"],
                ],
                "specializations": ["Pipeline", "Analytics", "Platform", "BI", "ML"]
            },
            "DevOps Engineer": {
                "skills": [
                    ["Docker", "Kubernetes", "Jenkins", "Terraform", "AWS"],
                    ["GitLab CI", "Ansible", "Prometheus", "Grafana", "Linux"],
                    ["Azure DevOps", "PowerShell", "ARM Templates", "Azure"],
                ],
                "specializations": ["Infrastructure", "Cloud", "Platform", "SRE", "CI/CD"]
            }
        }
        
        # Levels với weighting
        self.levels = ["fresher", "junior", "mid", "senior", "lead", "manager"]
        self.level_weights = [0.1, 0.2, 0.35, 0.25, 0.07, 0.03]
        
        # Cities với weighting (HCM, HN nhiều nhất)
        self.cities = ["Hồ Chí Minh", "Hà Nội", "Đà Nẵng", "Cần Thơ", "Hải Phòng", "Nha Trang"]
        self.city_weights = [0.45, 0.40, 0.10, 0.03, 0.015, 0.005]
        
        # Salaries theo level
        self.salary_ranges = {
            "low": ["15-20 triệu VND", "20-25 triệu VND", "20-30 triệu VND", "25-30 triệu VND"],
            "mid": ["25-35 triệu VND", "30-40 triệu VND", "35-45 triệu VND", "40-50 triệu VND"],
            "high": ["45-60 triệu VND", "50-70 triệu VND", "60-80 triệu VND", "Negotiable", "Up to 70 triệu VND"]
        }
        
        # Descriptions
        self.descriptions = {
            "Backend Developer": "Xây dựng hệ thống backend mở rộng cho hàng triệu người dùng",
            "Frontend Developer": "Phát triển giao diện người dùng tương tác cao với React/Vue",
            "Fullstack Developer": "Phát triển full-stack từ frontend đến backend và database",
            "Mobile Developer": "Xây dựng ứng dụng mobile native/hybrid cho iOS/Android",
            "Data Engineer": "Xây dựng data pipeline và xử lý dữ liệu quy mô lớn",
            "DevOps Engineer": "Quản lý infrastructure, CI/CD và cloud platform"
        }
        
    def simulate_ai_thinking(self):
        """Simulate AI crawling process"""
        steps = [
            "🧠 AI đang phân tích cấu trúc trang ITViec.com...",
            "📝 Nhận diện patterns: job cards, company info, salary...",
            "🔍 Xác định các trường dữ liệu cần extract...",
            "🎯 Áp dụng NLP để hiểu job descriptions...",
            "✨ Bắt đầu trích xuất jobs thông minh..."
        ]
        
        for step in steps:
            logger.info(step)
            time.sleep(0.4)
            
    def crawl_jobs(self, num_jobs=100):
        """Mô phỏng AI crawl nhiều jobs"""
        logger.info(f"\n🤖 AI đang crawl {num_jobs} jobs từ ITViec.com...")
        
        for i in range(num_jobs):
            # Random chọn job type
            job_type = random.choice(list(self.job_templates.keys()))
            template = self.job_templates[job_type]
            
            # Level (weighted)
            level = random.choices(self.levels, weights=self.level_weights)[0]
            
            # City (weighted - HCM, HN nhiều hơn)
            city = random.choices(self.cities, weights=self.city_weights)[0]
            
            # Salary theo level
            if level in ["fresher", "junior"]:
                salary = random.choice(self.salary_ranges["low"])
            elif level in ["mid"]:
                salary = random.choice(self.salary_ranges["mid"])
            else:
                salary = random.choice(self.salary_ranges["high"])
            
            # Skills và specialization
            skills = random.choice(template["skills"])
            spec = random.choice(template["specializations"])
            
            job = {
                "job_title": f"{job_type} - {spec}",
                "company_name": random.choice(self.companies),
                "salary": salary,
                "level": level,
                "city": city,
                "skills": skills,
                "description": self.descriptions[job_type],
                "crawled_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "method": "AI-Powered Mock v2"
            }
            
            self.jobs_data.append(job)
            
            # Progress indicator (mỗi 20 jobs)
            if (i + 1) % 20 == 0:
                logger.info(f"  ✓ Đã crawl {i + 1}/{num_jobs} jobs...")
        
        logger.info(f"✅ Hoàn thành! Đã crawl {len(self.jobs_data)} jobs")
        
    def save_results(self):
        """Save crawled data"""
        # Convert skills list to string
        for job in self.jobs_data:
            job['skills'] = str(job['skills'])
        
        df = pd.DataFrame(self.jobs_data)
        
        # Save to data_raw/
        output_path = Path(__file__).parent.parent.parent / "data_raw" / "ITViec_AI_demo.csv"
        output_path.parent.mkdir(exist_ok=True)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        logger.info(f"\n💾 Đã lưu vào: {output_path}")
        return df
        
    def auto_merge_to_main(self):
        """Tự động gộp vào data_clean/clean_data.csv"""
        try:
            project_root = Path(__file__).parent.parent.parent
            ai_file = project_root / "data_raw" / "ITViec_AI_demo.csv"
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
            df_processed['job_group'] = df_ai['job_title'].str.split(' - ').str[0]
            
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


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Crawler - Enhanced Mock Version')
    parser.add_argument('--jobs', type=int, default=100, 
                       help='Số lượng jobs cần crawl (default: 100)')
    parser.add_argument('--quick', action='store_true', 
                       help='Demo nhanh với 10 jobs')
    args = parser.parse_args()
    
    num_jobs = 10 if args.quick else args.jobs
    
    print("\n" + "="*70)
    print("🤖 AI CRAWLER - MÔ PHỎNG CRAWL THẬT (v2)")
    print("="*70)
    print(f"Mục tiêu: Crawl {num_jobs} jobs từ ITViec.com")
    print(f"Data: 50+ công ty, 6 job types, realistic skills & salaries")
    print("="*70 + "\n")
    
    # Initialize crawler
    crawler = AIJobCrawler()
    
    # Simulate AI thinking
    crawler.simulate_ai_thinking()
    
    # Crawl jobs
    print()
    crawler.crawl_jobs(num_jobs=num_jobs)
    
    # Save results
    df = crawler.save_results()
    
    # Auto merge
    crawler.auto_merge_to_main()
    
    # Show statistics
    print("\n" + "="*70)
    print("📊 THỐNG KÊ DỮ LIỆU")
    print("="*70)
    
    print(f"\n🔢 Tổng quan:")
    print(f"   • Tổng jobs: {len(df)}")
    print(f"   • Công ty: {df['company_name'].nunique()}")
    print(f"   • Thành phố: {df['city'].nunique()}")
    
    print(f"\n📊 Phân bố Job Types:")
    job_types = df['job_title'].str.split(' - ').str[0].value_counts()
    for jt, count in job_types.items():
        pct = count / len(df) * 100
        print(f"   • {jt}: {count} jobs ({pct:.1f}%)")
    
    print(f"\n🏙️ Phân bố Cities:")
    for city, count in df['city'].value_counts().head(5).items():
        pct = count / len(df) * 100
        print(f"   • {city}: {count} jobs ({pct:.1f}%)")
    
    print(f"\n📈 Phân bố Levels:")
    for level, count in df['level'].value_counts().items():
        pct = count / len(df) * 100
        print(f"   • {level}: {count} jobs ({pct:.1f}%)")
    
    # Show sample
    print(f"\n📋 MẪU 5 JOBS ĐẦU TIÊN:")
    print("="*70)
    sample_cols = ['job_title', 'company_name', 'salary', 'level', 'city']
    print(df[sample_cols].head().to_string(index=False))
    
    print("\n" + "="*70)
    print("✅ HOÀN THÀNH!")
    print("="*70)
    print(f"📊 Đã crawl: {len(df)} jobs")
    print(f"💾 Data đã gộp vào: data_clean/clean_data.csv")
    print(f"🔄 Refresh dashboard để xem data mới")
    print(f"\n💡 Tips:")
    print(f"   • Crawl nhiều hơn: --jobs 200")
    print(f"   • Demo nhanh: --quick")
    print()


if __name__ == "__main__":
    main()
