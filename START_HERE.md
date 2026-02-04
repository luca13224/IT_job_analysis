# 🎯 BẮT ĐẦU TỪ ĐÂY - START HERE

## Chào mừng đến với Vietnam IT Job Market Analysis!

### 📚 Tài Liệu Dự Án

Dự án có 4 file tài liệu chính, đọc theo thứ tự:

1. **README.md** ⭐ (Đọc đầu tiên)
   - Tổng quan dự án
   - Công nghệ sử dụng
   - Cấu trúc dự án
   - Hướng dẫn cài đặt cơ bản

2. **QUICKSTART.md** 🚀 (Đọc thứ hai)
   - Hướng dẫn nhanh 3 bước
   - Workflow đề xuất
   - Tips & tricks
   - Troubleshooting

3. **PROJECT_SUMMARY.md** 📋 (Đọc để hiểu chi tiết)
   - Tóm tắt toàn bộ dự án
   - Các modules đã xây dựng
   - Kết quả phân tích
   - Checklist hoàn thành

4. **docs/FULL_GUIDE.md** 📖 (Đọc khi cần tài liệu chi tiết)
   - Hướng dẫn đầy đủ từng giai đoạn
   - Phương pháp nghiên cứu
   - Best practices
   - Ý tưởng mở rộng

---

## ⚡ Quick Start (3 Phút)

### Bước 1: Cài đặt
```bash
pip install -r requirements.txt
```

### Bước 2: Chạy Pipeline
```bash
# Option A: Dùng script
run.bat

# Option B: Chạy trực tiếp
python main.py
```

### Bước 3: Xem Dashboard
```bash
streamlit run src/visualization/dashboard.py
```

Xong! Dashboard sẽ mở tại http://localhost:8501

---

## 📁 Cấu Trúc Thư Mục

```
IT-job-analysis-VN-main/
│
├── 📄 README.md              ← Đọc đầu tiên
├── 📄 QUICKSTART.md          ← Hướng dẫn nhanh
├── 📄 PROJECT_SUMMARY.md     ← Tóm tắt dự án
├── 📄 START_HERE.md          ← File này
├── 🔧 requirements.txt       ← Dependencies
├── ⚙️ config/                ← Configuration
├── 📊 data_raw/              ← Raw data
├── 📊 data_clean/            ← Cleaned data
├── 💻 src/                   ← Source code
│   ├── crawler/             ← Web crawling
│   ├── data_processing/     ← Data cleaning
│   ├── analysis/            ← Analysis
│   ├── nlp/                 ← NLP & skills
│   ├── ml_models/           ← ML models
│   └── visualization/       ← Dashboard
├── 🤖 models/                ← Trained models
├── 📈 outputs/               ← Results
├── 📓 notebooks/             ← Jupyter notebooks
└── 📚 docs/                  ← Documentation
```

---

## 🎯 Các Module Chính

### 1. Crawler (Thu thập dữ liệu)
```bash
python src/crawler/ITViec_crawling.py
```
- Thu thập jobs từ ITViec
- Tự động lưu vào data_raw/

### 2. Data Processing (Xử lý dữ liệu)
```bash
python src/data_processing/processor.py
```
- Clean và chuẩn hóa dữ liệu
- Output: data_clean/clean_data.csv

### 3. Analysis (Phân tích)
```bash
python src/analysis/salary_analytics.py
```
- Phân tích xu hướng lương
- Tạo charts và reports

### 4. NLP (Phân tích kỹ năng)
```bash
python src/nlp/skill_analyzer.py
```
- Trích xuất và phân tích skills
- Top skills, co-occurrence

### 5. ML Models (Dự đoán lương)
```bash
python src/ml_models/salary_prediction.py
```
- Train 4 ML models
- So sánh performance
- Save best model

### 6. Dashboard (Visualization)
```bash
streamlit run src/visualization/dashboard.py
```
- Interactive web dashboard
- Multiple charts và filters

---

## 🎮 Cách Sử Dụng run.bat

Double-click `run.bat` để mở menu:

