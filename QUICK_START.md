# 🚀 Hướng dẫn Demo đầy đủ - Từ Crawl đến Dashboard

## 📋 Tóm tắt nhanh

```bash
# OPTION A: Demo với dữ liệu có sẵn (NHANH NHẤT - Khuyên dùng)
streamlit run src/visualization/dashboard_v2.py

# OPTION B: Demo từ đầu (Crawl AI → Dashboard)
python src/crawler/ITViec_AI_demo.py
streamlit run src/visualization/dashboard_v2.py
```

---

## 🎯 OPTION A: Demo Dashboard với dữ liệu có sẵn (Khuyên dùng cho thuyết trình)

### Bước 1: Kích hoạt môi trường
```bash
# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### Bước 2: Chạy Dashboard
```bash
streamlit run src/visualization/dashboard_v2.py
```

### Bước 3: Mở trình duyệt
- Dashboard tự động mở tại: **http://localhost:8501**
- Hoặc click link trong terminal

### 📊 Tính năng demo:
- ✅ 10 trang interactive (Tổng quan, ML recommendations, Career simulator...)
- ✅ 1,141 jobs từ ITViec đã xử lý sẵn
- ✅ Không cần API key, không cần crawl mới
- ✅ Chạy nhanh, ổn định

---

## 🤖 OPTION B: Demo đầy đủ từ AI Crawl đến Dashboard

### Bước 1: Chuẩn bị môi trường

```bash
# Kích hoạt virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Kiểm tra packages đã cài
pip list | findstr "streamlit pandas selenium"
```

### Bước 2: Crawl dữ liệu với AI (MOCK - Không cần API)

```bash
# Chạy AI Crawler Demo (Mock version - không cần OpenAI API)
python src/crawler/ITViec_AI_demo.py
```

**Output:**
- ✅ Demo quá trình AI thinking (5 bước)
- ✅ Tạo 10 jobs mẫu từ VNG, FPT, Tiki, Shopee...
- ✅ Hiển thị bảng so sánh AI vs Traditional
- ✅ Lưu file: `data_raw/ITViec_AI_demo.csv`

**Thời gian:** ~5 giây (với mock data)

### Bước 3: (Optional) Làm sạch dữ liệu

```bash
# Nếu muốn xử lý data mới crawl
python -c "from src.data_processing.processor import DataProcessor; DataProcessor().process_pipeline()"
```

**Hoặc dùng data có sẵn:** `data_clean/clean_data.csv` (1,141 jobs)

### Bước 4: Chạy Dashboard

```bash
streamlit run src/visualization/dashboard_v2.py
```

### Bước 5: Trải nghiệm Dashboard

**URL:** http://localhost:8501

**10 trang chức năng:**

| Trang | Tính năng | Demo điểm nhấn |
|-------|-----------|----------------|
| 🏠 Tổng quan | 4 metrics chính, charts | Hiển thị 1,141 jobs, top skills |
| 📊 Phân tích | Phân bố theo nghề/level/city | Interactive filters |
| 🔍 Gợi ý AI | Job recommendation (ML) | Nhập skills → Top 5 matches |
| 💰 Lương | Salary analytics, predictions | Median salary by role |
| 🎓 Kỹ năng | Top 20 skills, combinations | Python chiếm 45% |
| 🎬 Demo | 5 pre-built scenarios | 1-click demo for teachers |
| 🚀 Lộ trình | Career path 5-10 years | Junior → Senior projections |
| ⚖️ So sánh | Compare jobs/cities | Side-by-side comparison |
| 📥 Xuất báo cáo | Export Excel/CSV/JSON | Download full analysis |
| 🤖 Chatbot | Q&A về thị trường IT | "Lương Backend bao nhiêu?" |

---

## 🎓 Kịch bản thuyết trình cho Thầy

### Phần 1: Giới thiệu AI Crawler (5 phút)

```bash
# Demo AI Crawler
python src/crawler/ITViec_AI_demo.py
```

**Điểm nhấn:**
- ✨ So sánh code: 300 dòng (Selenium) vs 100 dòng (AI)
- 🔄 Tự thích nghi khi web đổi layout
- 🧠 Natural language task: "Trích xuất jobs Backend từ ITViec"
- 📊 Bảng so sánh chi tiết 8 tiêu chí

### Phần 2: Dashboard phân tích (10 phút)

```bash
streamlit run src/visualization/dashboard_v2.py
```

**Flow demo:**

1. **Trang Tổng quan** (1 phút)
   - Metrics: 1,141 jobs, 250+ companies
   - Top 5 skills nhu cầu cao

2. **Gợi ý AI (ML)** (2 phút)
   - Nhập: "Python, Django, PostgreSQL"
   - Hiển thị: Top 5 jobs khớp với % match score

3. **Demo Scenarios** (2 phút)
   - Click "Senior Backend Engineer"
   - Auto-fill skills → Gợi ý ngay

4. **Career Simulator** (2 phút)
   - Input: Junior Backend, 3 năm kinh nghiệm
   - Output: Lộ trình 10 năm, salary projection chart

5. **So sánh cities** (2 phút)
   - HCM vs Hà Nội: Số jobs, median salary, top skills

6. **Xuất báo cáo** (1 phút)
   - Download Excel: Full analysis report

### Phần 3: Q&A với Chatbot (2 phút)

**Ví dụ câu hỏi:**
- "Kỹ năng nào cần học để làm Backend?"
- "Lương Senior Backend bao nhiêu?"
- "So sánh Frontend vs Backend?"

---

## 📂 Cấu trúc File quan trọng

```
📁 Project
├── src/crawler/
│   ├── ITViec_AI_demo.py          # 🤖 AI Crawler Demo (Mock)
│   ├── ITViec_AI_crawler.py       # AI Crawler (cần OpenAI API)
│   └── ITViec_crawling.py         # Traditional Selenium
│
├── data_raw/
│   ├── ITViec_data.csv            # Data gốc từ Selenium
│   └── ITViec_AI_demo.csv         # Data từ AI demo
│
├── data_clean/
│   └── clean_data.csv             # 1,141 jobs đã xử lý (DÙNG CHO DASHBOARD)
│
├── src/visualization/
│   └── dashboard_v2.py            # 🎯 Main Dashboard (10 trang)
│
└── src/data_processing/
    └── processor.py               # Data cleaning pipeline
