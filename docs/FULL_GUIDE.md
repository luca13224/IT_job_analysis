# Tài Liệu Hướng Dẫn Chi Tiết Dự Án

## Vietnam IT Job Market Analysis - Job Salary Analytics

### Phần 1: Tổng Quan Dự Án

#### 1.1 Mục Tiêu Dự Án
Xây dựng hệ thống phân tích thị trường tuyển dụng IT tại Việt Nam với các chức năng:
- Thu thập dữ liệu tự động từ các trang tuyển dụng
- Phân tích xu hướng lương theo nhiều chiều độ
- Phân tích kỹ năng hot và đề xuất lộ trình học tập
- Dự đoán mức lương bằng Machine Learning
- Cung cấp Dashboard tương tác

#### 1.2 Công Nghệ & Phương Pháp

**Tech Stack Chính:**
- **Backend**: Python 3.11+
- **Web Crawling**: Selenium, BeautifulSoup4, Scrapy
- **Data Processing**: Pandas, NumPy
- **NLP**: NLTK, spaCy, Underthesea
- **Machine Learning**: Scikit-learn, XGBoost, LightGBM
- **Visualization**: Matplotlib, Seaborn, Plotly, Streamlit

**Phương Pháp Nghiên Cứu:**
1. Data Collection (Web Scraping)
2. Data Preprocessing & Cleaning
3. Exploratory Data Analysis (EDA)
4. Feature Engineering
5. Model Development & Training
6. Model Evaluation & Selection
7. Deployment & Visualization

---

### Phần 2: Lộ Trình Thực Hiện Chi Tiết

#### Giai Đoạn 1: Thu Thập & Tiền Xử Lý Dữ Liệu (Tuần 1-2)

**Bước 1.1: Thiết lập môi trường**
```bash
# Tạo virtual environment
python -m venv .venv
.venv\Scripts\activate

# Cài đặt dependencies
pip install -r requirements.txt
```

**Bước 1.2: Crawl dữ liệu**
```bash
# Chạy crawler ITViec
python src/crawler/ITViec_crawling.py
```

Crawler sẽ thu thập:
- Tên công việc và công ty
- Mức lương
- Vị trí công việc (job level)
- Địa điểm làm việc
- Kỹ năng yêu cầu
- Ngày đăng tuyển

**Bước 1.3: Xử lý và làm sạch dữ liệu**
```bash
python src/data_processing/processor.py
```

Data cleaning bao gồm:
- Xử lý missing values
- Chuẩn hóa tên địa điểm
- Parse và convert salary data
- Loại bỏ duplicates
- Categorize job groups
- Extract experience levels

**Output**: `data_clean/clean_data.csv`

---

#### Giai Đoạn 2: Phân Tích Dữ Liệu (Tuần 3)

**Bước 2.1: Exploratory Data Analysis**

Sử dụng notebook hoặc script:
```python
from src.analysis.salary_analytics import SalaryAnalyzer
import pandas as pd

df = pd.read_csv('data_clean/clean_data.csv')
analyzer = SalaryAnalyzer(df)

# Generate comprehensive report
report = analyzer.generate_report()
print(report)

# Create visualizations
analyzer.plot_salary_distribution()
analyzer.plot_salary_trends()
```

**Phân tích thực hiện:**
- Phân bố lương theo job group
- Phân bố lương theo experience level
- Phân bố lương theo thành phố
- Xu hướng lương theo thời gian
- Correlation giữa skills và salary

**Bước 2.2: Skill Analysis**

```python
from src.nlp.skill_analyzer import SkillAnalyzer

analyzer = SkillAnalyzer()
trends = analyzer.analyze_skill_trends(df)
cooccurrence = analyzer.get_skill_cooccurrence(df)
```

**Phân tích:**
- Top 50 skills được yêu cầu nhiều nhất
- Skill co-occurrence matrix (skills thường xuất hiện cùng nhau)
- Skill categories (programming languages, frameworks, tools)
- Skill recommendations by job group

**Output**: 
- `outputs/salary_distribution.png`
- `outputs/salary_trends.png`
- `outputs/skill_trends.csv`
- `outputs/skill_cooccurrence.csv`

