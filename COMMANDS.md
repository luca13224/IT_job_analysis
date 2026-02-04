# 📋 Tổng Hợp Lệnh Demo - Quick Reference

## ⚡ Lệnh nhanh nhất (1 click)

### Windows:
```bash
# Double-click file này:
demo_quick.bat
```

### Mac/Linux/Terminal:
```bash
# Chạy dashboard ngay
streamlit run src/visualization/dashboard_v2.py
```

---

## 🎯 Các lệnh theo kịch bản

### 1. Demo Dashboard (Nhanh nhất - 5 giây)
```bash
# Kích hoạt venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Chạy dashboard
streamlit run src/visualization/dashboard_v2.py
```
→ Mở: http://localhost:8501

---

### 2. Demo AI Crawler + Dashboard (Đầy đủ - 10 giây)

#### Windows (1 click):
```bash
demo_full.bat
```

#### Manual:
```bash
# Bước 1: Activate venv
.venv\Scripts\activate

# Bước 2: Demo AI Crawler
python src/crawler/ITViec_AI_demo.py

# Bước 3: Dashboard
streamlit run src/visualization/dashboard_v2.py
```

---

### 3. Demo cho Thầy (Khuyên dùng)

```bash
# Terminal 1: Chạy AI Demo trước
python src/crawler/ITViec_AI_demo.py

# Chờ xem output (bảng so sánh, code examples)

# Terminal 2: Chạy Dashboard
streamlit run src/visualization/dashboard_v2.py
```

**Điểm nhấn khi demo:**
- ✅ AI tạo 10 jobs từ VNG, FPT, Tiki trong 5 giây
- ✅ Bảng so sánh: 300 dòng code vs 100 dòng code
- ✅ Natural language: "Trích xuất Backend jobs từ ITViec"
- ✅ Dashboard với 10 trang tương tác

---

## 📊 Flow Demo đầy đủ (15 phút)

### Phần 1: AI Crawler (3 phút)
```bash
python src/crawler/ITViec_AI_demo.py
```
**Show:**
- AI thinking process (5 bước)
- 10 jobs generated
- Comparison table (8 tiêu chí)
- Code comparison (300 vs 100 lines)

### Phần 2: Dashboard (10 phút)
```bash
streamlit run src/visualization/dashboard_v2.py
```
**Demo pages:**
1. 🏠 Tổng quan → Show 1,141 jobs metrics
2. 🔍 Gợi ý AI → Input "Python, Django" → Top 5 matches
3. 🎬 Kịch bản → "Senior Backend Engineer" scenario
4. 🚀 Lộ trình → Career 10 năm, salary projection
5. ⚖️ So sánh → HCM vs Hà Nội
6. 🤖 Chatbot → "Lương Backend Developer?"

### Phần 3: Q&A (2 phút)
- Dùng chatbot trả lời câu hỏi từ khán giả

---

## 🛠 Lệnh Troubleshooting

### Kiểm tra môi trường
```bash
# Python version
python --version  # Cần 3.11+

# Check venv activated
where python  # Windows
which python  # Mac/Linux

# Test packages
python -c "import streamlit, pandas; print('✅ OK')"
```

### Fix lỗi thường gặp
```bash
# Lỗi: ModuleNotFoundError
pip install -r requirements.txt

# Lỗi: Port 8501 đã dùng
taskkill /F /IM streamlit.exe  # Windows
streamlit run src/visualization/dashboard_v2.py --server.port 8502

# Lỗi: Không load được data
dir data_clean\clean_data.csv  # Kiểm tra file tồn tại
```

### Cài đặt lại môi trường
```bash
# Remove old venv
rmdir /s .venv  # Windows
rm -rf .venv    # Mac/Linux

# Create new venv
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📦 Lệnh Git

### Clone project
```bash
git clone https://github.com/luca13224/IT_job_analysis.git
cd IT_job_analysis
```

### Update code mới nhất
```bash
git pull origin main
```

### Xem commit history
```bash
git log --oneline -5
```

---

## 🎓 Checklist Trước Demo

### 5 phút trước:
```bash
# 1. Activate venv
.venv\Scripts\activate

# 2. Test AI crawler
python src/crawler/ITViec_AI_demo.py | Select-Object -First 20

# 3. Test dashboard
timeout /t 2 && streamlit run src/visualization/dashboard_v2.py
# Ctrl+C sau khi mở được

# 4. Kiểm tra data
type data_clean\clean_data.csv | Select-Object -First 5
```

### Trong khi demo:
- [ ] Terminal sẵn sàng ở thư mục gốc
- [ ] Browser mở tab http://localhost:8501
- [ ] VS Code mở file ITViec_AI_demo.py
- [ ] QUICK_START.md mở sẵn

---

## 📊 Lệnh Data Processing (Optional)

### Nếu cần xử lý data mới
```bash
# Process raw data
python -c "from src.data_processing.processor import DataProcessor; DataProcessor().process_pipeline()"

# Hoặc dùng main pipeline
python main.py
```

### Kiểm tra data stats
```bash
# Quick stats
python -c "import pandas as pd; df=pd.read_csv('data_clean/clean_data.csv'); print(df.info()); print(df.describe())"
```

---

## 🚀 Deploy lên Streamlit Cloud (Bonus)

```bash
# 1. Commit code
git add .
git commit -m "Deploy dashboard"
git push origin main

# 2. Vào https://share.streamlit.io
# 3. Connect GitHub repo: luca13224/IT_job_analysis
# 4. Main file: src/visualization/dashboard_v2.py
# 5. Deploy!
```

---

## 📞 Lệnh Hỗ Trợ

### Xem logs
```bash
# Streamlit logs
Get-Content "$env:USERPROFILE\.streamlit\logs\*.log" -Tail 20
```

### Monitor resources
```bash
# Check CPU/Memory
Get-Process python | Select-Object CPU,PM
```

### Kill all Python processes (Emergency)
```bash
# Windows
taskkill /F /IM python.exe

# Mac/Linux
pkill -9 python
```

---

## 💡 Tips

### Shortcuts trong Dashboard
- `R` - Rerun app
- `Ctrl+R` - Force reload
- `Ctrl+C` trong terminal - Stop server

### Performance
```bash
# Chạy với cache disable (nếu có lỗi cache)
streamlit run src/visualization/dashboard_v2.py --server.runOnSave false

# Chạy ở port khác
streamlit run src/visualization/dashboard_v2.py --server.port 8502
```

---

## 📚 Xem thêm

- [QUICK_START.md](QUICK_START.md) - Hướng dẫn đầy đủ
- [README.md](README.md) - Project overview
- [GitHub Repo](https://github.com/luca13224/IT_job_analysis)

---

**Tóm tắt ngắn gọn:**
```bash
# Demo nhanh nhất
streamlit run src/visualization/dashboard_v2.py

# Demo đầy đủ
python src/crawler/ITViec_AI_demo.py && streamlit run src/visualization/dashboard_v2.py
```

✅ Thời gian: 7 giây | 📊 Data: 1,141 jobs | 🤖 AI: GPT-4 concept
