# 🚀 Launch Scripts

This folder contains convenience scripts for starting and managing the dashboard.

## 📜 Available Scripts

### **Windows Batch Files**

#### **START_DASHBOARD.bat**
Launch the dashboard on localhost (default port 8501)
```bash
# Double-click or run from command line:
START_DASHBOARD.bat
```

#### **START_DASHBOARD_NETWORK.bat**
Launch the dashboard with network access (accessible from other devices)
```bash
# Useful for VM deployments or multi-user access:
START_DASHBOARD_NETWORK.bat
```

#### **SETUP_FIRST_TIME.bat**
First-time setup script that:
- Checks Python installation
- Installs required dependencies
- Verifies data files
- Creates necessary folders

#### **STOP_DASHBOARD.bat**
Gracefully stop all running Streamlit instances
```bash
STOP_DASHBOARD.bat
```

#### **COPY_DATA_FROM_ONEDRIVE.bat**
Copy data files from OneDrive location (customize for your setup)

---

### **PowerShell Script**

#### **start_dashboard.ps1**
PowerShell version of the launcher with enhanced error handling
```powershell
# Run from PowerShell:
.\start_dashboard.ps1
```

---

## 🎯 Recommended Workflow

### First Time Setup
1. Run `SETUP_FIRST_TIME.bat`
2. Verify data files are in `/data/` folder
3. Run `START_DASHBOARD.bat`

### Daily Use
- **Local use**: `START_DASHBOARD.bat`
- **Network use**: `START_DASHBOARD_NETWORK.bat`
- **Stop**: `STOP_DASHBOARD.bat`

---

## 🐧 Linux/Mac Users

If you're on Linux or Mac, use the command line directly:

```bash
# Install dependencies (first time only)
pip install -r requirements.txt

# Run dashboard
streamlit run streamlit_dashboard_bnt113_real_data.py

# Run with network access
streamlit run streamlit_dashboard_bnt113_real_data.py --server.address=0.0.0.0
```

---

## ⚙️ Customization

All scripts can be edited with any text editor to:
- Change default ports
- Adjust Python paths
- Modify data file locations
- Add environment variables

---

## 🔧 Troubleshooting

**"Python not found"**
- Install Python 3.9+ from python.org
- Add Python to PATH

**"Streamlit not found"**
- Run `SETUP_FIRST_TIME.bat`
- Or manually: `pip install -r requirements.txt`

**"Port already in use"**
- Run `STOP_DASHBOARD.bat`
- Or change port in script (default: 8501)

---

**For more help, see**: [../docs/QUICK_REFERENCE.txt](../docs/QUICK_REFERENCE.txt)

