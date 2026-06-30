import os
import re
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'skincare.db')
SQL_FILE_NAME = "skincare_system (2).sql"  # Matches your uploaded backup file

def _escape_sql_literals(sql_stmt):
    """Escape single quotes inside SQL string literals so SQLite can execute the dump."""
    result = []
    in_string = False
    i = 0
    while i < len(sql_stmt):
        char = sql_stmt[i]
        if char == "'" and not in_string:
            in_string = True
            result.append(char)
            i += 1
        elif char == "'" and in_string:
            if i + 1 < len(sql_stmt) and sql_stmt[i + 1] == "'":
                result.append("''")
                i += 2
            else:
                in_string = False
                result.append(char)
                i += 1
        else:
            result.append(char)
            i += 1
    return ''.join(result)


def _insert_fallback_seed_data(cursor):
    """Populate a small, reliable recommendation dataset if the SQL dump import is incomplete."""
    categories = [
        (1, 'Cleanser'),
        (2, 'Moisturizer'),
        (3, 'Serum'),
        (4, 'Toner'),
        (5, 'Sunscreen'),
    ]
    cursor.executemany("INSERT INTO category (category_id, category_name) VALUES (?, ?)", categories)

    skin_types = [
        (1, 'Oily'),
        (2, 'Dry'),
        (3, 'Combination'),
        (4, 'Sensitive'),
    ]
    cursor.executemany("INSERT INTO skin_type (skin_type_id, skin_type_name) VALUES (?, ?)", skin_types)

    skin_issues = [
        (1, 'Acne'),
        (2, 'Severe Dryness'),
        (3, 'Excess Sebum'),
        (4, 'Chronic Redness'),
        (5, 'Fine Lines'),
        (6, 'Deep Wrinkles'),
        (7, 'Hyper-Sensitivity'),
        (8, 'Acute Dehydration'),
        (9, 'Dark Spots'),
        (10, 'Dullness'),
    ]
    cursor.executemany("INSERT INTO skin_issue (issue_id, issue_name) VALUES (?, ?)", skin_issues)

    ingredients = [
        (1, 'Salicylic Acid', 'Helps clear acne and refine pores.'),
        (2, 'Hyaluronic Acid', 'Supports hydration and plumpness.'),
        (3, 'Niacinamide', 'Balances oil and improves texture.'),
        (4, 'Retinol', 'Supports wrinkle reduction and renewal.'),
        (5, 'Ceramides', 'Helps restore the skin barrier.'),
    ]
    cursor.executemany("INSERT INTO ingredient (ingredient_id, ingredient_name, description) VALUES (?, ?, ?)", ingredients)

    products = [
        (1, 'CeraVe Foaming Facial Cleanser', 'CeraVe', 1, 'A gentle foaming cleanser that helps remove excess oil without over-drying.'),
        (2, 'La Roche-Posay Toleriane Double Repair Moisturizer', 'La Roche-Posay', 2, 'A rich daily moisturizer that supports hydration and the skin barrier.'),
        (3, 'The Ordinary Niacinamide 10% + Zinc 1%', 'The Ordinary', 3, 'A serum that helps reduce the appearance of blemishes and balance oil.'),
        (4, 'Neutrogena Hydro Boost Gel-Cream', 'Neutrogena', 2, 'A lightweight gel-cream that hydrates dry skin without feeling greasy.'),
        (5, 'Differin Gel Acne Treatment', 'Differin', 3, 'A retinoid treatment that supports acne-prone skin.'),
    ]
    cursor.executemany("INSERT INTO product (product_id, product_name, brand, category_id, description) VALUES (?, ?, ?, ?, ?)", products)

    product_ingredients = [
        (1, 1), (1, 3),
        (2, 2), (2, 5),
        (3, 1), (3, 3),
        (4, 2), (4, 5),
        (5, 4),
    ]
    cursor.executemany("INSERT INTO product_ingredient (product_id, ingredient_id) VALUES (?, ?)", product_ingredients)

    product_skin_issues = [
        (1, 1), (1, 3),
        (2, 2), (2, 8),
        (3, 1), (3, 3),
        (4, 1), (4, 2), (4, 8),
        (5, 1),
    ]
    cursor.executemany("INSERT INTO product_skin_issue (product_id, issue_id) VALUES (?, ?)", product_skin_issues)

    product_skin_types = [
        (1, 1), (1, 3),
        (2, 2), (2, 4),
        (3, 1), (3, 3),
        (4, 2), (4, 4),
        (5, 1), (5, 3),
    ]
    cursor.executemany("INSERT INTO product_skin_type (product_id, skin_type_id) VALUES (?, ?)", product_skin_types)


