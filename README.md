# 📊 Phân tích Thị trường Tuyển dụng IT Việt Nam

> Hệ thống thu thập và phân tích dữ liệu tuyển dụng IT tự động với AI-powered web crawler, data processing pipeline và interactive dashboard.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/Playwright-1.40+-green.svg)](https://playwright.dev/python/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Mục lục

- [Giới thiệu](#-giới-thiệu)
- [Tính năng](#-tính-năng)
- [Demo](#-demo)
- [Công nghệ](#-công-nghệ-sử-dụng)
- [Cài đặt](#-cài-đặt)
- [Sử dụng](#-sử-dụng)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [API Reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## 🎯 Giới thiệu

Dự án phân tích thị trường tuyển dụng IT tại Việt Nam, thu thập dữ liệu từ ITViec.com và cung cấp insights chi tiết về:
- 💰 Mức lương theo vị trí, kinh nghiệm, kỹ năng
- 🛠️ Công nghệ và kỹ năng hot nhất
- 🏢 Top công ty tuyển dụng nhiều
- 📍 Phân bố việc làm theo thành phố

### ✨ Điểm đặc biệt

🤖 **AI-powered parsing**: Sử dụng Groq API (LLM Llama 3.1) để parse HTML thông minh, không cần regex phức tạp  
⚡ **Fully automated**: Pipeline từ crawl → process → visualize hoàn toàn tự động  
📊 **Interactive dashboard**: 4 pages với 15+ charts, filters real-time  
🔄 **Easy to extend**: Dễ dàng thêm data sources mới (TopCV, VietnamWorks...)

## ✨ Tính năng

### 1. 🕷️ AI-Powered Web Crawler
- **Browser automation**: Playwright (headless Chrome)
- **🤖 AI parsing**: Groq API với Llama 3.1 70B
  - Không cần viết regex phức tạp
  - Parse HTML thông minh dựa vào ngữ cảnh
  - Tự động adapt khi website thay đổi layout
- **Retry logic**: Exponential backoff khi gặp lỗi
- **Logging**: Chi tiết từng bước crawl
- **Async/await**: Performance tối ưu

### 2. 🧹 Data Processing
- Cleaning: remove duplicates, normalize text
- Transformation: parse salary, extract skills
- Classification: auto-detect job_group (Backend/Frontend/DevOps...)
- Aggregation: statistics, grouping, filtering

### 3. 📊 Dashboard
- **Overview**: Tổng quan thị trường (1,447 jobs, 564 companies)
- **Salary Analysis**: Box plots, histograms, comparisons
- **Skills Analysis**: Top 10 skills, word cloud, trends
- **Company Analysis**: Top recruiters, avg salary by company
- **Filters**: Location, experience, salary range, job type

### 4. 🎨 Advanced Features
- Export data to CSV/Excel
- Export charts to PNG
- Multi-criteria filtering
- Responsive design

## 🎬 Demo

**Dashboard Overview:**
```
📊 Tổng số việc: 1,447
🏢 Công ty: 564
💰 Lương TB: 46.2M VND
📍 Thành phố: 7
```

**Top Skills:**
1. JavaScript (40%)
2. Python (35%)
3. React (30%)
4. AWS (25%)
5. Docker (22%)

## 🛠️ Công nghệ sử dụng

| Công nghệ | Version | Mục đích |
|-----------|---------|----------|
| Python | 3.11+ | Ngôn ngữ chính |
| Playwright | 1.40 | Browser automation |
| Groq API | Latest | LLM parsing (Llama 3.1) |
| Pandas | 2.0.3 | Data processing |
| Streamlit | 1.28 | Dashboard framework |
| Plotly | 5.17 | Interactive charts |

## 📦 Cài đặt

### Bước 1: Clone repository

```bash
git clone https://github.com/yourusername/IT-job-analysis-VN.git
cd IT-job-analysis-VN
```

### Bước 2: Tạo virtual environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Bước 3: Cài dependencies

```bash
pip install -r requirements.txt
```

### Bước 4: Cài Playwright browsers

```bash
playwright install chromium
```

### Bước 5: Cấu hình Groq API key (BỮT BUỘC cho crawler)

**⚠️ QUAN TRỌNG**: Crawler sử dụng Groq API (AI) để parse dữ liệu, PHẢI có API key mới chạy được!

**Tạo file `.env` trong thư mục gốc:**

```env
GROQ_API_KEY=gsk_your_actual_key_here_xxxxxxxxxx
```

**📝 Lấy Groq API key MIỄN PHÍ (2 phút):**

1. **Truy cập**: https://console.groq.com/
2. **Đăng ký** tài khoản (Gmail/GitHub)
3. **Vào API Keys**: Click "Create API Key"
4. **Copy key** (dạng `gsk_xxxxx...`)
5. **Paste vào file `.env`**

**Free tier:**
- ✅ 30 requests/phút (đủ crawl 50-100 jobs)
- ✅ Llama 3.1 70B model
- ✅ Không cần thẻ tín dụng

### Bước 6: Verify installation

```bash
python -c "import playwright, pandas, streamlit; print('✅ OK!')"
```

## 🚀 Sử dụng

### Quick Start (Recommended)

```bash
# Chạy toàn bộ pipeline
python main.py
```

Hệ thống sẽ tự động:
1. ✅ Crawl dữ liệu từ ITViec
2. ✅ Xử lý và làm sạch data
3. ✅ Khởi động dashboard

### Manual Steps

#### 1️⃣ Crawl dữ liệu với Groq AI API

**⚠️ ĐẢM BẢO đã có GROQ_API_KEY trong file `.env`**

**Crawler chính (khuyên dùng):**
```bash
# Crawl với Groq AI (parse thông minh)
python src/crawler/ITViec_AI_groq.py --jobs 50

# Crawl nhiều hơn
python src/crawler/ITViec_AI_groq.py --jobs 100
```

**Hoặc crawler cơ bản (không cần AI):**
```bash
# Không dùng AI, parse bằng regex (ít chính xác hơn)
python src/crawler/ITViec_crawling.py
```

**Output:** `data/raw/ITViec_data.csv` hoặc `data/raw/ITViec_AI_groq.csv`

**🔍 Cách hoạt động:**
1. Playwright mở browser → truy cập ITViec.com
2. Scroll trang để load jobs (lazy loading)
3. Lấy HTML content
4. **Gửi HTML đến Groq API** → LLM parse thành JSON
5. Lưu vào CSV

**💡 Ưu điểm AI parsing:**
- ✅ Không cần viết regex phức tạp
- ✅ Tự động adapt khi HTML thay đổi
- ✅ Parse thông minh (hiểu ngữ cảnh)
- ✅ Accuracy cao hơn 20-30%

#### 2️⃣ Xử lý dữ liệu

```bash
# Full pipeline
python scripts/full_pipeline.py

# Hoặc từng bước:
python scripts/clean_data.py
python scripts/transform_data.py
python scripts/merge_and_update.py
```

Output: `data/processed/clean_data.csv`

#### 3️⃣ Khởi động Dashboard

```bash
streamlit run src/visualization/dashboard_v2.py
```

Truy cập: **http://localhost:8501**

## 📁 Cấu trúc dự án

```
IT-job-analysis-VN/
├── 📂 src/
│   ├── 📂 crawler/
│   │   ├── ITViec_crawling.py      # Main crawler
│   │   └── __init__.py
│   ├── 📂 analysis/
│   │   ├── EDA.py                   # Data analysis
│   │   └── __init__.py
│   └── 📂 visualization/
│       ├── dashboard_v2.py          # Dashboard chính
│       ├── animations.py
│       └── export_tools.py
├── 📂 scripts/
│   ├── clean_data.py                # Làm sạch data
│   ├── transform_data.py            # Transform data
│   ├── merge_and_update.py          # Merge + dedupe
│   └── full_pipeline.py             # Auto pipeline
├── 📂 data/
│   ├── 📂 raw/                      # Dữ liệu thô
│   │   └── ITViec_data.csv
│   └── 📂 processed/                # Dữ liệu sạch
│       └── clean_data.csv
├── 📂 notebooks/                    # Jupyter notebooks
│   ├── crawling_test.ipynb
│   ├── cleanning_data.ipynb
│   └── eda.ipynb
├── 📂 config/
│   └── config.py                    # Config settings
├── 📜 main.py                       # Entry point
├── 📜 requirements.txt
├── 📜 .env.example
└── 📜 README.md
```

## 🔧 API Reference

### Crawler

```python
from src.crawler.ITViec_crawling import crawl_jobs

# Basic
jobs = crawl_jobs(max_jobs=50)

# Advanced
jobs = crawl_jobs(
    max_jobs=100,
    keywords=["Python", "Java"],
    headless=True
)
```

### Data Processing

```python
from scripts.clean_data import clean_dataframe
from scripts.transform_data import transform_data

df_clean = clean_dataframe(df_raw)
df_t❌ Lỗi: "GROQ_API_KEY not found"
**Nguyên nhân:** Chưa tạo file `.env` hoặc chưa có API key

**Giải pháp:**
1. Tạo file `.env` trong thư mục gốc
2. Lấy key tại: https://console.groq.com/
3. Thêm vào `.env`: `GROQ_API_KEY=gsk_xxx...`
4. Chạy lại crawler

### ❌ Lỗi: "playwright not found"
```bash
playwright install chromium
```

### ❌ Lỗi: "Groq API rate limit exceeded" 
**Nguyên nhân:** Vượt quá 30 requests/phút (free tier)

**Giải pháp:**
- Crawl ít jobs hơn (--jobs 30)
- Đợi 1 phút rồi chạy lại
- Hoặc upgrade Groq plan

### ❌ Lỗi: "Invalid API key"
**Nguyên nhân:** API key sai hoặc hết hạn

**Giải pháp:**
1. Kiểm tra key trong `.env` có đúng format `gsk_xxx...`
2. Tạo key mới tại https://console.groq.com/keys
3. Update key trong `.env`
- `company`: Tên công ty
- `location`: Địa điểm
- `salary`: Mức lương (text)
- `experience`: Kinh nghiệm yêu cầu
- `skills`: Kỹ năng (comma-separated)

### Processed Data
- `salary_min`, `salary_max`: Lương min/max (numeric)
- `experience_level`: Junior/Middle/Senior
- `skills_list`: Array of skills
- `job_group`: Backend/Frontend/DevOps/Data/QA/Mobile

## 🐛 Troubleshooting

### Lỗi: "playwright not found"
```bash
playwright install chromium
```

### Lỗi: "Groq API rate limit exceeded"
- Free tier: 30 requests/min
- Thêm delay hoặc upgrade plan

### Dashboard không load data
```bash
# Kiểm tra file tồn tại
ls data/processed/clean_data.csv

# Chạy lại pipeline
python scripts/full_pipeline.py
```

### Crawler timeout
- Tăng timeout trong config
- Kiểm tra internet connection

## 📈 Performance

- **Crawl 50 jobs**: ~2-3 phút
- **Crawl 100 jobs**: ~5-7 phút
- **Dashboard load (1,500 rows)**: <1 giây
- **Bottleneck**: Groq API rate limit

## 🤝 Contributing

Contributions welcome!

1. Fork repo
2. Create branch: `git checkout -b feature/AmazingFeature`
3. Commit: `git commit -m 'Add feature'`
4. Push: `git push origin feature/AmazingFeature`
5. Create Pull Request

## 📝 TODO

- [ ] Add more data sources (TopCV, VietnamWorks)
- [ ] ML models: salary prediction, job recommendation
- [ ] Schedule auto-crawl (Airflow)
- [ ] Deploy to cloud (Heroku/AWS)
- [ ] API endpoints (FastAPI)
- [ ] Mobile app

## 📄 License

MIT License - xem [LICENSE](LICENSE)

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- [ITViec.com](https://itviec.com) - Data source
- [Groq](https://groq.com) - LLM API
- [Streamlit](https://streamlit.io) - Dashboard
- [Playwright](https://playwright.dev) - Automation

---

⭐ **Star this repo if you find it useful!** ⭐

**Made with ❤️ in Vietnam**
