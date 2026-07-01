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
    .stApp,
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF;
        color: #111827;
    }

    [data-testid="stHeader"] {
        background-color: rgba(255, 255, 255, 0);
    }

    [data-testid="stSidebar"] {
        background-color: #F3F4F6;
    }

    .top-dashboard-border {
        width: 100%;
        border-top: 4px solid #2E5A36;
        padding-top: 16px;
        margin-bottom: 24px;
    }

    .main-header {
        color: #2E5A36;
        font-weight: 800;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 0;
    }

    .sub-header {
        color: #111827;
        text-align: center;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }

    p,
    label,
    .stMarkdown,
    .stText,
    [data-testid="stMarkdownContainer"] {
        color: #111827;
    }

    .product-card {
        background-color: #F3F4F6;
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #2E5A36;
        margin-bottom: 15px;
        box-shadow: none;
    }

    .product-title {
        font-size: 20px;
        color: #111827;
        font-weight: 700;
        margin: 0 0 10px 0;
    }

    .product-desc {
        font-size: 14px;
        color: #111827;
        margin: 0;
    }

    div[data-testid="stAlert"],
    div[data-testid="stForm"] {
        background-color: #F3F4F6;
        color: #111827;
        border-radius: 10px;
    }

    div[data-testid="stSelectbox"] > div {
        background-color: #F3F4F6;
        color: #111827;
        border-radius: 10px;
    }

    div[data-baseweb="select"] > div {
        background-color: #F3F4F6 !important;
        color: #111827 !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="select"] span {
        color: #111827 !important;
    }

    div[role="listbox"] {
        background-color: #FFFFFF !important;
        color: #111827 !important;
    }

    div[role="option"] {
        background-color: #FFFFFF !important;
        color: #111827 !important;
    }

    div[role="option"]:hover {
        background-color: #F3F4F6 !important;
        color: #111827 !important;
    }

    div.stButton,
    div.stFormSubmitButton {
        width: fit-content;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        background-color: #2E7D32 !important;
        border-color: #2E7D32 !important;
        color: #FFFFFF !important;
        font-weight: 600;
        width: fit-content;
        min-width: unset;
        padding: 0.5rem 1rem;
    }

    div.stButton > button *,
    div.stFormSubmitButton > button * {
        color: #FFFFFF !important;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        background-color: #256628 !important;
        border-color: #256628 !important;
        color: #FFFFFF !important;
    }

    div.stButton > button:focus,
    div.stFormSubmitButton > button:focus {
        box-shadow: 0 0 0 0.2rem rgba(46, 125, 50, 0.25);
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="top-dashboard-border"></div>', unsafe_allow_html=True)

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
            "Identify baseline skin behavior:", 
            options=[None] + skin_types['skin_type_id'].tolist(),
            format_func=lambda x: "Select your skin type" if x is None else skin_types.loc[skin_types['skin_type_id'] == x, 'skin_type_name'].values[0]
        )
        
        st.write("### 2. Primary Skin Concern")
        selected_issue = st.selectbox(
            "What is your main target for treatment?", 
            options=[None] + skin_issues['issue_id'].tolist(),
            format_func=lambda x: "Select your primary skin concern" if x is None else skin_issues.loc[skin_issues['issue_id'] == x, 'issue_name'].values[0]
        )
        
        submitted = st.form_submit_button("Generate Routine", type="primary", use_container_width=True)
        
        if submitted:
            if selected_type is None or selected_issue is None:
                st.warning("Please select both your skin type and primary skin concern.")
                st.stop()
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