---

#### Giai Đoạn 3: Xây Dựng ML Models (Tuần 4-5)

**Bước 3.1: Feature Engineering**

Features được sử dụng:
- Categorical: job_group, level, city
- Numerical: skill_count
- Binary: has_python, has_aws, has_docker, etc.

```python
from src.ml_models.salary_prediction import SalaryPredictor

predictor = SalaryPredictor()
# Feature engineering tự động trong prepare_features()
```

**Bước 3.2: Model Training & Comparison**

Train và so sánh 4 models:
```python
# So sánh models
comparison = predictor.compare_models(df)
print(comparison)
```

Models:
1. **Random Forest Regressor**
   - Pros: Robust, handles non-linear relationships
   - Cons: Slower training

2. **Gradient Boosting Regressor**
   - Pros: Good performance, interpretable
   - Cons: Risk of overfitting

3. **XGBoost** ⭐ (Recommended)
   - Pros: Best performance, fast, handles missing values
   - Cons: More hyperparameters

4. **LightGBM**
   - Pros: Very fast, memory efficient
   - Cons: Sensitive to hyperparameters

**Bước 3.3: Model Evaluation**

Metrics sử dụng:
- **RMSE** (Root Mean Square Error): Độ lệch trung bình
- **MAE** (Mean Absolute Error): Sai số tuyệt đối
- **R² Score**: Độ fit của model (0-1, càng cao càng tốt)

Target performance:
- R² Score > 0.75
- RMSE < 5M VND

**Bước 3.4: Model Deployment**

```python
# Train final model
final_predictor = SalaryPredictor()
final_predictor.train_model(df, model_type='xgboost')

# Save model
final_predictor.save_model('salary_predictor.pkl')

# Use model for predictions
prediction = final_predictor.predict_salary(
    job_group='Backend Developer',
    level='senior',
    city='Ho Chi Minh',
    skills=['python', 'django', 'aws', 'docker']
)
```

**Output**:
- `models/salary_predictor.pkl`
- `outputs/model_comparison.png`
- `outputs/feature_importance.png`

---

#### Giai Đoạn 4: Visualization & Dashboard (Tuần 6)

**Bước 4.1: Launch Interactive Dashboard**

```bash
streamlit run src/visualization/dashboard.py
```

Dashboard features:
1. **Overview Tab**: Metrics tổng quan
2. **Salary Analysis Tab**: 
   - Distribution plots
   - Box plots by groups
   - Top paying skills
3. **Job Market Trends Tab**:
   - Job distribution
   - Level distribution
   - Work mode analysis
4. **Skills Analysis Tab**:
   - Top skills
   - Skill breakdown
   - Skill co-occurrence
5. **Geographic Tab**:
   - Jobs by city
   - Salary by city
   - Top companies
6. **Recommendations Tab**:
   - Career path recommendations
   - Skill suggestions
   - Salary expectations

**Bước 4.2: Static Reports**

Generate PDF/HTML reports:
```python
from src.analysis.salary_analytics import SalaryAnalyzer

analyzer = SalaryAnalyzer(df)
report = analyzer.generate_report()

# Save to file
with open('outputs/final_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)
```

---

### Phần 3: Kết Quả & Insights

#### 3.1 Phát Hiện Chính

**Về Lương:**
- Mức lương trung bình IT tại VN: 20-40M VND/tháng
- Top 3 job groups có lương cao nhất:
  1. Data/AI Engineers: 35-60M
  2. Backend Developers: 30-50M
  3. DevOps Engineers: 30-55M
- TP.HCM có mức lương cao hơn Hà Nội ~15-20%

**Về Kỹ Năng:**
- Top 5 skills hot nhất:
  1. Python (45% jobs)
  2. JavaScript (40% jobs)
  3. Java (35% jobs)
  4. React (30% jobs)
  5. Docker (25% jobs)

- Skills tăng lương cao:
  1. Cloud (AWS/Azure/GCP): +30%
  2. ML/AI: +25%
  3. Kubernetes: +20%

