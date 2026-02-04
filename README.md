# 🇻🇳 Vietnam IT Job Market Analysis - Job Salary Analytics

Dự án phân tích thị trường việc làm IT tại Việt Nam với tập trung vào **phân tích xu hướng lương** và **kỹ năng**. Sử dụng Web Crawling, NLP, Machine Learning và Data Visualization để cung cấp insights chi tiết về thị trường tuyển dụng IT.

## ✨ New Features (Version 2.0)

🎉 **Major Update!** Xem chi tiết tại [NEW_FEATURES.md](NEW_FEATURES.md)

- ✅ **TopCV Crawler** - Mở rộng nguồn dữ liệu với TopCV.vn
- ✅ **Enhanced Dashboard UI/UX** - Thiết kế hiện đại với gradient theme
- ✅ **AI Job Recommendations** - Gợi ý việc làm thông minh dựa trên kỹ năng
- ✅ **Streamlit Cloud Ready** - Deploy lên cloud trong 5 phút

## 🎯 Mục Tiêu Dự Án

- **Crawl dữ liệu**: Thu thập thông tin từ ITViec, TopCV ✨NEW, VietnamWorks
- **Phân tích lương**: Phân tích xu hướng, phân phối và dự đoán mức lương theo vị trí, cấp độ, địa điểm
- **Phân tích kỹ năng**: Trích xuất và phân tích các kỹ năng hot nhất, kỹ năng đi cùng nhau
- **Machine Learning**: Dự đoán lương + Gợi ý việc làm AI ✨NEW
- **Visualization**: Dashboard tương tác hiện đại với 5 trang phân tích ✨NEW

## 🛠 Công Nghệ Sử Dụng

### Web Crawling & Data Collection
- **Selenium** - Browser automation
- **BeautifulSoup4** - HTML parsing  
- **Scrapy** - Advanced web scraping

### Data Processing & Analysis
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing

### NLP & Text Processing
- **NLTK** - Natural language processing
- **spaCy** - Advanced NLP
- **Underthesea** - Vietnamese NLP
- **WordCloud** - Visualization

### Machine Learning
- **Scikit-learn** - ML algorithms
- **XGBoost** - Gradient boosting
- **LightGBM** - Fast gradient boosting
- **CatBoost** - Categorical features

### Data Visualization
- **Matplotlib & Seaborn** - Static plots
- **Plotly** - Interactive charts
- **Streamlit** - Web dashboard

## 📁 Cấu Trúc Dự Án

```
IT-job-analysis-VN-main/
│
├── config/                      # Configuration files
│   └── config.py               # Project configuration
│
├── data_raw/                   # Raw crawled data
│   └── ITViec_data.csv
│
├── data_clean/                 # Cleaned data
│   └── clean_data.csv
│
├── src/                        # Source code
│   ├── crawler/               # Web crawling modules
│   │   └── ITViec_crawling.py
│   │
│   ├── data_processing/       # Data cleaning & processing
│   │   └── processor.py
│   │
│   ├── analysis/              # Analysis modules
│   │   ├── EDA.py
│   │   └── salary_analytics.py
│   │
│   ├── nlp/                   # NLP & skill extraction
│   │   └── skill_analyzer.py
│   │
│   ├── ml_models/             # Machine learning models
│   │   └── salary_prediction.py
│   │
│   └── visualization/         # Visualization & dashboard
│       └── dashboard.py
│
├── models/                     # Trained ML models
│   └── salary_predictor.pkl
│
├── outputs/                    # Analysis outputs
│   ├── salary_distribution.png
│   ├── salary_trends.png
│   ├── feature_importance.png
│   └── reports/
│
├── notebooks/                  # Jupyter notebooks
│   ├── crawling_test.ipynb
│   ├── cleanning_data.ipynb
│   └── eda.ipynb
│
├── docs/                       # Documentation
│
├── main.py                     # Main pipeline
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## 🚀 Hướng Dẫn Cài Đặt & Chạy Dự Án

### Bước 1: Clone Repository & Setup Environment

```bash
# Clone repository
git clone <your-repo-url>
cd IT-job-analysis-VN-main

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Bước 2: Cấu Hình Dự Án

File cấu hình tại `config/config.py` đã được thiết lập sẵn. Bạn có thể tùy chỉnh:
- Đường dẫn thư mục
- Crawler settings
- ML model parameters

### Bước 3: Thu Thập Dữ Liệu (Data Crawling)

```bash
# Crawl data from ITViec
python src/crawler/ITViec_crawling.py

# Chương trình sẽ:
# 1. Mở trình duyệt Chrome
# 2. Yêu cầu bạn đăng nhập ITViec
# 3. Nhấn ENTER để bắt đầu crawl
# 4. Lưu dữ liệu vào data_raw/ITViec_data.csv
```

**Lưu ý**: Crawler có thể cần Chrome Driver. Nếu gặp lỗi, cài đặt:
```bash
pip install webdriver-manager
```

### Bước 4: Chạy Pipeline Phân Tích Hoàn Chỉnh

```bash
# Run toàn bộ pipeline (recommended)
python main.py
```

Pipeline sẽ thực hiện:
1. ✅ Data Processing - Làm sạch và chuẩn hóa dữ liệu
2. ✅ Salary Analysis - Phân tích xu hướng lương
3. ✅ Skill Analysis - Phân tích kỹ năng hot
4. ✅ ML Models - Train mô hình dự đoán lương

