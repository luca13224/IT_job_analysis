# 🎯 DEMO COMMANDS - Quick Reference

## 📌 Setup nhanh (1 lần duy nhất)

```bash
# 1. Lấy Groq API key (30 giây)
https://console.groq.com → Create API Key

# 2. Thêm vào .env
GROQ_API_KEY=gsk_your_key_here

# 3. Cài thư viện (nếu chưa có)
pip install groq playwright
playwright install chromium
```

---

## 🚀 LỆNH DEMO CHÍNH

### Option 1: Dashboard ngay (Không cần crawl)
```bash
streamlit run src/visualization/dashboard_v2.py
```
📊 **1,436 jobs** sẵn có → Xem ngay!

---

### Option 2: AI Crawl + Dashboard

#### A. Crawl ITViec (THẬT)
```bash
# Quick (5 jobs, 30 giây)
python src/crawler/ITViec_AI_groq.py --jobs 5

# Standard (20 jobs, 1-2 phút)
python src/crawler/ITViec_AI_groq.py --jobs 20
```

#### B. Crawl VietnamWorks (THẬT)
```bash
# Quick (10 jobs, 30 giây)
python src/crawler/VietnamWorks_AI_groq.py --jobs 10

# Standard (20 jobs, 1-2 phút)  
python src/crawler/VietnamWorks_AI_groq.py --jobs 20
```

#### C. Crawl Mock (FAKE - Không cần API)
```bash
# Demo nhanh (50 jobs, 5 giây)
python src/crawler/ITViec_AI_demo.py --jobs 50

# Standard (100 jobs, 10 giây)
python src/crawler/ITViec_AI_demo.py --jobs 100

# Full (200 jobs, 20 giây)
python src/crawler/ITViec_AI_demo.py --jobs 200
```

---

## 🎬 DEMO FLOW (15 phút)

### 1️⃣ Show Dashboard (3 phút)
```bash
streamlit run src/visualization/dashboard_v2.py
```
- **Trang Overview**: Tổng quan 1,436 jobs
- **Trang Skill Analysis**: Top skills demand
- **Trang Salary**: Phân tích lương
- **Trang ML Recommendation**: AI gợi ý jobs

### 2️⃣ Demo AI Crawler (5 phút)
```bash
# Terminal 1: Chạy crawler
python src/crawler/ITViec_AI_groq.py --jobs 5

# Giải thích trong khi chạy:
# - Browser tự động mở (Playwright)
# - HTML gửi lên Groq AI (Llama 3.3)
# - AI parse và extract data
# - Auto-merge vào clean_data.csv
```

### 3️⃣ Show Results (3 phút)
```bash
# Xem data vừa crawl
python -c "import pandas as pd; df=pd.read_csv('data_raw/ITViec_AI_groq.csv'); print(df[['job_title','company_name','city']].head())"

# Check tổng jobs
python -c "import pandas as pd; print(f'Total jobs: {len(pd.read_csv(\"data_clean/clean_data.csv\"))}')"

# Refresh dashboard → Thấy jobs mới
streamlit run src/visualization/dashboard_v2.py
```

### 4️⃣ Q&A (4 phút)
**Câu hỏi thường gặp:**

**Q: Tại sao dùng AI?**
→ Selenium break khi web đổi layout, AI hiểu semantic

**Q: Chi phí?**
→ $0 - Groq miễn phí (30 requests/phút)

**Q: So với Selenium?**
→ Selenium: CSS selectors cố định, AI: linh hoạt

---

## 🧪 TEST NHANH

```bash
# Test tất cả crawlers (3+5 jobs = 8 jobs mới)
python src/crawler/test_all_crawlers.py

# Kiểm tra kết quả
python -c "import pandas as pd; df=pd.read_csv('data_clean/clean_data.csv'); print(f'✅ Total: {len(df)} jobs'); print(df[['job_names','company_names']].tail(8))"
```

---

## 📊 KIỂM TRA DATA

```bash
# 1. Check raw data files
ls data_raw/*.csv

# 2. Count jobs
python -c "import pandas as pd; df=pd.read_csv('data_clean/clean_data.csv'); print(f'Total jobs: {len(df)}'); print(f'Companies: {df[\"company_names\"].nunique()}'); print(f'Cities: {df[\"city\"].unique()}')"

# 3. Sample data
python -c "import pandas as pd; df=pd.read_csv('data_clean/clean_data.csv'); print(df[['job_names','company_names','city','salaries']].sample(10))"

# 4. Latest jobs
python -c "import pandas as pd; df=pd.read_csv('data_clean/clean_data.csv'); print(df[['job_names','company_names']].tail(10))"
```

---

## 🛠️ TROUBLESHOOTING

### Lỗi: "GROQ_API_KEY not found"
```bash
# Check .env
cat .env | grep GROQ

# Add key
echo "GROQ_API_KEY=gsk_your_key_here" >> .env
```

### Lỗi: "playwright not installed"
```bash
pip install playwright
playwright install chromium
```

### Lỗi: "Rate limit exceeded"
```bash
# Đợi 1-2 phút, Groq free tier: 30 req/phút
# Hoặc dùng mock crawler (không cần API)
python src/crawler/ITViec_AI_demo.py --jobs 50
```

### Dashboard không hiện data mới
```bash
# Refresh browser (Ctrl+F5)
# Hoặc restart Streamlit
Ctrl+C → streamlit run src/visualization/dashboard_v2.py
```

---

## 📚 FILES QUAN TRỌNG

```
src/crawler/
├── ITViec_AI_groq.py         ⭐ Crawler THẬT ITViec
├── VietnamWorks_AI_groq.py   ⭐ Crawler THẬT VietnamWorks  
├── ITViec_AI_demo.py         🎭 Mock crawler (demo)
├── README_AI_CRAWLERS.md     📖 Docs đầy đủ
└── test_all_crawlers.py      🧪 Test script

data_raw/                      📁 Raw crawler output
data_clean/clean_data.csv      ✅ Main data (1,436 jobs)

src/visualization/
└── dashboard_v2.py            📊 Streamlit dashboard

README.md                      📘 Main docs
AI_CRAWLING_EXPLANATION.md     💡 Giải thích cho GV
QUICK_DEMO_GV.md              🎬 Demo script cho thầy
```

---

## ⚡ QUICK COMMANDS (Copy-Paste)

```bash
# Full demo flow (5 phút)
python src/crawler/ITViec_AI_groq.py --jobs 5 && \
python src/crawler/VietnamWorks_AI_groq.py --jobs 10 && \
streamlit run src/visualization/dashboard_v2.py

# Mock demo (10 giây + dashboard)
python src/crawler/ITViec_AI_demo.py --jobs 100 && \
streamlit run src/visualization/dashboard_v2.py

# Test all
python src/crawler/test_all_crawlers.py && \
python -c "import pandas as pd; print(f'Total: {len(pd.read_csv(\"data_clean/clean_data.csv\"))} jobs')"
```

---

## 🎓 KEYWORDS CHO THUYẾT TRÌNH

- ✅ **AI-powered crawler** (không phải Selenium thuần)
- ✅ **Semantic understanding** (AI hiểu ngữ nghĩa HTML)
- ✅ **LLM (Llama 3.3 70B)** qua Groq API
- ✅ **Zero-shot extraction** (không cần training)
- ✅ **Free tier** (30 requests/phút)
- ✅ **Auto-merge & deduplication**
- ✅ **Production ready** (1,436 jobs thật)

---

Made with 🤖 AI + ⚡ Groq