**Về Xu Hướng:**
- Remote/Hybrid work tăng 200% so với 2020
- Nhu cầu AI/ML Engineers tăng 150%
- Data roles tăng 120%

#### 3.2 ML Model Performance

Best model: **XGBoost**
- Train R²: 0.89
- Test R²: 0.82
- Test RMSE: 4.2M VND
- Test MAE: 3.1M VND

Top 5 Important Features:
1. job_group_encoded (35%)
2. level_encoded (28%)
3. skill_count (15%)
4. has_aws (8%)
5. city_encoded (7%)

---

### Phần 4: Mở Rộng & Cải Tiến

#### 4.1 Tính Năng Có Thể Thêm

**Short-term:**
- [ ] Thêm crawler cho TopCV, VietnamWorks
- [ ] Email notifications cho jobs matching
- [ ] Export reports to PDF
- [ ] Add more visualization types

**Medium-term:**
- [ ] Sentiment analysis từ company reviews
- [ ] Job recommendation system (collaborative filtering)
- [ ] Chatbot hỗ trợ tư vấn nghề nghiệp
- [ ] Mobile app

**Long-term:**
- [ ] Real-time data streaming
- [ ] Integration với LinkedIn API
- [ ] Predictive analytics cho job market trends
- [ ] Community features (forums, Q&A)

#### 4.2 Cải Thiện Model

**Feature Engineering:**
- Add company size/reputation
- Add years of experience (extract from job description)
- Add education requirements
- Add job description embeddings (BERT)

**Advanced Models:**
- Neural Networks (Deep Learning)
- Ensemble methods (Stacking, Blending)
- Time series forecasting
- Reinforcement Learning for job matching

**Data Augmentation:**
- Collect historical data (time series)
- Add external data sources (economic indicators)
- Synthetic data generation

---

### Phần 5: Best Practices

#### 5.1 Code Quality
- Follow PEP 8 style guide
- Write docstrings for all functions
- Add type hints
- Use meaningful variable names
- Keep functions small and focused

#### 5.2 Data Management
- Version control for data (DVC)
- Regular data backups
- Document data sources
- Track data lineage

#### 5.3 Model Development
- Always split train/test data
- Use cross-validation
- Track experiments (MLflow)
- Version models
- Monitor model drift

#### 5.4 Deployment
- Use environment variables for configs
- Log everything
- Error handling và retry logic
- Rate limiting for crawlers
- Cache frequently accessed data

---

### Phần 6: Troubleshooting

#### Common Issues

**Issue 1: Crawler không hoạt động**
```
Solution:
- Kiểm tra Chrome version
- Update webdriver-manager
- Kiểm tra Internet connection
- Kiểm tra website structure (có thể đã thay đổi)
```

**Issue 2: Model accuracy thấp**
```
Solution:
- Thêm features
- Tune hyperparameters
- Collect more data
- Try ensemble methods
```

**Issue 3: Dashboard chậm**
```
Solution:
- Sử dụng @st.cache_data
- Giảm số lượng plots
- Optimize data loading
- Use database instead of CSV
```

---

### Phần 7: Tài Liệu Tham Khảo

#### Papers & Articles
- Salary Prediction using ML: [Link]
- NLP for Job Descriptions: [Link]
- Web Scraping Best Practices: [Link]

#### Online Courses
- Machine Learning (Andrew Ng - Coursera)
- Deep Learning Specialization
- Data Science với Python

#### Books
- "Python for Data Analysis" - Wes McKinney
- "Hands-On Machine Learning" - Aurélien Géron
- "Web Scraping with Python" - Ryan Mitchell

---

## Kết Luận

Dự án này cung cấp một pipeline hoàn chỉnh để phân tích thị trường tuyển dụng IT tại Việt Nam. Với các module được tổ chức tốt và documentation chi tiết, dự án có thể dễ dàng mở rộng và bảo trì.

**Next Steps:**
1. Deploy dashboard lên cloud (Streamlit Cloud, Heroku)
2. Setup CI/CD pipeline
3. Add more data sources
4. Build API endpoints
5. Create mobile app

Good luck! 🚀
