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

---

## 🔄 Data Pipeline - Quy trình xử lý dữ liệu

### 📊 Tổng quan luồng dữ liệu

```
Crawling (Selenium) → Processing (Pandas) → Analysis (ML/NLP) → Dashboard (Streamlit)
   1,141 jobs      →    Clean data     →   Insights/Models  →     10 pages
```

---

### 1️⃣ **Web Crawling - Thu thập dữ liệu**

**Nguồn:** ITViec.vn (Vietnam's #1 IT Job Site)

**Quy trình:**
1. Khởi tạo Selenium WebDriver với Chrome
2. User đăng nhập thủ công (bypass Cloudflare protection)
3. Script tự động lặp qua tất cả các trang (pagination)
4. Mỗi trang: Scroll để load dynamic content, lấy danh sách job cards
5. Click vào từng job → Extract thông tin chi tiết:
   - Job title, company name, salary range
   - Experience level (Fresher/Junior/Mid/Senior)
   - Location (city)
   - Skills required (tags)
   - Job description
6. Lưu từng job vào CSV ngay lập tức (tránh mất data nếu crash)
7. Random delay 1-3s giữa các request (tránh bị block)

**Kỹ thuật đặc biệt:**
- ✅ Resume crawling: Lưu `current_page.txt` để tiếp tục nếu bị gián đoạn
- ✅ Error handling: Try-catch cho từng element, log lỗi chi tiết
- ✅ Duplicate check: Skip jobs đã crawl trước đó

**Kết quả:** `data_raw/ITViec_data.csv` - 1,141 jobs

---

### 2️⃣ **Data Processing - Làm sạch & chuẩn hóa**

**Input:** Raw CSV với dữ liệu thô (inconsistent formats)

**Các bước xử lý:**

**A. Salary Normalization (Chuẩn hóa lương):**
- Convert text → số VND: "Up to $2,000" → 46,000,000 VND
- Xử lý USD: Nhân với tỷ giá 23,000 VND
- Range salary: Lấy trung bình (min+max)/2
- "Negotiable" → NULL

**B. Skills Extraction (Trích xuất kỹ năng):**
- Parse string → list: "['Python', 'Django']" → Python array
- Lowercase tất cả để match dễ dàng
- Remove duplicates trong mỗi job

**C. Job Categorization (Phân loại nghề):**
- Dựa vào keywords trong job title:
  - Backend: Python, Java, Golang, Node.js
  - Frontend: React, Vue, Angular
  - Fullstack: Full-stack, Full stack
  - Data/AI: Data, ML, Machine Learning
  - Mobile: iOS, Android, Flutter
  - DevOps: DevOps, Cloud, AWS
- 15+ categories tổng cộng

**D. Location Standardization:**
- Chuẩn hóa tên thành phố: "HCM" → "Hồ Chí Minh"
- "Hanoi" → "Hà Nội"

**E. Deduplication:**
- Remove jobs trùng lặp (same title + company)

**Kết quả:** `data_clean/clean_data.csv` - Data sạch, consistent format

---

### 3️⃣ **ML Job Recommendations - AI Matching**

**Algorithm:** TF-IDF (Term Frequency - Inverse Document Frequency) + Cosine Similarity

**Cách hoạt động (đơn giản):**

**Bước 1: Build TF-IDF Matrix**
- Chuyển skills của mỗi job thành text: ['Python', 'Django'] → "python django"
- TF-IDF tính "tầm quan trọng" của mỗi skill:
  - Skill phổ biến (JavaScript) → score thấp
  - Skill hiếm (Rust) → score cao
- Tạo matrix 1,141 jobs × 200 features

**Bước 2: User Input**
- User nhập skills: ['Python', 'Django', 'Docker']

**Bước 3: Calculate Similarity**
- Chuyển user skills → vector cùng format
- So sánh với TẤT CẢ 1,141 jobs bằng Cosine Similarity
- Similarity score = Góc giữa 2 vectors (0-100%)

**Bước 4: Ranking**
- Sort jobs theo score giảm dần
- Apply filters: level, city, min salary
- Return top 10 matches

**Ví dụ matching:**
- User có: Python, Django, AWS
- Job A có: Python, Django, PostgreSQL → Match 75%
- Job B có: Java, Spring Boot → Match 0%
- Job C có: Python, Django, AWS, Docker, K8s → Match 92%

**Ưu điểm:**
- ✅ Fast: 1,141 jobs trong < 1 giây
- ✅ Accurate: Dựa trên content thực tế
- ✅ No training data needed

---

### 4️⃣ **NLP Analysis - Phân tích kỹ năng**

**Skill Frequency Analysis:**
- Đếm số lần xuất hiện của mỗi skill
- Top 20 skills: JavaScript, Python, React, Docker, AWS...

**Skill Co-occurrence (Skills đi cùng nhau):**
- Phân tích skills nào thường xuất hiện chung
- Ví dụ: React thường đi với TypeScript, Redux
- Python thường đi với Django, PostgreSQL

**Skill Recommendations:**
- Dựa vào skills hiện tại, gợi ý skill nên học thêm
- Logic: Tìm jobs có skills tương tự → Extract skills còn thiếu

---

### 5️⃣ **Interactive Dashboard - 10 Pages**

**Architecture:** Streamlit (Python web framework)

**Caching Strategy:**
- Data loading cached → Không reload mỗi lần
- ML models cached → Build 1 lần, reuse nhiều lần

**10 Pages:**
1. **Overview** - Metrics tổng quan, key stats
2. **Market Analysis** - Distribution charts (jobs by city/level/group)
3. **Job Recommendations** - AI matching với user skills
4. **Salary Insights** - Salary ranges, percentiles, comparisons
5. **Skills Analysis** - Top skills, trends, co-occurrence
6. **Demo Scenarios** - 5 pre-built personas (Fresher, HR, Recruiter...)
7. **Career Simulator** - 5-10 year salary projection
8. **Compare Tool** - Side-by-side comparison (jobs/cities/companies)
9. **Export Tools** - Download Excel/CSV/JSON + Reports
10. **AI Chatbot** - Q&A về thị trường IT

**UI/UX:**
- Purple/Blue gradient theme
- Responsive layout với st.columns
- Interactive filters trong sidebar
- Real-time updates

---

### 6️⃣ **Career Simulator - Dự đoán lộ trình**

**Input:** Job group + Current level + Years (1-10)

**Logic:**
- Career progression: Fresher → Junior (2 năm) → Mid (2 năm) → Senior
- Mỗi level: Query real salary data từ dataset
- Calculate: Average, Min (25th percentile), Max (75th percentile)
- Show timeline chart với salary growth
- Suggest skills cần học theo từng giai đoạn

**Output:** Interactive timeline với projected salary + skills roadmap

---

### 7️⃣ **AI Chatbot - Q&A System**

**Intent Detection (Keyword matching):**
- Lương/salary → Salary query
- Kỹ năng/skill → Skills query
- So sánh/compare → Comparison query
- Lộ trình/career → Career advice

**Entity Extraction:**
- Job types: Backend, Frontend, Data...
- Levels: Fresher, Junior, Mid, Senior
- Cities: HCM, Hà Nội...

**Response Generation:**
- Query data dựa trên intent + entities
- Format kết quả với markdown
- Show charts nếu cần

---

## 📈 Performance & Scalability

- **Dataset:** 1,141 jobs (có thể mở rộng bằng TopCV crawler)
- **Dashboard load:** ~2-3 giây với caching
- **TF-IDF build:** ~0.5 giây
- **Memory:** ~50MB
- **Recommendation:** < 1 giây cho 1,141 jobs

**Optimization:**
- Streamlit caching (st.cache_data, st.cache_resource)
- Incremental crawling (resume từ last page)
- Batch processing (100 jobs/batch)

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