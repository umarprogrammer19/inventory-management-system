import streamlit as st
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

# App title
st.title("📦 Inventory Management System")

# Sidebar Menu
menu = ["Select an option...", "Home", "Login", "Register"]
choice = st.sidebar.selectbox("Menu", options=menu, index=0)

if choice == "Select an option...":
    st.info("Please select an option from the menu on the left.")

elif choice == "Register":
    st.subheader("Create New Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if register_user(username, password):
            st.success("✅ Account created successfully!")
        else:
            st.error("❌ Username already exists.")

elif choice == "Login":
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login_user(username, password):
            st.success("✅ Login Successful!")
            st.session_state["logged_in"] = True
        else:
            st.error("❌ Invalid username or password.")

elif choice == "Home":
    st.subheader("Welcome to the Inventory Dashboard")

    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        st.subheader("Manage Products")

        # Add Product Section
        with st.expander("➕ Add New Product"):
            name = st.text_input("Product Name")
            quantity = st.number_input("Quantity", min_value=0)
            price = st.number_input("Price ($)", min_value=0.0, format="%.2f")
            if st.button("Add Product"):
                if name and quantity >= 0 and price >= 0:
                    add_product(name, quantity, price)
                    st.success(f"✅ Added **{name}** successfully!")
                else:
                    st.error("❌ Please fill all fields correctly.")

        # View Products Section
        products = get_all_products()
        st.write("### 📋 Product List")
        if products:
            for p in products:
                st.write(
                    f"📦 **{p.name}** | Quantity: `{p.quantity}` | Price: `$ {p.price:.2f}`"
                )
        else:
            st.info("No products added yet.")

        # Product Update Section
        with st.expander("✏️ Update Product Stock"):
            product_id = st.number_input("Product ID to Update", min_value=1)
            new_quantity = st.number_input("New Quantity", min_value=0)
            if st.button("Update Stock"):
                update_stock(product_id, new_quantity)
                st.success(
                    f"✅ Stock for product ID {product_id} updated to {new_quantity}."
                )

        # Product Delete Section
        with st.expander("🗑️ Delete Product"):
            product_id_to_delete = st.number_input("Product ID to Delete", min_value=1)
            if st.button("Delete Product"):
                delete_product(product_id_to_delete)
                st.success(f"✅ Product with ID {product_id_to_delete} deleted.")

        # Simulate Payment Button
        st.write("---")
        if st.button("💳 Simulate Premium Payment ($10)"):
            if simulate_payment(10):
                st.success("✅ Payment Successful. Premium Features Unlocked!")

    else:
        st.warning("🔒 Please login to access the dashboard.")
