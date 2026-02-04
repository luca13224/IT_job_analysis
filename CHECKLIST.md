# ✅ CHECKLIST TRƯỚC KHI DEMO

## 🔧 Setup (Làm 1 lần)

- [ ] Python 3.11+ installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Groq API key: Vào [console.groq.com](https://console.groq.com) → Create key
- [ ] API key added to `.env`: `GROQ_API_KEY=gsk_...`
- [ ] Playwright installed: `playwright install chromium`

## 📖 Đọc Docs (20 phút)

- [ ] **DEMO_COMMANDS.md** - Học lệnh cơ bản
- [ ] **AI_CRAWLING_EXPLANATION.md** - Hiểu AI works
- [ ] **QUICK_DEMO_GV.md** - Đọc script demo

## 🧪 Test (10 phút)

### Test 1: Dashboard
```bash
streamlit run src/visualization/dashboard_v2.py
```
- [ ] Dashboard mở được (localhost:8501)
- [ ] 10 pages đều load
- [ ] Data hiển thị: 1,436 jobs

### Test 2: AI Crawler (ITViec)
```bash
python src/crawler/ITViec_AI_groq.py --jobs 5
```
- [ ] Browser tự mở
- [ ] Groq API hoạt động (không lỗi 429)
- [ ] Extract được 5 jobs
- [ ] File saved: `data_raw/ITViec_AI_groq.csv`
- [ ] Merged vào `clean_data.csv`

### Test 3: AI Crawler (VietnamWorks)
```bash
python src/crawler/VietnamWorks_AI_groq.py --jobs 10
```
- [ ] Crawl thành công
- [ ] Extract được 10 jobs
- [ ] Companies THẬT (FPT, SmartOSC...)

### Test 4: Mock Crawler
```bash
python src/crawler/ITViec_AI_demo.py --jobs 50
```
- [ ] Chạy nhanh (<10 giây)
- [ ] Generate 50 fake jobs
- [ ] Auto-merge

## 🎬 Practice Demo (15 phút)

### Part 1: Intro (2 phút)
- [ ] Giới thiệu project
- [ ] Show dashboard overview
- [ ] Highlight: AI-powered crawlers

### Part 2: Demo AI Crawler (5 phút)
```bash
python src/crawler/ITViec_AI_groq.py --jobs 5
```
**Giải thích trong khi chạy:**
- [ ] "Browser tự động mở - đây là Playwright"
- [ ] "HTML gửi lên Groq AI - Llama 3.3 70B"
- [ ] "AI parse semantic, không cần CSS selectors"
- [ ] "Auto-merge vào database"

### Part 3: Show Results (3 phút)
```bash
# Show crawled data
python -c "import pandas as pd; df=pd.read_csv('data_raw/ITViec_AI_groq.csv'); print(df.head())"

# Refresh dashboard
streamlit run src/visualization/dashboard_v2.py
```
- [ ] Point out: Companies THẬT (VNG, FPT, Tiki...)
- [ ] Show: Jobs increased từ 1,436 → 1,441

### Part 4: Compare Approaches (3 phút)
- [ ] **Selenium**: CSS selectors → breaks khi web đổi
- [ ] **AI (Groq)**: Semantic understanding → flexible
- [ ] **Cost**: $0 - Groq free tier

### Part 5: Q&A (2 phút)
**Prepare answers for:**
- [ ] "Tại sao không dùng Selenium?" → Brittleness
- [ ] "Chi phí AI?" → $0 - Groq free
- [ ] "Tốc độ?" → 1-2 phút, acceptable
- [ ] "Production ready?" → Yes, 1,436 jobs thật

## 📝 Talking Points (Học thuộc)

### Key Messages:
1. ✅ **AI-powered** - Llama 3.3 70B qua Groq
2. ✅ **FREE** - Groq API miễn phí (30 req/min)
3. ✅ **SMART** - AI hiểu semantic, không cần selectors
4. ✅ **REAL** - 1,436 jobs thật từ ITViec + VietnamWorks
5. ✅ **AUTO** - Auto-merge, dedup, transform

### Why AI > Selenium:
```
Selenium:
soup.find('div', class='job-card-v2')  ← Breaks khi class đổi

AI:
"Extract job titles from HTML"         ← AI tự tìm
```

### Architecture:
```
Playwright → HTML → Groq AI → JSON → Transform → Merge
```

## 🐛 Troubleshooting

### Lỗi thường gặp:
- [ ] **API key not found** → Check `.env` file
- [ ] **Rate limit 429** → Đợi 1-2 phút
- [ ] **Browser not opening** → `playwright install chromium`
- [ ] **Dashboard không load** → Check port 8501

### Quick fixes:
```bash
# Check API key
cat .env | grep GROQ

# Reinstall Playwright
pip install playwright
playwright install chromium

# Check data
python -c "import pandas as pd; print(len(pd.read_csv('data_clean/clean_data.csv')))"
```

## 📊 Stats to Remember

- **Jobs**: 1,436 (ITViec 1,155 + VietnamWorks 281)
- **Companies**: 400+ unique
- **Cities**: Ho Chi Minh, Ha Noi, Da Nang
- **Crawl time**: 1-2 phút/site
- **AI Model**: Llama 3.3 70B (Groq)
- **Cost**: $0 (FREE)
- **Dashboard**: 10 interactive pages

## ✅ Final Check (Before Demo)

- [ ] Git pushed: Latest commit on GitHub
- [ ] Data updated: `clean_data.csv` has 1,436+ jobs
- [ ] Docs ready: All 5 docs accessible
- [ ] Commands ready: Copy-paste from DEMO_COMMANDS.md
- [ ] Browser clear: Close unnecessary tabs
- [ ] Terminal ready: Open 2 terminals (crawler + dashboard)
- [ ] Backup plan: Mock crawler if API fails

## 🎯 Success Criteria

Demo thành công nếu:
- ✅ Dashboard load và show data
- ✅ AI crawler chạy và extract jobs
- ✅ Giải thích được tại sao dùng AI
- ✅ Answer được Q&A từ giáo viên
- ✅ Show được code + architecture

## 💡 Bonus Points

If có thời gian:
- [ ] Show code của AI crawler (explain prompt)
- [ ] Compare với Selenium code (show complexity)
- [ ] Show dashboard analytics (Top skills, Salary trends)
- [ ] Demo ML recommendation feature

---

## 🚀 GO TIME!

Khi sẵn sàng:
1. Open [DEMO_COMMANDS.md](DEMO_COMMANDS.md)
2. Open [QUICK_DEMO_GV.md](QUICK_DEMO_GV.md)
3. Open 2 terminals
4. Deep breath
5. **LET'S GO!** 🎬

---

Made with ❤️ for successful demo!
