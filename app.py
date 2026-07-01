import os
import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime
from init_db import init_database_with_real_data, DB_PATH

# Initialize database on app startup if missing
if not os.path.exists(DB_PATH):
    init_database_with_real_data()

# Initialize session history tracking state capped at 50 records max
if "session_history" not in st.session_state:
    st.session_state.session_history = []

st.set_page_config(page_title="Skinalyze | Matrix Recommendation Engine", page_icon="🌿", layout="centered")

# CSS Styling Matching original dashboard architecture
st.markdown("""
    <style>
    .cat-title-header { font-size: 24px; font-weight: bold; color: #4a5c4e; border-bottom: 2px solid #E2E8F0; padding-bottom: 6px; margin-top: 25px; margin-bottom: 15px; }
    .product-display-card { background-color: #F8FAFC; padding: 18px; border-radius: 10px; border-left: 5px solid #4a5c4e; margin-bottom: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .product-main-title { font-size: 18px; color: #1E293B; margin: 0; font-weight: 600; }
    .product-brand { font-size: 14px; color: #64748B; font-weight: 500; text-transform: uppercase; margin-bottom: 5px; }
    .product-ingredients { font-size: 13px; color: #475569; background-color: #EDF2F7; padding: 6px 10px; border-radius: 6px; margin-top: 8px; }
    </style>
""", unsafe_allow_html=True)

# Sidebar view navigation setup
st.sidebar.title("🌿 Skinalyze Nav Matrix")
current_view = st.sidebar.radio("Navigate Workspace:", ["Home/Portal", "Skin Assessment", "Information Guide", "Session History"])

# Establish clean connection helper
def get_db_records():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
# VIEW 1: PORTAL HOME
# ==========================================
if current_view == "Home/Portal":
    st.title("Welcome to Skinalyze")
    st.subheader("Smart Rule-Based Skincare Alignment Matrix")
    st.write("Our alignment matrix compares cross-functional product parameters against your targeted biological properties to generate optimized routines.")
    
    st.info("ℹ️ **Disclaimer:** This system provides prompt cosmetic ingredient pairings. It is not a replacement for a dermatologist.")
    if st.button("Start Skin Assessment Matrix →", use_container_width=True):
        st.switch_page("app.py") # Triggers refresh visually

