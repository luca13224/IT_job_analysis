# 🇻🇳 Phân tích thị trường việc làm IT Việt Nam

### 🤖 AI-Powered Web Crawler + Interactive Dashboard

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)](https://streamlit.io)
[![AI](https://img.shields.io/badge/AI-GPT--4%20Browser--Use-brightgreen.svg)](https://platform.openai.com)
[![Data](https://img.shields.io/badge/Jobs-1,422-orange.svg)](data_clean/clean_data.csv)

Dashboard phân tích thị trường tuyển dụng IT với **AI-powered crawler** (GPT-4 + Browser Use), **10 trang tương tác**, ML recommendations, career simulator. Sử dụng dữ liệu thực từ ITViec.vn.

---

## ⚡ Chạy nhanh (1 lệnh)

### Option 1: Dashboard Only (Khuyên dùng)
```bash
streamlit run src/visualization/dashboard_v2.py
```
🌐 Mở: **http://localhost:8501** - Dashboard với 1,422 jobs sẵn có

### Option 2: Crawl thêm data với AI → Dashboard
```bash
# 1. Crawl thêm 100-200 jobs mới (AI mock)
python src/crawler/ITViec_AI_demo.py --jobs 100

# 2. Chạy dashboard
streamlit run src/visualization/dashboard_v2.py
```

**💡 Tips:** `--jobs 50` (nhanh) | `--jobs 100` (cân bằng) | `--jobs 200` (nhiều data)

---

## 📚 Tài Liệu Quan Trọng

| File | Mục đích | Khi nào đọc |
|------|----------|-------------|
| **[LOGIC_EXPLANATION.md](LOGIC_EXPLANATION.md)** | ⭐ Giải thích logic, vấn đáp | **Chuẩn bị thuyết trình** |
| [QUICK_START.md](QUICK_START.md) | Hướng dẫn demo đầy đủ | Demo cho thầy |
| [COMMANDS.md](COMMANDS.md) | Quick reference lệnh | Troubleshooting |
| [START_HERE.md](START_HERE.md) | Bắt đầu nhanh | Lần đầu sử dụng |

## ✨ Tính năng chính

### 🤖 AI-Powered Crawlers
- **🎭 AI Enhanced Crawler** (Mock - Không cần API) ⭐ Khuyên dùng
  - ✨ Mô phỏng AI crawl với 50-200 jobs realistic
  - 🏢 50+ công ty nổi tiếng (VNG, FPT, Tiki, Grab, Shopee...)
  - 💼 6 job types: Backend, Frontend, Fullstack, Mobile, Data, DevOps
  - 📊 Skills đa dạng theo từng vị trí
  - ⚡ Tự động merge vào data chính
  - 🎓 Hoàn hảo cho demo và thuyết trình
  
- **GPT-4 Real Crawler** - Browser Use + LangChain (Cần API key)
  - Natural language task: "Go to ITViec, extract Backend jobs"
  - Self-adaptive to layout changes
  - AI understands page context
  
- **Traditional Selenium Crawler** - Fast, free, stable
  - 298 dòng code với CSS selectors
  - Crawl nhanh (3 phút), miễn phí
  - Backup ổn định cho production

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
AI Crawling:** Browser Use, LangChain, GPT-4 ⚡ NEW!
- **Traditional
### 🎯 Data Sources
- **ITViec.vn** - 1,141 jobs crawled
- **TopCV.vn** - Multi-page crawler


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
├── 📚 LOGIC_EXPLANATION.md  # ⭐ ĐỌC ĐỂ VẤN ĐÁP/THUYẾT TRÌNH
├── 📋 QUICK_START.md          # Hướng dẫn demo đầy đủ
├── ⚡ COMMANDS.md             # Quick reference lệnh
├── 🎯 START_HERE.md           # Bắt đầu nhanh
├── 📊 DEMO_SUMMARY.md         # Tổng kết project
│
├── data_clean/
│   └── clean_data.csv         # 1,150 jobs (sẵn dùng)
├── data_raw/
│   ├── ITViec_data.csv        # Data từ Selenium (1,141)
│   └── ITViec_AI_demo.csv     # Data từ AI (10)
│
├── src/
│   ├── crawler/
│   │   ├── ITViec_AI_demo.py      # 🤖 AI Crawler (CHÍNH - All-in-one)
│   │   ├── ITViec_crawling.py     # Traditional Selenium (backup)
│   │   └── topcv_crawling.py      # TopCV crawler
│   │
│   ├── ml_models/
│   │   └── job_recommender.py     # TF-IDF + Cosine Similarity
│   │
│   ├── visualization/
│   │   └── dashboard_v2.py        # 🎯 Main Dashboard (10 trang)
│   │
│   └── data_processing/
│       └── processor.py           # Data cleaning pipeline
│
└── requirements.txt               # Dependencies
```

**💡 Files quan trọng:**
- **LOGIC_EXPLANATION.md** - ⭐ Giải thích logic cho vấn đáp/thuyết trình
- **ITViec_AI_demo.py** - AI crawler + auto merge (All-in-one)
- **dashboard_v2.py** - Dashboard chính
- **clean_data.csv** - 1,150 jobs sẵn dùng


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

**Made with ❤️ by Vietnam IT Job Market Analysis Team**```bash
# Dashboard không chạy
pip install --upgrade streamlit pandas plotly

# Thiếu data
# → Dữ liệu có sẵn tại data_clean/clean_data.csv

# Lỗi import module
# → Đảm bảo chạy từ thư mục gốc: IT-job-analysis-VN-main/

# Port 8501 bị chiếm
streamlit run src/visualization/dashboard_v2.py --server.port 8502
```

## 📝 License

MIT License - Xem [LICENSE](LICENSE) để biết thêm chi tiết.

## 🙏 Acknowledgments

- Dữ liệu từ [ITViec.vn](https://itviec.com)
- Built with [Streamlit](https://streamlit.io)
- Icons from [Icons8](https://icons8.com)

---

**⭐ Star repo nếu project hữu ích!**