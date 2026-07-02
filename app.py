import sqlite3
import pandas as pd
import streamlit as st
import os

# ==========================================
# 1. PAGE CONFIGURATION & STYLES
# ==========================================
st.set_page_config(page_title="Skinalyze | Precision Matrix", layout="centered")

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
# 2. SESSION STATE MANAGEMENT
# ==========================================
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = pd.DataFrame()

# ==========================================
# 3. TOP HEADER MENU
# ==========================================
# ==========================================
# 3. TOP HEADER MENU & SIDEBAR
# ==========================================
col1, col2 = st.columns([1.5, 8.5])
with col1:
    if st.button("..."):
        # Safely get the current state and toggle it
        current_sidebar_state = st.session_state.get('show_sidebar', False)
        st.session_state.show_sidebar = not current_sidebar_state
        st.rerun()

st.markdown('<div class="top-dashboard-border"></div>', unsafe_allow_html=True)

# Toggleable Sidebar Content using safe .get()
if st.session_state.get('show_sidebar', False):
    with st.sidebar:
        st.title("Skinalyze")
        
        if st.button("Home", use_container_width=True):
            st.session_state.view = 'home'
            st.session_state.show_sidebar = False
            st.rerun()
            
        if st.button("Skincare Info Guide", use_container_width=True):
            pass # Placeholder for future functionality
            
        if st.button("History", use_container_width=True):
            pass # Placeholder for future functionality

# ==========================================
# 4. DATABASE CONNECTION FUNCTION
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
# PDF GENERATION FUNCTION
# ==========================================
def generate_pdf(user_name, skin_type, skin_issue, results):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    import io
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Title
    p.setFont("Helvetica-Bold", 20)
    p.setFillColorRGB(0.18, 0.35, 0.21) # #2E5A36
    p.drawString(50, height - 50, "Skinalyze | Precision Matrix Routine")
    
    # Header Divider Line
    p.setStrokeColorRGB(0.18, 0.35, 0.21)
    p.setLineWidth(2)
    p.line(50, height - 60, width - 50, height - 60)
    
    # Greeting Content
    p.setFont("Helvetica", 11)
    p.setFillColorRGB(0.07, 0.09, 0.15) # #111827
    greeting_text = f"Hello {user_name}, here is your custom configuration targeted precisely for {skin_type} and {skin_issue}."
    p.drawString(50, height - 90, greeting_text)
    
    y = height - 130
    
    if results.empty:
        p.drawString(50, y, "No exact matches found for this specific combination.")
    else:
        categories = results['category_name'].unique()
        for cat in categories:
            if y < 100:
                p.showPage()
                y = height - 50
                
            p.setFont("Helvetica-Bold", 14)
            p.setFillColorRGB(0.18, 0.35, 0.21)
            p.drawString(50, y, f"{cat}")
            y -= 20
            
            cat_products = results[results['category_name'] == cat].head(3)
            for _, row in cat_products.iterrows():
                if y < 80:
                    p.showPage()
                    y = height - 50
                    
                p.setFont("Helvetica-Bold", 11)
                p.setFillColorRGB(0.07, 0.09, 0.15)
                p.drawString(60, y, f"• {row['product_name']}")
                y -= 15
                
                p.setFont("Helvetica", 10)
                desc = row['description'] if pd.notna(row['description']) else "Clinical formulation."
                if len(desc) > 85:
                    desc = desc[:82] + "..."
                p.drawString(72, y, desc)
                y -= 25
            y -= 10
            
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer.getvalue()

# ==========================================
# 6. VIEWS (HOME / ASSESSMENT / RESULTS)
# ==========================================

if st.session_state.view == 'home':
    st.markdown('<div class="main-header">Skinalyze</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Clinical Rule-Based Skincare Architecture</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Welcome to a smart rule-based skincare matching system! To get started, please press the button below to begin the skin assessment.</div>', unsafe_allow_html=True)
    
    st.info("👋 **Disclaimer:** This website provides general information only and is not intended as medical advice. Please consult a dermatologist for personalized skincare recommendations.")
    
    if st.button("Start Skin Assessment ➔", use_container_width=True, type="primary"):
        st.session_state.view = 'assessment'
        st.rerun()

elif st.session_state.view == 'assessment':
    st.title("Skin Profiler")
    st.markdown(f"Select your skin type and primary skin concern to receive a personalized skincare routine. You can also provide a profile name for easy reference.")
    
    # Fetch dropdown options from DB
    try:
        skin_types = fetch_data("SELECT * FROM skin_type")
        skin_issues = fetch_data("SELECT * FROM skin_issue")
    except Exception as e:
        st.error(f"Database Error: Could not load data. Ensure 'skincare.db' is in the folder. Details: {e}")
        st.stop()

    with st.form("diagnostic_form"):
        st.write("### Profile Name (Optional)")
        user_name = st.text_input("Enter a name for this profile:")

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
            
            # Save the names for the results page display
            st.session_state.user_name = user_name.strip() if user_name.strip() else "there"
            st.session_state.current_skin_type_name = skin_types.loc[skin_types['skin_type_id'] == selected_type, 'skin_type_name'].values[0]
            st.session_state.current_skin_issue_name = skin_issues.loc[skin_issues['issue_id'] == selected_issue, 'issue_name'].values[0]

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
    st.title("Your Skinalyze Matrix Blueprint")
    results = st.session_state.recommendations

    # Custom Greeting
    st.markdown(f"**Hello {st.session_state.user_name}, here is the custom configuration targeted precisely for {st.session_state.current_skin_type_name} and {st.session_state.current_skin_issue_name}.**")
    st.write("") # Add a little spacing
    
    # Export to PDF Button
    try:
        pdf_bytes = generate_pdf(
            st.session_state.user_name,
            st.session_state.current_skin_type_name,
            st.session_state.current_skin_issue_name,
            results
        )
        st.download_button(
            label="📥 Export Routine to PDF",
            data=pdf_bytes,
            file_name=f"skinalyze_routine_{st.session_state.user_name}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Error generating PDF utility: {e}")
        
    st.write("") # Spacing container
    
    if results.empty:
        st.warning("⚠️ No exact matches found for this specific combination. Try broadening your criteria.")
    else:
        # Group by category (Cleanser, Moisturizer, etc.)
        categories = results['category_name'].unique()
        
        for _, row in cat_products.iterrows():
            # Use 'active_ingredients' from your database query
            ingredients = row['active_ingredients'] if pd.notna(row['active_ingredients']) and row['active_ingredients'].strip() != "" else None
            
            # Format the description block based on whether ingredients exist
            if ingredients:
                # If there are commas, it automatically handles multiple ingredients nicely
                desc_text = f"**Key Ingredients:** {ingredients}"
            else:
                desc_text = "Clinical formulation."

            st.markdown(f"""
                <div class="product-card">
                    <div class="product-title">{row['product_name']}</div>
                    <div class="product-desc">{desc_text}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.write("---")
    if st.button("↺ Restart Diagnostic", use_container_width=True):
        st.session_state.view = 'assessment'
        st.rerun()