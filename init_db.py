import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "skincare.db")
SQL_PATH = os.path.join(BASE_DIR, "skincare_system (4).sql")

def init_database_with_real_data():
    """Reads the raw backup .sql file and writes its tables and rows into skincare.db"""
    print("🚀 Initializing database seeding engine...")
    
    # 1. Clear out an empty or corrupted database file if it exists
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass

    # 2. Check if the raw sql script is missing
    if not os.path.exists(SQL_PATH):
        print(f"❌ Error: Cannot find backup file at {SQL_PATH}")
        return False

    try:
        # 3. Read raw SQL commands
        with open(SQL_PATH, 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()

        # 4. Open connection and execute script commands to seed rows
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Execute script containing table creations and inserts
        cursor.executescript(sql_script)
        
        conn.commit()
        conn.close()
        print("✅ Database successfully populated with your tables and rows!")
        return True
    except Exception as e:
        print(f"❌ Failed to parse SQL script: {e}")
        return False

if __name__ == "__main__":
    init_database_with_real_data()