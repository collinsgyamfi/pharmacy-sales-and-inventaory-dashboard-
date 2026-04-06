# 💊 Pharmacy Sales Dashboard

A comprehensive **real-time analytics dashboard** for pharmacy businesses to track sales performance, manage inventory, and make data-driven decisions. Built with Streamlit and Plotly for interactive visualization and seamless user experience.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Data Format](#data-format)
- [Configuration](#configuration)
- [Dashboard Sections](#dashboard-sections)
- [Inventory Management](#inventory-management)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The **Pharmacy Sales Dashboard** is a powerful business intelligence tool designed for pharmacy owners and managers to:

- 📊 Analyze sales data across custom date ranges
- 💰 Track revenue, transactions, and basket sizes in real-time
- 🏥 Monitor medication performance and trends
- 📦 Manage inventory with automated stock level alerts
- 💳 Analyze payment method preferences
- 📈 Visualize sales trends and patterns

**Currency:** All monetary values are displayed in **Ghana Cedis (₵)**

---

## ✨ Key Features

### 📅 Flexible Date Range Selection
- **Custom Date Picker**: Select any start and end date
- **Quick Selection Buttons**: 
  - Today
  - Yesterday
  - Last 7 Days
  - Last 30 Days
- **Persistent Selection**: Date range stays selected during navigation

### 📊 Real-Time KPI Dashboard
- **Total Revenue**: Aggregate sales for selected period
- **Total Transactions**: Count of all transactions
- **Avg Basket Size**: Average transaction value
- **Avg Daily Revenue**: Daily revenue average

### 🥇 Top Medications & Categories Analytics
- Top 10 medications by revenue
- Top 10 medications by quantity sold
- Category-wise performance breakdown
- Interactive bar charts with drill-down capability

### 💳 Payment Method Analysis
- Payment method distribution (pie chart)
- Daily payment trends (stacked bar chart)
- Payment percentage breakdown
- Support for: Cash, Card, Insurance, UPI/Mobile

### 📈 Sales Trends & Patterns
- Daily revenue trend line chart
- Average basket size trend visualization
- Multi-line trend analysis
- Marker-based data point identification

### 📦 Advanced Inventory Management
- **Real-time Stock Tracking**: Automatic calculation of current stock
- **Stock Status Filtering**:
  - ✅ OK (50+ units)
  - ⚠️ LOW (30-49 units)
  - 🚨 CRITICAL (<30 units)
- **Automated Alerts**:
  - 🚨 Critical stock alerts for immediate action
  - ⚠️ Low stock warnings for proactive restocking
- **Inventory Dashboard**:
  - Color-coded stock status table (Green → Red gradient)
  - Restock priority pie chart
  - Initial stock, sold units, and current stock tracking

### 🎯 Smart Filtering System
- **Category Filter**: Filter by medication category
- **Payment Method Filter**: Filter by payment type
- **Stock Status Filter**: Filter inventory by stock level
- **Combinable Filters**: Mix and match filters for precise analysis

### 📱 Responsive Design
- Wide layout optimized for desktop and tablet viewing
- Mobile-friendly interface components
- Collapsible sidebar for easy navigation

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend Framework** | Streamlit | Interactive web application |
| **Data Processing** | Pandas & NumPy | Data manipulation & aggregation |
| **Visualization** | Plotly Express | Interactive charts & graphs |
| **Data Source** | CSV Upload or Sample Data | Flexible data input |
| **Currency** | Ghana Cedis (₵) | All monetary calculations |

---

## 📥 Installation

### Prerequisites
- **Python 3.8+**
- **pip** (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/pharmacy-sales-dashboard.git
cd pharmacy-sales-dashboard
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Dashboard
```bash
streamlit run app.py
```

The dashboard will open in your default browser at `http://localhost:8501`

---

## 🚀 Usage

### Quick Start Demo
1. **Launch the app** - Dashboard loads with 60 days of sample data
2. **Explore Quick Buttons** - Click "Last 7 Days" to filter sales data
3. **View Inventory Alerts** - Check stock status and critical items
4. **Upload Real Data** - Use your own CSV file for actual business data

### Using with Your Data

#### Option 1: Upload CSV File
1. Click **"Upload your dataset (CSV)"** in the sidebar
2. Select your CSV file
3. Dashboard auto-updates with your data

#### Option 2: Manual Date Selection
1. Use date input fields to select custom range
2. Filters automatically update all visualizations
3. Scroll to view all dashboard sections

#### Applying Filters
1. **Category Filter**: Select specific medication categories
2. **Payment Filter**: Analyze by payment method
3. **Inventory Filter**: View stock status breakdown

---

## 📊 Data Format

### Required CSV Columns

Your CSV file must include these columns:

```
sale_id          - Unique transaction identifier (Integer)
medication       - Medication name (String)
category         - Medication category (String)
unit             - Unit type: Tab, Bottle, Vial, Strip (String)
quantity_sold    - Quantity sold in transaction (Integer)
unit_price       - Price per unit in Ghana Cedis (Float)
payment_method   - Payment type (String)
date             - Transaction date (Date format: YYYY-MM-DD)
```

### Example CSV Format
```csv
sale_id,medication,category,unit,quantity_sold,unit_price,payment_method,date
1,Paracetamol,Pain Relief,Tab,2,15.50,Cash,2025-03-01
2,Amoxicillin,Antibiotics,Bottle,1,45.00,Card,2025-03-01
3,Insulin,Chronic Care,Vial,1,125.00,Insurance,2025-03-02
```

### Sample Medications Included
- Paracetamol (Pain Relief)
- Amoxicillin (Antibiotics)
- Ibuprofen (Pain Relief)
- Vitamin D3 (Vitamins)
- Insulin (Chronic Care)
- Cetirizine (Allergy)
- Omeprazole (Gastro)
- Metformin (Diabetes)

---

## ⚙️ Configuration

### Inventory Stock Thresholds

Edit stock level thresholds in `app.py` (line ~65):

```python
current_stock['status'] = current_stock['current_stock'].apply(
    lambda x: '🚨 CRITICAL' if x < 30 else ('⚠️ LOW' if x < 50 else '✅ OK')
)
```

**Current Thresholds:**
- CRITICAL: < 30 units
- LOW: 30-49 units
- OK: 50+ units

### Sample Data Configuration

To modify sample data generation (line ~26):

```python
dates = pd.date_range(start='2025-03-01', periods=60, freq='D')  # 60 days
n = 2000  # Number of transactions
```

### Initial Stock Levels

Modify initial medication stock (line ~45):

```python
initial_stock = {
    'Paracetamol': 500,
    'Amoxicillin': 300,
    'Ibuprofen': 250,
    # ... Add more medications
}
```

---

## 📋 Dashboard Sections

### 1. **KPI Overview**
- 💰 Total Revenue
- 📦 Total Transactions  
- 🛒 Average Basket Size
- 📈 Average Daily Revenue

Display period: Selected date range

### 2. **Inventory Status & Stock Alerts**
- Real-time stock levels for all medications
- Color-coded status indicators
- Priority-based restock recommendations
- Automated critical and low stock warnings

### 3. **Top Medications & Categories**
- Revenue ranking (Top 10)
- Quantity ranking (Top 10)
- Category distribution
- Interactive bar charts

### 4. **Payment Method Breakdown**
- Payment type distribution (pie chart)
- Daily payment trends (stacked bar chart)
- Payment method analytics

### 5. **Sales Trends**
- Daily revenue trend line
- Basket size trend analysis
- Pattern identification
- Helps predict business performance

---

## 📦 Inventory Management

### Stock Alert System

**Critical Stock Alerts (< 30 units)**
```
🚨 CRITICAL ALERT: Immediate restock needed for: [Medication Names]
```

**Low Stock Alerts (30-49 units)**
```
⚠️ LOW STOCK ALERT: Please prepare restock for: [Medication Names]
```

### Inventory Dashboard Features
- ✅ **Stock Status Table**: Initial stock → Current stock tracking
- 📊 **Priority Pie Chart**: OK vs Low vs Critical distribution
- 🎨 **Color Gradient**: Green (Full) → Red (Empty) visualization
- 🔍 **Stock Filter**: Filter by status level

### Inventory Calculations
```
Current Stock = Initial Stock - Total Quantity Sold
Status = Automatic based on current stock level
```

---

## 📁 File Structure

```
pharmacy-sales-dashboard/
│
├── app.py                          # Main application file
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
│
├── sample_data/
│   └── sample_pharmacy_data.csv   # Example data format
│
└── docs/
    ├── INSTALLATION.md            # Detailed setup guide
    ├── DATA_GUIDE.md              # Data format specification
    └── TROUBLESHOOTING.md         # Common issues & solutions
```

---

## 🔧 Troubleshooting

### Quick Selection Buttons Not Working
**Solution**: Ensure Streamlit is running latest version
```bash
pip install --upgrade streamlit
```

### CSV Upload Error
**Solution**: Verify CSV contains all required columns (see [Data Format](#data-format))

### Charts Not Displaying
**Solution**: Check data date format is YYYY-MM-DD

### Session State Issues
**Solution**: Clear browser cache or restart Streamlit
```bash
streamlit run app.py --logger.level=debug
```

---

## 📊 Sample Dashboard Insights

The dashboard provides actionable insights such as:

- **Revenue Patterns**: Identify peak sales days
- **Top Sellers**: Focus inventory on best-performing medications
- **Payment Trends**: Optimize payment method offerings
- **Inventory Health**: Prevent stockouts and overstocking
- **Business Growth**: Track daily/weekly/monthly trends

---

## 🤝 Contributing

Contributions welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Bug Reports
Please report bugs via GitHub Issues with:
- Description of issue
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable

---

## 📝 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

## 👤 Author & Support

**Created by**: [Your Name/Organization]  
**Email**: [your.email@example.com]  
**GitHub**: [@yourusername](https://github.com/yourusername)

### Support & Documentation
- 📖 [Full Documentation](#)
- 🐛 [Report Issues](https://github.com/yourusername/pharmacy-sales-dashboard/issues)
- 💬 [Discussions](https://github.com/yourusername/pharmacy-sales-dashboard/discussions)

---

## 🎯 Roadmap

### Planned Features (v2.0)
- [ ] Database integration (SQLite/PostgreSQL)
- [ ] User authentication & role-based access
- [ ] Export reports to PDF/Excel
- [ ] Email alerts for critical stock levels
- [ ] Advanced forecasting with ML
- [ ] Multi-location support
- [ ] Mobile app companion
- [ ] API for third-party integrations

### Recent Updates (v1.0)
- ✅ Quick date selection (Today, Yesterday, Last 7/30 days)
- ✅ Session state persistence for date selection
- ✅ Inventory management with stock alerts
- ✅ Ghana Cedis currency support
- ✅ Responsive dashboard design

---

## 🏆 Features Highlight

| Feature | Benefit |
|---------|---------|
| Real-time Analytics | Make instant business decisions |
| Inventory Alerts | Prevent medication stockouts |
| Flexible Filtering | Analyze specific segments |
| Interactive Charts | Explore data visually |
| Export Capability | Share insights with stakeholders |
| Currency Support | Localized for Ghana (₵) |

---

## 📞 Contact & Feedback

Have suggestions or found a bug? 
- **GitHub Issues**: [Report here](https://github.com/yourusername/pharmacy-sales-dashboard/issues)
- **Email**: [your.email@example.com]
- **LinkedIn**: [Your Profile](https://linkedin.com/in/yourprofile)

---

## ⭐ Show Your Support

If this dashboard helps your pharmacy business, please:
- ⭐ **Star** this repository
- 🔗 **Share** with other pharmacy owners
- 💬 **Provide feedback** via GitHub Discussions
- 🐛 **Report issues** to help improve the project

---

**Last Updated**: April 2026  
**Version**: 1.0.0  
**Status**: Production Ready ✅

---

**Made with ❤️ for Pharmacy Businesses**
