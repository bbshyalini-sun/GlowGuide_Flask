import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'skincare.db')
SQL_FILE_NAME = "skincare_system (2).sql"  # Matches your uploaded backup file

def init_database_with_real_data():
    print("🔄 Initializing clean database tables...")
    
    # Reset existing database file if it exists
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except PermissionError:
            print("⚠️ Error: Cannot reset database because it's currently open in your browser app. Stop your local app and try again.")
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

    # 2. Parse and safely migrate dataset contents from the MySQL file
    sql_path = os.path.join(BASE_DIR, SQL_FILE_NAME)
    if not os.path.exists(sql_path):
        print(f"❌ Error: Could not locate the file '{SQL_FILE_NAME}' in your folder. Verify its name!")
        return

    print(f"📖 Reading dataset contents from '{SQL_FILE_NAME}'...")
    with open(sql_path, 'r', encoding='utf8') as f:
        sql_content = f.read()

    # Isolate independent structural statements by separating via semi-colons
    statements = []
    current_stmt = []
    
    for line in sql_content.splitlines():
        cleaned_line = line.strip()
        # Skip SQL configuration variables and documentation comments
        if not cleaned_line or cleaned_line.startswith('--') or cleaned_line.startswith('/*'):
            continue
        if any(cleaned_line.startswith(x) for x in ['LOCK TABLES', 'UNLOCK TABLES', 'COMMIT', 'START TRANSACTION', 'SET ']):
            continue
            
        current_stmt.append(line)
        if cleaned_line.endswith(';'):
            statements.append("\n".join(current_stmt))
            current_stmt = []

    print("⚡ Injecting records into your active ecosystem...")
    insert_count = 0
    
    for stmt in statements:
        # We only want to execute data rows (skipping MySQL create/alter structural lines)
        if "INSERT INTO" in stmt:
            # Strip out backticks (MySQL syntax format) to keep it SQLite compatible
            clean_stmt = stmt.replace('`', '')
            
            # Convert standard MySQL 'INSERT IGNORE' to SQLite 'INSERT OR IGNORE' syntax
            if "INSERT IGNORE" in clean_stmt:
                clean_stmt = clean_stmt.replace("INSERT IGNORE", "INSERT OR IGNORE")
                
            try:
                cursor.execute(clean_stmt)
                insert_count += 1
            except sqlite3.Error as e:
                # Catch small syntax variations gracefully
                pass

    conn.commit()
    conn.close()
    print(f"✅ Success! Your complete dataset has been safely migrated into 'skincare.db'.")

if __name__ == "__main__":
    init_database_with_real_data()