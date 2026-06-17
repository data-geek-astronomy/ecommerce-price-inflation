# Deploy to Hugging Face Spaces

## Step 1: Create Hugging Face Account

1. Go to [huggingface.co](https://huggingface.co)
2. Click "Sign Up"
3. Create account with GitHub (recommended)

## Step 2: Create a New Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Fill in details:
   - **Space name**: `ecommerce-price-inflation`
   - **License**: MIT
   - **Space SDK**: Streamlit
   - **Visibility**: Public

4. Click "Create Space"

## Step 3: Push Your Code to HF Space

HuggingFace provides a Git repo for each Space. Clone and push:

```bash
# Navigate to your project
cd "/Users/aravindkumar/Documents/Claude/Projects/stripe portfolio project"

# Add HF as remote (replace YOUR_USERNAME)
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/ecommerce-price-inflation

# Push to Hugging Face
git push hf main
```

Alternatively, use HF CLI:

```bash
pip install huggingface-hub

huggingface-cli repo create ecommerce-price-inflation --type space --space-sdk streamlit

git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/ecommerce-price-inflation

git push hf main
```

## Step 4: Configure Space Settings

In HuggingFace Space settings:

1. **Runtime** → Select "CPU basic" (free tier)
2. **Permissions** → Keep "Public"
3. **Secrets** (optional) → Add BLS_API_KEY if using live data
4. **Requirements** → Auto-detected from `requirements.txt`

## Step 5: Monitor Deployment

- Space will auto-build when you push
- Watch the build logs in the Space page
- App launches at: `https://huggingface.co/spaces/YOUR_USERNAME/ecommerce-price-inflation`

## Project Files Structure for HF

```
ecommerce-price-inflation/
├── app/
│   └── streamlit_app.py          # ← HF runs this
├── src/
│   ├── scraper/
│   ├── analysis/
│   └── utils/
├── requirements.txt               # ← Automatically installed
├── README.md                       # ← Shown on Space page
├── README_HF.md                    # ← HF-specific info
└── .gitignore
```

## What HF Automatically Does

✅ Installs `requirements.txt`  
✅ Runs `streamlit run app/streamlit_app.py`  
✅ Handles SSL/HTTPS  
✅ Provides public URL  
✅ Auto-restarts on errors  
✅ Version control via Git  

## Hugging Face Space Features

### Free Tier (CPU Basic)
- 2 CPU cores
- 16 GB RAM
- Public access
- Perfect for this project

### Public Space Metrics
- View counter
- Hardware info visible
- Shareable link
- Embeddable widget

## Environment Variables on HF

Create `.env` file for secrets:

```bash
# In Space Settings → Secrets, add:
BLS_API_KEY=your_key_here
```

Access in code:
```python
import os
api_key = os.getenv('BLS_API_KEY', '')
```

## Space URL Structure

```
https://huggingface.co/spaces/data-geek-astronomy/ecommerce-price-inflation
```

Direct app link: 
```
https://data-geek-astronomy-ecommerce-price-inflation.hf.space
```

## Benefits of HF Spaces

✨ **Free hosting** for Streamlit apps  
🔗 **No credit card** needed  
📊 **Community discoverability**  
⚡ **Auto-scaling** (pay as you go for higher tiers)  
🔐 **Private/Public** control  
📈 **Analytics** included  

## Troubleshooting

### App won't start
- Check `requirements.txt` syntax
- Verify `app/streamlit_app.py` exists
- Check Space logs for errors

### Build fails
- Run locally: `streamlit run app/streamlit_app.py`
- Fix errors locally first
- Then push to HF

### Data not loading
- App generates data automatically
- No external files needed
- Check if data generation works locally

## Next Steps

1. **Update Profile**: Add project link to GitHub profile
2. **Share**: Post space URL on LinkedIn/Twitter
3. **Customize**: Add badge to README
4. **Monitor**: Check Space analytics

## Share Badge

Add to your GitHub README:

```markdown
[![Hugging Face Spaces](https://img.shields.io/badge/🤗-Open%20in%20Spaces-blue.svg)](https://huggingface.co/spaces/data-geek-astronomy/ecommerce-price-inflation)
```

## Resources

- [HF Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [Streamlit on HF](https://huggingface.co/docs/hub/spaces-config-reference)
- [Space Settings Guide](https://huggingface.co/docs/hub/spaces-overview)

---

**Your Space URL**: https://huggingface.co/spaces/data-geek-astronomy/ecommerce-price-inflation
