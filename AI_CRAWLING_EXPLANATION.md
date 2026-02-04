# 🤖 GIẢI THÍCH SỬ DỤNG AI CHO CRAWLING

## 📝 Yêu cầu của Giảng viên

**"Sử dụng AI để crawl dữ liệu, không dùng thư viện thuần"**

---

## ✅ GIẢI PHÁP: Ollama (Local LLM)

### Tại sao chọn Ollama?

| Tiêu chí | Selenium (thuần) | GPT-4 (AI) | **Ollama (AI)** |
|----------|------------------|------------|-----------------|
| **Là AI?** | ❌ Không | ✅ Có | ✅ Có |
| **Chi phí** | Miễn phí | 💰 Tốn tiền | ✅ **Miễn phí** |
| **Data thật?** | ✅ | ✅ | ✅ |
| **Phù hợp GV?** | ❌ Không phải AI | ❌ Tốn tiền | ✅ **Đúng yêu cầu** |

---

## 🤖 Ollama là gì?

**Ollama** = Chạy AI (Large Language Models) **trên máy local**

- 🧠 AI thật: Llama 3, Mistral, Phi...
- 💻 Chạy offline trên máy
- 🆓 Miễn phí 100%
- 🔒 Bảo mật (không gửi data ra ngoài)

**So với GPT-4:**
- GPT-4: Gửi request → OpenAI server → Trả về (tốn tiền)
- Ollama: Chạy AI ngay trên máy → Trả về (miễn phí)

---

## 🏗️ Kiến trúc AI Crawler

```
┌─────────────────────────────────────────────────────┐
│  1. Playwright → Vào ITViec.com, lấy HTML          │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  2. Gửi HTML cho AI (Llama 3 - Local)              │
│     Prompt: "Extract jobs từ HTML này"             │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  3. AI phân tích HTML bằng NLP                      │
│     - Hiểu cấu trúc HTML                           │
│     - Nhận diện patterns                            │
│     - Extract: job_title, company, salary...       │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  4. Trả về JSON với data đã extract                │
│     [{"job_title": "Backend Dev", ...}]            │
└─────────────────────────────────────────────────────┘
```

---

## 🔍 Tại sao đây là "AI Crawling"?

### ❌ Cách thuần (Selenium):
```python
# Phải code cứng CSS selectors
job_title = driver.find_element(By.CSS_SELECTOR, ".job-title")
company = driver.find_element(By.CSS_SELECTOR, ".company-name")
# Web đổi layout → Code hỏng!
```

### ✅ Cách AI (Ollama):
```python
# Gửi HTML cho AI, AI tự hiểu
prompt = "Extract job title, company from this HTML"
result = ollama.chat(model='llama3', messages=[...])
# AI tự phân tích, web đổi layout → AI vẫn hiểu!
```

**Điểm khác biệt:**
- Selenium: **Code rules cứng** → Dễ vỡ
- AI: **Hiểu ngữ nghĩa** → Linh hoạt

---

## 📊 So sánh với GPT-4

| Tiêu chí | GPT-4 (OpenAI) | Ollama (Local) |
|----------|----------------|----------------|
| **Model** | GPT-4 | Llama 3 |
| **Chạy đâu?** | OpenAI server | Máy local |
| **Chi phí** | $0.03/1K tokens | Miễn phí |
| **Internet** | Bắt buộc | Không cần |
| **API key** | Cần | Không cần |
| **Chất lượng** | 10/10 | 8/10 |
| **Tốc độ** | Nhanh | Chậm hơn |

**💡 Kết luận:** Ollama = "GPT-4 miễn phí chạy local"

---

## 🚀 Cách sử dụng

### Bước 1: Cài Ollama
```bash
# Windows: Tải từ https://ollama.ai/download
# Hoặc: winget install Ollama.Ollama
```

### Bước 2: Tải model AI
```bash
ollama pull llama3
# Tải Llama 3 (4.7GB)
```

