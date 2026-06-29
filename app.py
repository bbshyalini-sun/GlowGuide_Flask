import os
import mysql.connector
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Skinalyze | Precision Skin Diagnostics",
    page_icon="🌿",
    layout="centered"
)

# 2. Database Connection Config (Preserved from original Flask app)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'skincare_system',
    'charset': 'utf8mb4'
}

# 3. Core Database Helper Functions
def fetch_options():
    """Fetches skin types and issues with exact default fallbacks from your Flask app."""
    skin_types = []
    skin_issues = []
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT skin_type_id, skin_type_name FROM skin_type")
        skin_types = cursor.fetchall() or []

        cursor.execute("SELECT issue_id, issue_name FROM skin_issue ORDER BY issue_name")
        skin_issues = cursor.fetchall() or []
        
        cursor.close()
        conn.close()
    except Exception:
        # Gracefully handle missing/uninitialized databases safely
        pass
        
    if not skin_types:
        skin_types = [
            {'skin_type_id': 1, 'skin_type_name': 'Oily'},
            {'skin_type_id': 2, 'skin_type_name': 'Dry'},
            {'skin_type_id': 3, 'skin_type_name': 'Combination'},
            {'skin_type_id': 4, 'skin_type_name': 'Sensitive'},
        ]
    if not skin_issues:
        skin_issues = [
            {'issue_id': 1, 'issue_name': 'Acne'},
            {'issue_id': 2, 'issue_name': 'Dryness'},
            {'issue_id': 3, 'issue_name': 'Oiliness'},
            {'issue_id': 4, 'issue_name': 'Redness'},
            {'issue_id': 5, 'issue_name': 'Dark Spots'},
        ]
    return skin_types, skin_issues


def get_recommendations(skin_type_id, issue_id):
    """Executes the specific JOIN matrix execution and categorizes results."""
    raw_products = []
    selected_type_name = "Selected Skin Type"
    selected_issue_name = "Selected Concern"
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT skin_type_name FROM skin_type WHERE skin_type_id = %s", (skin_type_id,))
        res_type = cursor.fetchone()
        if res_type:
            selected_type_name = res_type['skin_type_name']

        cursor.execute("SELECT issue_name FROM skin_issue WHERE issue_id = %s", (issue_id,))
        res_issue = cursor.fetchone()
        if res_issue:
            selected_issue_name = res_issue['issue_name']
            
        query = """
            SELECT 
                p.product_name, p.brand, p.description, c.category_name,
                GROUP_CONCAT(i.ingredient_name, ', ') AS active_ingredients
            FROM product p
            JOIN category c ON p.category_id = c.category_id
            JOIN product_skin_type pst ON p.product_id = pst.product_id
            JOIN product_skin_issue psi ON p.product_id = psi.product_id
            LEFT JOIN product_ingredient pi ON p.product_id = pi.product_id
            LEFT JOIN ingredient i ON pi.ingredient_id = i.ingredient_id
            WHERE pst.skin_type_id = %s AND psi.issue_id = %s
            GROUP BY p.product_id
            ORDER BY c.category_id ASC, p.product_name ASC
        """
        cursor.execute(query, (skin_type_id, issue_id))
        raw_products = cursor.fetchall() or []
        cursor.close()
        conn.close()
    except Exception:
        pass

    # Group linear query data records into structural bucket dictionaries
    recommendations = {}
    for prod in raw_products:
        prod_dict = prod.copy() if isinstance(prod, dict) else dict(prod)
        if 'brand' not in prod_dict or not prod_dict.get('brand') or prod_dict.get('brand') == 'Skinalyze':
            prod_dict['brand'] = None

        cat = prod_dict.get('category_name', 'Uncategorized')
        if cat not in recommendations:
            recommendations[cat] = []
        recommendations[cat].append(prod_dict)

    # Hard-enforce maximum cap boundary of 5 records per functional category block
    for category, products in recommendations.items():
        recommendations[category] = products[:5]
        
    return recommendations, selected_type_name, selected_issue_name


# 4. State Management Integration for Seamless Navigation Transitions
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "results_data" not in st.session_state:
    st.session_state.results_data = None
if "feedback" not in st.session_state:
    st.session_state.feedback = None

def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()


# 5. Sidebar Layout & Navigation Structure
st.sidebar.title("🌿 Skinalyze Navigation")
st.sidebar.markdown("---")

if st.sidebar.button("🏠 Home Dashboard", use_container_width=True):
    navigate_to("Home")
if st.sidebar.button("📋 Profile Assessment Matrix", use_container_width=True):
    st.session_state.results_data = None  # Clear previous run views
    st.session_state.feedback = None
    navigate_to("Assessment")
if st.sidebar.button("ℹ️ Scientific Information Guide", use_container_width=True):
    navigate_to("Information")


