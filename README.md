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

## 🔄 Data Pipeline - Logic hoạt động

### 📊 Tổng quan luồng dữ liệu

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Crawling  │ --> │  Processing  │ --> │   Analysis   │ --> │    Dash UI   │
│  (Selenium) │     │   (Pandas)   │     │   (ML/NLP)   │     │  (Streamlit) │
└─────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
     1,141 jobs         Clean data         Insights/Models      10 pages
```

---

### 1️⃣ **Web Crawling** - Thu thập dữ liệu

**File:** `src/crawler/ITViec_crawling.py`

**Logic hoạt động:**

```python
# Bước 1: Khởi tạo Selenium WebDriver
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://itviec.com/it-jobs")

# Bước 2: Đăng nhập thủ công (để bypass Cloudflare)
# User đăng nhập → Nhấn Enter → Script bắt đầu crawl

# Bước 3: Lặp qua từng trang (pagination)
for page in range(1, total_pages + 1):
    # Scroll để load dynamic content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    
    # Lấy danh sách job cards
    job_cards = driver.find_elements(By.CSS_SELECTOR, ".job-card")
    
    # Bước 4: Lặp qua từng job
    for card in job_cards:
        job_url = card.find_element(By.TAG_NAME, "a").get_attribute("href")
        
        # Mở job detail page
        driver.get(job_url)
        
        # Bước 5: Extract thông tin chi tiết
        job_data = {
            "job_titles": driver.find_element(By.CLASS_NAME, "job-title").text,
            "company_names": driver.find_element(By.CLASS_NAME, "company-name").text,
            "salary": driver.find_element(By.CLASS_NAME, "salary").text,
            "level": driver.find_element(By.CLASS_NAME, "level").text,
            "city": driver.find_element(By.CLASS_NAME, "address").text,
            "skills": [skill.text for skill in driver.find_elements(By.CLASS_NAME, "skill-tag")],
            "job_description": driver.find_element(By.CLASS_NAME, "job-desc").text
        }
        
        # Bước 6: Lưu vào CSV ngay lập tức (tránh mất dữ liệu)
        save_to_csv(job_data, "data_raw/ITViec_data.csv")
        
        # Chờ random 1-3s để tránh bị block
        time.sleep(random.uniform(1, 3))
```

**Kỹ thuật quan trọng:**
- ✅ **Dynamic scroll**: Load AJAX content
- ✅ **Random delays**: Tránh bị detect bot (1-3s mỗi request)
- ✅ **Resume crawling**: Lưu `current_page.txt` để tiếp tục nếu crash
- ✅ **Error handling**: Try-catch cho từng element, log lỗi
- ✅ **Incremental save**: Lưu từng job ngay lập tức (không đợi hết)

**Output:** `data_raw/ITViec_data.csv` (1,141 rows)

---

### 2️⃣ **Data Processing** - Làm sạch & chuẩn hóa

**File:** `src/data_processing/processor.py`

**Logic hoạt động:**

```python
import pandas as pd
import re

# Bước 1: Load raw data
df = pd.read_csv("data_raw/ITViec_data.csv")

# Bước 2: Clean salary (chuyển về VND số)
def clean_salary(text):
    # "Up to $2,000" → 46,000,000 VND (tỷ giá 23,000)
    # "1000 - 1500 USD" → 23,000,000 VND (lấy trung bình)
    # "Negotiable" → NaN
    
    if "negotiable" in text.lower():
        return None
    
    # Extract numbers
    numbers = re.findall(r'\d+', text.replace(',', ''))
    
    # Check currency
    if "$" in text or "USD" in text:
        avg = sum([int(n) for n in numbers]) / len(numbers)
        return avg * 23_000  # Convert to VND
    else:
        avg = sum([int(n) for n in numbers]) / len(numbers)
        return avg * 1_000_000  # Already in triệu → full number

df['salary_numeric'] = df['salary'].apply(clean_salary)

# Bước 3: Parse skills array
def parse_skills(text):
    # "['Python', 'Django', 'AWS']" → list object
    try:
        return ast.literal_eval(text)
    except:
        return []

df['array_skills'] = df['skills'].apply(parse_skills)

# Bước 4: Categorize job groups
def categorize_job(title):
    title_lower = title.lower()
    
    if any(word in title_lower for word in ['backend', 'java', 'python', 'golang']):
        return 'Backend Developer'
    elif any(word in title_lower for word in ['frontend', 'react', 'vue', 'angular']):
        return 'Frontend Developer'
    elif any(word in title_lower for word in ['fullstack', 'full stack', 'full-stack']):
        return 'Fullstack Developer'
    elif any(word in title_lower for word in ['data', 'ai', 'ml', 'machine learning']):
        return 'Data / AI'
    # ... more categories
    else:
        return 'Other'

df['job_group'] = df['job_titles'].apply(categorize_job)

