# BNT113 Clinical Trial Progress Dashboard - Demo Version

> ⚠️ **DEMONSTRATION DATA ONLY** - This dashboard contains completely fictional patient data for demonstration purposes. Do not use for any real clinical trial analysis or decision making.

## 🎯 Purpose

This demo version showcases the BNT113 clinical trial dashboard with realistic but entirely fictional data. Perfect for:

- **Portfolio demonstrations** on LinkedIn/GitHub
- **Technical presentations**
- **Code reviews**
- **Learning and training**

## 📊 Demo Data Overview

### Fictional Clinical Trial: BNT113-01
- **Study Type**: Cancer immunotherapy trial
- **Phase**: Phase II/III
- **Patient Population**: Head and neck cancer patients
- **Timeline**: April 2025 - September 2025

### Demo Dataset
- **488 patient records** across 15 CVLP sites
- **9 trial sites** with varying recruitment rates
- **Realistic timelines** and clinical workflows
- **Complete data pipeline** from screening to randomization

## 🚀 Quick Start

### Option 1: Run Locally
```bash
# Install dependencies (if needed)
pip install -r requirements.txt

# Run the dashboard
python -m streamlit run streamlit_dashboard_bnt113_real_data.py
```

### Option 2: Use Provided Scripts
```bash
# Windows
START_DASHBOARD.bat

# Or PowerShell
.\start_dashboard.ps1
```

### Option 3: Network Access
```bash
START_DASHBOARD_NETWORK.bat
```

## 📈 Dashboard Features Demonstrated

### ✅ Recruitment Analytics
- Monthly recruitment trends
- Site performance metrics
- Target vs actual comparisons
- Recruitment velocity analysis

### ✅ Patient Journey Tracking
- Screening → Referral → Consent → Randomization
- Screen failure analysis
- Timeline visualizations

### ✅ Site Performance
- Multi-site comparison dashboards
- Go-live date tracking
- Recruitment rate analysis

### ✅ Interactive Features
- Privacy mode controls
- Admin authentication
- Data quality metrics
- Export capabilities

## 🔒 Data Privacy & Security

### ✅ Safe for Sharing
- **No real patient data** - all data is synthetically generated
- **No PHI/PII** - all identifiers are fictional
- **No clinical outcomes** - only recruitment metrics
- **No site-identifying information** beyond generic names

### ✅ Realistic Structure
- Maintains exact column structure of real data
- Realistic clinical trial workflows
- Appropriate data distributions
- Professional presentation

## 📁 Demo Data Files

```
data/
├── BNT113-01 Master Tracker v1 15-Apr-2025.xlsx    # Main patient tracking data
├── BNT113-01 Screening Logs1.xlsx                 # Site screening logs
└── CVLP BNT113 reporting.xlsx                     # Performance reports
```

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib
- **Styling**: Custom CSS
- **Deployment**: Standalone Python application

## 📝 Usage Guidelines

### ✅ Appropriate Uses
- Personal portfolio demonstrations
- Technical interviews
- Educational presentations
- Code documentation
- Learning Streamlit development

### ❌ Not Appropriate For
- Real clinical trial management
- Patient data analysis
- Regulatory submissions
- Clinical decision making
- Any medical or research purposes

## 🔄 From Demo to Real Data

To use with real clinical trial data:

1. **Replace demo files** in the `data/` folder with real Excel files
2. **Ensure column names match** the expected structure
3. **Update site configurations** if needed
4. **Test thoroughly** with real data before production use

## 📞 Support

For questions about the demo or technical implementation:
- Review the main documentation in `COMPLETE_SETUP_GUIDE.md`
- Check `QUICK_REFERENCE.txt` for quick answers
- Examine the code in `streamlit_dashboard_bnt113_real_data.py`

---

**⚠️ LEGAL DISCLAIMER**: This demo contains fictional data only. The creators assume no responsibility for any misuse of this demonstration software or data. Always use real clinical trial data responsibly and in accordance with applicable regulations and ethical guidelines.
