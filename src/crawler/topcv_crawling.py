"""
TopCV Job Crawler
Web scraper for TopCV.vn job listings
"""
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
from config.config import DATA_RAW_DIR


class TopCVCrawler:
    """Crawler for TopCV.vn"""
    
    def __init__(self):
        self.base_url = "https://www.topcv.vn"
        self.driver = None
        self.jobs_data = []
        
    def init_driver(self):
        """Initialize Chrome driver with options"""
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        options.add_argument('--disable-notifications')
        options.add_argument('--lang=vi-VN')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()
        print("✓ Chrome driver initialized")
        
    def search_jobs(self, keyword="IT", location="", page=1):
        """Search for jobs"""
        search_url = f"{self.base_url}/tim-viec-lam-{keyword.lower().replace(' ', '-')}"
        if location:
            search_url += f"-tai-{location}"
        search_url += f"?page={page}"
        
        print(f"Searching: {search_url}")
        self.driver.get(search_url)
        time.sleep(random.uniform(2, 4))
        
    def crawl_jobs(self, keyword="IT", max_pages=5):
        """Crawl multiple pages of job listings"""
        print(f"\n{'='*70}")
        print(f"Starting TopCV crawler - Keyword: {keyword}")
        print(f"{'='*70}\n")
        
        self.init_driver()
        
        for page in range(1, max_pages + 1):
            print(f"\n📄 Page {page}/{max_pages}")
            
            try:
                self.search_jobs(keyword=keyword, page=page)
                
                # Wait for job listings to load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "job-item-default"))
                )
                
                # Get job cards
                job_cards = self.driver.find_elements(By.CLASS_NAME, "job-item-default")
                print(f"  Found {len(job_cards)} jobs")
                
                for idx, card in enumerate(job_cards, 1):
                    try:
                        job_data = self._extract_job_data(card)
                        if job_data:
                            self.jobs_data.append(job_data)
                            print(f"  ✓ Extracted job {idx}: {job_data['job_title'][:50]}")
                    except Exception as e:
                        print(f"  ✗ Error extracting job {idx}: {e}")
                        continue
                
                time.sleep(random.uniform(3, 5))
                
            except TimeoutException:
                print(f"  ⚠️  Timeout on page {page}")
                continue
            except Exception as e:
                print(f"  ❌ Error on page {page}: {e}")
                continue
        
        self.driver.quit()
        print(f"\n✅ Crawling completed! Total jobs: {len(self.jobs_data)}")
        
    def _extract_job_data(self, card):
        """Extract data from a job card"""
        try:
            # Job title
            title_elem = card.find_element(By.CSS_SELECTOR, ".title a")
            job_title = title_elem.text.strip()
            job_url = title_elem.get_attribute("href")
            
            # Company name
            try:
                company = card.find_element(By.CSS_SELECTOR, ".company a").text.strip()
            except:
                company = "N/A"
            
            # Salary
            try:
                salary = card.find_element(By.CSS_SELECTOR, ".salary").text.strip()
            except:
                salary = "Thỏa thuận"
            
            # Location
            try:
                location = card.find_element(By.CSS_SELECTOR, ".label-content").text.strip()
            except:
                location = "N/A"
            
            # Posted date
            try:
                posted_date = card.find_element(By.CSS_SELECTOR, ".time").text.strip()
            except:
                posted_date = datetime.now().strftime("%Y-%m-%d")
            
            return {
                'job_title': job_title,
                'company': company,
                'salary': salary,
                'location': location,
                'posted_date': posted_date,
                'url': job_url,
                'source': 'TopCV',
                'crawled_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            print(f"    Error extracting job data: {e}")
            return None
    
    def save_to_csv(self, filename="TopCV_data.csv"):
        """Save crawled data to CSV"""
        if not self.jobs_data:
            print("⚠️  No data to save")
            return
        
        df = pd.DataFrame(self.jobs_data)
        filepath = Path(DATA_RAW_DIR) / filename
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        
        print(f"\n💾 Saved {len(df)} jobs to: {filepath}")
        print(f"\nData preview:")
        print(df.head())
        print(f"\nColumns: {list(df.columns)}")


def main():
    """Run TopCV crawler"""
    crawler = TopCVCrawler()
    
    # Crawl IT jobs
    crawler.crawl_jobs(keyword="IT", max_pages=3)
    
    # Save to CSV
    crawler.save_to_csv()


if __name__ == "__main__":
    main()