# Bước 5: Standardize locations
def clean_city(text):
    if 'hồ chí minh' in text.lower() or 'hcm' in text.lower():
        return 'Hồ Chí Minh'
    elif 'hà nội' in text.lower() or 'hanoi' in text.lower():
        return 'Hà Nội'
    # ... more cities
    else:
        return text

df['city'] = df['city'].apply(clean_city)

# Bước 6: Remove duplicates
df = df.drop_duplicates(subset=['job_titles', 'company_names'])

# Bước 7: Save clean data
df.to_csv("data_clean/clean_data.csv", index=False, encoding='utf-8-sig')
```

**Transformations:**
- ✅ **Salary normalization**: USD → VND, text → number
- ✅ **Skills extraction**: String → List
- ✅ **Job categorization**: Title → Group (Backend/Frontend/etc)
- ✅ **Location standardization**: Various formats → Consistent names
- ✅ **Deduplication**: Remove same job posted multiple times

**Output:** `data_clean/clean_data.csv` (1,141 rows cleaned)

---

### 3️⃣ **ML Models** - AI Job Recommendations

**File:** `src/ml_models/job_recommender.py`

**Logic hoạt động (TF-IDF + Cosine Similarity):**

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Bước 1: Build TF-IDF Matrix
# Chuyển skills của mỗi job thành text
skills_texts = []
for job in jobs:
    # ['Python', 'Django', 'AWS'] → "python django aws"
    skills_texts.append(' '.join(job['skills']).lower())

# Tạo TF-IDF vectors
vectorizer = TfidfVectorizer(max_features=200)
tfidf_matrix = vectorizer.fit_transform(skills_texts)
# Shape: (1141 jobs, 200 features)

# Bước 2: User input skills
user_skills = ['python', 'django', 'docker']
user_text = ' '.join(user_skills)

# Bước 3: Transform user skills to vector
user_vector = vectorizer.transform([user_text])
# Shape: (1, 200)

# Bước 4: Calculate similarity với TẤT CẢ jobs
similarities = cosine_similarity(user_vector, tfidf_matrix)
# Shape: (1, 1141)

# Bước 5: Rank jobs theo similarity score
df['match_score'] = similarities[0] * 100  # Convert to percentage

# Bước 6: Apply filters
filtered = df[
    (df['match_score'] > 0) &  # Có ít nhất 1 skill match
    (df['level'] == 'mid') &   # Filter by level
    (df['city'] == 'Hồ Chí Minh')  # Filter by city
]

# Bước 7: Sort và return top N
recommendations = filtered.nlargest(10, 'match_score')
```

**Giải thích TF-IDF:**
- **TF (Term Frequency)**: Skill xuất hiện bao nhiêu lần trong job
- **IDF (Inverse Document Frequency)**: Skill hiếm → score cao hơn
- **Cosine Similarity**: Góc giữa 2 vectors (0-1, 1 = giống nhất)

**Ví dụ matching:**
```
User: ['Python', 'Django', 'AWS']

Job A: ['Python', 'Django', 'PostgreSQL', 'Redis']
→ Match: Python ✓, Django ✓ → Score: 75%

Job B: ['Java', 'Spring Boot', 'MySQL']
→ Match: None → Score: 0%

Job C: ['Python', 'Django', 'AWS', 'Docker', 'K8s']
→ Match: Python ✓, Django ✓, AWS ✓ → Score: 92%
```

---

### 4️⃣ **NLP Analysis** - Skill Extraction & Trends

**File:** `src/nlp/skill_analyzer.py`

**Logic hoạt động:**

```python
from collections import Counter

# Bước 1: Flatten all skills
all_skills = []
for job in jobs:
    all_skills.extend(job['skills'])

# Bước 2: Count frequency
skill_counts = Counter(all_skills)

# Top 20: [('Python', 450), ('JavaScript', 380), ...]

# Bước 3: Skill co-occurrence (skills đi cùng nhau)
from itertools import combinations

cooccur = Counter()
for job in jobs:
    # Tạo tất cả pairs từ skills của job
    for skill1, skill2 in combinations(job['skills'], 2):
        pair = tuple(sorted([skill1, skill2]))
        cooccur[pair] += 1

# Top pairs: [('Python', 'Django'), ('React', 'TypeScript'), ...]

# Bước 4: Skill recommendations
def recommend_skills(current_skills):
    # Find jobs có current_skills
    similar_jobs = [job for job in jobs 
                    if any(s in job['skills'] for s in current_skills)]
    
    # Extract other skills from those jobs
    other_skills = []
    for job in similar_jobs:
        other_skills.extend([s for s in job['skills'] 
                            if s not in current_skills])
    
    # Return top suggested skills
    return Counter(other_skills).most_common(10)
```

---

### 5️⃣ **Visualization** - Interactive Dashboard

