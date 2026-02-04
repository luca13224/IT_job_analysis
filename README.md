<div align="center">

# 🇻🇳 Vietnam IT Job Market Analysis

### 📊 Interactive Dashboard with AI-Powered Career Insights

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Data](https://img.shields.io/badge/Jobs-1,141-orange.svg)](data_clean/clean_data.csv)

*Dashboard phân tích thị trường tuyển dụng IT với **10 trang tương tác**, AI chatbot, và công cụ mô phỏng lộ trình nghề nghiệp*

[Demo](#-chạy-nhanh-3-bước) • [Features](#-tính-năng-chính) • [Installation](#-chạy-nhanh-3-bước) • [Documentation](#-insights-chính)

</div>

---

## 🚀 Chạy nhanh (3 bước)

### Prerequisites
- Python 3.11 or higher
- Git

### Installation

```bash
# 1. Clone repository
git clone https://github.com/luca13224/IT_job_analysis.git
cd IT_job_analysis

# 2. Create virtual environment (khuyến nghị)
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run dashboard
streamlit run src/visualization/dashboard_v2.py

# 5. Mở browser: http://localhost:8501
#    ⚠️ KHÔNG dùng 0.0.0.0:8501 (sẽ lỗi ERR_ADDRESS_INVALID)
```

### 🎯 Quick Test
```bash
# Kiểm tra cài đặt thành công
python -c "import streamlit; import pandas; import plotly; print('✅ All dependencies OK!')"
```

## ✨ Tính năng chính

### 📊 Dashboard 10 trang
1. **🏠 Tổng quan** - Metrics tổng quan thị trường
2. **📊 Phân tích thị trường** - Phân bố jobs theo nhóm nghề/cấp độ/thành phố
3. **🔍 Gợi ý việc làm** - AI matching dựa trên kỹ năng (TF-IDF + Cosine Similarity)
4. **💰 Phân tích lương** - Phân tích chi tiết mức lương theo vị trí
5. **🎓 Phân tích kỹ năng** - Top skills, skill combinations, trends
6. **🎬 Kịch bản Demo** - 5 pre-built scenarios cho presentation
7. **🚀 Mô phỏng lộ trình** - Career path 5-10 năm với salary projection
8. **⚖️ Công cụ so sánh** - So sánh jobs/cities/companies
9. **📥 Xuất báo cáo** - Export Excel/CSV/JSON + generate reports
10. **🤖 Trợ lý AI** - Chatbot Q&A về thị trường IT

### 🎯 Crawlers
- **ITViec.vn** - 1,141 jobs crawled
- **TopCV.vn** - Multi-page crawler với rate limiting


## 🛠 Tech Stack

- **Web Crawling:** Selenium, BeautifulSoup4
- **Data:** Pandas, NumPy
- **NLP:** NLTK, spaCy, Underthesea (Vietnamese)
- **ML:** Scikit-learn (TF-IDF, Cosine Similarity)
- **Visualization:** Plotly, Streamlit
- **UI/UX:** Custom CSS với gradient theme (Purple/Blue)

## 📁 Cấu trúc Project

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

Dashboard có 5 kịch bản demo sẵn:

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

## 🙏 Acknowledgments

- Dữ liệu từ [ITViec.vn](https://itviec.com) - Vietnam's #1 IT Job Site
- Built with [Streamlit](https://streamlit.io) - The fastest way to build data apps
- Icons from [Icons8](https://icons8.com) - Free icons and design resources

## 📧 Contact & Support

- 📫 GitHub Issues: [Report bugs or request features](https://github.com/luca13224/IT_job_analysis/issues)
- ⭐ Star this repo if you find it useful!
- 🍴 Fork and customize for your needs

---

<div align="center">

**Made with ❤️ for the Vietnamese IT Community**

[![GitHub stars](https://img.shields.io/github/stars/luca13224/IT_job_analysis?style=social)](https://github.com/luca13224/IT_job_analysis)
[![GitHub forks](https://img.shields.io/github/forks/luca13224/IT_job_analysis?style=social)](https://github.com/luca13224/IT_job_analysis/fork)

</div>