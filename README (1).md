# CareRewards Lead Manager v1

Self-insured employer pipeline management tool for market segmentation and prioritization.

## Features

✅ **Smart Filtering**
- Geographic priority tiers (Tier 1: MA/NY/CA, Tier 2: IL/TX/PA/FL/NJ/OH)
- Participant size filters with quick buttons (1K+, 2.5K+, 5K+)
- Market segment filtering (Mid-Market vs Large)
- Search by employer name or EIN

✅ **Visual Analytics**
- Summary dashboard with key metrics
- Geographic distribution charts
- Participant size distribution
- Real-time filter updates

✅ **Priority Lead Management**
- Top 50 priority leads (auto-sorted by tier + participant count)
- One-click export for instant outreach
- Pre-generated Perplexity queries for lead enrichment

✅ **Export Capabilities**
- Download filtered results as CSV
- Export with Perplexity enrichment queries
- Top 50 priority leads instant export

---

## Quick Start (5 Minutes)

### Prerequisites
- Python 3.8+ installed
- Your `self_insured_crm_list.csv` file

### Local Setup

1. **Create project folder and add files**
```bash
mkdir careRewards-crm
cd careRewards-crm
```

2. **Copy these files into the folder:**
   - `app.py` (the Streamlit application)
   - `requirements.txt` (Python dependencies)
   - `self_insured_crm_list.csv` (your lead data)

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the app**
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## Deploy to Streamlit Cloud (Free Hosting - 15 Minutes)

### Step 1: Create GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click "+" → "New repository"
3. Name it `careRewards-crm` (or any name)
4. Make it **Public** (required for free Streamlit hosting)
5. Click "Create repository"

### Step 2: Upload Your Files

**Option A: Via GitHub Web Interface (Easiest)**
1. On your new repo page, click "uploading an existing file"
2. Drag and drop these 3 files:
   - `app.py`
   - `requirements.txt`
   - `self_insured_crm_list.csv`
3. Click "Commit changes"

**Option B: Via Git Command Line**
```bash
cd careRewards-crm
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/careRewards-crm.git
git push -u origin main
```

### Step 3: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select:
   - **Repository**: `YOUR_USERNAME/careRewards-crm`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click "Deploy"

**Your app will be live at:** `https://YOUR_USERNAME-careRewards-crm.streamlit.app`

⏱️ First deployment takes ~3-5 minutes. Subsequent updates deploy in ~30 seconds.

---

## Usage Guide

### Dashboard Tab
- View high-level metrics (total leads, median participants, tier 1 count)
- Analyze geographic and size distributions
- Understand your pipeline at a glance

### Lead Table Tab
- Browse paginated lead list (50 per page)
- Sort and search through filtered results
- Export filtered leads with/without Perplexity queries
- Generate individual Perplexity enrichment queries

### Top Priority Tab
- **Instant access to top 50 leads** (Tier 1 first, then by size)
- One-click export for immediate outreach
- Priority breakdown metrics

---

## Filtering Strategy

### Quick Workflow for Targeted Outreach

**Scenario 1: High-Value MA/NY/CA Leads**
1. Click "Tier 1 States" button
2. Click "5K+" button
3. Go to "Top Priority" tab
4. Click "Export Top 50 Priority Leads"
→ Instant CSV with your best prospects

**Scenario 2: Mid-Market IL/TX Focus**
1. Select IL and TX from state dropdown
2. Set participant range to 1,000-5,000
3. Select "Mid-Market (500-5K)" segment
4. Export filtered results

**Scenario 3: Large Employers Nationwide**
1. Click "All States" button
2. Click "5K+" button
3. Select "Large (5K+)" segment only
4. Browse and export

---

## Perplexity Enrichment Workflow

### Individual Lead (Manual - v1)
1. In "Lead Table" tab, select an employer from dropdown
2. Copy the generated Perplexity query
3. Paste into Perplexity Pro
4. Save contact details separately (Excel, notes, etc.)

### Bulk Enrichment (Manual - v1)
1. Export filtered leads with Perplexity queries
2. Open CSV in Excel
3. Copy queries one by one to Perplexity Pro
4. Add contact details in new columns

**Coming in v2:** In-app contact storage so you can paste Perplexity results directly into the tool.

---

## Updating Your Data

### Local Version
1. Replace `self_insured_crm_list.csv` in your project folder
2. Refresh browser (Ctrl+R or Cmd+R)

### Streamlit Cloud Version
1. Update CSV in GitHub repo
   - Go to repo → Click on CSV file → Click pencil icon → Upload new version
   - Or use git: `git add . && git commit -m "Update leads" && git push`
2. Streamlit auto-redeploys in ~30 seconds

---

## Troubleshooting

### "FileNotFoundError: self_insured_crm_list.csv not found"
**Fix:** Ensure the CSV file is in the same folder as `app.py`

### App won't start locally
**Fix:** 
```bash
pip install --upgrade streamlit pandas plotly
streamlit run app.py
```

### Streamlit Cloud deploy fails
**Common causes:**
- CSV file not uploaded to GitHub repo
- Typo in file names (case-sensitive!)
- Private repo (must be public for free tier)

**Check deployment logs:**
- On Streamlit Cloud dashboard, click your app → "Manage app" → View logs

### Filters not updating
**Fix:** Click "Clear cache" in Streamlit menu (top right ⋮) → "Clear cache"

---

## What's Next?

### When to Add v2 Features
- **After you've contacted 50-100 leads manually**: Add status tracking (Not Contacted / Contacted / Meeting / etc.)
- **When Perplexity copy-paste becomes tedious**: Add in-app enrichment storage (paste contact details directly)
- **When you need prioritization logic**: Add lead scoring (auto-calculate: State tier × Participant size)

### When to Move to Claude Code
- **Bug fixes**: If you get errors running locally, bring them to Claude Code
- **Adding v2 features**: Describe what you want in Claude Chat → I'll give updated code → test in Claude Code
- **Deployment issues**: Claude Code can help debug Streamlit Cloud problems

### When to Migrate to HubSpot/Salesforce
- **$10K+ MRR**: You can afford real CRM licensing
- **>500 active leads**: Need robust pipeline management
- **Team of 3+**: Multiple users need simultaneous access

For now, this Streamlit app gives you 80% of CRM functionality at 0% of the cost.

---

## Architecture Notes

**Tech Stack:**
- **Streamlit**: Web framework (free hosting on Community Cloud)
- **Pandas**: Data manipulation
- **Plotly**: Interactive charts

**Data Storage (v1):**
- CSV file in repo (14K+ leads)
- No database needed yet
- Filters applied in-memory (instant performance)

**Security (v1):**
- App is public (anyone with link can view)
- **No PII stored** (just company names, EINs, participant counts)
- v2 will add basic password protection when contact details are added

---

## Cost Breakdown

| Component | Cost |
|-----------|------|
| Streamlit Cloud hosting | **$0** (free tier) |
| GitHub repo | **$0** (public repo) |
| Python/Pandas/Plotly | **$0** (open source) |
| Your time investment | 30 min setup + 5 min/week maintenance |
| **TOTAL** | **$0/month** |

Compare to:
- HubSpot CRM: $450/month (Starter tier)
- Salesforce: $1,000+/month
- Custom dev shop: $10K+ upfront

---

## Support

**Got errors?** → Bring them to Claude Code for debugging  
**Want new features?** → Describe in Claude Chat, I'll update the code  
**Need help deploying?** → Check Streamlit Cloud docs or bring issues to Claude Code

**Feedback?** → Update this README with notes for v2 (save in GitHub repo)

---

Built with ❤️ for CareRewards | v1.0 | February 2025
