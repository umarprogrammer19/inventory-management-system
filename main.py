import streamlit as st
import time
import pandas as pd
import plotly.express as px
from datetime import datetime
import random
from services.auth_service import register_user, login_user
from services.inventory_service import (
    add_product,
    get_all_products,
    update_stock,
    delete_product,
)
from services.payment_service import simulate_payment
from database.db import create_tables

# Initialize database tables
create_tables()

# Set page configuration
st.set_page_config(
    page_title="InventoryPro",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Define color scheme
PRIMARY_COLOR = "#4F46E5"  # Indigo
SECONDARY_COLOR = "#818CF8"  # Light indigo
SUCCESS_COLOR = "#10B981"  # Emerald
ERROR_COLOR = "#EF4444"  # Red
WARNING_COLOR = "#F59E0B"  # Amber
BG_COLOR = "#F9FAFB"  # Light gray
CARD_BG_COLOR = "#FFFFFF"  # White
TEXT_COLOR = "#1F2937"  # Dark gray
MUTED_TEXT_COLOR = "#6B7280"  # Medium gray

# Custom CSS for styling
st.markdown(f"""
<style>
    /* Base styling */
    [data-testid="stAppViewContainer"] {{
        background-color: {BG_COLOR};
    }}
    
    .stApp {{
        background-color: {BG_COLOR};
    }}
    
    /* Hide sidebar completely */
    [data-testid="stSidebar"] {{
        display: none;
    }}
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Inter', sans-serif;
        color: {TEXT_COLOR};
        font-weight: 700;
    }}
    
    p, li, div {{
        font-family: 'Inter', sans-serif;
        color: {TEXT_COLOR};
    }}
    
    /* Main container */
    .main-container {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 1rem;
    }}
    
    /* Header */
    .header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 1px solid #E5E7EB;
        margin-bottom: 2rem;
    }}
    
    .logo {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 1.5rem;
        font-weight: 700;
        color: {PRIMARY_COLOR};
    }}
    
    /* Navigation */
    .nav {{
        display: flex;
        gap: 0.5rem;
        align-items: center;
    }}
    
    .nav-button {{
        background-color: transparent;
        color: {TEXT_COLOR};
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    
    .nav-button:hover {{
        background-color: rgba(79, 70, 229, 0.1);
        color: {PRIMARY_COLOR};
    }}
    
    .nav-button.active {{
        background-color: {PRIMARY_COLOR};
        color: white;
    }}
    
    .nav-button.primary {{
        background-color: {PRIMARY_COLOR};
        color: white;
    }}
    
    .nav-button.primary:hover {{
        background-color: #4338CA;
    }}
    
    .nav-button.outline {{
        border: 1px solid {PRIMARY_COLOR};
        color: {PRIMARY_COLOR};
    }}
    
    .nav-button.outline:hover {{
        background-color: rgba(79, 70, 229, 0.1);
    }}
    
    /* Cards */
    .card {{
        background-color: {CARD_BG_COLOR};
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #E5E7EB;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    
    .card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }}
    
    .card-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        border-bottom: 1px solid #E5E7EB;
        padding-bottom: 0.75rem;
    }}
    
    .card-title {{
        font-size: 1.25rem;
        font-weight: 600;
        color: {TEXT_COLOR};
        margin: 0;
    }}
    
    .card-subtitle {{
        font-size: 0.875rem;
        color: {MUTED_TEXT_COLOR};
        margin-top: 0.25rem;
    }}
    
    /* Stat cards */
    .stats-container {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }}
    
    .stat-card {{
        background-color: {CARD_BG_COLOR};
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
        padding: 1.25rem;
        border: 1px solid #E5E7EB;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    
    .stat-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }}
    
    .stat-icon {{
        display: flex;
        align-items: center;
        justify-content: center;
        width: 3rem;
        height: 3rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }}
    
    .stat-value {{
        font-size: 1.875rem;
        font-weight: 700;
        color: {TEXT_COLOR};
        margin-bottom: 0.25rem;
    }}
    
    .stat-label {{
        font-size: 0.875rem;
        color: {MUTED_TEXT_COLOR};
    }}
    
    /* Buttons */
    .btn {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.5rem 1rem;
        font-weight: 500;
        border-radius: 0.375rem;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
        border: none;
        font-size: 0.875rem;
        gap: 0.5rem;
    }}
    
    .btn-primary {{
        background-color: {PRIMARY_COLOR};
        color: white;
    }}
    
    .btn-primary:hover {{
        background-color: #4338CA;
    }}
    
    .btn-secondary {{
        background-color: white;
        color: {TEXT_COLOR};
        border: 1px solid #E5E7EB;
    }}
    
    .btn-secondary:hover {{
        background-color: #F9FAFB;
    }}
    
    .btn-success {{
        background-color: {SUCCESS_COLOR};
        color: white;
    }}
    
    .btn-success:hover {{
        background-color: #059669;
    }}
    
    .btn-danger {{
        background-color: {ERROR_COLOR};
        color: white;
    }}
    
    .btn-danger:hover {{
        background-color: #DC2626;
    }}
    
    .btn-warning {{
        background-color: {WARNING_COLOR};
        color: white;
    }}
    
    .btn-warning:hover {{
        background-color: #D97706;
    }}
    
    .btn-icon {{
        padding: 0.5rem;
    }}
    
    /* Forms */
    .form-container {{
        background-color: {CARD_BG_COLOR};
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
        padding: 1.5rem;
        border: 1px solid #E5E7EB;
    }}
    
    .form-group {{
        margin-bottom: 1rem;
    }}
    
    .form-label {{
        display: block;
        margin-bottom: 0.5rem;
        font-weight: 500;
        color: {TEXT_COLOR};
    }}
    
    /* Alerts */
    .alert {{
        padding: 1rem;
        border-radius: 0.375rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }}
    
    .alert-success {{
        background-color: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.2);
        color: #065F46;
    }}
    
    .alert-error {{
        background-color: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.2);
        color: #B91C1C;
    }}
    
    .alert-warning {{
        background-color: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.2);
        color: #92400E;
    }}
    
    .alert-info {{
        background-color: rgba(79, 70, 229, 0.1);
        border: 1px solid rgba(79, 70, 229, 0.2);
        color: #4338CA;
    }}
    
    /* Tables */
    .custom-table {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 0.5rem;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
    }}
    
    .custom-table thead {{
        background-color: #F3F4F6;
    }}
    
    .custom-table th {{
        padding: 0.75rem 1rem;
        text-align: left;
        font-weight: 600;
        color: {TEXT_COLOR};
        border-bottom: 1px solid #E5E7EB;
    }}
    
    .custom-table td {{
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #E5E7EB;
    }}
    
    .custom-table tr:last-child td {{
        border-bottom: none;
    }}
    
    .custom-table tr:hover {{
        background-color: #F9FAFB;
    }}
    
    /* Badges */
    .badge {{
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.5rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 500;
    }}
    
    .badge-success {{
        background-color: rgba(16, 185, 129, 0.1);
        color: #065F46;
    }}
    
    .badge-warning {{
        background-color: rgba(245, 158, 11, 0.1);
        color: #92400E;
    }}
    
    .badge-danger {{
        background-color: rgba(239, 68, 68, 0.1);
        color: #B91C1C;
    }}
    
    /* Tabs */
    .custom-tabs {{
        display: flex;
        border-bottom: 1px solid #E5E7EB;
        margin-bottom: 1.5rem;
    }}
    
    .custom-tab {{
        padding: 0.75rem 1rem;
        cursor: pointer;
        border-bottom: 2px solid transparent;
        font-weight: 500;
        color: {MUTED_TEXT_COLOR};
        transition: all 0.2s ease;
    }}
    
    .custom-tab:hover {{
        color: {PRIMARY_COLOR};
    }}
    
    .custom-tab.active {{
        color: {PRIMARY_COLOR};
        border-bottom-color: {PRIMARY_COLOR};
    }}
    
    /* Animations */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .animate-fade-in {{
        animation: fadeIn 0.3s ease forwards;
    }}
    
    /* Utilities */
    .text-primary {{ color: {PRIMARY_COLOR}; }}
    .text-success {{ color: {SUCCESS_COLOR}; }}
    .text-error {{ color: {ERROR_COLOR}; }}
    .text-warning {{ color: {WARNING_COLOR}; }}
    .text-muted {{ color: {MUTED_TEXT_COLOR}; }}
    
    .bg-primary {{ background-color: {PRIMARY_COLOR}; }}
    .bg-success {{ background-color: {SUCCESS_COLOR}; }}
    .bg-error {{ background-color: {ERROR_COLOR}; }}
    .bg-warning {{ background-color: {WARNING_COLOR}; }}
    
    .flex {{ display: flex; }}
    .items-center {{ align-items: center; }}
    .justify-between {{ justify-content: space-between; }}
    .gap-2 {{ gap: 0.5rem; }}
    .gap-4 {{ gap: 1rem; }}
    
    .mt-2 {{ margin-top: 0.5rem; }}
    .mt-4 {{ margin-top: 1rem; }}
    .mb-2 {{ margin-bottom: 0.5rem; }}
    .mb-4 {{ margin-bottom: 1rem; }}
    
    .w-full {{ width: 100%; }}
    .h-full {{ height: 100%; }}
    
    .rounded {{ border-radius: 0.375rem; }}
    .rounded-full {{ border-radius: 9999px; }}
    
    .shadow {{ box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06); }}
    .shadow-md {{ box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); }}
    
    /* Custom Streamlit overrides */
    .stTextInput > div > div > input {{
        border-radius: 0.375rem;
        border: 1px solid #E5E7EB;
        padding: 0.5rem 0.75rem;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {PRIMARY_COLOR};
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
    }}
    
    .stNumberInput > div > div > input {{
        border-radius: 0.375rem;
        border: 1px solid #E5E7EB;
        padding: 0.5rem 0.75rem;
    }}
    
    .stNumberInput > div > div > input:focus {{
        border-color: {PRIMARY_COLOR};
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
    }}
    
    .stSelectbox > div > div > div {{
        border-radius: 0.375rem;
        border: 1px solid #E5E7EB;
    }}
    
    .stSelectbox > div > div > div:focus-within {{
        border-color: {PRIMARY_COLOR};
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
    }}
    
    .stButton > button {{
        border-radius: 0.375rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{display: none;}}
    footer {{display: none;}}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: #F3F4F6;
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: #D1D5DB;
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: #9CA3AF;
    }}
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'home'
if 'show_success' not in st.session_state:
    st.session_state['show_success'] = None
if 'show_error' not in st.session_state:
    st.session_state['show_error'] = None
if 'last_action_time' not in st.session_state:
    st.session_state['last_action_time'] = None
if 'is_premium' not in st.session_state:
    st.session_state['is_premium'] = False
if 'active_tab' not in st.session_state:
    st.session_state['active_tab'] = 0

# Helper functions
def navigate_to(page):
    st.session_state['current_page'] = page
    st.session_state['show_success'] = None
    st.session_state['show_error'] = None

def show_success(message):
    st.session_state['show_success'] = message
    st.session_state['last_action_time'] = time.time()

def show_error(message):
    st.session_state['show_error'] = message
    st.session_state['last_action_time'] = time.time()

def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.session_state['is_premium'] = False
    navigate_to('home')
    show_success("You have been logged out successfully")

# Icon functions (using emoji and HTML for simplicity)
def icon(name, color=None):
    icons = {
        'home': '🏠',
        'login': '🔑',
        'register': '📝',
        'dashboard': '📊',
        'inventory': '📦',
        'reports': '📈',
        'settings': '⚙️',
        'logout': '🚪',
        'add': '➕',
        'edit': '✏️',
        'delete': '🗑️',
        'search': '🔍',
        'user': '👤',
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': '📌',
        'premium': '💎',
        'money': '💰',
        'chart': '📊',
        'product': '📦',
        'stock': '📋',
        'low_stock': '⚠️',
        'value': '💵',
    }
    
    if color:
        return f'<span style="color: {color};">{icons.get(name, "")}</span>'
    return icons.get(name, "")

# Custom components
def custom_header():
    st.markdown(f"""
    <div class="header">
        <div class="logo">
            {icon('product')} InventoryPro
        </div>
        <div class="nav">
    """, unsafe_allow_html=True)
    
    # Navigation buttons based on login status
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    
    with col1:
        home_class = "active" if st.session_state['current_page'] == 'home' else ""
        if st.button(f"{icon('home')} Home", key="nav_home", 
                    help="Go to home page"):
            navigate_to('home')
    
    with col2:
        if not st.session_state['logged_in']:
            login_class = "active" if st.session_state['current_page'] == 'login' else ""
            if st.button(f"{icon('login')} Login", key="nav_login", 
                        help="Login to your account"):
                navigate_to('login')
        else:
            dashboard_class = "active" if st.session_state['current_page'] == 'dashboard' else ""
            if st.button(f"{icon('dashboard')} Dashboard", key="nav_dashboard", 
                        help="View your dashboard"):
                navigate_to('dashboard')
    
    with col3:
        if not st.session_state['logged_in']:
            register_class = "active" if st.session_state['current_page'] == 'register' else ""
            if st.button(f"{icon('register')} Register", key="nav_register", 
                        help="Create a new account"):
                navigate_to('register')
        else:
            inventory_class = "active" if st.session_state['current_page'] == 'inventory' else ""
            if st.button(f"{icon('inventory')} Inventory", key="nav_inventory", 
                        help="Manage your inventory"):
                navigate_to('inventory')
    
    with col4:
        if st.session_state['logged_in']:
            reports_class = "active" if st.session_state['current_page'] == 'reports' else ""
            if st.button(f"{icon('reports')} Reports", key="nav_reports", 
                        help="View reports and analytics"):
                navigate_to('reports')
    
    with col5:
        if st.session_state['logged_in']:
            if st.button(f"{icon('logout')} Logout", key="nav_logout", 
                        help="Log out of your account"):
                logout()
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

def custom_card(title, content, icon_name=None, icon_color=None):
    icon_html = f'<span class="card-icon">{icon(icon_name, icon_color)}</span>' if icon_name else ''
    
    st.markdown(f"""
    <div class="card animate-fade-in">
        <div class="card-header">
            <h3 class="card-title">{icon_html} {title}</h3>
        </div>
        <div class="card-content">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)

def stat_card(value, label, icon_name, icon_color, change=None):
    change_html = f'<div class="stat-change {"text-success" if change and change > 0 else "text-error" if change and change < 0 else ""}">{change:+.1f}% from last month</div>' if change is not None else ''
    
    st.markdown(f"""
    <div class="stat-card animate-fade-in">
        <div class="stat-icon" style="background-color: {icon_color}20; color: {icon_color};">
            {icon(icon_name, icon_color)}
        </div>
        <div class="stat-value">{value}</div>
        <div class="stat-label">{label}</div>
        {change_html}
    </div>
    """, unsafe_allow_html=True)

def custom_alert(message, type="info"):
    icon_map = {
        "success": "success",
        "error": "error",
        "warning": "warning",
        "info": "info"
    }
    
    st.markdown(f"""
    <div class="alert alert-{type} animate-fade-in">
        {icon(icon_map.get(type, "info"))} {message}
    </div>
    """, unsafe_allow_html=True)

def custom_button(label, type="primary", icon_name=None, key=None, help=None):
    icon_html = f'{icon(icon_name)} ' if icon_name else ''
    return st.button(f"{icon_html}{label}", key=key, help=help)

# Display notifications
def show_notifications():
    if st.session_state['show_success']:
        custom_alert(st.session_state['show_success'], "success")
        # Auto-clear message after 3 seconds
        if st.session_state['last_action_time'] and time.time() - st.session_state['last_action_time'] > 3:
            st.session_state['show_success'] = None
    
    if st.session_state['show_error']:
        custom_alert(st.session_state['show_error'], "error")
        # Auto-clear message after 3 seconds
        if st.session_state['last_action_time'] and time.time() - st.session_state['last_action_time'] > 3:
            st.session_state['show_error'] = None

# Main app structure
def main():
    # Custom header with navigation
    custom_header()
    
    # Show notifications
    show_notifications()
    
    # Main content container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Page content based on current page
    if st.session_state['current_page'] == 'home':
        render_home_page()
    elif st.session_state['current_page'] == 'login':
        render_login_page()
    elif st.session_state['current_page'] == 'register':
        render_register_page()
    elif st.session_state['current_page'] == 'dashboard' and st.session_state['logged_in']:
        render_dashboard_page()
    elif st.session_state['current_page'] == 'inventory' and st.session_state['logged_in']:
        render_inventory_page()
    elif st.session_state['current_page'] == 'reports' and st.session_state['logged_in']:
        render_reports_page()
    else:
        # If user is not logged in but tries to access protected pages
        if st.session_state['current_page'] in ['dashboard', 'inventory', 'reports'] and not st.session_state['logged_in']:
            custom_alert("🔒 Please login to access this page", "warning")
            render_login_page()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Page renderers
def render_home_page():
    # Hero section
    st.markdown(f"""
    <div class="card" style="background: linear-gradient(135deg, {PRIMARY_COLOR}, {SECONDARY_COLOR}); color: white;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div style="max-width: 60%;">
                <h1 style="color: white; font-size: 2.5rem; margin-bottom: 1rem;">Modern Inventory Management</h1>
                <p style="color: rgba(255, 255, 255, 0.9); font-size: 1.1rem; margin-bottom: 2rem;">
                    Streamline your inventory operations with our powerful, easy-to-use management system.
                    Track products, monitor stock levels, and generate insightful reports.
                </p>
                <div style="display: flex; gap: 1rem;">
                    <button class="btn btn-primary" style="background-color: white; color: {PRIMARY_COLOR};">
                        Get Started
                    </button>
                    <button class="btn" style="background-color: rgba(255, 255, 255, 0.2); color: white;">
                        Learn More
                    </button>
                </div>
            </div>
            <div style="font-size: 8rem; opacity: 0.8;">
                📦
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features section
    st.markdown("<h2 style='text-align: center; margin: 2rem 0;'>Key Features</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="card" style="height: 100%;">
            <div style="font-size: 3rem; color: {PRIMARY_COLOR}; text-align: center; margin-bottom: 1rem;">
                📊
            </div>
            <h3 style="text-align: center; margin-bottom: 0.5rem;">Real-time Dashboard</h3>
            <p style="text-align: center; color: {MUTED_TEXT_COLOR};">
                Get a comprehensive overview of your inventory with our intuitive dashboard.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="card" style="height: 100%;">
            <div style="font-size: 3rem; color: {PRIMARY_COLOR}; text-align: center; margin-bottom: 1rem;">
                📦
            </div>
            <h3 style="text-align: center; margin-bottom: 0.5rem;">Product Management</h3>
            <p style="text-align: center; color: {MUTED_TEXT_COLOR};">
                Easily add, update, and track all your products in one place.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="card" style="height: 100%;">
            <div style="font-size: 3rem; color: {PRIMARY_COLOR}; text-align: center; margin-bottom: 1rem;">
                📈
            </div>
            <h3 style="text-align: center; margin-bottom: 0.5rem;">Advanced Analytics</h3>
            <p style="text-align: center; color: {MUTED_TEXT_COLOR};">
                Generate detailed reports and gain insights into your inventory performance.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown(f"""
    <div class="card" style="text-align: center; margin-top: 2rem;">
        <h2 style="margin-bottom: 1rem;">Ready to Get Started?</h2>
        <p style="color: {MUTED_TEXT_COLOR}; margin-bottom: 1.5rem;">
            Join thousands of businesses that use InventoryPro to manage their inventory efficiently.
        </p>
        <div style="display: flex; gap: 1rem; justify-content: center;">
            <button class="btn btn-primary">Create Account</button>
            <button class="btn btn-secondary">Learn More</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_login_page():
    st.markdown(f"""
    <div class="card form-container animate-fade-in">
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 3rem; color: {PRIMARY_COLOR}; margin-bottom: 1rem;">🔑</div>
            <h2>Welcome Back</h2>
            <p style="color: {MUTED_TEXT_COLOR};">Login to access your inventory dashboard</p>
        </div>
    """, unsafe_allow_html=True)
    
    username = st.text_input("Username", key="login_username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Login", key="btn_login", use_container_width=True):
            if not username or not password:
                show_error("Please enter both username and password")
            else:
                with st.spinner("Logging in..."):
                    time.sleep(0.5)  # Simulate processing
                    if login_user(username, password):
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = username
                        show_success("Login successful!")
                        navigate_to('dashboard')
                    else:
                        show_error("Invalid username or password")
    
    with col2:
        if st.button("Register Instead", key="goto_register", use_container_width=True):
            navigate_to('register')
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_register_page():
    st.markdown(f"""
    <div class="card form-container animate-fade-in">
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 3rem; color: {PRIMARY_COLOR}; margin-bottom: 1rem;">📝</div>
            <h2>Create an Account</h2>
            <p style="color: {MUTED_TEXT_COLOR};">Sign up to start managing your inventory</p>
        </div>
    """, unsafe_allow_html=True)
    
    username = st.text_input("Username", key="reg_username", placeholder="Choose a username")
    
    col1, col2 = st.columns(2)
    with col1:
        password = st.text_input("Password", type="password", key="reg_password", placeholder="Create a password")
    with col2:
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Confirm your password")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Create Account", key="btn_register", use_container_width=True):
            if not username or not password:
                show_error("Please fill in all fields")
            elif password != confirm_password:
                show_error("Passwords do not match")
            else:
                with st.spinner("Creating your account..."):
                    time.sleep(0.5)  # Simulate processing
                    if register_user(username, password):
                        show_success("Account created successfully!")
                        # Auto-login after registration
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = username
                        navigate_to('dashboard')
                    else:
                        show_error("Username already exists")
    
    with col2:
        if st.button("Login Instead", key="goto_login", use_container_width=True):
            navigate_to('login')
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_dashboard_page():
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
        <h1>Welcome, {st.session_state['username']}!</h1>
        <div class="badge" style="background-color: {PRIMARY_COLOR}; color: white; padding: 0.5rem 1rem;">
            {icon('premium')} {"Premium" if st.session_state['is_premium'] else "Free"} Account
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Dashboard stats
    products = get_all_products()
    total_products = len(products)
    total_items = sum(p.quantity for p in products) if products else 0
    total_value = sum(p.quantity * p.price for p in products) if products else 0
    low_stock = sum(1 for p in products if p.quantity < 10) if products else 0
    
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        stat_card(total_products, "Total Products", "product", PRIMARY_COLOR, change=5.2)
    
    with col2:
        stat_card(total_items, "Items in Stock", "stock", SUCCESS_COLOR, change=2.8)
    
    with col3:
        stat_card(f"${total_value:.2f}", "Inventory Value", "money", WARNING_COLOR, change=7.5)
    
    with col4:
        stat_card(low_stock, "Low Stock Items", "low_stock", ERROR_COLOR, change=-3.1)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent activity and charts
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">{icon('chart')} Inventory Overview</h3>
            </div>
        """, unsafe_allow_html=True)
        
        if products:
            # Create data for visualization
            product_names = [p.name for p in products]
            quantities = [p.quantity for p in products]
            
            # Create a bar chart
            fig = px.bar(
                x=product_names, 
                y=quantities,
                labels={"x": "Product", "y": "Quantity"},
                title="",
                color=quantities,
                color_continuous_scale="Blues"
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(
                    showgrid=False,
                    showline=True,
                    linecolor='#E5E7EB'
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='#E5E7EB',
                    showline=True,
                    linecolor='#E5E7EB'
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add products to see your inventory overview")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="card" style="height: 100%;">
            <div class="card-header">
                <h3 class="card-title">{icon('info')} Recent Activity</h3>
            </div>
            <div style="overflow-y: auto; max-height: 300px;">
        """, unsafe_allow_html=True)
        
        if products:
            for i, p in enumerate(products[:5]):
                activity_date = datetime.now().strftime('%b %d, %Y')
                activity_time = datetime.now().strftime('%I:%M %p')
                
                st.markdown(f"""
                <div style="display: flex; gap: 1rem; padding: 0.75rem 0; border-bottom: 1px solid #E5E7EB;">
                    <div style="background-color: {PRIMARY_COLOR}20; color: {PRIMARY_COLOR}; width: 2.5rem; height: 2.5rem; border-radius: 0.5rem; display: flex; align-items: center; justify-content: center;">
                        {icon('product')}
                    </div>
                    <div>
                        <div style="font-weight: 500;">{p.name} updated</div>
                        <div style="font-size: 0.75rem; color: {MUTED_TEXT_COLOR};">{activity_date} at {activity_time}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent activity to display")
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Quick actions
    st.markdown(f"""
    <h2 style="margin: 1.5rem 0 1rem 0;">Quick Actions</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="card" style="text-align: center; cursor: pointer;" onclick="alert('Navigate to inventory')">
            <div style="font-size: 2rem; color: {PRIMARY_COLOR}; margin-bottom: 0.5rem;">
                {icon('inventory')}
            </div>
            <h3 style="margin-bottom: 0.5rem;">Manage Inventory</h3>
            <p style="font-size: 0.875rem; color: {MUTED_TEXT_COLOR};">
                Add, edit, or remove products
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Manage Inventory", key="goto_inventory", use_container_width=True):
            navigate_to('inventory')
    
    with col2:
        st.markdown(f"""
        <div class="card" style="text-align: center; cursor: pointer;" onclick="alert('Navigate to reports')">
            <div style="font-size: 2rem; color: {PRIMARY_COLOR}; margin-bottom: 0.5rem;">
                {icon('reports')}
            </div>
            <h3 style="margin-bottom: 0.5rem;">View Reports</h3>
            <p style="font-size: 0.875rem; color: {MUTED_TEXT_COLOR};">
                Analyze your inventory data
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("View Reports", key="goto_reports", use_container_width=True):
            navigate_to('reports')
    
    with col3:
        st.markdown(f"""
        <div class="card" style="text-align: center; cursor: pointer;">
            <div style="font-size: 2rem; color: {PRIMARY_COLOR}; margin-bottom: 0.5rem;">
                {icon('add')}
            </div>
            <h3 style="margin-bottom: 0.5rem;">Add Product</h3>
            <p style="font-size: 0.875rem; color: {MUTED_TEXT_COLOR};">
                Quickly add a new product
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Add Product", key="quick_add_product", use_container_width=True):
            navigate_to('inventory')
            st.session_state['active_tab'] = 1  # Set to "Add Product" tab
    
    with col4:
        st.markdown(f"""
        <div class="card" style="text-align: center; cursor: pointer;">
            <div style="font-size: 2rem; color: {PRIMARY_COLOR}; margin-bottom: 0.5rem;">
                {icon('premium')}
            </div>
            <h3 style="margin-bottom: 0.5rem;">Premium Features</h3>
            <p style="font-size: 0.875rem; color: {MUTED_TEXT_COLOR};">
                Upgrade to access premium features
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Upgrade to Premium", key="upgrade_premium", use_container_width=True):
            with st.spinner("Processing payment..."):
                time.sleep(1)
                if simulate_payment(10):
                    st.session_state['is_premium'] = True
                    show_success("Payment Successful. Premium Features Unlocked!")
                else:
                    show_error("Payment failed. Please try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_inventory_page():
    st.markdown("""
    <h1>Inventory Management</h1>
    <p style="color: #6B7280; margin-bottom: 1.5rem;">Add, update, and manage your products</p>
    """, unsafe_allow_html=True)
    
    # Custom tabs
    tabs = ["📋 Product List", "➕ Add Product", "✏️ Update Stock", "🗑️ Delete Product"]
    
    st.markdown('<div class="custom-tabs">', unsafe_allow_html=True)
    cols = st.columns(len(tabs))
    
    for i, (col, tab) in enumerate(zip(cols, tabs)):
        with col:
            active_class = "active" if st.session_state['active_tab'] == i else ""
            if st.button(tab, key=f"tab_{i}", use_container_width=True):
                st.session_state['active_tab'] = i
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab content
    if st.session_state['active_tab'] == 0:  # Product List
        render_product_list_tab()
    elif st.session_state['active_tab'] == 1:  # Add Product
        render_add_product_tab()
    elif st.session_state['active_tab'] == 2:  # Update Stock
        render_update_stock_tab()
    elif st.session_state['active_tab'] == 3:  # Delete Product
        render_delete_product_tab()

def render_product_list_tab():
    st.markdown(f"""
    <div class="card">
        <div class="card-header">
            <h3 class="card-title">{icon('inventory')} Product List</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Search functionality
    search_query = st.text_input("🔍 Search Products", placeholder="Enter product name...", key="product_search")
    
    products = get_all_products()
    if search_query:
        products = [p for p in products if search_query.lower() in p.name.lower()]
    
    if products:
        # Convert to DataFrame for better display
        data = {
            "ID": [p.id for p in products],
            "Product Name": [p.name for p in products],
            "Quantity": [p.quantity for p in products],
            "Price ($)": [f"${p.price:.2f}" for p in products],
            "Value": [f"${(p.quantity * p.price):.2f}" for p in products],
            "Status": ["Low Stock" if p.quantity < 10 else "In Stock" for p in products]
        }
        
        df = pd.DataFrame(data)
        
        # Apply styling to the dataframe
        def highlight_low_stock(val):
            if val == "Low Stock":
                return f'background-color: {ERROR_COLOR}20; color: {ERROR_COLOR}; border-radius: 9999px; padding: 0.25rem 0.5rem;'
            elif val == "In Stock":
                return f'background-color: {SUCCESS_COLOR}20; color: {SUCCESS_COLOR}; border-radius: 9999px; padding: 0.25rem 0.5rem;'
            return ""
        
        # Apply the styling
        styled_df = df.style.applymap(highlight_low_stock, subset=['Status'])
        
        # Display the styled dataframe
        st.dataframe(styled_df, use_container_width=True)
        
        # Export option
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("📥 Export to CSV", key="export_csv"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="inventory_export.csv",
                    mime="text/csv"
                )
    else:
        st.info("No products found. Add some products to get started.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_add_product_tab():
    st.markdown(f"""
    <div class="card form-container">
        <div class="card-header">
            <h3 class="card-title">{icon('add')} Add New Product</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Product Name", key="add_name", placeholder="Enter product name")
    with col2:
        category = st.selectbox("Category", ["Electronics", "Clothing", "Food", "Office Supplies", "Other"], key="add_category")
    
    col1, col2 = st.columns(2)
    with col1:
        quantity = st.number_input("Quantity", min_value=0, key="add_quantity")
    with col2:
        price = st.number_input("Price ($)", min_value=0.0, format="%.2f", key="add_price")
    
    description = st.text_area("Description (Optional)", height=100, key="add_description", placeholder="Enter product description")
    
    # Product image upload (placeholder)
    st.file_uploader("Product Image (Optional)", type=["jpg", "jpeg", "png"], key="add_image")
    
    if st.button("Add Product", key="btn_add_product", use_container_width=True):
        if not name:
            show_error("Product name is required")
        elif quantity < 0 or price < 0:
            show_error("Quantity and price must be positive values")
        else:
            with st.spinner("Adding product..."):
                time.sleep(0.5)  # Simulate processing
                add_product(name, quantity, price, description)
                show_success(f"Added {name} successfully!")
                # Clear form fields
                st.session_state["add_name"] = ""
                st.session_state["add_quantity"] = 0
                st.session_state["add_price"] = 0.0
                st.session_state["add_description"] = ""
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_update_stock_tab():
    st.markdown(f"""
    <div class="card form-container">
        <div class="card-header">
            <h3 class="card-title">{icon('edit')} Update Product Stock</h3>
        </div>
    """, unsafe_allow_html=True)
    
    products = get_all_products()
    if products:
        product_options = {f"{p.id}: {p.name}": p.id for p in products}
        selected_product = st.selectbox("Select Product", list(product_options.keys()), key="update_product")
        product_id = product_options[selected_product]
        
        # Get current quantity for the selected product
        current_quantity = next((p.quantity for p in products if p.id == product_id), 0)
        
        st.markdown(f"""
        <div class="alert alert-info">
            {icon('info')} Current quantity: <strong>{current_quantity}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        new_quantity = st.number_input("New Quantity", min_value=0, value=current_quantity, key="update_quantity")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Add Stock", key="btn_add_stock", use_container_width=True):
                with st.spinner("Updating stock..."):
                    time.sleep(0.5)  # Simulate processing
                    update_stock(product_id, current_quantity + 10)
                    show_success(f"Added 10 units to stock")
        
        with col2:
            if st.button("➖ Remove Stock", key="btn_remove_stock", use_container_width=True):
                with st.spinner("Updating stock..."):
                    time.sleep(0.5)  # Simulate processing
                    new_qty = max(0, current_quantity - 10)
                    update_stock(product_id, new_qty)
                    show_success(f"Removed 10 units from stock")
        
        if st.button("Update Stock", key="btn_update_stock", use_container_width=True):
            with st.spinner("Updating stock..."):
                time.sleep(0.5)  # Simulate processing
                update_stock(product_id, new_quantity)
                show_success(f"Stock updated to {new_quantity}")
    else:
        st.info("No products available to update")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_delete_product_tab():
    st.markdown(f"""
    <div class="card form-container">
        <div class="card-header">
            <h3 class="card-title">{icon('delete')} Delete Product</h3>
        </div>
    """, unsafe_allow_html=True)
    
    products = get_all_products()
    if products:
        product_options = {f"{p.id}: {p.name}": p.id for p in products}
        selected_product = st.selectbox("Select Product to Delete", list(product_options.keys()), key="delete_product")
        product_id = product_options[selected_product]
        
        # Get product details
        product = next((p for p in products if p.id == product_id), None)
        
        if product:
            st.markdown(f"""
            <div style="background-color: #FEF2F2; border: 1px solid #FEE2E2; border-radius: 0.375rem; padding: 1rem; margin: 1rem 0;">
                <div style="display: flex; align-items: center; gap: 0.5rem; color: #B91C1C; margin-bottom: 0.5rem;">
                    {icon('warning')} <strong>Warning</strong>
                </div>
                <p style="color: #B91C1C;">
                    You are about to delete the following product. This action cannot be undone.
                </p>
            </div>
            
            <div style="background-color: white; border: 1px solid #E5E7EB; border-radius: 0.375rem; padding: 1rem; margin: 1rem 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <strong>Product ID:</strong>
                    <span>{product.id}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <strong>Name:</strong>
                    <span>{product.name}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <strong>Quantity:</strong>
                    <span>{product.quantity}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <strong>Price:</strong>
                    <span>${product.price:.2f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            confirm = st.checkbox("I understand that this action cannot be undone", key="confirm_delete")
            
            if st.button("Delete Product", key="btn_delete_product", disabled=not confirm, use_container_width=True):
                with st.spinner("Deleting product..."):
                    time.sleep(0.5)  # Simulate processing
                    delete_product(product_id)
                    show_success(f"Product deleted successfully")
                    st.session_state["confirm_delete"] = False
        else:
            st.error("Product not found")
    else:
        st.info("No products available to delete")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_reports_page():
    st.markdown("""
    <h1>Inventory Reports</h1>
    <p style="color: #6B7280; margin-bottom: 1.5rem;">Analyze your inventory data with detailed reports</p>
    """, unsafe_allow_html=True)
    
    products = get_all_products()
    
    if not products:
        st.info("No products available to generate reports")
    else:
        # Create data for visualization
        product_names = [p.name for p in products]
        quantities = [p.quantity for p in products]
        values = [p.quantity * p.price for p in products]
        
        # Tabs for different reports
        tab1, tab2, tab3 = st.tabs(["📊 Stock Levels", "💰 Inventory Value", "📉 Low Stock Items"])
        
        with tab1:
            st.markdown(f"""
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">{icon('stock')} Current Stock Levels</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Create a bar chart with improved styling
            fig = px.bar(
                x=product_names, 
                y=quantities,
                labels={"x": "Product", "y": "Quantity"},
                title="",
                color=quantities,
                color_continuous_scale="Blues"
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(
                    showgrid=False,
                    showline=True,
                    linecolor='#E5E7EB'
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='#E5E7EB',
                    showline=True,
                    linecolor='#E5E7EB'
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Data table
            st.markdown("<h4>Stock Levels Data</h4>", unsafe_allow_html=True)
            stock_data = pd.DataFrame({
                "Product": product_names,
                "Quantity": quantities,
                "Status": ["Low Stock" if q < 10 else "In Stock" for q in quantities]
            })
            
            st.dataframe(stock_data, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown(f"""
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">{icon('money')} Inventory Value Distribution</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Create a pie chart with improved styling
            fig = px.pie(
                names=product_names,
                values=values,
                title="",
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=20, b=20),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                )
            )
            
            fig.update_traces(
                textinfo='percent+label',
                textposition='inside',
                hoverinfo='label+percent+value'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Value summary
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Value", f"${sum(values):.2f}", f"{random.uniform(2, 8):.1f}%")
            
            with col2:
                st.metric("Average Value", f"${sum(values)/len(values):.2f}", f"{random.uniform(-2, 5):.1f}%")
            
            with col3:
                st.metric("Highest Value", f"${max(values):.2f}", f"{random.uniform(0, 10):.1f}%") 
                st.metric("Highest Value", f"${max(values):.2f}", f"{random.uniform(0, 10):.1f}%")
            
            # Data table
            st.markdown("<h4>Value Distribution Data</h4>", unsafe_allow_html=True)
            value_data = pd.DataFrame({
                "Product": product_names,
                "Quantity": quantities,
                "Unit Price": [f"${p.price:.2f}" for p in products],
                "Total Value": [f"${v:.2f}" for v in values]
            })
            
            st.dataframe(value_data, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown(f"""
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">{icon('warning')} Low Stock Items</h3>
                </div>
            """, unsafe_allow_html=True)
            
            low_stock_products = [p for p in products if p.quantity < 10]
            
            if low_stock_products:
                # Create data for visualization
                low_stock_names = [p.name for p in low_stock_products]
                low_stock_quantities = [p.quantity for p in low_stock_products]
                
                # Create a horizontal bar chart with improved styling
                fig = px.bar(
                    y=low_stock_names,
                    x=low_stock_quantities,
                    labels={"y": "Product", "x": "Quantity"},
                    title="",
                    color=low_stock_quantities,
                    color_continuous_scale="Reds_r",
                    orientation='h'
                )
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=20, r=20, t=20, b=20),
                    xaxis=dict(
                        showgrid=True,
                        gridcolor='#E5E7EB',
                        showline=True,
                        linecolor='#E5E7EB'
                    ),
                    yaxis=dict(
                        showgrid=False,
                        showline=True,
                        linecolor='#E5E7EB'
                    )
                )
                
                # Add a vertical line for the threshold
                fig.add_shape(
                    type="line",
                    x0=10, y0=-0.5,
                    x1=10, y1=len(low_stock_names) - 0.5,
                    line=dict(color="red", width=2, dash="dash")
                )
                
                fig.add_annotation(
                    x=10, y=len(low_stock_names),
                    text="Low Stock Threshold",
                    showarrow=False,
                    yshift=10,
                    font=dict(color="red")
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Data table
                st.markdown("<h4>Low Stock Items</h4>", unsafe_allow_html=True)
                low_stock_data = pd.DataFrame({
                    "Product": [p.name for p in low_stock_products],
                    "Current Stock": [p.quantity for p in low_stock_products],
                    "Price": [f"${p.price:.2f}" for p in low_stock_products],
                    "Status": ["Critical" if p.quantity < 5 else "Low" for p in low_stock_products]
                })
                
                st.dataframe(low_stock_data, use_container_width=True)
                
                # Reorder recommendations
                st.markdown(f"""
                <div style="background-color: {WARNING_COLOR}10; border: 1px solid {WARNING_COLOR}20; border-radius: 0.375rem; padding: 1rem; margin-top: 1rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem; color: {WARNING_COLOR}; margin-bottom: 0.5rem;">
                        {icon('warning')} <strong>Reorder Recommendations</strong>
                    </div>
                    <p style="color: {TEXT_COLOR};">
                        The following products are running low and should be reordered soon:
                    </p>
                    <ul style="margin-top: 0.5rem;">
                """, unsafe_allow_html=True)
                
                for p in low_stock_products:
                    reorder_qty = 20 if p.quantity < 5 else 10
                    st.markdown(f"""
                    <li style="margin-bottom: 0.25rem;">
                        <strong>{p.name}</strong> - Reorder {reorder_qty} units
                    </li>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.success("No low stock items found. Your inventory is in good shape!")
            
            st.markdown('</div>', unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()