### Bước 5: Xem Dashboard Tương Tác

```bash
# Launch Streamlit dashboard
streamlit run src/visualization/dashboard.py
```

Dashboard sẽ mở tại `http://localhost:8501` với các tính năng:
- 💰 Salary Analysis - Phân tích lương theo nhiều chiều
- 📈 Job Market Trends - Xu hướng thị trường
- 🔧 Skills Analysis - Phân tích kỹ năng
- 🌍 Geographic Distribution - Phân bố địa lý
- 🎯 Career Recommendations - Gợi ý nghề nghiệp

## 📊 Các Module Chi Tiết

### 1. Data Processing (`src/data_processing/processor.py`)

```python
from src.data_processing.processor import DataProcessor

processor = DataProcessor()
processor.process_pipeline()
processor.get_summary()
```

Chức năng:
- Clean salary data (chuyển đổi sang VND)
- Categorize skills (phân loại kỹ năng)
- Extract job groups (nhóm công việc)
- Standardize locations (chuẩn hóa địa điểm)
- Remove duplicates

### 2. Salary Analytics (`src/analysis/salary_analytics.py`)

```python
from src.analysis.salary_analytics import SalaryAnalyzer

analyzer = SalaryAnalyzer(df)
report = analyzer.generate_report()
analyzer.plot_salary_distribution()
```

Phân tích:
- Overall salary statistics
- Salary by job group
- Salary by experience level
- Salary by city
- Salary by skill
- Trends over time

### 3. Skill Analyzer (`src/nlp/skill_analyzer.py`)

```python
from src.nlp.skill_analyzer import SkillAnalyzer

analyzer = SkillAnalyzer()
trends = analyzer.analyze_skill_trends(df)
cooccur = analyzer.get_skill_cooccurrence(df)
recommendations = analyzer.generate_skill_recommendations(
    job_group='Backend Developer',
    current_skills=['python', 'django'],
    df=df
)
```

Phân tích:
- Top in-demand skills
- Skill categories (languages, frameworks, tools)
- Skill co-occurrence (kỹ năng đi cùng nhau)
- Skill recommendations

### 4. ML Salary Prediction (`src/ml_models/salary_prediction.py`)

```python
from src.ml_models.salary_prediction import SalaryPredictor

# Train model
predictor = SalaryPredictor()
predictor.train_model(df, model_type='xgboost')
predictor.save_model()

# Predict salary
prediction = predictor.predict_salary(
    job_group='Backend Developer',
    level='senior',
    city='Ho Chi Minh',
    skills=['python', 'django', 'aws', 'docker']
)
print(f"Predicted salary: {prediction['predicted_salary_m']:.2f}M VND")
```

Models:
- Random Forest
- Gradient Boosting
- XGBoost ⭐ (Best performance)
- LightGBM

## 📈 Kết Quả Phân Tích

### Thống Kê Tổng Quan
- **Tổng số việc làm**: ~1,000+ positions
- **Job groups**: 15+ nhóm công việc
- **Mức lương trung bình**: 20-40M VND
- **Top job groups**: Backend Developer, Frontend Developer, Data/AI

### Top In-Demand Skills
1. **Programming Languages**: Python, Java, JavaScript, TypeScript
2. **Frameworks**: React, Vue, Django, Spring Boot
3. **Tools & DevOps**: Docker, Kubernetes, AWS, Git
4. **Data & AI**: Machine Learning, TensorFlow, Pandas

### Salary Insights
- **Backend Developer (Senior)**: 30-50M VND
- **Data/AI Engineer**: 35-60M VND
- **DevOps Engineer**: 30-55M VND
- **Frontend Developer (Mid)**: 20-35M VND

### Top Paying Skills
- Cloud (AWS, Azure, GCP): +30%
- Machine Learning/AI: +25%
- Kubernetes: +20%
- Golang: +15%

## 🎓 Hướng Dẫn Phát Triển Thêm

### Mở Rộng Crawler
```python
# Add more job sites
# src/crawler/topcv_crawling.py
# src/crawler/vietnamworks_crawling.py
```

### Thêm Feature Mới
```python
# Add new features to ML model
# In salary_prediction.py
def prepare_features(self, df):
    # Add company size feature
    features['company_size'] = ...
    # Add years of experience
    features['years_exp'] = ...
```

### Custom Analysis
```python
# Create custom analysis in notebooks/
# Example: Industry-specific analysis
industry_df = df[df['domain_group'] == 'Finance']
analyze_finance_jobs(industry_df)
```

## 🐛 Troubleshooting

### Lỗi crawling
```bash
# Cài lại webdriver-manager
pip install --upgrade webdriver-manager
```

### Lỗi encoding
```bash
# Đọc file với encoding UTF-8
df = pd.read_csv('data.csv', encoding='utf-8-sig')
```

### Lỗi dependencies
```bash
# Cài lại tất cả dependencies
pip install -r requirements.txt --force-reinstall
```

## 📚 Tài Liệu Tham Khảo

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)

## 👥 Đóng Góp

Mọi đóng góp đều được hoan nghênh! Vui lòng:
1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License.

## 📧 Contact

Nếu có câu hỏi, vui lòng mở Issue trên GitHub.

---

**Made with ❤️ by Vietnam IT Job Market Analysis Team**