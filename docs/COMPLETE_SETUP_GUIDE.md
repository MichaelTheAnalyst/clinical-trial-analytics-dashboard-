# BNT113 Dashboard - Complete Setup & User Guide

> **Comprehensive documentation for deploying and using the BNT113 Trial Dashboard on Windows Server VM**

---

## 📑 Table of Contents

1. [Quick Start](#quick-start)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Troubleshooting](#troubleshooting)
7. [Features](#features)
8. [Maintenance](#maintenance)
9. [Security](#security)
10. [Support](#support)

---

## 🚀 Quick Start

### For First-Time Setup (5 Minutes)

**On Your VM (SRV04750.soton.ac.uk):**

```batch
1. Copy BNT113_VM_DEPLOYMENT folder to: F:\projects\BNT113_Dashboard\
2. Double-click: SETUP_FIRST_TIME.bat
3. Double-click: COPY_DATA_FROM_ONEDRIVE.bat  
4. Double-click: START_DASHBOARD.bat
```

**Access:** `http://localhost:8501`  
**Login:** admin / sctu2024 ⚠️ Change immediately!

### For Subsequent Use

```batch
Double-click: START_DASHBOARD.bat
```

---

## 💻 System Requirements

### Minimum
- **OS:** Windows Server 2012 R2 or Windows 10+
- **Python:** 3.8 or higher
- **RAM:** 2 GB available
- **Storage:** 500 MB free
- **Network:** Internet (initial setup only)

### Recommended
- **OS:** Windows Server 2016 or later
- **Python:** 3.10 or higher
- **RAM:** 4 GB available
- **Storage:** 1 GB free
- **Browser:** Chrome, Firefox, or Edge (latest)

### Python Packages Required
```
streamlit >= 1.28.0
pandas >= 1.5.0
plotly >= 5.15.0
numpy >= 1.24.0
openpyxl >= 3.1.0
reportlab >= 4.0.0
Pillow >= 9.5.0
pandera >= 0.17.0
PyYAML >= 6.0.0
```

---

## 📦 Installation

### Step 1: Install Python (If Needed)

1. Download from: https://www.python.org/downloads/
2. Run installer
3. ✅ **CRITICAL:** Check "Add Python to PATH"
4. Complete installation
5. Verify: Open Command Prompt, type `python --version`

### Step 2: Copy Files to VM

**Option A - OneDrive (Recommended):**
- Files sync automatically from your OneDrive folder
- Check: `F:\projects\OneDrive_*\bnt122 progress report dashboard\BNT113_VM_DEPLOYMENT\`

**Option B - Manual Copy:**
- Copy entire `BNT113_VM_DEPLOYMENT` folder
- Destination: `F:\projects\BNT113_Dashboard\`

### Step 3: Run First-Time Setup

```batch
cd F:\projects\BNT113_Dashboard
SETUP_FIRST_TIME.bat
```

This will:
- ✅ Check Python installation
- ✅ Install all dependencies
- ✅ Verify setup
- ✅ Offer to start dashboard

**Time:** ~5 minutes (one-time only)

### Step 4: Copy Data Files

**Automated Method:**
```batch
COPY_DATA_FROM_ONEDRIVE.bat
```

**Manual Method:**
Copy from: `F:\projects\OneDrive_2025-10-21\bnt122 progress report dashboard\BNT113 real data\`  
To: `F:\projects\BNT113_Dashboard\data\`

**Required Files:**
- ✅ `BNT113-01 Master Tracker v1 15-Apr-2025.xlsx`
- ⚪ `BNT113-01 Screening Logs1.xlsx` (optional, enhances accuracy)
- ⚪ `CVLP BNT113 reporting.xlsx` (optional)

### Step 5: Start Dashboard

```batch
START_DASHBOARD.bat
```

Browser opens automatically at `http://localhost:8501`

---

## ⚙️ Configuration

### File Locations

```
BNT113_Dashboard/
├── streamlit_dashboard_bnt113_real_data.py   # Main application
├── requirements.txt                           # Dependencies
├── START_DASHBOARD.bat                        # Local launcher
├── START_DASHBOARD_NETWORK.bat                # Network launcher
├── STOP_DASHBOARD.bat                         # Stop script
├── data/                                      # Excel files
│   ├── BNT113-01 Master Tracker...xlsx
│   ├── BNT113-01 Screening Logs...xlsx
│   └── CVLP BNT113 reporting.xlsx
└── assets/                                    # Logo & images
    └── SCTU Logo (mediabin resized).jpg
```

### Access Modes

**Local Access (Default):**
```
URL: http://localhost:8501
Use: START_DASHBOARD.bat
Security: High (VM only)
```

**Network Access:**
```
URL: http://SRV04750.soton.ac.uk:8501
Use: START_DASHBOARD_NETWORK.bat
Security: Medium (requires secure network)
```

⚠️ **Only enable network access on secure networks**

### Port Configuration

Default port: `8501`

To change (if port is in use):
1. Edit `START_DASHBOARD.bat`
2. Change `--server.port 8501` to `--server.port 8502`
3. Save and restart

### Admin Credentials

**Default:**
- Username: `admin`
- Password: `sctu2024`

**⚠️ Change immediately after first login via dashboard settings**

---

## 📊 Usage

### Uploading Data Files

1. Open dashboard
2. Sidebar → File upload sections
3. Upload required Excel files:
   - Master Tracker (required)
   - Screening Logs (optional)
   - CVLP Reporting (optional)

### Privacy Mode

**Enable for presentations/screenshots:**
1. Sidebar → Privacy toggle
2. Select "Privacy Mode"
3. Sensitive data is masked

**Full Data Mode:**
- Requires admin login
- Shows all patient data
- Use for analysis only

### Key Features

#### 1. Trial Overview Cards
- Total Sites, Open Sites
- Total Patients, Consented
- Key performance metrics

#### 2. Monthly Trial Metrics Table
- Recruitment tracking by month
- Targets vs. actuals
- Future projections
- RAG status indicators

#### 3. Site Performance Table
- Performance by site
- Days to first referral
- Days since last patient
- Average monthly rates
- Trend analysis
- **Gradient RAG coloring** for quick status assessment

#### 4. Interactive Charts
- Monthly trends
- Site comparisons
- Performance heatmaps
- Recruitment funnels

#### 5. Export Functionality
- Export as HTML
- Select specific sections
- Include/exclude timestamps
- Download to local machine

### Exporting Reports

1. Scroll to bottom → "📥 Export Dashboard"
2. Select content to include:
   - ☑ Trial Overview Cards
   - ☑ Monthly Trial Metrics
   - ☑ Site Performance
   - ☑ Charts & Graphs
3. Click "📥 Export as HTML"
4. Download appears → Save file
5. Open in any browser

**To Create PDF:**
1. Export as HTML
2. Open HTML in browser
3. Press Ctrl+P
4. Select "Save as PDF"

---

## 🐛 Troubleshooting

### Dashboard Won't Start

**Problem:** `Python is not installed`
```
Solution: 
1. Install Python 3.8+ from python.org
2. ✅ Check "Add Python to PATH" during installation
3. Restart Command Prompt
4. Verify: python --version
```

**Problem:** `'streamlit' is not recognized`
```
Solution: Fixed in all launch scripts!
Scripts now use: python -m streamlit
Just run START_DASHBOARD.bat again
```

**Problem:** `Port already in use`
```
Solution:
1. Run STOP_DASHBOARD.bat
2. Then START_DASHBOARD.bat
OR
Change port in START_DASHBOARD.bat to 8502
```

**Problem:** `Module not found errors`
```
Solution:
pip install -r requirements.txt --force-reinstall
```

### Data Issues

**Problem:** Excel file won't load
```
Solution:
- Close Excel file if open
- Check file path is correct
- Verify file format is .xlsx
- Check file permissions
- Re-upload through dashboard
```

**Problem:** Numbers showing as 0
```
Solution:
- Verify date columns are formatted correctly
- Check column names match expected format
- Review data file structure
- Check sidebar status messages
```

**Problem:** Missing data in tables
```
Solution:
- Ensure all required Excel files are uploaded
- Check file dates match expected format
- Verify column headers in Excel files
- Upload Screening Logs for enhanced data
```

### Performance Issues

**Problem:** Dashboard is slow
```
Solution:
- Reduce data file size
- Close other applications
- Increase VM resources
- Clear browser cache
- Restart dashboard
```

**Problem:** Browser timeout
```
Solution:
- Check network connection
- Restart dashboard
- Try different browser
- Check VM resources
```

### Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `IndentationError` | File corruption | Re-copy dashboard file |
| `KeyError: column` | Excel format changed | Check column names in Excel |
| `PermissionError` | File in use | Close Excel, restart dashboard |
| `MemoryError` | Large files | Reduce data file size |
| Connection refused | Port blocked | Check firewall, change port |

---

## ✨ Features

### Trial Metrics

**Monthly Tracking:**
- Open Sites (Actual vs. Target)
- Referred patients
- Reviewed patients
- Recruited to CVLP
- Consented patients (pre-screen & main trial)
- Randomised patients
- Screen failures
- Future projections

**Calculations:**
- Cumulative and monthly views
- Target achievement %
- Projected targets
- Trend analysis

### Site Performance Analytics

**Key Metrics:**
- Days from site open to first referral
- Days since last patient referred
- Average monthly recruitment
- Change in recruitment rate
- Average monthly referrals
- Change in referral rate

**Visual Indicators:**
- **Gradient RAG coloring:**
  - Green: Excellent (0-30 days)
  - Light Green: Good (31-60 days)
  - Yellow: Attention needed (61-75 days)
  - Orange: Concern (76-90 days)
  - Light Red: Action required (91-120 days)
  - Dark Red: Critical (>120 days)

**Site Trends:**
- Individual site monthly performance
- Detailed breakdown tables
- Comparative analysis
- Line charts for trends

### Data Validation

- Automatic date format detection
- Column name matching
- Data type validation
- Missing data handling
- Error logging

### Security Features

**Authentication:**
- Admin login required for full data
- Session management
- Password protection

**Privacy Mode:**
- Masks patient identifiers
- Hides site-specific details
- Safe for presentations
- Screenshot-friendly

**Data Security:**
- All processing local
- No external transmission
- Secure file handling
- Session-based access

---

## 🔄 Maintenance

### Regular Updates

**Daily:**
- Upload new data files as received
- Check dashboard for errors

**Weekly:**
- Review site performance metrics
- Export reports for records
- Verify data accuracy

**Monthly:**
- Archive old reports
- Update target values if needed
- Review performance trends
- Clean up old data files

### Updating Data

**Method 1 - File Upload:**
1. Dashboard → Sidebar
2. Upload new Excel files
3. Dashboard auto-processes

**Method 2 - File Replacement:**
1. Stop dashboard
2. Replace files in `data/` folder
3. Restart dashboard

### Updating Dashboard

1. Receive new `streamlit_dashboard_bnt113_real_data.py`
2. Stop dashboard (Ctrl+C or STOP_DASHBOARD.bat)
3. Replace the file
4. Check `requirements.txt` for new dependencies
5. Run: `pip install -r requirements.txt --upgrade`
6. Restart dashboard

### Backups

**What to Backup:**
- All Excel files in `data/`
- Exported HTML reports
- Configuration files

**Backup Schedule:**
- Daily: Excel data files
- Weekly: Exported reports
- Monthly: Full folder backup

**Backup Location:**
```
F:\Backups\BNT113_Dashboard\[Date]\
```

### Version Control

**Current Version:** 2.0.2 (October 2025)

**Version History:**
- v2.0.2: Sidebar cleanup, bug fixes
- v2.0.1: Streamlit command fix, schema warning removed
- v2.0.0: Initial VM deployment

**Check for Updates:**
- Contact SCTU Data Management Team
- Review changelog in package

---

## 🔐 Security

### Best Practices

1. **Change Default Password**
   - First login → Settings
   - Use strong password
   - Store securely

2. **Enable Privacy Mode**
   - For presentations
   - For screenshots
   - When sharing screen

3. **Network Access**
   - Use only on secure networks
   - Enable only when needed
   - Monitor access logs

4. **Data Handling**
   - Keep Excel files secure
   - Regular backups
   - Proper file permissions
   - Secure disposal of old files

5. **VM Security**
   - Keep VM updated
   - Firewall configured
   - Access controls in place
   - Regular security reviews

### Compliance

- All data processing is local
- No external data transmission
- GDPR-compliant data handling
- Audit trail via exports
- Secure authentication

### Firewall Configuration

**If enabling network access:**
```
Port: 8501
Protocol: TCP
Direction: Inbound
Action: Allow
Scope: Secure network only
```

---

## 📞 Support

### Documentation

All documentation in this package:
- **This file:** Complete setup & usage guide
- `QUICK_REFERENCE.txt`: Command reference
- `CHANGELOG.txt`: Version history & recent fixes
- Inline help in dashboard

### Contact

**SCTU Data Management Team**
- University of Southampton
- Southampton Clinical Trials Unit

### Self-Help Resources

**Python:**
- https://www.python.org/downloads/
- https://docs.python.org/

**Streamlit:**
- https://docs.streamlit.io/
- https://discuss.streamlit.io/

**Pandas:**
- https://pandas.pydata.org/docs/
- https://pandas.pydata.org/pandas-docs/stable/user_guide/

### Reporting Issues

When reporting problems, include:
1. Error message (full text)
2. Dashboard version
3. Python version (`python --version`)
4. Steps to reproduce
5. Screenshot (if applicable)
6. Data file info (no sensitive data)

---

## 📋 Quick Reference

### Common Commands

```batch
# Start dashboard (local)
START_DASHBOARD.bat

# Start dashboard (network)
START_DASHBOARD_NETWORK.bat

# Stop dashboard
STOP_DASHBOARD.bat
Ctrl+C in Command Prompt

# Copy data files
COPY_DATA_FROM_ONEDRIVE.bat

# First-time setup
SETUP_FIRST_TIME.bat

# Check Python
python --version

# Install dependencies
pip install -r requirements.txt

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### File Locations

```
Dashboard: F:\projects\BNT113_Dashboard\
Data: F:\projects\BNT113_Dashboard\data\
OneDrive: F:\projects\OneDrive_*\bnt122 progress report dashboard\
```

### URLs

```
Local: http://localhost:8501
Network: http://SRV04750.soton.ac.uk:8501
```

### Keyboard Shortcuts

```
F5: Refresh dashboard
Ctrl+C: Stop dashboard (in terminal)
Ctrl+P: Print/Export to PDF (in browser)
Ctrl+F: Find in page (in browser)
```

---

## 🎯 Success Checklist

Before going live:

- [ ] Python 3.8+ installed
- [ ] All dependencies installed
- [ ] Data files uploaded
- [ ] Dashboard starts without errors
- [ ] Can access at localhost:8501
- [ ] Admin login works
- [ ] Data displays correctly
- [ ] All tables render
- [ ] Charts display
- [ ] Privacy mode functions
- [ ] Export works
- [ ] Admin password changed
- [ ] Backup procedure established
- [ ] Team trained
- [ ] Support contacts identified

---

## 📝 Notes

### Data Sources

The dashboard integrates multiple data sources:
1. **Master Tracker:** Primary trial data
2. **Screening Logs:** Site-specific screening
3. **CVLP Reporting:** Additional metrics

### Calculations

- **Cumulative:** Running totals to date
- **Monthly:** Period-specific counts
- **Targets:** Based on site count × rates
- **Projections:** Trend-based forecasts

### Known Limitations

- Maximum file upload: 200 MB
- Recommended max sites: 50
- Refresh rate: Manual (F5)
- Export format: HTML (PDF via print)

### Future Enhancements

- Direct PDF export
- Email integration
- Automated alerts
- Mobile app
- API access

---

## 🎉 You're Ready!

Your BNT113 Trial Dashboard is ready to use. For quick help, press `?` in the dashboard or check the Quick Reference section above.

**Need immediate help?** Start with the Troubleshooting section or contact SCTU Data Management Team.

---

**Version:** 2.0.2 | **Last Updated:** October 2025 | **Package:** VM Deployment v1.0