# 6. Page View Components
# ──────────────────────────────────────────────────────────────────────────
# PAGE: HOME VIEW (Replicates index.html functionality)
if st.session_state.page == "Home":
    st.markdown("<div style='text-align: right;'><span style='background-color:#d4edda; color:#155724; padding:4px 10px; border-radius:12px; font-size:0.85rem;'>Matrix Engine Ready</span></div>", unsafe_gradient=True)
    
    st.title("Skinalyze")
    st.markdown("### Welcome to your smart rule-based skincare matching system.")
    st.write(
        "Our alignment matrix compares cross-functional product parameters against "
        "your targeted biological properties to generate clinical combinations."
    )
    
    st.warning(
        "**Disclaimer:** This website provides quick skincare recommendations only. "
        "It is not a replacement for a dermatologist and should not override professional "
        "dermatological advice. If you are experiencing a severe skin issue, please "
        "seek medical care from a qualified professional."
    )
    
    if st.button("Start Skin Assessment →", type="primary", use_container_width=True):
        navigate_to("Assessment")


# ──────────────────────────────────────────────────────────────────────────
# PAGE: ASSESSMENT VIEW & RESULTS (Replicates assessment.html & result.html)
elif st.session_state.page == "Assessment":
    st.title("Skincare Diagnostics Profile")
    st.write("Configure your exact physiological target markers to filter the database matrices.")
    
    skin_types, skin_issues = fetch_options()
    
    # Selection Mapping Builders
    type_mapping = {item['skin_type_name']: item['skin_type_id'] for item in skin_types}
    issue_mapping = {item['issue_name']: item['issue_id'] for item in skin_issues}
    
    # Form Interface Rendering
    with st.form("diagnostic_matrix_form"):
        selected_type_label = st.selectbox("1. Identify Primary Skin Type:", options=list(type_mapping.keys()))
        selected_issue_label = st.selectbox("2. Isolate Target Epidermal Concern:", options=list(issue_mapping.keys()))
        
        submit_btn = st.form_submit_button("Process Recommendation Architecture", type="primary", use_container_width=True)
        
    if submit_btn:
        st.session_state.feedback = None  # Reset feedback on new query
        st.session_state.results_data = get_recommendations(
            type_mapping[selected_type_label], 
            issue_mapping[selected_issue_label]
        )

    # Inline Rendering Engine for Recommendations (result.html layout conversion)
    if st.session_state.results_data is not None:
        recs, type_name, issue_name = st.session_state.results_data
        
        st.markdown("---")
        st.header("Your Personalized Architecture Matrix Routine")
        st.info(f"**Target Diagnostic Match Parameters:** {type_name} Skin | {issue_name} Target Focus")
        
        if recs:
            for category_name, products in recs.items():
                st.markdown(f"### 🏷️ Category: {category_name}")
                
                for prod in products:
                    # Emulate visual design card borders via native streamlit containers
                    with st.container(border=True):
                        brand_display = prod['brand'] if prod['brand'] else "Generic / Formulated Formulation"
                        st.subheader(f"{prod['product_name']} (`{brand_display}`)")
                        
                        if prod['active_ingredients']:
                            st.markdown(f"**Active Chemical Traces:** *{prod['active_ingredients']}*")
                        else:
                            st.markdown("**Active Chemical Traces:** *Standard base properties*")
                            
                        st.write(prod['description'])
                st.write("")
                
            # Interactive User Assessment Feedback Loop Component
            st.markdown("##### Was this matrix configuration calculation optimal for your objectives?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 Yes, Accurate", use_container_width=True):
                    st.session_state.feedback = "success"
            with col2:
                if st.button("👎 No, Inaccurate", use_container_width=True):
                    st.session_state.feedback = "warning"
                    
            if st.session_state.feedback == "success":
                st.success("Thank you for using Skinalyze services.")
            elif st.session_state.feedback == "warning":
                st.warning("We apologize for the experience. Would you like to retry the diagnostic?")
        else:
            st.error("### No matching profile sets compiled.")
            st.write("Verify your underlying logic matrices contain products configured for this precise intersection of parameters.")


# ──────────────────────────────────────────────────────────────────────────
# PAGE: INFORMATION GUIDE (Replicates info.html functionality)
elif st.session_state.page == "Information":
    st.title("Skinalyze | Information Guide")
    
    st.markdown("### 1. Biological Skin Typologies")
    st.markdown(
        """
        - **Oily:** Characterized by hyper-production of lipid sebum layers. Requires oil-less structural carriers (e.g., Gel foundations) combined with sebum-control actives such as Salicylic Acid or Niacinamide.
        - **Dry:** Breakdown of barrier lipids. Requires deep moisture traps like Ceramides, Humectants, and rich creams to lower trans-epidermal moisture loss.
        - **Combination:** Fluctuating skin parameters across regions (dry zones versus over-productive T-zones), calling for strict systemic balancing routines.
        - **Sensitive:** Highly reactive barrier prone to irritation. Requires calming components such as Centella Asiatica (Cica), Panthenol, and clean mineral-based UV filters.
        """
    )
    
    st.markdown("### 2. Matrix Target Alignments")
    st.write(
        "The core matrix runs deep calculations to target precise conditions. For example, selecting "
        "Acne flags the query to highlight formulations with anti-bacterial or micro-exfoliating properties, "
        "while selecting Redness restricts matches to soothing ingredients with anti-inflammatory characteristics."
    )
    
    st.write("")
    if st.button("Return to Live Profiler Matrix", use_container_width=True):
        navigate_to("Assessment")