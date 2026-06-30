import os
import sqlite3
import pandas as pd
import streamlit as st

# 1. PAGE SETUP & STYLING
st.set_page_config(
    page_title="Skinalyze | Precision Skincare Engine",
    page_icon="🌿",
    layout="centered"
)

st.markdown("""
    <style>
    .category-header { font-size: 22px; font-weight: bold; color: #2E5A36; border-bottom: 2px solid #E0E0E0; padding-bottom: 5px; margin-top: 25px; margin-bottom: 15px; }
    .product-card { background-color: #F9FBF9; padding: 15px; border-radius: 8px; border-left: 4px solid #2E5A36; margin-bottom: 12px; }
    @media print {
        header, footer, .stButton, [data-testid="stSidebar"], [data-testid="stHeader"] { display: none !important; }
        .main .block-container { padding-top: 0rem !important; }
        body { color: #000000 !important; background-color: #FFFFFF !important; }
    }
    </style>
""", unsafe_allow_html=True)

# Define Hardcoded Fail-Safe Options so dropdowns can NEVER break
FALLBACK_TYPES = [
    {"id": 1, "name": "Oily"},
    {"id": 2, "name": "Dry"},
    {"id": 3, "name": "Combination"},
    {"id": 4, "name": "Sensitive"}
]

FALLBACK_ISSUES = [
    {"id": 1, "name": "Acne"},
    {"id": 2, "name": "Dryness"},
    {"id": 3, "name": "Oiliness"},
    {"id": 4, "name": "Redness"},
    {"id": 5, "name": "Aging"}
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "skincare.db")

