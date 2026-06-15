# Deployment Guide

## Local Deployment

### Quick Start
```bash
cd "/Users/aravindkumar/Documents/Claude/Projects/stripe portfolio project"

# Generate data and run dashboard
python src/scraper/main.py
python src/analysis/main_analysis.py
streamlit run app/streamlit_app.py
```

Dashboard opens at: `http://localhost:8501`

### From root directory
If data already exists:
```bash
streamlit run app/streamlit_app.py
```

## Streamlit Cloud Deployment (FREE)

### Step 1: Push to GitHub
```bash
git remote add origin https://github.com/yourusername/ecommerce-price-inflation.git
git push -u origin master
```

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your GitHub repo
4. Choose branch: `master`
5. Set main file path: `app/streamlit_app.py`
6. Click "Deploy"

The app will:
- Auto-install requirements.txt
- Generate sample data on first run
- Run analysis pipeline
- Launch dashboard

**Public URL**: `https://yourusername-ecommerce-price-inflation.streamlit.app`

### Step 3: Optional - Configure Secrets
Create `.streamlit/secrets.toml`:
```toml
bls_api_key = "your_bls_api_key"
```

Then push to GitHub - Streamlit automatically uses it.

## Docker Deployment

### Build & Run Locally
```bash
# Build image
docker build -t ecommerce-price-app .

# Run container
docker run -p 8501:8501 ecommerce-price-app
```

Access at: `http://localhost:8501`

### Deploy to Cloud

#### Heroku
```bash
# Install Heroku CLI, then:
heroku create your-app-name
git push heroku master
heroku open
```

#### Google Cloud Run
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/ecommerce-price-app
gcloud run deploy ecommerce-price-app \
  --image gcr.io/PROJECT-ID/ecommerce-price-app \
  --platform managed \
  --region us-central1
```

#### AWS EC2
```bash
# SSH into EC2 instance
git clone <repo-url>
cd ecommerce-price-inflation
docker build -t ecommerce .
docker run -d -p 80:8501 ecommerce
```

## Production Checklist

- [ ] Data is generated automatically on first run
- [ ] File paths work on different servers
- [ ] Requirements.txt is up-to-date
- [ ] .gitignore excludes sensitive files
- [ ] Error handling is robust
- [ ] Cache is configured for performance
- [ ] HTTPS is enabled (Streamlit Cloud auto-enables)
- [ ] Health checks pass
- [ ] Logs are visible for debugging

## Troubleshooting

### "No such file or directory" Error
**Solution**: The app now checks multiple paths. Ensure you:
1. Run `python src/scraper/main.py` first
2. Run `python src/analysis/main_analysis.py` second
3. Then launch the dashboard

### Data Not Updating
**Solution**: Clear Streamlit cache:
```bash
streamlit cache clear
```

### Port Already in Use
**Solution**: Use different port:
```bash
streamlit run app/streamlit_app.py --server.port 8502
```

### On Streamlit Cloud: Files Not Found
**Solution**: 
1. Verify files are committed to GitHub
2. Check repository is public
3. Redeploy app from Streamlit Cloud dashboard

## Performance Tips

1. **Cache Data**: Already implemented with `@st.cache_data`
2. **Optimize Images**: Plotly charts are lightweight
3. **Lazy Load**: Only load selected category data
4. **Monitor**: Check Streamlit Cloud logs for performance

## Security

- No sensitive data in code
- BLS API key goes in `.streamlit/secrets.toml`
- `.gitignore` excludes data and credentials
- HTTPS enabled automatically on Streamlit Cloud

---

**Recommended**: Deploy on Streamlit Cloud (free, no infrastructure needed)
