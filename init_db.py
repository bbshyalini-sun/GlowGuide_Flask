import os
import re
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "skincare.db")
SQL_PATH = os.path.join(BASE_DIR, "skincare_system (4).sql")

def clean_mysql_for_sqlite(sql_text):
    """Transforms raw MySQL backup text into perfect SQLite compliance."""
    # 1. Convert auto increment syntax safely
    sql_text = re.sub(r'AUTO_INCREMENT', 'AUTOINCREMENT', sql_text, flags=re.IGNORECASE)
    sql_text = re.sub(r'AUTO_INCREMENT', 'AUTOINCREMENT', sql_text, flags=re.IGNORECASE)
    
    # 2. Strip MySQL server configuration headers/footers (lines starting with /*! ... */)
    sql_text = re.sub(r'/\*!.*?\*/;', '', sql_text)
    sql_text = re.sub(r'/\*!.*?\*/', '', sql_text)
    
    # 3. Clean up table creation suffixes like ENGINE=InnoDB DEFAULT CHARSET=...
    sql_text = re.sub(r'ENGINE\s*=\s*\w+(?:\s+DEFAULT\s+CHARSET\s*=\s*\w+)?', '', sql_text, flags=re.IGNORECASE)
    sql_text = re.sub(r'COLLATE\s*=\s*\w+', '', sql_text, flags=re.IGNORECASE)
    sql_text = re.sub(r'DEFAULT\s+CHARSET\s*=\s*\w+', '', sql_text, flags=re.IGNORECASE)
    
    # 4. Remove unsupported MySQL table locks
    sql_text = re.sub(r'LOCK TABLES.*?;', '', sql_text, flags=re.IGNORECASE)
    sql_text = re.sub(r'UNLOCK TABLES\s*;', '', sql_text, flags=re.IGNORECASE)
    
    # 5. Handle backtick variations cleanly
    sql_text = sql_text.replace('`', '"')
    
    return sql_text

def init_database_with_real_data():
    print("🚀 Initializing deep-cleaning database seeding engine...")
    
    # Force close any existing file connections and wipe old corruption
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass

    if not os.path.exists(SQL_PATH):
        print(f"❌ Error: Cannot find backup file at {SQL_PATH}")
        return False

    try:
        with open(SQL_PATH, 'r', encoding='utf-8') as sql_file:
            raw_script = sql_file.read()

        # Run the text sanitizer
        cleaned_script = clean_mysql_for_sqlite(raw_script)

        # Connect and execute the safe code directly into SQLite
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.executescript(cleaned_script)
        conn.commit()
        
        # Verify it actually built your requested table 
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='skin_type'")
        if cursor.fetchone():
            print("✅ Database tables successfully built and populated!")
            built_successfully = True
        else:
            print("⚠️ Table creation skipped. Check SQL file contents structure.")
            built_successfully = False
            
        conn.close()
        return built_successfully
    except Exception as e:
        print(f"❌ Failed to parse SQL script: {e}")
        return False

if __name__ == "__main__":
    init_database_with_real_data()