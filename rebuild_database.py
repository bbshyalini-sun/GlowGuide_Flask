import sqlite3
import os

DB_NAME = "skincare.db"

def clean_string(value, fallback="Not Specified"):
    """Validates and cleans input data to prevent unexpected NULL spaces."""
    if value is None:
        return fallback
    cleaned = str(value).strip()
    return cleaned if cleaned else fallback

def rebuild_database():
    # Remove existing database file to ensure a completely clean slate
    if os.path.exists(DB_NAME):
        try:
            os.remove(DB_NAME)
            print(f"[*] Found existing '{DB_NAME}'. Deleted for fresh rebuild.")
        except Exception as e:
            print(f"[!] Error deleting existing database: {e}")
            return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    print("[*] Creating table schemas with application-aligned constraints...")
    try:
        # Lookup Tables
        cursor.execute("CREATE TABLE category (category_id INTEGER PRIMARY KEY AUTOINCREMENT, category_name TEXT NOT NULL UNIQUE);")
        cursor.execute("CREATE TABLE skin_type (skin_type_id INTEGER PRIMARY KEY AUTOINCREMENT, skin_type_name TEXT NOT NULL UNIQUE);")
        cursor.execute("CREATE TABLE skin_issue (issue_id INTEGER PRIMARY KEY AUTOINCREMENT, issue_name TEXT NOT NULL UNIQUE);")
        
        # NEW: Ingredient Lookup Table (Required by your app)
        cursor.execute("CREATE TABLE ingredient (ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT, ingredient_name TEXT NOT NULL UNIQUE);")

        # Core Product Table (Ingredients column removed since it is now relational)
        cursor.execute("""
            CREATE TABLE product (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                brand TEXT NOT NULL DEFAULT 'Not Specified',
                description TEXT NOT NULL DEFAULT 'Not Specified',
                category_id INTEGER NOT NULL,
                FOREIGN KEY (category_id) REFERENCES category(category_id) ON DELETE CASCADE
            );
        """)

        # Many-to-Many Bridge Tables
        cursor.execute("""
            CREATE TABLE product_skin_type (
                product_id INTEGER, skin_type_id INTEGER,
                PRIMARY KEY (product_id, skin_type_id),
                FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE,
                FOREIGN KEY (skin_type_id) REFERENCES skin_type(skin_type_id) ON DELETE CASCADE
            );
        """)
        cursor.execute("""
            CREATE TABLE product_skin_issue (
                product_id INTEGER, issue_id INTEGER,
                PRIMARY KEY (product_id, issue_id),
                FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE,
                FOREIGN KEY (issue_id) REFERENCES skin_issue(issue_id) ON DELETE CASCADE
            );
        """)
        
        # NEW: Product-Ingredient Bridge Table (Required by your app)
        cursor.execute("""
            CREATE TABLE product_ingredient (
                product_id INTEGER, ingredient_id INTEGER,
                PRIMARY KEY (product_id, ingredient_id),
                FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE,
                FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id) ON DELETE CASCADE
            );
        """)
        
        conn.commit()
        print("[+] Schema successfully initialized.")

    except sqlite3.Error as e:
        print(f"[!] Critical Error during schema initialization: {e}")
        conn.close()
        return

    print("[*] Injecting core lookup configurations...")
    categories = ["Serums", "Toners", "Cleansers", "Moisturisers"]
    cursor.executemany("INSERT INTO category (category_name) VALUES (?);", [(c,) for c in categories])
    
    skin_types = ["Normal", "Oily", "Dry", "Sensitive"]
    cursor.executemany("INSERT INTO skin_type (skin_type_name) VALUES (?);", [(st,) for st in skin_types])

    skin_issues = ["Acne", "Aging", "Hyperpigmentation", "Dehydration", "Dullness"]
    cursor.executemany("INSERT INTO skin_issue (issue_name) VALUES (?);", [(si,) for si in skin_issues])
    conn.commit()

    # Base Ingredients Pool to dynamically allocate to products
    base_ingredients = ["Salicylic Acid", "Hyaluronic Acid", "Niacinamide", "Glycerin", "Retinol", "Vitamin C", "Ceramides", "Aqua"]
    cursor.executemany("INSERT OR IGNORE INTO ingredient (ingredient_name) VALUES (?);", [(ing,) for ing in base_ingredients])
    conn.commit()

    # Map lookups dynamically
    category_map = {row[1]: row[0] for row in cursor.execute("SELECT category_id, category_name FROM category").fetchall()}
    type_map = {row[1]: row[0] for row in cursor.execute("SELECT skin_type_id, skin_type_name FROM skin_type").fetchall()}
    issue_map = {row[1]: row[0] for row in cursor.execute("SELECT issue_id, issue_name FROM skin_issue").fetchall()}
    ingredient_map = {row[1]: row[0] for row in cursor.execute("SELECT ingredient_id, ingredient_name FROM ingredient").fetchall()}

    print("[*] Generating 50 production-grade entries mapped to independent tables...")
    brands = ["GlowTech", "DermPure", "HydraAura", "SkinAesthetic", "BioVerde"]
    
    product_ingredient_relationships = [] # Tracks links for the bridge table

    for i in range(1, 51):
        cat_name = categories[(i - 1) % len(categories)]
        cat_id = category_map[cat_name]
        brand_name = brands[(i - 1) % len(brands)]
        
        # Fallback test cases
        if i == 15:
            p_name, brand_name, desc = "Experimental Complex E15", None, "Beta trial compound."
            prod_ings = ["Aqua"]
        elif i == 35:
            p_name, brand_name, desc = "Minimalist Tonic", "PureEssence", None
            prod_ings = ["Aqua", "Glycerin"]
        else:
            p_name = f"{brand_name} {cat_name[:-1]} Solution v{i}"
            desc = f"A high-potency {cat_name[:-1].lower()} optimized for targeted cellular nourishment."
            # Alternate ingredients systematically
            prod_ings = ["Aqua", base_ingredients[i % len(base_ingredients)], base_ingredients[(i + 1) % len(base_ingredients)]]

        cleaned_p_name = clean_string(p_name, fallback="Unnamed Product")
        cleaned_brand = clean_string(brand_name, fallback="Not Specified")
        cleaned_desc = clean_string(desc, fallback="Not Specified")
        
        cursor.execute("""
            INSERT INTO product (product_name, brand, description, category_id)
            VALUES (?, ?, ?, ?);
        """, (cleaned_p_name, cleaned_brand, cleaned_desc, cat_id))
        
        current_product_id = cursor.lastrowid
        
        # Link mapped ingredients to this product ID
        for ing in prod_ings:
            ing_id = ingredient_map[ing]
            product_ingredient_relationships.append((current_product_id, ing_id))

    # Bulk insert ingredient relationships
    cursor.executemany("INSERT OR IGNORE INTO product_ingredient (product_id, ingredient_id) VALUES (?, ?);", product_ingredient_relationships)
    conn.commit()

    print("[*] Establishing Many-to-Many skin type/issue relations...")
    product_ids = [row[0] for row in cursor.execute("SELECT product_id FROM product").fetchall()]
    
    oily_id, acne_id = type_map["Oily"], issue_map["Acne"]
    bridge_types, bridge_issues = [], []
    
    for idx, pid in enumerate(product_ids):
        if idx < 10:
            bridge_types.append((pid, oily_id))
            bridge_issues.append((pid, acne_id))
        else:
            st_name = skin_types[idx % len(skin_types)]
            si_name = skin_issues[idx % len(skin_issues)]
            if st_name == "Oily" and si_name == "Acne":
                si_name = "Aging"
            bridge_types.append((pid, type_map[st_name]))
            bridge_issues.append((pid, issue_map[si_name]))

    cursor.executemany("INSERT INTO product_skin_type (product_id, skin_type_id) VALUES (?, ?);", bridge_types)
    cursor.executemany("INSERT INTO product_skin_issue (product_id, issue_id) VALUES (?, ?);", bridge_issues)
    conn.commit()
    
    print("\n" + "="*50)
    print("        DATABASE STRUCTURAL VALIDATION REPORT       ")
    print("="*50)
    tables = ['category', 'skin_type', 'skin_issue', 'ingredient', 'product', 'product_skin_type', 'product_skin_issue', 'product_ingredient']
    for table in tables:
        count = cursor.execute(f"SELECT COUNT(*) FROM {table};").fetchone()[0]
        print(f" Table: {table:<20} | Row Count: {count}")
    print("="*50)

    conn.close()
    print("[SUCCESS] Database rebuilt successfully to comply with your Streamlit application!")

if __name__ == "__main__":
    rebuild_database()