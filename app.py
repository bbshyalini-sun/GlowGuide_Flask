import os
import io
import sqlite3
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

# ==========================================
# 1. PAGE CONFIGURATION & GLOBAL STYLES
# ==========================================
st.set_page_config(
    page_title="Skinalyze",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_BACKGROUND = "#f7f9fb"
CARD_BACKGROUND = "#ffffff"
TEXT = "#0f172a"
MUTED = "#475569"
PRIMARY = "#2f6c72"
PRIMARY_DARK = "#255a5d"
ACCENT = "#4d7c72"

st.markdown(
    f"""
    <style>
        :root {{ color-scheme: light; }}
        body {{ background: {APP_BACKGROUND}; }}
        .stApp {{ background: {APP_BACKGROUND}; color: {TEXT}; }}
        [data-testid="stAppViewContainer"] {{ background: {APP_BACKGROUND}; }}
        [data-testid="stSidebar"] {{ background: #ffffff; border-right: 1px solid rgba(15, 23, 42, 0.08); }}
        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        header {{ visibility: hidden; }}
        [data-testid="collapsedControl"] {{ display: none !important; }}

        .hero-panel {{
            background: linear-gradient(180deg, rgba(47,108,114,0.12), rgba(255,255,255,0.95));
            border: 1px solid rgba(79, 143, 143, 0.18);
            border-radius: 28px;
            padding: 36px;
            margin-bottom: 32px;
            box-shadow: 0 20px 60px rgba(47,108,114,0.08);
        }}
        .hero-title {{ font-size: 3rem; font-weight: 800; margin: 0; color: {TEXT}; }}
        .hero-subtitle {{ font-size: 1.05rem; color: {MUTED}; margin-top: 16px; max-width: 720px; }}
        .section-card {{
            background: {CARD_BACKGROUND};
            border-radius: 22px;
            padding: 28px;
            border: 1px solid rgba(15, 23, 42, 0.08);
            box-shadow: 0 16px 40px rgba(15, 23, 42, 0.04);
            margin-bottom: 24px;
        }}
        .feature-card {{
            background: {CARD_BACKGROUND};
            padding: 22px;
            border-radius: 22px;
            border: 1px solid rgba(15, 23, 42, 0.08);
            min-height: 180px;
        }}
        .feature-title {{ font-size: 1.05rem; font-weight: 700; margin-bottom: 0.5rem; color: {TEXT}; }}
        .feature-copy {{ color: {MUTED}; line-height: 1.7; margin: 0; }}
        .product-card {{
            background: {CARD_BACKGROUND};
            border-radius: 20px;
            padding: 22px;
            border: 1px solid rgba(15, 23, 42, 0.06);
            margin-bottom: 18px;
        }}
        .product-title {{ margin: 0 0 8px 0; color: {TEXT}; font-size: 1.15rem; font-weight: 700; }}
        .product-meta {{ color: {ACCENT}; margin-bottom: 12px; font-size: 0.95rem; letter-spacing: 0.01em; }}
        .product-desc {{ color: {MUTED}; line-height: 1.7; margin: 0.35rem 0; font-size: 0.95rem; }}
        .section-header {{ color: {TEXT}; margin-bottom: 14px; }}
        .step-pill {{ display: inline-flex; align-items: center; padding: 0.65rem 1rem; border-radius: 999px; background: rgba(79, 143, 143, 0.12); color: {TEXT}; font-size: 0.95rem; margin-right: 10px; margin-bottom: 14px; }}
        .step-pill.active {{ background: {PRIMARY}; color: #ffffff; }}
        .disclaimer-card {{ background: rgba(47, 108, 114, 0.08); border-radius: 18px; padding: 20px; color: {TEXT}; border: 1px solid rgba(47, 108, 114, 0.14); }}
        .metric-card {{ background: rgba(255,255,255,0.95); border-radius: 18px; padding: 18px; border: 1px solid rgba(15, 23, 42, 0.08); min-height: 120px; }}
        .metric-value {{ font-size: 2rem; font-weight: 700; margin: 0; color: {TEXT}; }}
        .metric-label {{ margin: 0; color: {MUTED}; font-size: 0.95rem; }}
        .stButton > button, .stFormSubmitButton > button {{ background-color: {PRIMARY} !important; color: #ffffff !important; border: none !important; padding: 0.8rem 1.5rem !important; border-radius: 999px !important; box-shadow: 0 10px 30px rgba(47, 108, 114, 0.18) !important; }}
        .stButton > button:hover, .stFormSubmitButton > button:hover {{ background-color: {PRIMARY_DARK} !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div style="height: 16px"></div>', unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE & DATABASE HELPERS
# ==========================================
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = pd.DataFrame()
if 'history' not in st.session_state:
    st.session_state.history = []
if 'selected_products' not in st.session_state:
    st.session_state.selected_products = []
if 'selected_categories' not in st.session_state:
    st.session_state.selected_categories = []
if 'results_page_key' not in st.session_state:
    st.session_state.results_page_key = ''

DB_PATH = os.path.join(os.path.dirname(__file__), 'skincare.db')

@st.cache_resource
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

@st.cache_data
def fetch_data(query, params=()):
    conn = get_connection()
    return pd.read_sql_query(query, conn, params=params)

@st.cache_data
def get_counts():
    conn = get_connection()
    product_count = pd.read_sql_query('SELECT COUNT(*) AS total FROM product', conn).iloc[0, 0]
    category_count = pd.read_sql_query('SELECT COUNT(*) AS total FROM category', conn).iloc[0, 0]
    skin_type_count = pd.read_sql_query('SELECT COUNT(*) AS total FROM skin_type', conn).iloc[0, 0]
    skin_issue_count = pd.read_sql_query('SELECT COUNT(*) AS total FROM skin_issue', conn).iloc[0, 0]
    return {
        'products': int(product_count),
        'categories': int(category_count),
        'types': int(skin_type_count),
        'issues': int(skin_issue_count),
    }


def update_history():
    now = datetime.now()
    st.session_state.history = [entry for entry in st.session_state.history
                                if now - datetime.fromisoformat(entry['timestamp']) < timedelta(hours=24)]


def add_history_entry(skin_type, skin_issue, count):
    update_history()
    entry = {
        'timestamp': datetime.now().isoformat(),
        'skin_type': skin_type,
        'skin_issue': skin_issue,
        'count': int(count),
    }
    st.session_state.history.insert(0, entry)
    update_history()


def generate_pdf(user_name, skin_type, skin_issue, results):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    buffer = io.BytesIO()
    page = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    page.setFont('Helvetica-Bold', 22)
    page.setFillColorRGB(0.18, 0.35, 0.36)
    page.drawString(50, height - 60, 'Skinalyze Skincare Brief')
    page.setStrokeColorRGB(0.18, 0.35, 0.36)
    page.setLineWidth(2)
    page.line(50, height - 70, width - 50, height - 70)

    page.setFont('Helvetica', 10)
    page.setFillColorRGB(0.15, 0.2, 0.28)
    page.drawString(50, height - 95, f'Date generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    page.drawString(50, height - 110, f'Profile name: {user_name}')
    page.drawString(50, height - 125, f'Skin type: {skin_type}')
    page.drawString(50, height - 140, f'Primary concern: {skin_issue}')

    page.setFont('Helvetica-Bold', 14)
    page.drawString(50, height - 170, 'Recommended products')
    y = height - 190

    if results.empty:
        page.setFont('Helvetica', 11)
        page.drawString(50, y, 'No products selected for export.')
    else:
        for _, row in results.iterrows():
            if y < 90:
                page.showPage()
                y = height - 50

            page.setFont('Helvetica-Bold', 11)
            page.drawString(50, y, row['product_name'])
            y -= 14

            page.setFont('Helvetica', 9)
            brand_text = f"Brand: {row['brand']}" if pd.notna(row.get('brand')) else 'Brand: Standard formula'
            page.drawString(56, y, brand_text)
            y -= 12
            page.drawString(56, y, f"Category: {row['category_name']}")
            y -= 12
            ingredients = row['active_ingredients'] if pd.notna(row['active_ingredients']) else 'Not listed'
            page.drawString(56, y, f"Key ingredients: {ingredients}")
            y -= 12
            description = row['description'] if pd.notna(row['description']) else 'Description unavailable.'
            if len(description) > 90:
                description = description[:90].rstrip() + '...'
            page.drawString(56, y, f"{description}")
            y -= 18

    page.showPage()
    page.save()
    buffer.seek(0)
    return buffer.getvalue()


# ==========================================
# 3. NAVIGATION
# ==========================================
def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div style='padding: 24px 0 14px 0;'>
                <div style='font-size: 1.35rem; font-weight: 800; color: #0f172a; margin-bottom: 6px;'>Skinalyze</div>
                <div style='color: #475569; font-size: 0.95rem; line-height: 1.6;'>A cleaner, smarter way to build your skincare routine.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button('🏠 Home', use_container_width=True):
            st.session_state.view = 'home'
            st.experimental_rerun()
        if st.button('🧴 Skin Assessment', use_container_width=True):
            st.session_state.view = 'assessment'
            st.experimental_rerun()
        if st.button('✨ Results', use_container_width=True):
            st.session_state.view = 'results'
            st.experimental_rerun()
        if st.button('🕒 Recent Recommendations', use_container_width=True):
            st.session_state.view = 'history'
            st.experimental_rerun()
        if st.button('📚 Skincare Guide', use_container_width=True):
            st.session_state.view = 'guide'
            st.experimental_rerun()
        if st.button('ℹ️ About', use_container_width=True):
            st.session_state.view = 'about'
            st.experimental_rerun()

        st.markdown('---')
        stats = get_counts()
        st.markdown(
            f"""
            <div style='display:flex; gap: 12px; flex-wrap: wrap;'>
                <div style='background: rgba(47, 108, 114, 0.08); border-radius: 14px; padding: 14px; min-width: 100px;'>
                    <div style='font-weight:700; font-size:1.2rem;'>{stats['products']}</div>
                    <div style='color:{MUTED}; font-size:0.9rem;'>Products</div>
                </div>
                <div style='background: rgba(79, 143, 143, 0.08); border-radius: 14px; padding: 14px; min-width: 100px;'>
                    <div style='font-weight:700; font-size:1.2rem;'>{stats['categories']}</div>
                    <div style='color:{MUTED}; font-size:0.9rem;'>Categories</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


render_sidebar()


# ==========================================
# 4. PAGE RENDERERS
# ==========================================
def render_home():
    st.markdown('<div class="hero-panel">', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">A clearer skincare path, tailored to your needs.</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Skinalyze helps you discover routine recommendations with product-focused clarity and a premium, distraction-free layout.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">What this experience provides</div>', unsafe_allow_html=True)
    st.markdown(
        '<ul style="color: #475569; font-size: 1rem; line-height: 1.9; padding-left: 18px; margin: 0;">'
        '<li>Select your skin type and main concern.</li>'
        '<li>See product suggestions grouped by routine category.</li>'
        '<li>Export only the items you want in a polished PDF.</li>'
        '</ul>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Guided assessment</div>', unsafe_allow_html=True)
        st.markdown('<p class="feature-copy">Answer a simple skin profile and get relevant recommendations without guesswork.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Clear results</div>', unsafe_allow_html=True)
        st.markdown('<p class="feature-copy">View products by category with ingredient highlights and explanation notes.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">Smart export</div>', unsafe_allow_html=True)
        st.markdown('<p class="feature-copy">Select individual items or whole categories before exporting a professional summary.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(
        '<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">'
        '<div><div style="font-size:1.1rem; font-weight:700; margin-bottom:8px;">Start with what matters</div>'
        '<div style="color:#475569; line-height:1.75;">Choose your profile, review the recommended routine, and export only the products that match your needs.</div></div>'
        '<div><button style="background: #2f6c72; color: #ffffff; border:none; border-radius: 999px; padding: 0.85rem 1.4rem; font-weight: 700;">Ready to begin</button></div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="disclaimer-card">', unsafe_allow_html=True)
    st.markdown('<strong>Disclaimer:</strong> Skinalyze delivers general skincare guidance only. It does not replace medical advice. For complex skin conditions, consult a licensed dermatologist.', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button('Start Skin Assessment', use_container_width=False):
        st.session_state.view = 'assessment'
        st.experimental_rerun()


def render_assessment():
    st.markdown('<div class="step-pill active">Step 1 of 3: Profile your skin</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Complete a short assessment to see tailored skincare recommendations.</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 1rem; color: #475569; line-height: 1.75; margin-bottom: 18px;">Use the options below to describe your skin and the issue you want to address first.</div>', unsafe_allow_html=True)

    try:
        skin_types = fetch_data('SELECT * FROM skin_type ORDER BY skin_type_name')
        skin_issues = fetch_data('SELECT * FROM skin_issue ORDER BY issue_name')
    except Exception as err:
        st.error(f'Database error loading profile options. Please ensure skincare.db is available. {err}')
        return

    with st.form('assessment_form'):
        st.text_input('Profile name (optional)', key='profile_name', help='Add a short label so you can recognize this routine later.')

        st.markdown('### Your skin type')
        selected_type = st.selectbox(
            'Select the option that best matches your skin.',
            options=[None] + skin_types['skin_type_id'].tolist(),
            format_func=lambda value: 'Choose skin type' if value is None else skin_types.loc[skin_types['skin_type_id'] == value, 'skin_type_name'].values[0],
            help='This helps match product recommendations to your skin behavior.',
        )

        st.markdown('### Primary concern')
        selected_issue = st.selectbox(
            'Which concern should we prioritize?',
            options=[None] + skin_issues['issue_id'].tolist(),
            format_func=lambda value: 'Choose primary concern' if value is None else skin_issues.loc[skin_issues['issue_id'] == value, 'issue_name'].values[0],
            help='Pick the skin issue you want to address first.',
        )

        st.markdown('<div style="color: #475569; margin-top:12px;">If you are unsure, select the concern that feels most urgent today.</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button('Review recommendations')

        if submitted:
            if selected_type is None or selected_issue is None:
                st.warning('Please choose both your skin type and your main concern to continue.')
                st.stop()

            st.session_state.user_name = st.session_state.profile_name.strip() or 'Guest'
            st.session_state.current_skin_type_name = skin_types.loc[skin_types['skin_type_id'] == selected_type, 'skin_type_name'].values[0]
            st.session_state.current_skin_issue_name = skin_issues.loc[skin_issues['issue_id'] == selected_issue, 'issue_name'].values[0]

            query = '''
                SELECT
                    p.product_id,
                    p.product_name,
                    p.brand,
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
                GROUP BY p.product_id, p.product_name, p.brand, c.category_name, p.description, c.category_id
                ORDER BY c.category_id ASC, p.product_name ASC
            '''
            results = fetch_data(query, (selected_type, selected_issue))
            st.session_state.recommendations = results
            st.session_state.selected_products = results['product_id'].tolist()
            st.session_state.selected_categories = results['category_name'].unique().tolist() if not results.empty else []
            st.session_state.results_page_key = f'{selected_type}-{selected_issue}'
            add_history_entry(st.session_state.current_skin_type_name, st.session_state.current_skin_issue_name, len(results))
            st.session_state.view = 'results'
            st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)


def render_results():
    results = st.session_state.recommendations
    if results.empty:
        st.warning('No recommendations are available yet. Please complete the assessment first.')
        return

    st.markdown('<div class="step-pill active">Step 2 of 3: Review recommendations</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Your personalized product roadmap is ready.</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #475569; margin-bottom: 16px;">Select the products you want to export, then download a professional summary.</div>', unsafe_allow_html=True)
    st.markdown('<div class="disclaimer-card">This website does not own or sponsor any of the brands shown. Product details were sourced from open public datasets and independent sources.</div>', unsafe_allow_html=True)

    expected_key = f"{st.session_state.current_skin_type_name}-{st.session_state.current_skin_issue_name}"
    if st.session_state.results_page_key != expected_key:
        st.session_state.selected_products = results['product_id'].tolist()
        st.session_state.selected_categories = results['category_name'].unique().tolist()
        st.session_state.results_page_key = expected_key

    product_categories = results['category_name'].unique().tolist()
    category_selection = st.multiselect(
        'Show categories',
        options=product_categories,
        default=st.session_state.selected_categories or product_categories,
        help='Filter which product cards are visible.',
    )

    if not category_selection:
        st.warning('Pick at least one category to see recommendations.')
        return

    visible_products = results[results['category_name'].isin(category_selection)]

    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button('Select all products'):
            st.session_state.selected_products = results['product_id'].tolist()
    with col2:
        if st.button('Clear selections'):
            st.session_state.selected_products = []

    selected_ids = set(st.session_state.selected_products)
    for _, row in visible_products.iterrows():
        key = f'product_select_{int(row.product_id)}'
        label = f'{row.product_name} — {row.brand if pd.notna(row.brand) else "Trusted formula"}'
        checked = st.checkbox(label, value=row.product_id in selected_ids, key=key)
        if checked:
            selected_ids.add(row.product_id)
        else:
            selected_ids.discard(row.product_id)

    st.session_state.selected_products = list(selected_ids)
    selected_results = results[results['product_id'].isin(st.session_state.selected_products)]

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">', unsafe_allow_html=True)
    st.markdown(f'<div><div style="font-size:1.1rem; font-weight:700;">{len(selected_results)} selected</div><div style="color:#475569;">Choose which products to include in the export.</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    export_container = st.container()
    if selected_results.empty:
        st.warning('No products are selected. Use the checkboxes above to pick products before exporting.')
    else:
        try:
            pdf_bytes = generate_pdf(
                st.session_state.user_name,
                st.session_state.current_skin_type_name,
                st.session_state.current_skin_issue_name,
                selected_results,
            )
            export_container.download_button(
                label='📥 Export selected products',
                data=pdf_bytes,
                file_name=f'Skinalyze_{st.session_state.user_name}_recommendations.pdf',
                mime='application/pdf',
            )
        except Exception as err:
            st.error(f'Unable to generate export file: {err}')

    for category in category_selection:
        category_products = results[results['category_name'] == category]
        if category_products.empty:
            continue

        st.markdown(f'### {category}')
        for _, row in category_products.iterrows():
            product_selected = row.product_id in st.session_state.selected_products
            ingredient_text = row.active_ingredients if pd.notna(row.active_ingredients) else 'No ingredients listed.'
            brand_text = row.brand if pd.notna(row.brand) else 'Trusted formula'
            description = row.description if pd.notna(row.description) else 'No description available.'

            st.markdown(
                f"""
                <div class="product-card">
                    <div class="product-title">{row.product_name}</div>
                    <div class="product-meta">{brand_text} • {row.category_name}</div>
                    <p class="product-desc"><strong>Key ingredients:</strong> {ingredient_text}</p>
                    <p class="product-desc"><strong>Why this is recommended:</strong> Matched to your skin type and concern.</p>
                    <p class="product-desc">{description}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_history():
    update_history()
    st.markdown('<div class="step-pill active">Recent recommendations</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Your last 24 hours of recommendation activity.</div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.info('No recent recommendations. Complete the skin assessment to generate your first routine.')
        return

    rows = []
    for entry in st.session_state.history:
        when = datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M')
        rows.append({
            'Date': when,
            'Skin type': entry['skin_type'],
            'Concern': entry['skin_issue'],
            'Product count': entry['count'],
        })

    st.table(pd.DataFrame(rows))


def render_guide():
    st.markdown('<div class="step-pill active">Skincare guide</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Understand skin types, concerns, and routine essentials.</div>', unsafe_allow_html=True)

    with st.expander('Skin types explained', expanded=True):
        st.markdown(
            '<div style="color:#475569; line-height:1.8;">'
            '<strong>Oily</strong>: Skin that appears shiny and may feel greasy by midday. Ideal routines focus on lightweight hydration and oil control.<br>'
            '<strong>Dry</strong>: Skin that feels tight, flaky, or uncomfortable. Look for rich, moisture-retaining products.<br>'
            '<strong>Combination</strong>: Oil in the T-zone with drier cheeks. Balance hydration without overloading oily areas.<br>'
            '<strong>Sensitive</strong>: Skin that reacts easily to ingredients. Choose calming, low-irritant formulas.</div>',
            unsafe_allow_html=True,
        )

    with st.expander('Common concerns', expanded=False):
        st.markdown(
            '<div style="color:#475569; line-height:1.8;">'
            '<strong>Acne</strong>: Look for gentle exfoliation and oil-balancing support.<br>'
            '<strong>Dryness</strong>: Prioritize humectants and occlusives for lasting hydration.<br>'
            '<strong>Excess sebum</strong>: Reduce shine with lightweight, non-comedogenic products.<br>'
            '<strong>Redness</strong>: Use soothing, barrier-supporting ingredients.</div>',
            unsafe_allow_html=True,
        )

    with st.expander('Ingredient insights', expanded=False):
        st.markdown(
            '<div style="color:#475569; line-height:1.8;">'
            '<strong>Hyaluronic acid</strong>: Hydrates by drawing moisture into the skin.<br>'
            '<strong>Niacinamide</strong>: Balances oil production and supports barrier strength.<br>'
            '<strong>Vitamin C</strong>: Helps brighten dullness and support a more even skin tone.<br>'
            '<strong>Ceramides</strong>: Restore the skin barrier and lock in moisture.</div>',
            unsafe_allow_html=True,
        )

    with st.expander('Routine tips', expanded=False):
        st.markdown(
            '<div style="color:#475569; line-height:1.8;">'
            '<strong>Cleanse</strong> with a gentle cleanser to remove impurities without stripping skin.<br>'
            '<strong>Treat</strong> with serums and targeted support for your main concern.<br>'
            '<strong>Moisturize</strong> daily to keep the skin barrier healthy.<br>'
            '<strong>Protect</strong> with SPF each morning when exposed to sunlight.</div>',
            unsafe_allow_html=True,
        )


def render_about():
    st.markdown('<div class="step-pill active">About Skinalyze</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Why this system exists and how it works.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(
        '<div style="color:#475569; line-height:1.8;">Skinalyze uses your skin profile to surface practical product recommendations from a curated database. '
        'It applies a rule-based matching process to pair skin types and concerns with suitable products and ingredient profiles.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div style="font-weight:700; margin-bottom:10px;">How recommendations are generated</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="color:#475569; line-height:1.8;">The system finds products that are linked to your chosen skin type and primary concern. '
        'Results are grouped by category so you can review cleansers, moisturizers, serums, and more in an organized way.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div style="font-weight:700; margin-bottom:10px;">Technologies used</div>', unsafe_allow_html=True)
    st.markdown(
        '<ul style="color: #475569; font-size: 1rem; line-height: 1.8; padding-left: 18px; margin: 0;">'
        '<li>Streamlit for interface and navigation.</li>'
        '<li>SQLite for light product and profile data storage.</li>'
        '<li>ReportLab to generate export-ready PDF summaries.</li>'
        '</ul>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="disclaimer-card">', unsafe_allow_html=True)
    st.markdown('<strong>Note:</strong> This service offers general skincare suggestions and is not a substitute for professional medical advice.', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 5. ROUTE PAGES
# ==========================================
if st.session_state.view == 'home':
    render_home()
elif st.session_state.view == 'assessment':
    render_assessment()
elif st.session_state.view == 'results':
    render_results()
elif st.session_state.view == 'history':
    render_history()
elif st.session_state.view == 'guide':
    render_guide()
elif st.session_state.view == 'about':
    render_about()
else:
    render_home()
