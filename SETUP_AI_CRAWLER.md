# 🤖 Hướng dẫn Setup AI Crawler THẬT

## ⚠️ Yêu cầu

Để crawl data THẬT từ ITViec.vn bằng AI, bạn cần:

1. ✅ **OpenAI API Key** (có phí ~$0.50/100 jobs)
2. ✅ **Python 3.11+**
3. ✅ **Thư viện browser-use + playwright**

---

## 📝 Bước 1: Lấy OpenAI API Key

1. Vào: https://platform.openai.com/api-keys
2. Đăng ký/Đăng nhập tài khoản OpenAI
3. Click "Create new secret key"
4. Copy API key (bắt đầu bằng `sk-proj-...`)
5. Nạp tiền vào account: https://platform.openai.com/account/billing
   - Tối thiểu: $5 USD
   - $5 = ~1000 jobs crawled

---

## 📝 Bước 2: Cấu hình API Key

Mở file `.env` và paste API key:

```env
# File: .env
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE
OPENAI_MODEL=gpt-3.5-turbo  # hoặc gpt-4 (đắt hơn nhưng tốt hơn)
```

**💡 Chọn model:**
- `gpt-3.5-turbo`: Nhanh, rẻ (~$0.50/100 jobs) ⭐ Khuyên dùng
- `gpt-4`: Chậm hơn, đắt hơn (~$2/100 jobs), chính xác hơn

---

## 📝 Bước 3: Cài đặt thư viện

```bash
# Kích hoạt venv
.venv\Scripts\activate

# Cài browser-use + playwright
pip install browser-use langchain-openai playwright

# Cài Chromium browser
playwright install chromium
```

**⏱️ Thời gian:** ~5-10 phút (tải Chromium ~300MB)

---

## 🚀 Bước 4: Chạy AI Crawler THẬT

```bash
# Demo nhanh - 20 jobs (khuyên dùng lần đầu)
python src/crawler/ITViec_AI_real.py --quick

# Crawl 50 jobs
python src/crawler/ITViec_AI_real.py --jobs 50

# Crawl 100 jobs
python src/crawler/ITViec_AI_real.py --jobs 100
```

**⏱️ Thời gian:**
- 20 jobs: ~5 phút
- 50 jobs: ~10 phút
- 100 jobs: ~15-20 phút

**💰 Chi phí (gpt-3.5-turbo):**
- 20 jobs: ~$0.10
- 50 jobs: ~$0.25
- 100 jobs: ~$0.50

---

## 📊 Kết quả

AI sẽ:
1. ✅ Tự vào trang ITViec.vn
2. ✅ Tự scroll, click "Load more"
3. ✅ Trích xuất data THẬT: job title, company, salary, skills...
4. ✅ Lưu vào `data_raw/ITViec_AI_real.csv`
5. ✅ Tự động merge vào `data_clean/clean_data.csv`
6. ✅ Sẵn sàng cho dashboard

---

## ❌ Troubleshooting

### Lỗi: "Chưa có OpenAI API key"
**Giải pháp:** Check file `.env` có API key chưa

### Lỗi: "Thiếu thư viện browser-use"
**Giải pháp:**
```bash
pip install browser-use langchain-openai playwright
playwright install chromium
```

### Lỗi: "API key không hợp lệ"
**Giải pháp:**
1. Check API key đúng chưa (bắt đầu bằng `sk-proj-`)
2. Check đã nạp tiền vào account chưa: https://platform.openai.com/account/billing
3. Check usage limits: https://platform.openai.com/usage

### Lỗi: "Không parse được data"
**Giải pháp:**
1. Đổi model sang `gpt-4` trong file `.env`
2. Thử lại với số jobs ít hơn (--jobs 20)

### Crawl quá chậm?
**Giải pháp:**
- ✅ Bình thường! AI cần thời gian để:
  - Phân tích trang web
  - Điều hướng browser
  - Trích xuất data
- 💡 Dùng mock crawler nếu cần nhanh (không phí, không cần API)

---

## 🆚 So sánh: AI Real vs Mock

| Tiêu chí | AI Real (file này) | AI Mock (ITViec_AI_demo.py) |
|----------|-------------------|----------------------------|
| **Data** | ✅ Thật từ web | ❌ Fake (generated) |
| **API Key** | ✅ Cần | ❌ Không cần |
| **Chi phí** | 💰 $0.50/100 jobs | 🆓 Miễn phí |
| **Thời gian** | ⏱️ 10-15 phút | ⚡ 30 giây |
| **Demo** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Production** | ✅ Dùng được | ❌ Chỉ demo |

**💡 Khuyên:**
- **Demo/Thuyết trình:** Dùng Mock (nhanh, miễn phí, đủ concept)
- **Production/Data thật:** Dùng AI Real (có phí)
- **Data nhiều nhất:** Dùng Selenium (1000+ jobs, miễn phí, 3 phút)

---

## 📞 Support

**Lỗi OpenAI API:**
- Docs: https://platform.openai.com/docs
- Billing: https://platform.openai.com/account/billing
- Usage: https://platform.openai.com/usage

**Lỗi browser-use:**
- GitHub: https://github.com/browser-use/browser-use
- Docs: https://docs.browser-use.com

---

*Last updated: 2026-02-04*
