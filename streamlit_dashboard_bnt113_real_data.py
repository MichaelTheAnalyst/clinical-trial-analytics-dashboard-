import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
import plotly.graph_objects as go
import os
import hashlib
import re
import base64
import io
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import plotly.io as pio
import tempfile
import yaml
from pathlib import Path

# =============================================================================
# UNIFIED COLOR PALETTE - Brand Consistency
# =============================================================================

COLOR_PALETTE = {
    # Primary Brand Colors
    'primary': '#667eea',           # Main brand purple-blue
    'primary_dark': '#764ba2',      # Dark purple accent
    'primary_light': '#8b9aee',     # Light purple-blue
    
    # Semantic Colors (Status & Actions)
    'success': '#4CAF50',           # Green for success/positive
    'success_light': '#81C784',     # Light green
    'success_dark': '#388E3C',      # Dark green
    
    'warning': '#FF9800',           # Orange for warnings
    'warning_light': '#FFB74D',     # Light orange
    'warning_dark': '#F57C00',      # Dark orange
    
    'danger': '#F44336',            # Red for errors/failures
    'danger_light': '#E57373',      # Light red
    'danger_dark': '#D32F2F',       # Dark red
    
    'info': '#2196F3',              # Blue for information
    'info_light': '#64B5F6',        # Light blue
    'info_dark': '#1976D2',         # Dark blue
    
    # Neutral Colors (Text & Backgrounds)
    'text_primary': '#2c3e50',      # Main text color
    'text_secondary': '#5a6c7d',    # Secondary text
    'text_muted': '#95a5a6',        # Muted/helper text
    
    'bg_white': '#ffffff',          # Pure white
    'bg_light': '#f8f9fa',          # Light gray background
    'bg_lighter': '#f8fbff',        # Very light background
    'bg_card': '#ffffff',           # Card background
    
    'border_light': '#e9ecef',      # Light border
    'border_medium': '#dee2e6',     # Medium border
    
    # Chart Colors (Diverse palette for data visualization)
    'chart_1': '#667eea',           # Primary purple-blue
    'chart_2': '#764ba2',           # Dark purple
    'chart_3': '#4CAF50',           # Green
    'chart_4': '#2196F3',           # Blue
    'chart_5': '#FF5722',           # Deep orange
    'chart_6': '#9C27B0',           # Purple
    'chart_7': '#FF9800',           # Orange
    'chart_8': '#00BCD4',           # Cyan
    'chart_9': '#4facfe',           # Light blue
    'chart_10': '#43e97b',          # Mint green
    'chart_11': '#f5576c',          # Coral red
    'chart_12': '#ffecd2',          # Peach
    
    # RAG Status Colors (for tables)
    'rag_green_bg': '#d4edda',
    'rag_green_text': '#155724',
    'rag_amber_bg': '#fff3cd',
    'rag_amber_text': '#856404',
    'rag_red_bg': '#f8d7da',
    'rag_red_text': '#721c24',
    
    # Shadow Colors (RGBA)
    'shadow_light': 'rgba(102, 126, 234, 0.12)',
    'shadow_medium': 'rgba(102, 126, 234, 0.25)',
    'shadow_dark': 'rgba(0, 0, 0, 0.15)',
}

# Chart color array for easy access
CHART_COLORS = [
    COLOR_PALETTE[f'chart_{i}'] for i in range(1, 13)
]

# =============================================================================
# MODERN UI/UX CONFIGURATION
# =============================================================================

# Configure Streamlit page
st.set_page_config(
    page_title="BNT113 Clinical Trial Dashboard",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.streamlit.io/community',
        'Report a bug': None,
        'About': "BNT113 Clinical Trial Progress Dashboard - Advanced Analytics & Reporting"
    }
)