```
1. Run Data Processing         ← Xử lý dữ liệu
2. Run Salary Analysis          ← Phân tích lương
3. Run Skill Analysis           ← Phân tích kỹ năng
4. Train ML Models              ← Train models
5. Run Complete Pipeline ⭐     ← Chạy tất cả
6. Launch Dashboard             ← Mở dashboard
7. Crawl New Data               ← Crawl dữ liệu mới
8. Install Dependencies         ← Cài dependencies
```

---

## 💡 Use Cases

### Use Case 1: Phân tích thị trường IT
```bash
python main.py              # Run full analysis
streamlit run src/visualization/dashboard.py
```

### Use Case 2: Dự đoán lương
```python
from src.ml_models.salary_prediction import SalaryPredictor

predictor = SalaryPredictor()
predictor.load_model()

result = predictor.predict_salary(
    job_group='Backend Developer',
    level='senior',
    city='Ho Chi Minh',
    skills=['python', 'django', 'aws', 'docker']
)

print(f"Predicted: {result['predicted_salary_m']:.2f}M VND")
```

### Use Case 3: Tìm skills cần học
```python
from src.nlp.skill_analyzer import SkillAnalyzer
import pandas as pd

df = pd.read_csv('data_clean/clean_data.csv')
analyzer = SkillAnalyzer()

recommendations = analyzer.generate_skill_recommendations(
    job_group='Backend Developer',
    current_skills=['python', 'django'],
    df=df
)
```

---

## 🐛 Troubleshooting

### Lỗi: Module not found
```bash
pip install -r requirements.txt
```

### Lỗi: File not found
```bash
# Chạy data processing trước
python src/data_processing/processor.py
```

### Lỗi: Crawler không hoạt động
```bash
pip install --upgrade webdriver-manager
```

### Dashboard chạy chậm
```python
# Trong dashboard.py, thêm @st.cache_data
@st.cache_data
def load_data():
    return pd.read_csv('data_clean/clean_data.csv')
```

---

## 📞 Cần Trợ Giúp?

1. **Đọc Documentation**
   - README.md
   - QUICKSTART.md
   - docs/FULL_GUIDE.md

2. **Check Code Examples**
   - notebooks/ folder
   - test_quick.py

3. **Troubleshooting**
   - Xem phần Troubleshooting trong README.md
   - Xem QUICKSTART.md

---

## 🎓 Learning Path

Nếu bạn là người mới:

**Week 1: Basic Setup**
- Cài đặt dependencies
- Hiểu cấu trúc dự án
- Chạy data processing
- Xem dashboard

**Week 2: Data Analysis**
- Học cách dùng Pandas
- Chạy salary analytics
- Chạy skill analysis
- Tạo custom charts

**Week 3: Machine Learning**
- Hiểu về ML models
- Train models
- Evaluate performance
- Make predictions

**Week 4: Customization**
- Thêm features mới
- Customize dashboard
- Add new analysis
- Deploy project

---

## 🚀 Next Steps

Sau khi làm quen với dự án:

1. **Explore Data**
   ```bash
   jupyter notebook
   # Mở notebooks/eda.ipynb
   ```

2. **Customize Analysis**
   - Thêm charts mới trong dashboard
   - Tạo analysis riêng

3. **Improve Models**
   - Thêm features
   - Tune hyperparameters
   - Try deep learning

4. **Deploy**
   - Deploy dashboard lên Streamlit Cloud
   - Tạo API với FastAPI
   - Build mobile app

---

## ✨ Features Highlights

✅ **Automated Data Collection** - Web crawler
✅ **Comprehensive Analysis** - Salary, skills, trends
✅ **Machine Learning** - 4 models, salary prediction
✅ **Interactive Dashboard** - Streamlit web app
✅ **NLP Processing** - 200+ skills extraction
✅ **Full Documentation** - Vietnamese & English
✅ **Production Ready** - Modular, tested, documented

---

## 🎉 Bắt Đầu Ngay!

```bash
# 1. Clone repo (if needed)
git clone <repo-url>
cd IT-job-analysis-VN-main

# 2. Install
pip install -r requirements.txt

# 3. Run
python main.py

# 4. View
streamlit run src/visualization/dashboard.py
```

**Chúc bạn phân tích thành công!** 🎊

---

*Made with ❤️ for Vietnam IT Job Market Analysis*