# ==========================================
# VIEW 2: SKIN ASSESSMENT
# ==========================================
elif current_view == "Skin Assessment":
    st.title("🔬 Clinical Profile Diagnostic")
    
    # Pull selections directly from database to avoid broken static assets
    conn = get_db_records()
    cursor = conn.cursor()
    
    cursor.execute("SELECT skin_type_id, skin_type_name FROM skin_type;")
    skin_type_map = {row["skin_type_name"]: row["skin_type_id"] for row in cursor.fetchall()}
    
    cursor.execute("SELECT issue_id, issue_name FROM skin_issue ORDER BY issue_name;")
    skin_issue_map = {row["issue_name"]: row["issue_id"] for row in cursor.fetchall()}
    conn.close()

    with st.form("assessment_matrix_form"):
        user_name = st.text_input("Enter Client Profile Reference / Name:", placeholder="Anonymous Profile")
        selected_type_name = st.selectbox("1. Identify Primary Biological Skin Type:", list(skin_type_map.keys()))
        selected_issue_name = st.selectbox("2. Identify Target Dermatological Concern:", list(skin_issue_map.keys()))
        
        submit_diagnostic = st.form_submit_button("Process Recommendation Architecture", use_container_width=True)

    if submit_diagnostic:
        # Resolve textual selections back to valid database integers safely
        target_type_id = skin_type_map[selected_type_name]
        target_issue_id = skin_issue_map[selected_issue_name]
        
        try:
            conn = get_db_records()
            cursor = conn.cursor()
            
            # The Exact Rule-Based Query fetching ingredient intersections
            # Updated robust query with fallback mechanics
            query = """
                SELECT DISTINCT p.product_id, p.product_name, c.category_name, p.description
                FROM product p
                JOIN category c ON p.category_id = c.category_id
                JOIN product_skin_type pst ON p.product_id = pst.product_id
                JOIN product_skin_issue psi ON p.product_id = psi.product_id
                WHERE 
                    -- Primary matching logic
                    (pst.skin_type_id = %s AND psi.issue_id = %s)
                    OR 
                    -- Intelligent Fallback: If it matches Acne (1), also pull items 
                    -- tagged with Oil Control issues (3) since they go hand-in-hand
                    (psi.issue_id = %s AND %s = 3 AND psi.issue_id = 1)
                GROUP BY p.product_id
                ORDER BY c.category_id ASC, p.product_name ASC
            """
            # Pass (skin_type_id, issue_id, issue_id, skin_type_id) to the execution tuple
            cursor.execute(query, (skin_type_id, issue_id, issue_id, skin_type_id))
            raw_rows = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            # Process Category Bucketing
            bucketed_recommendations = {}
            for item in raw_rows:
                cat = item.get("category_name", "General Care")
                if cat not in bucketed_recommendations:
                    bucketed_recommendations[cat] = []
                bucketed_recommendations[cat].append(item)
                
            # Enforce Top 5 Capping Rule per Category Step
            for cat in bucketed_recommendations:
                bucketed_recommendations[cat] = bucketed_recommendations[cat][:5]
                
            # Log successful compilation into session state history tracking logs
            history_record = {
                "name": user_name if user_name.strip() else "Anonymous Matrix",
                "type": selected_type_name,
                "issue": selected_issue_name,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "results": bucketed_recommendations
            }
            st.session_state.session_history.insert(0, history_record)
            if len(st.session_state.session_history) > 50:
                st.session_state.session_history.pop()

            # Output UI Display Elements
            st.success(f"✔️ Alignment Compiled! Found product combinations matching: {selected_type_name} + {selected_issue_name}")
            
            if not bucketed_recommendations:
                st.warning("⚠️ No strict product mappings exist in database matrices matching this combination.")
            else:
                export_accumulator = []
                for category, products in bucketed_recommendations.items():
                    st.markdown(f'<div class="cat-title-header">🧼 Step Category: {category}</div>', unsafe_allow_html=True)
                    for prod in products:
                        brand_text = prod['brand'] if prod.get('brand') else 'Clinical Formula'
                        ing_text = prod['active_ingredients'] if prod.get('active_ingredients') else 'Base Hydrating Emulsion'
                        desc_text = prod['description'] if prod.get('description') else 'No documentation specified.'
                        
                        st.markdown(f"""
                            <div class="product-display-card">
                                <div class="product-brand">{brand_text}</div>
                                <div class="product-main-title">{prod['product_name']}</div>
                                <div style="margin-top:5px; color:#475569; font-size:14px;">{desc_text}</div>
                                <div class="product-ingredients"><b>Key Compounds:</b> {ing_text}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        export_accumulator.append({
                            "Category": category,
                            "Brand": brand_text,
                            "Product Name": prod['product_name'],
                            "Description": desc_text,
                            "Ingredients": ing_text
                        })
                
                # Output Data Utilities Export Frame
                st.write("---")
                st.subheader("📋 Routine Administration Operations")
                csv_payload = pd.DataFrame(export_accumulator).to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export Current Routine Data Frame (.CSV File)",
                    data=csv_payload,
                    file_name="skinalyze_curated_routine.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
        except Exception as err:
            st.error(f"Engine Registry Fault: {err}")

# ==========================================
# VIEW 3: INFORMATION GUIDE
# ==========================================
elif current_view == "Information Guide":
    st.title("📖 Biological Matrix Guide")
    st.write("Review the rule parameters behind the recommendation engine layers:")
    st.markdown("""
    - **Oily Matrix Rules:** Targets formulations regulating excessive sebum using micro-exfoliants (Salicylic Acids, Witch hazel, Clay) combined with non-comedogenic bases.
    - **Acne Matrix Rules:** Filters specifically for antiseptic, pore-clearing agents (Benzoyl peroxide, Salicylic compound strings) mapped cross-functionally through Cleanser and Serum indices.
    - **Combination / Fallback Filters:** Elements missing definitive classifications fallback automatically to standardized balancing matrices.
    """)

# ==========================================
# VIEW 4: SESSION HISTORY
# ==========================================
elif current_view == "Session History":
    st.title("⏳ Volatile Memory History Matrix")
    st.write("Displays the 50 most recent records stored during this session session run:")
    
    if st.button("Clear Volatile Session Logs", type="primary", use_container_width=True):
        st.session_state.session_history = []
        st.rerun()
        
    if not st.session_state.session_history:
        st.info("No assessment records found in memory cache yet.")
    else:
        for idx, record in enumerate(st.session_state.session_history):
            with st.expander(f"Record #{idx+1}: {record['name']} — {record['timestamp']}"):
                st.write(f"**Parameters Passed:** Skin Type: `{record['type']}`, Target Issue: `{record['issue']}`")
                st.write("**Curated Allocation Categories:**")
                for cat, prods in record['results'].items():
                    st.write(f"- **{cat}**: {len(prods)} products matched and limited.")