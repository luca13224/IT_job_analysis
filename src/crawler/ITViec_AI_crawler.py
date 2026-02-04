"""
🤖 AI-Powered ITViec Job Crawler using Browser Use
==================================================
This crawler uses LLM (GPT-4/Claude) to automatically extract job data
from ITViec.vn without manual CSS selectors.

Key differences from traditional Selenium:
- AI agent understands the page and finds elements automatically
- More resilient to website layout changes
- Natural language task descriptions
- Self-healing when page structure changes

Author: AI-Enhanced Crawler
Date: 2026
"""

import os
import asyncio
import pandas as pd
from datetime import datetime
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


# ==========================
# LLM WRAPPER FOR BROWSER USE
# ==========================
class BrowserUseLLM:
    """
    Wrapper to make ChatOpenAI compatible with browser-use
    Pass through all required attributes
    """
    def __init__(self, model="gpt-3.5-turbo", api_key=None):
        self.model = model
        self.model_name = model  # Required by browser-use
        self.api_key = api_key
        self.provider = "openai"  # Required by browser-use
        
        self._llm = ChatOpenAI(
            model=model,
            temperature=0,
            openai_api_key=api_key
        )
    
    def __getattr__(self, name):
        """Pass through any missing attributes to underlying LLM"""
        return getattr(self._llm, name)
    
    async def __call__(self, *args, **kwargs):
        """Make the wrapper callable"""
        return await self._llm.ainvoke(*args, **kwargs)
    
    def invoke(self, *args, **kwargs):
        """Sync invoke"""
        return self._llm.invoke(*args, **kwargs)
    
    async def ainvoke(self, *args, **kwargs):
        """Async invoke"""
        return await self._llm.ainvoke(*args, **kwargs)
    
    def bind(self, **kwargs):
        """Bind additional parameters"""
        return self._llm.bind(**kwargs)
    
    def with_structured_output(self, *args, **kwargs):
        """Support structured output"""
        return self._llm.with_structured_output(*args, **kwargs)