# Modern CSS Styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styling */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Modern Header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 2rem 1.5rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        color: white;
        text-align: center;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-subtitle {
        font-size: 1.1rem;
        font-weight: 400;
        opacity: 0.9;
        margin-bottom: 1rem;
    }
    
    .header-stats {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 1rem;
    }
    
    .header-stat {
        text-align: center;
        background: rgba(255,255,255,0.1);
        padding: 0.8rem 1.2rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    .header-stat-value {
        font-size: 1.5rem;
        font-weight: 600;
        display: block;
    }
    
    .header-stat-label {
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    /* Modern Metric Cards - Enhanced */
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem 1.8rem;
        border-radius: 20px;
        box-shadow: 
            0 10px 30px rgba(102, 126, 234, 0.12),
            0 1px 3px rgba(0, 0, 0, 0.08),
            inset 0 1px 0 rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(102, 126, 234, 0.08);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 20px 45px rgba(102, 126, 234, 0.25),
            0 5px 15px rgba(0, 0, 0, 0.12),
            inset 0 1px 0 rgba(255, 255, 255, 1);
        border-color: rgba(102, 126, 234, 0.2);
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    .metric-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover .metric-icon {
        transform: scale(1.1) rotateZ(5deg);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #2c3e50;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
        line-height: 1.2;
        transition: color 0.3s ease;
    }
    
    .metric-card:hover .metric-value {
        color: #667eea;
    }
    
    .metric-label {
        font-size: 1.05rem;
        color: #5a6c7d;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.3rem;
    }
    
    /* Animated entrance for metric cards */
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    .metric-card.fade-in {
        animation: slideInUp 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
        color: white;
    }
    
    /* Admin Panel Styling */
    .admin-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #007bff;
        margin-bottom: 1rem;
    }
    
    .admin-title {
        color: #007bff;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }
    
    /* Chart Container */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
        border: 1px solid #e9ecef;
    }
    
    /* Table Styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Modern Section Headers */
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin: 3rem 0 2rem 0;
        font-weight: 700;
        font-size: 1.5rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        letter-spacing: 0.5px;
    }
    
    /* Modern Section Dividers */
    .section-divider {
        margin: 60px 0;
        text-align: center;
        position: relative;
    }
    
    .section-divider::before {
        content: '';
        display: block;
        height: 2px;
        background: linear-gradient(90deg, transparent, #e0e0e0, transparent);
        margin-bottom: 20px;
    }
    
    .section-divider-icon {
        display: inline-block;
        background: white;
        padding: 15px;
        border-radius: 50%;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        color: #667eea;
        font-size: 1.5rem;
    }
    
    .section-divider::after {
        content: '';
        display: block;
        height: 2px;
        background: linear-gradient(90deg, transparent, #e0e0e0, transparent);
        margin-top: 20px;
    }
    
    /* Status Indicators */
    .status-green {
        background: #d4edda;
        color: #155724;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    .status-amber {
        background: #fff3cd;
        color: #856404;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    .status-red {
        background: #f8d7da;
        color: #721c24;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    /* Animation */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .header-stats {
            flex-direction: column;
            gap: 1rem;
        }
        
        .metric-card {
            padding: 1.2rem;
            margin-bottom: 1rem;
            border-radius: 15px;
        }
        
        .metric-icon {
            font-size: 2.2rem;
        }
        
        .metric-value {
            font-size: 1.8rem;
        }
        
        .metric-label {
            font-size: 0.9rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# MODERN CHART THEMES & UTILITIES
# =============================================================================

def apply_modern_chart_theme(fig, title=None, height=500):
    """Apply modern, professional styling to plotly charts with enhanced interactivity"""
    
    fig.update_layout(
        # Modern transparent background
        plot_bgcolor=f'rgba(248, 251, 255, 0.5)',
        paper_bgcolor='rgba(0,0,0,0)',
        
        # Enhanced typography
        font=dict(
            family="Inter, -apple-system, BlinkMacSystemFont, sans-serif",
            size=13,
            color=COLOR_PALETTE['text_primary']
        ),
        
        # Professional title styling
        title=dict(
            text=title,
            font=dict(
                size=20, 
                color=COLOR_PALETTE['text_primary'], 
                family="Inter",
                weight=600
            ),
            x=0.5,
            xanchor='center',
            y=0.98,
            yanchor='top',
            pad=dict(b=20)
        ) if title else None,
        
        # Modern grid and axes
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(102, 126, 234, 0.1)',
            showline=True,
            linewidth=2,
            linecolor=COLOR_PALETTE['shadow_dark'],
            tickfont=dict(color=COLOR_PALETTE['text_secondary'], size=12),
            title_font=dict(size=14, color=COLOR_PALETTE['text_primary'])
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(102, 126, 234, 0.1)',
            showline=True,
            linewidth=2,
            linecolor=COLOR_PALETTE['shadow_dark'],
            tickfont=dict(color=COLOR_PALETTE['text_secondary'], size=12),
            title_font=dict(size=14, color=COLOR_PALETTE['text_primary'])
        ),
        
        # Enhanced legend
        legend=dict(
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="rgba(102, 126, 234, 0.2)",
            borderwidth=2,
            font=dict(color=COLOR_PALETTE['text_primary'], size=12),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        
        # Margins and sizing
        margin=dict(l=70, r=70, t=100, b=70),
        height=height,
        
        # Enhanced hover effects
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Inter",
            bordercolor="rgba(102, 126, 234, 0.3)",
            font=dict(color=COLOR_PALETTE['text_primary'])
        ),
        
        # Interactivity
        hovermode='x unified',
        
        # Modern animation
        transition={'duration': 500, 'easing': 'cubic-in-out'}
    )
    
    # Update traces with modern colors and effects
    if hasattr(fig, 'data'):
        for i, trace in enumerate(fig.data):
            # Apply colors from unified palette
            color = CHART_COLORS[i % len(CHART_COLORS)]
            
            if hasattr(trace, 'marker'):
                trace.marker.update(
                    color=color,
                    line=dict(width=0.5, color='white')
                )
            
            if hasattr(trace, 'line'):
                trace.line.update(
                    color=color,
                    width=3
                )
    
    # Add subtle shadow effect via shapes
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(102, 126, 234, 0.08)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(102, 126, 234, 0.08)')
    
    return fig

def create_chart_container(chart_fig, title=None):
    """Wrap charts in modern containers"""
    st.markdown(f"""
    <div class="chart-container fade-in">
        {f'<h3 style="margin-bottom: 1rem; color: #2c3e50;">{title}</h3>' if title else ''}
    """, unsafe_allow_html=True)
    
    st.plotly_chart(chart_fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def create_enhanced_metric_card(icon, label, value, subtitle="", color=None):
    """Create an enhanced metric card with modern styling using container approach"""
    if color is None:
        color = COLOR_PALETTE['primary']
    
    # Create a container with custom styling
    with st.container():
        st.markdown(f"""
        <div style="
            background: linear-gradient(145deg, {COLOR_PALETTE['bg_white']} 0%, {COLOR_PALETTE['bg_light']} 100%);
            padding: 2rem 1.5rem;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.1), 0 2px 6px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(102, 126, 234, 0.08);
            border-top: 3px solid {color};
            text-align: center;
            margin-bottom: 1rem;
            min-height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">{icon}</div>
            <div style="font-size: 2.2rem; font-weight: 700; color: {COLOR_PALETTE['text_primary']}; margin-bottom: 0.5rem; letter-spacing: -0.5px;">{value}</div>
            <div style="font-size: 0.9rem; color: {COLOR_PALETTE['text_secondary']}; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 0.5rem;">{label}</div>
            <div style="font-size: 0.8rem; color: {COLOR_PALETTE['text_muted']};">{subtitle}</div>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# P0 PRIORITY: SCHEMA-DRIVEN KPI ENGINE
# =============================================================================

# KPI Configuration (Embedded for P0 Implementation)
KPI_CONFIG = {
    'metadata': {
        'version': '1.0.0',
        'description': 'BNT113 Clinical Trial KPI Definitions',
        'last_updated': '2025-06-09'
    },
    'kpis': {
        'total_referred': {
            'name': 'Total Referred',
            'description': 'Individual patients referred',
            'calculation': {'type': 'derived_column_sum', 'column': 'is_referred', 'fallback_value': 0},
            'display': {'icon': '👥', 'color': COLOR_PALETTE['info'], 'subtitle': 'Individual patients referred'},
            'targets': {'default': 50}
        },
        'referred_to_prescreen': {
            'name': 'Referred to Pre-screen',
            'description': 'Patients referred to pre-screening',
            'calculation': {'type': 'derived_column_sum', 'column': 'is_referred_to_prescreen', 'fallback_value': 0},
            'display': {'icon': '🔍', 'color': COLOR_PALETTE['chart_6'], 'subtitle': 'Patients referred to pre-screening'},
            'targets': {'default': 40}
        },
        'referred_to_main_trial': {
            'name': 'Referred to Main Trial',
            'description': 'Patients referred to main trial screening',
            'calculation': {'type': 'derived_column_sum', 'column': 'is_referred_to_main_trial', 'fallback_value': 0},
            'display': {'icon': '🎯', 'color': COLOR_PALETTE['warning'], 'subtitle': 'Patients referred to main trial screening'},
            'targets': {'default': 30}
        },
        'recruited_to_cvlp': {
            'name': 'Recruited to CVLP',
            'description': 'CVLP consented patients',
            'calculation': {'type': 'derived_column_sum', 'column': 'is_recruited_to_cvlp', 'fallback_value': 0},
            'display': {'icon': '✅', 'color': COLOR_PALETTE['success'], 'subtitle': 'CVLP consented patients'},
            'targets': {'default': 25}
        },
        'consented_prescreen': {
            'name': 'Consented BNT113-01',
            'description': 'Pre-screening consented patients',
            'calculation': {'type': 'derived_column_sum', 'column': 'is_consented_prescreen', 'fallback_value': 0},
            'display': {'icon': '📝', 'color': COLOR_PALETTE['chart_8'], 'subtitle': 'Pre-screening consented'},
            'targets': {'default': 20}
        },
        'randomised': {
            'name': 'Randomised BNT113-01',
            'description': 'Patients randomised to BNT113-01 trial',
            'calculation': {'type': 'derived_column_sum', 'column': 'is_randomised', 'fallback_value': 0},
            'display': {'icon': '🎲', 'color': COLOR_PALETTE['chart_9'], 'subtitle': 'Randomised to BNT113-01'},
            'targets': {'default': 15}
        },
        'screen_failures': {
            'name': 'Screen Failures',
            'description': 'BNT113-01 screen failures',
            'calculation': {'type': 'derived_column_sum', 'column': 'is_screen_failure', 'fallback_value': 0},
            'display': {'icon': '⚠️', 'color': COLOR_PALETTE['danger'], 'subtitle': 'BNT113-01 screen failures', 'border_color': COLOR_PALETTE['danger']},
            'targets': {'default': 8}
        }
    },
    'dashboard_layout': {
        'title': '📊 BNT113 Trial Metrics Overview (Schema-Driven)',
        'sections': {
            'primary_metrics': {
                'kpis': ['total_referred', 'referred_to_prescreen', 'referred_to_main_trial', 'recruited_to_cvlp'],
                'layout': '4_columns'
            },
            'secondary_metrics': {
                'kpis': ['consented_prescreen', 'randomised', 'screen_failures'],
                'layout': '3_columns_centered'
            }
        }
    }
}

class SchemaKPIEngine:
    """P0 Priority: Schema-driven KPI Engine for clinical trial dashboards"""
    
    def __init__(self):
        self.config = KPI_CONFIG
        self.kpis = self.config.get('kpis', {})
        self.targets = {}
        
        # Load default targets
        for kpi_id, kpi_config in self.kpis.items():
            self.targets[kpi_id] = kpi_config.get('targets', {}).get('default', 0)
    
    def calculate_kpis(self, df):
        """Calculate all KPIs from DataFrame using schema configuration"""
        results = {}
        
        for kpi_id, kpi_config in self.kpis.items():
            try:
                calculation = kpi_config.get('calculation', {})
                column = calculation.get('column')
                fallback = calculation.get('fallback_value', 0)
                
                if column in df.columns:
                    value = int(df[column].sum())
                else:
                    value = fallback
                
                results[kpi_id] = {
                    'value': value,
                    'config': kpi_config,
                    'target': self.targets.get(kpi_id, 0),
                    'achievement': self._calculate_achievement(value, self.targets.get(kpi_id, 0))
                }
                
            except Exception as e:
                results[kpi_id] = {
                    'value': 0,
                    'config': kpi_config,
                    'target': 0,
                    'achievement': 0,
                    'error': str(e)
                }
        
        return results
    
    def _calculate_achievement(self, actual, target):
        """Calculate achievement percentage against target"""
        if target <= 0:
            return 100.0 if actual > 0 else 0.0
        return min((actual / target) * 100, 200.0)
    
    def render_schema_driven_metrics_tiles(self, df):
        """Render KPI metrics tiles using schema configuration"""
        if df.empty:
            st.warning("No data available to create metrics")
            return
        
        # Calculate KPIs using schema
        kpi_results = self.calculate_kpis(df)
        
        # Get layout configuration
        layout_config = self.config.get('dashboard_layout', {})
        title = layout_config.get('title', '📊 KPI Dashboard')
        
        st.markdown(f"<h2 style='text-align: center; margin-bottom: 30px;'>{title}</h2>", 
                   unsafe_allow_html=True)
        
        # Add schema-driven badge
        st.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <span style='background: linear-gradient(90deg, #4CAF50, #2196F3); color: white; padding: 8px 16px; border-radius: 20px; font-size: 12px; font-weight: 600;'>
                ✨ SCHEMA-DRIVEN BI ✨ No Code Changes Required for KPI Updates
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Render sections
        sections = layout_config.get('sections', {})
        
        for section_id, section_config in sections.items():
            section_kpis = section_config.get('kpis', [])
            layout_type = section_config.get('layout', '4_columns')
            
            if layout_type == '4_columns':
                cols = st.columns(4)
            elif layout_type == '3_columns_centered':
                cols = st.columns([1, 2, 2, 2, 1])
                cols = [cols[1], cols[2], cols[3]]
            else:
                cols = st.columns(len(section_kpis))
            
            for i, kpi_id in enumerate(section_kpis):
                if i < len(cols) and kpi_id in kpi_results:
                    with cols[i]:
                        self._render_kpi_tile(kpi_id, kpi_results[kpi_id])
            
            st.markdown("<br>", unsafe_allow_html=True)
    
    def _render_kpi_tile(self, kpi_id, kpi_data):
        """Render a single KPI tile using schema configuration"""
        config = kpi_data['config']
        display_config = config.get('display', {})
        
        name = config.get('name', kpi_id)
        value = kpi_data['value']
        target = kpi_data['target']
        achievement = kpi_data['achievement']
        subtitle = display_config.get('subtitle', '')
        icon = display_config.get('icon', '📊')
        color = display_config.get('color', '#3949AB')
        border_color = display_config.get('border_color', '')
        
        formatted_value = f"{int(value):,}"
        border_style = f"border-left: 4px solid {border_color};" if border_color else ""
        
        # Add achievement indicator using unified colors
        achievement_color = COLOR_PALETTE['success'] if achievement >= 80 else COLOR_PALETTE['warning'] if achievement >= 50 else COLOR_PALETTE['danger']
        achievement_text = f"🎯 {achievement:.0f}% of target" if target > 0 else ""
        
        tile_html = f"""
        <div class="metric-card" style="{border_style}">
            <div class="metric-label">{icon} {name}</div>
            <div class="big-metric" style="color: {color} !important;">{formatted_value}</div>
            <div style="font-size: 12px; color: #666; margin-top: 5px;">{subtitle}</div>
            {f'<div style="font-size: 11px; color: {achievement_color}; margin-top: 3px; font-weight: 600;">{achievement_text}</div>' if achievement_text else ''}
        </div>
        """
        
        st.markdown(tile_html, unsafe_allow_html=True)
    
    def render_target_configuration_ui(self):
        """Render schema-driven target configuration UI in sidebar"""
        with st.sidebar.expander("🎯 Schema-Driven KPI Targets"):
            st.markdown("### Configure KPI Targets")
            st.markdown("*✨ Business users can modify targets without code changes*")
            
            new_targets = {}
            
            for kpi_id, kpi_config in self.kpis.items():
                kpi_name = kpi_config.get('name', kpi_id)
                current_target = self.targets.get(kpi_id, 0)
                
                new_target = st.number_input(
                    f"{kpi_name}",
                    min_value=0,
                    value=int(current_target),
                    step=1,
                    key=f"schema_target_{kpi_id}",
                    help=f"Default: {kpi_config.get('targets', {}).get('default', 0)}"
                )
                
                new_targets[kpi_id] = new_target
            
            if st.button("💾 Update Schema Targets", key="update_schema_targets"):
                # Update targets in memory (schema-driven approach)
                for kpi_id, target_value in new_targets.items():
                    self.targets[kpi_id] = float(target_value)
                
                st.success("✅ Schema targets updated successfully!")
                st.info("💡 Changes applied immediately - No code deployment needed")
    
    def render_schema_info(self):
        """Render schema-driven BI information panel"""
        with st.sidebar.expander("⚙️ Schema-Driven BI Features"):
            metadata = self.config.get('metadata', {})
            
            st.markdown("**Configuration Details:**")
            st.text(f"Version: {metadata.get('version', '1.0.0')}")
            st.text(f"KPIs Defined: {len(self.kpis)}")
            st.text(f"Last Updated: {metadata.get('last_updated', 'Unknown')}")
            
            st.markdown("**✨ Schema-Driven Benefits:**")
            st.markdown("• ✅ **Zero Code Changes** for KPI updates")
            st.markdown("• ✅ **Business User Configurable** targets")
            st.markdown("• ✅ **Version Controlled** schemas")
            st.markdown("• ✅ **Dynamic Layout** management")
            st.markdown("• ✅ **Real-time Target** adjustments")
            st.markdown("• ✅ **Consistent Styling** across metrics")
            
            st.markdown("**🚀 P0 Implementation:**")
            st.markdown("• Configuration-driven KPI engine")
            st.markdown("• Business logic externalized to config")
            st.markdown("• Maintainable and scalable architecture")

# Initialize Schema-Driven KPI Engine
schema_kpi_engine = SchemaKPIEngine()

# =============================================================================
# END OF SCHEMA-DRIVEN KPI ENGINE
# =============================================================================

# P0 PRIORITY: Import schema validation module
try:
    from schema_validation import (
        validate_master_tracker_data, 
        generate_data_quality_report, 
        display_quality_metrics
    )
    SCHEMA_VALIDATION_AVAILABLE = True
except ImportError:
    # Schema validation is optional - silently disable if not available
    SCHEMA_VALIDATION_AVAILABLE = False

# Add logo integration functions
def get_base64_encoded_image(image_path):
    """Convert image to base64 string for CSS embedding"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# Get base64 encoded logo
logo_base64 = get_base64_encoded_image("assets/SCTU Logo (mediabin resized).jpg")

# Custom CSS for enhanced visual design with logo integration
st.markdown(f"""
<style>
    /* Modern Typography */
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    /* Logo watermark background */
    .main .block-container {{
        background-image: url("data:image/jpeg;base64,{logo_base64}");
        background-repeat: no-repeat;
        background-position: center center;
        background-size: 400px;
        background-attachment: fixed;
        background-opacity: 0.03;
        position: relative;
    }}
    
    .main .block-container::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(255, 255, 255, 0.97);
        z-index: -1;
    }}
    
    /* Sidebar logo styling */
    .sidebar-logo {{
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px 10px;
        margin-bottom: 20px;
        background: linear-gradient(135deg, #f8f9ff 0%, #e8eaf6 100%);
        border-radius: 12px;
        border: 2px solid #e1e5fe;
    }}
    
    /* Better Headers */
    h1 {{
        font-weight: 700 !important;
        color: #1A237E !important;
        padding-bottom: 10px;
        border-bottom: 2px solid #E8EAF6;
    }}
    h2 {{
        font-weight: 600 !important;
        color: #283593 !important;
    }}
    h3 {{
        font-weight: 500 !important;
        color: #3949AB !important;
    }}
    
    /* Enhanced Metric Display for Schema-Driven Tiles */
    .big-metric {{
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        color: #2c3e50 !important;
        letter-spacing: -0.5px !important;
        line-height: 1.2 !important;
        transition: all 0.3s ease !important;
        display: block !important;
        margin: 0.5rem 0 !important;
    }}
    
    .metric-card:hover .big-metric {{
        color: #667eea !important;
        transform: scale(1.05);
    }}
    
    .metric-label {{
        font-size: 0.95rem;
        color: #5a6c7d;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }}
    
    /* Mobile Optimization */
    @media (max-width: 768px) {{
        .big-metric {{
            font-size: 2rem !important;
        }}
        .metric-card {{
            padding: 1.2rem;
            margin-bottom: 1rem;
        }}
        .metric-icon {{
            font-size: 2.2rem;
        }}
        .metric-value {{
            font-size: 1.8rem;
        }}
    }}
    
    /* Table styling */
    .styled-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 0.9em;
        font-family: 'Inter', sans-serif;
        min-width: 400px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        border-radius: 8px;
        overflow: hidden;
    }}
    .styled-table thead tr {{
        background-color: #3949AB;
        color: #ffffff;
        text-align: left;
    }}
    .styled-table th,
    .styled-table td {{
        padding: 12px 15px;
    }}
    .styled-table tbody tr {{
        border-bottom: 1px solid #dddddd;
    }}
    .styled-table tbody tr:nth-of-type(even) {{
        background-color: #f3f3f3;
    }}
    .styled-table tbody tr:last-of-type {{
        border-bottom: 2px solid #3949AB;
    }}
</style>
""", unsafe_allow_html=True)

# Define a professional, clinical color palette
clinical_colors = {
    'primary': ['#E8EAF6', '#C5CAE9', '#9FA8DA', '#7986CB', '#5C6BC0', '#3F51B5', '#3949AB', '#303F9F', '#283593', '#1A237E'],
    'secondary': ['#E1F5FE', '#B3E5FC', '#81D4FA', '#4FC3F7', '#29B6F6', '#03A9F4', '#039BE5', '#0288D1', '#0277BD', '#01579B'],
    'success': ['#E8F5E9', '#C8E6C9', '#A5D6A7', '#81C784', '#66BB6A', '#4CAF50', '#43A047', '#388E3C', '#2E7D32', '#1B5E20'],
    'warning': ['#FFF8E1', '#FFECB3', '#FFE082', '#FFD54F', '#FFCA28', '#FFC107', '#FFB300', '#FFA000', '#FF8F00', '#FF6F00'],
    'danger': ['#FFEBEE', '#FFCDD2', '#EF9A9A', '#E57373', '#EF5350', '#F44336', '#E53935', '#D32F2F', '#C62828', '#B71C1C'],
    'neutral': ['#FAFAFA', '#F5F5F5', '#EEEEEE', '#E0E0E0', '#BDBDBD', '#9E9E9E', '#757575', '#616161', '#424242', '#212121']
}

# =====================================
# SIDEBAR CONTROLS - CLEAN & ORGANIZED  
# =====================================

# =============================================================================
# MODERN DASHBOARD HEADER
# =============================================================================

# Add modern header to main content
st.markdown("""
<div class="main-header fade-in">
    <div class="main-title">🧬 BNT113 Clinical Trial Dashboard</div>
    <div class="main-subtitle">Advanced Analytics & Progress Monitoring System</div>
    <div class="header-stats">
        <div class="header-stat">
            <span class="header-stat-value">Real-time</span>
            <span class="header-stat-label">Data Updates</span>
        </div>
        <div class="header-stat">
            <span class="header-stat-value">Multi-site</span>
            <span class="header-stat-label">Tracking</span>
        </div>
        <div class="header-stat">
            <span class="header-stat-value">GDPR</span>
            <span class="header-stat-label">Compliant</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# MODERN SIDEBAR DESIGN
# =============================================================================

# Sidebar header
st.sidebar.markdown("""
<div class="sidebar-header">
    <h2 style="margin: 0; font-size: 1.3rem;">⚙️ Dashboard Controls</h2>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">Configure your view</p>
</div>
""", unsafe_allow_html=True)

# === MAIN CONTROLS ===
st.sidebar.header("📊 Data Controls")

# File upload
uploaded_master_file = st.sidebar.file_uploader(
    "📁 Upload Master Tracker", 
    type=["xlsx"],
    help="Upload your BNT113-01 Master Tracker Excel file"
)

# Screening Logs file upload
uploaded_screening_logs_file = st.sidebar.file_uploader(
    "📋 Upload Screening Logs", 
    type=["xlsx"],
    help="Upload your BNT113-01 Screening Logs Excel file"
)

# Privacy controls
st.sidebar.subheader("🔒 Privacy Mode")
privacy_mode = st.sidebar.radio(
    "Select privacy level:",
    ["Pseudonymized (Safe)", "Full Data (Admin)"],
    index=0,
    help="Pseudonymized mode protects patient data while maintaining accurate metrics"
)

# === TRIAL PROGRESS REPORTS ===
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Trial Progress Reports")

if st.sidebar.button("🏆 Achievements & Barriers", type="secondary", use_container_width=True):
    st.session_state.show_achievements = True

if st.sidebar.button("🏥 CPGC and Trial Site Set Up", type="secondary", use_container_width=True):
    st.session_state.show_cpgc_trial_setup = True

if st.sidebar.button("📊 CPGC BNT Reporting", type="secondary", use_container_width=True):
    st.session_state.show_cpgc_reporting = True

# === ADMIN PANEL ===
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class="admin-section">
    <div class="admin-title">⚙️ Admin Panel</div>
    <p style="margin: 0; font-size: 0.9rem; color: #6c757d;">Toggle sections for external sharing</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state for admin controls
if 'admin_settings' not in st.session_state:
    st.session_state.admin_settings = {
        # Core Metrics & Overview
        'show_key_metrics': True,
        'show_referral_performance': True,
        
        # Monthly Analysis
        'show_monthly_table': True,
        'show_monthly_charts': True,
        'show_monthly_trends': True,
        
        # Site Analysis
        'show_site_performance': True,
        'show_site_metrics_table': True,
        'show_site_visualizations': True,
        'show_cvlp_site_breakdown': True,
        
        # Referral Analysis
        'show_trial_referral_reporting': True,
        'show_referral_visualizations': True,
        'show_referral_breakdown': True,
        
        # Advanced Analytics
        'show_statistical_control': True,
        'show_performance_radar': True,
        'show_combined_analysis': True,
        
        # Technical & Debug
        'show_debug_info': True,
        'show_data_quality': True,
        'show_column_detection': True
    }

# Initialize session state for achievements tab
if 'show_achievements' not in st.session_state:
    st.session_state.show_achievements = False

# Initialize session state for CPGC and Trial Site Set Up tab
if 'show_cpgc_trial_setup' not in st.session_state:
    st.session_state.show_cpgc_trial_setup = False

# Initialize session state for CPGC BNT Reporting tab
if 'show_cpgc_reporting' not in st.session_state:
    st.session_state.show_cpgc_reporting = False

# Initialize session state for privacy mode
if 'privacy_mode' not in st.session_state:
    st.session_state.privacy_mode = False

# Privacy Mode Toggle
st.sidebar.markdown("**🔒 Privacy Controls:**")
privacy_col1, privacy_col2 = st.sidebar.columns([1, 4])
with privacy_col1:
    st.session_state.privacy_mode = st.checkbox("Privacy Mode", value=st.session_state.privacy_mode, key="toggle_privacy", label_visibility="collapsed")
with privacy_col2:
    st.markdown("Hide sensitive metrics from external parties")

st.sidebar.markdown("---")

# Admin toggles with descriptions - organized by category
st.sidebar.markdown("**📊 Core Sections:**")
admin_col1, admin_col2 = st.sidebar.columns([1, 4])

with admin_col1:
    st.session_state.admin_settings['show_key_metrics'] = st.checkbox("Key Metrics Cards", value=st.session_state.admin_settings['show_key_metrics'], key="toggle_metrics", label_visibility="collapsed")
with admin_col2:
    st.markdown("Key Metrics Cards")

with admin_col1:
    st.session_state.admin_settings['show_referral_performance'] = st.checkbox("Referral Performance", value=st.session_state.admin_settings['show_referral_performance'], key="toggle_referral_perf", label_visibility="collapsed")
with admin_col2:
    st.markdown("Referral Performance vs Targets")

st.sidebar.markdown("**📅 Monthly Analysis:**")
with admin_col1:
    st.session_state.admin_settings['show_monthly_table'] = st.checkbox("Monthly Table", value=st.session_state.admin_settings['show_monthly_table'], key="toggle_monthly", label_visibility="collapsed")
with admin_col2:
    st.markdown("Monthly Metrics Table")

with admin_col1:
    st.session_state.admin_settings['show_monthly_charts'] = st.checkbox("Monthly Charts", value=st.session_state.admin_settings['show_monthly_charts'], key="toggle_monthly_charts", label_visibility="collapsed")
with admin_col2:
    st.markdown("Monthly Charts & Projections")

with admin_col1:
    st.session_state.admin_settings['show_monthly_trends'] = st.checkbox("Monthly Trends", value=st.session_state.admin_settings['show_monthly_trends'], key="toggle_monthly_trends", label_visibility="collapsed")
with admin_col2:
    st.markdown("Monthly Trends Visualization")

st.sidebar.markdown("**🏥 Site Analysis:**")
with admin_col1:
    st.session_state.admin_settings['show_site_performance'] = st.checkbox("Site Performance", value=st.session_state.admin_settings['show_site_performance'], key="toggle_site", label_visibility="collapsed")
with admin_col2:
    st.markdown("CVLP Site Performance")

with admin_col1:
    st.session_state.admin_settings['show_site_metrics_table'] = st.checkbox("Site Metrics Table", value=st.session_state.admin_settings['show_site_metrics_table'], key="toggle_site_table", label_visibility="collapsed")
with admin_col2:
    st.markdown("Site Metrics Table")

with admin_col1:
    st.session_state.admin_settings['show_site_visualizations'] = st.checkbox("Site Visualizations", value=st.session_state.admin_settings['show_site_visualizations'], key="toggle_site_viz", label_visibility="collapsed")
with admin_col2:
    st.markdown("Site Visualizations")

with admin_col1:
    st.session_state.admin_settings['show_cvlp_site_breakdown'] = st.checkbox("CVLP Breakdown", value=st.session_state.admin_settings['show_cvlp_site_breakdown'], key="toggle_cvlp_breakdown", label_visibility="collapsed")
with admin_col2:
    st.markdown("CVLP Site Breakdown")

st.sidebar.markdown("**📋 Referral Analysis:**")
with admin_col1:
    st.session_state.admin_settings['show_trial_referral_reporting'] = st.checkbox("Trial Referral Reporting", value=st.session_state.admin_settings['show_trial_referral_reporting'], key="toggle_trial_ref", label_visibility="collapsed")
with admin_col2:
    st.markdown("Trial Referral Reporting")

with admin_col1:
    st.session_state.admin_settings['show_referral_visualizations'] = st.checkbox("Referral Visualizations", value=st.session_state.admin_settings['show_referral_visualizations'], key="toggle_ref_viz", label_visibility="collapsed")
with admin_col2:
    st.markdown("Referral Visualizations")

with admin_col1:
    st.session_state.admin_settings['show_referral_breakdown'] = st.checkbox("Referral Breakdown", value=st.session_state.admin_settings['show_referral_breakdown'], key="toggle_ref_breakdown", label_visibility="collapsed")
with admin_col2:
    st.markdown("Referral Metrics Breakdown")

st.sidebar.markdown("**📈 Advanced Analytics:**")
with admin_col1:
    st.session_state.admin_settings['show_statistical_control'] = st.checkbox("Statistical Control", value=st.session_state.admin_settings['show_statistical_control'], key="toggle_stats", label_visibility="collapsed")
with admin_col2:
    st.markdown("Statistical Control Charts")

with admin_col1:
    st.session_state.admin_settings['show_performance_radar'] = st.checkbox("Performance Radar", value=st.session_state.admin_settings['show_performance_radar'], key="toggle_radar", label_visibility="collapsed")
with admin_col2:
    st.markdown("Performance Radar Charts")

with admin_col1:
    st.session_state.admin_settings['show_combined_analysis'] = st.checkbox("Combined Analysis", value=st.session_state.admin_settings['show_combined_analysis'], key="toggle_combined", label_visibility="collapsed")
with admin_col2:
    st.markdown("Combined Analysis")

st.sidebar.markdown("**🔧 Technical:**")
with admin_col1:
    st.session_state.admin_settings['show_debug_info'] = st.checkbox("Debug Info", value=st.session_state.admin_settings['show_debug_info'], key="toggle_debug", label_visibility="collapsed")
with admin_col2:
    st.markdown("Debug Information")

with admin_col1:
    st.session_state.admin_settings['show_data_quality'] = st.checkbox("Data Quality", value=st.session_state.admin_settings['show_data_quality'], key="toggle_quality", label_visibility="collapsed")
with admin_col2:
    st.markdown("Data Quality Checks")

with admin_col1:
    st.session_state.admin_settings['show_column_detection'] = st.checkbox("Column Detection", value=st.session_state.admin_settings['show_column_detection'], key="toggle_columns", label_visibility="collapsed")
with admin_col2:
    st.markdown("Column Detection Debug")

# Quick preset buttons
st.sidebar.markdown("**Quick Presets:**")
preset_col1, preset_col2 = st.sidebar.columns(2)

with preset_col1:
    if st.button("👥 External", help="Hide sensitive sections for external sharing"):
        st.session_state.admin_settings.update({
            # Core Sections - Show key metrics only, hide referral performance
            'show_key_metrics': True,
            'show_referral_performance': False,  # HIDDEN for external
            
            # Monthly Analysis - Show basic table only, hide trends
            'show_monthly_table': True,
            'show_monthly_charts': False,
            'show_monthly_trends': False,  # HIDDEN for external
            
            # Site Analysis - Hide performance and visualizations
            'show_site_performance': True,
            'show_site_metrics_table': False,
            'show_site_visualizations': False,  # HIDDEN for external
            'show_cvlp_site_breakdown': False,
            
            # Referral Analysis - Hide all detailed breakdowns
            'show_trial_referral_reporting': False,
            'show_referral_visualizations': False,
            'show_referral_breakdown': False,  # HIDDEN for external
            
            # Advanced Analytics - Hide all including combined analysis
            'show_statistical_control': False,
            'show_performance_radar': False,
            'show_combined_analysis': False,  # HIDDEN for external
            
            # Technical - Hide all
            'show_debug_info': False,
            'show_data_quality': False,
            'show_column_detection': False
        })
        st.rerun()

with preset_col2:
    if st.button("🔓 Full", help="Show all sections for internal use"):
        st.session_state.admin_settings.update({
            # Core Sections
            'show_key_metrics': True,
            'show_referral_performance': True,
            
            # Monthly Analysis
            'show_monthly_table': True,
            'show_monthly_charts': True,
            'show_monthly_trends': True,
            
            # Site Analysis
            'show_site_performance': True,
            'show_site_metrics_table': True,
            'show_site_visualizations': True,
            'show_cvlp_site_breakdown': True,
            
            # Referral Analysis
            'show_trial_referral_reporting': True,
            'show_referral_visualizations': True,
            'show_referral_breakdown': True,
            
            # Advanced Analytics
            'show_statistical_control': True,
            'show_performance_radar': True,
            'show_combined_analysis': True,
            
            # Technical
            'show_debug_info': True,
            'show_data_quality': True,
            'show_column_detection': True
        })
        st.rerun()

# Admin status indicator
admin_active_count = sum(st.session_state.admin_settings.values())
admin_total_count = len(st.session_state.admin_settings)
st.sidebar.markdown(f"**Status:** {admin_active_count}/{admin_total_count} sections active")

# Export/Import Settings
st.sidebar.markdown("**Settings:**")
settings_col1, settings_col2 = st.sidebar.columns(2)

with settings_col1:
    if st.button("📥 Export", help="Copy settings to clipboard"):
        import json
        settings_json = json.dumps(st.session_state.admin_settings, indent=2)
        st.sidebar.code(settings_json, language="json")

with settings_col2:
    if st.button("📤 Reset", help="Reset to default settings"):
        st.session_state.admin_settings = {
            # Core Metrics & Overview
            'show_key_metrics': True,
            'show_referral_performance': True,
            
            # Monthly Analysis
            'show_monthly_table': True,
            'show_monthly_charts': True,
            'show_monthly_trends': True,
            
            # Site Analysis
            'show_site_performance': True,
            'show_site_metrics_table': True,
            'show_site_visualizations': True,
            'show_cvlp_site_breakdown': True,
            
            # Referral Analysis
            'show_trial_referral_reporting': True,
            'show_referral_visualizations': True,
            'show_referral_breakdown': True,
            
            # Advanced Analytics
            'show_statistical_control': True,
            'show_performance_radar': True,
            'show_combined_analysis': True,
            
            # Technical & Debug
            'show_debug_info': True,
            'show_data_quality': True,
            'show_column_detection': True
        }
        st.rerun()

# Require file upload before rendering the dashboard
if uploaded_master_file is None:
    # Splash screen with centered logo and informative cancer messages
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style='display:flex; align-items:center; justify-content:center; margin: 10px 0 20px 0;'>
            <img src="data:image/jpeg;base64,{logo_base64}" alt="SCTU Logo" style="max-width: 480px; width: 40vw; height: auto; opacity: 0.95;"/>
        </div>
        <div style='text-align:center; max-width: 900px; margin: 0 auto; font-family: Inter, -apple-system, BlinkMacSystemFont, sans-serif;'>
            <h2 style='color:#1A237E; margin-bottom: 8px;'>BNT113 Clinical Trial Dashboard</h2>
            <p style='color:#5C6BC0; margin-top:0;'>Southampton Clinical Trials Unit</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Key informational messages
    st.markdown("### Cancer information and support")
    st.markdown(
        "- Early diagnosis improves outcomes. If you notice persistent, unusual symptoms, speak to a healthcare professional.\n"
        "- Screening and regular check-ups can detect cancers earlier. Follow local screening invitations where applicable.\n"
        "- Help is available. For general information and support, see trusted resources such as NHS information services or national cancer charities."
    )

    st.info("To begin, upload your BNT113-01 Master Tracker Excel file using the sidebar.")
    st.stop()

# Admin authentication for full data
if privacy_mode == "Full Data (Admin)":
    admin_password = st.sidebar.text_input("🔑 Admin Password:", type="password")
    if admin_password:
        if admin_password != "admin123":  # Replace with secure password
            st.sidebar.error("❌ Invalid password")
            privacy_mode = "Pseudonymized (Safe)"  # Fallback to safe mode
        else:
            st.sidebar.success("✅ Admin access granted")

# === QUICK STATS ===
st.sidebar.markdown("---")
st.sidebar.subheader("📈 Quick Stats")

# Add anonymization info
with st.sidebar.expander("🛡️ Privacy Information"):
    st.markdown("""
    **Pseudonymization Features:**
    - Patient names → Patient-XXXX
    - NHS Numbers → NHS-XXXXX
    - IDs → Masked format
    - Birth dates → Year only
    
    **Data Protection:**
    - No sensitive data in charts
    - Aggregated metrics only
    - Full data requires admin access
    """)

# Add pseudonymization function
def pseudonymize_data(df):
    """
    Pseudonymize sensitive patient data for dashboard display
    """
    if df.empty:
        return df
    
    df_pseudo = df.copy()
    
    # Define sensitive columns that need pseudonymization
    sensitive_columns = [
        'Patient full name',
        'NHS Number',
        'CVLP Participant ID',
        'Main trial participant ID',
        'Pre-screening ID',
        'Sample tracking ID',
        'Tissue Block ID',
        'Accession number',
        'Airway bill number',
        'Shipping tracking ID for curls & slides'
    ]
    
    for col in sensitive_columns:
        if col in df_pseudo.columns:
            # Create pseudonymized versions
            if col == 'Patient full name':
                # Replace with Patient-XXX format
                df_pseudo[col] = df_pseudo[col].apply(lambda x: 
                    f"Patient-{hash(str(x)) % 9999:04d}" if pd.notna(x) and str(x).strip() != '' else x)
            
            elif col == 'NHS Number':
                # Replace with NHS-XXX format, keeping length
                df_pseudo[col] = df_pseudo[col].apply(lambda x: 
                    f"NHS-{'X' * (len(str(x)) - 4)}" if pd.notna(x) and str(x).strip() != '' else x)
            
            elif 'ID' in col or 'Number' in col:
                # Replace with masked format keeping prefix
                df_pseudo[col] = df_pseudo[col].apply(lambda x: 
                    f"{str(x)[:4]}***{str(x)[-3:]}" if pd.notna(x) and len(str(x)) > 7 
                    else f"{str(x)[:2]}***" if pd.notna(x) and str(x).strip() != '' else x)
            
            else:
                # Generic masking for other sensitive fields
                df_pseudo[col] = df_pseudo[col].apply(lambda x: 
                    f"***{hash(str(x)) % 999:03d}" if pd.notna(x) and str(x).strip() != '' else x)
    
    # Optionally mask dates to just show month/year for additional privacy
    date_columns = [
        'Date of Birth',
        'Date patient consented into CVLP',
        'Date pre-screening referral form sent to trial site',
        'Date main trial screening referral form sent to trial site'
    ]
    
    for col in date_columns:
        if col in df_pseudo.columns:
            if col == 'Date of Birth':
                # Show only year for DOB
                df_pseudo[col] = pd.to_datetime(df_pseudo[col], errors='coerce').dt.year
            # Other dates keep as-is for analytics but could be further masked if needed
    
    return df_pseudo

# App title and description with SCTU branding
col1, col2 = st.columns([1, 4])

with col1:
    if os.path.exists("assets/SCTU Logo (mediabin resized).jpg"):
        st.image("assets/SCTU Logo (mediabin resized).jpg", width=120)

with col2:
    st.markdown("""
    <div style='margin-left: 40px; text-align: center;'>
        <h1 style='color: #1A237E; margin: 0; font-size: 3.2em; font-weight: 700;'>BNT113 Clinical Trial Dashboard</h1>
        <p style='color: #5C6BC0; margin: 5px 0; font-size: 1.4em; font-weight: 500;'>Southampton Clinical Trials Unit</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='margin: 20px 0; border: 1px solid #E8EAF6;'>", unsafe_allow_html=True)

# Load the data
@st.cache_data
def load_master_data_real(uploaded_file=None):
    try:
        if uploaded_file is not None:
            # Try different header configurations to find the right one
            # First try header=2 (row 3) - common Excel format with row 1 empty, row 2 titles, row 3 headers
            df = pd.read_excel(uploaded_file, sheet_name="CVLP - Master Tracker", header=2, index_col=False)
        else:
            # Use the local copy to avoid permission issues
            file_path = "BNT113-01-Master-Tracker-Local.xlsx"
            if not os.path.exists(file_path):
                # Fallback to original path
                file_path = os.path.join("..", "BNT113 real data", "BNT113-01 Master Tracker v1 15-Apr-2025.xlsx")
            if not os.path.exists(file_path):
                # Try alternative path
                file_path = "../BNT113 real data/BNT113-01 Master Tracker v1 15-Apr-2025.xlsx"
            df = pd.read_excel(file_path, sheet_name="CVLP - Master Tracker", header=0, index_col=False)
        
        # Only remove completely empty rows, keep the rest
        if not df.empty:
            df = df.dropna(how='all')
            df = df.reset_index(drop=True)
            
            # Clean up any unnamed columns that might be empty
            df = df.loc[:, ~df.columns.astype(str).str.contains('^Unnamed')]
        
        # Debug information - show what columns we actually loaded
        st.sidebar.success(f"✅ Loaded real data: {len(df)} records, {len(df.columns)} columns")
        
        return df
    except Exception as e:
        st.error(f"Error loading real master data: {str(e)}")
        st.error(f"Current directory: {os.getcwd()}")
        # Try with fallback approach if the first attempt fails
        try:
            st.warning("Trying alternative loading approach with header=1...")
            if uploaded_file is not None:
                df = pd.read_excel(uploaded_file, sheet_name="CVLP - Master Tracker", header=1, index_col=False)
            else:
                file_path = "BNT113-01-Master-Tracker-Local.xlsx"
                if not os.path.exists(file_path):
                    file_path = os.path.join("..", "BNT113 real data", "BNT113-01 Master Tracker v1 15-Apr-2025.xlsx")
                if not os.path.exists(file_path):
                    file_path = "../BNT113 real data/BNT113-01 Master Tracker v1 15-Apr-2025.xlsx"
                df = pd.read_excel(file_path, sheet_name="CVLP - Master Tracker", header=0, index_col=False)
            
            if not df.empty:
                df = df.dropna(how='all')
                df = df.reset_index(drop=True)
                df = df.loc[:, ~df.columns.astype(str).str.contains('^Unnamed')]
                
            st.sidebar.success(f"✅ Fallback loaded: {len(df)} records, {len(df.columns)} columns")
            
            return df
        except Exception as e2:
            st.error(f"Alternative loading also failed: {str(e2)}")
        return pd.DataFrame()

# Load the master data
master_df = load_master_data_real(uploaded_master_file)

# === DATA STATUS ===
if master_df.empty:
    st.sidebar.error("❌ No data loaded")
    st.sidebar.info("Please upload your Excel file above")
else:
    st.sidebar.success(f"✅ {len(master_df)} records loaded")
    
    # Quick data metrics
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("📊 Rows", len(master_df))
    with col2:
        st.metric("📋 Columns", len(master_df.columns))

# === SETTINGS ===
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Settings")
    
# Target configuration
with st.sidebar.expander("🎯 Configure Targets"):
    st.markdown("**Referral Targets:**")
    referred_target = st.number_input("Monthly Referral Target", min_value=0, value=50, step=1, key="referred_target")
    st.markdown("**Site Targets:**")
    st.info("Site targets are automatically calculated based on trial timeline")

# === ADVANCED OPTIONS ===
with st.sidebar.expander("🔧 Advanced Options"):
    st.markdown("**Developer Tools:**")
    show_debug = st.checkbox("Show Debug Information", value=False)
    show_column_info = st.checkbox("Show Column Details", value=False)
    
    if show_column_info and not master_df.empty:
        st.markdown("**Data Quality:**")
        # Check for missing values in key columns
        key_columns = ['CVLP Site', 'Trial Site', 'Patient full name']
        for col in key_columns:
            if col in master_df.columns:
                missing_count = master_df[col].isna().sum()
                if missing_count > 0:
                    st.warning(f"{col}: {missing_count} missing")
        else:
                    st.success(f"{col}: Complete")
        
        # Show columns AD, AM, BN, AC, AK, BL for BNT113-01 date tracking
        st.markdown("**🔍 BNT113-01 Date Columns:**")
        all_cols = list(master_df.columns)
        if len(all_cols) > 29:
            st.text(f"Col AD (30): {all_cols[29]}")
        if len(all_cols) > 30:
            st.text(f"Col AC (29): {all_cols[28]}")
        if len(all_cols) > 36:
            st.text(f"Col AK (37): {all_cols[36]}")
        if len(all_cols) > 38:
            st.text(f"Col AM (39): {all_cols[38]}")
        if len(all_cols) > 65:
            st.text(f"Col BN (66): {all_cols[65]}")
        if len(all_cols) > 63:
            st.text(f"Col BL (64): {all_cols[63]}")

# === ACHIEVEMENTS & BARRIERS TAB ===

# === ACTIONS ===
    st.sidebar.markdown("---")
if st.sidebar.button("🔄 Refresh Dashboard", type="primary"):
    st.rerun()

# Add a clean footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Version:** 2.0")
st.sidebar.markdown("**Updated:** January 2025")

# Apply pseudonymization before processing
if privacy_mode == "Pseudonymized (Safe)":
    # Apply pseudonymization to master data
    if not master_df.empty:
        master_df = pseudonymize_data(master_df)
        st.sidebar.info("🔒 Data pseudonymized for privacy")

# Data preprocessing function adapted for real data
def preprocess_real_data(df):
    if df.empty:
        return df, datetime.now(), datetime(2024, 12, 31)
    
    # Map your column names to what the dashboard expects (define at top of function)
    prescreen_referral_col = 'Please input the date the pre-screening referral form was sent to the trial site\n(dd/mm/yyyy)'
    main_trial_referral_col = 'Please input the date the main trial screening referral form was sent to the trial site\n(dd/mm/yyyy)'
    cvlp_consent_col = 'Please input the date the patient signed the consent form (dd/mm/yyyy)'
    cvlp_status_col = 'Please select the CVLP consent status'
    
    # Map additional columns from your file
    prescreen_consent_col = 'To be confirmed by trial site (Yes = consent confirmed, No = screen fail)'
    main_trial_consent_col = 'To be confirmed by trial site (Yes = consent confirmed, No = screen fail).1'
    enrolled_col = 'To be confirmed by trial site (enrolled = Yes, screen fail = No)'
    
    # Map screen failure columns from your file
    prescreen_fail_col = 'Clinical Liaison to confirm screen fail with CVLP site'
    main_trial_fail_col = 'Email the CVLP site to confirm that patient has not consented to the main trial'
    enrolment_fail_col = 'Email the CVLP site to confirm that patient has not enrolled to the trial'
    
    # DEBUG: Show which key columns we're looking for vs what we found
    key_columns_to_check = {
        'CVLP Site': 'CVLP Site',
        'Trial Site': 'Trial Site', 
        'CVLP Consent': cvlp_consent_col,
        'Prescreen Referral': prescreen_referral_col,
        'Main Trial Referral': main_trial_referral_col,
        'CVLP Status': cvlp_status_col
    }
    
    # Check which columns exist
    found_columns = {}
    missing_columns = []
    
    for label, col_name in key_columns_to_check.items():
        if col_name in df.columns:
            found_columns[label] = col_name
        else:
            missing_columns.append(label)
    
    # Convert date columns to datetime using the actual column names from your file
    date_columns = [
        cvlp_consent_col,
        prescreen_referral_col,
        main_trial_referral_col,
        'Please input the date  tissue block sent to CPGC\n(dd/mm/yyyy)',
        'Please confirm date of next surveillance visit for patients referred to pre-screening. The Clinical Liaison will use this to check for updates on main trial eligibility',
        'Date of advanced diagnosis (confirmed by CVLP site by email or on referral form)'
    ]
    
    for col in date_columns:
        if col in df.columns:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
            except:
                pass
    
    # Calculate today's date and intervals
    today = datetime.now()
    dec_2024 = pd.Timestamp('2024-12-31')
    
    # Create calculated fields using the actual column names from your file
    
    # Referred (Count of SINGLE patients referral - either pre-screening OR main trial)
    df['is_referred'] = False
    if prescreen_referral_col in df.columns:
        df['is_referred'] = df['is_referred'] | (~df[prescreen_referral_col].isna())
    if main_trial_referral_col in df.columns:
        df['is_referred'] = df['is_referred'] | (~df[main_trial_referral_col].isna())
    
    # Referred to pre-screen
    df['is_referred_to_prescreen'] = False
    if prescreen_referral_col in df.columns:
        df['is_referred_to_prescreen'] = ~df[prescreen_referral_col].isna()
    
    # Referred to main trial
    df['is_referred_to_main_trial'] = False
    if main_trial_referral_col in df.columns:
        df['is_referred_to_main_trial'] = ~df[main_trial_referral_col].isna()
    
    # Recruited to CVLP (CVLP consented patients)
    df['is_recruited_to_cvlp'] = False
    if cvlp_status_col in df.columns:
        df['is_recruited_to_cvlp'] = df[cvlp_status_col].astype(str).str.strip().str.lower() == 'obtained'
    elif cvlp_consent_col in df.columns:
        df['is_recruited_to_cvlp'] = ~df[cvlp_consent_col].isna()
    
    # Consented BNT113-01 (pre-screen)
    df['is_consented_prescreen'] = False
    if prescreen_consent_col in df.columns:
        df['is_consented_prescreen'] = df[prescreen_consent_col].astype(str).str.strip().str.lower().isin(['yes', 'y', 'true'])
    
    # Randomised BNT113-01 (enrolled participants)
    df['is_randomised'] = False
    if enrolled_col in df.columns:
        df['is_randomised'] = df[enrolled_col].astype(str).str.strip().str.lower().isin(['yes', 'y', 'true'])
    
    # BNT113-01 Screen Failures
    df['is_screen_failure'] = False
    
    # Screen failures could be derived from various columns
    if prescreen_fail_col in df.columns:
        df['is_screen_failure'] = df['is_screen_failure'] | (~df[prescreen_fail_col].isna())
    if main_trial_fail_col in df.columns:
        df['is_screen_failure'] = df['is_screen_failure'] | (~df[main_trial_fail_col].isna())
    if enrolment_fail_col in df.columns:
        df['is_screen_failure'] = df['is_screen_failure'] | (~df[enrolment_fail_col].isna())
    
    return df, today, dec_2024

processed_df, today, dec_2024 = preprocess_real_data(master_df)

# Create the metrics tiles dashboard component instead of table
def create_metrics_tiles(df):
    if df.empty:
        st.warning("No data available to create metrics")
        return
    
    # Safely get the counts, defaulting to 0 if columns don't exist
    try:
        referred_count = int(df['is_referred'].sum())
    except:
        referred_count = 0
        
    try:
        referred_to_prescreen_count = int(df['is_referred_to_prescreen'].sum())
    except:
        referred_to_prescreen_count = 0
        
    try:
        referred_to_main_trial_count = int(df['is_referred_to_main_trial'].sum()) 
    except:
        referred_to_main_trial_count = 0
        
    try:
        recruited_to_cvlp_count = int(df['is_recruited_to_cvlp'].sum())
    except:
        recruited_to_cvlp_count = 0
        
    try:
        consented_prescreen_count = int(df['is_consented_prescreen'].sum())
    except:
        consented_prescreen_count = 0
        
    try:
        randomised_count = int(df['is_randomised'].sum())
    except:
        randomised_count = 0
        
    try:
        screen_failures_count = int(df['is_screen_failure'].sum())
    except:
        screen_failures_count = 0
    
    # Create modern section header
    st.markdown("""
    <div class="section-header fade-in">
        📊 Trial Progress Overview - Key Metrics
    </div>
    """, unsafe_allow_html=True)
    
    # First row - 4 tiles
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"""
            <div class="metric-card fade-in" style="animation-delay: 0s;">
                <div style="text-align: center;">
                    <div class="metric-icon" style="color: {COLOR_PALETTE['info']};">👥</div>
                    <div class="metric-value" style="background: linear-gradient(135deg, {COLOR_PALETTE['info']} 0%, {COLOR_PALETTE['info_dark']} 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">{referred_count}</div>
                    <div class="metric-label">Total Referred</div>
                    <div style="font-size: 0.85rem; color: {COLOR_PALETTE['text_muted']}; margin-top: 0.5rem;">Individual patients referred</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="metric-card fade-in" style="animation-delay: 0.1s;">
                <div style="text-align: center;">
                    <div class="metric-icon" style="color: {COLOR_PALETTE['chart_6']};">🔍</div>
                    <div class="metric-value" style="background: linear-gradient(135deg, {COLOR_PALETTE['chart_6']} 0%, {COLOR_PALETTE['primary_dark']} 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">{referred_to_prescreen_count}</div>
                    <div class="metric-label">Pre-screen Referrals</div>
                    <div style="font-size: 0.85rem; color: {COLOR_PALETTE['text_muted']}; margin-top: 0.5rem;">Patients referred to pre-screening</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="metric-card fade-in" style="animation-delay: 0.2s;">
                <div style="text-align: center;">
                    <div class="metric-icon" style="color: {COLOR_PALETTE['warning']};">🎯</div>
                    <div class="metric-value" style="background: linear-gradient(135deg, {COLOR_PALETTE['warning']} 0%, {COLOR_PALETTE['warning_dark']} 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">{referred_to_main_trial_count}</div>
                    <div class="metric-label">Main Trial Referrals</div>
                    <div style="font-size: 0.85rem; color: {COLOR_PALETTE['text_muted']}; margin-top: 0.5rem;">Patients referred to main trial</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            f"""
            <div class="metric-card fade-in" style="animation-delay: 0.3s;">
                <div style="text-align: center;">
                    <div class="metric-icon" style="color: {COLOR_PALETTE['success']};">✅</div>
                    <div class="metric-value" style="background: linear-gradient(135deg, {COLOR_PALETTE['success']} 0%, {COLOR_PALETTE['success_dark']} 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">{recruited_to_cvlp_count}</div>
                    <div class="metric-label">CVLP Recruited</div>
                    <div style="font-size: 0.85rem; color: {COLOR_PALETTE['text_muted']}; margin-top: 0.5rem;">CVLP consented patients</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Second row - 3 tiles centered
    col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 1])
    
    with col2:
        st.markdown(
            f"""
            <div class="metric-card fade-in" style="animation-delay: 0.4s;">
                <div style="text-align: center;">
                    <div class="metric-icon" style="color: {COLOR_PALETTE['chart_8']};">📋</div>
                    <div class="metric-value" style="background: linear-gradient(135deg, {COLOR_PALETTE['chart_8']} 0%, {COLOR_PALETTE['info_dark']} 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">{consented_prescreen_count}</div>
                    <div class="metric-label">BNT113-01 Consented</div>
                    <div style="font-size: 0.85rem; color: {COLOR_PALETTE['text_muted']}; margin-top: 0.5rem;">Pre-screening consented</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="metric-card fade-in" style="animation-delay: 0.5s;">
                <div style="text-align: center;">
                    <div class="metric-icon" style="color: {COLOR_PALETTE['chart_9']};">🎲</div>
                    <div class="metric-value" style="background: linear-gradient(135deg, {COLOR_PALETTE['chart_9']} 0%, {COLOR_PALETTE['info']} 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">{randomised_count}</div>
                    <div class="metric-label">Randomised</div>
                    <div style="font-size: 0.85rem; color: {COLOR_PALETTE['text_muted']}; margin-top: 0.5rem;">Randomised to BNT113-01</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            f"""
            <div class="metric-card fade-in" style="animation-delay: 0.6s;">
                <div style="text-align: center;">
                    <div class="metric-icon" style="color: {COLOR_PALETTE['danger']};">⚠️</div>
                    <div class="metric-value" style="background: linear-gradient(135deg, {COLOR_PALETTE['danger']} 0%, {COLOR_PALETTE['danger_dark']} 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">{screen_failures_count}</div>
                    <div class="metric-label">Screen Failures</div>
                    <div style="font-size: 0.85rem; color: {COLOR_PALETTE['text_muted']}; margin-top: 0.5rem;">Failed screening criteria</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# Create dashboard sections
if st.session_state.admin_settings['show_key_metrics']:
    st.markdown("""
    <div class="section-header fade-in">
        🎯 Trial Progress Overview
    </div>
    """, unsafe_allow_html=True)

# Create the metrics overview
with st.container():
    create_metrics_tiles(processed_df)

# Data Quality Dashboard disabled to avoid user disruption

# Add modern spacing
st.markdown("""
<div style="margin: 3rem 0;">
    <hr style="border: none; height: 1px; background: linear-gradient(90deg, transparent, #e9ecef, transparent); margin: 2rem 0;">
</div>
""", unsafe_allow_html=True)

# Create referral vs target visualization
if st.session_state.admin_settings['show_referral_performance'] and not processed_df.empty:
    st.markdown("""
    <div class="section-header fade-in">
        📈 Referral Performance vs Targets
    </div>
    """, unsafe_allow_html=True)
    
    # Get actual metrics
    try:
        referred_actual = int(processed_df['is_referred'].sum())
    except:
        referred_actual = 0
        
    try:
        prescreen_actual = int(processed_df['is_referred_to_prescreen'].sum())
    except:
        prescreen_actual = 0
        
    try:
        main_trial_actual = int(processed_df['is_referred_to_main_trial'].sum())
    except:
        main_trial_actual = 0
        
    try:
        cvlp_actual = int(processed_df['is_recruited_to_cvlp'].sum())
    except:
        cvlp_actual = 0
        
    try:
        randomised_actual = int(processed_df['is_randomised'].sum())
    except:
        randomised_actual = 0
    
    # Use the target from the sidebar Settings section
    referred_target = st.session_state.get('referred_target', 50)
    
    # Create the comparison data
    metrics = ['Total\nReferred']
    actual_values = [referred_actual]
    target_values = [referred_target]
    
    # Create DataFrame for plotting
    chart_data = pd.DataFrame({
        'Metric': metrics * 2,
        'Value': actual_values + target_values,
        'Type': ['Actual'] * 1 + ['Target'] * 1
    })
    
    # Create the bar chart
    fig = px.bar(
        chart_data,
        x='Metric',
        y='Value',
        color='Type',
        barmode='group',
        title='Trial Performance: Actual vs Target',
        color_discrete_map={
            'Actual': clinical_colors['primary'][5],
            'Target': clinical_colors['neutral'][4]
        }
    )
    
    # Customize the chart
    fig.update_layout(
        xaxis_title='',
        yaxis_title='Number of Patients',
        plot_bgcolor='rgba(0,0,0,0)',
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Add percentage achievement annotations
    for i, (actual, target) in enumerate(zip(actual_values, target_values)):
        if target > 0:
            percentage = (actual / target) * 100
            color = 'green' if percentage >= 80 else 'orange' if percentage >= 50 else 'red'
            fig.add_annotation(
                x=i,
                y=max(actual, target) + max(target_values) * 0.05,
                text=f"{percentage:.1f}%",
                showarrow=False,
                font=dict(color=color, size=12, family="Arial Black")
            )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add a summary metrics table below the chart
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_actual = sum(actual_values)
        total_target = sum(target_values)
        overall_percentage = (total_actual / total_target * 100) if total_target > 0 else 0
        create_enhanced_metric_card(
            icon="🎯",
            label="Overall Achievement",
            value=f"{overall_percentage:.1f}%",
            subtitle=f"{total_actual}/{total_target}",
            color=COLOR_PALETTE['success'] if overall_percentage >= 80 else COLOR_PALETTE['warning'] if overall_percentage >= 50 else COLOR_PALETTE['danger']
        )
    
    with col2:
        # Count metrics achieving >80% of target
        high_performers = sum(1 for a, t in zip(actual_values, target_values) if t > 0 and (a/t) >= 0.8)
        create_enhanced_metric_card(
            icon="⭐",
            label="Metrics Above 80%",
            value=f"{high_performers}/1",
            subtitle="High Performance",
            color=COLOR_PALETTE['info']
        )
    
    with col3:
        # Show the metric with highest achievement
        best_metric_idx = 0
        best_percentage = 0
        for i, (actual, target) in enumerate(zip(actual_values, target_values)):
            if target > 0:
                percentage = (actual / target) * 100
                if percentage > best_percentage:
                    best_percentage = percentage
                    best_metric_idx = i
        
        create_enhanced_metric_card(
            icon="🏆",
            label="Best Performing",
            value=metrics[best_metric_idx].replace('\n', ' '),
            subtitle=f"{best_percentage:.1f}%",
            color=COLOR_PALETTE['success']
        )

# Monthly Trial Metrics Table section
if st.session_state.admin_settings['show_monthly_table']:
    st.markdown("""
    <div class="section-divider">
        <div class="section-divider-icon">📊</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header fade-in">
        📅 Monthly Trial Metrics Table
    </div>
    """, unsafe_allow_html=True)

# Function to create the monthly breakdown table matching the Excel structure
def create_monthly_projections_table(master_df, uploaded_file=None):
    st.markdown("### Monthly Trial Metrics Table")
    
    # Define the month range and site opening schedule (Contract ends Nov-26)
    months = [
        'Apr-25', 'May-25', 'Jun-25', 'Jul-25', 'Aug-25', 'Sep-25', 'Oct-25', 'Nov-25', 'Dec-25',
        'Jan-26', 'Feb-26', 'Mar-26', 'Apr-26', 'May-26', 'Jun-26', 'Jul-26', 'Aug-26', 'Sep-26', 
        'Oct-26', 'Nov-26'
    ]
    
    # Site opening targets (updated from colleague's data) - ends at Nov-26
    site_targets = [7, 12, 18, 22, 26, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
    
    # Projected cumulative targets (updated from colleague's data) - ends at Nov-26
    projected_targets = [1, 2, 4, 7, 11, 17, 24, 31, 35, 40, 50, 60, 66, 73, 81, 90, 100, 111, 123, 136]
    
    # Create the DataFrame structure with actual calculations
    table_data = []
    
    # Hardcoded Go-Live dates for ALL 19 CVLP sites (ACTUAL DATES FROM CLIENT)
    # These dates are used to compute "Open Sites - Actual" per month
    HARDCODED_OPENING_DATES = {
        # May 2025 openings
        "Coventry and Warwickshire": pd.Timestamp("2025-05-13"),
        "Bath": pd.Timestamp("2025-05-15"),
        "Gloucestershire": pd.Timestamp("2025-05-15"),
        "Univeristy Hospitals Dorset": pd.Timestamp("2025-05-15"),
        "Mid & South Essex - Broomfield": pd.Timestamp("2025-05-21"),
        "Mid & South Essex - Southend": pd.Timestamp("2025-05-21"),
        "Bedfordshire": pd.Timestamp("2025-05-22"),
        "Hull": pd.Timestamp("2025-05-22"),
        "Royal Surrey": pd.Timestamp("2025-05-29"),
        
        # June 2025 openings
        "Royal Berkshire": pd.Timestamp("2025-06-30"),
        
        # July 2025 openings
        "United Lincolnshire": pd.Timestamp("2025-07-17"),
        "York & Scarborough": pd.Timestamp("2025-07-22"),
        
        # August 2025 openings
        "Royal Free (North Middlesex)": pd.Timestamp("2025-08-05"),
        "Barking Havering and Redbridge": pd.Timestamp("2025-08-08"),
        "East & North Herefordshire (Lister)": pd.Timestamp("2025-08-12"),
        "North Cumbria": pd.Timestamp("2025-08-27"),
        
        # September 2025 openings
        "West Suffolk": pd.Timestamp("2025-09-19"),
        "Maidstone": pd.Timestamp("2025-09-24"),
        "Leicester": pd.Timestamp("2025-09-29"),
    }
    # Make available globally so later code paths can reuse without re-reading
    globals()['site_opening_data'] = HARDCODED_OPENING_DATES
    globals()['site_opening_data_source'] = 'HARDCODED'
    
    # Check if CVLP Site column exists
    cvlp_site_col = 'CVLP Site'
    if cvlp_site_col not in master_df.columns:
        # Try alternative column names
        possible_site_cols = [
            'CVLP site', 
            'Please choose the CVLP site from the drop down',
            'Site',
            'CVLP Site Name',
            'Site Name'
        ]
        for col in possible_site_cols:
            if col in master_df.columns:
                cvlp_site_col = col
                break
        
        # If still not found, try fuzzy matching
        if cvlp_site_col not in master_df.columns:
            for col in master_df.columns:
                col_str = str(col).lower()
                if 'site' in col_str and ('cvlp' in col_str or 'drop' in col_str):
                    cvlp_site_col = col
                    break
    
    # Get current date for determining future months
    current_date = pd.Timestamp.now()
    
    for i, month in enumerate(months):
        # Parse month and year for date calculations
        month_parts = month.split('-')
        year = int('20' + month_parts[1])
        month_name = month_parts[0]
        
        # Map month name to number
        month_map = {
            'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
            'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
        }
        
        if month_name in month_map:
            month_num = month_map[month_name]
            
            # Define start and end dates for this month
            start_date = pd.Timestamp(year, month_num, 1)
            
            # Define end date for this month (last day of month)
            if month_num == 12:
                end_date = pd.Timestamp(year + 1, 1, 1) - pd.Timedelta(days=1)
            else:
                end_date = pd.Timestamp(year, month_num + 1, 1) - pd.Timedelta(days=1)
            
            # Check if this month is in the future
            is_future_month = end_date > current_date
            
            # Calculate actual values from data
            
            # 1. Open Sites - Actual: Get from CVLP Site Data sheet
            open_sites_actual = 0
            
            # Try to read site opening data from CVLP Site Data sheet
            # Skip reading if hardcoded opening dates have been provided
            if i == 0 and not (
                'site_opening_data' in globals() and isinstance(globals()['site_opening_data'], dict) and len(globals()['site_opening_data']) > 0
            ):  # Only do this once and store the result
                try:
                    # Read the CVLP Site Data sheet
                    cvlp_site_data_df = pd.read_excel(uploaded_file, sheet_name='CVLP Site Data', header=0)
                    
                    # Debug: Show what we found
                    # Look for site opening date columns
                    site_opening_data = {}
                    
                    # Try to find site names and opening dates
                    site_col = None
                    date_col = None
                    
                    # Look for site column
                    for col in cvlp_site_data_df.columns:
                        if 'site' in str(col).lower() or any(site_name in str(col) for site_name in ['Coventry', 'Bath', 'Gloucestershire']):
                            site_col = col
                            break
                    
                    # Look for opening date column with priority:
                    # 1) Go-Live / Green light
                    # 2) Site Active Date
                    # 3) Generic Open/Opening Date
                    for col in cvlp_site_data_df.columns:
                        col_lower = str(col).strip().lower()
                        if (
                            'go-live date' in col_lower
                            or 'go live date' in col_lower
                            or 'go live' in col_lower
                            or 'go-live' in col_lower
                            or 'green light' in col_lower
                        ):
                            date_col = col
                            break

                    if date_col is None:
                        for col in cvlp_site_data_df.columns:
                            col_lower = str(col).strip().lower()
                            if 'site active' in col_lower and 'date' in col_lower:
                                date_col = col
                                break

                    if date_col is None:
                        for col in cvlp_site_data_df.columns:
                            col_lower = str(col).strip().lower()
                            if (('open' in col_lower or 'opening' in col_lower) and 'date' in col_lower):
                                date_col = col
                                break
                    
                    # If we found both columns, extract the data
                    if site_col is not None and date_col is not None:
                        for _, row in cvlp_site_data_df.iterrows():
                            site_name = row[site_col]
                            opening_date = row[date_col]
                            if pd.notna(site_name) and pd.notna(opening_date):
                                try:
                                    opening_date_parsed = pd.to_datetime(opening_date, errors='coerce')
                                    if pd.notna(opening_date_parsed):
                                        site_opening_data[str(site_name)] = opening_date_parsed
                                except:
                                    pass
                
                    # Store this globally so we don't re-read every month
                    globals()['site_opening_data'] = site_opening_data
                except Exception as e:
                    pass  # Silently handle errors
                    # Fallback to all 9 sites open
                    globals()['site_opening_data'] = {}
            else:
                # Using hardcoded opening dates
                pass
            
            # Try to read screening logs data for multiple columns
            if i == 0:  # Only do this once
                try:
                    if uploaded_screening_logs_file is not None:
                        # Read all sheets from the screening logs file
                        excel_file = pd.ExcelFile(uploaded_screening_logs_file)
                        all_screening_data = []
                        all_cvlp_consent_data = []
                        all_referral_data = []
                        
                        # Loop through all sheets (site/city sheets)
                        for sheet_name in excel_file.sheet_names:
                            try:
                                sheet_df = pd.read_excel(uploaded_screening_logs_file, sheet_name=sheet_name, header=0)
                                
                                # Look for "Date of Screening" column (for Reviewed - Actual)
                                date_of_screening_col = None
                                for col in sheet_df.columns:
                                    col_str = str(col).strip().lower()
                                    if 'date of screening' in col_str or 'screening date' in col_str:
                                        date_of_screening_col = col
                                        break
                                
                                if date_of_screening_col and date_of_screening_col in sheet_df.columns:
                                    screening_dates = sheet_df[[date_of_screening_col]].copy()
                                    screening_dates.columns = ['Date of Screening']
                                    all_screening_data.append(screening_dates)
                                
                                # Look for CVLP consent column (for Recruited to CVLP - Actual)
                                # This can be either "Consented to CVLP" (Yes/No) or a date column
                                cvlp_consent_col = None
                                for col in sheet_df.columns:
                                    col_str = str(col).strip().lower()
                                    # Look for "Consented to CVLP" (Yes/No column) or date columns
                                    if ('consented to cvlp' in col_str or 
                                        'cvlp consent' in col_str or 
                                        ('cvlp' in col_str and ('date' in col_str or 'consent' in col_str))):
                                        cvlp_consent_col = col
                                        break
                                
                                if cvlp_consent_col and cvlp_consent_col in sheet_df.columns:
                                    cvlp_dates = sheet_df[[cvlp_consent_col]].copy()
                                    cvlp_dates.columns = ['CVLP Consent Date']
                                    all_cvlp_consent_data.append(cvlp_dates)
                                
                                # Look for referral date column (for Referred - Actual)
                                referral_date_col = None
                                for col in sheet_df.columns:
                                    col_lower = str(col).lower()
                                    if ('referral' in col_lower or 'referred' in col_lower) and 'date' in col_lower:
                                        referral_date_col = col
                                        break
                                
                                if referral_date_col and referral_date_col in sheet_df.columns:
                                    referral_dates = sheet_df[[referral_date_col]].copy()
                                    referral_dates.columns = ['Referral Date']
                                    all_referral_data.append(referral_dates)
                            except Exception as sheet_error:
                                pass  # Silently skip sheets with errors
                        
                        # Combine all data from all sheets
                        if all_screening_data:
                            combined_screening_df = pd.concat(all_screening_data, ignore_index=True)
                            globals()['screening_logs_data'] = combined_screening_df
                        else:
                            globals()['screening_logs_data'] = pd.DataFrame()
                        
                        if all_cvlp_consent_data:
                            combined_cvlp_df = pd.concat(all_cvlp_consent_data, ignore_index=True)
                            globals()['screening_logs_cvlp_data'] = combined_cvlp_df
                        else:
                            globals()['screening_logs_cvlp_data'] = pd.DataFrame()
                        
                        if all_referral_data:
                            combined_referral_df = pd.concat(all_referral_data, ignore_index=True)
                            globals()['screening_logs_referral_data'] = combined_referral_df
                        else:
                            globals()['screening_logs_referral_data'] = pd.DataFrame()
                    else:
                        globals()['screening_logs_data'] = pd.DataFrame()
                        globals()['screening_logs_cvlp_data'] = pd.DataFrame()
                        globals()['screening_logs_referral_data'] = pd.DataFrame()
                except Exception as e:
                    globals()['screening_logs_data'] = pd.DataFrame()
                    globals()['screening_logs_cvlp_data'] = pd.DataFrame()
                    globals()['screening_logs_referral_data'] = pd.DataFrame()
            
            # Calculate open sites for this month using the site opening data
            if 'site_opening_data' in globals():
                site_data = globals()['site_opening_data']
                if site_data:
                    # Count sites that opened by the end of this month
                    open_sites_actual = sum(1 for opening_date in site_data.values() 
                                          if opening_date <= end_date)
                else:
                    # Fallback: assume all 9 sites are open
                    open_sites_actual = 9
            else:
                # Fallback: assume all 9 sites are open
                open_sites_actual = 9
            
            # Debug for first few months
            
            # 2. Referred - Actual: CUMULATIVE count of unique patients referred UP TO this month
            referred_actual = 0
            
            # First, check screening logs data (if available)
            if 'screening_logs_referral_data' in globals() and not globals()['screening_logs_referral_data'].empty:
                referral_df = globals()['screening_logs_referral_data']
                if 'Referral Date' in referral_df.columns:
                    try:
                        referral_dates = pd.to_datetime(referral_df['Referral Date'], errors='coerce')
                        valid_dates = referral_dates.dropna()
                        # CUMULATIVE: count all referrals up to end of this month
                        referred_actual = (valid_dates <= end_date).sum()
                    except:
                        pass
            
            # If no screening logs data, fall back to master tracker
            if referred_actual == 0 and not master_df.empty:
                referred_mask = pd.Series(False, index=master_df.index)
                
                # Check pre-screening referral dates
                prescreen_col = 'Please input the date the pre-screening referral form was sent to the trial site\n(dd/mm/yyyy)'
                if prescreen_col in master_df.columns:
                    try:
                        prescreen_dates = pd.to_datetime(master_df[prescreen_col], errors='coerce')
                        # CUMULATIVE: count all referrals up to end of this month
                        referred_mask = referred_mask | (prescreen_dates <= end_date)
                    except:
                        pass
                
                # Check main trial referral dates
                main_trial_col = 'Please input the date the main trial screening referral form was sent to the trial site\n(dd/mm/yyyy)'
                if main_trial_col in master_df.columns:
                    try:
                        main_trial_dates = pd.to_datetime(master_df[main_trial_col], errors='coerce')
                        # CUMULATIVE: count all referrals up to end of this month
                        referred_mask = referred_mask | (main_trial_dates <= end_date)
                    except:
                        pass
                
                referred_actual = referred_mask.sum()
            
            # 3. Referred to pre-screen - Actual (CUMULATIVE)
            referred_prescreen_actual = 0
            if not master_df.empty and prescreen_col in master_df.columns:
                try:
                    prescreen_dates = pd.to_datetime(master_df[prescreen_col], errors='coerce')
                    # CUMULATIVE: count all pre-screen referrals up to end of this month
                    referred_prescreen_actual = (prescreen_dates <= end_date).sum()
                except:
                    pass
            
            # 4. Referred to main trial - Actual (CUMULATIVE)
            referred_main_trial_actual = 0
            if not master_df.empty and main_trial_col in master_df.columns:
                try:
                    main_trial_dates = pd.to_datetime(master_df[main_trial_col], errors='coerce')
                    # CUMULATIVE: count all main trial referrals up to end of this month
                    referred_main_trial_actual = (main_trial_dates <= end_date).sum()
                except:
                    pass
            
            # 5. Recruited to CVLP - Actual (CUMULATIVE count from BOTH Screening Logs AND Master Tracker)
            recruited_cvlp_actual_from_logs = 0
            recruited_cvlp_actual_from_master = 0
            
            # First, check screening logs data (if available)
            # The "Consented to CVLP" column contains "Yes"/"No" values, not dates
            if 'screening_logs_cvlp_data' in globals() and not globals()['screening_logs_cvlp_data'].empty:
                cvlp_df = globals()['screening_logs_cvlp_data']
                if 'CVLP Consent Date' in cvlp_df.columns:
                    try:
                        # Check if the column contains Yes/No values or dates
                        sample_value = cvlp_df['CVLP Consent Date'].dropna().iloc[0] if len(cvlp_df['CVLP Consent Date'].dropna()) > 0 else None
                        
                        if sample_value and isinstance(sample_value, str):
                            # It's a Yes/No column - count "Yes" values (cumulative)
                            # We need to match this with screening dates to make it cumulative
                            if 'screening_logs_data' in globals() and not globals()['screening_logs_data'].empty:
                                screening_df = globals()['screening_logs_data']
                                if 'Date of Screening' in screening_df.columns and len(cvlp_df) == len(screening_df):
                                    # Combine the data
                                    combined = pd.DataFrame({
                                        'consent': cvlp_df['CVLP Consent Date'],
                                        'date': pd.to_datetime(screening_df['Date of Screening'], errors='coerce')
                                    })
                                    # Count "Yes" values where date is up to end of this month
                                    recruited_cvlp_actual_from_logs = ((combined['consent'].astype(str).str.strip().str.lower() == 'yes') & 
                                                            (combined['date'] <= end_date)).sum()
                        else:
                            # It's a date column
                            cvlp_consent_dates = pd.to_datetime(cvlp_df['CVLP Consent Date'], errors='coerce')
                            valid_dates = cvlp_consent_dates.dropna()
                            recruited_cvlp_actual_from_logs = (valid_dates <= end_date).sum()
                    except:
                        pass
            
            # Also check master tracker (to capture any additional patients not in screening logs)
            if not master_df.empty:
                cvlp_consent_col = 'Please input the date the patient signed the consent form (dd/mm/yyyy)'
                if cvlp_consent_col in master_df.columns:
                    try:
                        cvlp_dates = pd.to_datetime(master_df[cvlp_consent_col], errors='coerce')
                        # CUMULATIVE: count all CVLP consents up to end of this month
                        recruited_cvlp_actual_from_master = (cvlp_dates <= end_date).sum()
                    except:
                        pass
            
            # Use the MAXIMUM of the two sources (to avoid double counting, use the higher value)
            # This assumes that one source is more complete than the other
            recruited_cvlp_actual = max(recruited_cvlp_actual_from_logs, recruited_cvlp_actual_from_master)
            
            # 5a. Reviewed - Actual (from Screening Logs - all sheets combined) - CUMULATIVE
            reviewed_actual = 0
            if 'screening_logs_data' in globals() and not globals()['screening_logs_data'].empty:
                screening_df = globals()['screening_logs_data']
                
                # The combined data has "Date of Screening" column
                if 'Date of Screening' in screening_df.columns:
                    try:
                        # Convert to datetime and filter - CUMULATIVE (up to end of this month)
                        screening_dates = pd.to_datetime(screening_df['Date of Screening'], errors='coerce')
                        # Count all non-null dates UP TO the end of this month (cumulative)
                        valid_dates = screening_dates.dropna()
                        reviewed_actual = (valid_dates <= end_date).sum()
                        
                        # Debug for first few months
                    except Exception as e:
                        pass  # Silently handle errors
            
            # 6. Consented BNT113-01 (pre-screen) - Actual (cumulative up to this month)
            # Use actual consent date from column AD (index 29)
            consented_prescreen_actual = 0
            if not master_df.empty and len(master_df.columns) > 29:
                try:
                    # Column AD contains pre-screening consent date
                    prescreen_consent_date_col = master_df.columns[29]
                    consent_dates = pd.to_datetime(master_df[prescreen_consent_date_col], errors='coerce')
                    # Count all consents up to end of this month (cumulative)
                    consented_prescreen_actual = (consent_dates <= end_date).sum()
                    
                    # Debug for first month
                except Exception as e:
                    pass  # Silently handle errors
            
            # 7. Consented BNT113-01 (main trial) - Actual (cumulative up to this month)
            # Use actual consent date from column AM (index 38)
            consented_main_trial_actual = 0
            if not master_df.empty and len(master_df.columns) > 38:
                try:
                    # Column AM contains main trial consent date
                    main_trial_consent_date_col = master_df.columns[38]
                    consent_dates = pd.to_datetime(master_df[main_trial_consent_date_col], errors='coerce')
                    # Count all consents up to end of this month (cumulative)
                    consented_main_trial_actual = (consent_dates <= end_date).sum()
                    
                    # Debug for first month
                except Exception as e:
                    pass  # Silently handle errors
            
            # 8. Randomised BNT113-01 - Actual (cumulative up to this month)
            # Use actual randomisation date from column BN (index 65)
            randomised_actual = 0
            if not master_df.empty and len(master_df.columns) > 65:
                try:
                    # Column BN contains randomisation date
                    randomisation_date_col = master_df.columns[65]
                    randomisation_dates = pd.to_datetime(master_df[randomisation_date_col], errors='coerce')
                    # Count all randomisations up to end of this month (cumulative)
                    randomised_actual = (randomisation_dates <= end_date).sum()
                except Exception as e:
                    pass  # Silently handle errors
            
            # 9. BNT113-01 Screen Failures - Actual (cumulative up to this month)
            # Use actual screen fail dates from columns AC (28), AK (36), BL (63)
            screen_failures_actual = 0
            if not master_df.empty:
                try:
                    failure_mask = pd.Series(False, index=master_df.index)
                    
                    # Column AC (index 28) - screen fail date 1
                    if len(master_df.columns) > 28:
                        fail_date_col1 = master_df.columns[28]
                        fail_dates1 = pd.to_datetime(master_df[fail_date_col1], errors='coerce')
                        # Count all failures up to end of this month (cumulative)
                        failure_mask = failure_mask | ((fail_dates1 <= end_date) & fail_dates1.notna())
                    
                    # Column AK (index 36) - screen fail date 2
                    if len(master_df.columns) > 36:
                        fail_date_col2 = master_df.columns[36]
                        fail_dates2 = pd.to_datetime(master_df[fail_date_col2], errors='coerce')
                        # Count all failures up to end of this month (cumulative)
                        failure_mask = failure_mask | ((fail_dates2 <= end_date) & fail_dates2.notna())
                    
                    # Column BL (index 63) - screen fail date 3
                    if len(master_df.columns) > 63:
                        fail_date_col3 = master_df.columns[63]
                        fail_dates3 = pd.to_datetime(master_df[fail_date_col3], errors='coerce')
                        # Count all failures up to end of this month (cumulative)
                        failure_mask = failure_mask | ((fail_dates3 <= end_date) & fail_dates3.notna())
                    
                    screen_failures_actual = failure_mask.sum()
                except Exception as e:
                    pass  # Silently handle errors
            
            # Calculate targets
            sites_target = site_targets[i] if i < len(site_targets) else 30
            projected_target = projected_targets[i] if i < len(projected_targets) else 216
            
            # Calculate Referred - Target (0.25/site) as ACCUMULATIVE target
            if i == 0:
                # For first month (Apr-25), there are no previous open sites, so target = 0
                referred_target_per_site = 0
            else:
                # Calculate accumulative target: sum of all monthly targets up to current month
                accumulative_target = 0
                for j in range(1, i + 1):  # Start from month 1 (skip first month)
                    if j <= len(table_data):
                        # Use previous month's actual sites for each month's contribution
                        prev_month_data = table_data[j-1] if j > 0 else None
                        if prev_month_data:
                            prev_actual_sites = prev_month_data['Open Sites - Actual']
                            # Handle "-" string for future months - skip calculation
                            if isinstance(prev_actual_sites, str) and prev_actual_sites == '-':
                                continue  # Skip future months in accumulative calculation
                            monthly_contribution = prev_actual_sites * 0.25
                            accumulative_target += monthly_contribution
                
                referred_target_per_site = round(accumulative_target)
            
            # Add row to monthly data
            # For future months, use "-" for actual values but keep target values
            row = {
                'Month': month,
                'Open Sites - Actual': '-' if is_future_month else open_sites_actual,
                'Open Sites - Target': sites_target,
                'Referred - Actual': '-' if is_future_month else referred_actual,
                'Referred - Target (0.25/site)': referred_target_per_site,
                'Referred - Target (projected)': projected_target,
                'Referred to pre-screen - Actual': '-' if is_future_month else referred_prescreen_actual,
                'Referred to main trial - Actual': '-' if is_future_month else referred_main_trial_actual,
                'Reviewed - Actual': '-' if is_future_month else reviewed_actual,
                'Recruited to CVLP - Actual': '-' if is_future_month else recruited_cvlp_actual,
                'Consented BNT113-01 (pre-screen) - Actual': '-' if is_future_month else consented_prescreen_actual,
                'Consented BNT113-01 (main trial) - Actual': '-' if is_future_month else consented_main_trial_actual,
                'Randomised BNT113-01 - Actual': '-' if is_future_month else randomised_actual,
                'BNT113-01 Screen Failures - Actual': '-' if is_future_month else screen_failures_actual
            }
            table_data.append(row)
    
    # Create DataFrame
    df_monthly = pd.DataFrame(table_data)
    
    # Custom formatter function that handles both numbers and "-"
    def format_actual_values(val):
        if isinstance(val, str) and val == '-':
            return '-'
        try:
            return '{:.0f}'.format(float(val))
        except:
            return str(val)
    
    # Display the table with styling
    styled_table = df_monthly.style.format({
        'Open Sites - Target': '{:.0f}',
        'Referred - Target (0.25/site)': '{:.1f}',
        'Referred - Target (projected)': '{:.0f}',
        'Open Sites - Actual': format_actual_values,
        'Referred - Actual': format_actual_values,
        'Referred to pre-screen - Actual': format_actual_values,
        'Referred to main trial - Actual': format_actual_values,
        'Reviewed - Actual': format_actual_values,
        'Recruited to CVLP - Actual': format_actual_values,
        'Consented BNT113-01 (pre-screen) - Actual': format_actual_values,
        'Consented BNT113-01 (main trial) - Actual': format_actual_values,
        'Randomised BNT113-01 - Actual': format_actual_values,
        'BNT113-01 Screen Failures - Actual': format_actual_values
    }).set_properties(**{
        'text-align': 'center',
        'padding': '14px 18px',
        'border': '1px solid #e8f4fd',
        'font-size': '13px',
        'font-weight': '500',
        'font-family': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif'
    }).set_table_styles([
        # Modern gradient header
        {'selector': 'thead th', 'props': [
            ('background', 'linear-gradient(135deg, #4472C4 0%, #3b5ba5 100%)'),
            ('color', 'white'),
            ('font-weight', '600'),
            ('text-align', 'center'),
            ('border', 'none'),
            ('padding', '16px 12px'),
            ('font-size', '12px'),
            ('text-transform', 'uppercase'),
            ('letter-spacing', '0.5px'),
            ('box-shadow', '0 2px 4px rgba(68, 114, 196, 0.2)'),
            ('font-family', 'Inter, -apple-system, BlinkMacSystemFont, sans-serif')
        ]},
        # Zebra striping with better contrast
        {'selector': 'tbody tr:nth-child(even)', 'props': [
            ('background-color', '#f8fbfc')
        ]},
        {'selector': 'tbody tr:nth-child(odd)', 'props': [
            ('background-color', '#ffffff')
        ]},
        # Hover effects
        {'selector': 'tbody tr:hover', 'props': [
            ('background-color', '#e3f2fd'),
            ('transform', 'scale(1.005)'),
            ('transition', 'all 0.2s ease'),
            ('box-shadow', '0 2px 8px rgba(68, 114, 196, 0.15)')
        ]},
        # Table container
        {'selector': 'table', 'props': [
            ('border-collapse', 'separate'),
            ('border-spacing', '0'),
            ('border-radius', '10px'),
            ('overflow', 'hidden'),
            ('box-shadow', '0 4px 20px rgba(0, 0, 0, 0.08)'),
            ('margin', '20px 0'),
            ('width', '100%'),
            ('font-family', 'Inter, -apple-system, BlinkMacSystemFont, sans-serif')
        ]},
        # Better cell borders
        {'selector': 'td, th', 'props': [
            ('border-bottom', '1px solid #e8f4fd'),
            ('border-right', '1px solid #e8f4fd')
        ]},
        {'selector': 'td:last-child, th:last-child', 'props': [
            ('border-right', 'none')
        ]},
        {'selector': 'tbody tr:last-child td', 'props': [
            ('border-bottom', 'none')
        ]}
    ])
    
    # Display the table with enhanced container
    st.markdown("""
    <div style="margin: 30px 0; padding: 25px; background: linear-gradient(135deg, #f8fbff 0%, #e8f4fd 100%); border-radius: 12px; border: 1px solid #d1e7fd; box-shadow: 0 4px 15px rgba(68, 114, 196, 0.1);">
    """, unsafe_allow_html=True)
    
    st.write(styled_table.to_html(escape=False, table_uuid="monthly_projections"), unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add data extraction info (only show for internal users)
    if st.session_state.admin_settings['show_debug_info']:
        st.info(f"""
    **Data Extraction Summary:**
            - ✅ **Open Sites - Actual**: Count of sites with Go‑Live/Green‑light date on or before month end
                - Source: 'CVLP Site Data' sheet → Go‑Live/Green‑light (fallback: Site Active/Open Date)
                - Logic: Sites counted once their Go‑Live (or fallback) date is reached
    - ✅ **Referred - Actual**: COUNT(patients WHERE (prescreen_referral_date <= month_end OR main_trial_referral_date <= month_end))
    - ✅ **Referred - Target (0.25/site)**: ACCUMULATIVE target - sum of monthly targets (each month = previous_month_actual_sites × 0.25)
    - ✅ **Referred - Target (projected)**: Static projections from Excel
    - ✅ **All other metrics**: Extracted from real Excel data columns
    - ⚠️ **Reviewed - Actual**: Set to 0 (requires screening log data not available)
    """)
    
    # Add summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_target_sites = site_targets[-1]
        create_enhanced_metric_card(
            icon="🏥",
            label="Target Sites (End)",
            value=str(total_target_sites),
            subtitle="Final target",
            color=COLOR_PALETTE['info']
        )
    
    with col2:
        total_referred_target = projected_targets[-1]
        create_enhanced_metric_card(
            icon="📊",
            label="Cumulative Referred Target",
            value=str(total_referred_target),
            subtitle="By Nov-26",
            color=COLOR_PALETTE['primary']
        )
    
    with col3:
        monthly_rate = 0.25
        create_enhanced_metric_card(
            icon="📈",
            label="Target Rate",
            value=f"{monthly_rate}/site/month",
            subtitle="Referral rate",
            color=COLOR_PALETTE['warning']
        )
    
    with col4:
        months_tracked = len(months)
        create_enhanced_metric_card(
            icon="📅",
            label="Tracking Period",
            value=f"{months_tracked} months",
            subtitle="Apr-25 to Nov-26",
            color=COLOR_PALETTE['success']
        )

    # Add Figure 1 - Monthly referral chart
    if st.session_state.admin_settings['show_monthly_charts']:
        st.markdown("---")
    st.markdown("""
    <div class="section-header fade-in">
        📈 Monthly BNT113-01 Referral Totals vs Projections/Target
    </div>
    """, unsafe_allow_html=True)
    
    # Add informational note about actual data filtering (only show for internal users)
    if st.session_state.admin_settings['show_debug_info']:
        st.info("💡 **Note:** The red 'Actual' line only shows data up to the current month, while projected targets show the full timeline.")
    
    if not df_monthly.empty:
        # Get current month for filtering actual data
        current_date = pd.Timestamp.now()
        current_month_str = current_date.strftime('%b-%y')  # e.g., 'Jan-25'
        
        # Create chart data for plotting
        chart_data = []
        
        for _, row in df_monthly.iterrows():
            month = row['Month']
            
            # Parse the month to compare with current month
            try:
                # Convert month string (e.g., 'Apr-25') to datetime for comparison
                month_date = pd.to_datetime(f"01-{month}", format='%d-%b-%y')
                
                # Add actual referrals data point only up to current month
                if month_date <= current_date:
                    chart_data.append({
                        'Month': month,
                        'Value': row['Referred - Actual'],
                        'Type': 'Actual',
                        'Series': 'Actual'
                    })
                else:
                    # For future months, show actual as None/NaN
                    chart_data.append({
                        'Month': month,
                        'Value': None,
                        'Type': 'Actual',
                        'Series': 'Actual'
                    })
            except:
                # If parsing fails, include the data point
                chart_data.append({
                    'Month': month,
                    'Value': row['Referred - Actual'],
                    'Type': 'Actual',
                    'Series': 'Actual'
                })
            
            # Add projected target data point (always show full timeline)
            chart_data.append({
                'Month': month,
                'Value': row['Referred - Target (projected)'],
                'Type': 'Target (Projected)',
                'Series': 'Target (Projected)'
            })
            
            # Add 0.25/site target data point (always show full timeline)
            chart_data.append({
                'Month': month,
                'Value': row['Referred - Target (0.25/site)'],
                'Type': 'Target (0.25/site)',
                'Series': 'Target (0.25/site)'
            })
        
        # Create DataFrame for plotting
        chart_df = pd.DataFrame(chart_data)
        
        # Remove rows where Value is None/NaN for Actual series
        chart_df = chart_df.dropna(subset=['Value'])
        
        # Create the line chart
        fig_referrals = px.line(
            chart_df,
            x='Month',
            y='Value',
            color='Series',
            title='Monthly BNT113-01 Referral Totals vs Projections/Target',
            markers=True,
            color_discrete_map={
                'Actual': '#d32f2f',  # Red for actual
                'Target (Projected)': '#9e9e9e',  # Gray for projected target
                'Target (0.25/site)': '#ff9800'  # Orange for 0.25/site target
            }
        )
        
        # Customize the chart layout
        fig_referrals.update_layout(
            xaxis_title='Month',
            yaxis_title='Number of Referrals',
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis={'tickangle': 45},
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                title="CVLP - Referrals & Projections"
            ),
            hovermode='x unified'
        )
        
        # Add grid lines
        fig_referrals.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
        fig_referrals.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
        
        # Display the chart
        st.plotly_chart(fig_referrals, use_container_width=True)
        
        # Add chart interpretation
        # Get the latest actual data (up to current month)
        current_date = pd.Timestamp.now()
        current_month_str = current_date.strftime('%b-%y')
        
        # Find the latest actual data point (up to current month)
        latest_actual = 0
        latest_actual_month = "N/A"
        for _, row in df_monthly.iterrows():
            try:
                month_date = pd.to_datetime(f"01-{row['Month']}", format='%d-%b-%y')
                if month_date <= current_date and row['Referred - Actual'] > 0:
                    latest_actual = row['Referred - Actual']
                    latest_actual_month = row['Month']
            except:
                pass
        
        latest_projected = df_monthly['Referred - Target (projected)'].iloc[-1] if len(df_monthly) > 0 else 0
        latest_site_target = df_monthly['Referred - Target (0.25/site)'].iloc[-1] if len(df_monthly) > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        
        # Only show target comparison metrics if not in privacy mode
        if not st.session_state.privacy_mode:
            with col1:
                if latest_projected > 0:
                    vs_projected = (latest_actual / latest_projected) * 100
                    create_enhanced_metric_card(
                        icon="📊",
                        label="vs Projected Target",
                        value=f"{vs_projected:.1f}%",
                        subtitle=f"{latest_actual}/{latest_projected} (as of {latest_actual_month})",
                        color=COLOR_PALETTE['success'] if vs_projected >= 80 else COLOR_PALETTE['warning'] if vs_projected >= 50 else COLOR_PALETTE['danger']
                    )
                else:
                    create_enhanced_metric_card(
                        icon="📊",
                        label="vs Projected Target",
                        value="N/A",
                        subtitle="No target set",
                        color=COLOR_PALETTE['text_muted']
                    )
            
            with col2:
                if latest_site_target > 0:
                    vs_site_target = (latest_actual / latest_site_target) * 100
                    create_enhanced_metric_card(
                        icon="🏥",
                        label="vs Site-based Target",
                        value=f"{vs_site_target:.1f}%",
                        subtitle=f"{latest_actual}/{latest_site_target:.1f} (as of {latest_actual_month})",
                        color=COLOR_PALETTE['success'] if vs_site_target >= 80 else COLOR_PALETTE['warning'] if vs_site_target >= 50 else COLOR_PALETTE['danger']
                    )
                else:
                    create_enhanced_metric_card(
                        icon="🏥",
                        label="vs Site-based Target",
                        value="N/A",
                        subtitle="No sites active",
                        color=COLOR_PALETTE['text_muted']
                    )
            
            with col3:
                # Count months with actual data (up to current month)
                months_with_data = 0
                for _, row in df_monthly.iterrows():
                    try:
                        month_date = pd.to_datetime(f"01-{row['Month']}", format='%d-%b-%y')
                        if month_date <= current_date and row['Referred - Actual'] > 0:
                            months_with_data += 1
                    except:
                        pass
                
                total_months_to_date = len([m for m in df_monthly['Month'] if pd.to_datetime(f"01-{m}", format='%d-%b-%y', errors='coerce') <= current_date])
                
                # Only show data coverage metric for internal users
                if st.session_state.admin_settings['show_debug_info']:
                    create_enhanced_metric_card(
                        icon="📅",
                        label="Data Coverage",
                        value=f"{months_with_data}/{total_months_to_date}",
                        subtitle=f"Months with referrals (up to {current_month_str})",
                        color=COLOR_PALETTE['info']
                    )
    
    else:
        st.warning("No monthly data available for chart generation")

    # --- NEW: User-selectable metrics visualization ---
    if st.session_state.admin_settings['show_monthly_trends']:
        st.markdown("### 📊 Visualize Monthly Metrics Trends")
    if not df_monthly.empty:
        # Exclude Month column for selection
        metric_options = [col for col in df_monthly.columns if col != 'Month']
        selected_metrics = st.multiselect(
            "Select monthly metrics to visualize:",
            options=metric_options,
            default=[metric_options[0]] if metric_options else []
        )
        if selected_metrics:
            # Filter data for visualization - actual metrics only show up to current month
            current_date = pd.Timestamp.now()
            df_for_viz = df_monthly.copy()
            
            # Get current month in the format used in the data (e.g., 'Dec-25')
            current_month_str = current_date.strftime('%b-%y')
            
            # Find the index of current month or closest past month
            current_month_idx = None
            for idx, month in enumerate(df_monthly['Month']):
                try:
                    month_date = pd.to_datetime(f"01-{month}", format='%d-%b-%y')
                    if month_date <= current_date:
                        current_month_idx = idx
                    else:
                        break
                except:
                    continue
            
            # Convert selected metrics to numeric, handling "-" strings
            for metric in selected_metrics:
                if metric in df_for_viz.columns:
                    # Convert "-" to None, then to numeric
                    df_for_viz[metric] = df_for_viz[metric].apply(
                        lambda x: None if (isinstance(x, str) and x == '-') else x
                    )
                    df_for_viz[metric] = pd.to_numeric(df_for_viz[metric], errors='coerce')
            
            # For each selected metric, filter actual data to current month
            for metric in selected_metrics:
                if 'Actual' in metric and current_month_idx is not None:
                    # Set future actual values to NaN so they don't show on the chart
                    df_for_viz.loc[current_month_idx + 1:, metric] = None
            
            fig_metrics = px.line(
                df_for_viz,
                x='Month',
                y=selected_metrics,
                markers=True,
                title='Monthly Trends for Selected Metrics'
            )
            fig_metrics.update_layout(
                xaxis_title='Month',
                yaxis_title='Value',
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis={'tickangle': 45},
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                    title="Metrics"
                ),
                hovermode='x unified'
            )
            st.plotly_chart(fig_metrics, use_container_width=True)
            
            # Add explanation about actual data filtering (only show for internal users)
            if st.session_state.admin_settings['show_debug_info']:
                actual_metrics_selected = [m for m in selected_metrics if 'Actual' in m]
                if actual_metrics_selected:
                    st.info(f"📅 **Note**: 'Actual' metrics only show data up to the current month ({current_month_str}). Future months cannot have actual data yet.")
        else:
            st.info("Select at least one metric to visualize trends.")
    
    # Add CVLP Recruitment/Referrals Against Sites Chart
    st.markdown("### 📊 CVLP Recruitment/Referrals Against Sites")
    if not df_monthly.empty:
        # Prepare data for visualization - convert "-" to None for proper plotting
        current_date = pd.Timestamp.now()
        df_combo_viz = df_monthly.copy()
        
        # Convert "-" strings to None for proper plotting, but preserve numeric values
        for col in ['Open Sites - Actual', 'Recruited to CVLP - Actual', 'Referred - Actual']:
            if col in df_combo_viz.columns:
                df_combo_viz[col] = df_combo_viz[col].apply(
                    lambda x: None if (isinstance(x, str) and x == '-') else x
                )
        
        # Ensure all numeric columns are properly converted to numeric type
        numeric_cols = ['Open Sites - Actual', 'Open Sites - Target', 'Referred - Target (0.25/site)', 'Referred - Actual']
        for col in numeric_cols:
            if col in df_combo_viz.columns:
                # Only convert if not already None
                df_combo_viz[col] = df_combo_viz[col].apply(
                    lambda x: None if x is None else (pd.to_numeric(x, errors='coerce') if pd.notna(x) else None)
                )
        
        # Create the combination chart using plotly graph objects for dual y-axes
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        
        # Create subplot with secondary y-axis
        fig_combo = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Filter out None/NaN values for each trace
        # Open Sites - only valid values
        open_sites_mask = df_combo_viz['Open Sites - Actual'].notna()
        
        # Add Open Sites bars (right y-axis)
        fig_combo.add_trace(
            go.Bar(
                x=df_combo_viz.loc[open_sites_mask, 'Month'],
                y=df_combo_viz.loc[open_sites_mask, 'Open Sites - Actual'],
                name='Open Sites',
                marker_color='#4CAF50',
                opacity=0.7,
                text=df_combo_viz.loc[open_sites_mask, 'Open Sites - Actual'],
                textposition='outside',
                texttemplate='%{text}',
                yaxis='y2'
            ),
            secondary_y=True
        )
        
        # Site Opening Trajectory - only valid values
        trajectory_mask = df_combo_viz['Open Sites - Target'].notna()
        
        # Add Site Opening Trajectory line (right y-axis) 
        fig_combo.add_trace(
            go.Scatter(
                x=df_combo_viz.loc[trajectory_mask, 'Month'],
                y=df_combo_viz.loc[trajectory_mask, 'Open Sites - Target'],
                mode='lines',
                name='Site Opening Trajectory',
                line=dict(color='#2196F3', width=2, dash='dot'),
                yaxis='y2'
            ),
            secondary_y=True
        )
        
        # Referral Target - only valid values
        target_mask = df_combo_viz['Referred - Target (0.25/site)'].notna()
        
        # Add Referral Target line (left y-axis)
        fig_combo.add_trace(
            go.Scatter(
                x=df_combo_viz.loc[target_mask, 'Month'],
                y=df_combo_viz.loc[target_mask, 'Referred - Target (0.25/site)'],
                mode='lines+markers',
                name='Referral Target (0.25/site)',
                line=dict(color='#FF5722', width=3, dash='dash'),
                marker=dict(size=6),
                showlegend=True,
                yaxis='y'
            ),
            secondary_y=False
        )
        
        # Referred - only valid values
        referred_mask = df_combo_viz['Referred - Actual'].notna()
        
        # Add Referred line (left y-axis)
        fig_combo.add_trace(
            go.Scatter(
                x=df_combo_viz.loc[referred_mask, 'Month'],
                y=df_combo_viz.loc[referred_mask, 'Referred - Actual'],
                mode='lines+markers',
                name='Referred',
                line=dict(color='#9C27B0', width=3),
                marker=dict(size=6),
                showlegend=True,
                yaxis='y'
            ),
            secondary_y=False
        )
        
        # Update layout
        fig_combo.update_layout(
            title='CVLP Recruitment/Referrals Against Sites',
            xaxis_title='Month',
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis={'tickangle': 45},
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            ),
            hovermode='x unified'
        )
        
        # Set y-axes titles
        fig_combo.update_yaxes(title_text="Referrals", secondary_y=False)
        fig_combo.update_yaxes(title_text="Number of Sites", secondary_y=True)
        
        # Set y-axis ranges as requested
        fig_combo.update_yaxes(range=[0, 120], secondary_y=False)  # Left axis for referrals
        fig_combo.update_yaxes(range=[0, 30], secondary_y=True)   # Right axis for sites
        
        st.plotly_chart(fig_combo, use_container_width=True)
        
        # Add explanation (only show for internal users)
        if st.session_state.admin_settings['show_debug_info']:
            current_month_str = current_date.strftime('%b-%y')
        st.info(f"📅 **Note**: This chart shows actual data up to the current month ({current_month_str}). Green bars show open sites, blue dotted line shows site opening trajectory, purple line shows actual referrals, and dashed red line shows referral targets (0.25 patients per site per month).")
    else:
        st.info("📁 Please upload your Excel file to view the CVLP Recruitment/Referrals chart.")
    
    return df_monthly

# Call the functions to display the tables (only if we have data)
if st.session_state.admin_settings['show_monthly_table']:
    if not master_df.empty and uploaded_master_file is not None:
        df_monthly = create_monthly_projections_table(processed_df, uploaded_master_file)
    else:
        df_monthly = pd.DataFrame()  # Empty DataFrame if no data
        st.info("📁 Please upload your Excel file using the sidebar to view the Monthly Trial Metrics Table.")
else:
    df_monthly = pd.DataFrame()  # Empty DataFrame if section is hidden

# Trial Referral Reporting Section
if st.session_state.admin_settings['show_trial_referral_reporting']:
    st.markdown("""
    <div class="section-divider">
        <div class="section-divider-icon">📋</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        📊 Trial Referral Reporting
    </div>
    """, unsafe_allow_html=True)

def create_trial_referral_reporting_table(master_df):
    """Create a comprehensive trial referral reporting table showing metrics by trial site"""
    st.markdown("### Trial Referral Reporting")
    
    if master_df.empty:
        st.info("📁 Please upload your Excel file to view the Trial Referral Reporting.")
        return
    
    # Get trial site column
    trial_site_col = 'Trial Site'
    if trial_site_col not in master_df.columns:
        # Try alternative column names
        possible_trial_site_cols = [
            'Please choose the Trial site from the drop down',
            'trial site',
            'Trial site',
            'Referring Site',
            'Site',
            'Hospital',
            'Hospital Site'
        ]
        for col in possible_trial_site_cols:
            if col in master_df.columns:
                trial_site_col = col
                break

    # If still not found, try to use CVLP Site as fallback for demo data
    if trial_site_col not in master_df.columns:
        if 'CVLP Site' in master_df.columns:
            trial_site_col = 'CVLP Site'
            st.info("ℹ️ Using 'CVLP Site' as Trial Site column (demo data fallback)")
        else:
            st.error(f"**Debug**: Trial Site column not found. Total columns: {len(master_df.columns)}")
            st.error(f"Available columns containing 'site' or 'trial':")
            site_related_cols = [col for col in master_df.columns if 'site' in str(col).lower() or 'trial' in str(col).lower()]
            if site_related_cols:
                for col in site_related_cols[:10]:
                    st.text(f"  - {col}")
            else:
                st.text("  - No columns containing 'site' or 'trial' found")
                st.text("All columns:")
                for col in list(master_df.columns)[:20]:  # Show first 20 columns
                    st.text(f"  - {col}")
            return
    
    # Get unique trial sites, filtering out placeholders
    trial_sites = master_df[trial_site_col].dropna().unique()
    trial_sites = [site for site in trial_sites if str(site).strip() != '' and 
                  'enter' not in str(site).lower() and 
                  'placeholder' not in str(site).lower()]
    
    if len(trial_sites) == 0:
        st.warning("No valid trial sites found in the data")
        return
    
    # Define months for the reporting period (Contract ends Nov-26)
    months = ['May-25', 'Jun-25', 'Jul-25', 'Aug-25', 'Sep-25', 'Oct-25', 'Nov-25', 'Dec-25', 
              'Jan-26', 'Feb-26', 'Mar-26', 'Apr-26', 'May-26', 'Jun-26', 'Jul-26', 'Aug-26', 
              'Sep-26', 'Oct-26', 'Nov-26']
    
    # Define date columns mapping
    date_columns = {
        'prescreen_referral': None,
        'main_trial_referral': None,
        'cvlp_consent': None,
        'prescreen_consent': None,
        'main_trial_consent': None,
        'randomisation': None
    }
    
    # Auto-detect date columns based on your actual column names
    for col in master_df.columns:
        col_lower = str(col).lower()
        if 'pre-screening referral form was sent' in col_lower:
            date_columns['prescreen_referral'] = col
        elif 'main trial screening referral form was sent' in col_lower:
            date_columns['main_trial_referral'] = col
        elif 'cvlp' in col_lower and ('consent' in col_lower or 'recruited' in col_lower):
            date_columns['cvlp_consent'] = col
        elif 'pre' in col_lower and 'screen' in col_lower and 'consent' in col_lower:
            date_columns['prescreen_consent'] = col
        elif 'main' in col_lower and 'trial' in col_lower and 'consent' in col_lower:
            date_columns['main_trial_consent'] = col
        elif ('enrolled = yes' in col_lower or 'enrolled = Yes' in col_lower or 'enrolled' in col_lower) and ('screen fail' in col_lower):
            date_columns['randomisation'] = col
        elif 'trial site acknowledged pre-screening referral' in col_lower:
            date_columns['prescreen_acknowledgment'] = col
        elif 'consent confirmed' in col_lower or 'screen fail' in col_lower:
            date_columns['consent_confirmation'] = col
    

    
    # Create table data
    table_data = []
    
    for site in sorted(trial_sites):
        # Filter data for this trial site
        site_df = master_df[master_df[trial_site_col] == site].copy()
        
        if site_df.empty:
            continue
        
        # Calculate total metrics for this site
        total_referrals = 0
        total_pre_screening = 0
        total_main_trial = 0
        total_patients = 0
        total_pre_screening_consents = 0
        total_main_trial_consents = 0
        awaiting_consent = 0
        total_randomised = 0
        drop_out = 0
        
        # Calculate totals using unique patient logic (OR logic, not additive)
        
        # Initialize boolean masks for referrals
        prescreen_referral_mask = pd.Series(False, index=site_df.index)
        main_trial_referral_mask = pd.Series(False, index=site_df.index)
        
        if date_columns['prescreen_referral'] and date_columns['prescreen_referral'] in master_df.columns:
            prescreen_referral_mask = pd.to_datetime(site_df[date_columns['prescreen_referral']], errors='coerce').notna()
            total_pre_screening = prescreen_referral_mask.sum()
        
        if date_columns['main_trial_referral'] and date_columns['main_trial_referral'] in master_df.columns:
            main_trial_referral_mask = pd.to_datetime(site_df[date_columns['main_trial_referral']], errors='coerce').notna()
            total_main_trial = main_trial_referral_mask.sum()
        
        # Total referrals = unique patients with EITHER pre-screening OR main trial referral (or both)
        total_referrals = (prescreen_referral_mask | main_trial_referral_mask).sum()
        
        # Initialize boolean masks for consents
        prescreen_consent_mask = pd.Series(False, index=site_df.index)
        main_trial_consent_mask = pd.Series(False, index=site_df.index)
        
        if date_columns['prescreen_consent'] and date_columns['prescreen_consent'] in master_df.columns:
            prescreen_consent_mask = site_df[date_columns['prescreen_consent']].astype(str).str.strip().str.lower().isin(['yes', 'y', 'true'])
            total_pre_screening_consents = prescreen_consent_mask.sum()
        
        if date_columns['main_trial_consent'] and date_columns['main_trial_consent'] in master_df.columns:
            main_trial_consent_mask = site_df[date_columns['main_trial_consent']].astype(str).str.strip().str.lower().isin(['yes', 'y', 'true'])
            total_main_trial_consents = main_trial_consent_mask.sum()
        
        # Total patients = unique patients with EITHER pre-screening OR main trial consent (or both)
        total_patients = (prescreen_consent_mask | main_trial_consent_mask).sum()
        
        if date_columns['randomisation'] and date_columns['randomisation'] in master_df.columns:
            total_randomised = site_df[date_columns['randomisation']].astype(str).str.strip().str.lower().isin(['yes', 'y', 'true']).sum()
        
        total_patients = total_pre_screening_consents + total_main_trial_consents
        awaiting_consent = total_referrals - total_patients
        
        # Create row with totals
        row = {
            'Trial Site': site,
            'Total Referrals': total_referrals,
            'Total Pre-Screening Referrals': total_pre_screening,
            'Total Main Trial Referrals': total_main_trial,
            'Total Patients': total_patients,
            'Total Pre-Screening Consents': total_pre_screening_consents,
            'Total Main Trial Consents': total_main_trial_consents,
            'Awaiting Consent': awaiting_consent,
            'Total Randomised': total_randomised,
            'Drop Out': drop_out  # This would need specific logic based on your data
        }
        
        # Add monthly breakdown
        for month in months:
            # Parse month to get start and end dates
            try:
                month_parts = month.split('-')
                month_num = {
                    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                    'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
                }[month_parts[0]]
                year = int('20' + month_parts[1])
                
                # Get start and end of month
                from datetime import datetime
                import calendar
                start_date = datetime(year, month_num, 1)
                last_day = calendar.monthrange(year, month_num)[1]
                end_date = datetime(year, month_num, last_day, 23, 59, 59)
                
                # Count referrals for this month
                monthly_referrals = 0
                
                # Count pre-screen referrals for this month
                if date_columns['prescreen_referral'] and date_columns['prescreen_referral'] in master_df.columns:
                    prescreen_dates = pd.to_datetime(site_df[date_columns['prescreen_referral']], errors='coerce')
                    monthly_referrals += len(prescreen_dates[(prescreen_dates >= start_date) & (prescreen_dates <= end_date)])
                
                # Count main trial referrals for this month
                if date_columns['main_trial_referral'] and date_columns['main_trial_referral'] in master_df.columns:
                    main_trial_dates = pd.to_datetime(site_df[date_columns['main_trial_referral']], errors='coerce')
                    monthly_referrals += len(main_trial_dates[(main_trial_dates >= start_date) & (main_trial_dates <= end_date)])
                
                row[month] = monthly_referrals
                
            except:
                row[month] = 0
        
        table_data.append(row)
    
    # Create DataFrame
    df_trial_referral = pd.DataFrame(table_data)
    
    if df_trial_referral.empty:
        st.warning("No trial referral data available")
        return
    
    # Define column order with shorter names for better display
    summary_columns = [
        'Trial Site', 'Total Referrals', 'Total Pre-Screening Referrals', 'Total Main Trial Referrals',
        'Total Patients', 'Total Pre-Screening Consents', 'Total Main Trial Consents',
        'Awaiting Consent', 'Total Randomised', 'Drop Out'
    ]
    
    display_columns = summary_columns + months
    available_columns = [col for col in display_columns if col in df_trial_referral.columns]
    display_df = df_trial_referral[available_columns].copy()
    
    # Create much shorter column names for better display
    column_mapping = {
        'Trial Site': 'Site',
        'Total Referrals': 'Total Ref', 
        'Total Pre-Screening Referrals': 'Pre-Screen Ref',
        'Total Main Trial Referrals': 'Main Trial Ref', 
        'Total Patients': 'Patients',
        'Total Pre-Screening Consents': 'Pre-Screen Cons',
        'Total Main Trial Consents': 'Main Trial Cons',
        'Awaiting Consent': 'Awaiting',
        'Total Randomised': 'Randomised',
        'Drop Out': 'Drop Out'
    }
    
    # Apply column name mapping
    display_df = display_df.rename(columns=column_mapping)
    
    # Apply styling similar to your reference image
    def style_trial_referral_table(df):
        def apply_colors(row):
            colors = []
            for i, col in enumerate(df.columns):
                if col == 'Site':
                    colors.append('background-color: #f0f0f0; font-weight: bold')
                elif col == 'Total Ref':
                    colors.append('background-color: #E3F2FD; color: #1976D2')
                elif 'Pre-Screen' in col:
                    colors.append('background-color: #E8F5E8; color: #2E7D32')
                elif 'Main Trial' in col:
                    colors.append('background-color: #FFF3E0; color: #F57C00')
                elif col == 'Patients':
                    colors.append('background-color: #F3E5F5; color: #7B1FA2')
                elif col == 'Awaiting':
                    colors.append('background-color: #FFEBEE; color: #C62828')
                elif col == 'Randomised':
                    colors.append('background-color: #E8F5E8; color: #2E7D32')
                elif col == 'Drop Out':
                    colors.append('background-color: #FFCDD2; color: #D32F2F')
                elif col in months:
                    # Highlight current month
                    current_month = pd.Timestamp.now().strftime('%b-%y')
                    if col == current_month:
                        colors.append('background-color: #FFEB3B; color: #F57F17; font-weight: bold')
                    else:
                        colors.append('background-color: #FAFAFA')
                else:
                    colors.append('')
            return colors
        
        return df.style.apply(apply_colors, axis=1)
    
    
    # Display the styled table - clean approach
    styled_table = style_trial_referral_table(display_df)
    st.dataframe(
        styled_table,
        use_container_width=True,
        height=400
    )
    
    # Add summary metrics
    if st.session_state.admin_settings['show_referral_visualizations']:
        st.markdown("### 📈 Trial Referral Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sites = len(df_trial_referral)
        create_enhanced_metric_card(
            icon="🏥",
            label="Total Trial Sites",
            value=str(total_sites),
            subtitle="Active sites",
            color=COLOR_PALETTE['info']
        )
    
    with col2:
        total_referrals = df_trial_referral['Total Referrals'].sum()
        create_enhanced_metric_card(
            icon="📋",
            label="Total Referrals",
            value=str(total_referrals),
            subtitle="All referrals",
            color=COLOR_PALETTE['primary']
        )
    
    with col3:
        total_patients = df_trial_referral['Total Patients'].sum()
        create_enhanced_metric_card(
            icon="👥",
            label="Total Patients",
            value=str(total_patients),
            subtitle="Consented patients",
            color=COLOR_PALETTE['success']
        )
    
    with col4:
        total_randomised = df_trial_referral['Total Randomised'].sum()
        create_enhanced_metric_card(
            icon="🎲",
            label="Total Randomised",
            value=str(total_randomised),
            subtitle="Randomised patients",
            color=COLOR_PALETTE['chart_9']
        )
    
    # Add visualizations
    if st.session_state.admin_settings['show_referral_visualizations']:
        st.markdown("### 📊 Trial Referral Visualizations")
    
    # Create two columns for charts
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### Total Referrals by Trial Site")
        # Create horizontal bar chart
        fig_horizontal = px.bar(
            df_trial_referral.sort_values('Total Referrals', ascending=True),
            x='Total Referrals',
            y='Trial Site',
            orientation='h',
            title='Total Referrals by Trial Site',
            text='Total Referrals'
        )
        fig_horizontal.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(l=150, r=50, t=50, b=50)
        )
        fig_horizontal.update_traces(
            texttemplate='%{text}', 
            textposition='outside',
            marker_color='#2196F3'
        )
        st.plotly_chart(fig_horizontal, use_container_width=True)
    
    with chart_col2:
        st.markdown("#### Monthly Referrals by Trial Site")
        # Prepare data for stacked bar chart by month
        monthly_data = []
        for _, row in df_trial_referral.iterrows():
            for month in months:
                if month in row and row[month] > 0:
                    monthly_data.append({
                        'Month': month,
                        'Trial Site': row['Trial Site'],
                        'Referrals': row[month]
                    })
        
        if monthly_data:
            monthly_df = pd.DataFrame(monthly_data)
            
            # Create stacked bar chart
            fig_monthly = px.bar(
                monthly_df,
                x='Month',
                y='Referrals',
                color='Trial Site',
                title='Monthly Referrals by Trial Site',
                text='Referrals'
            )
            fig_monthly.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis={'tickangle': 45},
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=1,
                    xanchor="left",
                    x=1.02
                )
            )
            fig_monthly.update_traces(texttemplate='%{text}', textposition='inside')
            st.plotly_chart(fig_monthly, use_container_width=True)
        else:
            st.info("No monthly referral data available for visualization")
    
    # Add detailed breakdown chart
    if st.session_state.admin_settings['show_referral_breakdown']:
        st.markdown("#### 📈 Referral Metrics Breakdown by Trial Site")
    
    # Create a comprehensive comparison chart
    metrics_for_chart = ['Total Referrals', 'Total Pre-Screening Referrals', 'Total Main Trial Referrals', 'Total Patients', 'Total Randomised']
    available_metrics = [col for col in metrics_for_chart if col in df_trial_referral.columns]
    
    if available_metrics:
        # Prepare data for grouped bar chart
        chart_data = []
        for _, row in df_trial_referral.iterrows():
            for metric in available_metrics:
                chart_data.append({
                    'Trial Site': row['Trial Site'],
                    'Metric': metric.replace('Total ', ''),
                    'Value': row[metric]
                })
        
        chart_df = pd.DataFrame(chart_data)
        
        fig_comparison = px.bar(
            chart_df,
            x='Trial Site',
            y='Value',
            color='Metric',
            title='Trial Referral Metrics Comparison by Site',
            barmode='group',
            text='Value'
        )
        fig_comparison.update_layout(
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis={'tickangle': 45},
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            )
        )
        fig_comparison.update_traces(texttemplate='%{text}', textposition='outside')
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Add CVLP Site Breakdown by Trial Site
    st.markdown("### 🏥 CVLP Site Breakdown by Trial Site")
    st.markdown("Click on a trial site below to see which CVLP sites the patients come from:")
    
    # Get CVLP site column
    cvlp_site_col = 'CVLP Site'
    if cvlp_site_col not in master_df.columns:
        # Try alternative column names
        possible_cvlp_site_cols = [
            'Please choose the CVLP site from the drop down',
            'CVLP site',
            'CVLP Site Name'
        ]
        for col in possible_cvlp_site_cols:
            if col in master_df.columns:
                cvlp_site_col = col
                break
    
    if cvlp_site_col in master_df.columns:
        for _, row in df_trial_referral.iterrows():
            trial_site_name = row['Trial Site']
            total_referrals = row['Total Referrals']
            
            if total_referrals > 0:
                with st.expander(f"🏥 {trial_site_name} ({total_referrals} referrals)", expanded=False):
                    # Filter data for this trial site
                    trial_site_data = master_df[master_df[trial_site_col] == trial_site_name].copy()
                    
                    if not trial_site_data.empty:
                        # Count patients by CVLP site
                        cvlp_breakdown = trial_site_data[cvlp_site_col].value_counts()
                        cvlp_breakdown = cvlp_breakdown[cvlp_breakdown > 0]  # Only show sites with patients
                        
                        if not cvlp_breakdown.empty:
                            # Create two columns for display
                            breakdown_col1, breakdown_col2 = st.columns([1, 1])
                            
                            with breakdown_col1:
                                if st.session_state.admin_settings['show_cvlp_site_breakdown']:
                                    st.markdown("#### 📊 Patient Count by CVLP Site")
                                # Create a DataFrame for better display
                                breakdown_df = pd.DataFrame({
                                    'CVLP Site': cvlp_breakdown.index,
                                    'Patient Count': cvlp_breakdown.values,
                                    'Percentage': (cvlp_breakdown.values / cvlp_breakdown.sum() * 100).round(1)
                                })
                                
                                # Style the breakdown table
                                def style_breakdown_table(df):
                                    def apply_breakdown_colors(row):
                                        colors = []
                                        for col in df.columns:
                                            if col == 'CVLP Site':
                                                colors.append('background-color: #E3F2FD; font-weight: bold')
                                            elif col == 'Patient Count':
                                                colors.append('background-color: #E8F5E8; text-align: center')
                                            elif col == 'Percentage':
                                                colors.append('background-color: #FFF3E0; text-align: center')
                                            else:
                                                colors.append('')
                                        return colors
                                    return df.style.apply(apply_breakdown_colors, axis=1)
                                
                                styled_breakdown = style_breakdown_table(breakdown_df)
                                st.dataframe(styled_breakdown, use_container_width=True, hide_index=True)
                            
                            with breakdown_col2:
                                if st.session_state.admin_settings['show_cvlp_site_breakdown']:
                                    st.markdown("#### 📈 Visual Breakdown")
                                # Create a pie chart for the breakdown
                                fig_pie = px.pie(
                                    values=cvlp_breakdown.values,
                                    names=cvlp_breakdown.index,
                                    title=f'Patient Distribution for {trial_site_name}',
                                    color_discrete_sequence=px.colors.qualitative.Set3
                                )
                                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                                fig_pie.update_layout(
                                    height=400,
                                    showlegend=True,
                                    legend=dict(
                                        orientation="v",
                                        yanchor="middle",
                                        y=0.5,
                                        xanchor="left",
                                        x=1.02
                                    )
                                )
                                st.plotly_chart(fig_pie, use_container_width=True)
                            
                            # Add detailed patient information
                            st.markdown("#### 📋 Detailed Patient Information")
                            
                            # Create a summary table with referral details
                            detailed_breakdown = []
                            for cvlp_site in cvlp_breakdown.index:
                                cvlp_site_patients = trial_site_data[trial_site_data[cvlp_site_col] == cvlp_site]
                                
                                # Count different types of referrals
                                prescreen_referrals = 0
                                main_trial_referrals = 0
                                
                                if date_columns['prescreen_referral'] and date_columns['prescreen_referral'] in master_df.columns:
                                    prescreen_referrals = pd.to_datetime(cvlp_site_patients[date_columns['prescreen_referral']], errors='coerce').notna().sum()
                                
                                if date_columns['main_trial_referral'] and date_columns['main_trial_referral'] in master_df.columns:
                                    main_trial_referrals = pd.to_datetime(cvlp_site_patients[date_columns['main_trial_referral']], errors='coerce').notna().sum()
                                
                                detailed_breakdown.append({
                                    'CVLP Site': cvlp_site,
                                    'Total Patients': len(cvlp_site_patients),
                                    'Pre-Screen Referrals': prescreen_referrals,
                                    'Main Trial Referrals': main_trial_referrals,
                                    'Percentage of Trial Site': f"{(len(cvlp_site_patients) / len(trial_site_data) * 100):.1f}%"
                                })
                            
                            detailed_df = pd.DataFrame(detailed_breakdown)
                            
                            # Style the detailed table
                            def style_detailed_table(df):
                                def apply_detailed_colors(row):
                                    colors = []
                                    for col in df.columns:
                                        if col == 'CVLP Site':
                                            colors.append('background-color: #f0f0f0; font-weight: bold')
                                        elif 'Referrals' in col:
                                            colors.append('background-color: #E8F5E8; text-align: center')
                                        elif col == 'Total Patients':
                                            colors.append('background-color: #E3F2FD; text-align: center')
                                        elif col == 'Percentage of Trial Site':
                                            colors.append('background-color: #FFF3E0; text-align: center')
                                        else:
                                            colors.append('text-align: center')
                                    return colors
                                return df.style.apply(apply_detailed_colors, axis=1)
                            
                            styled_detailed = style_detailed_table(detailed_df)
                            st.dataframe(styled_detailed, use_container_width=True, hide_index=True)
                        
                        else:
                            st.warning(f"No CVLP site information available for {trial_site_name}")
                    else:
                        st.warning(f"No patient data found for {trial_site_name}")
            else:
                st.info(f"{trial_site_name}: No referrals to show breakdown")
    else:
        st.warning("CVLP Site column not found. Cannot show breakdown by CVLP sites.")
    
    return df_trial_referral

# Call the trial referral reporting function
if not master_df.empty and uploaded_master_file is not None:
    df_trial_referral = create_trial_referral_reporting_table(master_df)
else:
    st.info("📁 Please upload your Excel file to view the Trial Referral Reporting.")

def create_site_based_metrics_table(master_df):
    """Create a comprehensive site-based metrics table showing all trial metrics by site"""
    st.markdown("### Trial Metrics by Site")
    
    # Get all sites from the data
    cvlp_site_col = 'CVLP Site'
    if cvlp_site_col not in master_df.columns:
        # Try alternative column names
        possible_site_cols = [
            'CVLP site', 
            'Please choose the CVLP site from the drop down',
            'Site',
            'CVLP Site Name'
        ]
        for col in possible_site_cols:
            if col in master_df.columns:
                cvlp_site_col = col
                break
    
    # If CVLP Site not found, try to use Trial Site as fallback for demo data
    if cvlp_site_col not in master_df.columns:
        if 'Trial Site' in master_df.columns:
            cvlp_site_col = 'Trial Site'
            st.info("ℹ️ Using 'Trial Site' as CVLP Site column (demo data fallback)")
        else:
            st.error(f"**Debug**: CVLP Site column not found. Available columns containing 'site' or 'CVLP':")
            site_related_cols = [col for col in master_df.columns if 'site' in str(col).lower() or 'cvlp' in str(col).lower()]
            if site_related_cols:
                for col in site_related_cols[:10]:  # Show first 10 matches
                    st.text(f"  - {col}")
            else:
                st.text("  - No columns containing 'site' or 'cvlp' found")
                st.text("All columns:")
                for col in list(master_df.columns)[:20]:  # Show first 20 columns
                    st.text(f"  - {col}")
            st.text(f"Total columns in data: {len(master_df.columns)}")
            return
    
    if cvlp_site_col not in master_df.columns or master_df.empty:
        st.warning("No site data available for metrics calculation")
        return
    
    # Get unique sites from the data, filtering out placeholders
    sites = master_df[cvlp_site_col].dropna().unique()
    sites = [site for site in sites if str(site).strip() != '' and 
             'enter' not in str(site).lower() and 
             'placeholder' not in str(site).lower()]
    
    if len(sites) == 0:
        st.warning("No valid sites found in the data")
        return
    
    # Create the DataFrame structure with actual calculations
    site_data = []
    
    # Define column mappings for easier access
    date_columns = {
        'cvlp_consent': 'Please input the date the patient signed the consent form (dd/mm/yyyy)',
        'prescreen_referral': 'Please input the date the pre-screening referral form was sent to the trial site\n(dd/mm/yyyy)',
        'main_trial_referral': 'Please input the date the main trial screening referral form was sent to the trial site\n(dd/mm/yyyy)',
        'prescreen_consent': 'To be confirmed by trial site (Yes = consent confirmed, No = screen fail)',
        'main_trial_consent': 'To be confirmed by trial site (Yes = consent confirmed, No = screen fail).1',
        'enrollment': 'To be confirmed by trial site (enrolled = Yes, screen fail = No)'
    }
    
    # Screen failure columns
    failure_columns = [
        'Clinical Liaison to confirm screen fail with CVLP site',
        'Email the CVLP site to confirm that patient has not consented to the main trial',
        'Email the CVLP site to confirm that patient has not enrolled to the trial'
    ]
    
    for site in sorted(sites):
        # Filter data for this site
        site_df = master_df[master_df[cvlp_site_col] == site].copy()
        
        if site_df.empty:
            continue
        
        # Calculate metrics for this site
        
        # 1. Site Opening Date (first patient consent to CVLP)
        site_opening_date = "N/A"
        if date_columns['cvlp_consent'] in master_df.columns:
            consent_dates = pd.to_datetime(site_df[date_columns['cvlp_consent']], errors='coerce')
            valid_dates = consent_dates.dropna()
            if not valid_dates.empty:
                site_opening_date = valid_dates.min().strftime('%d-%b-%y')
        
        # 2. Total Referred (unique patients referred to either pre-screen or main trial)
        total_referred = 0
        referred_mask = pd.Series(False, index=site_df.index)
        
        if date_columns['prescreen_referral'] in master_df.columns:
            prescreen_dates = pd.to_datetime(site_df[date_columns['prescreen_referral']], errors='coerce')
            referred_mask = referred_mask | prescreen_dates.notna()
        
        if date_columns['main_trial_referral'] in master_df.columns:
            main_trial_dates = pd.to_datetime(site_df[date_columns['main_trial_referral']], errors='coerce')
            referred_mask = referred_mask | main_trial_dates.notna()
        
        total_referred = referred_mask.sum()
        
        # 3. Referred to pre-screen
        referred_prescreen = 0
        if date_columns['prescreen_referral'] in master_df.columns:
            prescreen_dates = pd.to_datetime(site_df[date_columns['prescreen_referral']], errors='coerce')
            referred_prescreen = prescreen_dates.notna().sum()
        
        # 4. Referred to main trial
        referred_main_trial = 0
        if date_columns['main_trial_referral'] in master_df.columns:
            main_trial_dates = pd.to_datetime(site_df[date_columns['main_trial_referral']], errors='coerce')
            referred_main_trial = main_trial_dates.notna().sum()
        
        # 5. Recruited to CVLP (consented to CVLP)
        recruited_cvlp = 0
        if date_columns['cvlp_consent'] in master_df.columns:
            cvlp_dates = pd.to_datetime(site_df[date_columns['cvlp_consent']], errors='coerce')
            recruited_cvlp = cvlp_dates.notna().sum()
        
        # 6. Consented BNT113-01 (pre-screen)
        consented_prescreen = 0
        if date_columns['prescreen_consent'] in master_df.columns:
            consented_prescreen = site_df[date_columns['prescreen_consent']].astype(str).str.strip().str.lower().isin(['yes', 'y', 'true']).sum()
        
        # 7. Consented BNT113-01 (main trial)
        consented_main_trial = 0
        if date_columns['main_trial_consent'] in master_df.columns:
            consented_main_trial = site_df[date_columns['main_trial_consent']].astype(str).str.strip().str.lower().isin(['yes', 'y', 'true']).sum()
        
        # 8. Randomised BNT113-01
        randomised = 0
        if date_columns['enrollment'] in master_df.columns:
            randomised = site_df[date_columns['enrollment']].astype(str).str.strip().str.lower().isin(['yes', 'y', 'true']).sum()
        
        # 9. Screen Failures
        screen_failures = 0
        failure_mask = pd.Series(False, index=site_df.index)
        for fail_col in failure_columns:
            if fail_col in master_df.columns:
                failure_mask = failure_mask | (~site_df[fail_col].isna())
        screen_failures = failure_mask.sum()
        
        # 10. Calculate key conversion rates
        # CVLP→Referral Rate: How many referred vs recruited to CVLP
        cvlp_to_referral_rate = (total_referred / recruited_cvlp * 100) if recruited_cvlp > 0 else 0
        
        # Referral→Randomisation Rate: Conversion from referral to randomisation
        referral_to_randomisation_rate = (randomised / total_referred * 100) if total_referred > 0 else 0
        
        # Add row to site data (Recruited to CVLP before Total Referred)
        row = {
            'Site': site,
            'Site Opening Date': site_opening_date,
            'Recruited to CVLP': recruited_cvlp,
            'Total Referred': total_referred,
            'Referred to Pre-screen': referred_prescreen,
            'Referred to Main Trial': referred_main_trial,
            'Consented BNT113-01 (Pre-screen)': consented_prescreen,
            'Consented BNT113-01 (Main Trial)': consented_main_trial,
            'Randomised BNT113-01': randomised,
            'Screen Failures': screen_failures,
            'CVLP→Referral Rate (%)': round(cvlp_to_referral_rate, 1),
            'Referral→Randomisation Rate (%)': round(referral_to_randomisation_rate, 1)
        }
        site_data.append(row)
    
    # Create DataFrame
    df_sites = pd.DataFrame(site_data)
    
    if df_sites.empty:
        st.warning("No site metrics data available")
        return
    
    # Enhanced table styling with modern UI/UX
    def highlight_conversion_rates(row):
        """Highlight conversion rate cells based on performance (only CVLP→Referral Rate)"""
        colors = []
        for col in row.index:
            # Only apply color coding to CVLP→Referral Rate (%), not Referral→Randomisation Rate (%)
            if col == 'CVLP→Referral Rate (%)':
                value = row[col] if pd.notna(row[col]) else 0
                if value >= 75:
                    colors.append('background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); color: #155724; font-weight: 600; border-left: 4px solid #28a745;')
                elif value >= 50:
                    colors.append('background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); color: #856404; font-weight: 600; border-left: 4px solid #ffc107;')
                elif value > 0:
                    colors.append('background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); color: #721c24; font-weight: 600; border-left: 4px solid #dc3545;')
                else:
                    colors.append('background-color: #f8f9fa; color: #6c757d;')
            else:
                colors.append('')
        return colors

    styled_table = df_sites.style.apply(highlight_conversion_rates, axis=1).format({
        'Recruited to CVLP': '{:.0f}',
        'Total Referred': '{:.0f}',
        'Referred to Pre-screen': '{:.0f}',
        'Referred to Main Trial': '{:.0f}',
        'Consented BNT113-01 (Pre-screen)': '{:.0f}',
        'Consented BNT113-01 (Main Trial)': '{:.0f}',
        'Randomised BNT113-01': '{:.0f}',
        'Screen Failures': '{:.0f}',
        'CVLP→Referral Rate (%)': '{:.1f}%',
        'Referral→Randomisation Rate (%)': '{:.1f}%'
    }).set_properties(**{
        'text-align': 'center',
        'padding': '12px 16px',
        'border': '1px solid #e8f4fd',
        'font-size': '13px',
        'font-weight': '500'
    }).set_table_styles([
        # Modern gradient header
        {'selector': 'thead th', 'props': [
            ('background', 'linear-gradient(135deg, #28a745 0%, #20c997 100%)'),
            ('color', 'white'),
            ('font-weight', '600'),
            ('text-align', 'center'),
            ('border', 'none'),
            ('padding', '16px 12px'),
            ('font-size', '13px'),
            ('text-transform', 'uppercase'),
            ('letter-spacing', '0.5px'),
            ('box-shadow', '0 2px 4px rgba(40, 167, 69, 0.2)')
        ]},
        # Zebra striping
        {'selector': 'tbody tr:nth-child(even)', 'props': [
            ('background-color', '#f8fbfc')
        ]},
        {'selector': 'tbody tr:nth-child(odd)', 'props': [
            ('background-color', '#ffffff')
        ]},
        # Hover effects
        {'selector': 'tbody tr:hover', 'props': [
            ('background-color', '#e8f5e9'),
            ('transform', 'scale(1.01)'),
            ('transition', 'all 0.2s ease'),
            ('box-shadow', '0 2px 8px rgba(40, 167, 69, 0.15)')
        ]},
        # Table container
        {'selector': 'table', 'props': [
            ('border-collapse', 'separate'),
            ('border-spacing', '0'),
            ('border-radius', '8px'),
            ('overflow', 'hidden'),
            ('box-shadow', '0 4px 20px rgba(0, 0, 0, 0.08)'),
            ('margin', '20px 0'),
            ('width', '100%')
        ]},
        # Better borders
        {'selector': 'td, th', 'props': [
            ('border-bottom', '1px solid #e8f4fd'),
            ('border-right', '1px solid #e8f4fd')
        ]},
        {'selector': 'td:last-child, th:last-child', 'props': [
            ('border-right', 'none')
        ]},
        {'selector': 'tbody tr:last-child td', 'props': [
            ('border-bottom', 'none')
        ]}
    ])

    # Add enhanced container for the table
    st.markdown("""
    <div style="margin: 30px 0 20px 0;">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 15px;">
            <div style="width: 8px; height: 40px; background: linear-gradient(180deg, #28a745, #20c997); border-radius: 4px;"></div>
            <div>
                <h4 style="color: #28a745; font-size: 18px; font-weight: 600; margin: 0;">Conversion Rate Metrics</h4>
                <p style="color: #666; font-size: 13px; margin: 5px 0 0 0;">
                    <span style="background: linear-gradient(135deg, #d4edda, #c3e6cb); padding: 2px 8px; border-radius: 4px; margin-right: 8px; font-size: 11px;">
                        🟢 CVLP→Referral Rate: Referral efficiency per CVLP patient
                    </span>
                    <span style="background: linear-gradient(135deg, #cce5ff, #b3d9ff); padding: 2px 8px; border-radius: 4px; font-size: 11px;">
                        🔵 Referral→Randomisation Rate: Final conversion success
                    </span>
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Display the table with enhanced container
    st.markdown("""
    <div style="margin: 20px 0; padding: 25px; background: linear-gradient(135deg, #f8fffb 0%, #e8f5e9 100%); border-radius: 12px; border: 1px solid #c8e6c9;">
    """, unsafe_allow_html=True)
    
    st.write(styled_table.to_html(escape=False, table_uuid="site_metrics"), unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    # Only show site metrics if not in privacy mode
    if not st.session_state.privacy_mode:
        with col1:
            total_sites = len(df_sites)
            active_sites = len(df_sites[df_sites['Total Referred'] > 0])
            create_enhanced_metric_card(
                icon="🏥",
                label="Total Sites",
                value=str(total_sites),
                subtitle=f"{active_sites} active",
                color=COLOR_PALETTE['info']
            )
        
        with col2:
            total_referred_all = df_sites['Total Referred'].sum()
            total_recruited_all = df_sites['Recruited to CVLP'].sum()
            overall_rate = (total_recruited_all / total_referred_all * 100) if total_referred_all > 0 else 0
            create_enhanced_metric_card(
                icon="📊",
                label="Overall Referral→CVLP Rate",
                value=f"{overall_rate:.1f}%",
                subtitle=f"{total_recruited_all}/{total_referred_all}",
                color=COLOR_PALETTE['success'] if overall_rate >= 80 else COLOR_PALETTE['warning'] if overall_rate >= 50 else COLOR_PALETTE['danger']
            )
        
        with col3:
            total_randomised_all = df_sites['Randomised BNT113-01'].sum()
            randomisation_rate = (total_randomised_all / total_recruited_all * 100) if total_recruited_all > 0 else 0
            create_enhanced_metric_card(
                icon="🎲",
                label="Overall CVLP→Randomisation Rate",
                value=f"{randomisation_rate:.1f}%",
                subtitle=f"{total_randomised_all}/{total_recruited_all}",
                color=COLOR_PALETTE['success'] if randomisation_rate >= 80 else COLOR_PALETTE['warning'] if randomisation_rate >= 50 else COLOR_PALETTE['danger']
            )
        
        with col4:
            total_failures = df_sites['Screen Failures'].sum()
            failure_rate = (total_failures / total_referred_all * 100) if total_referred_all > 0 else 0
            create_enhanced_metric_card(
                icon="⚠️",
                label="Overall Screen Failure Rate",
                value=f"{failure_rate:.1f}%",
                subtitle=f"{total_failures}/{total_referred_all}",
                color=COLOR_PALETTE['danger'] if failure_rate >= 50 else COLOR_PALETTE['warning'] if failure_rate >= 25 else COLOR_PALETTE['success']
            )
    
    # Add site performance visualization (hidden in privacy mode)
    if not st.session_state.privacy_mode:
        st.markdown("### 📊 Site Performance Visualization")
    
    # Site performance chart
    if len(df_sites) > 0 and not st.session_state.privacy_mode:
        fig_site_performance = px.bar(
            df_sites,
            x='Site',
            y=['Total Referred', 'Recruited to CVLP', 'Randomised BNT113-01'],
            title='Site Performance: Referrals → CVLP → Randomisation',
            barmode='group'
        )
        fig_site_performance.update_layout(
            xaxis_title='Site',
            yaxis_title='Number of Patients',
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis={'tickangle': 45},
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            )
        )
        st.plotly_chart(fig_site_performance, use_container_width=True)
        
        # Enhanced conversion rates chart with only the two key metrics
        fig_conversion = px.bar(
            df_sites,
            x='Site',
            y=['CVLP→Referral Rate (%)', 'Referral→Randomisation Rate (%)'],
            title='Key Conversion Rates by Site',
            barmode='group',
            color_discrete_map={
                'CVLP→Referral Rate (%)': '#28a745',
                'Referral→Randomisation Rate (%)': '#2196F3'
            }
        )
        fig_conversion.update_layout(
            xaxis_title='Site',
            yaxis_title='Conversion Rate (%)',
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis={'tickangle': 45},
            legend=dict(
                title='Metric',
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            ),
            font=dict(size=12)
        )
        fig_conversion.update_traces(
            marker=dict(
                line=dict(width=1, color='white')
            ),
            texttemplate='%{y:.1f}%',
            textposition='outside'
        )
        st.plotly_chart(fig_conversion, use_container_width=True)
    
    # Add data extraction info (only show for internal users)
    if st.session_state.admin_settings['show_debug_info']:
        st.info(f"""
    **Site-based Data Extraction Summary:**
    - ✅ **Site Opening Date**: First patient consent date to CVLP for each site
    - ✅ **Total Referred**: COUNT(DISTINCT patients WHERE prescreen_referral OR main_trial_referral)
    - ✅ **Recruited to CVLP**: COUNT(patients WHERE cvlp_consent_date IS NOT NULL)
    - ✅ **Conversion Rates**: Calculated as percentages between funnel stages
    - ✅ **Screen Failures**: COUNT(patients WHERE any_screen_failure_notification IS NOT NULL)
    - 📊 **All metrics**: Calculated per site using the same logic as monthly metrics
    """)
    
    return df_sites

# Add Site-based Trial Metrics Table
st.markdown("""
<div class="section-divider">
    <div class="section-divider-icon">🏥</div>
</div>
""", unsafe_allow_html=True)
if st.session_state.admin_settings['show_site_metrics_table']:
    st.markdown("""
    <div class="section-header">
        🏥 Site-based Trial Metrics Table
    </div>
    """, unsafe_allow_html=True)

# Call the site-based table function (only if we have data)
if not master_df.empty and uploaded_master_file is not None:
    site_metrics_df = create_site_based_metrics_table(master_df)
else:
    site_metrics_df = pd.DataFrame()  # Initialize empty DataFrame
    st.info("📁 Please upload your Excel file using the sidebar to view the Site-based Trial Metrics Table.")

# Site metrics visualization

# Add Site-based Metrics Visualization
if site_metrics_df is not None and not site_metrics_df.empty and not st.session_state.privacy_mode:
    st.markdown("### 📊 Visualize Site-based Metrics")
    
    # Get numeric columns for visualization (exclude Site and Site Opening Date)
    numeric_cols = [col for col in site_metrics_df.columns 
                   if col not in ['Site', 'Site Opening Date'] and 
                   site_metrics_df[col].dtype in ['int64', 'float64']]
    
    if numeric_cols:
        # Bar Chart Visualization Section (hidden in privacy mode)
        if not st.session_state.privacy_mode:
            st.markdown("---")
            st.markdown("#### 📊 Bar Chart Visualization")
            selected_site_metrics = st.multiselect(
                "Select site metrics to visualize as bar charts:",
                options=numeric_cols,
                default=[numeric_cols[0]] if numeric_cols else [],
                key="site_bar_metrics"
            )
            
            if selected_site_metrics:
                for metric in selected_site_metrics:
                    fig_bar = px.bar(
                        site_metrics_df,
                        x='Site',
                        y=metric,
                        title=f'{metric} by Site',
                        text=metric
                    )
                    fig_bar.update_layout(
                        xaxis_title='Site',
                        yaxis_title=metric,
                        height=400,
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis={'tickangle': 45},
                        showlegend=False
                    )
                    fig_bar.update_traces(texttemplate='%{text}', textposition='outside')
                    st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("Select at least one metric to visualize as bar charts.")
            
            # Multi-Metric Comparison Section
            st.markdown("---")
            st.markdown("#### 📈 Multi-Metric Comparison")
            selected_comparison_metrics = st.multiselect(
                "Select metrics to compare across sites:",
                options=numeric_cols,
                default=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols,
                key="site_comparison_metrics"
            )
            
            if selected_comparison_metrics:
                # Create grouped bar chart
                fig_grouped = px.bar(
                    site_metrics_df,
                    x='Site',
                    y=selected_comparison_metrics,
                    title='Multi-Metric Site Comparison',
                    barmode='group'
                )
                fig_grouped.update_layout(
                    xaxis_title='Site',
                    yaxis_title='Value',
                    height=500,
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis={'tickangle': 45},
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="center",
                        x=0.5
                    )
                )
                st.plotly_chart(fig_grouped, use_container_width=True)
                
                # Create radar chart for top performing sites (if we have rate columns)
                rate_cols = [col for col in selected_comparison_metrics if 'Rate' in col or '%' in col]
                if rate_cols and len(site_metrics_df) <= 10:  # Only for reasonable number of sites
                    if st.session_state.admin_settings['show_performance_radar']:
                        st.markdown("#### Performance Radar Chart (Rates Only)")
                    
                    # Prepare data for radar chart
                    radar_data = []
                    for _, row in site_metrics_df.iterrows():
                        for rate_col in rate_cols:
                            radar_data.append({
                                'Site': row['Site'],
                                'Metric': rate_col.replace(' (%)', '').replace('Rate', 'Rate'),
                                'Value': row[rate_col]
                            })
                    
                    if radar_data:
                        radar_df = pd.DataFrame(radar_data)
                        fig_radar = px.line_polar(
                            radar_df, 
                            r='Value', 
                            theta='Metric', 
                            color='Site',
                            line_close=True,
                            title='Site Performance Radar Chart (Conversion Rates)'
                        )
                        fig_radar.update_layout(height=600)
                        st.plotly_chart(fig_radar, use_container_width=True)
            else:
                st.info("Select at least one metric for comparison.")
            
            # Performance Matrix Section (hidden in privacy mode)
            st.markdown("---")
            st.markdown("#### 🎯 Performance Matrix")
            
            # Create a heatmap of all numeric metrics
            if len(numeric_cols) >= 2:
                # Normalize data for heatmap (0-100 scale)
                heatmap_data = site_metrics_df[['Site'] + numeric_cols].copy()
                
                # Normalize each metric to 0-100 scale for better comparison
                for col in numeric_cols:
                    if heatmap_data[col].max() > 0:
                        heatmap_data[f'{col}_normalized'] = (heatmap_data[col] / heatmap_data[col].max()) * 100
                
                normalized_cols = [col for col in heatmap_data.columns if '_normalized' in col]
                
                if normalized_cols:
                    # Create heatmap
                    fig_heatmap = px.imshow(
                        heatmap_data[normalized_cols].T,
                        labels=dict(x="Site Index", y="Metrics", color="Normalized Score (0-100)"),
                        x=heatmap_data['Site'],
                        y=[col.replace('_normalized', '') for col in normalized_cols],
                        title="Site Performance Heatmap (Normalized Scores)",
                        aspect="auto",
                        color_continuous_scale="RdYlGn"
                    )
                    fig_heatmap.update_layout(
                        height=400,
                        xaxis={'tickangle': 45}
                    )
                    st.plotly_chart(fig_heatmap, use_container_width=True)
                
                st.info("💡 **Heatmap Guide**: Green = High performance, Red = Low performance. Each metric is normalized to 0-100 scale for comparison.")
        else:
            st.info("Need at least 2 numeric metrics to create performance matrix.")
    else:
        st.info("No numeric metrics available for visualization.")

# Enhanced Combined Visualization Section
if 'df_monthly' in locals() and df_monthly is not None and not df_monthly.empty and site_metrics_df is not None and not site_metrics_df.empty and not st.session_state.privacy_mode:
    if st.session_state.admin_settings['show_combined_analysis']:
        st.markdown("---")
    st.markdown("### 🔄 Combined Monthly & Site Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📅 Monthly Trends")
        monthly_metric_options = [col for col in df_monthly.columns if col != 'Month']
        selected_monthly_trend = st.selectbox(
            "Select monthly metric for trend analysis:",
            options=monthly_metric_options,
            key="combined_monthly"
        )
        
        if selected_monthly_trend:
            # Filter data for visualization - actual metrics only show up to current month
            current_date = pd.Timestamp.now()
            df_trend_viz = df_monthly.copy()
            
            # Convert selected metric to numeric, handling "-" strings
            if selected_monthly_trend in df_trend_viz.columns:
                df_trend_viz[selected_monthly_trend] = df_trend_viz[selected_monthly_trend].apply(
                    lambda x: None if (isinstance(x, str) and x == '-') else x
                )
                df_trend_viz[selected_monthly_trend] = pd.to_numeric(df_trend_viz[selected_monthly_trend], errors='coerce')
            
            # For actual metrics, filter to current month
            if 'Actual' in selected_monthly_trend:
                # Find the index of current month or closest past month
                current_month_idx = None
                for idx, month in enumerate(df_monthly['Month']):
                    try:
                        month_date = pd.to_datetime(f"01-{month}", format='%d-%b-%y')
                        if month_date <= current_date:
                            current_month_idx = idx
                        else:
                            break
                    except:
                        continue
                
                # Set future actual values to NaN
                if current_month_idx is not None:
                    df_trend_viz.loc[current_month_idx + 1:, selected_monthly_trend] = None
            
            fig_monthly_trend = px.line(
                df_trend_viz,
                x='Month',
                y=selected_monthly_trend,
                markers=True,
                title=f'Monthly Trend: {selected_monthly_trend}'
            )
            fig_monthly_trend.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis={'tickangle': 45}
            )
            st.plotly_chart(fig_monthly_trend, use_container_width=True)
            
            # Add explanation for actual metrics (only show for internal users)
            if st.session_state.admin_settings['show_debug_info']:
                if 'Actual' in selected_monthly_trend:
                    current_month_str = current_date.strftime('%b-%y')
                    st.info(f"📅 **Note**: This 'Actual' metric only shows data up to the current month ({current_month_str}). Future months cannot have actual data yet.")
    
    with col2:
        st.markdown("#### 🏥 Site Performance")
        site_numeric_cols = [col for col in site_metrics_df.columns 
                           if col not in ['Site', 'Site Opening Date'] and 
                           site_metrics_df[col].dtype in ['int64', 'float64']]
        
        selected_site_metric = st.selectbox(
            "Select site metric for comparison:",
            options=site_numeric_cols,
            key="combined_site"
        )
        
        if selected_site_metric:
            fig_site_comparison = px.bar(
                site_metrics_df,
                x='Site',
                y=selected_site_metric,
                title=f'Site Comparison: {selected_site_metric}'
            )
            fig_site_comparison.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis={'tickangle': 45},
                showlegend=False
            )
            st.plotly_chart(fig_site_comparison, use_container_width=True)

# Add CVLP Site Performance section
st.markdown("""
<div class="section-divider">
    <div class="section-divider-icon">📈</div>
</div>
""", unsafe_allow_html=True)
if st.session_state.admin_settings['show_site_performance']:
    st.markdown("""
    <div class="section-header">
        🏥 CVLP Site Performance
    </div>
    """, unsafe_allow_html=True)

def create_cvlp_site_performance_table(df, uploaded_file=None):
    """Create a comprehensive CVLP Site Performance table tracking multiple metrics over time"""
    
    if df.empty:
        st.warning("No data available for CVLP Site Performance")
        return
    
    # First, try to get the official site list and pre-calculated data from "CVLP Site Data" sheet
    official_sites = []
    site_data_dict = {}  # Store pre-calculated data from CVLP Site Data sheet
    
    if uploaded_file is not None:
        try:
            # Try different possible sheet names
            excel_file = pd.ExcelFile(uploaded_file)
            available_sheets = excel_file.sheet_names
            possible_sheet_names = ["CVLP Site Data", "CVLP Site Data ", "Site Data", "CVLP Sites", "Sites"]
            sheet_found = None
            
            for sheet_name in possible_sheet_names:
                if sheet_name in available_sheets:
                    sheet_found = sheet_name
                    break
            
            if sheet_found:
                # Try different header rows in case data doesn't start at row 0
                site_col_found = False
                for header_row in [0, 1, 2, 3]:
                    try:
                        cvlp_site_data = pd.read_excel(uploaded_file, sheet_name=sheet_found, header=header_row)
                        
                        # Look for the CVLP Site column
                        site_col = None
                        possible_site_cols = ['CVLP Site', 'CVLP site', 'Site name', 'Site Name', 'Site']
                        for col in cvlp_site_data.columns:
                            if str(col) in possible_site_cols:
                                site_col = col
                                break
                        
                        if site_col:
                            # Extract official site names, filtering out empty/NaN values and placeholder text
                            official_sites = cvlp_site_data[site_col].dropna().unique().tolist()
                            official_sites = [site for site in official_sites if str(site).strip() != '' and 
                                            'enter' not in str(site).lower() and 
                                            'placeholder' not in str(site).lower() and
                                            'cvlp site' not in str(site).lower()]
                            
                            if len(official_sites) > 0:
                                site_col_found = True
                                
                                # Remove any sites that are actually column headers
                                official_sites = [s for s in official_sites if not any(
                                    header_word in str(s).lower() 
                                    for header_word in ['site name', 'green light', 'date', 'screened']
                                )]
                                
                                # Now read additional columns from CVLP Site Data
                                # Look for "Days Since Site Active" (Total days since last patient referred / site opened)
                                days_since_col = None
                                possible_days_cols = [
                                    'Days Since Site Active',
                                    'Days since site active',
                                    'Total days since last patient referred / site opened',
                                    'Total days since last patient referred/site opened',
                                    'Days since last referral',
                                    'Days since last patient referred'
                                ]
                                for col in cvlp_site_data.columns:
                                    col_str = str(col).strip()
                                    if any(possible.lower() in col_str.lower() for possible in possible_days_cols):
                                        days_since_col = col
                                        break
                                
                                # Look for "Days Between Site Open & Referral" (days from site open to first referral)
                                days_to_referral_col = None
                                possible_days_to_ref_cols = [
                                    'Days Between Site Open & Referral',
                                    'Days between site open & referral',
                                    'Days to first referral'
                                ]
                                for col in cvlp_site_data.columns:
                                    col_str = str(col).strip()
                                    if any(possible.lower() in col_str.lower() for possible in possible_days_to_ref_cols):
                                        days_to_referral_col = col
                                        break
                                
                                # Look for green light date column (site opened date) - keeping for potential future use
                                green_light_col = None
                                possible_green_light_cols = [
                                    'Go-Live Date',
                                    'Go live date',
                                    'Enter green light date',
                                    'Green light date',
                                    'Site opened date',
                                    'Site open date'
                                ]
                                for col in cvlp_site_data.columns:
                                    col_str = str(col).strip()
                                    if any(possible.lower() in col_str.lower() for possible in possible_green_light_cols):
                                        green_light_col = col
                                        break
                                
                                # Look for first referral date column - keeping for potential future use
                                first_pt_col = None
                                possible_first_pt_cols = [
                                    'Date of first referral',
                                    'Date of First Referral',
                                    'Enter date first pt screened at site',
                                    'Date first pt screened at site',
                                    'First patient screened',
                                    'First screening date'
                                ]
                                for col in cvlp_site_data.columns:
                                    col_str = str(col).strip()
                                    if any(possible.lower() in col_str.lower() for possible in possible_first_pt_cols):
                                        first_pt_col = col
                                        break
                                
                                # Debug: Show what columns were found (temporary)
                                if 'show_debug' not in st.session_state:
                                    st.session_state.show_debug = {}
                                st.session_state.show_debug['green_light_col'] = green_light_col
                                st.session_state.show_debug['first_pt_col'] = first_pt_col
                                st.session_state.show_debug['days_since_col'] = days_since_col
                                st.session_state.show_debug['days_to_referral_col'] = days_to_referral_col
                                st.session_state.show_debug['all_columns'] = list(cvlp_site_data.columns)
                                
                                # Store the data in a dictionary for quick lookup
                                for idx, row in cvlp_site_data.iterrows():
                                    if pd.notna(row[site_col]):
                                        site_name = row[site_col]
                                        site_data_dict[site_name] = {}
                                        
                                        # Read "Days Since Site Active" (total days since last patient referred / site opened)
                                        if days_since_col and days_since_col in row.index:
                                            days_since_value = row[days_since_col]
                                            if pd.notna(days_since_value):
                                                try:
                                                    site_data_dict[site_name]['days_since_last_referral'] = float(days_since_value)
                                                except:
                                                    pass
                                        
                                        # Read "Days Between Site Open & Referral" (days from site open to first referral)
                                        if days_to_referral_col and days_to_referral_col in row.index:
                                            days_to_ref_value = row[days_to_referral_col]
                                            if pd.notna(days_to_ref_value):
                                                try:
                                                    site_data_dict[site_name]['days_to_first_referral'] = float(days_to_ref_value)
                                                except:
                                                    pass
                                        
                                        # Read green light date and first referral date for potential future use
                                        if green_light_col and green_light_col in row.index:
                                            green_light_date = pd.to_datetime(row[green_light_col], errors='coerce')
                                            site_data_dict[site_name]['green_light_date'] = green_light_date
                                        
                                        if first_pt_col and first_pt_col in row.index:
                                            first_pt_date = pd.to_datetime(row[first_pt_col], errors='coerce')
                                            site_data_dict[site_name]['first_pt_screened_date'] = first_pt_date
                                
                                break
                    except:
                        continue
                
                if not site_col_found:
                    # If we can't read the sheet properly, use all 19 CVLP sites (exact names)
                    official_sites = [
                        "Coventry and Warwickshire",
                        "Bath",
                        "Gloucestershire",
                        "Univeristy Hospitals Dorset",
                        "Mid & South Essex - Broomfield",
                        "Mid & South Essex - Southend",
                        "Bedfordshire",
                        "Hull",
                        "Royal Surrey",
                        "Royal Berkshire",
                        "United Lincolnshire",
                        "York & Scarborough",
                        "Royal Free (North Middlesex)",
                        "Barking Havering and Redbridge",
                        "East & North Herefordshire (Lister)",
                        "North Cumbria",
                        "West Suffolk",
                        "Maidstone",
                        "Leicester"
                    ]

            else:
                # Use all 19 CVLP sites as fallback (exact names)
                official_sites = [
                    "Coventry and Warwickshire",
                    "Bath",
                    "Gloucestershire",
                    "Univeristy Hospitals Dorset",
                    "Mid & South Essex - Broomfield",
                    "Mid & South Essex - Southend",
                    "Bedfordshire",
                    "Hull",
                    "Royal Surrey",
                    "Royal Berkshire",
                    "United Lincolnshire",
                    "York & Scarborough",
                    "Royal Free (North Middlesex)",
                    "Barking Havering and Redbridge",
                    "East & North Herefordshire (Lister)",
                    "North Cumbria",
                    "West Suffolk",
                    "Maidstone",
                    "Leicester"
                ]

                    
        except Exception as e:
            # Use all 19 CVLP sites as fallback on any error (exact names)
            official_sites = [
                "Coventry and Warwickshire",
                "Bath",
                "Gloucestershire",
                "Univeristy Hospitals Dorset",
                "Mid & South Essex - Broomfield",
                "Mid & South Essex - Southend",
                "Bedfordshire",
                "Hull",
                "Royal Surrey",
                "Royal Berkshire",
                "United Lincolnshire",
                "York & Scarborough",
                "Royal Free (North Middlesex)",
                "Barking Havering and Redbridge",
                "East & North Herefordshire (Lister)",
                "North Cumbria",
                "West Suffolk",
                "Maidstone",
                "Leicester"
            ]

    
    # If we couldn't get official sites, use comprehensive list of all 19 CVLP sites as final fallback (exact names)
    if not official_sites:
        official_sites = [
            "Coventry and Warwickshire",
            "Bath",
            "Gloucestershire",
            "Univeristy Hospitals Dorset",
            "Mid & South Essex - Broomfield",
            "Mid & South Essex - Southend",
            "Bedfordshire",
            "Hull",
            "Royal Surrey",
            "Royal Berkshire",
            "United Lincolnshire",
            "York & Scarborough",
            "Royal Free (North Middlesex)",
            "Barking Havering and Redbridge",
            "East & North Herefordshire (Lister)",
            "North Cumbria",
            "West Suffolk",
            "Maidstone",
            "Leicester"
        ]

    
    if len(official_sites) == 0:
        st.warning("No CVLP sites found in the data")
        return
    
    # Find CVLP Site column in main data for filtering
    cvlp_site_col = None
    possible_site_cols = ['CVLP Site', 'CVLP site', 'Please choose the CVLP site from the drop down']
    
    for col in possible_site_cols:
        if col in df.columns:
            cvlp_site_col = col
            break
    
    # Date columns for analysis - checking multiple possible column names
    date_columns = {}
    
    # CVLP Consent - find the correct column
    cvlp_consent_options = [
        'Date patient consented into CVLP',
        'Please input the date the patient signed the consent form (dd/mm/yyyy)',
        'CVLP consent date',
        'Date of CVLP consent',
        'Date patient consented into CVLP ',  # with trailing space
        'Please input the date the patient signed the consent form',
        'Patient consent date',
        'CVLP Site consent date'
    ]
    for col in cvlp_consent_options:
        if col in df.columns:
            date_columns['cvlp_consent'] = col
            break
    
    # Pre-screen referral - find the correct column
    prescreen_referral_options = [
        'Please input the date the pre-screening referral form was sent to the trial site\n(dd/mm/yyyy)',
        'Please input the date the pre-screening referral form was sent to the trial site (dd/mm/yyyy)',
        'Date pre-screening referral sent',
        'Pre-screening referral date'
    ]
    for col in prescreen_referral_options:
        if col in df.columns:
            date_columns['prescreen_referral'] = col
            break
    
    # Main trial referral - find the correct column
    main_trial_referral_options = [
        'Please input the date the main trial screening referral form was sent to the trial site\n(dd/mm/yyyy)',
        'Please input the date the main trial screening referral form was sent to the trial site (dd/mm/yyyy)',
        'Date main trial referral sent',
        'Main trial referral date'
    ]
    for col in main_trial_referral_options:
        if col in df.columns:
            date_columns['main_trial_referral'] = col
            break
    
    # Randomised/Enrolled - find the correct column
    randomised_options = [
        'Date participant enrolled',
        'Participant enrolled to BNT113-01?',
        'Date of enrollment',
        'Enrollment date',
        'Randomisation date'
    ]
    for col in randomised_options:
        if col in df.columns:
            date_columns['randomised'] = col
            break
    
    
    # Convert date columns to datetime
    for key, col in date_columns.items():
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Define months for analysis (Apr-25 to current)
    months = []
    current_date = datetime.now()
    start_date = pd.Timestamp('2025-04-01')
    
    # Generate month list
    temp_date = start_date
    while temp_date <= current_date:
        months.append({
            'name': temp_date.strftime('%b-%y'),
            'start': temp_date,
            'end': temp_date + pd.DateOffset(months=1) - pd.Timedelta(days=1)
        })
        temp_date = temp_date + pd.DateOffset(months=1)
    
    # Create performance data structure
    performance_data = []
    
    for site in official_sites:
        # Filter data for this site (only if we have the CVLP site column)
        if cvlp_site_col:
            site_data = df[df[cvlp_site_col] == site]
        else:
            site_data = pd.DataFrame()  # Empty DataFrame if no site column found
        
        # Initialize site row - all official sites are considered open and active
        site_row = {
            'Site name': site,
            'Site opened': 'Yes'  # All official CVLP sites are open
        }
        
        # Calculate metrics for each month
        for month in months:
            month_name = month['name']
            
            # Filter data for this month
            month_data = site_data.copy()
            
            # Consented to CVLP
            cvlp_consented = 0
            if 'cvlp_consent' in date_columns and date_columns['cvlp_consent'] in df.columns:
                cvlp_consented = len(month_data[
                    (month_data[date_columns['cvlp_consent']] >= month['start']) &
                    (month_data[date_columns['cvlp_consent']] <= month['end'])
                ])
            site_row[f'Consented to CVLP_{month_name}'] = cvlp_consented
            
            # Referred to pre-screen
            prescreen_referred = 0
            if 'prescreen_referral' in date_columns and date_columns['prescreen_referral'] in df.columns:
                prescreen_referred = len(month_data[
                    (month_data[date_columns['prescreen_referral']] >= month['start']) &
                    (month_data[date_columns['prescreen_referral']] <= month['end'])
                ])
            site_row[f'Referred to pre-screen_{month_name}'] = prescreen_referred
            
            # Referred to main trial
            main_trial_referred = 0
            if 'main_trial_referral' in date_columns and date_columns['main_trial_referral'] in df.columns:
                main_trial_referred = len(month_data[
                    (month_data[date_columns['main_trial_referral']] >= month['start']) &
                    (month_data[date_columns['main_trial_referral']] <= month['end'])
                ])
            site_row[f'Referred to main trial_{month_name}'] = main_trial_referred
            
            # Consented to pre-screen
            prescreen_consented = 0
            if 'prescreen_consent' in date_columns and date_columns['prescreen_consent'] in df.columns:
                prescreen_consented = len(month_data[
                    (month_data[date_columns['prescreen_consent']] >= month['start']) &
                    (month_data[date_columns['prescreen_consent']] <= month['end'])
                ])
            site_row[f'Consented to pre-screen_{month_name}'] = prescreen_consented
            
        
        # Calculate overall metrics for the site
        total_consented = 0
        total_referred_prescreen = 0
        total_referred_main = 0
        
        if 'cvlp_consent' in date_columns and date_columns['cvlp_consent'] in df.columns:
            total_consented = len(site_data[site_data[date_columns['cvlp_consent']].notna()])
        
        if 'prescreen_referral' in date_columns and date_columns['prescreen_referral'] in df.columns:
            total_referred_prescreen = len(site_data[site_data[date_columns['prescreen_referral']].notna()])
        
        if 'main_trial_referral' in date_columns and date_columns['main_trial_referral'] in df.columns:
            total_referred_main = len(site_data[site_data[date_columns['main_trial_referral']].notna()])
        
        # Calculate site opened date (earliest CVLP consent date for this site)
        site_opened_date = None
        if 'cvlp_consent' in date_columns and date_columns['cvlp_consent'] in df.columns:
            site_dates = site_data[site_data[date_columns['cvlp_consent']].notna()][date_columns['cvlp_consent']]
            if len(site_dates) > 0:
                site_opened_date = site_dates.min()
        
        # Get days from site open to first referral - prioritize CVLP Site Data sheet
        days_to_first_referral = None
        days_to_first_referral_status = None
        
        # First try to get from the CVLP Site Data sheet
        if site in site_data_dict and 'days_to_first_referral' in site_data_dict[site]:
            days_to_first_referral = site_data_dict[site]['days_to_first_referral']
        
        # If not found in CVLP Site Data, calculate it from main tracker data
        if days_to_first_referral is None:
            first_referral_date = None
            
            # Find first referral date (either pre-screen or main trial)
            referral_dates = []
            if 'prescreen_referral' in date_columns and date_columns['prescreen_referral'] in df.columns:
                prescreen_dates = site_data[site_data[date_columns['prescreen_referral']].notna()][date_columns['prescreen_referral']]
                if len(prescreen_dates) > 0:
                    referral_dates.append(prescreen_dates.min())
            
            if 'main_trial_referral' in date_columns and date_columns['main_trial_referral'] in df.columns:
                main_dates = site_data[site_data[date_columns['main_trial_referral']].notna()][date_columns['main_trial_referral']]
                if len(main_dates) > 0:
                    referral_dates.append(main_dates.min())
            
            if referral_dates:
                first_referral_date = min(referral_dates)
            
            if site_opened_date and first_referral_date:
                days_to_first_referral = (first_referral_date - site_opened_date).days
        
        # Apply color coding
        if days_to_first_referral is not None:
            # Color coding: Green <60, Orange 60-90, Red >90
            if days_to_first_referral > 90:
                days_to_first_referral_status = 'RED'
            elif days_to_first_referral >= 60:
                days_to_first_referral_status = 'ORANGE'
        else:
                days_to_first_referral_status = 'GREEN'
        
        site_row['Days from site open to first referral'] = days_to_first_referral
        site_row['Days from site open to first referral (Status)'] = days_to_first_referral_status
        
        # Calculate total days since last patient referred / site opened
        # Formula: Today - date of last referral (or site opened if no referrals)
        # Use the most recent date from either pre-screening or main trial referral
        days_since_last_referral = None
        days_since_last_referral_status = None
        last_referral_date = None
        
        # Find last (most recent) referral date (either pre-screen or main trial)
        last_referral_dates = []
        if 'prescreen_referral' in date_columns and date_columns['prescreen_referral'] in df.columns:
            prescreen_dates = site_data[site_data[date_columns['prescreen_referral']].notna()][date_columns['prescreen_referral']]
            if len(prescreen_dates) > 0:
                last_referral_dates.append(prescreen_dates.max())
        
        if 'main_trial_referral' in date_columns and date_columns['main_trial_referral'] in df.columns:
            main_dates = site_data[site_data[date_columns['main_trial_referral']].notna()][date_columns['main_trial_referral']]
            if len(main_dates) > 0:
                last_referral_dates.append(main_dates.max())
        
        if last_referral_dates:
            # Has referrals - use the most recent referral date
            last_referral_date = max(last_referral_dates)
            days_since_last_referral = (current_date - last_referral_date).days
        else:
            # No referrals yet - use site opened date (first CVLP consent date)
            if site_opened_date:
                days_since_last_referral = (current_date - site_opened_date).days
            else:
                # If no site opened date either, try to get from CVLP Site Data
                if site in site_data_dict and 'green_light_date' in site_data_dict[site]:
                    green_light = site_data_dict[site]['green_light_date']
                    if pd.notna(green_light):
                        days_since_last_referral = (current_date - green_light).days
        
        # Apply color coding
        if days_since_last_referral is not None:
            # Color coding: Green <30, Orange 30-60, Red >60
            if days_since_last_referral > 60:
                days_since_last_referral_status = 'RED'
            elif days_since_last_referral >= 30:
                days_since_last_referral_status = 'ORANGE'
            else:
                days_since_last_referral_status = 'GREEN'
        
        site_row['Total days since last patient referred / site opened'] = days_since_last_referral
        site_row['Total days since last patient referred / site opened (Status)'] = days_since_last_referral_status
        
        # Calculate average monthly recruitment up to Sep-25
        # Formula: Total CVLP consented / (Days site active / 30.44)
        # Days site active = End of Sep-25 - Date of first patient screened at site
        sep_2025_end = pd.Timestamp('2025-09-30')
        
        # Find the date of first patient screened at this site (earliest CVLP consent date)
        first_screening_date = None
        if 'cvlp_consent' in date_columns and date_columns['cvlp_consent'] in df.columns:
            site_consent_dates = site_data[site_data[date_columns['cvlp_consent']].notna()][date_columns['cvlp_consent']]
            if len(site_consent_dates) > 0:
                first_screening_date = site_consent_dates.min()
        
        # Calculate average monthly recruitment
        avg_monthly_recruitment = 0
        if first_screening_date and first_screening_date <= sep_2025_end:
            # Calculate days site has been active
            days_active = (sep_2025_end - first_screening_date).days
            
            # Count total consents up to Sep 2025
            consents_to_sep = 0
            if 'cvlp_consent' in date_columns and date_columns['cvlp_consent'] in df.columns:
                consents_to_sep = len(site_data[
                    (site_data[date_columns['cvlp_consent']].notna()) &
                    (site_data[date_columns['cvlp_consent']] <= sep_2025_end)
                ])
            
            # Calculate average: Total consented / (Days active / 30.44 days per month)
            if days_active > 0:
                months_active = days_active / 30.44
                avg_monthly_recruitment = consents_to_sep / months_active
        
        site_row['Average monthly recruitment up to Sep-25'] = avg_monthly_recruitment
        
        # Calculate average monthly referrals up to Sep-25
        # Using the same logic as recruitment
        avg_monthly_referrals = 0
        if first_screening_date and first_screening_date <= sep_2025_end:
            days_active = (sep_2025_end - first_screening_date).days
            
            # Count referrals up to Sep 2025
            referrals_to_sep_prescreen = 0
            referrals_to_sep_main = 0
            
            if 'prescreen_referral' in date_columns and date_columns['prescreen_referral'] in df.columns:
                referrals_to_sep_prescreen = len(site_data[
                    (site_data[date_columns['prescreen_referral']].notna()) &
                    (site_data[date_columns['prescreen_referral']] <= sep_2025_end)
                ])
            
            if 'main_trial_referral' in date_columns and date_columns['main_trial_referral'] in df.columns:
                referrals_to_sep_main = len(site_data[
                    (site_data[date_columns['main_trial_referral']].notna()) &
                    (site_data[date_columns['main_trial_referral']] <= sep_2025_end)
                ])
            
            # Calculate average: Total referrals / (Days active / 30.44 days per month)
            if days_active > 0:
                months_active = days_active / 30.44
                avg_monthly_referrals = (referrals_to_sep_prescreen + referrals_to_sep_main) / months_active
        
        site_row['Average monthly referrals up to Sep-25'] = avg_monthly_referrals
        
        # Calculate change in average monthly recruitment (comparing current month to previous month)
        # Get last two complete months (August and September 2025)
        sep_2025_start = pd.Timestamp('2025-09-01')
        sep_2025_end = pd.Timestamp('2025-09-30')
        aug_2025_start = pd.Timestamp('2025-08-01')
        aug_2025_end = pd.Timestamp('2025-08-31')
        
        # Calculate August's average monthly rate (up to end of Aug)
        aug_2025_end_ts = pd.Timestamp('2025-08-31')
        aug_avg_recruitment = 0
        aug_avg_referrals = 0
        
        if first_screening_date and first_screening_date <= aug_2025_end_ts:
            days_active_aug = (aug_2025_end_ts - first_screening_date).days
            if days_active_aug > 0:
                # Count consents up to August
                consents_to_aug = 0
                if 'cvlp_consent' in date_columns and date_columns['cvlp_consent'] in df.columns:
                    consents_to_aug = len(site_data[
                        (site_data[date_columns['cvlp_consent']].notna()) &
                        (site_data[date_columns['cvlp_consent']] <= aug_2025_end_ts)
                    ])
                
                months_active_aug = days_active_aug / 30.44
                aug_avg_recruitment = consents_to_aug / months_active_aug if months_active_aug > 0 else 0
                
                # Count referrals up to August
                referrals_to_aug_prescreen = 0
                referrals_to_aug_main = 0
                if 'prescreen_referral' in date_columns and date_columns['prescreen_referral'] in df.columns:
                    referrals_to_aug_prescreen = len(site_data[
                        (site_data[date_columns['prescreen_referral']].notna()) &
                        (site_data[date_columns['prescreen_referral']] <= aug_2025_end_ts)
                    ])
                if 'main_trial_referral' in date_columns and date_columns['main_trial_referral'] in df.columns:
                    referrals_to_aug_main = len(site_data[
                        (site_data[date_columns['main_trial_referral']].notna()) &
                        (site_data[date_columns['main_trial_referral']] <= aug_2025_end_ts)
                    ])
                
                total_referrals_to_aug = referrals_to_aug_prescreen + referrals_to_aug_main
                aug_avg_referrals = total_referrals_to_aug / months_active_aug if months_active_aug > 0 else 0
        
        # Calculate change from August to September
        change_in_recruitment = None
        change_in_referrals = None
        
        if aug_avg_recruitment > 0 and avg_monthly_recruitment > 0:
            change_in_recruitment = ((avg_monthly_recruitment - aug_avg_recruitment) / aug_avg_recruitment) * 100
        
        if aug_avg_referrals > 0 and avg_monthly_referrals > 0:
            change_in_referrals = ((avg_monthly_referrals - aug_avg_referrals) / aug_avg_referrals) * 100
        
        site_row['Change in average monthly recruitment'] = change_in_recruitment
        site_row['Change in average monthly referrals'] = change_in_referrals
        
        performance_data.append(site_row)
    
    # Create DataFrame
    performance_df = pd.DataFrame(performance_data)
    
    if performance_df.empty:
        st.warning("No performance data to display")
        return
    
    # Display site performance table with enhanced visual design
    st.markdown("""
    <div style="text-align: center; margin: 40px 0 30px 0;">
        <h2 style="color: #2E7D32; font-size: 28px; font-weight: 700; margin-bottom: 8px; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            📊 Site Performance Metrics
        </h2>
        <p style="color: #666; font-size: 16px; margin: 0; font-weight: 400;">
            Comprehensive site-by-site performance tracking with activity and trend analysis
        </p>
        <div style="width: 100px; height: 4px; background: linear-gradient(90deg, #4CAF50, #2196F3); margin: 20px auto; border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Select columns to display
    display_columns = [
        'Site name',
        'Days from site open to first referral',
        'Total days since last patient referred / site opened',
        'Average monthly recruitment up to Sep-25',
        'Change in average monthly recruitment',
        'Average monthly referrals up to Sep-25',
        'Change in average monthly referrals'
    ]
    
    # Filter to available columns
    available_display_columns = [col for col in display_columns if col in performance_df.columns]
    display_df = performance_df[available_display_columns].copy()
    
    # Function to color cells based on status and values
    def highlight_performance(row):
        colors = []
        for col in row.index:
            # Days from site open to first referral
            if col == 'Days from site open to first referral':
                value = row[col]
                status_col = 'Days from site open to first referral (Status)'
                if status_col in row.index:
                    status = row[status_col]
                    if status == 'GREEN':
                        colors.append('background-color: #4CAF50; color: white; font-weight: bold')
                    elif status == 'ORANGE':
                        colors.append('background-color: #FF9800; color: white; font-weight: bold')
                    elif status == 'RED':
                        colors.append('background-color: #F44336; color: white; font-weight: bold')
                    else:
                        colors.append('')
                elif pd.notna(value):
                    # Direct value coloring as fallback
                    if value > 90:
                        colors.append('background-color: #F44336; color: white; font-weight: bold')
                    elif value >= 60:
                        colors.append('background-color: #FF9800; color: white; font-weight: bold')
                    else:
                        colors.append('background-color: #4CAF50; color: white; font-weight: bold')
                else:
                    colors.append('')

            # Total days since last patient referred / site opened
            elif col == 'Total days since last patient referred / site opened':
                value = row[col]
                status_col = 'Total days since last patient referred / site opened (Status)'
                if status_col in row.index:
                    status = row[status_col]
                    if status == 'GREEN':
                        colors.append('background-color: #4CAF50; color: white; font-weight: bold')
                    elif status == 'ORANGE':
                        colors.append('background-color: #FF9800; color: white; font-weight: bold')
                    elif status == 'RED':
                        colors.append('background-color: #F44336; color: white; font-weight: bold')
                    else:
                        colors.append('')
                elif pd.notna(value):
                    # Direct value coloring as fallback
                    if value > 60:
                        colors.append('background-color: #F44336; color: white; font-weight: bold')
                    elif value >= 30:
                        colors.append('background-color: #FF9800; color: white; font-weight: bold')
                    else:
                        colors.append('background-color: #4CAF50; color: white; font-weight: bold')
                else:
                    colors.append('')
            
            # Average monthly metrics - light background coloring
            elif 'Average monthly' in col:
                value = row[col] if pd.notna(row[col]) else 0
                if value >= 1.0:
                    colors.append('background-color: #E8F5E8')
                elif value >= 0.5:
                    colors.append('background-color: #FFF3E0')
                elif value > 0:
                    colors.append('background-color: #FFEBEE')
                else:
                    colors.append('background-color: #FFEBEE')
            
            # Change metrics - color based on positive/negative
            elif 'Change in' in col:
                value = row[col]
                if pd.notna(value):
                    if value > 0:
                        colors.append('background-color: #E8F5E8; color: #2E7D32')
                    elif value < 0:
                        colors.append('background-color: #FFEBEE; color: #D32F2F')
                    else:
                        colors.append('')
                else:
                    colors.append('')
            
            else:
                colors.append('')
        return colors
    
    # === DISPLAY PERFORMANCE TABLE ===
    if not display_df.empty:
        # Create a modified highlight function that works with limited columns
        def highlight_performance_display(row):
            colors = []
            # Get the corresponding row from performance_df to access status columns
            full_row = performance_df.loc[row.name]
            
            for col in row.index:
                # Days from site open to first referral - Gradient RAG coloring
                if col == 'Days from site open to first referral':
                    value = row[col]
                    if pd.notna(value):
                        # Green (<60) to Orange (60-90) to Red (>90) gradient
                        if value <= 30:
                            # Deep green for very fast
                            colors.append('background: linear-gradient(135deg, #4CAF50, #66BB6A); color: white; font-weight: bold; box-shadow: inset 0 0 10px rgba(0,0,0,0.1)')
                        elif value <= 60:
                            # Light green transitioning
                            colors.append('background: linear-gradient(135deg, #81C784, #AED581); color: white; font-weight: bold; box-shadow: inset 0 0 10px rgba(0,0,0,0.1)')
                        elif value <= 75:
                            # Yellow-orange transition
                            colors.append('background: linear-gradient(135deg, #FFB74D, #FFA726); color: white; font-weight: bold; box-shadow: inset 0 0 10px rgba(0,0,0,0.1)')
                        elif value <= 90:
                            # Orange
                            colors.append('background: linear-gradient(135deg, #FF9800, #FB8C00); color: white; font-weight: bold; box-shadow: inset 0 0 10px rgba(0,0,0,0.1)')
                        elif value <= 120:
                            # Light red
                            colors.append('background: linear-gradient(135deg, #EF5350, #E53935); color: white; font-weight: bold; box-shadow: inset 0 0 10px rgba(0,0,0,0.1)')
                        else:
                            # Deep red for very delayed
                            colors.append('background: linear-gradient(135deg, #F44336, #D32F2F); color: white; font-weight: bold; box-shadow: inset 0 0 10px rgba(0,0,0,0.1)')
                    else:
                        colors.append('')
                
                # Total days since last patient referred / site opened - Gradient RAG coloring
                elif col == 'Total days since last patient referred / site opened':
                    value = row[col]
                    if pd.notna(value):
                        # Green (<30) to Orange (30-60) to Red (>60) gradient
                        if value <= 15:
                            # Deep green for very recent
                            colors.append('background: linear-gradient(135deg, #4CAF50, #66BB6A); color: white; font-weight: bold; box-shadow: inset 0 0 10px rgba(0,0,0,0.1)')
                        elif value <= 30:
                            # Light green
                            colors.append('background: linear-gradient(135deg, #81C784, #AED581); color: white; font-weight: bold; box-shadow: inset 0 0 10px rgba(0,0,0,0.1)')
                        elif value <= 45:
                            # Yellow-orange transition
                            colors.append('background: linear-gradient(135deg, #FFB74D, #FFA726); color: white; font-weight: bold; box-shadow: inset 0 0 10px rgba(0,0,0,0.1)')
                        elif value <= 60:
                            # Orange
                            colors.append('background: linear-gradient(135deg, #FF9800, #FB8C00); color: white; font-weight: bold; box-shadow: inset 0 0 10px rgba(0,0,0,0.1)')
                        elif value <= 90:
                            # Light red
                            colors.append('background: linear-gradient(135deg, #EF5350, #E53935); color: white; font-weight: bold; box-shadow: inset 0 0 10px rgba(0,0,0,0.1)')
                        else:
                            # Deep red for very delayed
                            colors.append('background: linear-gradient(135deg, #F44336, #D32F2F); color: white; font-weight: bold; box-shadow: inset 0 0 10px rgba(0,0,0,0.1)')
                    else:
                        colors.append('')
                
                # Average monthly metrics - light background coloring
                elif 'Average monthly' in col:
                    value = row[col] if pd.notna(row[col]) else 0
                    if value >= 1.0:
                        colors.append('background-color: #E8F5E8')
                    elif value >= 0.5:
                        colors.append('background-color: #FFF3E0')
                    elif value > 0:
                        colors.append('background-color: #FFEBEE')
                    else:
                        colors.append('background-color: #FFEBEE')
                
                # Change metrics - color based on positive/negative
                elif 'Change in' in col:
                    value = row[col]
                    if pd.notna(value):
                        if value > 0:
                            colors.append('background-color: #E8F5E8; color: #2E7D32; font-weight: bold')
                        elif value < 0:
                            colors.append('background-color: #FFEBEE; color: #D32F2F; font-weight: bold')
                        else:
                            colors.append('')
                    else:
                        colors.append('')
                
                else:
                    colors.append('')
            return colors
        
        # Apply styling to display dataframe
        final_styled_df = display_df.style.apply(highlight_performance_display, axis=1).format({
            'Days from site open to first referral': lambda x: f'{int(x)}' if pd.notna(x) else '',
            'Total days since last patient referred / site opened': lambda x: f'{int(x)}' if pd.notna(x) else '',
            'Average monthly recruitment up to Sep-25': '{:.2f}',
            'Change in average monthly recruitment': lambda x: f'{x:+.1f}%' if pd.notna(x) else '-',
            'Average monthly referrals up to Sep-25': '{:.2f}',
            'Change in average monthly referrals': lambda x: f'{x:+.1f}%' if pd.notna(x) else '-'
        }).set_properties(**{
            'text-align': 'center',
            'padding': '12px 16px',
            'border': '1px solid #e8f4fd',
            'font-size': '13px',
            'font-weight': '500',
            'border-radius': '4px'
        }).set_table_styles([
            # Modern header styling
            {'selector': 'thead th', 'props': [
                ('background', 'linear-gradient(135deg, #4CAF50 0%, #45a049 100%)'),
                ('color', 'white'),
                ('font-weight', '600'),
                ('text-align', 'center'),
                ('border', 'none'),
                ('padding', '16px 12px'),
                ('font-size', '12px'),
                ('text-transform', 'uppercase'),
                ('letter-spacing', '0.5px'),
                ('box-shadow', '0 2px 4px rgba(76, 175, 80, 0.2)')
            ]},
            # Alternate row colors
            {'selector': 'tbody tr:nth-child(odd)', 'props': [
                ('background-color', '#ffffff')
            ]},
            {'selector': 'tbody tr:nth-child(even)', 'props': [
                ('background-color', '#f8fbfc')
            ]},
            # Hover effects
            {'selector': 'tbody tr:hover', 'props': [
                ('background-color', '#e8f5e8'),
                ('transform', 'scale(1.005)'),
                ('transition', 'all 0.2s ease'),
                ('box-shadow', '0 2px 8px rgba(76, 175, 80, 0.1)')
            ]},
            # Table container
            {'selector': 'table', 'props': [
                ('border-collapse', 'separate'),
                ('border-spacing', '0'),
                ('border-radius', '8px'),
                ('overflow', 'hidden'),
                ('box-shadow', '0 4px 20px rgba(0, 0, 0, 0.08)'),
                ('margin', '20px 0'),
                ('width', '100%')
            ]},
            # Cell borders
            {'selector': 'td, th', 'props': [
                ('border-bottom', '1px solid #e8f4fd'),
                ('border-right', '1px solid #e8f4fd')
            ]},
            {'selector': 'td:last-child, th:last-child', 'props': [
                ('border-right', 'none')
            ]},
            {'selector': 'tbody tr:last-child td', 'props': [
                ('border-bottom', 'none')
            ]},
            # First column (Site name) styling
            {'selector': 'td:first-child', 'props': [
                ('text-align', 'left'),
                ('font-weight', '600'),
                ('color', '#2E7D32')
            ]}
        ])
        
        # Add a container div for better spacing
        st.markdown("""
        <div style="margin: 30px 0; padding: 20px; background: linear-gradient(135deg, #f8fff9 0%, #e8f5e9 100%); border-radius: 12px; border: 1px solid #c8e6c9;">
        """, unsafe_allow_html=True)
        
        st.write(final_styled_df.to_html(escape=False), unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("📊 No performance data available for display")
    
    # === MONTHLY TRENDS SECTION ===
    st.markdown("""
    <div style="text-align: center; margin: 50px 0 30px 0;">
        <h3 style="color: #2E7D32; font-size: 24px; font-weight: 700; margin-bottom: 8px;">
            📈 Monthly Recruitment & Referral Trends
        </h3>
        <p style="color: #666; font-size: 14px; margin: 0; font-weight: 400;">
            Month-by-month average rates and changes for each site
        </p>
        <div style="width: 80px; height: 3px; background: linear-gradient(90deg, #4CAF50, #2196F3); margin: 15px auto; border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Site selector for detailed view
    st.markdown("**Select a site to view monthly trends:**")
    selected_site = st.selectbox(
        "Choose site",
        options=['All Sites'] + list(official_sites),
        key='monthly_trends_site_selector',
        label_visibility="collapsed"
    )
    
    if selected_site and selected_site != 'All Sites':
        # Show detailed monthly breakdown for selected site
        if cvlp_site_col:
            site_data = df[df[cvlp_site_col] == selected_site]
        else:
            site_data = pd.DataFrame()
        
        if len(site_data) > 0:
            # Find first screening date for this site
            first_screening_date = None
            if 'cvlp_consent' in date_columns and date_columns['cvlp_consent'] in df.columns:
                site_consent_dates = site_data[site_data[date_columns['cvlp_consent']].notna()][date_columns['cvlp_consent']]
                if len(site_consent_dates) > 0:
                    first_screening_date = site_consent_dates.min()
            
            if first_screening_date:
                # Build monthly data
                monthly_data = []
                prev_recruitment_rate = None
                prev_referral_rate = None
                
                for month in months:
                    month_end = month['end']
                    if month_end < first_screening_date:
                        continue  # Skip months before site started
                    
                    # Calculate days active up to this month
                    days_active = (month_end - first_screening_date).days
                    if days_active <= 0:
                        continue
                    
                    # Count consents up to this month
                    consents = len(site_data[
                        (site_data[date_columns['cvlp_consent']].notna()) &
                        (site_data[date_columns['cvlp_consent']] <= month_end)
                    ])
                    
                    # Count referrals up to this month
                    referrals_prescreen = 0
                    referrals_main = 0
                    if 'prescreen_referral' in date_columns:
                        referrals_prescreen = len(site_data[
                            (site_data[date_columns['prescreen_referral']].notna()) &
                            (site_data[date_columns['prescreen_referral']] <= month_end)
                        ])
                    if 'main_trial_referral' in date_columns:
                        referrals_main = len(site_data[
                            (site_data[date_columns['main_trial_referral']].notna()) &
                            (site_data[date_columns['main_trial_referral']] <= month_end)
                        ])
                    total_referrals = referrals_prescreen + referrals_main
                    
                    # Calculate rates
                    months_active = days_active / 30.44
                    avg_recruitment_rate = consents / months_active if months_active > 0 else 0
                    avg_referral_rate = total_referrals / months_active if months_active > 0 else 0
                    
                    # Calculate change from previous month
                    recruitment_change = None
                    referral_change = None
                    if prev_recruitment_rate is not None and prev_recruitment_rate > 0:
                        recruitment_change = ((avg_recruitment_rate - prev_recruitment_rate) / prev_recruitment_rate) * 100
                    if prev_referral_rate is not None and prev_referral_rate > 0:
                        referral_change = ((avg_referral_rate - prev_referral_rate) / prev_referral_rate) * 100
                    
                    monthly_data.append({
                        'Month': month['name'],
                        'Days Active': days_active,
                        'Total Consents': consents,
                        'Avg Monthly Recruitment': avg_recruitment_rate,
                        'Change (%)': recruitment_change,
                        'Total Referrals': total_referrals,
                        'Avg Monthly Referrals': avg_referral_rate,
                        'Referral Change (%)': referral_change
                    })
                    
                    prev_recruitment_rate = avg_recruitment_rate
                    prev_referral_rate = avg_referral_rate
                
                if monthly_data:
                    monthly_df = pd.DataFrame(monthly_data)
                    
                    # Display table
                    st.markdown(f"### 📊 {selected_site} - Monthly Trends")
                    
                    # Style the dataframe
                    def highlight_changes(row):
                        colors = []
                        for col in row.index:
                            if 'Change' in col:
                                val = row[col]
                                if pd.notna(val):
                                    if val > 0:
                                        colors.append('background-color: #E8F5E8; color: #2E7D32; font-weight: bold')
                                    elif val < 0:
                                        colors.append('background-color: #FFEBEE; color: #D32F2F; font-weight: bold')
                                    else:
                                        colors.append('')
                                else:
                                    colors.append('')
                            else:
                                colors.append('')
                        return colors
                    
                    styled_monthly_df = monthly_df.style.apply(highlight_changes, axis=1).format({
                        'Days Active': '{:.0f}',
                        'Total Consents': '{:.0f}',
                        'Avg Monthly Recruitment': '{:.2f}',
                        'Change (%)': lambda x: f'{x:+.1f}%' if pd.notna(x) else '-',
                        'Total Referrals': '{:.0f}',
                        'Avg Monthly Referrals': '{:.2f}',
                        'Referral Change (%)': lambda x: f'{x:+.1f}%' if pd.notna(x) else '-'
        }).set_properties(**{
            'text-align': 'center',
                        'padding': '10px',
                        'font-size': '13px'
        }).set_table_styles([
            {'selector': 'thead th', 'props': [
                            ('background', 'linear-gradient(135deg, #4CAF50, #45a049)'),
                ('color', 'white'),
                            ('font-weight', '600'),
                            ('padding', '12px'),
                            ('font-size', '12px')
                        ]},
                        {'selector': 'tbody tr:hover', 'props': [
                            ('background-color', '#f5f5f5')
                        ]},
                        {'selector': 'table', 'props': [
                            ('border-radius', '8px'),
                            ('overflow', 'hidden'),
                            ('box-shadow', '0 2px 10px rgba(0,0,0,0.1)')
                        ]}
                    ])
                    
                    st.write(styled_monthly_df.to_html(escape=False), unsafe_allow_html=True)
                    
                    # Add line charts
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig_recruitment = px.line(
                            monthly_df,
                            x='Month',
                            y='Avg Monthly Recruitment',
                            title=f'{selected_site} - Recruitment Trend',
                            markers=True
                        )
                        fig_recruitment.update_layout(height=300, showlegend=False)
                        fig_recruitment.update_traces(line_color='#4CAF50', marker_size=8)
                        st.plotly_chart(fig_recruitment, use_container_width=True)
                    
                    with col2:
                        fig_referral = px.line(
                            monthly_df,
                            x='Month',
                            y='Avg Monthly Referrals',
                            title=f'{selected_site} - Referral Trend',
                            markers=True
                        )
                        fig_referral.update_layout(height=300, showlegend=False)
                        fig_referral.update_traces(line_color='#2196F3', marker_size=8)
                        st.plotly_chart(fig_referral, use_container_width=True)
                else:
                    st.info(f"No monthly data available for {selected_site}")
            else:
                st.info(f"{selected_site} has no screening activity yet")
        else:
            st.info(f"No data available for {selected_site}")
    else:
        st.info("👆 Select a specific site above to view detailed monthly trends and changes")
    
    # Add a debug section to show detailed calculations
    with st.expander("🔍 Show Detailed Monthly Calculations"):
        st.markdown("**Detailed breakdown of calculations by site and month:**")
        
        for site in official_sites:
            # Filter data for this site (only if we have the CVLP site column)
            if cvlp_site_col:
                site_data = df[df[cvlp_site_col] == site]
            else:
                site_data = pd.DataFrame()  # Empty DataFrame if no site column found
            
            if len(site_data) > 0:
                st.markdown(f"### {site}")
                
                # Show monthly breakdown
                monthly_breakdown = []
                for month in months:
                    month_name = month['name']
                    
                    # Calculate monthly values
                    cvlp_consented = 0
                    prescreen_referred = 0
                    randomised = 0
                    
                    if 'cvlp_consent' in date_columns and date_columns['cvlp_consent'] in df.columns:
                        cvlp_consented = len(site_data[
                            (site_data[date_columns['cvlp_consent']] >= month['start']) &
                            (site_data[date_columns['cvlp_consent']] <= month['end'])
                        ])
                    
                    if 'prescreen_referral' in date_columns and date_columns['prescreen_referral'] in df.columns:
                        prescreen_referred = len(site_data[
                            (site_data[date_columns['prescreen_referral']] >= month['start']) &
                            (site_data[date_columns['prescreen_referral']] <= month['end'])
                        ])
                    
                    monthly_breakdown.append({
                        'Month': month_name,
                        'Consented to CVLP': cvlp_consented,
                        'Referred to pre-screen': prescreen_referred
                    })
                
                breakdown_df = pd.DataFrame(monthly_breakdown)
                if not breakdown_df.empty:
                    # Split into separate consent and referral tables
                    st.markdown("**📝 Monthly Consent Breakdown:**")
                    consent_breakdown = breakdown_df[['Month', 'Consented to CVLP']].copy()
                    st.dataframe(consent_breakdown, use_container_width=True)
                    
                    st.markdown("**📋 Monthly Referral Breakdown:**")
                    referral_breakdown = breakdown_df[['Month', 'Referred to pre-screen']].copy()
                    st.dataframe(referral_breakdown, use_container_width=True)
                
                # Show totals and averages
                total_consented = breakdown_df['Consented to CVLP'].sum() if not breakdown_df.empty else 0
                total_referred = breakdown_df['Referred to pre-screen'].sum() if not breakdown_df.empty else 0
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(f"Total Consented", total_consented)
                with col2:
                    st.metric(f"Total Referred", total_referred)
                
                # Calculate and show averages
                total_months = len(months)
                avg_recruitment = (total_consented / total_months) if total_months > 0 else 0
                avg_referral = (total_referred / total_months) if total_months > 0 else 0
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Avg Monthly Recruitment Rate", f"{avg_recruitment:.1f}")
                with col2:
                    st.metric("Avg Monthly Referral Rate", f"{avg_referral:.1f}")
                
                st.markdown("---")
    
    # Add summary statistics
    st.markdown("### 📈 Performance Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sites = len(performance_df)
        create_enhanced_metric_card(
            icon="🏥",
            label="Total Sites",
            value=str(total_sites),
            subtitle=f"{total_sites} sites",
            color=COLOR_PALETTE['info']
        )
    
    with col2:
        # Count sites with recent activity (< 30 days since last referral)
        active_sites = 0
        if 'Total days since last patient referred / site opened (Status)' in performance_df.columns:
            active_sites = len(performance_df[performance_df['Total days since last patient referred / site opened (Status)'] == 'GREEN'])
        active_percentage = (active_sites/total_sites*100) if total_sites > 0 else 0
        create_enhanced_metric_card(
            icon="🟢",
            label="Recently Active Sites",
            value=str(active_sites),
            subtitle=f"{active_percentage:.0f}% (< 30 days)",
            color=COLOR_PALETTE['success']
        )
    
    with col3:
        avg_recruitment = performance_df['Average monthly recruitment up to Sep-25'].mean() if 'Average monthly recruitment up to Sep-25' in performance_df.columns else 0
        create_enhanced_metric_card(
            icon="📊",
            label="Overall Avg Recruitment",
            value=f"{avg_recruitment:.2f}/month",
            subtitle="Per site up to Sep-25",
            color=COLOR_PALETTE['primary']
        )
    
    with col4:
        avg_referral = performance_df['Average monthly referrals up to Sep-25'].mean() if 'Average monthly referrals up to Sep-25' in performance_df.columns else 0
        create_enhanced_metric_card(
            icon="📋",
            label="Overall Avg Referral",
            value=f"{avg_referral:.2f}/month",
            subtitle="Per site up to Sep-25",
            color=COLOR_PALETTE['warning']
        )
    
    # Create performance visualization
    st.markdown("### 📊 Site Performance Visualization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Activity status distribution based on days since last referral
        if 'Total days since last patient referred / site opened (Status)' in performance_df.columns:
            status_counts = performance_df['Total days since last patient referred / site opened (Status)'].value_counts()
            
            # Create color mapping based on status
            color_mapping = []
            for status in status_counts.index:
                if status == 'GREEN':
                    color_mapping.append('#4CAF50')  # Green
                elif status == 'ORANGE':
                    color_mapping.append('#FF9800')  # Orange
                elif status == 'RED':
                    color_mapping.append('#F44336')  # Red
                else:
                    color_mapping.append('#9E9E9E')  # Gray for unknown
            
            fig_activity = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title='Site Activity Status Distribution'
            )
            fig_activity.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                marker_colors=color_mapping
            )
            st.plotly_chart(fig_activity, use_container_width=True)
        else:
            st.info("No activity status data available")
    
    with col2:
        # Average recruitment rate by site
        if 'Average monthly recruitment up to Sep-25' in performance_df.columns:
            chart_data = performance_df[['Site name', 'Average monthly recruitment up to Sep-25']].copy()
            chart_data = chart_data.sort_values('Average monthly recruitment up to Sep-25', ascending=True)
            
            fig_recruitment = px.bar(
                chart_data,
                x='Average monthly recruitment up to Sep-25',
                y='Site name',
                title='Average Monthly Recruitment Rate by Site',
                orientation='h',
                color='Average monthly recruitment up to Sep-25',
                color_continuous_scale='RdYlGn'
            )
            
            fig_recruitment.update_layout(
                xaxis_title='Patients per Month',
                yaxis_title='Site',
                height=max(400, len(chart_data) * 30),
                showlegend=False
            )
            
            st.plotly_chart(fig_recruitment, use_container_width=True)
        else:
            st.info("No recruitment data available")

# Call the function to display CVLP Site Performance
if st.session_state.admin_settings['show_site_performance']:
    if not processed_df.empty:
        create_cvlp_site_performance_table(processed_df, uploaded_master_file)
else:
    st.warning("No data available to show CVLP Site Performance")




# === ACHIEVEMENTS & BARRIERS SECTION ===
if st.session_state.show_achievements:
    st.markdown("""
    <div class="section-divider">
        <div class="section-divider-icon">🏆</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-header">
        🏆 Achievements & Barriers
    </div>
    """, unsafe_allow_html=True)
    
    # Achievements Section
    st.markdown("### 🎯 Achievements")
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #28a745;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.1);
    ">
        <ul style="margin: 0; padding-left: 20px; font-size: 1.1rem; line-height: 1.8;">
            <li><strong>7 patients referred</strong> to the trial</li>
            <li><strong>81% of sites opened</strong> within 5 weeks of their SIV</li>
            <li><strong>Royal Surrey</strong> have referred their first patient (4 CVLP sites have consented a patient)</li>
            <li><strong>Held focus calls</strong> with 7 sites to check progress and promote pre-screening, feedback led to discussion on expanding referral criteria and increase pre-screening referrals</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Aims for Month Ahead Section
    st.markdown("### 🎯 Aims for Month Ahead")
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #ffc107;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(255, 193, 7, 0.1);
    ">
        <ul style="margin: 0; padding-left: 20px; font-size: 1.1rem; line-height: 1.8;">
            <li>Continue to improve understanding of trial site processes/timelines following referral, particularly for new sites</li>
            <li>Continue with site opening, focusing on those that are engaging well during set up</li>
            <li>Escalation of sites that are less engaged/slow to set-up to NIHR VIP and Cancer Alliances</li>
            <li>Continue with screening log reviews for all sites open</li>
            <li>Increase promotion of pre-screening at CVLP sites</li>
            <li>Focus calls with sites regarding recruitment barriers and any successes</li>
            <li>To explore expanding CVLP referral criteria to include high risk patients</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Issues Table Section
    st.markdown("### 🚨 Issues & Barriers")
    
    # Create the issues data - All 24 records
    issues_data = [
        {
            "Issue": "Nottingham only accepting referrals from limited number of CVLP sites",
            "Category": "Trial site",
            "Date Identified": "14-Mar-25",
            "Detail": "Only accepting CVLP referrals from Lincoln and Derby & Burton. Leicester in set up with a travel time of only 45mins to Nottingham. Leicester have agreed to refer to Oxford or Cambridge as alternatives but the travel time to these sites are 1hr 45mins.",
            "Action Taken": "1. Escalated to BNT",
            "Actions Outstanding": "1. Derby & Burton to confirm participation. 2. Identify alternative CVLP sites for if they decline. 3. To monitor capacity with trial site on CVLP site opening.",
            "Resolution": "Site will likely increase cap once they have an understanding of the number of CVLP referrals they will see each month.",
            "Date Resolved": ""
        },
        {
            "Issue": "Marsden only accepting referrals from limited number of CVLP site",
            "Category": "Trial site",
            "Date Identified": "13-Feb-25",
            "Detail": "Only accepting CVLP referrals from Maidstone and Imperial",
            "Action Taken": "1. Escalated to BNT",
            "Actions Outstanding": "1. Imperial to confirm participation. 2. Identify alternative CVLP site if they decline. 3. To monitor capacity with trial site on CVLP site opening.",
            "Resolution": "Site will likely increase cap once they have an understanding of the number of CVLP referrals they will see each month. Imperial confirmed participation on 08/08/2025",
            "Date Resolved": "06/08/2025"
        },
        {
            "Issue": "CPGC missing refrigerant packs and styrofoam containers",
            "Category": "LabCorp",
            "Date Identified": "07-May-25",
            "Detail": "LabCorp did not send refrigerant packs or styrofoam containers to all CPGCs with initial shipment, risk of delays to sample shipments.",
            "Action Taken": "1. Requested LabCorp send out supplies to all CPGCs. 2. Marken to collect first patient sample (Coventry & Warwickshire/Oxford patient) and provide shipping materials. 3. Followed up with all CPGCs to confirm received supplies.",
            "Actions Outstanding": "None",
            "Resolution": "BNT confirmed error in initial shipment details on LabCorp end has been resolved, future CPGCs receiving initial shipments will receive required supplies. Refridgerant packs/containers sent out to all CPGCs missing them.",
            "Date Resolved": "20-May-25"
        },
        {
            "Issue": "Delays in consenting participants at Oxford trial site",
            "Category": "Trial site",
            "Date Identified": "14-May-25",
            "Detail": "Referral from Coventry & Warwickshire submitted on 14-May, planned with Oxford to consent pt on 15-May. PI wants to discuss pt in MDT prior to consenting. Oxford trial team did not provide details to MDT team in time for MDT and pt missed slot at MDT on 15-May, resulting in delay to consent to 22-May and delayed tissue pathway. Site staff at the Oxford trial site was not delegated on the logs to take pre-screening consent which also delayed the pathway.",
            "Action Taken": "1. BNT emailed PI to escalate 2. SCTU suggested pre-consenting the participant to begin tissue pathway sooner 3. Clarified referral pathway with Oxford trial team",
            "Actions Outstanding": "None",
            "Resolution": "PI confirmed process for discussing all potential patients at MDT on Thursdays, clinic takes place later that day and patient can be consented then. CVLP sites need to send complete referrals to the trial site by Tuesday pm at latest to be seen on Thursday in same week.",
            "Date Resolved": "22-May-25"
        },
        {
            "Issue": "LabCorp portal not permitting SCTU to register samples",
            "Category": "LabCorp",
            "Date Identified": "23-May-25",
            "Detail": "Unable to register first BNT113-01 sample, error message states that user must be assigned to the correct protocol.",
            "Action Taken": "1. Escalated to LabCorp, currently with IT team 2. Confirmed that sample has arrived at LabCorp",
            "Actions Outstanding": "1. LabCorp to resolve issue (CTU not be able to register the sample in the Labcorp portal as they only have access to the CPGC sites. The samples are assigned to the trial sites so only trial sites can register the sample) 2. SCTU to register samples when possible",
            "Resolution": "LabCorp to send SCTU Clinical Liasion reconcilations via email within 24 hours. Clinical Liason to monitor this is happening and feedback issues to BNT. Miguel to continue liasion with Labcorp to confirm receipt of sample with the SCTU for oversight. BNT/Labcorp unable to find a sustainable workaround for sample tracking",
            "Date Resolved": "01-Jul-25"
        },
        {
            "Issue": "BNT113 consent at Mount Vernon trial",
            "Category": "Trial site",
            "Date Identified": "24-Jun-25",
            "Detail": "Bedfordshire have referred 3 main trial patients to Mount Vernon. Mount Vernon have reported to SCTU that they were unaware that consent to BNT113 was required for central testing of PD-L1, mistakenly believing CVLP consent covered central testing. Patients were also of the understanding that CVLP consent covered testing of their samples. Mount Vernon report this consent step as causing a delay the SOC patient pathway whilst waiting for consent to BNT113 consent with CPGCs holding the block during this time rather than being able to proceed with SOC PD-L1 testing.",
            "Action Taken": "1. Escalated to BNT and discussion at Monthly Reporting Meeting (09-Jul-2025) 2. Meeting with Mount Vernon and BioNTech to find resolution (02-Jul-2025) 3. Have calls with trial sites when they receive their first referrals to check understanding of the pathway 4. SCTU to arrange meeting with Luton to discuss pathway",
            "Actions Outstanding": "Meeting held with Mount Vernon team on 02-Jul-2025. BNT representative unable to attend. In line with GCP, SCTU have agreed with Mount Vernon that they should offer patients referred all trials that they would be suitable for. SCTU to collect reasons why patients choose other studies where possible.",
            "Resolution": "The following has been sent to Luton and Lister CVLP sites: 1) Main trial patients must be PD-L1 positive before CVLP referral. 2) Patients with primary tumours of the larynx, hypopharynx, or oral cavity should not be referred to Mount Vernon for pre-screening or for the main trial. 3) CVLP site to hold the transfer of tissue to the CPGC until the SCTU Clinical Liaison team notifies them that the patient has provided consent for BNT113-01. 4) To focus on the pre-screening pathway where possible. 5) High risk patients should only be approached for CVLP consent and BNT113-01 pre-screening at least 12 weeks after the end of their radical initial treatment (surgery + radiotherapy/chemoradiotherapy).",
            "Date Resolved": "11/09/2025"
        },
        {
            "Issue": "Mid and South Essex stopping recruitment",
            "Category": "CVLP",
            "Date Identified": "25-Jun-25",
            "Detail": "Mid & South Essex are no longer willing to refer patients to UCLH for BNT113-01 as they believe it is too far to travel and too often for this patient population.",
            "Action Taken": "1. SCTU to offer Cambridge once open as another potential trial site.",
            "Actions Outstanding": "1. Wait for PI to return from emergency leave to discuss Cambridge further",
            "Resolution": "Site confirmed that they were now happy to refer patients to UCLH and Cambridge when they are activated.",
            "Date Resolved": "15/07/2025"
        },
        {
            "Issue": "Feedback from Leicester CPGC",
            "Category": "CPGC",
            "Date Identified": "30-Jun-25",
            "Detail": "Leicester have written the full DOB on the requisition forms when sending samples to LabCorp and therefore, LabCorp have received full DOB for two CVLP patients. LabCorp have not raised reconciliations for these issues so SCTU not immediately aware. Leicester report transport booking only offered 'ambient' or 'frozen' options. No refrigerated option was available. Leicester also report freezer packs not fitting well within the packaging provided.",
            "Action Taken": "1. Retrain Leicester on completion of the requisition form 2. Escalate to BNT during Monthly Reporting Meeting (09-Jul-2025) and Labcorp 3. Clarified process for LabCorp raising reconciliations relating to incorrect completion of the reconciliation form.",
            "Actions Outstanding": "1. Awaiting clarification from BNT on courier transport options. 2. Awaiting feedback from BNT/LabCorp on number of samples that should fit within packaging provided",
            "Resolution": "Retraining of Leicester CPGC on completion of requisition forms completed 07/08/2025",
            "Date Resolved": ""
        },
        {
            "Issue": "Bath Screening",
            "Category": "CVLP",
            "Date Identified": "01-Jul-25",
            "Detail": "No screening activity - SCTU unsure if screening log completion process is being followed.",
            "Action Taken": "1. SCTU to contact site to understand the reasons for no screening activity. 2. Encourage better engagement via e.g. attendance at drop in sessions.",
            "Actions Outstanding": "1. Continue monitoring their activity 2. Schedule calls based on activity levels",
            "Resolution": "Bath have started screening patients in the month of July. All non-modifiable, call to be held with site to discuss.",
            "Date Resolved": "02-Jul-25"
        },
        {
            "Issue": "Hull Screening",
            "Category": "CVLP",
            "Date Identified": "01-Jul-25",
            "Detail": "No screening activity - SCTU unsure if screening log completion process is being followed.",
            "Action Taken": "1. SCTU to contact site to understand the reasons for no screening activity. 2. Encourage better engagement via e.g. attendance at drop in sessions. 3. Meeting with site requested to discuss low screening activity and promote pre-screening.",
            "Actions Outstanding": "1. Continue monitoring their activity 2. Hold call to discuss performance",
            "Resolution": "CL held a focus call with Hull on 27th August to discuss performance and any barriers to recruitment. They mentioned that the CVLP pre-screening eligibility should expand to include high risk patients. Hull consented a main trial patient to the CVLP on the 02/09/2025",
            "Date Resolved": "02-Sep-25"
        },
        {
            "Issue": "Royal Surrey competing trial",
            "Category": "CVLP",
            "Date Identified": "01-Jul-25",
            "Detail": "Royal Surrey have shown limited activity with competing trials given as the reason. Royal Surrey have ORIGAMI open which includes 3 cohorts, one of which they believe competes with BNT113 (p16 +ve patients who have had 2 lines of treatment). RSH updated that Origami-4, cohort 5 is still open with 30% of its target left to recruitment, as so it is still competing with CVLP.",
            "Action Taken": "1. Escalated to BioNTech to review ORIGAMI 2. LU advised cohort 5, that was directly competing with BNT113-01, has now closed. 3. Royal Surrey contacted to clarify",
            "Actions Outstanding": "1. Monitoring impact of competing trials on recruitment",
            "Resolution": "CL held a focus call with R.Surrey, who mentioned that Origami is closed to recruitment soon. The patient is likely to choose the Origami trial, as it is not randomised and therefore patient is guaranteed of receiving the investigational drug. Ultimately, it's dependent on patient choice on which trial they choose.",
            "Date Resolved": "11-Sep-25"
        },
        {
            "Issue": "Labcorp",
            "Category": "Central Lab",
            "Date Identified": "30-Jun-25",
            "Detail": "Received a reconciliation query from Labcorp asking whether genomic testing was required. SCTU is unclear why this question was raised.",
            "Action Taken": "1. Escalate to BNT during Monthly reporting meeting (09-Jul-2025)",
            "Actions Outstanding": "1. To escalate to BNT in the monthly meeting",
            "Resolution": "SCTU has not received any reconciliation regarding genomic testing since this was raised",
            "Date Resolved": "10-Jul-25"
        },
        {
            "Issue": "SCTU email containing PID",
            "Category": "SCTU",
            "Date Identified": "30-Jun-25",
            "Detail": "SCTU forwarded email containing patient name and NHS to BNT and Labcorp",
            "Action Taken": "1. Retraining for SCTU on redacting/ensuring any PID is removed when sending information to the Sponsor/LabCorp 2. SCTU recorded this internally as a deviation",
            "Actions Outstanding": "1. To confirm whether the email chain has been deleted from BNT and Labcorp's inbox",
            "Resolution": "1. New email chain started without PID",
            "Date Resolved": "09-Jul-25"
        },
        {
            "Issue": "Patient declined CVLP due to travel costs to trial site",
            "Category": "CVLP",
            "Date Identified": "17-Jul-25",
            "Detail": "Gloucestershire patient declined participation in the CVLP trial due to reluctance to travel to the Oxford trial site. They expressed concerns about using public transport and were also unwilling to travel by taxi, due to the high out-of-pocket cost (£120 one way).",
            "Action Taken": "1. Escalated to BioNTech and NHSE",
            "Actions Outstanding": "1. SCTU to explore travel arrangement for patients who are not able to pay the costs upfront. SCTU exploring trials connect - easy patient payment system.",
            "Resolution": "ASK NK",
            "Date Resolved": ""
        },
        {
            "Issue": "Delays at trial sites following referrals for main trial consents",
            "Category": "CVLP",
            "Date Identified": "31-Jul-25",
            "Detail": "Delays at trial sites following referrals for main trial consents. Shortest referral to consent time is 6 days, average is 18 days. This, combined with LabCorp timelines, means replacing SoC testing is not viable. Delays are partly due to limited clinic availability (e.g., Oxford only holding clinics on Thursdays) and the need for two separate consents (CVLP and BNT consent) for tissue preparation.",
            "Action Taken": "",
            "Actions Outstanding": "1. To escalate to BNT in the monthly meeting on 17-Sept-2025. 2. BNT/SCTU to explore ways to reduce main trial consent timeframe. 3. Implement e-consent to accelerate pre-screening timeframes",
            "Resolution": "",
            "Date Resolved": ""
        },
        {
            "Issue": "Delays at trial sites following referrals for main trial consents",
            "Category": "CVLP",
            "Date Identified": "31-Jul-25",
            "Detail": "Delays at trial sites following referrals for main trial consents. Shortest referral to consent time is 6 days, average is 18 days. This, combined with LabCorp timelines, means replacing SoC testing is not viable. Delays are partly due to limited clinic availability (e.g., Oxford only holding clinics on Thursdays) and the need for two separate consents (CVLP and BNT consent) for tissue preparation.",
            "Action Taken": "",
            "Actions Outstanding": "1. To escalate to BNT in the monthly meeting on 17-Sept-2025. 2. BNT/SCTU to explore ways to reduce main trial consent timeframe. 3. Implement e-consent to accelerate pre-screening timeframes",
            "Resolution": "",
            "Date Resolved": ""
        },
        {
            "Issue": "Expedited testing missing on pre-screening requisition form",
            "Category": "CPGC",
            "Date Identified": "23-Jul-25",
            "Detail": "The prescreening requisition forms for the CPGC are missing a checkbox to indicate that the sample must be tested within 10–12 calendar days",
            "Action Taken": "1. Escalated to BioNTech",
            "Actions Outstanding": "1. BioNTech to update the pre-screening requisition form to include this 2. Labcorp are emailing SCTU Clinical Liaison to confirm when samples require expedited testing.",
            "Resolution": "LabCorp have updated the pre-screening requisition form to include this. CL have shared the new pre-screening requisition form with CPGC sites",
            "Date Resolved": "10-Sep-25"
        },
        {
            "Issue": "CPGC reporting affected by inability to access LabCorp investigator portal",
            "Category": "CPGC",
            "Date Identified": "06-Aug-25",
            "Detail": "SCTU cannot reliably report on timeframes for LabCorp delivering results within the agreed window as we cannot access the following information: - Date sample received at LabCorp (to confirm when clock begins for providing results) - Date result available (SCTU rely on trial sites to provide data)",
            "Action Taken": "1. MP looking into ways to share LabCorp information with SCTU team 2. MP shared report with SCTU team, does not include central testing result or date result was available",
            "Actions Outstanding": "1. SCTU to be notified when sample received at LabCorp for a CVLP patient 2. SCTU to be notified of results directly by LabCorp to prevent delays in trial sites sending results",
            "Resolution": "",
            "Date Resolved": ""
        },
        {
            "Issue": "Issues with sample collection",
            "Category": "CPGC",
            "Date Identified": "12-Aug-25",
            "Detail": "DHL failed to collect a sample from North Bristol on 12th and 13th August. Although DHL claimed the driver had arrived, the package was not collected - possibly due to going to the wrong location. Driver failed to call CPGC. The sample was finally collected on 14 August.",
            "Action Taken": "1. CL to provide LabCorp with correct addresses and contact details for all BNT113 CPGCs.",
            "Actions Outstanding": "N/A",
            "Resolution": "CL provided correct addresses and contact details to avoid issues with future collections",
            "Date Resolved": "11-Sep-25"
        },
        {
            "Issue": "Southampton Trial site capacity for accepting referrals",
            "Category": "Trial site",
            "Date Identified": "13-Aug-25",
            "Detail": "Surge in referrals and enquiries from cancer patients outside of the CVLP pathway following media coverage, adding to the team's workload. Notably, six referrals to Southampton were received within 24 hours, none were eligible",
            "Action Taken": "1. Escalated to BioNTech 2. SCTU held call with Southampton trial site on 29th August to discuss capacity.",
            "Actions Outstanding": "N/A",
            "Resolution": "Southampton trial site is limited to a maximum of four patients receiving the drug at the same time. Referrals will be turned off when treatment cap is reached. Advised team to send patient queries on CVLP directly to SCTU team to triage and support with capacity at site.",
            "Date Resolved": "29-Aug-25"
        },
        {
            "Issue": "Sample collected outside of collection window",
            "Category": "CPGC",
            "Date Identified": "29-Aug-25",
            "Detail": "DHL collected the sample outside the collection window and driver failed to wait 10 mins while the sample was being packaged. This led to driver collecting the sample much later in the day.",
            "Action Taken": "",
            "Actions Outstanding": "1. Escalated to BNT, continuing to monitor with future collections",
            "Resolution": "",
            "Date Resolved": "09-Sep-25"
        },
        {
            "Issue": "Trial sites requesting PACS transfer of radiology images",
            "Category": "Trial site",
            "Date Identified": "05-Sep-25",
            "Detail": "Two trial sites have requested PACS transfer of radiology reports from CVLP sites. While CVLP sites have not yet requested reimbursement, the additional activity represents an extra burden on them.",
            "Action Taken": "1. NHSE to consider re-imbursing the sites for this activity. SCTU will let them know the costs to approve before implementing 2. To escalate to BioNTech",
            "Actions Outstanding": "1. SCTU to discuss with trial sites and assess if PACS is a requirement for all patients, or only certain cases",
            "Resolution": "1. SCTU to gather information regarding costs and process around the PACS process and to continue monitoring any further requests",
            "Date Resolved": "16-Sep-25"
        },
        {
            "Issue": "Mount Vernon only accepting pre-screening referrals",
            "Category": "Trial site",
            "Date Identified": "01-Oct-25",
            "Detail": "Luton and Mount Vernon PI did not see the benefit of referring CVLP patients through the main trial pathway as mount Vernon see these patients as part of SoC",
            "Action Taken": "1. Held call on 01-Oct-25 to discuss with Mount Vernon and CVLP sites to consolidate an optimal pathway 2. Expanding the pre-screening pathway to high risk patients",
            "Actions Outstanding": "1. SCTU to hold focus calls with Luton and Lister CVLP sites to ensure understanding of the pre-screening pathway.",
            "Resolution": "Came to an agreement that main trial referrals are not required as Mt Vernon team will normally pick these up through SoC, just adds more work for everyone and Mt Vernon PI is still concerned that they are being funnelled into one trial instead of being offered all options. Focus is going to be on pre-screening to get PD-L1/HPV results as early as possible and then pt makes a decision at recurrence if they want to carry on with the study.",
            "Date Resolved": "01-Oct-25"
        },
        {
            "Issue": "Lincolnshire - not screened any patients",
            "Category": "CVLP",
            "Date Identified": "02/10/2025",
            "Detail": "CVLP site has been opened for 6 weeks but have not been able to screen any patients",
            "Action Taken": "",
            "Actions Outstanding": "1. SCTU to hold focus calls and check in weekly regarding screening activity",
            "Resolution": "",
            "Date Resolved": ""
        }
    ]
    
    # Create DataFrame and display as styled table
    issues_df = pd.DataFrame(issues_data)
    # Set index to start from 1 instead of 0
    issues_df.index = range(1, len(issues_df) + 1)
    
    # Style the issues table
    styled_issues = issues_df.style.set_properties(**{
        'text-align': 'left',
        'padding': '12px 16px',
        'border': '1px solid #e8f4fd',
        'font-size': '13px',
        'font-weight': '500'
    }).set_table_styles([
        # Header styling
        {'selector': 'thead th', 'props': [
            ('background', 'linear-gradient(135deg, #dc3545 0%, #c82333 100%)'),
            ('color', 'white'),
            ('font-weight', '600'),
            ('text-align', 'center'),
            ('border', 'none'),
            ('padding', '16px 12px'),
            ('font-size', '13px'),
            ('text-transform', 'uppercase'),
            ('letter-spacing', '0.5px'),
            ('box-shadow', '0 2px 4px rgba(220, 53, 69, 0.2)')
        ]},
        # Zebra striping
        {'selector': 'tbody tr:nth-child(even)', 'props': [
            ('background-color', '#f8f9fa')
        ]},
        {'selector': 'tbody tr:nth-child(odd)', 'props': [
            ('background-color', '#ffffff')
        ]},
        # Hover effects
        {'selector': 'tbody tr:hover', 'props': [
            ('background-color', '#e3f2fd'),
            ('transform', 'scale(1.01)'),
            ('box-shadow', '0 2px 8px rgba(0,0,0,0.1)')
        ]},
        # Cell borders
        {'selector': 'td, th', 'props': [
            ('border', '1px solid #dee2e6'),
            ('vertical-align', 'top')
        ]}
    ])
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #dee2e6;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    ">
    """, unsafe_allow_html=True)
    
    st.write(styled_issues.to_html(escape=False), unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Close button
    if st.button("❌ Close Achievements & Barriers", type="secondary"):
        st.session_state.show_achievements = False
        st.rerun()

# === CPGC AND TRIAL SITE SET UP SECTION ===
if st.session_state.show_cpgc_trial_setup:
    st.markdown("""
    <div class="section-divider">
        <div class="section-divider-icon">🏥</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-header">
        🏥 CPGC and Trial Site Set Up
        <div class="section-subtitle">Comprehensive overview of CPGC and Trial Site activation status and training schedules</div>
    </div>
    """, unsafe_allow_html=True)
    
    # CPGC Table
    st.markdown("### 🧬 CPGC Status")
    
    cpgc_data = [
        {
            "GLH": "Central and South",
            "CPGC": "Thames Valley (Oxford)",
            "Actual Activation Date / Planned Activation Date": "No CVLP sites mapped to CPGC",
            "Status (Active/Ready/In Set-Up/Suspended)": "In set up (No kits/disposable forceps/PCR clean)",
            "Date of BNT113-01 Training Session": "02-Apr-25"
        },
        {
            "GLH": "Central and South",
            "CPGC": "Wessex (Southampton)",
            "Actual Activation Date / Planned Activation Date": "01-May-25",
            "Status (Active/Ready/In Set-Up/Suspended)": "Active",
            "Date of BNT113-01 Training Session": "02-Apr-25"
        },
        {
            "GLH": "Central and South",
            "CPGC": "Northen West Midlands (Wolverhampton)",
            "Actual Activation Date / Planned Activation Date": "19-May-25",
            "Status (Active/Ready/In Set-Up/Suspended)": "Active",
            "Date of BNT113-01 Training Session": "02-Apr-25"
        },
        {
            "GLH": "East",
            "CPGC": "Nottingham",
            "Actual Activation Date / Planned Activation Date": "26-Jun-25",
            "Status (Active/Ready/In Set-Up/Suspended)": "Active",
            "Date of BNT113-01 Training Session": "02-Apr-25"
        },
        {
            "GLH": "East",
            "CPGC": "Leicester",
            "Actual Activation Date / Planned Activation Date": "15-May-25",
            "Status (Active/Ready/In Set-Up/Suspended)": "Active",
            "Date of BNT113-01 Training Session": "02-Apr-25"
        },
        {
            "GLH": "North East and Yorkshire",
            "CPGC": "Leeds",
            "Actual Activation Date / Planned Activation Date": "21-May-25",
            "Status (Active/Ready/In Set-Up/Suspended)": "Active",
            "Date of BNT113-01 Training Session": "02-Apr-25"
        },
        {
            "GLH": "North East and Yorkshire",
            "CPGC": "Newcastle",
            "Actual Activation Date / Planned Activation Date": "No CVLP sites mapped to CPGC",
            "Status (Active/Ready/In Set-Up/Suspended)": "Active",
            "Date of BNT113-01 Training Session": "02-Apr-25"
        },
        {
            "GLH": "North Thames",
            "CPGC": "Barts",
            "Actual Activation Date / Planned Activation Date": "01-Jul-25",
            "Status (Active/Ready/In Set-Up/Suspended)": "Active",
            "Date of BNT113-01 Training Session": "02-Apr-25"
        },
        {
            "GLH": "North Thames",
            "CPGC": "Royal Marsden",
            "Actual Activation Date / Planned Activation Date": "25-Jun-25",
            "Status (Active/Ready/In Set-Up/Suspended)": "Active",
            "Date of BNT113-01 Training Session": "02-Apr-25"
        },
        {
            "GLH": "North West",
            "CPGC": "Cheshire and Mersey (Liverpool)",
            "Actual Activation Date / Planned Activation Date": "01-Jul-25",
            "Status (Active/Ready/In Set-Up/Suspended)": "Ready",
            "Date of BNT113-01 Training Session": "02-Apr-25"
        },
        {
            "GLH": "North West",
            "CPGC": "Lancashire and South Cumbria (Morecambe Bay)",
            "Actual Activation Date / Planned Activation Date": "TBC",
            "Status (Active/Ready/In Set-Up/Suspended)": "Suspended",
            "Date of BNT113-01 Training Session": "02-Apr-25"
        },
        {
            "GLH": "North West",
            "CPGC": "Manchester",
            "Actual Activation Date / Planned Activation Date": "No CVLP sites mapped to CPGC",
            "Status (Active/Ready/In Set-Up/Suspended)": "Ready",
            "Date of BNT113-01 Training Session": "02-Apr-25"
        },
        {
            "GLH": "South East",
            "CPGC": "Kings's",
            "Actual Activation Date / Planned Activation Date": "22-May-25",
            "Status (Active/Ready/In Set-Up/Suspended)": "Active",
            "Date of BNT113-01 Training Session": "02-Apr-25"
        },
        {
            "GLH": "South East",
            "CPGC": "Maidstone & Tunbridge Wells",
            "Actual Activation Date / Planned Activation Date": "28-May-25",
            "Status (Active/Ready/In Set-Up/Suspended)": "Active",
            "Date of BNT113-01 Training Session": "02-Apr-25"
        },
        {
            "GLH": "South West",
            "CPGC": "West of England (North Bristol)",
            "Actual Activation Date / Planned Activation Date": "12-May-25",
            "Status (Active/Ready/In Set-Up/Suspended)": "Active",
            "Date of BNT113-01 Training Session": "02-Apr-25"
        },
        {
            "GLH": "South West",
            "CPGC": "Peninsula (Plymouth)",
            "Actual Activation Date / Planned Activation Date": "09-Sep-25",
            "Status (Active/Ready/In Set-Up/Suspended)": "Ready",
            "Date of BNT113-01 Training Session": "02-Apr-25"
        }
    ]
    
    # Create DataFrame and display as styled table
    cpgc_df = pd.DataFrame(cpgc_data)
    # Set index to start from 1 instead of 0
    cpgc_df.index = range(1, len(cpgc_df) + 1)
    
    # Style the CPGC table
    styled_cpgc = cpgc_df.style.set_properties(**{
        'text-align': 'left',
        'padding': '12px 16px',
        'border': '1px solid #e8f4fd',
        'font-size': '13px',
        'font-weight': '500'
    }).set_table_styles([
        # Header styling
        {'selector': 'thead th', 'props': [
            ('background', 'linear-gradient(135deg, #2E8B57 0%, #228B22 100%)'),
            ('color', 'white'),
            ('font-weight', '600'),
            ('text-align', 'center'),
            ('border', 'none'),
            ('padding', '16px 12px'),
            ('font-size', '14px')
        ]},
        # Row styling
        {'selector': 'tbody tr', 'props': [
            ('border-bottom', '1px solid #e8f4fd'),
            ('transition', 'background-color 0.2s ease')
        ]},
        # Hover effect
        {'selector': 'tbody tr:hover', 'props': [
            ('background-color', '#f8f9fa'),
            ('transform', 'scale(1.01)')
        ]},
        # Status column styling
        {'selector': 'td:nth-child(4)', 'props': [
            ('font-weight', '600'),
            ('text-align', 'center')
        ]}
    ])
    
    # Display the styled table
    st.write(styled_cpgc.to_html(escape=False), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Trial Site Table
    st.markdown("### 🏥 Trial Site Status")
    
    trial_site_data = [
        {
            "Trial Site": "Birmingham",
            "Status (Active for referrals/Ready to receive referrals/In Set-Up/Paused)": "Paused - capacity concerns, to revisit September 2025",
            "Actual Activation Date / Planned Activation Date": "TBC",
            "Date of Intro/Training Session": "07-Feb-25",
            "Date OID received": "",
            "Date C&C received (where applicable)": ""
        },
        {
            "Trial Site": "Preston",
            "Status (Active for referrals/Ready to receive referrals/In Set-Up/Paused)": "Ready",
            "Actual Activation Date / Planned Activation Date": "26-Mar-25",
            "Date of Intro/Training Session": "13-Feb-25",
            "Date OID received": "26-Mar-25",
            "Date C&C received (where applicable)": "26-Mar-25"
        },
        {
            "Trial Site": "Southampton",
            "Status (Active for referrals/Ready to receive referrals/In Set-Up/Paused)": "Active",
            "Actual Activation Date / Planned Activation Date": "19-Mar-25",
            "Date of Intro/Training Session": "24-Feb-25",
            "Date OID received": "19-Mar-25",
            "Date C&C received (where applicable)": "19-Mar-25"
        },
        {
            "Trial Site": "Velindre",
            "Status (Active for referrals/Ready to receive referrals/In Set-Up/Paused)": "Active",
            "Actual Activation Date / Planned Activation Date": "14-Apr-25",
            "Date of Intro/Training Session": "06-Feb-25",
            "Date OID received": "14-Apr-25",
            "Date C&C received (where applicable)": "14-Apr-25"
        },
        {
            "Trial Site": "Oxford",
            "Status (Active for referrals/Ready to receive referrals/In Set-Up/Paused)": "Active",
            "Actual Activation Date / Planned Activation Date": "06-May-25",
            "Date of Intro/Training Session": "13-Mar-25",
            "Date OID received": "02-May-25",
            "Date C&C received (where applicable)": "06-May-25"
        },
        {
            "Trial Site": "UCLH",
            "Status (Active for referrals/Ready to receive referrals/In Set-Up/Paused)": "Active",
            "Actual Activation Date / Planned Activation Date": "06-May-25",
            "Date of Intro/Training Session": "14-Feb-25",
            "Date OID received": "17-Apr-25",
            "Date C&C received (where applicable)": "06-May-25"
        },
        {
            "Trial Site": "Mount Vernon",
            "Status (Active for referrals/Ready to receive referrals/In Set-Up/Paused)": "Active",
            "Actual Activation Date / Planned Activation Date": "07-May-25",
            "Date of Intro/Training Session": "09-Apr-25",
            "Date OID received": "07-May-25",
            "Date C&C received (where applicable)": "07-May-25"
        },
        {
            "Trial Site": "Leeds",
            "Status (Active for referrals/Ready to receive referrals/In Set-Up/Paused)": "Active",
            "Actual Activation Date / Planned Activation Date": "13-May-25",
            "Date of Intro/Training Session": "27-Feb-25",
            "Date OID received": "09-May-25",
            "Date C&C received (where applicable)": "13-May-25"
        },
        {
            "Trial Site": "Nottingham",
            "Status (Active for referrals/Ready to receive referrals/In Set-Up/Paused)": "Ready",
            "Actual Activation Date / Planned Activation Date": "21-May-25",
            "Date of Intro/Training Session": "12-Mar-25",
            "Date OID received": "21-May-25",
            "Date C&C received (where applicable)": "21-May-25"
        },
        {
            "Trial Site": "Guys",
            "Status (Active for referrals/Ready to receive referrals/In Set-Up/Paused)": "Active",
            "Actual Activation Date / Planned Activation Date": "30-Jun-25",
            "Date of Intro/Training Session": "02-Apr-25",
            "Date OID received": "16-May-25",
            "Date C&C received (where applicable)": "16-May-25"
        },
        {
            "Trial Site": "Cambridge",
            "Status (Active for referrals/Ready to receive referrals/In Set-Up/Paused)": "In set-up",
            "Actual Activation Date / Planned Activation Date": "27-Aug-25",
            "Date of Intro/Training Session": "07-Aug-25",
            "Date OID received": "29-Jul-25",
            "Date C&C received (where applicable)": "04-Aug-25"
        },
        {
            "Trial Site": "Royal Marsden",
            "Status (Active for referrals/Ready to receive referrals/In Set-Up/Paused)": "In set-up (Refresher training session 03/10.)",
            "Actual Activation Date / Planned Activation Date": "October",
            "Date of Intro/Training Session": "13-Feb-25",
            "Date OID received": "13-May-25",
            "Date C&C received (where applicable)": ""
        },
        {
            "Trial Site": "Christie",
            "Status (Active for referrals/Ready to receive referrals/In Set-Up/Paused)": "In set-up",
            "Actual Activation Date / Planned Activation Date": "TBC",
            "Date of Intro/Training Session": "27-May-25",
            "Date OID received": "",
            "Date C&C received (where applicable)": ""
        },
        {
            "Trial Site": "Torbay",
            "Status (Active for referrals/Ready to receive referrals/In Set-Up/Paused)": "In set-up",
            "Actual Activation Date / Planned Activation Date": "TBC",
            "Date of Intro/Training Session": "09-Jul-25",
            "Date OID received": "",
            "Date C&C received (where applicable)": ""
        }
    ]
    
    # Create DataFrame and display as styled table
    trial_site_df = pd.DataFrame(trial_site_data)
    # Set index to start from 1 instead of 0
    trial_site_df.index = range(1, len(trial_site_df) + 1)
    
    # Style the Trial Site table
    styled_trial_site = trial_site_df.style.set_properties(**{
        'text-align': 'left',
        'padding': '12px 16px',
        'border': '1px solid #e8f4fd',
        'font-size': '13px',
        'font-weight': '500'
    }).set_table_styles([
        # Header styling
        {'selector': 'thead th', 'props': [
            ('background', 'linear-gradient(135deg, #4169E1 0%, #1E90FF 100%)'),
            ('color', 'white'),
            ('font-weight', '600'),
            ('text-align', 'center'),
            ('border', 'none'),
            ('padding', '16px 12px'),
            ('font-size', '14px')
        ]},
        # Row styling
        {'selector': 'tbody tr', 'props': [
            ('border-bottom', '1px solid #e8f4fd'),
            ('transition', 'background-color 0.2s ease')
        ]},
        # Hover effect
        {'selector': 'tbody tr:hover', 'props': [
            ('background-color', '#f8f9fa'),
            ('transform', 'scale(1.01)')
        ]},
        # Status column styling
        {'selector': 'td:nth-child(2)', 'props': [
            ('font-weight', '600'),
            ('text-align', 'center')
        ]}
    ])
    
    # Display the styled table
    st.write(styled_trial_site.to_html(escape=False), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Close button
    if st.button("❌ Close CPGC and Trial Site Set Up", type="secondary"):
        st.session_state.show_cpgc_trial_setup = False
        st.rerun()

# === CPGC BNT REPORTING SECTION ===
if st.session_state.show_cpgc_reporting:
    st.markdown("""
    <div class="section-divider">
        <div class="section-divider-icon">📊</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-header">
        📊 CPGC BNT Reporting
        <div class="section-subtitle">Comprehensive CPGC performance metrics, deviations, and LabCorp reporting data</div>
    </div>
    """, unsafe_allow_html=True)
    
    # CPGC BNT Reporting Table
    st.markdown("### 🧬 CPGC Performance & LabCorp Reporting")
    
    cpgc_reporting_data = [
        {
            "GLH": "Central and South",
            "CPGC": "Thames Valley (Oxford)",
            "UKAS number": "8415",
            "UKAS Issue Date": "17-Jul-25",
            "ISO Accrediation": "15189:2022",
            "UKAS Comments": "",
            "Corresponding CVLP recruiting sites": "N/A",
            "Average number of days between CVLP dispatch & CPGC receipt": "N/A",
            "Average number of days before shipment of samples": "N/A",
            "% prepared within 3 working days": "-",
            "Instances of 1st set sent >3 days from notification": "-",
            "Number of deviations / reconciliations": "",
            "Average time to resolve deviations / reconciliations": "-",
            "Average number of days to provide non-urgent results": "0",
            "Instances of non-urgent results provided outside of window": "-",
            "Average number of days to provide urgent results": "0",
            "Instances of urgent results provided outside of window": "0"
        },
        {
            "GLH": "Central and South",
            "CPGC": "Wessex (Southampton)",
            "UKAS number": "8178",
            "UKAS Issue Date": "05-Feb-25",
            "ISO Accrediation": "15189:2022",
            "UKAS Comments": "",
            "Corresponding CVLP recruiting sites": "University Hospitals Dorset",
            "Average number of days between CVLP dispatch & CPGC receipt": "N/A",
            "Average number of days before shipment of samples": "N/A",
            "% prepared within 3 working days": "-",
            "Instances of 1st set sent >3 days from notification": "-",
            "Number of deviations / reconciliations": "",
            "Average time to resolve deviations / reconciliations": "-",
            "Average number of days to provide non-urgent results": "0",
            "Instances of non-urgent results provided outside of window": "-",
            "Average number of days to provide urgent results": "0",
            "Instances of urgent results provided outside of window": "0"
        },
        {
            "GLH": "Central and South",
            "CPGC": "Northen West Midlands (Wolverhampton)",
            "UKAS number": "8665",
            "UKAS Issue Date": "22-Jul-25",
            "ISO Accrediation": "15189:2022",
            "UKAS Comments": "",
            "Corresponding CVLP recruiting sites": "Coventry & Warwickshire",
            "Average number of days between CVLP dispatch & CPGC receipt": "4.3",
            "Average number of days before shipment of samples": "0.0",
            "% prepared within 3 working days": "100.00%",
            "Instances of 1st set sent >3 days from notification": "0",
            "Number of deviations / reconciliations": "",
            "Average time to resolve deviations / reconciliations": "-",
            "Average number of days to provide non-urgent results": "0",
            "Instances of non-urgent results provided outside of window": "-",
            "Average number of days to provide urgent results": "17",
            "Instances of urgent results provided outside of window": "1"
        },
        {
            "GLH": "East",
            "CPGC": "Nottingham",
            "UKAS number": "8162",
            "UKAS Issue Date": "27-Jun-25",
            "ISO Accrediation": "15189:2022",
            "UKAS Comments": "",
            "Corresponding CVLP recruiting sites": "N/A",
            "Average number of days between CVLP dispatch & CPGC receipt": "N/A",
            "Average number of days before shipment of samples": "N/A",
            "% prepared within 3 working days": "-",
            "Instances of 1st set sent >3 days from notification": "-",
            "Number of deviations / reconciliations": "",
            "Average time to resolve deviations / reconciliations": "-",
            "Average number of days to provide non-urgent results": "0",
            "Instances of non-urgent results provided outside of window": "-",
            "Average number of days to provide urgent results": "0",
            "Instances of urgent results provided outside of window": "0"
        },
        {
            "GLH": "East",
            "CPGC": "Leicester",
            "UKAS number": "8608",
            "UKAS Issue Date": "02-Jul-25",
            "ISO Accrediation": "15189:2022",
            "UKAS Comments": "",
            "Corresponding CVLP recruiting sites": "Bedfordshire",
            "Average number of days between CVLP dispatch & CPGC receipt": "1",
            "Average number of days before shipment of samples": "1.7",
            "% prepared within 3 working days": "100.00%",
            "Instances of 1st set sent >3 days from notification": "0",
            "Number of deviations / reconciliations": "3.00",
            "Average time to resolve deviations / reconciliations": "1.00",
            "Average number of days to provide non-urgent results": "0",
            "Instances of non-urgent results provided outside of window": "-",
            "Average number of days to provide urgent results": "13.3",
            "Instances of urgent results provided outside of window": "2"
        },
        {
            "GLH": "North East and Yorkshire",
            "CPGC": "Leeds",
            "UKAS number": "9862",
            "UKAS Issue Date": "10-Jun-25",
            "ISO Accrediation": "15189:2022",
            "UKAS Comments": "",
            "Corresponding CVLP recruiting sites": "Hull / York & Scarborough",
            "Average number of days between CVLP dispatch & CPGC receipt": "N/A",
            "Average number of days before shipment of samples": "N/A",
            "% prepared within 3 working days": "-",
            "Instances of 1st set sent >3 days from notification": "-",
            "Number of deviations / reconciliations": "",
            "Average time to resolve deviations / reconciliations": "-",
            "Average number of days to provide non-urgent results": "0",
            "Instances of non-urgent results provided outside of window": "-",
            "Average number of days to provide urgent results": "0",
            "Instances of urgent results provided outside of window": "0"
        },
        {
            "GLH": "North East and Yorkshire",
            "CPGC": "Newcastle",
            "UKAS number": "8534",
            "UKAS Issue Date": "13-Jun-25",
            "ISO Accrediation": "15189:2022",
            "UKAS Comments": "",
            "Corresponding CVLP recruiting sites": "N/A",
            "Average number of days between CVLP dispatch & CPGC receipt": "N/A",
            "Average number of days before shipment of samples": "N/A",
            "% prepared within 3 working days": "-",
            "Instances of 1st set sent >3 days from notification": "-",
            "Number of deviations / reconciliations": "",
            "Average time to resolve deviations / reconciliations": "-",
            "Average number of days to provide non-urgent results": "0",
            "Instances of non-urgent results provided outside of window": "-",
            "Average number of days to provide urgent results": "0",
            "Instances of urgent results provided outside of window": "0"
        },
        {
            "GLH": "North Thames",
            "CPGC": "Barts",
            "UKAS number": "8285",
            "UKAS Issue Date": "29-Jul-25",
            "ISO Accrediation": "15189:2022",
            "UKAS Comments": "",
            "Corresponding CVLP recruiting sites": "Mid & South Essex",
            "Average number of days between CVLP dispatch & CPGC receipt": "N/A",
            "Average number of days before shipment of samples": "N/A",
            "% prepared within 3 working days": "-",
            "Instances of 1st set sent >3 days from notification": "-",
            "Number of deviations / reconciliations": "",
            "Average time to resolve deviations / reconciliations": "-",
            "Average number of days to provide non-urgent results": "0",
            "Instances of non-urgent results provided outside of window": "-",
            "Average number of days to provide urgent results": "0",
            "Instances of urgent results provided outside of window": "0"
        },
        {
            "GLH": "North Thames",
            "CPGC": "Royal Marsden",
            "UKAS number": "9929",
            "UKAS Issue Date": "07-Oct-24",
            "ISO Accrediation": "15189:2022",
            "UKAS Comments": "",
            "Corresponding CVLP recruiting sites": "N/A",
            "Average number of days between CVLP dispatch & CPGC receipt": "N/A",
            "Average number of days before shipment of samples": "N/A",
            "% prepared within 3 working days": "-",
            "Instances of 1st set sent >3 days from notification": "-",
            "Number of deviations / reconciliations": "",
            "Average time to resolve deviations / reconciliations": "-",
            "Average number of days to provide non-urgent results": "0",
            "Instances of non-urgent results provided outside of window": "-",
            "Average number of days to provide urgent results": "0",
            "Instances of urgent results provided outside of window": "0"
        },
        {
            "GLH": "North West",
            "CPGC": "Cheshire and Mersey (Liverpool)",
            "UKAS number": "7924",
            "UKAS Issue Date": "26-Jun-25",
            "ISO Accrediation": "15189:2022",
            "UKAS Comments": "",
            "Corresponding CVLP recruiting sites": "N/A",
            "Average number of days between CVLP dispatch & CPGC receipt": "N/A",
            "Average number of days before shipment of samples": "N/A",
            "% prepared within 3 working days": "-",
            "Instances of 1st set sent >3 days from notification": "-",
            "Number of deviations / reconciliations": "",
            "Average time to resolve deviations / reconciliations": "-",
            "Average number of days to provide non-urgent results": "0",
            "Instances of non-urgent results provided outside of window": "-",
            "Average number of days to provide urgent results": "0",
            "Instances of urgent results provided outside of window": "0"
        },
        {
            "GLH": "North West",
            "CPGC": "Lancashire and South Cumbria (Morecambe Bay)",
            "UKAS number": "9369",
            "UKAS Issue Date": "Suspended from 17-Dec-2024",
            "ISO Accrediation": "N/A",
            "UKAS Comments": "Not handling samples until UKAS reinstated.",
            "Corresponding CVLP recruiting sites": "",
            "Average number of days between CVLP dispatch & CPGC receipt": "N/A",
            "Average number of days before shipment of samples": "N/A",
            "% prepared within 3 working days": "-",
            "Instances of 1st set sent >3 days from notification": "-",
            "Number of deviations / reconciliations": "",
            "Average time to resolve deviations / reconciliations": "-",
            "Average number of days to provide non-urgent results": "0",
            "Instances of non-urgent results provided outside of window": "-",
            "Average number of days to provide urgent results": "0",
            "Instances of urgent results provided outside of window": "0"
        },
        {
            "GLH": "North West",
            "CPGC": "Manchester",
            "UKAS number": "8648",
            "UKAS Issue Date": "04-Mar-25",
            "ISO Accrediation": "15189:2022",
            "UKAS Comments": "",
            "Corresponding CVLP recruiting sites": "N/A",
            "Average number of days between CVLP dispatch & CPGC receipt": "N/A",
            "Average number of days before shipment of samples": "N/A",
            "% prepared within 3 working days": "-",
            "Instances of 1st set sent >3 days from notification": "-",
            "Number of deviations / reconciliations": "",
            "Average time to resolve deviations / reconciliations": "-",
            "Average number of days to provide non-urgent results": "0",
            "Instances of non-urgent results provided outside of window": "-",
            "Average number of days to provide urgent results": "0",
            "Instances of urgent results provided outside of window": "0"
        },
        {
            "GLH": "South East",
            "CPGC": "Kings's",
            "UKAS number": "9705",
            "UKAS Issue Date": "01-Nov-23",
            "ISO Accrediation": "15189:2012",
            "UKAS Comments": "",
            "Corresponding CVLP recruiting sites": "N/A",
            "Average number of days between CVLP dispatch & CPGC receipt": "N/A",
            "Average number of days before shipment of samples": "N/A",
            "% prepared within 3 working days": "-",
            "Instances of 1st set sent >3 days from notification": "-",
            "Number of deviations / reconciliations": "",
            "Average time to resolve deviations / reconciliations": "-",
            "Average number of days to provide non-urgent results": "0",
            "Instances of non-urgent results provided outside of window": "-",
            "Average number of days to provide urgent results": "0",
            "Instances of urgent results provided outside of window": "0"
        },
        {
            "GLH": "South East",
            "CPGC": "Maidstone & Tunbridge Wells",
            "UKAS number": "8062",
            "UKAS Issue Date": "23-Feb-25",
            "ISO Accrediation": "15189:2022",
            "UKAS Comments": "",
            "Corresponding CVLP recruiting sites": "Royal Surrey",
            "Average number of days between CVLP dispatch & CPGC receipt": "2",
            "Average number of days before shipment of samples": "2.0",
            "% prepared within 3 working days": "100.00%",
            "Instances of 1st set sent >3 days from notification": "0.0",
            "Number of deviations / reconciliations": "",
            "Average time to resolve deviations / reconciliations": "-",
            "Average number of days to provide non-urgent results": "0",
            "Instances of non-urgent results provided outside of window": "-",
            "Average number of days to provide urgent results": "11",
            "Instances of urgent results provided outside of window": "0"
        },
        {
            "GLH": "South West",
            "CPGC": "West of England (North Bristol)",
            "UKAS number": "8130",
            "UKAS Issue Date": "30-Jul-24",
            "ISO Accrediation": "15189:2012",
            "UKAS Comments": "",
            "Corresponding CVLP recruiting sites": "Gloucestershire / Royal United Hospitals Bath",
            "Average number of days between CVLP dispatch & CPGC receipt": "2",
            "Average number of days before shipment of samples": "8.0",
            "% prepared within 3 working days": "0.00%",
            "Instances of 1st set sent >3 days from notification": "1.0",
            "Number of deviations / reconciliations": "",
            "Average time to resolve deviations / reconciliations": "-",
            "Average number of days to provide non-urgent results": "0",
            "Instances of non-urgent results provided outside of window": "-",
            "Average number of days to provide urgent results": "5",
            "Instances of urgent results provided outside of window": "0"
        },
        {
            "GLH": "South West",
            "CPGC": "Peninsula (Plymouth)",
            "UKAS number": "9881",
            "UKAS Issue Date": "30-Jul-25",
            "ISO Accrediation": "15189:2022",
            "UKAS Comments": "",
            "Corresponding CVLP recruiting sites": "N/A",
            "Average number of days between CVLP dispatch & CPGC receipt": "N/A",
            "Average number of days before shipment of samples": "N/A",
            "% prepared within 3 working days": "-",
            "Instances of 1st set sent >3 days from notification": "-",
            "Number of deviations / reconciliations": "",
            "Average time to resolve deviations / reconciliations": "-",
            "Average number of days to provide non-urgent results": "0",
            "Instances of non-urgent results provided outside of window": "-",
            "Average number of days to provide urgent results": "0",
            "Instances of urgent results provided outside of window": "0"
        },
        {
            "GLH": "Totals / Average",
            "CPGC": "",
            "UKAS number": "",
            "UKAS Issue Date": "",
            "ISO Accrediation": "",
            "UKAS Comments": "",
            "Corresponding CVLP recruiting sites": "",
            "Average number of days between CVLP dispatch & CPGC receipt": "2.6",
            "Average number of days before shipment of samples": "2.9",
            "% prepared within 3 working days": "100.00%",
            "Instances of 1st set sent >3 days from notification": "0",
            "Number of deviations / reconciliations": "2",
            "Average time to resolve deviations / reconciliations": "1.00",
            "Average number of days to provide non-urgent results": "0",
            "Instances of non-urgent results provided outside of window": "-",
            "Average number of days to provide urgent results": "11.575",
            "Instances of urgent results provided outside of window": "3"
        }
    ]
    
    # Create DataFrame and display as styled table
    cpgc_reporting_df = pd.DataFrame(cpgc_reporting_data)
    # Set index to start from 1 instead of 0
    cpgc_reporting_df.index = range(1, len(cpgc_reporting_df) + 1)
    
    # Style the CPGC Reporting table with color-coded headers
    styled_cpgc_reporting = cpgc_reporting_df.style.set_properties(**{
        'text-align': 'left',
        'padding': '8px 12px',
        'border': '1px solid #e8f4fd',
        'font-size': '12px',
        'font-weight': '500'
    }).set_table_styles([
        # CPGC Report headers (columns 1-7) - Green
        {'selector': 'thead th:nth-child(1), thead th:nth-child(2), thead th:nth-child(3), thead th:nth-child(4), thead th:nth-child(5), thead th:nth-child(6), thead th:nth-child(7)', 'props': [
            ('background', 'linear-gradient(135deg, #2E8B57 0%, #228B22 100%)'),
            ('color', 'white'),
            ('font-weight', '600'),
            ('text-align', 'center'),
            ('border', 'none'),
            ('padding', '12px 8px'),
            ('font-size', '12px')
        ]},
        # Deviations headers (columns 8-13) - Orange
        {'selector': 'thead th:nth-child(8), thead th:nth-child(9), thead th:nth-child(10), thead th:nth-child(11), thead th:nth-child(12), thead th:nth-child(13)', 'props': [
            ('background', 'linear-gradient(135deg, #FF6B35 0%, #F7931E 100%)'),
            ('color', 'white'),
            ('font-weight', '600'),
            ('text-align', 'center'),
            ('border', 'none'),
            ('padding', '12px 8px'),
            ('font-size', '12px')
        ]},
        # LabCorp headers (columns 14-17) - Blue
        {'selector': 'thead th:nth-child(14), thead th:nth-child(15), thead th:nth-child(16), thead th:nth-child(17)', 'props': [
            ('background', 'linear-gradient(135deg, #4169E1 0%, #1E90FF 100%) !important'),
            ('color', 'white'),
            ('font-weight', '600'),
            ('text-align', 'center'),
            ('border', 'none'),
            ('padding', '12px 8px'),
            ('font-size', '12px')
        ]},
        # Row styling
        {'selector': 'tbody tr', 'props': [
            ('border-bottom', '1px solid #e8f4fd'),
            ('transition', 'background-color 0.2s ease')
        ]},
        # Hover effect
        {'selector': 'tbody tr:hover', 'props': [
            ('background-color', '#f8f9fa'),
            ('transform', 'scale(1.005)')
        ]},
        # Totals row styling
        {'selector': 'tr:last-child', 'props': [
            ('background-color', '#f0f8ff'),
            ('font-weight', 'bold'),
            ('border-top', '2px solid #4169E1')
        ]},
        # Status columns styling
        {'selector': 'td:nth-child(10), td:nth-child(11), td:nth-child(12), td:nth-child(13), td:nth-child(14), td:nth-child(15), td:nth-child(16), td:nth-child(17)', 'props': [
            ('text-align', 'center'),
            ('font-weight', '600')
        ]},
        # Ensure last column header has LabCorp blue background
        {'selector': 'thead th:last-child', 'props': [
            ('background', 'linear-gradient(135deg, #4169E1 0%, #1E90FF 100%) !important'),
            ('color', 'white !important'),
            ('font-weight', '600'),
            ('text-align', 'center'),
            ('border', 'none'),
            ('padding', '12px 8px'),
            ('font-size', '12px')
        ]}
    ])
    
    # Add category header information with color coding
    st.markdown("""
    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #8B4513;">
        <h4 style="margin: 0 0 15px 0; color: #8B4513;">📊 Table Categories:</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; font-size: 14px;">
            <div style="background: linear-gradient(135deg, #2E8B57 0%, #228B22 100%); color: white; padding: 12px; border-radius: 8px; box-shadow: 0 2px 8px rgba(46, 139, 87, 0.3);">
                <div style="font-size: 16px; font-weight: bold; margin-bottom: 5px;">🏥 CPGC Report</div>
                <div style="font-size: 12px; opacity: 0.9;">GLH, CPGC, UKAS details, CVLP sites</div>
            </div>
            <div style="background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%); color: white; padding: 12px; border-radius: 8px; box-shadow: 0 2px 8px rgba(255, 107, 53, 0.3);">
                <div style="font-size: 16px; font-weight: bold; margin-bottom: 5px;">⚠️ Deviations</div>
                <div style="font-size: 12px; opacity: 0.9;">Dispatch times, preparation rates, deviations</div>
            </div>
            <div style="background: linear-gradient(135deg, #4169E1 0%, #1E90FF 100%); color: white; padding: 12px; border-radius: 8px; box-shadow: 0 2px 8px rgba(65, 105, 225, 0.3);">
                <div style="font-size: 16px; font-weight: bold; margin-bottom: 5px;">🧪 LabCorp</div>
                <div style="font-size: 12px; opacity: 0.9;">Result delivery times and instances</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the styled table with horizontal scrolling
    st.markdown("""
    <div style="overflow-x: auto; margin: 20px 0;">
    """, unsafe_allow_html=True)
    
    st.write(styled_cpgc_reporting.to_html(escape=False), unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Close button
    if st.button("❌ Close CPGC BNT Reporting", type="secondary"):
        st.session_state.show_cpgc_reporting = False
        st.rerun()

# Signature Section with Better UI/UX
st.markdown("<br><br>", unsafe_allow_html=True)

signature_container = st.container()
with signature_container:
    st.markdown("""
        <style>
        .signature-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.2);
            text-align: center;
            margin: 20px 0;
        }
        .signature-name {
            font-size: 2.2rem;
            font-weight: 800;
            color: white;
            margin-bottom: 10px;
            letter-spacing: 0.5px;
        }
        .signature-title {
            font-size: 1.1rem;
            color: rgba(255, 255, 255, 0.95);
            margin-bottom: 25px;
            font-weight: 500;
            letter-spacing: 1.5px;
        }
        .linkedin-btn {
            display: inline-block;
            padding: 14px 35px;
            background: white;
            color: #0077b5;
            text-decoration: none;
            border-radius: 30px;
            font-weight: 700;
            font-size: 1rem;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        .linkedin-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
            color: #005582;
        }
        </style>
        
        <div class="signature-card">
            <div class="signature-name">Masood Nazari</div>
            <div class="signature-title">Data | AI | Clinical Research</div>
            <a href="https://www.linkedin.com/in/masood-nazari" target="_blank" class="linkedin-btn">
                🔗 Connect on LinkedIn
            </a>
        </div>
    """, unsafe_allow_html=True)

 
        .linkedin-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
            color: #005582;
        }
        </style>
        
        <div class="signature-card">
            <div class="signature-name">Masood Nazari</div>
            <div class="signature-title">Data | AI | Clinical Research</div>
            <a href="https://www.linkedin.com/in/masood-nazari" target="_blank" class="linkedin-btn">
                🔗 Connect on LinkedIn
            </a>
        </div>
    """, unsafe_allow_html=True)

 