**File:** `src/visualization/dashboard_v2.py`

**Architecture:**

```python
import streamlit as st
import plotly.express as px

# Bước 1: Load data (cached)
@st.cache_data
def load_data():
    return pd.read_csv("data_clean/clean_data.csv")

df = load_data()

# Bước 2: Sidebar filters
job_group = st.sidebar.selectbox("Job Group", df['job_group'].unique())
level = st.sidebar.selectbox("Level", df['level'].unique())

# Bước 3: Filter data
filtered = df[
    (df['job_group'] == job_group) &
    (df['level'] == level)
]

# Bước 4: Show metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Jobs", len(filtered))
col2.metric("Avg Salary", f"{filtered['salary_numeric'].mean()/1e6:.1f}M")
col3.metric("Companies", filtered['company_names'].nunique())

# Bước 5: Interactive charts
fig = px.bar(filtered['city'].value_counts(), 
             title="Jobs by City")
st.plotly_chart(fig)

# Bước 6: Job recommendations
user_skills = st.multiselect("Your Skills", all_skills)
if user_skills:
    recommender = JobRecommender()
    recommendations = recommender.recommend_by_skills(user_skills, top_n=10)
    
    for job in recommendations:
        st.markdown(f"**{job['job_titles']}** - Match: {job['match_score']:.0f}%")
```

**10 Pages:**
1. **Overview**: Metrics + charts tổng quan
2. **Market Analysis**: Job distribution, trends
3. **Recommendations**: AI matching với user skills
4. **Salary Insights**: Salary ranges, percentiles
5. **Skills Analysis**: Top skills, co-occurrence
6. **Demo Scenarios**: 5 pre-built personas
7. **Career Simulator**: 5-10 year projection
8. **Compare Tool**: Side-by-side comparison
9. **Export**: Download Excel/CSV/JSON
10. **AI Chatbot**: Q&A về market

---

### 6️⃣ **Career Simulator** - Salary Projection

**File:** `src/visualization/career_simulator.py`

**Logic hoạt động:**

```python
# Input: Backend Developer, Fresher, 5 years
job_group = "Backend Developer"
current_level = "fresher"
years = 5

# Career progression: fresher → junior → mid → senior
levels = ['fresher', 'junior', 'mid', 'senior']
current_idx = levels.index(current_level)

# Simulate progression (avg 2 years per level)
timeline = []
for year in range(years + 1):
    level_idx = min(current_idx + (year // 2), len(levels) - 1)
    level = levels[level_idx]
    
    # Get salary data for this level
    salary_data = df[
        (df['job_group'] == job_group) &
        (df['level'] == level) &
        (df['salary_numeric'].notna())
    ]
    
    avg_salary = salary_data['salary_numeric'].mean()
    min_salary = salary_data['salary_numeric'].quantile(0.25)
    max_salary = salary_data['salary_numeric'].quantile(0.75)
    
    timeline.append({
        'year': year,
        'level': level,
        'avg_salary': avg_salary,
        'range': (min_salary, max_salary)
    })

# Visualize timeline với Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=[t['year'] for t in timeline],
    y=[t['avg_salary']/1e6 for t in timeline],
    mode='lines+markers',
    name='Projected Salary'
))
st.plotly_chart(fig)
```

---

### 7️⃣ **AI Chatbot** - Q&A System

**File:** `src/visualization/chatbot.py`

**Logic hoạt động:**

```python
# Bước 1: Detect intent từ user question
question = "Lương Backend Developer là bao nhiêu?"

# Bước 2: Keyword matching
if any(word in question for word in ['lương', 'salary']):
    intent = 'salary'
elif any(word in question for word in ['kỹ năng', 'skill']):
    intent = 'skills'
# ... more intents

# Bước 3: Extract entities
if 'backend' in question:
    job_group = 'Backend Developer'

# Bước 4: Query data
if intent == 'salary':
    salary_data = df[df['job_group'] == job_group]['salary_numeric']
    
    response = f"""
    **Backend Developer Salary:**
    - Average: {salary_data.mean()/1e6:.1f}M VND
    - Median: {salary_data.median()/1e6:.1f}M VND
    - Range: {salary_data.min()/1e6:.1f}M - {salary_data.max()/1e6:.1f}M
    """

# Bước 5: Display response
st.chat_message("assistant").markdown(response)
```

---

## 📈 Performance & Scalability

**Current Stats:**
- 📊 Dataset: 1,141 jobs
- ⚡ Dashboard load time: ~2-3s (với caching)
- 🚀 TF-IDF build: ~0.5s
- 💾 Memory usage: ~50MB

**Optimization techniques:**
- `@st.cache_data`: Cache loaded data
- `@st.cache_resource`: Cache ML models
- Incremental crawling: Resume từ last page
- Batch processing: Process 100 jobs at a time

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