class ITViecAICrawler:
    """
    AI-powered crawler for ITViec.vn using Browser Use library.
    
    Features:
    - LLM-driven element detection
    - Automatic pagination handling
    - Self-adaptive to layout changes
    - Natural language task definition
    """
    
    def __init__(self, api_key=None, model="gpt-3.5-turbo", output_file="data_raw/ITViec_data_AI.csv"):
        """
        Initialize AI crawler
        
        Args:
            api_key: OpenAI API key (will use env var if not provided)
            model: LLM model to use (gpt-4, gpt-4-turbo, gpt-3.5-turbo)
            output_file: Path to save crawled data
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("❌ OpenAI API key not found! Set OPENAI_API_KEY in .env file")
        
        self.model = model
        self.output_file = output_file
        self.jobs_data = []
        
        # Initialize LLM with browser-use compatible wrapper
        self.llm = BrowserUseLLM(
            model=model,
            api_key=self.api_key
        )
        
        logger.info(f"✅ AI Crawler initialized with {model}")
    
    async def crawl_jobs(self, job_keyword="Backend Developer", max_pages=3):
        """
        Main crawling function using AI agent
        
        Args:
            job_keyword: Search keyword for jobs
            max_pages: Maximum pages to crawl (default: 3 for demo)
        """
        logger.info(f"🚀 Starting AI crawl for: {job_keyword}")
        logger.info(f"📄 Max pages: {max_pages}")
        
        # Define task in natural language
        task = f"""
        Go to ITViec.com website and extract job listings data.
        
        Steps:
        1. Navigate to https://itviec.com/it-jobs
        2. Search for "{job_keyword}" jobs
        3. For each job listing on the page, extract:
           - Job title
           - Company name
           - Salary information (if available, otherwise "Negotiable")
           - Experience level (Fresher/Junior/Mid/Senior)
           - Location/City
           - Required skills (as a list)
           - Job description snippet
        4. Move to next page and repeat until you've processed {max_pages} pages
        5. Return all extracted data in a structured format
        
        Important:
        - Handle cases where salary is not displayed
        - Extract all visible skill tags
        - Skip any sponsored/featured ads that aren't real jobs
        - If login popup appears, close it
        """
        
        try:
            from browser_use import Agent
            
            # Create AI agent with wrapped LLM
            agent = Agent(
                task=task,
                llm=self.llm
            )
            
            # Run agent
            logger.info("🤖 AI Agent is working...")
            result = await agent.run()
            
            # Process results  
            self._process_ai_results(result)
            
            logger.info(f"✅ Crawl completed! Found {len(self.jobs_data)} jobs")
            
        except Exception as e:
            logger.error(f"❌ Crawl failed: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            raise
    
    def _process_ai_results(self, result):
        """
        Process and structure the AI agent's results
        
        Args:
            result: Raw result from Browser Use agent
        """
        logger.info("📊 Processing AI extracted data...")
        
        # Browser Use returns results in its own format
        # We need to extract and structure it
        try:
            # The agent should return structured data
            # Parse and convert to our format
            if hasattr(result, 'extracted_data'):
                raw_jobs = result.extracted_data
            else:
                # If result is a dict or list directly
                raw_jobs = result if isinstance(result, (list, dict)) else []
            
            # Convert to our standard format
            for job in raw_jobs:
                job_entry = {
                    'job_names': job.get('title', 'N/A'),
                    'company_names': job.get('company', 'N/A'),
                    'salary': job.get('salary', 'Negotiable'),
                    'level': job.get('level', 'N/A'),
                    'city': job.get('location', 'N/A'),
                    'skills': str(job.get('skills', [])),
                    'job_description': job.get('description', 'N/A'),
                    'crawled_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'crawl_method': 'AI-Powered (Browser Use)'
                }
                self.jobs_data.append(job_entry)
            
            logger.info(f"✅ Processed {len(self.jobs_data)} jobs")
            
        except Exception as e:
            logger.error(f"⚠️ Error processing results: {str(e)}")
            # Log raw result for debugging
            logger.debug(f"Raw result: {result}")
    
    def save_to_csv(self):
        """Save crawled data to CSV file"""
        if not self.jobs_data:
            logger.warning("⚠️ No data to save!")
            return
        
        try:
            df = pd.DataFrame(self.jobs_data)
            
            # Create directory if not exists
            os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
            
            # Save to CSV
            df.to_csv(self.output_file, index=False, encoding='utf-8-sig')
            logger.info(f"✅ Data saved to: {self.output_file}")
            logger.info(f"📊 Total jobs: {len(self.jobs_data)}")
            
            # Show sample
            logger.info("\n📋 Sample data:")
            print(df.head(3).to_string())
            
        except Exception as e:
            logger.error(f"❌ Failed to save data: {str(e)}")
            raise
    
    def get_statistics(self):
        """Print crawling statistics"""
        if not self.jobs_data:
            logger.info("No data available")
            return
        
        df = pd.DataFrame(self.jobs_data)
        
        print("\n" + "="*50)
        print("📊 CRAWLING STATISTICS")
        print("="*50)
        print(f"Total Jobs: {len(df)}")
        print(f"\nTop 5 Companies:")
        print(df['company_names'].value_counts().head())
        print(f"\nJobs by Level:")
        print(df['level'].value_counts())
        print(f"\nJobs by City:")
        print(df['city'].value_counts())
        print("="*50 + "\n")


# ==========================
# QUICK DEMO FUNCTION
# ==========================
async def demo_ai_crawler():
    """
    Quick demo function to test AI crawler
    Usage: python ITViec_AI_crawler.py
    """
    print("\n" + "="*60)
    print("🤖 AI-POWERED ITVIEC CRAWLER DEMO")
    print("="*60)
    print("This crawler uses GPT-4 to intelligently extract job data")
    print("No manual CSS selectors needed!\n")
    
    try:
        # Initialize crawler with GPT-3.5 (cheaper)
        crawler = ITViecAICrawler(
            model="gpt-3.5-turbo",  # Changed from gpt-4 to save costs
            output_file="data_raw/ITViec_data_AI.csv"
        )
        
        # Crawl jobs (limited pages for demo)
        await crawler.crawl_jobs(
            job_keyword="Backend Developer",
            max_pages=2  # Start with 2 pages for demo
        )
        
        # Save results
        crawler.save_to_csv()
        
        # Show statistics
        crawler.get_statistics()
        
        print("\n✅ Demo completed successfully!")
        print("💡 To crawl more pages, increase max_pages parameter")
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {str(e)}")
        print("\n📝 Setup Instructions:")
        print("1. Create a .env file in project root")
        print("2. Add your OpenAI API key: OPENAI_API_KEY=sk-...")
        print("3. Get API key from: https://platform.openai.com/api-keys")
        
    except Exception as e:
        print(f"\n❌ Crawl failed: {str(e)}")
        print("💡 Check your internet connection and API key")


# ==========================
# COMPARISON FUNCTION
# ==========================
def compare_with_traditional():
    """
    Compare AI crawler vs Traditional Selenium crawler
    """
    print("\n" + "="*60)
    print("⚖️  AI CRAWLER vs TRADITIONAL CRAWLER")
    print("="*60)
    
    comparison = """
    ┌─────────────────────┬─────────────────────┬─────────────────────┐
    │      Feature        │   Traditional       │    AI-Powered       │
    ├─────────────────────┼─────────────────────┼─────────────────────┤
    │ Code Length         │ ~300 lines          │ ~150 lines          │
    │ CSS Selectors       │ Manual (brittle)    │ Auto (AI finds)     │
    │ Layout Changes      │ Breaks easily       │ Self-adaptive       │
    │ Setup Complexity    │ Medium              │ Easy                │
    │ Speed               │ Fast                │ Slower (LLM calls)  │
    │ Cost                │ Free                │ API costs (~$0.50)  │
    │ Maintainability     │ High effort         │ Low effort          │
    │ Intelligence        │ Dumb (rule-based)   │ Smart (understands) │
    └─────────────────────┴─────────────────────┴─────────────────────┘
    
    💡 Use AI crawler when:
    - Website layout changes frequently
    - You need to scrape multiple similar sites
    - Demo/presentation needs "AI" factor
    - Maintenance time is limited
    
    💡 Use Traditional when:
    - Cost is a concern
    - Speed is critical
    - Website structure is stable
    - Offline/local execution needed
    """
    
    print(comparison)


# ==========================
# MAIN EXECUTION
# ==========================
if __name__ == "__main__":
    print("\n🚀 Starting AI Crawler...")
    
    # Check for .env file
    if not os.path.exists('.env'):
        print("\n⚠️  No .env file found!")
        print("Creating .env.example template...")
        
        with open('.env.example', 'w') as f:
            f.write("# OpenAI API Configuration\n")
            f.write("OPENAI_API_KEY=sk-your-api-key-here\n\n")
            f.write("# Get your API key from: https://platform.openai.com/api-keys\n")
            f.write("# Then rename this file to .env\n")
        
        print("✅ Created .env.example")
        print("📝 Please:")
        print("   1. Rename .env.example to .env")
        print("   2. Add your OpenAI API key")
        print("   3. Run again\n")
    else:
        # Run demo
        asyncio.run(demo_ai_crawler())
        
        # Show comparison
        compare_with_traditional()
