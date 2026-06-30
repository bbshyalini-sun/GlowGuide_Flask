import os
import sqlite3
import pandas as pd
import streamlit as st

# ==========================================
# 1. SETUP, CUSTOM DESIGN & PRINT CONFIG
# ==========================================
st.set_page_config(page_title="GlowGuide | Precision Matrix Engine", page_icon="🌿", layout="centered")

st.markdown("""
    <style>
    .cat-title-header { font-size: 24px; font-weight: bold; color: #2E5A36; border-bottom: 2px solid #E2E8F0; padding-bottom: 6px; margin-top: 30px; margin-bottom: 15px; }
    .product-display-card { background-color: #F8FAFC; padding: 18px; border-radius: 10px; border-left: 5px solid #2E5A36; margin-bottom: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .product-main-title { font-size: 19px; color: #1E293B; margin: 4px 0 4px 0; font-weight: 600; }
    
    /* Align sidebar menu buttons uniformly to the left */
    div[data-testid="stSidebar"] button {
        display: flex;
        justify-content: flex-start !important;
        text-align: left !important;
    }
    
    /* High-fidelity CSS overrides for web print layouts */
    @media print {
        header, footer, .stButton, .stDownloadButton, [data-testid="stSidebar"], [data-testid="stHeader"] { display: none !important; }
        .main .block-container { padding-top: 0rem !important; max-width: 100% !important; }
        body { background-color: #FFFFFF !important; color: #000000 !important; }
        .product-display-card { border: 1px solid #CBD5E1; background: #FFFFFF !important; box-shadow: none !important; page-break-inside: avoid; }
    }
    </style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "skincare.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Force active database auto-population on platform boot
def verify_underlying_matrix():
    try:
        import init_db
        if not os.path.exists(DB_PATH):
            init_db.init_database_with_real_data()
        else:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='skin_type'")
            has_table = c.fetchone()
            if not has_table:
                conn.close()
                init_db.init_database_with_real_data()
            else:
                c.execute("SELECT COUNT(*) FROM skin_type")
                if c.fetchone()[0] == 0:
                    conn.close()
                    init_db.init_database_with_real_data()
                else:
                    conn.close()
    except Exception:
        pass

verify_underlying_matrix()

# ==========================================
# 2. PERSISTENCE LAYER & MEMORY STATE
# ==========================================
if 'active_view' not in st.session_state:
    st.session_state.active_view = "Home"
if 'tracked_skin_type' not in st.session_state:
    st.session_state.tracked_skin_type = None
if 'tracked_skin_issues' not in st.session_state:
    st.session_state.tracked_skin_issues = []

# ==========================================
# 3. RETRACTABLE DASHBOARD SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("### 🎛️ GlowGuide Dashboard")
    st.markdown("Navigate across application states instantly.")
    st.write("---")
    
    if st.button("🏠 System Homepage", use_container_width=True):
        st.session_state.active_view = "Home"
        st.rerun()
        
    if st.button("📋 Skin Diagnostic Assessment", use_container_width=True):
        st.session_state.active_view = "Assessment"
        st.rerun()
        
    if st.button("🛒 Recommendation Engine Results", use_container_width=True):
        if not st.session_state.tracked_skin_issues:
            st.sidebar.warning("⚠️ Complete assessment input criteria first.")
        else:
            st.session_state.active_view = "Results"
            st.rerun()

# ==========================================
# 4. MUTABLE VIEW ROUTING ROUTINES
# ==========================================

# --- SYSTEM HOMEPAGE VIEW ---
if st.session_state.active_view == "Home":
    st.title("✨ Welcome to GlowGuide")
    st.markdown("""
        ### Strategic Precision Skincare Architecture
        Discover your tailored routine using our matrix formulation engine. 
        By assessing your biological skin profile against established product ingredients, 
        GlowGuide filters inventory schemas to provide matching, highly target-aligned products.
    """)
    st.write("---")
    if st.button("Begin Free Profile Assessment ➔", use_container_width=True, type="primary"):
        st.session_state.active_view = "Assessment"
        st.rerun()

# --- DIAGNOSTIC PARAMETER INPUT VIEW ---
elif st.session_state.active_view == "Assessment":
    st.title("📋 Skin Profile Diagnostic")
    st.markdown("Select your structural skin criteria below to filter the engine registry rules.")
    st.write("---")

    # STID LIVE DATABASE EXTRACTION PIPELINES
    try:
        conn = get_db_connection()
        db_types = conn.execute("SELECT skin_type_id, skin_type_name FROM skin_type").fetchall()
        db_issues = conn.execute("SELECT issue_id, issue_name FROM skin_issue").fetchall()
        conn.close()
        
        SKIN_TYPES_MAP = {row["skin_type_id"]: row["skin_type_name"] for row in db_types}
        SKIN_ISSUES_MAP = {row["issue_id"]: row["issue_name"] for row in db_issues}
    except Exception as err:
        st.error(f"❌ Database Extraction Failure. Confirm your SQL schema format details: {err}")
        st.stop()

    if not SKIN_TYPES_MAP or not SKIN_ISSUES_MAP:
        st.error("❌ Database Connection Succeeded, but the master tables contain 0 rows.")
        st.stop()

    # Track selection changes cleanly
    if st.session_state.tracked_skin_type not in SKIN_TYPES_MAP:
        st.session_state.tracked_skin_type = list(SKIN_TYPES_MAP.keys())[0]

    # 1. Single Choice Dropdown Selection
    selected_type_id = st.selectbox(
        "1. Select Your Biological Skin Typology (Single Choice Dropdown):",
        options=list(SKIN_TYPES_MAP.keys()),
        index=list(SKIN_TYPES_MAP.keys()).index(st.session_state.tracked_skin_type),
        format_func=lambda x: SKIN_TYPES_MAP[x]
    )
    st.session_state.tracked_skin_type = selected_type_id

    # 2. Multiple Selection Checklist Matrix
    selected_issue_ids = st.multiselect(
        "2. Select Your Target Matrix Conditions (Multiple Selection Checklist):",
        options=list(SKIN_ISSUES_MAP.keys()),
        default=[i for i in st.session_state.tracked_skin_issues if i in SKIN_ISSUES_MAP],
        format_func=lambda x: SKIN_ISSUES_MAP[x]
    )
    st.session_state.tracked_skin_issues = selected_issue_ids

    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back to Home", use_container_width=True):
            st.session_state.active_view = "Home"
            st.rerun()
    with col2:
        if st.button("Compile Matrix Results ➔", use_container_width=True, type="primary"):
            if not selected_issue_ids:
                st.error("Validation Error: Please select at least one skin issue option before submitting queries.")
            else:
                st.session_state.active_view = "Results"
                st.rerun()

# --- FILTER MATRIX RECOMMENDATIONS ENGINE RESULTS ---
elif st.session_state.active_view == "Results":
    st.title("🛒 Filtered Product Matrix Results")
    st.write("---")
    
    if not st.session_state.tracked_skin_issues:
        st.info("No selection parameters stored in active profile. Complete the assessment profile to start.")
        if st.button("Go to Assessment View", use_container_width=True):
            st.session_state.active_view = "Assessment"
            st.rerun()
    else:
        try:
            conn = get_db_connection()
            
            # Ensure all values are converted to integers to align perfectly with the database schema
            target_skin_type = int(st.session_state.tracked_skin_type)
            target_issues = [int(issue) for issue in st.session_state.tracked_skin_issues]
            
            # Create standard dynamic binding placeholders (?, ?, ...)
            issue_placeholders = ",".join("?" * len(target_issues))
            
            # STEP-BY-STEP FILTERING ENGINE:
            # 1. Selects base products grouped by category_name
            # 2. Filters through product_skin_type relationship mapping
            # 3. Filters again through product_skin_issue relationship mapping
            query = f"""
                SELECT DISTINCT p.product_id, p.product_name, c.category_name
                FROM product p
                JOIN category c ON p.category_id = c.category_id
                JOIN product_skin_type pst ON p.product_id = pst.product_id
                JOIN product_skin_issue psi ON p.product_id = psi.product_id
                WHERE pst.skin_type_id = ? 
                  AND psi.issue_id IN ({issue_placeholders})
                ORDER BY c.category_id, p.product_name
            """
            
            execution_params = [target_skin_type] + target_issues
            matched_records = conn.execute(query, execution_params).fetchall()
            conn.close()
            
            if not matched_records:
                st.info("No options match this exact set of criteria combinations in our database.")
            else:
                export_accumulator = []
                df_conversion = pd.DataFrame([dict(row) for row in matched_records])
                category_grouped = df_conversion.groupby('category_name')
                
                # Render results grouped cleanly by Category headers
                for category_title, category_rows in category_grouped:
                    st.markdown(f'<div class="cat-title-header">{category_title}</div>', unsafe_allow_html=True)
                    
                    for _, item_row in category_rows.iterrows():
                        export_accumulator.append({
                            "Category": item_row['category_name'],
                            "Product Name": item_row['product_name']
                        })
                        
                        st.markdown(f"""
                            <div class="product-display-card">
                                <div class="product-main-title">{item_row['product_name']}</div>
                            </div>
                        """, unsafe_allow_html=True)
                
                # Export and Printing Utilities block
                st.write("---")
                st.subheader("📋 Output and Export Operations")
                st.info("💡 **To Print or Save Directly to PDF File:** Press **Ctrl + P** (Windows) or **Cmd + P** (Mac). The layout will compile into a clean document automatically.")
                
                generated_csv_payload = pd.DataFrame(export_accumulator).to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export Filtered Profile Data (.CSV File)",
                    data=generated_csv_payload,
                    file_name="glowguide_skin_matrix_routine.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
        except Exception as query_error:
            st.error(f"Engine Runtime Error encountered: {query_error}")
            
    st.write("---")
    if st.button("↺ Restart Diagnostic Profile Sequence", use_container_width=True):
        st.session_state.tracked_skin_issues = []
        st.session_state.active_view = "Assessment"
        st.rerun()