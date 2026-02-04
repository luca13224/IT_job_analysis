# 🚀 Quick Start Guide

## Cách Sử Dụng Nhanh

### Option 1: Sử dụng Script (Recommended cho Windows)

```bash
# Double-click vào file run.bat
# Hoặc chạy từ command line:
run.bat
```

Menu sẽ hiển thị các tùy chọn:
1. Run Data Processing
2. Run Salary Analysis  
3. Run Skill Analysis
4. Train ML Models
5. **Run Complete Pipeline** ⭐ (Chạy tất cả)
6. Launch Dashboard
7. Crawl New Data
8. Install Dependencies

### Option 2: Chạy Từng Module

#### 1. Xử lý dữ liệu
```bash
python src/data_processing/processor.py
```

#### 2. Phân tích lương
```bash
python src/analysis/salary_analytics.py
```

#### 3. Phân tích kỹ năng
```bash
python src/nlp/skill_analyzer.py
```

#### 4. Train ML models
```bash
python src/ml_models/salary_prediction.py
```

#### 5. Chạy toàn bộ pipeline
```bash
python main.py
```

#### 6. Launch dashboard
```bash
streamlit run src/visualization/dashboard.py
```

### Option 3: Dùng Notebook

Mở Jupyter Notebook:
```bash
jupyter notebook
```

Sau đó mở các notebook trong thư mục `notebooks/`:
- `eda.ipynb` - Exploratory Data Analysis
- `cleanning_data.ipynb` - Data Cleaning
- `crawling_test.ipynb` - Test Crawler

---

## Workflow Đề Xuất

### Lần đầu setup:

1. **Cài đặt dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Crawl dữ liệu** (nếu chưa có)
   ```bash
   python src/crawler/ITViec_crawling.py
   ```
   - Đăng nhập ITViec khi browser mở
   - Nhấn ENTER để bắt đầu crawl

3. **Chạy complete pipeline**
   ```bash
   python main.py
   ```
   Hoặc dùng `run.bat` → chọn option 5

4. **Xem kết quả trong Dashboard**
   ```bash
   streamlit run src/visualization/dashboard.py
   ```
   Hoặc dùng `run.bat` → chọn option 6

### Sử dụng hàng ngày:

1. **Update dữ liệu mới**
   - Chạy crawler để lấy jobs mới

2. **Xem phân tích**
   - Mở dashboard để xem insights

3. **Dự đoán lương**
   ```python
   from src.ml_models.salary_prediction import SalaryPredictor
   
   predictor = SalaryPredictor()
   predictor.load_model()
   
   result = predictor.predict_salary(
       job_group='Backend Developer',
       level='senior',
       city='Ho Chi Minh',
       skills=['python', 'django', 'aws']
   )
   
   print(f"Predicted: {result['predicted_salary_m']:.2f}M VND")
   ```

---

## Kết Quả Output

Sau khi chạy pipeline, bạn sẽ có:

### Trong thư mục `outputs/`:
- `salary_distribution.png` - Biểu đồ phân phối lương
- `salary_trends.png` - Xu hướng lương theo thời gian
- `feature_importance.png` - Các yếu tố ảnh hưởng lương
- `model_comparison.png` - So sánh các ML models
- `salary_analysis_report.txt` - Báo cáo chi tiết
- `skill_trends.csv` - Top skills
- `skill_cooccurrence.csv` - Skills xuất hiện cùng nhau

### Trong thư mục `models/`:
- `salary_predictor.pkl` - ML model đã train

### Trong thư mục `data_clean/`:
- `clean_data.csv` - Dữ liệu đã được xử lý

---

## Tips & Tricks

### 1. Chạy nhanh một phần của pipeline
```python
# Chỉ chạy data processing
from src.data_processing.processor import DataProcessor
processor = DataProcessor()
processor.process_pipeline()
```

### 2. Load model đã train để dự đoán
```python
from src.ml_models.salary_prediction import SalaryPredictor
predictor = SalaryPredictor()
predictor.load_model()  # Load model đã train
```

### 3. Filter data trước khi phân tích
```python
import pandas as pd

df = pd.read_csv('data_clean/clean_data.csv')

# Chỉ lấy Backend Developer
backend_df = df[df['job_group'] == 'Backend Developer']

# Chỉ lấy jobs ở HCM
hcm_df = df[df['city'] == 'Ho Chi Minh']

# Chỉ lấy senior level
senior_df = df[df['level'] == 'senior']
```

### 4. Export kết quả sang Excel
```python
import pandas as pd

df = pd.read_csv('data_clean/clean_data.csv')

# Export sang Excel với nhiều sheets
with pd.ExcelWriter('analysis_results.xlsx') as writer:
    df.to_excel(writer, sheet_name='All Data', index=False)
    
    # Top paying jobs
    top_salary = df.nlargest(100, 'salary_numeric')
    top_salary.to_excel(writer, sheet_name='Top Salary', index=False)
    
    # By city
    for city in df['city'].unique():
        city_df = df[df['city'] == city]
        city_df.to_excel(writer, sheet_name=city, index=False)
```

---

## Troubleshooting

### Lỗi: Module not found
```bash
# Cài lại dependencies
pip install -r requirements.txt --force-reinstall
```

### Lỗi: File not found
```bash
# Chạy data processing trước
python src/data_processing/processor.py
```

### Dashboard chạy chậm
```bash
# Giảm số lượng data
df = df.sample(1000)  # Chỉ lấy 1000 records
```

### Crawler không hoạt động
```bash
# Update webdriver
pip install --upgrade webdriver-manager
```

---

## Next Steps

Sau khi làm quen với dự án:

1. **Customize dashboard** - Thêm charts riêng của bạn
2. **Add new features** - Thêm features mới vào ML model
3. **Expand crawlers** - Thêm crawler cho TopCV, VietnamWorks
4. **Deploy** - Deploy dashboard lên Streamlit Cloud

Happy analyzing! 🎉
