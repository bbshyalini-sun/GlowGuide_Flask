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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "skincare.db")

# 2. EMERGENCY AUTO-SEEDER LOGIC
def repair_and_seed_tables():
    """Ensures that essential metadata tables are structured and populated no matter what."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Ensure tables exist
    cursor.execute("CREATE TABLE IF NOT EXISTS skin_type (skin_type_id INTEGER PRIMARY KEY, skin_type_name TEXT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS skin_issue (issue_id INTEGER PRIMARY KEY, issue_name TEXT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS category (category_id INTEGER PRIMARY KEY, category_name TEXT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS product (product_id INTEGER PRIMARY KEY, product_name TEXT, brand TEXT, category_id INTEGER, image_url TEXT, product_url TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS product_skin_type (product_id INTEGER, skin_type_id INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS product_skin_issue (product_id INTEGER, issue_id INTEGER)")

    # Check and insert skin types if empty
    cursor.execute("SELECT COUNT(*) FROM skin_type")
    if cursor.fetchone()[0] == 0:
        types = [(1, 'Oily'), (2, 'Dry'), (3, 'Combination'), (4, 'Sensitive')]
        cursor.executemany("INSERT INTO skin_type (skin_type_id, skin_type_name) VALUES (?, ?)", types)
        
    # Check and insert skin issues if empty
    cursor.execute("SELECT COUNT(*) FROM skin_issue")
    if cursor.fetchone()[0] == 0:
        issues = [(1, 'Acne'), (2, 'Dryness'), (3, 'Oiliness'), (4, 'Redness'), (5, 'Aging')]
        cursor.executemany("INSERT INTO skin_issue (issue_id, issue_name) VALUES (?, ?)", issues)

    # Check and insert core categories if empty
    cursor.execute("SELECT COUNT(*) FROM category")
    if cursor.fetchone()[0] == 0:
        cats = [(1, 'Cleanser'), (2, 'Moisturizer'), (3, 'Serum'), (4, 'Toner'), (5, 'Sunscreen')]
        cursor.executemany("INSERT INTO category (category_id, category_name) VALUES (?, ?)", cats)

    conn.commit()
    conn.close()

# Run the database verification program explicitly
try:
    if not os.path.exists(DB_PATH):
        try:
            import init_db
            init_db.init_database_with_real_data()
        except Exception:
            pass
    repair_and_seed_tables()
except Exception as e:
    st.error(f"Database Initialization Warning: {e}")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 3. COMPILING DIAGNOSTIC VARIABLES
try:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    skin_types = cursor.execute("SELECT skin_type_id, skin_type_name FROM skin_type").fetchall()
    skin_issues = cursor.execute("SELECT issue_id, issue_name FROM skin_issue").fetchall()
    categories = cursor.execute("SELECT category_id, category_name FROM category ORDER BY category_id").fetchall()
    
    conn.close()
except Exception as e:
    st.error("Critical Dropdown Failure: Could not read metadata records from database.")
    st.stop()

# 4. UI RENDER SEQUENCE
st.title("🌿 Skinalyze Routine Matrix")
st.markdown("Select your biological parameters below to calculate a targeted rule-based product recommendation regime.")

col1, col2 = st.columns(2)
with col1:
    selected_type_id = st.selectbox(
        "1. Biological Skin Typology",
        options=[st_item['skin_type_id'] for st_item in skin_types],
        format_func=lambda x: next(st_item['skin_type_name'] for st_item in skin_types if st_item['skin_type_id'] == x)
    )

with col2:
    selected_issue_id = st.selectbox(
        "2. Primary Matrix Condition",
        options=[si_item['issue_id'] for si_item in skin_issues],
        format_func=lambda x: next(si_item['issue_name'] for si_item in skin_issues if si_item['issue_id'] == x)
    )

# 5. RECOMMENDATION COMPUTATION ENGINE (Rule-Based Algorithm)
if st.button("Generate Recommendation Profile", use_container_width=True):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT DISTINCT 
                p.product_id, p.product_name, p.brand, p.category_id, p.image_url, p.product_url
            FROM product p
            JOIN product_skin_type pst ON p.product_id = pst.product_id
            JOIN product_skin_issue psi ON p.product_id = psi.product_id
            WHERE pst.skin_type_id = ? AND psi.issue_id = ?
        """
        results = cursor.execute(query, (selected_type_id, selected_issue_id)).fetchall()
        conn.close()
        
        if not results:
            st.info("No matching structural products mapped to this configuration profile inside the inventory database yet.")
        else:
            st.success(f"Algorithm processing complete. Found {len(results)} matching formulas across internal registries.")
            report_data = []
            
            for cat in categories:
                cat_products = [p for p in results if p['category_id'] == cat['category_id']]
                if cat_products:
                    st.markdown(f'<div class="category-header">{cat["category_name"]}</div>', unsafe_allow_html=True)
                    for prod in cat_products:
                        report_data.append({
                            "Category": cat['category_name'], "Brand": prod['brand'],
                            "Product Name": prod['product_name'], "Resource URL": prod['product_url'] if prod['product_url'] else "N/A"
                        })
                        with st.container():
                            st.markdown(f"""
                                <div class="product-card">
                                    <span style="color:#757575; font-size:12px; text-transform:uppercase; letter-spacing:1px;">{prod['brand']}</span>
                                    <h4 style="margin: 2px 0 8px 0; color:#333;">{prod['product_name']}</h4>
                                    {"<a href='" + prod['product_url'] + "' target='_blank' style='color:#2E5A36; font-size:14px; font-weight:bold;'>View Product Source</a>" if prod['product_url'] else ""}
                                </div>
                            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.subheader("📋 Export & Print Options")
            report_df = pd.DataFrame(report_data)
            csv_payload = report_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Routine Report File (.CSV)", data=csv_payload,
                file_name="skinalyze_skincare_routine.csv", mime="text/csv", use_container_width=True
            )
            st.info("💡 **To Print or Save to PDF directly:** Simply hit **Ctrl + P** (or **Cmd + P** on Mac).")
    except Exception as e:
        st.error(f"Error executing recommendation rule algorithm: {e}")