# 2. SEEDING ENGINE TO PREVENT EMPTY DB FILES
def verify_and_force_seed():
    """Builds and forces rows into the database if missing."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("CREATE TABLE IF NOT EXISTS skin_type (skin_type_id INTEGER PRIMARY KEY, skin_type_name TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS skin_issue (issue_id INTEGER PRIMARY KEY, issue_name TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS category (category_id INTEGER PRIMARY KEY, category_name TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS product (product_id INTEGER PRIMARY KEY, product_name TEXT, brand TEXT, category_id INTEGER, image_url TEXT, product_url TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS product_skin_type (product_id INTEGER, skin_type_id INTEGER)")
        cursor.execute("CREATE TABLE IF NOT EXISTS product_skin_issue (product_id INTEGER, issue_id INTEGER)")
        
        cursor.execute("SELECT COUNT(*) FROM skin_type")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("INSERT INTO skin_type VALUES (?,?)", [(t['id'], t['name']) for t in FALLBACK_TYPES])
            
        cursor.execute("SELECT COUNT(*) FROM skin_issue")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("INSERT INTO skin_issue VALUES (?,?)", [(i['id'], i['name']) for i in FALLBACK_ISSUES])
            
        cursor.execute("SELECT COUNT(*) FROM category")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("INSERT INTO category VALUES (?,?)", [(1,'Cleanser'), (2,'Moisturizer'), (3,'Serum'), (4,'Toner'), (5,'Sunscreen')])
            
        conn.commit()
        conn.close()
    except Exception:
        pass  # Quiet bypass to allow memory array fallback to run cleanly

# Execute database structure check
verify_and_force_seed()

# 3. EXTRACT DROPDOWN MENU DATA ROWS Safely
skin_type_options = []
skin_issue_options = []
category_map = {1: 'Cleanser', 2: 'Moisturizer', 3: 'Serum', 4: 'Toner', 5: 'Sunscreen'}

try:
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        db_types = cursor.execute("SELECT skin_type_id, skin_type_name FROM skin_type").fetchall()
        skin_type_options = [{"id": r["skin_type_id"], "name": r["skin_type_name"]} for r in db_types]
        
        db_issues = cursor.execute("SELECT issue_id, issue_name FROM skin_issue").fetchall()
        skin_issue_options = [{"id": r["issue_id"], "name": r["issue_name"]} for r in db_issues]
        
        db_cats = cursor.execute("SELECT category_id, category_name FROM category").fetchall()
        if db_cats:
            category_map = {r["category_id"]: r["category_name"] for r in db_cats}
            
        conn.close()
except Exception:
    pass

# Direct Fallback Assignment if database reads returned absolutely empty values
if not skin_type_options:
    skin_type_options = FALLBACK_TYPES
if not skin_issue_options:
    skin_issue_options = FALLBACK_ISSUES

# 4. UI SELECTION DROPDOWNS
st.title("🌿 Skinalyze Routine Matrix")
st.markdown("Select your biological parameters below to calculate a targeted rule-based product recommendation regime.")

col1, col2 = st.columns(2)

with col1:
    selected_type_id = st.selectbox(
        "1. Biological Skin Typology",
        options=[t["id"] for t in skin_type_options],
        format_func=lambda x: next(t["name"] for t in skin_type_options if t["id"] == x)
    )

with col2:
    selected_issue_id = st.selectbox(
        "2. Primary Matrix Condition",
        options=[i["id"] for i in skin_issue_options],
        format_func=lambda x: next(i["name"] for i in skin_issue_options if i["id"] == x)
    )

# 5. RECOMMENDATION ENGINE CALCULATION
if st.button("Generate Recommendation Profile", use_container_width=True):
    results = []
    try:
        if os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = """
                SELECT DISTINCT p.product_id, p.product_name, p.brand, p.category_id, p.image_url, p.product_url
                FROM product p
                JOIN product_skin_type pst ON p.product_id = pst.product_id
                JOIN product_skin_issue psi ON p.product_id = psi.product_id
                WHERE pst.skin_type_id = ? AND psi.issue_id = ?
            """
            db_results = cursor.execute(query, (selected_type_id, selected_issue_id)).fetchall()
            results = [dict(row) for row in db_results]
            conn.close()
    except Exception as e:
        st.error(f"Database Query Error: {e}")

    if not results:
        st.info("No matching structural products mapped to this configuration profile inside the database yet.")
    else:
        st.success(f"Algorithm processing complete. Found {len(results)} matching formulas across internal registries.")
        report_data = []
        
        # Sort and render items separated neatly by categories
        for cat_id, cat_name in category_map.items():
            cat_products = [p for p in results if p['category_id'] == cat_id]
            
            if cat_products:
                st.markdown(f'<div class="category-header">{cat_name}</div>', unsafe_allow_html=True)
                for prod in cat_products:
                    report_data.append({
                        "Category": cat_name, "Brand": prod.get('brand',''),
                        "Product Name": prod.get('product_name',''), "Resource URL": prod.get('product_url','') if prod.get('product_url','') else "N/A"
                    })
                    with st.container():
                        st.markdown(f"""
                            <div class="product-card">
                                <span style="color:#757575; font-size:12px; text-transform:uppercase; letter-spacing:1px;">{prod.get('brand','Generic')}</span>
                                <h4 style="margin: 2px 0 8px 0; color:#333;">{prod.get('product_name','Unnamed Formula')}</h4>
                                {"<a href='" + prod['product_url'] + "' target='_blank' style='color:#2E5A36; font-size:14px; font-weight:bold;'>View Product Source</a>" if prod.get('product_url','') else ""}
                            </div>
                        """, unsafe_allow_html=True)
        
        if report_data:
            st.markdown("---")
            st.subheader("📋 Export & Print Options")
            report_df = pd.DataFrame(report_data)
            csv_payload = report_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Routine Report File (.CSV)", data=csv_payload,
                file_name="skinalyze_skincare_routine.csv", mime="text/csv", use_container_width=True
            )
            st.info("💡 **To Print or Save to PDF directly:** Simply hit **Ctrl + P** (or **Cmd + P** on Mac).")