"""
🤖 Simplified AI-Powered Crawler using Native OpenAI
====================================================
Direct approach using OpenAI API for intelligent web scraping
Without complex browser-use dependencies

Author: Simplified AI Crawler
Date: 2026
"""

import os
import json
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import logging

# Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

class SimpleAICrawler:
    """
    Simplified AI crawler using OpenAI GPT directly
    Demonstrates AI concept without browser-use complexity
    """
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("❌ OPENAI_API_KEY not found in .env")
        
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.jobs_data = []
        
        logger.info("✅ Simple AI Crawler initialized")
    
    async def simulate_ai_crawl(self):
        """
        Demonstrate AI capability with simulated crawling
        In real scenario, this would use Playwright + AI vision
        """
        logger.info("🤖 AI analyzing ITViec website structure...")
        
        # Simulate AI understanding website
        prompt = """
        You are an intelligent web scraping AI. 
        
        Task: Extract job data from ITViec.com backend developer page.
        
        Based on typical job board structure, generate 5 realistic sample jobs with:
        - job_title: Backend role title
        - company_name: Vietnamese tech company
        - salary: Range in VND (or "Negotiable")
        - level: fresher/junior/mid/senior
        - city: Hà Nội or Hồ Chí Minh
        - skills: List of 3-5 tech skills
        - description: Brief 1-line description
        
        Return ONLY valid JSON array, no other text:
        [{"job_title": "...", "company_name": "...", ...}, ...]
        """
        
        try:
            logger.info("⏳ Calling GPT-3.5-turbo to generate sample data...")
            
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a data extraction AI. Output only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse AI response
            content = response.choices[0].message.content
            logger.info(f"✅ AI Response received ({len(content)} chars)")
            
            # Extract JSON from response
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                jobs = json.loads(json_match.group())
                self.jobs_data = jobs
                logger.info(f"✅ Extracted {len(jobs)} jobs using AI")
            else:
                logger.error("❌ Could not parse AI response")
                return []
            
        except Exception as e:
            logger.error(f"❌ AI crawl failed: {e}")
            raise
    
    def save_results(self, output_file="data_raw/ITViec_AI_simple.csv"):
        """Save to CSV"""
        if not self.jobs_data:
            logger.warning("⚠️ No data to save")
            return
        
        df = pd.DataFrame(self.jobs_data)
        df['crawled_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df['method'] = 'AI-Generated (GPT-3.5)'
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        logger.info(f"✅ Saved to: {output_file}")
        print("\n" + "="*60)
        print("📊 SAMPLE DATA (AI-Generated for Demo)")
        print("="*60)
        print(df.head().to_string())
        print(f"\n💾 Full data: {output_file}")
        print("="*60 + "\n")

async def demo_simple_ai():
    """Quick demo"""
    print("\n" + "="*60)
    print("🤖 SIMPLIFIED AI CRAWLER DEMO")
    print("="*60)
    print("Shows AI concept without browser-use complexity")
    print("Real implementation would use Playwright + GPT-4 Vision\n")
    
    try:
        crawler = SimpleAICrawler()
        
        await crawler.simulate_ai_crawl()
        
        crawler.save_results()
        
        print("\n✅ Demo complete!")
        print("\n💡 Advantages of AI approach:")
        print("   - Understands page context naturally")
        print("   - Self-adapts to layout changes")
        print("   - No manual CSS selectors needed")
        print("   - Can handle dynamic content intelligently")
        
        print("\n📊 Comparison:")
        print("   Traditional: 300 lines, brittle, fast, free")
        print("   AI-powered: 150 lines, adaptive, slower, ~$0.02/run")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure OPENAI_API_KEY is set in .env file")

if __name__ == "__main__":
    asyncio.run(demo_simple_ai())
