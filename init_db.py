import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "skincare.db")
SQL_PATH = os.path.join(BASE_DIR, "skincare_system (4).sql")

def init_database_with_real_data():
    print("🚀 Initializing database seeding engine...")
    
    # 1. Force clear old corrupt or partial tables file
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.close()
            os.remove(DB_PATH)
        except Exception:
            pass

    if not os.path.exists(SQL_PATH):
        print(f"❌ Error: Cannot find backup file at {SQL_PATH}")
        return False

    try:
        # 2. Read raw SQL commands
        with open(SQL_PATH, 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()

        # 3. Translate MySQL keywords to SQLite keywords so it doesn't crash
        # This replaces "INTEGER PRIMARY KEY AUTO_INCREMENT" with "INTEGER PRIMARY KEY AUTOINCREMENT"
        sql_script = sql_script.replace("PRIMARY KEY AUTO_INCREMENT", "PRIMARY KEY AUTOINCREMENT")
        sql_script = sql_script.replace("PRIMARY KEY AUTO_INCREMENT", "PRIMARY KEY AUTOINCREMENT")

        # 4. Connect and inject tables and rows completely
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Run the entire SQL backup script
        cursor.executescript(sql_script)
        
        conn.commit()
        conn.close()
        print("✅ Database tables successfully built and populated!")
        return True
    except Exception as e:
        print(f"❌ Failed to parse SQL script: {e}")
        return False

if __name__ == "__main__":
    init_database_with_real_data()