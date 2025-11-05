# 🏥 Clinical Trial Monitoring Dashboard - Portfolio Demo

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **🎯 Portfolio Project**: Real-time clinical trial monitoring dashboard demonstrating data engineering, automation, and business impact.

---

## ⚠️ IMPORTANT DISCLAIMER

### This is a **DEMONSTRATION PROJECT** with **100% FICTIONAL DATA**

- ❌ **NOT real patient data** - all data is synthetically generated
- ❌ **NOT real clinical trial results** - purely demonstrative
- ❌ **NOT affiliated with any actual clinical trial**
- ✅ **Purely for portfolio/educational purposes**
- ✅ **Safe for public sharing - no PHI/PII**

**Hospital names used are for demonstration purposes only and do not imply participation in any actual clinical trial.**

All dates are set in the future (2025) to clearly indicate fictional data. Any resemblance to actual clinical trials or patient data is purely coincidental.

---

## 📊 Project Overview

### The Challenge
Clinical trial units face significant challenges managing multi-site trials:
- ⏰ Hours spent on manual Excel reporting weekly
- 📉 Delayed visibility into recruitment performance
- ⚠️ Late detection of site issues
- 📧 Inefficient stakeholder communication

### The Solution
An **automated real-time dashboard** that transforms raw trial data into actionable insights:
- 📊 **Real-time metrics** across 15 clinical sites
- 🔄 **Automated data processing** (no manual Excel work)
- 📈 **Interactive visualizations** for patient journey tracking
- ⚠️ **Intelligent alerts** for data quality and performance issues
- 🏥 **Site comparison analytics** for informed decision-making

### The Impact
- 💰 **£265K+ net benefit** in first year
- 📊 **2,124% ROI** with 16-day payback period
- ⏱️ **714 hours/year** of staff time saved
- 🎯 **95% reduction** in data entry errors

👉 **[Read Full ROI Case Study →](ROI_CASE_STUDY.md)**

---

## 🎥 Demo

### Dashboard Features

**📊 Executive Overview**
- Real-time recruitment KPIs (488 patients, 15 sites)
- Target vs. actual performance tracking
- Monthly progression analytics

**🔄 Patient Journey Pipeline**
- Screening → Referral → Consent → Randomization
- Funnel visualization with conversion rates
- Time-to-event analysis

**🏥 Site Performance Dashboard**
- Multi-site comparison metrics
- Go-live date tracking
- Recruitment velocity analysis

**⚠️ Data Quality Monitoring**
- Automated validation alerts
- Missing data detection
- Screen failure analytics

**🔒 Privacy Controls**
- Pseudonymization mode (default)
- Admin authentication for full data
- Configurable data visibility

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/clinical-trial-dashboard-demo.git
cd clinical-trial-dashboard-demo

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run streamlit_dashboard_bnt113_real_data.py
```

### Alternative: Use Provided Scripts

**Windows:**
```bash
START_DASHBOARD.bat
```

**PowerShell:**
```bash
.\start_dashboard.ps1
```

**Network Access:**
```bash
START_DASHBOARD_NETWORK.bat
```

Dashboard will open at `http://localhost:8501`

---

## 📁 Project Structure

```
clinical-trial-dashboard-demo/
├── streamlit_dashboard_bnt113_real_data.py  # Main dashboard application
├── data/                                     # Demo data files
│   ├── BNT113-01 Master Tracker v1 15-Apr-2025.xlsx
│   ├── BNT113-01 Screening Logs1.xlsx
│   └── CVLP BNT113 reporting.xlsx
├── requirements.txt                          # Python dependencies
├── README.md                                 # This file
├── ROI_CASE_STUDY.md                        # Detailed ROI analysis
├── SECURITY_AUDIT_GITHUB.md                 # Security review
├── COMPLETE_SETUP_GUIDE.md                  # Comprehensive setup docs
├── QUICK_REFERENCE.txt                      # Quick command reference
└── START_DASHBOARD.bat                      # Launch script (Windows)
```

