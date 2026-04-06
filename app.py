import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta
import numpy as np
import hashlib
import json
import os

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="Pharmacy Dashboard",
    page_icon="💊",
    layout="wide"
)

# ====================== SESSION STATE ======================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'show_signup' not in st.session_state:
    st.session_state.show_signup = False
if 'filter_start_date' not in st.session_state:
    st.session_state.filter_start_date = None
if 'filter_end_date' not in st.session_state:
    st.session_state.filter_end_date = None

# ====================== USER DATABASE ======================
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def format_large_number(value):
    """Format large numbers with K (thousands) or M (millions) notation"""
    if value >= 1_000_000:
        return f"₵{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"₵{value/1_000:.1f}K"
    else:
        return f"₵{value:,.2f}"

if 'users' not in st.session_state:
    st.session_state.users = load_users()

# ====================== CUSTOM CSS ======================
st.markdown("""
<style>
    .main {background-color: #f8f9fa;}
    .stMetric {background-color: white; padding: 18px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);}
    h1, h2, h3 {color: #1e40af;}
    .stButton>button {background-color: #3b82f6; color: white;}
</style>
""", unsafe_allow_html=True)

# ====================== AUTHENTICATION ======================
def login_page():
    st.title("💊 Pharmacy Management System")
    st.subheader("Sign In to Continue")

    col_login, col_image = st.columns([1, 1])
    with col_login:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("🔑 Sign In", use_container_width=True):
            if username and password:
                users = st.session_state.users
                if username in users and users[username] == hash_password(password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.warning("Please enter username and password")

    with col_image:
        st.markdown("### Welcome!")
        st.markdown("Manage your pharmacy sales, inventory, and profits efficiently.")

    if st.button("Don't have an account? Sign Up"):
        st.session_state.show_signup = True
        st.rerun()

def signup_page():
    st.title("💊 Create New Account")
    st.subheader("Sign Up")

    new_username = st.text_input("Choose Username", key="signup_user")
    new_password = st.text_input("Choose Password", type="password", key="signup_pass")
    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_pass")

    if st.button("Create Account", use_container_width=True):
        if not new_username or not new_password:
            st.error("Username and password are required")
        elif new_password != confirm_password:
            st.error("Passwords do not match")
        elif len(new_password) < 6:
            st.error("Password must be at least 6 characters long")
        elif new_username in st.session_state.users:
            st.error("Username already exists")
        else:
            hashed_pw = hash_password(new_password)
            st.session_state.users[new_username] = hashed_pw
            save_users(st.session_state.users)
            st.success("✅ Account created successfully!")
            st.session_state.show_signup = False
            st.rerun()

    if st.button("Back to Login"):
        st.session_state.show_signup = False
        st.rerun()

# ====================== MAIN DASHBOARD ======================
if not st.session_state.logged_in:
    if st.session_state.show_signup:
        signup_page()
    else:
        login_page()
else:
    with st.sidebar:
        st.success(f"👤 Logged in as: **{st.session_state.username}**")
        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

    st.title("💊 Pharmacy Sales & Inventory Dashboard")
    st.markdown(f"**Welcome, {st.session_state.username}!**")

    # ====================== DATA LOADING ======================
    st.sidebar.header("📁 Data Source")
    
    with st.sidebar.expander("📋 Supported File Formats & Requirements"):
        st.markdown("""
**Supported Files:**
- `.csv`
- `.xls`
- `.xlsx` (Excel)

**Required Columns:**
- `date`
- `medication`
- `quantity_sold`
- `unit_price`
- `payment_method`

**Optional Columns:**
- `category`, `initial_stock`, `total_price`, `sale_id`

**Currency:** Ghana Cedis (₵)
        """)

    uploaded_file = st.sidebar.file_uploader(
        "Upload your sales data", 
        type=["csv", "xls", "xlsx"],
        help="Supports CSV and Excel files"
    )

    if uploaded_file is not None:
        try:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension == 'csv':
                df = pd.read_csv(uploaded_file)
            else:
                # For .xls and .xlsx
                df = pd.read_excel(uploaded_file)
            
            # Required columns check
            required = ['date', 'medication', 'quantity_sold', 'unit_price', 'payment_method']
            missing = [col for col in required if col not in df.columns]
            
            if missing:
                st.error(f"❌ Missing required columns: {missing}")
                st.info("Please check the file format requirements in the sidebar.")
                st.stop()

            # Safe date conversion
            df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
            
            if df['date'].isnull().any():
                st.error("❌ Some dates could not be parsed. Please use YYYY-MM-DD format in your file.")
                st.stop()

            # Auto-calculate total_price if missing
            if 'total_price' not in df.columns:
                df['total_price'] = (df['quantity_sold'] * df['unit_price']).round(2)

            if 'category' not in df.columns:
                df['category'] = 'General'
            if 'initial_stock' not in df.columns:
                df['initial_stock'] = 200

            st.sidebar.success(f"✅ {uploaded_file.name} loaded successfully!")
            
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.error("Please make sure your file has the correct columns and format.")
            st.stop()
    else:
        # Sample Data (when no file uploaded)
        st.sidebar.info("Using sample data")
        np.random.seed(42)
        n = 2000
        dates = pd.date_range('2025-03-01', periods=90).date
        meds = ['Paracetamol 500mg', 'Amoxicillin 500mg', 'Ibuprofen 400mg', 'Vitamin D3', 
                'Cetirizine 10mg', 'Omeprazole 20mg', 'Metformin 500mg', 'Amlodipine 5mg']
        
        data = {
            'sale_id': range(1, n+1),
            'date': np.random.choice(dates, n),
            'medication': np.random.choice(meds, n),
            'category': np.random.choice(['Pain Relief','Antibiotics','Vitamins','Allergy','Gastro','Diabetes','Cardiovascular'], n),
            'quantity_sold': np.random.randint(1, 25, n),
            'unit_price': np.round(np.random.uniform(15, 250, n), 2),
            'payment_method': np.random.choice(['Cash','Card','Mobile Money','Insurance'], n)
        }
        df = pd.DataFrame(data)
        df['total_price'] = (df['quantity_sold'] * df['unit_price']).round(2)
        
        unique_meds = df['medication'].unique()
        df['initial_stock'] = df['medication'].map({med: np.random.randint(80, 800) for med in unique_meds})

    df['month'] = pd.to_datetime(df['date']).dt.to_period('M').astype(str)
    min_date = df['date'].min()
    max_date = df['date'].max()

    # ====================== FILTERS ======================
    st.sidebar.header("🔍 Filters")
    col1, col2 = st.sidebar.columns(2)
    
    # Clamp session state filter dates to ensure they're within the current data range
    if st.session_state.filter_start_date:
        st.session_state.filter_start_date = max(min(st.session_state.filter_start_date, max_date), min_date)
    if st.session_state.filter_end_date:
        st.session_state.filter_end_date = max(min(st.session_state.filter_end_date, max_date), min_date)
    
    # Default values using session state (ensure within data range)
    default_start_calc = max_date - timedelta(days=29)
    default_start = st.session_state.filter_start_date if st.session_state.filter_start_date else max(default_start_calc, min_date)
    default_end = st.session_state.filter_end_date if st.session_state.filter_end_date else max_date
    
    start_date = col1.date_input("Start Date", value=default_start, 
                                min_value=min_date, max_value=max_date)
    end_date = col2.date_input("End Date", value=default_end, 
                              min_value=min_date, max_value=max_date)

    st.sidebar.subheader("Quick Selection")
    c1, c2, c3, c4 = st.sidebar.columns(4)
    if c1.button("Today", use_container_width=True):
        st.session_state.filter_start_date = max_date
        st.session_state.filter_end_date = max_date
        st.rerun()
    if c2.button("Yesterday", use_container_width=True):
        yesterday = max_date - timedelta(days=1)
        st.session_state.filter_start_date = yesterday
        st.session_state.filter_end_date = yesterday
        st.rerun()
    if c3.button("Last 7 Days", use_container_width=True):
        start_calc = max_date - timedelta(days=6)
        st.session_state.filter_start_date = max(start_calc, min_date)
        st.session_state.filter_end_date = max_date
        st.rerun()
    if c4.button("Last 30 Days", use_container_width=True):
        start_calc = max_date - timedelta(days=29)
        st.session_state.filter_start_date = max(start_calc, min_date)
        st.session_state.filter_end_date = max_date
        st.rerun()

    selected_categories = st.sidebar.multiselect("Category", options=['All'] + sorted(df['category'].unique()), default=['All'])
    selected_payments = st.sidebar.multiselect("Payment Method", options=['All'] + sorted(df['payment_method'].unique()), default=['All'])

    st.sidebar.subheader("📦 Inventory")
    selected_medications = st.sidebar.multiselect("Medication", options=['All'] + sorted(df['medication'].unique()), default=['All'])
    
    stock_status_filter = st.sidebar.multiselect("Stock Status", 
                                               options=['OK', 'Low Stock', 'Critical'], 
                                               default=['OK', 'Low Stock', 'Critical'])

    # ====================== FILTERED DATA & INVENTORY ======================
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)].copy()
    
    # Apply category filter
    if 'All' not in selected_categories:
        filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]
    
    # Apply payment method filter
    if 'All' not in selected_payments:
        filtered_df = filtered_df[filtered_df['payment_method'].isin(selected_payments)]
    
    # Apply medication filter
    if 'All' not in selected_medications:
        filtered_df = filtered_df[filtered_df['medication'].isin(selected_medications)]
    
    # Calculate profit (assuming 30% profit margin)
    filtered_df['profit'] = filtered_df['total_price'] * 0.30
    df['profit'] = df['total_price'] * 0.30
    
    # ====================== INVENTORY CALCULATIONS ======================
    # Calculate current stock for each medication
    inventory_summary = df.groupby('medication').agg({
        'quantity_sold': 'sum',
        'initial_stock': 'first'
    }).reset_index()
    inventory_summary['current_stock'] = inventory_summary['initial_stock'] - inventory_summary['quantity_sold']
    
    # Define stock status thresholds
    LOW_STOCK_THRESHOLD = 50
    CRITICAL_STOCK_THRESHOLD = 20
    
    def get_stock_status(stock_level):
        if stock_level <= CRITICAL_STOCK_THRESHOLD:
            return 'Critical'
        elif stock_level <= LOW_STOCK_THRESHOLD:
            return 'Low Stock'
        else:
            return 'OK'
    
    inventory_summary['stock_status'] = inventory_summary['current_stock'].apply(get_stock_status)

    # ====================== DASHBOARD METRICS ======================
    if len(filtered_df) == 0:
        st.warning("⚠️ No data available for the selected filters. Try adjusting your filters.")
    else:
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            total_sales = filtered_df['total_price'].sum()
            st.metric("💰 Total Sales", format_large_number(total_sales))

        with col2:
            total_profit = filtered_df['profit'].sum()
            st.metric("📈 Total Profit", format_large_number(total_profit))

        with col3:
            total_qty = filtered_df['quantity_sold'].sum()
            st.metric("📦 Units Sold", f"{int(total_qty):,}")

        with col4:
            avg_transaction = filtered_df['total_price'].mean()
            st.metric("🔄 Avg Transaction", format_large_number(avg_transaction))

        with col5:
            num_transactions = len(filtered_df)
            st.metric("🛒 Transactions", f"{num_transactions:,}")

        # ====================== VISUALIZATIONS ======================
        st.markdown("---")
        st.subheader("📊 Sales Analytics")

        col1, col2 = st.columns(2)

        # Sales by Date (Line Chart)
        with col1:
            daily_sales = filtered_df.groupby('date')['total_price'].sum().reset_index()
            daily_sales['date'] = pd.to_datetime(daily_sales['date'])
            
            fig_sales = px.line(
                daily_sales,
                x='date',
                y='total_price',
                title='💹 Daily Sales Trend',
                labels={'total_price': 'Sales (₵)', 'date': 'Date'},
                markers=True
            )
            fig_sales.update_layout(hovermode='x unified')
            st.plotly_chart(fig_sales, use_container_width=True)

        # Sales by Category (Pie Chart)
        with col2:
            category_sales = filtered_df.groupby('category')['total_price'].sum().reset_index()
            fig_category = px.pie(
                category_sales,
                values='total_price',
                names='category',
                title='📂 Sales by Category'
            )
            st.plotly_chart(fig_category, use_container_width=True)

        col3, col4 = st.columns(2)

        # Monthly Profit Trend (Line Chart)
        with col3:
            monthly_profit = filtered_df.copy()
            monthly_profit['month'] = pd.to_datetime(monthly_profit['date']).dt.to_period('M').astype(str)
            monthly_profit_data = monthly_profit.groupby('month')['profit'].sum().reset_index()
            
            fig_profit_trend = px.line(
                monthly_profit_data,
                x='month',
                y='profit',
                title='📈 Monthly Profit Trend',
                labels={'profit': 'Profit (₵)', 'month': 'Month'},
                markers=True
            )
            fig_profit_trend.update_layout(hovermode='x unified')
            st.plotly_chart(fig_profit_trend, use_container_width=True)

        # Top Medications (Bar Chart)
        with col4:
            top_meds = filtered_df.groupby('medication')['quantity_sold'].sum().sort_values(ascending=False).head(10).reset_index()
            fig_meds = px.bar(
                top_meds,
                x='quantity_sold',
                y='medication',
                orientation='h',
                title='🏆 Top 10 Medications (by Quantity)',
                labels={'quantity_sold': 'Quantity Sold', 'medication': 'Medication'}
            )
            fig_meds.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_meds, use_container_width=True)

        col5, col6 = st.columns(2)

        # Profit by Category (Bar Chart)
        with col5:
            category_profit = filtered_df.groupby('category')['profit'].sum().sort_values(ascending=False).reset_index()
            fig_category_profit = px.bar(
                category_profit,
                x='category',
                y='profit',
                title='💵 Profit by Category',
                labels={'profit': 'Profit (₵)', 'category': 'Category'},
                color='profit',
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig_category_profit, use_container_width=True)

        # Payment Methods (Bar Chart)
        with col6:
            payment_sales = filtered_df.groupby('payment_method')['total_price'].sum().reset_index()
            fig_payment = px.bar(
                payment_sales,
                x='payment_method',
                y='total_price',
                title='💳 Sales by Payment Method',
                labels={'total_price': 'Sales (₵)', 'payment_method': 'Payment Method'},
                color='payment_method'
            )
            st.plotly_chart(fig_payment, use_container_width=True)

        # ====================== DETAILED DATA TABLE ======================
        st.markdown("---")
        st.subheader("📋 Transaction Details")

        display_cols = ['date', 'medication', 'category', 'quantity_sold', 'unit_price', 'total_price', 'profit', 'payment_method']
        display_df = filtered_df[display_cols].copy()
        display_df = display_df.sort_values('date', ascending=False)
        
        # Format columns for display
        display_df['total_price'] = display_df['total_price'].apply(lambda x: f"₵{x:,.2f}")
        display_df['profit'] = display_df['profit'].apply(lambda x: f"₵{x:,.2f}")

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # Download CSV
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"pharmacy_sales_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

        # ====================== SUMMARY STATISTICS ======================
        st.markdown("---")
        st.subheader("📈 Summary Statistics")

        summary_col1, summary_col2, summary_col3 = st.columns(3)

        with summary_col1:
            st.write("**Top Medication:**")
            top_med = filtered_df.groupby('medication')['quantity_sold'].sum().idxmax()
            st.write(f"🔹 {top_med}")

        with summary_col2:
            st.write("**Most Used Payment Method:**")
            top_payment = filtered_df['payment_method'].value_counts().idxmax()
            st.write(f"💳 {top_payment}")

        with summary_col3:
            st.write("**Best Performing Category:**")
            top_category = filtered_df.groupby('category')['total_price'].sum().idxmax()
            st.write(f"📂 {top_category}")
        
        # Profit Summary Statistics
        st.markdown("---")
        st.subheader("💵 Profit Summary")
        
        profit_col1, profit_col2, profit_col3 = st.columns(3)
        
        with profit_col1:
            highest_profit_med = filtered_df.groupby('medication')['profit'].sum().idxmax()
            highest_profit_amt = filtered_df.groupby('medication')['profit'].sum().max()
            st.write("**Highest Profit Medication:**")
            st.write(f"🔹 {highest_profit_med}")
            st.write(f"💰 ₵{highest_profit_amt:,.2f}")
        
        with profit_col2:
            highest_profit_cat = filtered_df.groupby('category')['profit'].sum().idxmax()
            highest_profit_cat_amt = filtered_df.groupby('category')['profit'].sum().max()
            st.write("**Highest Profit Category:**")
            st.write(f"📂 {highest_profit_cat}")
            st.write(f"💰 ₵{highest_profit_cat_amt:,.2f}")
        
        with profit_col3:
            profit_margin = (filtered_df['profit'].sum() / filtered_df['total_price'].sum() * 100) if filtered_df['total_price'].sum() > 0 else 0
            st.write("**Average Profit Margin:**")
            st.write(f"📊 {profit_margin:.1f}%")

        # ====================== INVENTORY MANAGEMENT ======================
        st.markdown("---")
        st.subheader("📦 Inventory Management")
        
        # Filter inventory by stock status
        inventory_display = inventory_summary.copy()
        if stock_status_filter and 'OK' not in stock_status_filter or 'Low Stock' not in stock_status_filter or 'Critical' not in stock_status_filter:
            if stock_status_filter:
                inventory_display = inventory_display[inventory_display['stock_status'].isin(stock_status_filter)]
        
        # Create inventory visualization
        inv_col1, inv_col2 = st.columns(2)
        
        # Stock Status Distribution (Pie Chart)
        with inv_col1:
            stock_dist = inventory_summary['stock_status'].value_counts().reset_index()
            stock_dist.columns = ['stock_status', 'count']
            
            fig_stock_dist = px.pie(
                stock_dist,
                values='count',
                names='stock_status',
                title='📊 Stock Status Distribution',
                color='stock_status',
                color_discrete_map={'OK': '#2ecc71', 'Low Stock': '#f39c12', 'Critical': '#e74c3c'}
            )
            st.plotly_chart(fig_stock_dist, use_container_width=True)
        
        # Current Stock by Medication (Bar Chart)
        with inv_col2:
            stock_sorted = inventory_display.sort_values('current_stock', ascending=True)
            fig_stock = px.bar(
                stock_sorted,
                y='medication',
                x='current_stock',
                color='stock_status',
                orientation='h',
                title='📦 Current Stock Levels',
                labels={'current_stock': 'Quantity in Stock', 'medication': 'Medication'},
                color_discrete_map={'OK': '#2ecc71', 'Low Stock': '#f39c12', 'Critical': '#e74c3c'}
            )
            fig_stock.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_stock, use_container_width=True)
        
        # Inventory Details Table
        st.markdown("---")
        st.subheader("📋 Inventory Details")
        
        inventory_table = inventory_display[['medication', 'initial_stock', 'quantity_sold', 'current_stock', 'stock_status']].copy()
        inventory_table = inventory_table.sort_values('current_stock', ascending=True)
        
        # Add color coding to status
        def highlight_status(val):
            if val == 'Critical':
                return '🔴 Critical'
            elif val == 'Low Stock':
                return '🟡 Low Stock'
            else:
                return '🟢 OK'
        
        inventory_table['stock_status'] = inventory_table['stock_status'].apply(highlight_status)
        inventory_table = inventory_table.rename(columns={
            'medication': 'Medication',
            'initial_stock': 'Initial Stock',
            'quantity_sold': 'Sold',
            'current_stock': 'Current Stock',
            'stock_status': 'Status'
        })
        
        st.dataframe(inventory_table, use_container_width=True, hide_index=True)
        
        # Restock Alert
        critical_items = inventory_summary[inventory_summary['stock_status'] == 'Critical']
        low_items = inventory_summary[inventory_summary['stock_status'] == 'Low Stock']
        
        if len(critical_items) > 0:
            st.error(f"🔴 **CRITICAL ALERT:** {len(critical_items)} medication(s) require immediate restocking!")
            for _, item in critical_items.iterrows():
                st.error(f"  • {item['medication']}: Only {int(item['current_stock'])} units left")
        
        if len(low_items) > 0:
            st.warning(f"🟡 **LOW STOCK WARNING:** {len(low_items)} medication(s) are running low")
            for _, item in low_items.iterrows():
                st.warning(f"  • {item['medication']}: {int(item['current_stock'])} units remaining")
