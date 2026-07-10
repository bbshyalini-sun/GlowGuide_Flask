import sqlite3
import os

DB_NAME = "skincare.db"

def clean_string(value, fallback="Not Specified"):
    """
    Validates and cleans input data to prevent unexpected NULL spaces.
    If the string is missing, empty, or whitespace-only, it returns the fallback.
    """
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

    # Establish clean connection
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Enable foreign key constraints for integrity
    cursor.execute("PRAGMA foreign_keys = ON;")

    print("[*] Creating table schemas with rigorous constraints...")
    try:
        # 1. Category Lookup Table
        cursor.execute("""
            CREATE TABLE category (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT NOT NULL UNIQUE
            );
        """)

        # 2. Skin Type Lookup Table
        cursor.execute("""
            CREATE TABLE skin_type (
                skin_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
                skin_type_name TEXT NOT NULL UNIQUE
            );
        """)

        # 3. Skin Issue Lookup Table
        cursor.execute("""
            CREATE TABLE skin_issue (
                issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
                issue_name TEXT NOT NULL UNIQUE
            );
        """)

        # 4. Core Product Table
        cursor.execute("""
            CREATE TABLE product (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                brand TEXT NOT NULL DEFAULT 'Not Specified',
                ingredients TEXT NOT NULL DEFAULT 'General Formulation',
                description TEXT NOT NULL DEFAULT 'Not Specified',
                category_id INTEGER NOT NULL,
                FOREIGN KEY (category_id) REFERENCES category(category_id) ON DELETE CASCADE
            );
        """)

        # 5. Many-to-Many Bridge: Product <-> Skin Type
        cursor.execute("""
            CREATE TABLE product_skin_type (
                product_id INTEGER,
                skin_type_id INTEGER,
                PRIMARY KEY (product_id, skin_type_id),
                FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE,
                FOREIGN KEY (skin_type_id) REFERENCES skin_type(skin_type_id) ON DELETE CASCADE
            );
        """)

        # 6. Many-to-Many Bridge: Product <-> Skin Issue
        cursor.execute("""
            CREATE TABLE product_skin_issue (
                product_id INTEGER,
                issue_id INTEGER,
                PRIMARY KEY (product_id, issue_id),
                FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE,
                FOREIGN KEY (issue_id) REFERENCES skin_issue(issue_id) ON DELETE CASCADE
            );
        """)
        
        conn.commit()
        print("[+] Schema successfully initialized.")

    except sqlite3.Error as e:
        print(f"[!] Critical Error during schema initialization: {e}")
        conn.close()
        return

    print("[*] Injecting core lookup configurations...")
    # Standard Categories
    categories = ["Serums", "Toners", "Cleansers", "Moisturisers"]
    cursor.executemany("INSERT INTO category (category_name) VALUES (?);", [(c,) for c in categories])
    
    # Standard Skin Types
    skin_types = ["Normal", "Oily", "Dry", "Sensitive"]
    cursor.executemany("INSERT INTO skin_type (skin_type_name) VALUES (?);", [(st,) for st in skin_types])

    # Standard Skin Issues
    skin_issues = ["Acne", "Aging", "Hyperpigmentation", "Dehydration", "Dullness"]
    cursor.executemany("INSERT INTO skin_issue (issue_name) VALUES (?);", [(si,) for si in skin_issues])
    
    conn.commit()

    # Map lookups dynamically to ensure programmatic precision in relational mappings
    category_map = {row[1]: row[0] for row in cursor.execute("SELECT category_id, category_name FROM category").fetchall()}
    type_map = {row[1]: row[0] for row in cursor.execute("SELECT skin_type_id, skin_type_name FROM skin_type").fetchall()}
    issue_map = {row[1]: row[0] for row in cursor.execute("SELECT issue_id, issue_name FROM skin_issue").fetchall()}

    print("[*] Generating 50 production-grade synthetic skincare entries...")
    
    # Master lists for product definitions to loop over programmatically
    brands = ["GlowTech", "DermPure", "HydraAura", "SkinAesthetic", "BioVerde"]
    
    products_to_inject = []
    
    # Generate exactly 50 products safely distributed
    for i in range(1, 51):
        # Evenly distribute categories across items
        cat_name = categories[(i - 1) % len(categories)]
        cat_id = category_map[cat_name]
        
        brand_name = brands[(i - 1) % len(brands)]
        
        # Intentional test case injections for data cleaning fallbacks (Items 15 & 35)
        if i == 15:
            p_name = "Experimental Complex E15"
            brand_name = None  # Will test the NULL clean handler
            ingredients = " "  # Will test whitespace fallback
            desc = "Beta trial compound."
        elif i == 35:
            p_name = "Minimalist Tonic"
            brand_name = "PureEssence"
            ingredients = "Aqua, Glycerin."
            desc = None  # Will test the NULL clean handler
        else:
            p_name = f"{brand_name} {cat_name[:-1]} Solution v{i}"
            ingredients = f"Active Complex {i}%, Aqua, Phenoxyethanol, Hyaluronic Acid."
            desc = f"A high-potency {cat_name[:-1].lower()} optimized for targeted cellular nourishment."

        # Pass inputs through data validation layers before tuple composition
        cleaned_p_name = clean_string(p_name, fallback="Unnamed Product")
        cleaned_brand = clean_string(brand_name, fallback="Not Specified")
        cleaned_ingredients = clean_string(ingredients, fallback="General Formulation")
        cleaned_desc = clean_string(desc, fallback="Not Specified")
        
        products_to_inject.append((cleaned_p_name, cleaned_brand, cleaned_ingredients, cleaned_desc, cat_id))

    # Bulk insert products safely
    cursor.executemany("""
        INSERT INTO product (product_name, brand, ingredients, description, category_id)
        VALUES (?, ?, ?, ?, ?);
    """, products_to_inject)
    conn.commit()

    print("[*] Establishing complex Many-to-Many relational intersections...")
    
    # Fetch all newly generated product IDs
    product_ids = [row[0] for row in cursor.execute("SELECT product_id FROM product").fetchall()]
    
    # EXPLICIT CONSTRAINT HANDLING: Allocate exactly the first 10 products to the Oily + Acne intersection
    oily_id = type_map["Oily"]
    acne_id = issue_map["Acne"]
    
    bridge_types = []
    bridge_issues = []
    
    for idx, pid in enumerate(product_ids):
        if idx < 10:
            # First 10 items strictly satisfy the Oily + Acne intersection
            bridge_types.append((pid, oily_id))
            bridge_issues.append((pid, acne_id))
        else:
            # Distribute remaining 40 items across various combinations evenly
            # Avoid placing these into Oily + Acne concurrently to protect target intersection metric
            st_name = skin_types[idx % len(skin_types)]
            si_name = skin_issues[idx % len(skin_issues)]
            
            # If the loop lands back on Oily + Acne randomly, offset it safely
            if st_name == "Oily" and si_name == "Acne":
                si_name = "Aging"
                
            bridge_types.append((pid, type_map[st_name]))
            bridge_issues.append((pid, issue_map[si_name]))

    # Batch insert into junction bridge configurations
    cursor.executemany("INSERT INTO product_skin_type (product_id, skin_type_id) VALUES (?, ?);", bridge_types)
    cursor.executemany("INSERT INTO product_skin_issue (product_id, issue_id) VALUES (?, ?);", bridge_issues)
    conn.commit()
    
    print("[+] Relational integrity layers bound successfully.")

    # 3. DUAL-INPUT STRUCTURAL VALIDATION REPORT
    print("\n" + "="*50)
    print("        DATABASE STRUCTURAL VALIDATION REPORT       ")
    print("="*50)
    
    tables = ['category', 'skin_type', 'skin_issue', 'product', 'product_skin_type', 'product_skin_issue']
    for table in tables:
        count = cursor.execute(f"SELECT COUNT(*) FROM {table};").fetchone()[0]
        print(f" Table: {table:<20} | Row Count: {count}")
    
    # Target Intersectional Validation Assert Check
    intersection_check = cursor.execute("""
        SELECT COUNT(*) 
        FROM product_skin_type pst
        JOIN product_skin_issue psi ON pst.product_id = psi.product_id
        WHERE pst.skin_type_id = ? AND psi.issue_id = ?;
    """, (oily_id, acne_id)).fetchone()[0]
    
    print("-"*50)
    print(f" TARGET VERIFICATION -> [Oily + Acne] Intersection: {intersection_check} items")
    print("="*50)

    if intersection_check == 10:
        print("[SUCCESS] Validation constraint checks passed without abnormalities.\n")
    else:
        print("[WARNING] Target verification skew detected. Check logic mappings.\n")

    # Safely close connection context
    conn.close()

if __name__ == "__main__":
    rebuild_database()