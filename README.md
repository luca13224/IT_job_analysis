<div align="center">

# 🇻🇳 Vietnam IT Job Market Analysis

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)](https://streamlit.io)
[![Data](https://img.shields.io/badge/Jobs-1,141-orange.svg)](data_clean/clean_data.csv)

Dashboard phân tích 1,141 jobs IT từ ITViec với AI recommendations, career simulator, và 10 trang tương tác.

</div>

---

## 🚀 Quick Start

```bash
# Clone & setup
git clone https://github.com/luca13224/IT_job_analysis.git
cd IT_job_analysis
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Run dashboard
streamlit run src/visualization/dashboard_v2.py
# → Open http://localhost:8501
```

## ✨ Features

**10 Dashboard Pages:**
1. 🏠 Overview - Market metrics
2. 📊 Market Analysis - Job distribution
3. 🔍 Job Recommendations - AI matching (TF-IDF + Cosine Similarity)
4. 💰 Salary Insights - Salary analysis by role
5. 🎓 Skills Analysis - Top skills & trends
6. 🎬 Demo Scenarios - 5 pre-built personas
7. 🚀 Career Simulator - 5-10 year salary projection
8. ⚖️ Compare Tool - Jobs/Cities/Companies comparison
9. 📥 Export Tools - Excel/CSV/JSON reports
10. 🤖 AI Chatbot - Q&A assistant

**Data Sources:** ITViec (1,141 jobs), TopCV crawler


## 🛠 Tech Stack

- **Web Crawling:** Selenium, BeautifulSoup4
- **Data:** Pandas, NumPy
**Crawling:** Selenium, BeautifulSoup | **Data:** Pandas, NumPy | **ML/NLP:** Scikit-learn, NLTK, spaCy | **Viz:** Streamlit, Plotly

## 🔄 Data Pipeline

```
Crawling → Processing → Analysis → Dashboard
1,141 jobs  → Clean data → ML/NLP → 10 pages
```

**Pipeline gồm 7 modules:**

1. **Web Crawling**: Selenium auto-scroll ITViec, extract job details, incremental save CSV
2. **Data Processing**: Normalize salary (USD→VND), parse skills, categorize jobs, standardize locations
3. **ML Recommendations**: TF-IDF vectorization + Cosine Similarity → Match user skills với jobs (0-100%)
4. **NLP Analysis**: Skill frequency, co-occurrence patterns, recommendations
5. **Dashboard**: 10 Streamlit pages với caching, filters, real-time charts
6. **Career Simulator**: Fresher→Junior→Mid→Senior progression với salary projection (5-10 years)
7. **AI Chatbot**: Intent detection (salary/skills/career queries) + entity extraction + data-driven responses

**Performance:** Load 2-3s | TF-IDF 0.5s | Recommendations <1s | Memory 50MB

```
IT-job-analysis-VN-main/
├── .streamlit/                    # Streamlit configuration
│   └── config.toml               # Server & UI settings
├── config/                        # Application config
├── data_clean/                    # ✅ Processed data (ready to use)
│   └── clean_data.csv            # 1,141 IT jobs from ITViec
├── data_raw/                      # Raw scraped data
├── src/
│   ├── crawler/                  # Web scraping modules
│   │   ├── ITViec_crawling.py   # ITViec scraper
│   │   └── topcv_crawling.py    # TopCV scraper
│   ├── ml_models/                # AI/ML models
│   │   └── job_recommender.py   # TF-IDF + Cosine Similarity
│   └── visualization/            # 📊 Dashboard modules (10 pages)
│       ├── dashboard_v2.py       # 🏠 Main entry point
│       ├── demo_scenarios.py     # 🎬 5 pre-built demos
│       ├── career_simulator.py   # 🚀 Career path projection
│       ├── compare_tool.py       # ⚖️ Job/City/Company comparison
│       ├── export_tools.py       # 📥 Excel/CSV/JSON export
│       ├── chatbot.py            # 🤖 AI Q&A assistant
│       └── animations.py         # 🎨 UI animations
├── notebooks/                     # Jupyter analysis
│   └── eda.ipynb                 # Exploratory Data Analysis
├── requirements.txt               # Python dependencies
├── run_dashboard_v2.bat          # 🚀 Quick launch script (Windows)
└── README.md                     # 📖 This file
```

> **💡 Tip:** Dữ liệu đã được xử lý sẵn tại `data_clean/clean_data.csv`. Bạn không cần chạy crawler để demo!


## 📊 Insights chính

**Thống kê tổng quan:**
- 1,141 jobs từ ITViec.vn
- 15+ nhóm nghề nghiệp
- Lương trung bình: 20-40M VND

**Top 5 nghề hot:**
1. Backend Developer
2. Frontend Developer  
3. Fullstack Developer
4. Data / AI
5. Mobile Developer

**Top 5 skills cần thiết:**
1. JavaScript / TypeScript
2. Python
3. React / Vue
4. Docker / Kubernetes
5. AWS / Cloud

**Insights lương:**
- Backend Senior: 30-50M VND
- Data/AI Engineer: 35-60M VND
- Frontend Mid: 20-35M VND
- DevOps Engineer: 30-55M VND

## 🎬 Demo Scenarios (cho Presentation)

Dashboard có 5 kịch bản demo:

1. **Fresh Graduate** - Sinh viên mới ra trường tìm việc
2. **Experienced Dev** - Dev 2 năm muốn đổi việc
3. **HR Analysis** - HR phân tích thị trường lương
4. **Recruiter** - Nhà tuyển dụng tìm trending skills
5. **Learner** - Người học chọn lộ trình (Frontend/Backend/Data)

## 🚀 Deploy lên Streamlit Cloud

```bash
# 1. Push code lên GitHub
git add .
git commit -m "Deploy dashboard"
git push origin main

# 2. Vào https://streamlit.io/cloud
# 3. Connect GitHub repo
# 4. Main file: src/visualization/dashboard_v2.py
# 5. Deploy!
```

## 🎯 Workflow Demo gợi ý (15-20 phút)

1. **Intro (2p)** → Tổng quan + animated metrics
2. **Market Analysis (3p)** → Charts & insights
3. **Career Planning (4p)** → Mô phỏng 5-year roadmap
4. **Comparison (3p)** → Backend vs Frontend
5. **AI Assistant (4p)** → Live Q&A với chatbot
6. **Export (2p)** → Download report
7. **Q&A (2p)** → Use chatbot trả lời audience

## 💡 Tips sử dụng

**Career Simulator:**
- Input: Job group + Current level + Years (1-10)
- Output: Timeline lương, skills cần học theo năm
- Best for: Lập kế hoạch nghề nghiệp dài hạn

**Compare Tool:**
- So sánh 2 jobs/cities/companies side-by-side
- Visual charts + auto insights
- Best for: Đưa ra quyết định nghề nghiệp

**AI Chatbot:**
- Hỏi về lương, skills, xu hướng, lộ trình
- Quick buttons cho câu hỏi phổ biến
- Best for: Q&A session trong demo

**Export Tools:**
- Excel có 2 sheets: Data + Summary
- CSV/JSON cho research
- Text reports với analysis

## 🐛 Troubleshooting

<details>
<summary><b>Dashboard không chạy được</b></summary>

```bash
# Cài lại dependencies
pip install --upgrade streamlit pandas plotly

# Kiểm tra Python version (cần >= 3.11)
python --version
```
</details>

<details>
<summary><b>Lỗi "ERR_ADDRESS_INVALID" khi mở browser</b></summary>

⚠️ **Không dùng** `http://0.0.0.0:8501`

✅ **Dùng:** `http://localhost:8501` hoặc `http://127.0.0.1:8501`
</details>

<details>
<summary><b>Thiếu file data</b></summary>

Dữ liệu đã có sẵn tại `data_clean/clean_data.csv` (1,141 jobs). Không cần chạy crawler!
</details>

<details>
<summary><b>Lỗi import module</b></summary>

```bash
# Đảm bảo chạy từ thư mục gốc
cd IT_job_analysis

# Kiểm tra cấu trúc thư mục
ls src/visualization/dashboard_v2.py
```
</details>

<details>
<summary><b>Port 8501 đã bị chiếm</b></summary>

```bash
# Dùng port khác
streamlit run src/visualization/dashboard_v2.py --server.port 8502
```
</details>

<details>
<summary><b>Lỗi encoding khi đọc CSV</b></summary>

```python
# Thêm encoding UTF-8
df = pd.read_csv('data.csv', encoding='utf-8-sig')
```
</details>

## 📚 Tài Liệu Tham Khảo

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)

## 👥 Đóng Góp

Contributions are welcome! Vui lòng:

1. Fork repository
2. Create feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open Pull Request

## 📝 License

MIT License - Xem [LICENSE](LICENSE) để biết thêm chi tiết.

## 🙏 Project Structure

```
├── data_clean/clean_data.csv    # 1,141 jobs (ready to use)
├── src/
│   ├── crawler/                 # ITViec & TopCV scrapers
│   ├── ml_models/               # TF-IDF recommender
│   └── visualization/           # 10 dashboard pages
│       ├── dashboard_v2.py      # Main entry
│       ├── career_simulator.py
│       ├── compare_tool.py
│       ├── export_tools.py
│       └── chatbot.py
└── requirements.txt
```Key Insights

- **1,141 jobs** từ ITViec | **15+ job groups** | Lương avg: 20-40M VND
- **Top roles:** Backend, Frontend, Fullstack, Data/AI, Mobile
- **Top skills:** JavaScript/TS, Python, React/Vue, Docker, AWS
- **Salary ranges:** Backend Senior 30-50M | Data/AI 35-60M | Frontend Mid 20-35M

## 🎬 Demo Tips

**5 Pre-built Scenarios:** Fresh Graduate | Dev 2 years exp | HR | Recruiter | Learner

**Suggested Demo Flow (15 mins):**
1. Overview (2m) → 2. Market Analysis (3m) → 3. Career Simulator (4m) → 4. Compare (3m) → 5. AI Chatbot (3m)

## 📝 License & Contact

MIT License | Data from [ITViec.vn](https://itviec.com) | Built with [Streamlit](https://streamlit.io)

⭐ [Star on GitHub](https://github.com/luca13224/IT_job_analysis) | 🐛 [Report Issues](https://github.com/luca13224/IT_job_analysis/issues)