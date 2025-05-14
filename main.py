import streamlit as st
import time
import pandas as pd
from datetime import datetime
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

# Minimal CSS to center the layout and hide sidebar/branding
st.markdown("""
<style>
    /* Hide sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Center the main content */
    .main-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {display: none;}
    footer {display: none;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
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

# Navigation header
def custom_header():
    st.title("InventoryPro 📦")
    cols = st.columns(5)
    nav_items = [
        ('home', 'Home', 'nav_home', 'Go to home page'),
        ('login' if not st.session_state['logged_in'] else 'dashboard', 
         'Login' if not st.session_state['logged_in'] else 'Dashboard', 
         'nav_login' if not st.session_state['logged_in'] else 'nav_dashboard',
         'Login to your account' if not st.session_state['logged_in'] else 'View your dashboard'),
        ('register' if not st.session_state['logged_in'] else 'inventory',
         'Register' if not st.session_state['logged_in'] else 'Inventory',
         'nav_register' if not st.session_state['logged_in'] else 'nav_inventory',
         'Create a new account' if not st.session_state['logged_in'] else 'Manage your inventory'),
        ('reports' if st.session_state['logged_in'] else '',
         'Reports' if st.session_state['logged_in'] else '',
         'nav_reports' if st.session_state['logged_in'] else '',
         'View reports and analytics' if st.session_state['logged_in'] else ''),
        ('logout' if st.session_state['logged_in'] else '',
         'Logout' if st.session_state['logged_in'] else '',
         'nav_logout' if st.session_state['logged_in'] else '',
         'Log out of your account' if st.session_state['logged_in'] else '')
    ]
    
    for idx, (page, label, key, help) in enumerate(nav_items):
        if label:
            with cols[idx]:
                if st.button(label, key=key, help=help):
                    if page == 'logout':
                        logout()
                    else:
                        navigate_to(page)
    st.markdown("---")

# Display notifications
def show_notifications():
    if st.session_state['show_success']:
        st.success(st.session_state['show_success'])
        if time.time() - st.session_state['last_action_time'] > 3:
            st.session_state['show_success'] = None
    
    if st.session_state['show_error']:
        st.error(st.session_state['show_error'])
        if time.time() - st.session_state['last_action_time'] > 3:
            st.session_state['show_error'] = None

# Main app structure
def main():
    custom_header()
    show_notifications()
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    page = st.session_state['current_page']
    if page == 'home':
        render_home_page()
    elif page == 'login':
        render_login_page()
    elif page == 'register':
        render_register_page()
    elif page == 'dashboard' and st.session_state['logged_in']:
        render_dashboard_page()
    elif page == 'inventory' and st.session_state['logged_in']:
        render_inventory_page()
    elif page == 'reports' and st.session_state['logged_in']:
        render_reports_page()
    else:
        st.error("Please login to access this page")
        render_login_page()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Page renderers
def render_home_page():
    st.header("Welcome to InventoryPro")
    st.write("Streamline your inventory operations with our easy-to-use management system.")
    
    st.subheader("Key Features")
    cols = st.columns(3)
    with cols[0]:
        st.write("📊 **Real-time Dashboard**")
        st.write("Get a comprehensive overview of your inventory.")
    with cols[1]:
        st.write("📦 **Product Management**")
        st.write("Easily add, update, and track your products.")
    with cols[2]:
        st.write("📈 **Advanced Analytics**")
        st.write("Generate detailed reports and insights.")

def render_login_page():
    st.header("Login")
    with st.form(key="login_form"):
        username = st.text_input("Username", placeholder="Enter your username", key="login_username")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Login")
        with col2:
            if st.form_submit_button("Register Instead"):
                navigate_to('register')
        
        if submit:
            if not username or not password:
                show_error("Please fill in all fields")
            else:
                with st.spinner("Logging in..."):
                    time.sleep(0.5)
                    if login_user(username, password):
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = username
                        show_success("Login successful!")
                        navigate_to('dashboard')
                    else:
                        show_error("Invalid username or password")

def render_register_page():
    st.header("Register")
    with st.form(key="register_form"):
        username = st.text_input("Username", placeholder="Choose a username", key="reg_username")
        col1, col2 = st.columns(2)
        with col1:
            password = st.text_input("Password", type="password", placeholder="Create a password", key="reg_password")
        with col2:
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="reg_confirm")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Create Account")
        with col2:
            if st.form_submit_button("Login Instead"):
                navigate_to('login')
        
        if submit:
            if not all([username, password, confirm_password]):
                show_error("Please fill in all fields")
            elif password != confirm_password:
                show_error("Passwords do not match")
            else:
                with st.spinner("Creating account..."):
                    time.sleep(0.5)
                    if register_user(username, password):
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = username
                        show_success("Account created successfully!")
                        navigate_to('dashboard')
                    else:
                        show_error("Username already exists")

def render_dashboard_page():
    st.header(f"Welcome, {st.session_state['username']}!")
    st.write(f"Account Type: {'Premium' if st.session_state['is_premium'] else 'Free'}")
    
    products = get_all_products()
    total_products = len(products)
    total_items = sum(p.quantity for p in products) if products else 0
    total_value = sum(p.quantity * p.price for p in products) if products else 0
    low_stock = sum(1 for p in products if p.quantity < 10) if products else 0
    
    cols = st.columns(4)
    with cols[0]:
        st.metric("Total Products", total_products)
    with cols[1]:
        st.metric("Items in Stock", total_items)
    with cols[2]:
        st.metric("Inventory Value", f"${total_value:.2f}")
    with cols[3]:
        st.metric("Low Stock Items", low_stock)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Inventory Overview")
        if products:
            df = pd.DataFrame({
                "Product": [p.name for p in products],
                "Quantity": [p.quantity for p in products]
            })
            st.dataframe(df)
        else:
            st.info("Add products to see your inventory overview")
    
    with col2:
        st.subheader("Recent Activity")
        if products:
            for p in products[:5]:
                st.write(f"- {p.name}: {p.quantity} units")
        else:
            st.info("No recent activity")

def render_inventory_page():
    st.header("Inventory Management")
    tab1, tab2, tab3, tab4 = st.tabs(["Product List", "Add Product", "Update Stock", "Delete Product"])
    
    with tab1:
        render_product_list_tab()
    with tab2:
        render_add_product_tab()
    with tab3:
        render_update_stock_tab()
    with tab4:
        render_delete_product_tab()

def render_product_list_tab():
    st.subheader("Product List")
    search_query = st.text_input("Search Products", placeholder="Enter product name...", key="product_search")
    products = get_all_products()
    
    if search_query:
        products = [p for p in products if search_query.lower() in p.name.lower()]
    
    if products:
        df = pd.DataFrame({
            "ID": [p.id for p in products],
            "Name": [p.name for p in products],
            "Quantity": [p.quantity for p in products],
            "Price": [f"${p.price:.2f}" for p in products],
            "Status": ["Low Stock" if p.quantity < 10 else "In Stock" for p in products]
        })
        st.dataframe(df, use_container_width=True)
        
        col1, _ = st.columns([1, 5])
        with col1:
            if st.button("Export to CSV", key="export_csv"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="inventory_export.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    else:
        st.info("No products found")

def render_add_product_tab():
    st.subheader("Add Product")
    with st.form(key="add_product_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Product Name", placeholder="Enter product name", key="add_name")
        with col2:
            category = st.selectbox("Category", ["Electronics", "Clothing", "Food", "Office Supplies", "Other"], key="add_category")
        
        col1, col2 = st.columns(2)
        with col1:
            quantity = st.number_input("Quantity", min_value=0, step=1, key="add_quantity")
        with col2:
            price = st.number_input("Price ($)", min_value=0.0, step=0.01, format="%.2f", key="add_price")
        
        description = st.text_area("Description (Optional)", placeholder="Enter product description", key="add_description")
        
        if st.form_submit_button("Add Product"):
            if not name:
                show_error("Product name is required")
            elif quantity < 0 or price < 0:
                show_error("Quantity and price must be positive")
            else:
                with st.spinner("Adding product..."):
                    time.sleep(0.5)
                    add_product(name, quantity, price, description)
                    show_success(f"Added {name} successfully")
                    st.session_state["add_name"] = ""
                    st.session_state["add_category"] = "Electronics"
                    st.session_state["add_quantity"] = 0
                    st.session_state["add_price"] = 0.0
                    st.session_state["add_description"] = ""

def render_update_stock_tab():
    st.subheader("Update Stock")
    products = get_all_products()
    if products:
        product_options = {f"{p.id}: {p.name}" : p.id for p in products}
        with st.form(key="update_stock_form"):
            selected_product = st.selectbox("Select Product", list(product_options.keys()), key="update_product")
            product_id = product_options[selected_product]
            
            current_quantity = next((p.quantity for p in products if p.id == product_id), 0)
            st.write(f"Current quantity: {current_quantity}")
            
            new_quantity = st.number_input("New Quantity", min_value=0, value=current_quantity, step=1, key="update_quantity")
            
            if st.form_submit_button("Update Stock"):
                with st.spinner("Updating stock..."):
                    time.sleep(0.5)
                    update_stock(product_id, new_quantity)
                    show_success(f"Stock updated to {new_quantity}")
    else:
        st.info("No products available to update")

def render_delete_product_tab():
    st.subheader("Delete Product")
    products = get_all_products()
    if products:
        product_options = {f"{p.id}: {p.name}" : p.id for p in products}
        with st.form(key="delete_product_form"):
            selected_product = st.selectbox("Select Product", list(product_options.keys()), key="delete_product")
            product_id = product_options[selected_product]
            
            product = next((p for p in products if p.id == product_id), None)
            if product:
                st.write(f"**Name:** {product.name}")
                st.write(f"**Quantity:** {product.quantity}")
                st.write(f"**Price:** ${product.price:.2f}")
                
                confirm = st.checkbox("I confirm I want to delete this product", key="confirm_delete")
                if st.form_submit_button("Delete Product", disabled=not confirm):
                    with st.spinner("Deleting product..."):
                        time.sleep(0.5)
                        delete_product(product_id)
                        show_success("Product deleted successfully")
                        st.session_state["confirm_delete"] = False
    else:
        st.info("No products available to delete")

def render_reports_page():
    st.header("Reports")
    products = get_all_products()
    if not products:
        st.info("No products available to generate reports")
        return
    
    tab1, tab2, tab3 = st.tabs(["Stock Levels", "Inventory Value", "Low Stock"])
    
    with tab1:
        st.subheader("Stock Levels")
        if products:
            df = pd.DataFrame({
                "Product": [p.name for p in products],
                "Quantity": [p.quantity for p in products]
            })
            st.dataframe(df)
    
    with tab2:
        st.subheader("Inventory Value")
        if products:
            values = [p.quantity * p.price for p in products]
            df = pd.DataFrame({
                "Product": [p.name for p in products],
                "Value": values
            })
            st.dataframe(df)
    
    with tab3:
        st.subheader("Low Stock")
        low_stock = [p for p in products if p.quantity < 10]
        if low_stock:
            df = pd.DataFrame({
                "Product": [p.name for p in low_stock],
                "Quantity": [p.quantity for p in low_stock]
            })
            st.dataframe(df)
        else:
            st.success("No low stock items found")

if __name__ == "__main__":
    main()