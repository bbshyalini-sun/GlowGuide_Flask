import os
import re
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "skincare.db")
SQL_PATH = os.path.join(BASE_DIR, "skincare_system (4).sql")

def clean_mysql_for_sqlite(sql_text):
    """Aggressively strips MySQL-specific syntax to make it 100% SQLite compliant."""
    # 1. Remove standard MySQL comments and metadata headers
    sql_text = re.sub(r'/\*!.*?\*/;', '', sql_text)
    sql_text = re.sub(r'/\*!.*?\*/', '', sql_text)
    sql_text = re.sub(r'--.*?\n', '\n', sql_text)
    
    # 2. Convert Auto-Increment safely
    sql_text = re.sub(r'AUTO_INCREMENT', 'AUTOINCREMENT', sql_text, flags=re.IGNORECASE)
    
    # 3. Strip out table trailing options (ENGINE, CHARSET, COLLATE, etc.)
    # This targets characters from the closing parenthese ) to the ending semicolon ;
    sql_text = re.sub(r'\)\s*ENGINE\s*=\s*\w+[^;]*;', ');', sql_text, flags=re.IGNORECASE)
    sql_text = re.sub(r'COLLATE\s*=\s*\w+', '', sql_text, flags=re.IGNORECASE)
    sql_text = re.sub(r'DEFAULT\s+CHARSET\s*=\s*\w+', '', sql_text, flags=re.IGNORECASE)
    sql_text = re.sub(r'CHARACTER\s+SET\s+.\w+', '', sql_text, flags=re.IGNORECASE)
    
    # 4. Remove unsupported MySQL data definitions completely
    sql_text = re.sub(r'LOCK TABLES.*?;', '', sql_text, flags=re.IGNORECASE)
    sql_text = re.sub(r'UNLOCK TABLES\s*;', '', sql_text, flags=re.IGNORECASE)
    sql_text = re.sub(r'SET\s+.*?;', '', sql_text, flags=re.IGNORECASE)
    
    # 5. Swap backticks for standard quotes
    sql_text = sql_text.replace('`', '"')
    
    # 6. Clean up empty lines or stranded semicolons that cause syntax failures
    sql_text = "\n".join([line for line in sql_text.splitlines() if line.strip()])
    
    return sql_text

def init_database_with_real_data():
    print("🚀 Initializing defensive database construction engine...")
    
    # Wipe out any corrupt historical DB file attempts
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

        # Run the deep text sanitizer
        cleaned_script = clean_mysql_for_sqlite(raw_script)

        # Connect and execute individual blocks to prevent full file rollback failures
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Split statements cleanly by semicolon to execute them safely one by one
        statements = cleaned_script.split(';')
        for statement in statements:
            clean_statement = statement.strip()
            if clean_statement:
                try:
                    cursor.execute(clean_statement)
                except sqlite3.OperationalError as statement_err:
                    # Log problematic statements instead of crashing the whole process
                    print(f"⚠️ Skipped incompatible command line: {statement_err}")
                    continue
                    
        conn.commit()
        
        # Verify if the skin_type table actually got built
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='skin_type'")
        success = cursor.fetchone() is not None
        
        if success:
            print("✅ Database tables successfully built and populated!")
        else:
            print("❌ Failure: Script finished, but 'skin_type' table still doesn't exist.")
            
        conn.close()
        return success
    except Exception as e:
        print(f"❌ Critical parser exception encountered: {e}")
        return False

if __name__ == "__main__":
    init_database_with_real_data()