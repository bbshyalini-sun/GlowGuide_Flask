import os
import re
import pandas as pd
import mysql.connector

# ==========================================
# 1. DATABASE CONNECTION SETUP
# ==========================================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Default password for XAMPP is empty
    'database': 'skincare_system',
    'charset': 'utf8mb4'
}

print("Attempting to connect to the skincare_system database...")
try:
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor()
    print("Successfully connected to MySQL Database!\n")
except mysql.connector.Error as err:
    print(f"Database Connection Error: {err}")
    print("Make sure XAMPP (Apache and MySQL) is turned ON and the database 'skincare_system' exists.")
    exit(1)

# ==========================================
# 2. CATEGORY, ISSUE, AND TYPE MAPPING LOGIC
# ==========================================
CATEGORY_MAP = {
    'moisturiser': 2, 'moisturizer': 2, 'tinted moisturizers': 2, 'spray moisturizer': 2, 'cream': 2,
    'cleanser': 1, 'face wash': 1, 'gel cleanser': 1, 'foam cleanser': 1,
    'serum': 3, 'essence': 3, 'treatment': 3, 'ampoule': 3,
    'toner': 4, 'toners & astringents': 4, 'liquid exfoliant': 4,
    'sunscreen': 5, 'sun care': 5, 'sun protection': 5, 'sunscreen milk': 5
}

ISSUE_KEYWORDS = {
    1: ['acne', 'salicylic', 'benzoyl', 'blemish', 'clear', 'pimple', 'blackhead', 'pore'],
    2: ['dry', 'dryness', 'flaking', 'nourishing', 'rich cream', 'shea butter', 'oil'],
    3: ['oil control', 'sebum', 'matte', 'mat', 'shiny', 'clay', 'witch hazel'],
    4: ['redness', 'calm', 'soothe', 'cica', 'centella', 'inflammation', 'heartleaf'],
    5: ['fine lines', 'peptide', 'aging', 'youthful', 'collagen', 'coenzyme'],
    6: ['wrinkle', 'retinol', 'firming', 'renewing', 'bakuchiol'],
    7: ['sensitive', 'reactive', 'hypoallergenic', 'toleriane', 'soothing', 'allantoin'],
    8: ['dehydrated', 'dehydration', 'hyaluronic', 'hydration', 'thirst', 'panthenol'],
    9: ['dark spot', 'arbutin', 'brightening', 'pigment', 'fade', 'niacinamide', 'licorice'],
    10: ['dull', 'vitamin c', 'glow', 'radiance', 'transparent', 'ascorbic', 'ferment']
}

TYPE_KEYWORDS = {
    1: ['oily', 'matte', 'sebum', 'gel', 'bha', 'salicylic', 'foam'],
    2: ['dry', 'cream', 'rich', 'balm', 'intense', 'butter', 'hyaluronic', 'moisturising'],
    3: ['combination', 'all skin types', 'balanced', 'daily lotion', 'fluid'],
    4: ['sensitive', 'gentle', 'unscented', 'fragrance-free', 'calming', 'cica', 'allantoin']
}

# ==========================================
# 3. CORE DATA PROCESSING PIPELINE FUNCTION
# ==========================================
def process_and_ingest_file(file_path):
    if not os.path.exists(file_path):
        print(f"Warning: File target missing, skipping: {file_path}")
        return

    print(f"Reading and analyzing dataset rows from: {file_path}...")
    df = pd.read_csv(file_path)
    
    # DYNAMICALLY DETECT COLUMNS TO PREVENT KEYERROR EXCEPTIONS
    category_col = None
    for col in ['product_type', 'category']:
        if col in df.columns:
            category_col = col
            break
            
    ingredients_col = None
    for col in ['clean_ingreds', 'ingredients']:
        if col in df.columns:
            ingredients_col = col
            break

    # If file headers are completely unexpected, log it and skip safely
    if not category_col or not ingredients_col:
        print(f"Error: Could not identify required columns in {file_path}. Skipping file.")
        return

    inserted_count = 0
    skipped_count = 0

    for _, row in df.iterrows():
        if pd.isna(row['product_name']):
            continue
            
        product_name = str(row['product_name']).strip()
        raw_category = str(row[category_col]).lower()
        
        category_id = None
        for key, cat_id in CATEGORY_MAP.items():
            if key in raw_category:
                category_id = cat_id
                break
        
        if not category_id:
            continue
            
        # Safely grab brand if it exists as an available column, fallback to placeholder
        brand = str(row['brand']).strip() if 'brand' in df.columns and not pd.isna(row['brand']) else "Retail Skincare Brand"
        description = f"Imported automated formulation. Source registry: {file_path}"
        
        raw_ingredients_text = str(row[ingredients_col]).lower()

        # Deduplication Safeguard (avoids polluting table if rerun)
        cursor.execute("SELECT product_id FROM product WHERE product_name = %s", (product_name,))
        if cursor.fetchone():
            skipped_count += 1
            continue

        # Insert item into core 'product' table
        cursor.execute(
            "INSERT INTO product (product_name, brand, category_id, description) VALUES (%s, %s, %s, %s)",
            (product_name, brand, category_id, description)
        )
        product_id = cursor.lastrowid
        inserted_count += 1

        # A. AUTO-MAPPING ACTIVE INGREDIENTS
        cursor.execute("SELECT ingredient_id, ingredient_name FROM ingredient")
        system_ingredients = cursor.fetchall()
        for ing_id, ing_name in system_ingredients:
            base_word = re.split(r'\s|\(', ing_name.lower())[0]
            if base_word in raw_ingredients_text or base_word in product_name.lower():
                cursor.execute(
                    "INSERT IGNORE INTO product_ingredient (product_id, ingredient_id) VALUES (%s, %s)",
                    (product_id, ing_id)
                )

        # B. AUTO-GENERATING RECOMMENDATION MATRIX LOGIC RULES
        search_blob = f"{product_name} {raw_ingredients_text}".lower()
        
        matched_an_issue = False
        for issue_id, keywords in ISSUE_KEYWORDS.items():
            if any(kw in search_blob for kw in keywords):
                cursor.execute(
                    "INSERT IGNORE INTO product_skin_issue (product_id, issue_id) VALUES (%s, %s)",
                    (product_id, issue_id)
                )
                matched_an_issue = True
                
        matched_a_type = False
        for type_id, keywords in TYPE_KEYWORDS.items():
            if any(kw in search_blob for kw in keywords):
                cursor.execute(
                    "INSERT IGNORE INTO product_skin_type (product_id, skin_type_id) VALUES (%s, %s)",
                    (product_id, type_id)
                )
                matched_a_type = True

        if not matched_a_type:
            cursor.execute("INSERT IGNORE INTO product_skin_type (product_id, skin_type_id) VALUES (%s, 3)", (product_id,))
        if not matched_an_issue:
            fallback_id = 10 if category_id == 5 else 8
            cursor.execute("INSERT IGNORE INTO product_skin_issue (product_id, issue_id) VALUES (%s, %s)", (product_id, fallback_id))

    db.commit()
    print(f"--> File Complete. Successfully added {inserted_count} new products. (Skipped {skipped_count} duplicates/unmapped categories).\n")

# ==========================================
# 4. RUN INGESTION SEQUENCES
# ==========================================
# Run all three files through the unified processing function
process_and_ingest_file('skincare_products_clean.csv')
process_and_ingest_file('skincare_products.csv')
process_and_ingest_file('1-200.csv')

# Clean context closure
cursor.close()
db.close()
print("All tasks completed successfully. Your database is now fully populated!")