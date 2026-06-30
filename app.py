import os
import sqlite3
import pandas as pd
import streamlit as st

# ==========================================
# 1. SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="GlowGuide | Skincare Engine", page_icon="✨", layout="centered")

# Custom CSS for Print Mode and Styling
st.markdown("""
    <style>
    .cat-header { font-size: 24px; font-weight: bold; color: #2C3E50; border-bottom: 2px solid #3498DB; margin-top: 30px; padding-bottom: 5px; }
    .product-box { background-color: #F8F9F9; padding: 15px; border-radius: 8px; border-left: 5px solid #3498DB; margin-bottom: 15px; }
    .brand-text { font-size: 12px; color: #7F8C8D; text-transform: uppercase; font-weight: bold; letter-spacing: 1px; }
    .prod-name { font-size: 18px; color: #2C3E50; margin: 5px 0; font-weight: 600; }
    
    /* Print Styles */
    @media print {
        header, footer, .stButton, .stDownloadButton, [data-testid="stSidebar"] { display: none !important; }
        .main .block-container { padding-top: 0rem !important; }
        body { background-color: white !important; }
    }
    </style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "skincare.db")

# Initialize Session State for Page Routing
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'user_issues' not in st.session_state:
    st.session_state.user_issues = []

# Database Connection Helper
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Fetch Data for Dropdowns
def fetch_options(table, id_col, name_col):
    try:
        conn = get_db_connection()
        data = conn.execute(f"SELECT {id_col}, {name_col} FROM {table}").fetchall()
        conn.close()
        return [{"id": row[id_col], "name": row[name_col]} for row in data]
    except Exception:
        return []

# ==========================================
# 2. PAGE 1: HOMEPAGE
# ==========================================
if st.session_state.current_page == "Home":
    st.title("✨ Welcome to GlowGuide")
    st.markdown("""
        **Discover your perfect skincare routine.**
        
        Our rule-based recommendation engine analyzes your unique biological skin type and specific concerns to curate a list of scientifically-backed products tailored just for you.
    """)
    st.write("---")
    
    # Navigation Button
    if st.button("Start My Diagnostic ➔", use_container_width=True, type="primary"):
        st.session_state.current_page = "Assessment"
        st.rerun()

# ==========================================
# 3. PAGE 2: ASSESSMENT (Inputs)
# ==========================================
elif st.session_state.current_page == "Assessment":
    st.title("📋 Skin Assessment")
    st.markdown("Please fill out your skin profile below to filter our product database.")

    skin_types = fetch_options("skin_type", "skin_type_id", "skin_type_name")
    skin_issues = fetch_options("skin_issue", "issue_id", "issue_name")

    # Input 1: Single Dropdown for Skin Type
    selected_type = st.selectbox(
        "1. What is your primary Skin Type? (Select One)",
        options=[t["id"] for t in skin_types],
        format_func=lambda x: next(t["name"] for t in skin_types if t["id"] == x)
    )

    # Input 2: Multiple Choice for Skin Issues
    selected_issues = st.multiselect(
        "2. What are your main Skin Concerns? (Select as many as apply)",
        options=[i["id"] for i in skin_issues],
        format_func=lambda x: next(i["name"] for i in skin_issues if i["id"] == x)
    )

    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back to Home", use_container_width=True):
            st.session_state.current_page = "Home"
            st.rerun()
    with col2:
        if st.button("Find My Routine ➔", use_container_width=True, type="primary"):
            if not selected_issues:
                st.warning("Please select at least one skin concern to proceed.")
            else:
                # Save to session and move to next page
                st.session_state.user_type = selected_type
                st.session_state.user_issues = selected_issues
                st.session_state.current_page = "Results"
                st.rerun()

# ==========================================
# 4. PAGE 3: RESULTS & EXPORT
# ==========================================
elif st.session_state.current_page == "Results":
    st.title("🛒 Your Recommended Routine")
    st.markdown("Based on your assessment, here are the products filtered specifically for your skin.")
    
    # Run the filtering algorithm
    conn = get_db_connection()
    
    # SQL Dynamic Query: Must match the ONE skin type, and AT LEAST ONE of the multiple issues
    placeholders = ",".join("?" * len(st.session_state.user_issues))
    query = f"""
        SELECT DISTINCT p.product_name, p.brand, p.product_url, c.category_name
        FROM product p
        JOIN product_skin_type pst ON p.product_id = pst.product_id
        JOIN product_skin_issue psi ON p.product_id = psi.product_id
        JOIN category c ON p.category_id = c.category_id
        WHERE pst.skin_type_id = ? 
        AND psi.issue_id IN ({placeholders})
        ORDER BY c.category_id
    """
    
    params = [st.session_state.user_type] + st.session_state.user_issues
    results = conn.execute(query, params).fetchall()
    conn.close()

    if not results:
        st.info("No products currently match this exact combination in our database.")
    else:
        # Group products dynamically by their category
        report_data = []
        df_results = pd.DataFrame([dict(row) for row in results])
        grouped = df_results.groupby('category_name')
        
        for category, group in grouped:
            st.markdown(f'<div class="cat-header">{category}</div>', unsafe_allow_html=True)
            
            for _, row in group.iterrows():
                report_data.append(row.to_dict())
                
                url_html = f"<a href='{row['product_url']}' target='_blank'>View Product</a>" if row['product_url'] else ""
                st.markdown(f"""
                    <div class="product-box">
                        <div class="brand-text">{row['brand'] or 'Generic'}</div>
                        <div class="prod-name">{row['product_name']}</div>
                        {url_html}
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("🖨️ Export & Print")
        
        # Action 1: Print via Browser (CSS handles layout)
        st.info("💡 **To Print or Save to PDF:** Press **Ctrl + P** (Windows) or **Cmd + P** (Mac). The layout will automatically format into a clean document.")
        
        # Action 2: Download CSV File
        csv = pd.DataFrame(report_data).to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Full List as CSV",
            data=csv,
            file_name="glowguide_recommendations.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.write("---")
    if st.button("↺ Retake Assessment", use_container_width=True):
        st.session_state.current_page = "Assessment"
        st.session_state.user_issues = []
        st.rerun()