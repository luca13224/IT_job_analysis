# 🚀 Hướng dẫn Push lên GitHub

## Bước 1: Kiểm tra remote repository

```bash
git remote -v
```

Nếu chưa có remote hoặc muốn đổi:

```bash
# Xóa remote cũ (nếu có)
git remote remove origin

# Thêm remote mới
git remote add origin https://github.com/USERNAME/REPO_NAME.git
```

## Bước 2: Push code lên GitHub

```bash
# Push lần đầu
git push -u origin main

# Hoặc nếu branch tên master
git push -u origin master
```

## Bước 3: Nhập credentials (nếu cần)

- **Username**: GitHub username của bạn
- **Password**: GitHub Personal Access Token (không phải password)

### Tạo Personal Access Token:

1. Vào GitHub → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token
4. Chọn scopes: `repo` (full control)
5. Copy token và lưu lại (chỉ hiện 1 lần)

## Bước 4: Verify trên GitHub

Vào `https://github.com/USERNAME/REPO_NAME` để kiểm tra code đã lên chưa.

## ✅ Done!

Các file sau đã được loại trừ (xem .gitignore):
- *.docx (báo cáo Word)
- .env (API keys)
- __pycache__/
- .venv/
- *.log

## Push lần sau

Khi có thay đổi:

```bash
git add .
git commit -m "Your commit message"
git push
```

## Troubleshooting

### Lỗi: "remote origin already exists"
```bash
git remote set-url origin https://github.com/USERNAME/REPO_NAME.git
```

### Lỗi: "Permission denied"
- Sử dụng Personal Access Token thay vì password
- Hoặc setup SSH keys

### Lỗi: "failed to push some refs"
```bash
# Pull trước, sau đó push
git pull origin main --rebase
git push
```
