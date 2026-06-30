import os
import sqlite3
import pandas as pd
import streamlit as st

# ==========================================
# 1. APPLICATION BOOTSTRAP & STYLING
# ==========================================
st.set_page_config(page_title="GlowGuide | Precision Matrix Engine", page_icon="🌿", layout="centered")

# Embedded layout configuration rules for custom containers and high-fidelity print mode
st.markdown("""
    <style>
    .cat-title-header { font-size: 24px; font-weight: bold; color: #2E5A36; border-bottom: 2px solid #E2E8F0; padding-bottom: 6px; margin-top: 30px; margin-bottom: 15px; }
    .product-display-card { background-color: #F8FAFC; padding: 18px; border-radius: 10px; border-left: 5px solid #2E5A36; margin-bottom: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .brand-meta-text { font-size: 11px; color: #64748B; text-transform: uppercase; font-weight: 700; letter-spacing: 1px; }
    .product-main-title { font-size: 19px; color: #1E293B; margin: 4px 0 8px 0; font-weight: 600; }
    
    /* Force sidebar buttons to align text to the left side */
    div[data-testid="stSidebar"] button {
        display: flex;
        justify-content: flex-start !important;
        text-align: left !important;
    }
    
    /* Native Print Formatting Optimization overrides */
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

# Ensure schema consistency across platforms 
def verify_underlying_matrix():
    try:
        if not os.path.exists(DB_PATH):
            import init_db
            init_db.init_database_with_real_data()
        else:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='skin_issue'")
            if not c.fetchone():
                import init_db
                init_db.init_database_with_real_data()
            conn.close()
    except Exception:
        pass

verify_underlying_matrix()

# ==========================================
# 2. SEEDED PERSISTENCE STATE ENGINE
# ==========================================
if 'active_view' not in st.session_state:
    st.session_state.active_view = "Home"

# Persistent trackers block to lock choice keys securely across state updates
if 'tracked_skin_type' not in st.session_state:
    st.session_state.tracked_skin_type = None
if 'tracked_skin_issues' not in st.session_state:
    st.session_state.tracked_skin_issues = []

# Fetch active query frames from database safely
try:
    conn = get_db_connection()
    raw_types = conn.execute("SELECT skin_type_id, skin_type_name FROM skin_type").fetchall()
    raw_issues = conn.execute("SELECT issue_id, issue_name FROM skin_issue").fetchall()
    conn.close()
    
    SKIN_TYPES_MAP = {r["skin_type_id"]: r["skin_type_name"] for r in raw_types}
    SKIN_ISSUES_MAP = {r["issue_id"]: r["issue_name"] for r in raw_issues}
except Exception:
    # Safe fallback tables structure to prevent breaking runtime if locked asynchronously
    SKIN_TYPES_MAP = {1: "Oily", 2: "Dry", 3: "Combination", 4: "Sensitive"}
    SKIN_ISSUES_MAP = {1: "Acne", 2: "Dryness", 3: "Oiliness", 4: "Redness", 5: "Aging"}

# Initialize trackers with valid defaults if empty
if st.session_state.tracked_skin_type is None and SKIN_TYPES_MAP:
    st.session_state.tracked_skin_type = list(SKIN_TYPES_MAP.keys())[0]

# ==========================================
# 3. SIDEBAR DASHBOARD NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown("### 🎛️ GlowGuide Dashboard")
    st.markdown("Use this panel to navigate across core system sections instantly.")
    st.write("---")
    
    # Navigation link items (Fixed: alignment variable stripped out, styled via CSS rules above)
    if st.button("🏠 System Homepage", use_container_width=True):
        st.session_state.active_view = "Home"
        st.rerun()
        
    if st.button("📋 Skin Diagnostic Assessment", use_container_width=True):
        st.session_state.active_view = "Assessment"
        st.rerun()
        
    if st.button("🛒 Recommendation Engine Results", use_container_width=True):
        if not st.session_state.tracked_skin_issues:
            st.sidebar.warning("⚠️ Complete assessment inputs first.")
        else:
            st.session_state.active_view = "Results"
            st.rerun()

# ==========================================
# 4. VIEW PAGE ROUTING CONTROLS
# ==========================================

# --- HOMEPAGE VIEW ---
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

# --- ASSESSMENT PARAMETERS INPUT VIEW ---
elif st.session_state.active_view == "Assessment":
    st.title("📋 Skin Profile Diagnostic")
    st.markdown("Select your structural skin criteria below to filter the engine registry rules.")
    st.write("---")

    # STRICT DIRECT DATABASE CONNECTIONS (No hardcoded fallbacks)
    try:
        conn = get_db_connection()
        db_types = conn.execute("SELECT skin_type_id, skin_type_name FROM skin_type").fetchall()
        db_issues = conn.execute("SELECT issue_id, issue_name FROM skin_issue").fetchall()
        conn.close()
        
        # Build strict dictionary maps directly from the active SQL rows
        SKIN_TYPES_MAP = {row["skin_type_id"]: row["skin_type_name"] for row in db_types}
        SKIN_ISSUES_MAP = {row["issue_id"]: row["issue_name"] for row in db_issues}
    except Exception as db_err:
        st.error(f"❌ Critical Database Mapping Error: Could not extract live tables. Matrix Details: {db_err}")
        st.stop()

    # Fallback validation to ensure tables aren't completely empty files
    if not SKIN_TYPES_MAP or not SKIN_ISSUES_MAP:
        st.error("❌ Database Connection Succeeded, but your 'skin_type' or 'skin_issue' tables contain 0 rows.")
        st.stop()

    # 1. Single Dropdown Selection for Skin Typology (Reads directly from skin_type table)
    selected_type_id = st.selectbox(
        "1. Select Your Biological Skin Typology (Single Choice Dropdown):",
        options=list(SKIN_TYPES_MAP.keys()),
        format_func=lambda x: SKIN_TYPES_MAP[x]
    )
    st.session_state.tracked_skin_type = selected_type_id

    # 2. Multi-Select Elements Matrix For Overlapping Concerns (Reads directly from skin_issue table)
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
                st.error("Validation Error: Please select at least one skin issue parameter before processing recommendations.")
            else:
                st.session_state.active_view = "Results"
                st.rerun()

# --- RECOMMENDATION FILTER ENGINE RESULTS VIEW ---
elif st.session_state.active_view == "Results":
    st.title("🛒 Filtered Product Matrix Results")
    st.markdown(f"Displaying dynamic rule recommendations matching Skin Type: **{SKIN_TYPES_MAP.get(st.session_state.tracked_skin_type, 'Unmapped')}** and selected condition filters.")
    st.write("---")
    
    if not st.session_state.tracked_skin_issues:
        st.info("No query params stored in profile stack. Please complete the assessment view profile.")
        if st.button("Go to Assessment View", use_container_width=True):
            st.session_state.active_view = "Assessment"
            st.rerun()
    else:
        try:
            conn = get_db_connection()
            issue_placeholders = ",".join("?" * len(st.session_state.tracked_skin_issues))
            
            # Complex relational join logic linking product properties, conditions, and category schemas
            query = f"""
                SELECT DISTINCT 
                    p.product_id, p.product_name, p.brand, p.product_url, c.category_name
                FROM product p
                JOIN product_skin_type pst ON p.product_id = pst.product_id
                JOIN product_skin_issue psi ON p.product_id = psi.product_id
                JOIN category c ON p.category_id = c.category_id
                WHERE pst.skin_type_id = ? 
                AND psi.issue_id IN ({issue_placeholders})
                ORDER BY c.category_id, p.brand, p.product_name
            """
            
            execution_params = [st.session_state.tracked_skin_type] + st.session_state.tracked_skin_issues
            matched_records = conn.execute(query, execution_params).fetchall()
            conn.close()
            
            if not matched_records:
                st.info("No structural formula options currently match your specific criteria matrix combinations within our product tables.")
            else:
                export_accumulator = []
                df_conversion = pd.DataFrame([dict(row) for row in matched_records])
                category_grouped = df_conversion.groupby('category_name')
                
                # Render sorted output structures separated by Category headers
                for category_group_title, category_data_rows in category_grouped:
                    st.markdown(f'<div class="cat-title-header">{category_group_title}</div>', unsafe_allow_html=True)
                    
                    for index_pos, item_row in category_data_rows.iterrows():
                        export_accumulator.append({
                            "Category": item_row['category_name'],
                            "Brand": item_row['brand'] if item_row['brand'] else "Generic",
                            "Product Name": item_row['product_name'],
                            "Source URL": item_row['product_url'] if item_row['product_url'] else "N/A"
                        })
                        
                        url_binding_html = f"<a href='{item_row['product_url']}' target='_blank' style='color:#2E5A36; font-weight:bold;'>View Formulation Source</a>" if item_row['product_url'] else ""
                        st.markdown(f"""
                            <div class="product-display-card">
                                <div class="brand-meta-text">{item_row['brand'] if item_row['brand'] else 'Generic'}</div>
                                <div class="product-main-title">{item_row['product_name']}</div>
                                {url_binding_html}
                            </div>
                        """, unsafe_allow_html=True)
                
                # Reporting Actions and File Exports Container
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
            st.error(f"Runtime Query Failure encountered during execution: {query_error}")
            
    st.write("---")
    if st.button("↺ Restart Diagnostic Profile Sequence", use_container_width=True):
        st.session_state.tracked_skin_issues = []
        st.session_state.active_view = "Assessment"
        st.rerun()