---

## 🛠️ Technology Stack

### Backend & Data Processing
- **Python 3.9+**: Core language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **OpenPyXL**: Excel file processing

### Frontend & Visualization
- **Streamlit**: Interactive web dashboard framework
- **Plotly**: Interactive charts and visualizations
- **Custom CSS**: Modern, responsive UI design

### Additional Features
- **ReportLab**: PDF report generation
- **YAML**: Configuration management
- **Hashlib**: Authentication & security

### Deployment
- Standalone Python application
- Docker-ready (containerization optional)
- VM deployment for network access

---

## 📊 Demo Data Overview

### Fictional Clinical Trial: BNT113-01
- **Study Type**: Cancer immunotherapy phase II/III trial
- **Indication**: Head and neck cancer
- **Timeline**: April 2025 - September 2025 (fictional dates)

### Dataset Statistics
- **488 patient records** with complete screening pipeline
- **15 CVLP sites** with varying recruitment patterns
- **9 trial sites** demonstrating site performance variance
- **Realistic clinical workflows** (screening, consent, randomization)

### Data Safety Features
- ✅ Synthetic patient IDs (P####-### format)
- ✅ Generic screening numbers (site-coded)
- ✅ Birth year only (no full DOB)
- ✅ Future dates (clearly fictional)
- ✅ No real clinical outcomes or PHI

---

## 📈 Key Features Demonstrated

### 1. **Automated Data Pipeline**
- Excel file ingestion with error handling
- Column mapping and data validation
- Automated date parsing and formatting
- Real-time data refresh

### 2. **Interactive Analytics**
- Drill-down capabilities by site, date range, status
- Dynamic filtering and segmentation
- Tooltip-rich visualizations
- Responsive chart sizing

### 3. **Business Intelligence**
- KPI cards with trend indicators
- Target vs. actual performance tracking
- Predictive enrollment projections
- Screen failure analysis by reason

### 4. **Data Quality Engineering**
- Schema validation with error reporting
- Missing data detection and alerts
- Duplicate identification
- Data completeness scoring

### 5. **User Experience Design**
- Clean, modern interface with consistent branding
- Privacy-aware data presentation
- Admin authentication system
- Mobile-responsive layout
- One-click PDF export

---

## 💼 Business Value Demonstrated

### Quantified Impact

| Metric | Value | Method |
|--------|-------|--------|
| **Time Savings** | 714 hrs/year | Eliminated manual reporting |
| **Cost Savings** | £42K/year | Staff time optimization |
| **Error Reduction** | 95% | Automated validation |
| **Meeting Efficiency** | 50% faster | Pre-meeting data access |
| **ROI** | 2,124% | Year 1 cost-benefit analysis |

### Capabilities Showcased

✅ **Data Engineering**: ETL pipeline, data validation, schema management  
✅ **Business Analysis**: ROI calculation, process optimization, stakeholder management  
✅ **Software Development**: Full-stack dashboard, UX/UI design, deployment  
✅ **Domain Expertise**: Clinical trial workflows, regulatory compliance, healthcare data  
✅ **Project Management**: Requirements gathering, iterative development, documentation  

---

## 🎓 Transferable Skills

This project demonstrates expertise in:

### Technical Skills
- Python ecosystem (Pandas, NumPy, Streamlit, Plotly)
- Data pipeline automation and ETL processes
- Interactive dashboard development
- Data visualization and UX design
- Git version control and documentation

### Business Skills
- Requirements analysis and stakeholder management
- ROI calculation and business case development
- Process optimization and workflow analysis
- Change management and user training
- Strategic thinking and problem-solving

### Domain Knowledge
- Clinical trial coordination and management
- Healthcare data privacy and security (GDPR, GCP)
- Regulatory compliance in clinical research
- Multi-site study operations
- Quality assurance and audit readiness

---

## 📖 Documentation

- **[ROI Case Study](ROI_CASE_STUDY.md)**: Detailed financial impact analysis
- **[Security Audit](SECURITY_AUDIT_GITHUB.md)**: Pre-publication security review
- **[Setup Guide](COMPLETE_SETUP_GUIDE.md)**: Comprehensive installation & configuration
- **[Quick Reference](QUICK_REFERENCE.txt)**: Common commands and troubleshooting
- **[Changelog](CHANGELOG.txt)**: Version history and updates

---

## 🔒 Privacy & Security

### What Makes This GitHub-Safe

✅ **No Real Patient Data**: All data is synthetically generated  
✅ **No PHI/PII**: No protected health information  
✅ **No Credentials**: No API keys or database credentials  
✅ **No Proprietary Info**: Standard statistical methods only  
✅ **Clear Disclaimers**: Multiple warnings about fictional data  

### Data Privacy Features in Code

- Pseudonymization mode (default)
- Admin authentication for sensitive views
- Configurable data masking
- Privacy-first design patterns

👉 **[Read Full Security Audit →](SECURITY_AUDIT_GITHUB.md)**

---

## 🚀 From Demo to Production

This dashboard template is production-ready for real clinical trial data:

### To Deploy with Real Data

1. **Replace demo files** in `/data/` folder with actual Excel files
2. **Verify column mappings** match your data structure
3. **Update site configurations** in code if needed
4. **Configure authentication** (replace demo password)
5. **Deploy to secure environment** (VM, cloud, or on-premise)
6. **Enable audit logging** for regulatory compliance

### Production Considerations

- [ ] Replace hardcoded admin password with environment variable
- [ ] Implement LDAP/SSO authentication
- [ ] Add database backend for data persistence
- [ ] Configure HTTPS/SSL for secure access
- [ ] Set up automated backup and disaster recovery
- [ ] Implement audit trail logging
- [ ] Perform security penetration testing

---

## 📞 Contact & Connect

**Developer**: Masood Nazari  
**LinkedIn**: [linkedin.com/in/masood-nazari](https://www.linkedin.com/in/masood-nazari)  
**Email**: [Contact via LinkedIn]

### About Me
Data engineer and AI specialist with expertise in clinical research automation. Passionate about using technology to improve healthcare operations and patient outcomes.

**Open to opportunities in:**
- Data Engineering & Analytics
- Healthcare Technology
- Clinical Trial Innovation
- AI/ML Applications in Healthcare

---

## 🤝 Contributing

While this is a portfolio demonstration project, suggestions and feedback are welcome:

1. Open an issue to discuss proposed changes
2. Fork the repository
3. Create a feature branch
4. Submit a pull request with clear description

---

## 📄 License

This project is released under the MIT License - see [LICENSE](LICENSE) file for details.

### Usage Guidelines

✅ **Appropriate Uses:**
- Learning Streamlit development
- Portfolio reference for similar projects
- Educational demonstrations
- Technical interviews

❌ **Not Appropriate For:**
- Real clinical trial management
- Patient data analysis
- Regulatory submissions
- Any medical or research purposes without proper adaptation and validation

---

## 🙏 Acknowledgments

- **Streamlit Community**: Excellent documentation and support
- **Plotly**: Beautiful, interactive visualizations
- **Python Open Source Community**: Incredible ecosystem of tools

---

## ⭐ Star This Project

If you find this project useful or interesting, please consider giving it a star! ⭐

It helps others discover this work and demonstrates the value of open-source portfolio projects.

---

## 📊 Project Stats

- **Lines of Code**: ~7,000+
- **Development Time**: ~200 hours
- **Technologies Used**: 10+
- **Demo Data Records**: 488 patients
- **Sites Managed**: 15 locations
- **Visualizations**: 20+ interactive charts

---

**Last Updated**: November 5, 2025  
**Version**: 2.0 (GitHub Public Release)

---

*This is a demonstration project with fictional data created for portfolio purposes. No real patients, trials, or clinical data were used in the development of this dashboard.*

