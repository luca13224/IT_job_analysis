# 🚀 HƯỚNG DẪN NHANH - AI CRAWLER CHO GV

## ⚡ Setup nhanh (5 phút)

### Bước 1: Cài Ollama
1. Download: https://ollama.ai/download (hoặc đã mở trong browser)
2. Chạy file `OllamaSetup.exe`
3. Cài đặt (next, next, finish)

### Bước 2: Tải AI Model
Mở Terminal mới và chạy:
```bash
ollama pull llama3
```
⏱️ Tải ~4.7GB, mất ~5-10 phút

### Bước 3: Cài Python package
```bash
pip install ollama
```

### Bước 4: Test thử
```bash
# Test Ollama hoạt động chưa
ollama run llama3 "Hello"

# Chạy AI crawler
python src/crawler/ITViec_AI_ollama.py --jobs 20
```

---

## 🎯 Demo cho GV (15 phút)

### Phần 1: Giới thiệu (3 phút)
**Nói:** "Em sử dụng AI (Llama 3) để crawl dữ liệu thay vì thư viện thuần như Selenium"

**Show:** File `AI_CRAWLING_EXPLANATION.md`
- Kiến trúc AI crawling
- So sánh AI vs Selenium thuần

### Phần 2: Chạy crawler (5 phút)
```bash
python src/crawler/ITViec_AI_ollama.py --jobs 20
```

**Giải thích trong khi chạy:**
1. "Playwright vào web lấy HTML"
2. "Gửi HTML cho AI Llama 3"
3. "AI phân tích bằng NLP, extract data"
4. "Trả về JSON với jobs"

### Phần 3: Show kết quả (5 phút)
- Mở file CSV đã crawl
- Show 20 jobs THẬT từ ITViec.vn
- Giải thích data đã merge vào dashboard

### Phần 4: Vấn đáp (2 phút)
**Q: Tại sao không dùng BeautifulSoup/Selenium?**
A: GV yêu cầu dùng AI. Đây là Llama 3 - AI thật.

**Q: Tại sao không dùng ChatGPT?**
A: ChatGPT tốn tiền. Ollama miễn phí, chạy local.

**Q: AI hiểu HTML như thế nào?**
A: LLM được train trên tỷ web pages, học patterns của HTML.

---

## 📁 Files quan trọng

| File | Mục đích |
|------|----------|
| `src/crawler/ITViec_AI_ollama.py` | ⭐ AI crawler chính |
| `AI_CRAWLING_EXPLANATION.md` | Giải thích chi tiết cho GV |
| `data_raw/ITViec_AI_ollama.csv` | Data đã crawl (sau khi chạy) |
| `data_clean/clean_data.csv` | Data đã merge |

---

## ❌ Troubleshooting

### Lỗi: "ollama not found"
→ Chưa cài Ollama hoặc chưa restart terminal
→ Cài lại: https://ollama.ai/download

### Lỗi: "model llama3 not found"
→ Chưa pull model
→ Chạy: `ollama pull llama3`

### Lỗi: "Out of memory"
→ RAM không đủ (cần 8GB+)
→ Dùng model nhỏ hơn: `ollama pull llama3:8b`

### Chạy chậm?
→ Bình thường! AI local chậm hơn GPT-4
→ Đợi 5-10 phút cho 20 jobs

---

## 🎓 Điểm cộng khi demo

✅ Dùng AI thật (không phải mock)
✅ Miễn phí (không tốn tiền)
✅ Crawl data thật từ web
✅ Tự thích nghi (AI hiểu ngữ nghĩa)
✅ Code ngắn gọn (AI làm phần phức tạp)

---

## 📞 Quick Commands

```bash
# Check Ollama
ollama --version

# List models
ollama list

# Test AI
ollama run llama3 "Extract job title from: <h1>Backend Developer</h1>"

# Chạy crawler
python src/crawler/ITViec_AI_ollama.py --jobs 20

# Xem kết quả
cat data_raw/ITViec_AI_ollama.csv
```

---

**Chúc thuyết trình tốt! 🎉**
