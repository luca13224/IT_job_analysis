"""
🎭 AI Crawler Demo (Mock Version - No API Needed)
==================================================
Demonstrates AI crawling concept without requiring OpenAI API
Perfect for presentation and understanding the approach

Author: Demo AI Crawler
Date: 2026
"""

import pandas as pd
from datetime import datetime
import time
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class MockAICrawler:
    """
    Mock AI crawler that demonstrates the concept
    without needing actual API calls
    """
    
    def __init__(self):
        self.jobs_data = []
        logger.info("✅ Khởi tạo AI Crawler Demo (Không cần API key)")
    
    def simulate_ai_thinking(self):
        """Simulate AI processing"""
        steps = [
            "🧠 AI đang phân tích cấu trúc trang ITViec.com...",
            "📝 Đang nhận diện các mẫu dữ liệu công việc...",
            "🔍 Xác định các trường: tiêu đề, công ty, lương, kỹ năng...",
            "🎯 Trích xuất thông tin thông minh...",
            "✨ Đang xử lý 10 việc làm Backend Developer...",
        ]
        
        for step in steps:
            logger.info(step)
            time.sleep(0.5)  # Simulate thinking time
    
    def generate_mock_data(self):
        """Generate realistic mock job data"""
        
        companies = [
            "VNG Corporation", "FPT Software", "Viettel Solutions",
            "MOMO", "Tiki", "Shopee Vietnam", "Grab Vietnam",
            "Zalo", "VinID", "TechComBank Digital"
        ]
        
        levels = ["fresher", "junior", "mid", "senior"]
        cities = ["Hồ Chí Minh", "Hà Nội", "Đà Nẵng"]
        
        skill_sets = [
            ["Python", "Django", "PostgreSQL", "Docker", "AWS"],
            ["Java", "Spring Boot", "MySQL", "Kubernetes", "Git"],
            ["Node.js", "Express", "MongoDB", "Redis", "CI/CD"],
            ["Go", "Microservices", "gRPC", "Kafka", "Docker"],
            ["PHP", "Laravel", "MySQL", "Redis", "Linux"]
        ]
        
        salaries = [
            "20-30 triệu VND",
            "30-40 triệu VND", 
            "40-60 triệu VND",
            "Negotiable",
            "Up to 50 triệu VND",
            "25-35 triệu VND"
        ]
        
        # Generate 10 jobs
        for i in range(10):
            job = {
                "job_title": f"Backend Developer - {random.choice(['Product', 'Platform', 'Core', 'API', 'Service'])}",
                "company_name": random.choice(companies),
                "salary": random.choice(salaries),
                "level": random.choice(levels),
                "city": random.choice(cities),
                "skills": random.choice(skill_sets),
                "description": "Xây dựng hệ thống backend mở rộng cho hàng triệu người dùng",
                "crawled_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "method": "AI-Powered (Demo)"
            }
            self.jobs_data.append(job)
        
        logger.info(f"✅ Đã tạo {len(self.jobs_data)} công việc bằng logic AI")
    
    def save_results(self, output_file="data_raw/ITViec_AI_demo.csv"):
        """Save mock data"""
        import os
        
        # Convert skills list to string for CSV
        for job in self.jobs_data:
            job['skills'] = str(job['skills'])
        
        df = pd.DataFrame(self.jobs_data)
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        logger.info(f"\n💾 Đã lưu vào: {output_file}")
        return df
    
    def show_comparison(self):
        """Show AI vs Traditional comparison"""
        print("\n" + "="*70)
        print("⚖️  SO SÁNH: AI CRAWLER vs CRAWLER TRUYỀN THỐNG")
        print("="*70)
        
        comparison = """
┌─────────────────────┬─────────────────────┬─────────────────────┐
│     Tiêu chí        │   Truyền thống      │    AI-Powered       │
├─────────────────────┼─────────────────────┼─────────────────────┤
│ Số dòng code        │ ~300 dòng           │ ~100 dòng           │
│ CSS Selectors       │ Thủ công (dễ lỗi)   │ Tự động (AI tìm)    │
│ Khi web đổi layout  │ Dễ bị lỗi           │ Tự thích nghi ✨    │
│ Độ phức tạp         │ Trung bình          │ Dễ dàng             │
│ Tốc độ             │ Nhanh (3 phút)      │ Chậm hơn (10 phút)  │
│ Chi phí            │ Miễn phí ✅         │ ~$0.50/100 jobs     │
│ Bảo trì            │ Tốn công sức        │ Ít công sức ✨      │
│ Độ thông minh      │ Dựa trên rule       │ Hiểu ngữ cảnh ✨    │
└─────────────────────┴─────────────────────┴─────────────────────┘

💡 Ưu điểm nổi bật của AI:
   ✅ Mô tả bằng ngôn ngữ tự nhiên: "Trích xuất công việc Backend từ ITViec"
   ✅ Không cần CSS selectors: AI hiểu cấu trúc trang web trực quan
   ✅ Tự sửa lỗi: Thích nghi khi website thay đổi giao diện
   ✅ Đa trang web: Cùng 1 AI dùng được cho nhiều trang tuyển dụng

💡 Khi nào dùng Truyền thống:
   • Cấu trúc web ổn định (ít thay đổi)
   • Cần crawl khối lượng lớn (10K+ jobs)
   • Ngân sách hạn chế (không tốn API)
   • Tốc độ là ưu tiên hàng đầu

💡 Khi nào dùng AI:
   • Website thay đổi giao diện thường xuyên
   • Cần demo dự án "AI-powered" cho thầy ✨
   • Thời gian bảo trì hạn chế
   • Crawl nhiều trang web khác nhau
"""
        print(comparison)
    
    def show_code_comparison(self):
        """Show code complexity difference"""
        print("\n" + "="*70)
        print("📝 SO SÁNH ĐỘ PHỨC TẠP CODE")
        print("="*70)
        
        print("\n🔴 SELENIUM TRUYỀN THỐNG (300 dòng):")
        print("""
# CSS selectors thủ công - dễ lỗi khi web thay đổi
driver.find_element(By.CSS_SELECTOR, ".job-title").text
driver.find_element(By.CLASS_NAME, "salary-info").text
driver.find_elements(By.CLASS_NAME, "skill-tag")

# Logic phân trang phức tạp
next_btn = driver.find_element(By.CSS_SELECTOR, "a.next-page")
if next_btn:
    next_btn.click()
    
# Phải xử lý lỗi từng element
try:
    salary = driver.find_element(By.CLASS_NAME, "salary").text
except NoSuchElementException:
    salary = "Thỏa thuận"
""")
        
        print("\n\n🟢 AI-POWERED (100 dòng):")
        print("""
# Ngôn ngữ tự nhiên - AI tự thích nghi
task = '''
Vào trang ITViec.com, tìm các công việc Backend.
Trích xuất: tiêu đề, công ty, lương, kỹ năng cho mỗi job.
Xử lý trường hợp không hiển thị lương.
'''

agent = Agent(task=task, llm=gpt4)
result = agent.run()  # AI làm tất cả! ✨
""")
        
        print("\n" + "="*70)
        print("💡 Cách tiếp cận AI ngắn gọn hơn 3 lần và tự sửa lỗi!")
        print("="*70 + "\n")


