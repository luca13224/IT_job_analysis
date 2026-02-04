"""
🧪 Test All AI Crawlers - Quick Validation
==========================================
Chạy test nhanh cho tất cả crawlers
"""

import asyncio
import subprocess
import sys
from pathlib import Path
import pandas as pd

def run_command(cmd):
    """Run shell command"""
    print(f"\n{'='*70}")
    print(f"🚀 Running: {cmd}")
    print('='*70)
    
    result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
    return result.returncode == 0

async def main():
    print("\n" + "="*70)
    print("🧪 TESTING AI CRAWLERS")
    print("="*70)
    
    base_path = Path(__file__).parent
    
    # Check if files exist
    itviec_file = base_path / "ITViec_AI_groq.py"
    vietnamworks_file = base_path / "VietnamWorks_AI_groq.py"
    
    if not itviec_file.exists():
        print("❌ ITViec_AI_groq.py not found!")
        return
    
    if not vietnamworks_file.exists():
        print("❌ VietnamWorks_AI_groq.py not found!")
        return
    
    print("✅ All crawler files found")
    
    # Get initial job count
    clean_data_path = base_path.parent.parent / "data_clean" / "clean_data.csv"
    if clean_data_path.exists():
        df_before = pd.read_csv(clean_data_path)
        jobs_before = len(df_before)
        print(f"\n📊 Current jobs in clean_data.csv: {jobs_before}")
    else:
        jobs_before = 0
        print("\n⚠️ clean_data.csv not found")
    
    # Test 1: ITViec (3 jobs for quick test)
    print("\n" + "="*70)
    print("TEST 1: ITViec Crawler (3 jobs)")
    print("="*70)
    
    success1 = run_command(f"python {itviec_file} --jobs 3")
    
    if success1:
        print("✅ ITViec crawler SUCCESS")
    else:
        print("❌ ITViec crawler FAILED")
    
    # Wait a bit
    print("\n⏳ Waiting 10 seconds before next crawl...")
    await asyncio.sleep(10)
    
    # Test 2: VietnamWorks (5 jobs)
    print("\n" + "="*70)
    print("TEST 2: VietnamWorks Crawler (5 jobs)")
    print("="*70)
    
    success2 = run_command(f"python {vietnamworks_file} --jobs 5")
    
    if success2:
        print("✅ VietnamWorks crawler SUCCESS")
    else:
        print("❌ VietnamWorks crawler FAILED")
    
    # Check final results
    print("\n" + "="*70)
    print("📊 FINAL RESULTS")
    print("="*70)
    
    if clean_data_path.exists():
        df_after = pd.read_csv(clean_data_path)
        jobs_after = len(df_after)
        new_jobs = jobs_after - jobs_before
        
        print(f"\n✅ Before: {jobs_before} jobs")
        print(f"✅ After: {jobs_after} jobs")
        print(f"✅ Added: +{new_jobs} jobs")
        
        # Show sample
        if new_jobs > 0:
            print("\n📋 SAMPLE OF NEW JOBS:")
            recent = df_after.tail(new_jobs)
            print(recent[['job_names', 'company_names', 'city']].head(8).to_string(index=False))
    
    # Summary
    print("\n" + "="*70)
    print("✅ TESTING COMPLETE")
    print("="*70)
    
    if success1 and success2:
        print("\n🎉 ALL CRAWLERS WORKING!")
        print(f"✅ Total new jobs: +{new_jobs if 'new_jobs' in locals() else 'N/A'}")
    else:
        print("\n⚠️ Some crawlers failed, check logs above")

if __name__ == "__main__":
    asyncio.run(main())