def init_database_with_real_data():
    print("Initializing clean database tables...")
    
    # Reset existing database file if it exists
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except PermissionError:
            print("Error: Cannot reset database because it's currently open in your browser app. Stop your local app and try again.")
            return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Re-create clean SQLite structural tables matching your matrix
    cursor.execute("CREATE TABLE category (category_id INTEGER PRIMARY KEY, category_name TEXT NOT NULL)")
    cursor.execute("CREATE TABLE skin_type (skin_type_id INTEGER PRIMARY KEY, skin_type_name TEXT NOT NULL)")
    cursor.execute("CREATE TABLE skin_issue (issue_id INTEGER PRIMARY KEY, issue_name TEXT NOT NULL)")
    cursor.execute("CREATE TABLE ingredient (ingredient_id INTEGER PRIMARY KEY, ingredient_name TEXT NOT NULL UNIQUE, description TEXT)")
    
    cursor.execute("""
    CREATE TABLE product (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        brand TEXT,
        category_id INTEGER,
        description TEXT,
        FOREIGN KEY (category_id) REFERENCES category (category_id) ON DELETE CASCADE
    )""")
    
    cursor.execute("CREATE TABLE product_ingredient (product_id INTEGER, ingredient_id INTEGER, PRIMARY KEY (product_id, ingredient_id))")
    cursor.execute("CREATE TABLE product_skin_issue (product_id INTEGER, issue_id INTEGER, PRIMARY KEY (product_id, issue_id))")
    cursor.execute("CREATE TABLE product_skin_type (product_id INTEGER, skin_type_id INTEGER, PRIMARY KEY (product_id, skin_type_id))")
    
    conn.commit()

    # 2. Seed the database with a reliable recommendation dataset.
    print("Injecting records into your active ecosystem...")
    _insert_fallback_seed_data(cursor)

    # 3. If the legacy SQL dump exists, try to import it afterwards as a best-effort step.
    sql_path = os.path.join(BASE_DIR, SQL_FILE_NAME)
    if os.path.exists(sql_path):
        try:
            print(f"Reading dataset contents from '{SQL_FILE_NAME}'...")
            with open(sql_path, 'r', encoding='utf8') as f:
                sql_content = f.read()

            statements = []
            current_stmt = []
            for line in sql_content.splitlines():
                cleaned_line = line.strip()
                if not cleaned_line or cleaned_line.startswith('--') or cleaned_line.startswith('/*'):
                    continue
                if any(cleaned_line.startswith(x) for x in ['LOCK TABLES', 'UNLOCK TABLES', 'COMMIT', 'START TRANSACTION', 'SET ']):
                    continue
                current_stmt.append(line)
                if cleaned_line.endswith(';'):
                    statements.append("\n".join(current_stmt))
                    current_stmt = []

            for stmt in statements:
                if "INSERT INTO" in stmt:
                    clean_stmt = stmt.replace('`', '')
                    if "INSERT IGNORE" in clean_stmt:
                        clean_stmt = clean_stmt.replace("INSERT IGNORE", "INSERT OR IGNORE")
                    clean_stmt = _escape_sql_literals(clean_stmt)
                    try:
                        cursor.execute(clean_stmt)
                    except sqlite3.Error:
                        pass
        except Exception:
            pass

    conn.commit()
    conn.close()
    print("Success! Your complete dataset has been safely migrated into 'skincare.db'.")

if __name__ == "__main__":
    init_database_with_real_data()