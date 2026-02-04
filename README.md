# 🇻🇳 Phân tích Thị trường Việc làm IT Việt Nam

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)](https://streamlit.io)
[![AI](https://img.shields.io/badge/AI-Groq%20Llama%203.3-brightgreen.svg)](https://console.groq.com)
[![Data](https://img.shields.io/badge/Jobs-1,436+-orange.svg)](data_clean/clean_data.csv)

Dashboard phân tích thị trường IT với **AI crawlers** (Groq Llama 3.3 - FREE) + **Interactive dashboard** (10 pages). Data thật từ ITViec + VietnamWorks.

---

## ⚡ Quick Start (1 phút)

### 1. Xem Dashboard ngay
```bash
streamlit run src/visualization/dashboard_v2.py
```
🌐 http://localhost:8501 - **1,436 jobs** sẵn có

### 2. Crawl thêm data (Optional)
```bash
# Setup: https://console.groq.com → API Key → .env
python src/crawler/ITViec_AI_groq.py --jobs 20         # REAL
python src/crawler/VietnamWorks_AI_groq.py --jobs 20   # REAL
python src/crawler/ITViec_AI_demo.py --jobs 100        # MOCK (no API)
```

---

## 📦 Setup

```bash
# 1. Clone & Install
git clone https://github.com/luca13224/IT_job_analysis.git
cd IT-job-analysis-VN-main
pip install -r requirements.txt
playwright install chromium

# 2. Groq API (Optional - chỉ cần nếu crawl REAL)
# https://console.groq.com → Create API Key
# Add to .env: GROQ_API_KEY=gsk_your_key_here
```

---

## 🎯 Demo (15 phút)

### 1. Dashboard (5 min)
```bash
streamlit run src/visualization/dashboard_v2.py
```
10 pages: Overview, Skills, Salary, ML Recommendation...

### 2. AI Crawler (5 min)
```bash
python src/crawler/ITViec_AI_groq.py --jobs 5
```
Explain: Playwright → HTML → Groq AI → JSON → Merge

### 3. Results (2 min)
```bash
# Show data
python -c "import pandas as pd; df=pd.read_csv('data_raw/ITViec_AI_groq.csv'); print(df.head())"

# Refresh dashboard (Ctrl+F5)
```

### 4. Q&A (3 min)
- **Why AI?** Selenium breaks, AI adapts
- **Cost?** $0 - Groq free
- **Speed?** 1-2 min/site

---

## 🤖 AI Crawlers

### Groq (REAL - FREE) ⭐
```bash
python src/crawler/ITViec_AI_groq.py --jobs 20
python src/crawler/VietnamWorks_AI_groq.py --jobs 20
```
✅ FREE • ⚡ 1-2 min • 🤖 Llama 3.3 • 🏢 VNG, FPT, Tiki...

### Mock (DEMO)
```bash
python src/crawler/ITViec_AI_demo.py --jobs 100
```
⚡ 10s • 🎭 Fake realistic • ✅ No API

### Selenium (Traditional)
```bash
python src/crawler/ITViec_crawling.py
```
🔧 No AI • ⚡ 3 min • ⚠️ Brittle

**Architecture:**
```
Playwright → HTML → Groq AI (Llama 3.3) → JSON → Transform → Merge
```

---

## 📂 Structure

```
src/
├── visualization/dashboard_v2.py    # 10-page dashboard
├── crawler/
│   ├── ITViec_AI_groq.py           # ⭐ REAL (FREE)
│   ├── VietnamWorks_AI_groq.py     # ⭐ REAL (FREE)
│   └── ITViec_AI_demo.py           # 🎭 MOCK
├── analysis/EDA.py
data_clean/clean_data.csv            # 1,436 jobs
notebooks/DATA_PROCESSING_LOGIC.ipynb # 📘 Logic xử lý data
```

---

## 🎓 Technical

### Why AI > Selenium

| Feature | Selenium | AI (Groq) |
|---------|----------|-----------|
| Approach | CSS selectors | Semantic |
| Flexibility | ❌ Breaks | ✅ Adapts |
| Cost | Free | Free |

### AI Prompt
```python
"Extract 20 jobs from HTML. Return JSON with: 
job_title, company_name, salary, level, city, skills"
```

### Data Pipeline
```
Raw → Clean → Transform → Feature Engineering → Analysis
```
📘 **Chi tiết:** [notebooks/DATA_PROCESSING_LOGIC.ipynb](notebooks/DATA_PROCESSING_LOGIC.ipynb)

---

## 🧪 Testing

```bash
python src/crawler/test_all_crawlers.py                    # Test all
python src/crawler/ITViec_AI_groq.py --jobs 5              # Quick test
python -c "import pandas as pd; print(len(pd.read_csv('data_clean/clean_data.csv')))"  # Verify
```

---

## 🐛 Troubleshooting

```bash
# API key not found
echo "GROQ_API_KEY=gsk_..." >> .env

# Rate limit → Wait 2 min or use mock
python src/crawler/ITViec_AI_demo.py --jobs 50

# Browser error
playwright install chromium

# Dashboard not updating
streamlit run src/visualization/dashboard_v2.py  # Restart
```

---

## 📈 Stats

- **1,436 jobs** • **400+ companies** • **3 cities** • **50+ skills**
- **AI**: Llama 3.3 70B • **Cost**: $0 • **Time**: 1-2 min/site

---

**Links:** [GitHub](https://github.com/luca13224/IT_job_analysis) • [Groq API](https://console.groq.com) • [Playwright](https://playwright.dev)

Made with 🤖 + ❤️