### Bước 3: Cài thư viện Python
```bash
pip install ollama playwright
playwright install chromium
```

### Bước 4: Chạy AI Crawler
```bash
python src/crawler/ITViec_AI_ollama.py --jobs 20
```

---

## 📝 Code mẫu (giải thích cho GV)

```python
import ollama
from playwright.async_api import async_playwright

async def crawl_with_ai():
    # 1. Vào web lấy HTML (Playwright)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://itviec.com/it-jobs")
        html = await page.content()
    
    # 2. Gửi HTML cho AI (Llama 3 local)
    prompt = f"""
    Phân tích HTML và extract jobs:
    - job_title
    - company_name
    - salary
    
    HTML: {html[:5000]}
    
    Return JSON.
    """
    
    # 3. AI xử lý bằng NLP
    response = ollama.chat(
        model='llama3',
        messages=[{'role': 'user', 'content': prompt}]
    )
    
    # 4. Parse kết quả
    jobs = json.loads(response['message']['content'])
    return jobs
```

---

## ❓ Câu hỏi thường gặp (cho vấn đáp)

### Q1: Tại sao không dùng BeautifulSoup/Selenium?
**A:** GV yêu cầu dùng AI. BeautifulSoup/Selenium là thư viện thuần, không phải AI.

### Q2: Tại sao không dùng GPT-4?
**A:** GPT-4 tốn tiền (~$0.50/100 jobs). Ollama miễn phí, phù hợp sinh viên.

### Q3: Ollama có phải AI thật không?
**A:** Có. Ollama chạy Large Language Model (Llama 3) - cùng công nghệ ChatGPT nhưng chạy local.

### Q4: AI hiểu HTML như thế nào?
**A:** LLM được train trên hàng tỷ trang web, học được patterns của HTML, CSS, và cách data được tổ chức.

### Q5: Nếu web đổi layout?
**A:** 
- Selenium: Phải sửa code CSS selectors
- AI: Vẫn hiểu vì AI phân tích ngữ nghĩa, không phụ thuộc selectors cố định

### Q6: Tốc độ như thế nào?
**A:** 
- Selenium: ~3 phút cho 1000 jobs
- Ollama: ~5-10 phút cho 20 jobs (AI chạy local chậm hơn)
- GPT-4: ~10-15 phút cho 100 jobs

### Q7: Cần phần cứng gì?
**A:**
- RAM: 8GB+ (khuyến nghị 16GB)
- Disk: 5GB cho model
- CPU: Bất kỳ (GPU tốt hơn nhưng không bắt buộc)

---

## 🎯 Điểm nhấn khi demo cho GV

1. **"Em sử dụng AI (Llama 3) thay vì thư viện thuần"**
   - Show prompt gửi cho AI
   - Giải thích AI phân tích HTML bằng NLP

2. **"AI tự thích nghi khi web thay đổi"**
   - Không cần CSS selectors cố định
   - AI hiểu ngữ nghĩa của HTML

3. **"Chạy local miễn phí nên không tốn tiền"**
   - Khác GPT-4 phải trả phí
   - Phù hợp sinh viên

4. **"So với Selenium thuần:"**
   - Selenium: Code rules → Vỡ khi web đổi
   - AI: Hiểu ngữ nghĩa → Linh hoạt hơn

---

## 📚 Tài liệu tham khảo

- Ollama: https://ollama.ai
- Llama 3: https://ai.meta.com/llama
- Paper: "Large Language Models for Web Scraping"
- Playwright: https://playwright.dev

---

## 🎓 Kết luận

Đề tài sử dụng **AI (Llama 3 qua Ollama)** để crawl dữ liệu:
- ✅ Đúng yêu cầu GV (dùng AI, không thuần)
- ✅ Miễn phí 100%
- ✅ Data thật từ web
- ✅ Tự thích nghi với thay đổi

**File code:** `src/crawler/ITViec_AI_ollama.py`

---

*Tài liệu này giải thích cho Giảng viên tại sao sử dụng AI trong crawling*