```

---

## 🛠 Lệnh hữu ích

### Kiểm tra môi trường
```bash
# Python version
python --version  # Cần 3.11+

# Packages installed
pip list | findstr "streamlit pandas selenium browser-use"

# Test import
python -c "import streamlit; import pandas; print('✅ OK')"
```

### Troubleshooting

**Lỗi: ModuleNotFoundError**
```bash
pip install -r requirements.txt
```

**Lỗi: Port 8501 đã dùng**
```bash
# Kill process
taskkill /F /IM streamlit.exe  # Windows
pkill -9 streamlit  # Mac/Linux

# Hoặc dùng port khác
streamlit run src/visualization/dashboard_v2.py --server.port 8502
```

**Dashboard không load data**
```bash
# Kiểm tra file data
dir data_clean\clean_data.csv  # Windows
ls data_clean/clean_data.csv   # Mac/Linux

# Nếu thiếu, copy từ data_raw
copy data_raw\ITViec_data.csv data_clean\clean_data.csv
```

---

## 🎬 Batch Script nhanh (Windows)

### Tạo file `demo.bat`:

```bat
@echo off
echo ========================================
echo   DEMO AI JOB ANALYSIS - FULL FLOW
echo ========================================
echo.

REM Kích hoạt venv
call .venv\Scripts\activate.bat

echo [1/3] Running AI Crawler Demo...
python src/crawler/ITViec_AI_demo.py
echo.

echo [2/3] Starting Dashboard...
echo Dashboard: http://localhost:8501
echo.
streamlit run src/visualization/dashboard_v2.py

pause
```

**Chạy:** Double-click `demo.bat`

---

## 📊 So sánh Crawler Options

| Tiêu chí | AI Demo (Mock) | AI Real (GPT-4) | Selenium Traditional |
|----------|----------------|-----------------|---------------------|
| **API Key** | ❌ Không cần | ✅ Cần OpenAI | ❌ Không cần |
| **Thời gian** | 5 giây | 10 phút | 3 phút |
| **Chi phí** | Miễn phí | $0.50/100 jobs | Miễn phí |
| **Jobs crawl** | 10 mẫu | ~100 real | ~1000 real |
| **Demo cho thầy** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Production** | ❌ Không phù hợp | ✅ Tốt nhất | ✅ Ổn định |

**💡 Khuyên dùng:** AI Demo (Mock) cho thuyết trình - nhanh, không cần API, demo đủ khái niệm.

---

## 🎯 Checklist trước khi Demo

### Chuẩn bị (5 phút trước):
- [ ] Kích hoạt venv: `.venv\Scripts\activate`
- [ ] Kiểm tra data: `dir data_clean\clean_data.csv`
- [ ] Test chạy dashboard: `streamlit run src/visualization/dashboard_v2.py`
- [ ] Mở trình duyệt: http://localhost:8501
- [ ] Chuẩn bị câu hỏi chatbot

### Trong khi Demo:
- [ ] Tab 1: Dashboard đang chạy
- [ ] Tab 2: Terminal chạy AI crawler
- [ ] Tab 3: VS Code mở file so sánh code
- [ ] Notepad: Các kịch bản demo

### Sau Demo:
- [ ] Export 1 file Excel báo cáo
- [ ] Screenshot dashboard đẹp
- [ ] Note feedback từ thầy

---

## 📝 Ghi chú thêm

### Dữ liệu hiện có:
- ✅ `data_clean/clean_data.csv`: 1,141 jobs (đã xử lý, sẵn dùng)
- ✅ `data_raw/ITViec_data.csv`: Data gốc từ Selenium
- ✅ `data_raw/ITViec_AI_demo.csv`: 10 jobs từ AI demo

### Không cần chạy lại crawl thật:
- Dashboard dùng `data_clean/clean_data.csv` sẵn có
- AI Demo tạo data mock đủ để demo khái niệm
- Chỉ chạy crawler thật khi cần data mới nhất

### Link hữu ích:
- Dashboard local: http://localhost:8501
- GitHub repo: (add your repo URL)
- OpenAI API: https://platform.openai.com (nếu dùng real AI)

---

## ✅ Tóm tắt lệnh 1 dòng

```bash
# Demo nhanh nhất (Dashboard only)
streamlit run src/visualization/dashboard_v2.py

# Demo đầy đủ (AI + Dashboard)
python src/crawler/ITViec_AI_demo.py && streamlit run src/visualization/dashboard_v2.py
```

**Thời gian:** 5 giây (mock AI) + 2 giây (load dashboard) = **~7 giây tổng**

---

Chúc bạn demo thành công! 🎉
