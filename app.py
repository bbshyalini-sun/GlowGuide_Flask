import os
import mysql.connector
from flask import Flask, render_template, request, g, abort, session, jsonify, redirect, url_for
from datetime import datetime

app = Flask(__name__)
# Temporary secret key for session storage (change in production)
app.secret_key = 'dev-secret-change-me'

# MySQL connection config (matches ingest_data.py defaults)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'skincare_system',
    'charset': 'utf8mb4'
}


def get_db():
    if 'db' not in g:
        conn = mysql.connector.connect(**DB_CONFIG)
        g.db = conn
    return g.db


@app.teardown_appcontext
def close_db(error=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT skin_type_id, skin_type_name FROM skin_type")
    skin_types = cursor.fetchall() or []

    cursor.execute("SELECT issue_id, issue_name FROM skin_issue ORDER BY issue_name")
    skin_issues = cursor.fetchall() or []

    cursor.close()

    # Fallback defaults if DB empty (helps when DB hasn't been initialized)
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

    return render_template('index.html', skin_types=skin_types, skin_issues=skin_issues)

@app.route('/assessment')
def assessment():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT skin_type_id, skin_type_name FROM skin_type")
    skin_types = cursor.fetchall() or []

    cursor.execute("SELECT issue_id, issue_name FROM skin_issue ORDER BY issue_name")
    skin_issues = cursor.fetchall() or []

    cursor.close()
    # Fallback defaults when DB not initialized
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

    # pass any existing temporary user name from session to pre-fill the form
    return render_template('assessment.html', skin_types=skin_types, skin_issues=skin_issues, user_name=session.get('user_name'))

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    
    skin_type_id = request.form.get('skin_type')
    issue_id = request.form.get('skin_issue')

    # store temporary user name in session (if provided)
    user_name = (request.form.get('user_name') or '').strip()
    # Require a non-empty name
    if not user_name:
        # fetch options to re-render assessment with an error
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT skin_type_id, skin_type_name FROM skin_type")
        skin_types = cursor.fetchall() or []
        cursor.execute("SELECT issue_id, issue_name FROM skin_issue ORDER BY issue_name")
        skin_issues = cursor.fetchall() or []
        cursor.close()


        # fallback defaults if DB empty
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
        return render_template('assessment.html', skin_types=skin_types, skin_issues=skin_issues, user_name=user_name, error='Please enter your name to continue')
    else:
        session['user_name'] = user_name

    db = get_db()
    # cast to integers when possible
    try:
        skin_type_id = int(skin_type_id) if skin_type_id is not None else None
    except ValueError:
        skin_type_id = None
    try:
        issue_id = int(issue_id) if issue_id is not None else None
    except ValueError:
        issue_id = None

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT skin_type_name FROM skin_type WHERE skin_type_id = %s", (skin_type_id,))
    selected_type = cursor.fetchone()

    cursor.execute("SELECT issue_name FROM skin_issue WHERE issue_id = %s", (issue_id,))
    selected_issue = cursor.fetchone()

    # Dynamic recommendation engine JOIN query execution
    
    #This is where the recommendation logic is applied to organize the products into categories and limit the number of products displayed per category.
    # Organize linear database query records into categorized dictionary buckets
    # limit displayed products to at most 5 per category
    query = """
        SELECT 
            p.product_name, c.category_name,
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

    recommendations = {}
    for prod in raw_products:
        prod_dict = prod.copy() if isinstance(prod, dict) else dict(prod)

        cat = prod_dict.get('category_name', 'Uncategorized')
        if cat not in recommendations:
            recommendations[cat] = []
        recommendations[cat].append(prod_dict)

    for category, products in recommendations.items():
        recommendations[category] = products[:5]

    # record this run in temporary session-backed history (keep newest first, capped)
    history = session.get('history', [])
    entry = {
        'id': int(datetime.utcnow().timestamp() * 1000),
        'user_name': session.get('user_name'),
        'skin_type_id': skin_type_id,
        'issue_id': issue_id,
        'skin_type': selected_type['skin_type_name'] if selected_type else '',
        'issue': selected_issue['issue_name'] if selected_issue else '',
        'date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    }
    history.insert(0, entry)
    # keep only last 50 entries to avoid session bloat
    session['history'] = history[:50]

    return render_template(
        'result.html', 
        recommendations=recommendations,
        skin_type=selected_type['skin_type_name'] if selected_type else 'Selected Skin Type',
        skin_issue=selected_issue['issue_name'] if selected_issue else 'Selected Concern'
        , user_name=session.get('user_name')
    )


@app.route('/end_session', methods=['POST'])
def end_session():
    # Clear only the temporary user name from session
    session.pop('user_name', None)
    return jsonify({'status': 'cleared'})


@app.route('/history/clear', methods=['POST'])
def clear_history():
    session.pop('history', None)
    return redirect(url_for('history'))


@app.route('/history')
def history():
    hist = session.get('history', [])
    return render_template('history.html', history=hist)


@app.route('/history/view/<int:entry_id>')
def history_view(entry_id):
    hist = session.get('history', [])
    entry = next((h for h in hist if h['id'] == entry_id), None)
    if not entry:
        abort(404)

    # Re-run recommendation query for the saved combo without altering history
    skin_type_id = entry.get('skin_type_id')
    issue_id = entry.get('issue_id')

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT skin_type_name FROM skin_type WHERE skin_type_id = %s", (skin_type_id,))
    selected_type = cursor.fetchone()

    cursor.execute("SELECT issue_name FROM skin_issue WHERE issue_id = %s", (issue_id,))
    selected_issue = cursor.fetchone()

    # Dynamic recommendation engine JOIN query execution
    query = """
        SELECT 
            p.product_name, c.category_name,
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

    # This is gotten from the previous recommendation logic, but we don't want to store this in history again
    recommendations = {}
    for prod in raw_products:
        prod_dict = prod.copy() if isinstance(prod, dict) else dict(prod)
        # There is no brand in the system
        cat = prod_dict.get('category_name', 'Uncategorized')
        if cat not in recommendations:
            recommendations[cat] = []
        recommendations[cat].append(prod_dict)

    for category, products in recommendations.items():
        recommendations[category] = products[:5]

    return render_template('result.html', recommendations=recommendations, skin_type=selected_type['skin_type_name'] if selected_type else entry.get('skin_type'), skin_issue=selected_issue['issue_name'] if selected_issue else entry.get('issue'), user_name=entry.get('user_name'))

if __name__ == '__main__':
    app.run(debug=True)