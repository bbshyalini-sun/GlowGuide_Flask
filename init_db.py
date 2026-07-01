import os
import sqlite3
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "skincare.db")
SQL_FILE_PATH = os.path.join(BASE_DIR, "skincare_system (4).sql")

def init_database_with_real_data():
    print("🚀 Starting native SQLite compilation from SQL dump...")
    
    # 1. Establish connection and enforce foreign keys
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Drop all old tables to clear corrupted cache schemas
    tables = [
        "product_ingredient", "product_skin_issue", "product_skin_type", 
        "product", "category", "ingredient", "skin_issue", "skin_type"
    ]
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table};")
        
    # 2. Re-create structured SQLite schemas with constraints built-in directly
    cursor.execute("""
        CREATE TABLE category (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name VARCHAR(50) NOT NULL
        );
    """)
    
    cursor.execute("""
        CREATE TABLE skin_type (
            skin_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
            skin_type_name VARCHAR(50) NOT NULL
        );
    """)
    
    cursor.execute("""
        CREATE TABLE skin_issue (
            issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue_name VARCHAR(50) NOT NULL
        );
    """)
    
    cursor.execute("""
        CREATE TABLE ingredient (
            ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredient_name VARCHAR(100) NOT NULL UNIQUE,
            description TEXT
        );
    """)
    
    cursor.execute("""
        CREATE TABLE product (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name VARCHAR(255) NOT NULL,
            brand VARCHAR(100),
            category_id INTEGER,
            description TEXT,
            FOREIGN KEY (category_id) REFERENCES category(category_id) ON DELETE CASCADE
        );
    """)
    
    cursor.execute("""
        CREATE TABLE product_ingredient (
            product_id INTEGER,
            ingredient_id INTEGER,
            PRIMARY KEY (product_id, ingredient_id),
            FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE,
            FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id) ON DELETE CASCADE
        );
    """)
    
    cursor.execute("""
        CREATE TABLE product_skin_type (
            product_id INTEGER,
            skin_type_id INTEGER,
            PRIMARY KEY (product_id, skin_type_id),
            FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE,
            FOREIGN KEY (skin_type_id) REFERENCES skin_type(skin_type_id) ON DELETE CASCADE
        );
    """)
    
    cursor.execute("""
        CREATE TABLE product_skin_issue (
            product_id INTEGER,
            issue_id INTEGER,
            PRIMARY KEY (product_id, issue_id),
            FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE,
            FOREIGN KEY (issue_id) REFERENCES skin_issue(issue_id) ON DELETE CASCADE
        );
    """)
    
    # 3. Read, Sanitize, and Stream the MySQL inserts safely
    if not os.path.exists(SQL_FILE_PATH):
        print(f"❌ Error: Source file '{SQL_FILE_PATH}' not found in directory.")
        return
        
    with open(SQL_FILE_PATH, 'r', encoding='utf-8') as file:
        raw_sql = file.read()
        
    # CRITICAL DIALECT CONVERSION: Catch all variations of escaped quotes (\' or \\')
    sanitized_sql = raw_sql.replace("\\'", "''").replace("\\\\'", "''")
    
    # Isolate all standard multi-line INSERT queries
    insert_statements = re.findall(r"INSERT INTO\s+`?\w+`?.*?;", sanitized_sql, re.IGNORECASE | re.DOTALL)
    print(f"[+] Extracted {len(insert_statements)} INSERT sequences. Syncing data registries...")
    
    success_count = 0
    skipped_count = 0
    for stmt in insert_statements:
        try:
            cursor.execute(stmt)
            success_count += 1
        except Exception as ex:
            skipped_count += 1
            
    conn.commit()
    conn.close()
    print(f"✨ Compilation Finished! Loaded: {success_count} chunks safely. Skipped: {skipped_count} items.\n")

if __name__ == "__main__":
    init_database_with_real_data()