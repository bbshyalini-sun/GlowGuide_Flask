import sqlite3
import pandas as pd
import streamlit as st
import os

# ==========================================
# 1. PAGE CONFIGURATION & STYLES
# ==========================================
st.set_page_config(page_title="Skinalyze | Precision Matrix", page_icon="🌿", layout="centered")

st.markdown("""
    <style>
    .main-header { color: #2E5A36; font-weight: 800; text-align: center; font-size: 3rem; margin-bottom: 0px;}
    .sub-header { color: #64748b; text-align: center; font-size: 1.2rem; margin-bottom: 2rem;}
    .product-card { background-color: #F8FAFC; padding: 20px; border-radius: 12px; border-left: 6px solid #2E5A36; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .product-title { font-size: 20px; color: #1E293B; font-weight: 700; margin: 0 0 10px 0; }
    .product-desc { font-size: 14px; color: #475569; margin: 0; }
        div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button[kind="primary"] {
        background-color: #2E7D32;
        border-color: #2E7D32;
        color: white;
    }

    div.stButton > button[kind="primary"]:hover,
    div.stFormSubmitButton > button[kind="primary"]:hover {
        background-color: #256628;
        border-color: #256628;
        color: white;
    }

    div.stButton > button[kind="primary"]:focus,
    div.stFormSubmitButton > button[kind="primary"]:focus {
        box-shadow: 0 0 0 0.2rem rgba(46, 125, 50, 0.25);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATABASE CONNECTION FUNCTION
# ==========================================
DB_PATH = os.path.join(os.path.dirname(__file__), 'skincare.db')

@st.cache_resource
def get_connection():
    """Establishes a persistent SQLite connection."""
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def fetch_data(query, params=()):
    """Helper function to run queries and return DataFrames."""
    conn = get_connection()
    return pd.read_sql_query(query, conn, params=params)

# ==========================================
# 3. SESSION STATE MANAGEMENT
# ==========================================
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = pd.DataFrame()

# ==========================================
# 4. VIEWS (HOME / ASSESSMENT / RESULTS)
# ==========================================

if st.session_state.view == 'home':
    st.markdown('<div class="main-header">Skinalyze</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Clinical Rule-Based Skincare Architecture</div>', unsafe_allow_html=True)
    
    st.info("👋 **Welcome!** Our matrix compares cross-functional product parameters against your targeted biological properties to generate personalized routines.")
    
    if st.button("Start Skin Assessment ➔", use_container_width=True, type="primary"):
        st.session_state.view = 'assessment'
        st.rerun()

elif st.session_state.view == 'assessment':
    st.title("📋 Skin Diagnostic")
    
    # Fetch dropdown options from DB
    try:
        skin_types = fetch_data("SELECT * FROM skin_type")
        skin_issues = fetch_data("SELECT * FROM skin_issue")
    except Exception as e:
        st.error(f"Database Error: Could not load data. Ensure 'skincare.db' is in the folder. Details: {e}")
        st.stop()

    with st.form("diagnostic_form"):
        st.write("### 1. Primary Skin Type")
        selected_type = st.selectbox(
            "Identify your baseline skin behavior:", 
            options=skin_types['skin_type_id'].tolist(),
            format_func=lambda x: skin_types.loc[skin_types['skin_type_id'] == x, 'skin_type_name'].values[0]
        )
        
        st.write("### 2. Primary Skin Concern")
        selected_issue = st.selectbox(
            "What is your main target for treatment?", 
            options=skin_issues['issue_id'].tolist(),
            format_func=lambda x: skin_issues.loc[skin_issues['issue_id'] == x, 'issue_name'].values[0]
        )
        
        submitted = st.form_submit_button("Generate Routine", type="primary", use_container_width=True)
        
        if submitted:
            # 💡 THE SMART FALLBACK QUERY
            # Looks for exact matches, but if targeting Acne (1), allows Oil Control (3) overlap.
            query = """
                SELECT
                    p.product_id,
                    p.product_name,
                    c.category_name,
                    p.description,
                    GROUP_CONCAT(DISTINCT i.ingredient_name) AS active_ingredients
                FROM product p
                JOIN category c ON p.category_id = c.category_id
                JOIN product_skin_type pst ON p.product_id = pst.product_id
                JOIN product_skin_issue psi ON p.product_id = psi.product_id
                LEFT JOIN product_ingredient pi ON p.product_id = pi.product_id
                LEFT JOIN ingredient i ON pi.ingredient_id = i.ingredient_id
                WHERE pst.skin_type_id = ? AND psi.issue_id = ?
                GROUP BY p.product_id, p.product_name, c.category_name, p.description, c.category_id
                ORDER BY c.category_id ASC, p.product_name ASC
            """
            
            results = fetch_data(query, (selected_type, selected_issue))
            st.session_state.recommendations = results
            st.session_state.view = 'results'
            st.rerun()

elif st.session_state.view == 'results':
    st.title("✨ Your Matrix Routine")
    results = st.session_state.recommendations
    
    if results.empty:
        st.warning("⚠️ No exact matches found for this specific combination. Try broadening your criteria.")
    else:
        # Group by category (Cleanser, Moisturizer, etc.)
        categories = results['category_name'].unique()
        
        for cat in categories:
            st.markdown(f"### {cat}")
            cat_products = results[results['category_name'] == cat].head(3) # Limit to top 3 per category
            
            for _, row in cat_products.iterrows():
                desc = row['description'] if pd.notna(row['description']) else "Clinical formulation."
                st.markdown(f"""
                    <div class="product-card">
                        <div class="product-title">{row['product_name']}</div>
                        <div class="product-desc">{desc}</div>
                    </div>
                """, unsafe_allow_html=True)
    
    st.write("---")
    if st.button("↺ Restart Diagnostic", use_container_width=True):
        st.session_state.view = 'home'
        st.rerun()