def main():
    """Main demo function"""
    print("\n" + "="*70)
    print("🤖 DEMO AI CRAWLER (PHIÊN BẢN MOCK)")
    print("="*70)
    print("Demo này minh họa khái niệm AI crawling mà không cần OpenAI API")
    print("Hoàn hảo cho bài thuyết trình và hiểu rõ cách tiếp cận")
    print("="*70 + "\n")
    
    crawler = MockAICrawler()
    
    # Simulate AI processing
    crawler.simulate_ai_thinking()
    
    # Generate mock data
    print()
    crawler.generate_mock_data()
    
    # Save results
    df = crawler.save_results()
    
    # Show sample data
    print("\n" + "="*70)
    print("📊 MẪU CÔNG VIỆC TRÍCH XUẤT BỞI AI")
    print("="*70)
    print(df[['job_title', 'company_name', 'salary', 'level', 'city']].head().to_string(index=False))
    
    # Show comparisons
    crawler.show_comparison()
    crawler.show_code_comparison()
    
    print("\n✅ Demo Hoàn Thành!")
    print("\n🎓 Hướng dẫn Thuyết trình:")
    print("   1. Trình bày output này để demo khái niệm AI")
    print("   2. Giải thích cách AI tự thích nghi khi web thay đổi")
    print("   3. So sánh với Selenium crawler truyền thống")
    print("   4. Nhấn mạnh: Không cần CSS selectors, tự sửa lỗi, ngôn ngữ tự nhiên")
    print("\n💾 Dữ liệu mock đã lưu tại: data_raw/ITViec_AI_demo.csv")
    print("🔄 Có thể tích hợp với dashboard hiện tại!")
    print()

if __name__ == "__main__":
    main()
