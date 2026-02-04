# 🚀 Deploying to Streamlit Cloud

## Prerequisites
- GitHub account
- Data files (`data_clean/clean_data.csv`) committed to repository

## Deployment Steps

### 1. Push Code to GitHub
```bash
git init
git add .
git commit -m "Initial commit - IT Job Analysis Dashboard"
git branch -M main
git remote add origin https://github.com/your-username/IT-job-analysis-VN.git
git push -u origin main
```

### 2. Prepare for Deployment

#### Create `.gitignore`
```
.venv/
__pycache__/
*.pyc
.env
.DS_Store
*.log
.vscode/
.idea/
models/*.pkl
current_page.txt
```

#### Ensure `requirements.txt` is complete
```bash
# Test locally first
pip install -r requirements.txt
streamlit run src/visualization/dashboard_v2.py
```

### 3. Deploy on Streamlit Cloud

#### a. Sign up/Login
- Go to [share.streamlit.io](https://share.streamlit.io)
- Sign in with GitHub

#### b. New App
1. Click "New app"
2. Select your repository: `your-username/IT-job-analysis-VN`
3. Select branch: `main`
4. Main file path: `src/visualization/dashboard_v2.py`
5. Click "Deploy!"

#### c. Advanced Settings (Optional)
- **Python version**: 3.11
- **Secrets**: Add any API keys if needed

### 4. Configuration Files

The following files are already created for deployment:
- `.streamlit/config.toml` - Streamlit configuration
- `requirements.txt` - Python dependencies

### 5. Post-Deployment

#### Monitor Deployment
- Check logs in Streamlit Cloud dashboard
- Deployment typically takes 3-5 minutes

#### Custom Domain (Optional)
- In app settings, add custom domain
- Update DNS records as instructed

#### Share Your App
Your app will be live at:
```
https://share.streamlit.io/your-username/IT-job-analysis-VN/main/src/visualization/dashboard_v2.py
```

Or shorter URL (if configured):
```
https://your-app-name.streamlit.app
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Module Import Errors
**Problem**: `ModuleNotFoundError`
**Solution**: Ensure all dependencies are in `requirements.txt`

#### 2. File Not Found
**Problem**: `FileNotFoundError: data_clean/clean_data.csv`
**Solution**: 
- Make sure data files are committed to git
- Check file paths in `config/config.py`

#### 3. Memory Issues
**Problem**: App crashes or slow performance
**Solution**:
- Use `@st.cache_data` decorator
- Optimize data loading
- Consider data size limits (1GB for Streamlit Cloud)

#### 4. Deployment Fails
**Problem**: Red status in deployment
**Solution**:
- Check logs for specific errors
- Verify Python version compatibility
- Test locally with same Python version

## 📊 App Features on Cloud

Your deployed app includes:
- ✅ Interactive dashboard with 5 sections
- ✅ AI-powered job recommendations
- ✅ Real-time filtering and analysis
- ✅ Responsive design for mobile/desktop
- ✅ Beautiful UI with gradient themes

## 🔐 Security

### Environment Variables
If you need secrets (API keys, database credentials):

1. Go to app settings on Streamlit Cloud
2. Click "Secrets"
3. Add secrets in TOML format:
```toml
[database]
username = "your_username"
password = "your_password"

[api]
key = "your_api_key"
```

Access in code:
```python
import streamlit as st
db_user = st.secrets["database"]["username"]
```

## 💡 Best Practices

1. **Version Control**
   - Commit meaningful changes
   - Use branches for features
   - Tag releases

2. **Performance**
   - Cache expensive computations
   - Lazy load data when possible
   - Optimize queries

3. **Monitoring**
   - Check usage analytics
   - Monitor error logs
   - Update dependencies regularly

4. **Updates**
   - Test locally first
   - Deploy during low-traffic times
   - Keep changelog

## 📱 Sharing Your App

Share your deployed dashboard:
- 📧 Email link to stakeholders
- 💼 Add to LinkedIn portfolio
- 🎓 Include in thesis documentation
- 🌐 Share on social media

## 🔄 Updating Deployed App

Push changes to GitHub:
```bash
git add .
git commit -m "Update: description of changes"
git push
```

Streamlit Cloud will automatically redeploy!

## 📈 Usage Analytics

Monitor your app usage:
- View count
- User locations
- Peak usage times
- Error rates

Access via Streamlit Cloud dashboard.

## 🎓 For Thesis

Include in documentation:
- Live demo URL
- Screenshots of all features
- Deployment architecture diagram
- Performance metrics

## 🆘 Support

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Community Forum](https://discuss.streamlit.io)
- [GitHub Issues](https://github.com/your-username/IT-job-analysis-VN/issues)

---

**Note**: Free tier limitations:
- 1 app per user
- Public repositories only
- Resources: 1 CPU, 800 MB RAM
- Auto-sleep after inactivity

For unlimited apps and private repos, consider Streamlit Cloud Pro.
