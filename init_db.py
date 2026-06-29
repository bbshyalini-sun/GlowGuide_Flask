import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'skincare.db')

def init_database():
    """Initialize the database with tables and data from phpMyAdmin SQL dump"""
    # Delete existing database if present
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create skin_type table
    cursor.execute('''
    CREATE TABLE skin_type (
        skin_type_id INTEGER PRIMARY KEY,
        skin_type_name TEXT NOT NULL
    )
    ''')
    
    # Create skin_issue table
    cursor.execute('''
    CREATE TABLE skin_issue (
        issue_id INTEGER PRIMARY KEY,
        issue_name TEXT NOT NULL
    )
    ''')
    
    # Create category table
    cursor.execute('''
    CREATE TABLE category (
        category_id INTEGER PRIMARY KEY,
        category_name TEXT NOT NULL
    )
    ''')
    
    # Create ingredient table
    cursor.execute('''
    CREATE TABLE ingredient (
        ingredient_id INTEGER PRIMARY KEY,
        ingredient_name TEXT NOT NULL UNIQUE,
        description TEXT NOT NULL
    )
    ''')
    
    # Create product table
    cursor.execute('''
    CREATE TABLE product (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL UNIQUE,
        brand TEXT NOT NULL,
        category_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        FOREIGN KEY (category_id) REFERENCES category(category_id)
    )
    ''')
    
    # Create product_ingredient table
    cursor.execute('''
    CREATE TABLE product_ingredient (
        product_id INTEGER NOT NULL,
        ingredient_id INTEGER NOT NULL,
        PRIMARY KEY (product_id, ingredient_id),
        FOREIGN KEY (product_id) REFERENCES product(product_id),
        FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id)
    )
    ''')
    
    # Create product_skin_issue table
    cursor.execute('''
    CREATE TABLE product_skin_issue (
        product_id INTEGER NOT NULL,
        issue_id INTEGER NOT NULL,
        PRIMARY KEY (product_id, issue_id),
        FOREIGN KEY (product_id) REFERENCES product(product_id),
        FOREIGN KEY (issue_id) REFERENCES skin_issue(issue_id)
    )
    ''')
    
    # Create product_skin_type table
    cursor.execute('''
    CREATE TABLE product_skin_type (
        product_id INTEGER NOT NULL,
        skin_type_id INTEGER NOT NULL,
        PRIMARY KEY (product_id, skin_type_id),
        FOREIGN KEY (product_id) REFERENCES product(product_id),
        FOREIGN KEY (skin_type_id) REFERENCES skin_type(skin_type_id)
    )
    ''')
    
    # Insert skin_type data
    skin_types = [
        (1, 'Oily'),
        (2, 'Dry'),
        (3, 'Combination'),
        (4, 'Sensitive'),
    ]
    cursor.executemany('INSERT INTO skin_type (skin_type_id, skin_type_name) VALUES (?, ?)', skin_types)
    
    # Insert skin_issue data
    skin_issues = [
        (1, 'Acne'),
        (2, 'Dryness'),
        (3, 'Oiliness'),
        (4, 'Redness'),
        (5, 'Dark Spots'),
        (6, 'Dullness'),
        (7, 'Large Pores'),
        (8, 'Uneven Texture'),
        (9, 'Sensitivity'),
        (10, 'Dehydration'),
        (11, 'Fine Lines'),
        (12, 'Hyperpigmentation'),
        (13, 'Blackheads'),
        (14, 'Irritation'),
    ]
    cursor.executemany('INSERT INTO skin_issue (issue_id, issue_name) VALUES (?, ?)', skin_issues)
    
    # Insert category data
    categories = [
        (1, 'Cleanser'),
        (2, 'Moisturizer'),
        (3, 'Serum'),
        (4, 'Toner'),
        (5, 'Sunscreen'),
    ]
    cursor.executemany('INSERT INTO category (category_id, category_name) VALUES (?, ?)', categories)
    
    # Insert ingredient data
    ingredients = [
        (1, 'Salicylic Acid', 'Helps acne and oily skin'),
        (2, 'Niacinamide', 'Controls oil and brightens skin'),
        (3, 'Ceramide', 'Repairs skin barrier'),
        (4, 'Centella', 'Soothes redness'),
        (5, 'Hyaluronic Acid', 'Hydrates dry skin'),
        (6, 'Retinol', 'Stimulates collagen and improves skin firmness and texture'),
        (7, 'Vitamin C', 'Powerful antioxidant that brightens skin and fades dark spots'),
        (8, 'Benzoyl Peroxide', 'Kills acne-causing bacteria and prevents breakouts'),
        (9, 'Lactic Acid', 'Gentle AHA that exfoliates surface skin and hydrates'),
        (11, 'Zinc Oxide', 'Physical UV filter that also soothes irritated skin'),
        (12, 'Squalane', 'Lightweight lipid that moisturizes without clogging pores'),
        (13, 'Glycerin', 'Humectant that draws water into the outer layer of the skin'),
        (14, 'Panthenol (Vitamin B5)', 'Soothes inflammation and promotes skin healing'),
        (15, 'Peptides', 'Short chains of amino acids that rebuild the skin barrier'),
        (16, 'Azelaic Acid', 'Reduces redness, rosacea, and unclogs pores'),
        (17, 'Kojic Acid', 'Inhibits melanin production to treat hyperpigmentation'),
        (18, 'Sulfur', 'Absorbs excess oil and dries out dead skin cells to clear acne'),
        (19, 'Tea Tree Oil', 'Natural antibacterial and anti-inflammatory oil for acne'),
        (20, 'Urea', 'Breaks down dead skin while providing deep hydration'),
        (21, 'Allantoin', 'Extracted from the comfrey plant, highly effective at healing'),
        (23, 'Bakuchiol', 'Plant-based, gentler alternative to Retinol for sensitive skin'),
        (24, 'Ferulic Acid', 'Boosts the effectiveness of other antioxidants like Vitamin C'),
        (25, 'Polyhydroxy Acid (PHA)', 'Very gentle exfoliant suitable for highly sensitive skin'),
        (26, 'Titanium Dioxide', 'Gentle mineral UV filter for sun protection'),
        (29, 'Green Tea Extract', 'Soothes skin and provides protection against free radicals'),
        (38, 'Zinc PCA', 'Controls sebum production'),
        (40, 'Alpha Arbutin', 'Targets pigmentation'),
        (41, 'Glycolic Acid', 'Improves dullness'),
        (43, 'PHA', 'Mild exfoliation for sensitive skin'),
        (44, 'Mandelic Acid', 'Improves texture'),
        (45, 'Aloe Vera', 'Hydrates and calms'),
        (50, 'Chamomile Extract', 'Calms irritation'),
        (52, 'Shea Butter', 'Repairs dryness'),
        (55, 'Tranexamic Acid', 'Improves dark spots'),
        (56, 'Arbutin', 'Brightening ingredient'),
        (57, 'Caffeine', 'Reduces puffiness'),
        (58, 'Kaolin Clay', 'Absorbs oil'),
        (59, 'BHA', 'Deep exfoliation'),
        (60, 'AHA', 'Surface exfoliation'),
        (61, 'Rice Extract', 'Brightening'),
        (62, 'Licorice Extract', 'Reduces redness'),
        (63, 'Rose Water', 'Hydrating toner ingredient'),
        (64, 'Vitamin E', 'Antioxidant'),
        (65, 'Collagen', 'Supports elasticity'),
        (66, 'Snail Mucin', 'Repairs barrier'),
        (67, 'Propolis', 'Soothes acne'),
        (70, 'Ginseng Extract', 'Revitalizes skin'),
        (71, 'Witch Hazel', 'Controls oil'),
        (72, 'Charcoal', 'Deep cleansing'),
        (73, 'Honey Extract', 'Hydrating'),
        (74, 'Cica', 'Sensitive skin support'),
        (75, 'Bisabolol', 'Calming ingredient'),
        (76, 'Oat Extract', 'Barrier support'),
        (77, 'Jojoba Oil', 'Balancing oil'),
        (78, 'Sunflower Oil', 'Moisturizing oil'),
        (79, 'Seaweed Extract', 'Hydration support'),
        (80, 'Copper Peptides', 'Firming ingredient'),
        (81, 'Beta Glucan', 'Soothing ingredient'),
        (82, 'Berry Extract', 'Antioxidant ingredient'),
        (83, 'Lemon Extract', 'Brightening ingredient'),
        (84, 'Papaya Extract', 'Exfoliating ingredient'),
        (85, 'Apple Extract', 'Texture improvement'),
        (86, 'Coconut Water', 'Hydration ingredient'),
        (87, 'Mint Extract', 'Refreshing ingredient'),
        (89, 'Resveratrol', 'Anti-aging antioxidant'),
        (91, 'Madecassoside', 'Calming ingredient'),
    ]
    cursor.executemany('INSERT INTO ingredient (ingredient_id, ingredient_name, description) VALUES (?, ?, ?)', ingredients)
    
    # Insert product data
    products = [
        (1, 'Oil Control Cleanser', 'Skinalyze', 1, 'Cleanser for oily acne-prone skin'),
        (2, 'Purifying Acne Cleanser', 'Skinalyze', 1, 'Targets blackheads and acne'),
        (3, 'Hydrating Foam Cleanser', 'Skinalyze', 1, 'Gentle hydrating cleanser'),
        (4, 'Sensitive Skin Cleanser 16', 'Skinalyze', 1, 'Calming cleanser for redness'),
        (5, 'Deep Pore Cleanser 21', 'Skinalyze', 1, 'Deep cleansing formula'),
        (6, 'Balancing Gel Cleanser 26', 'Skinalyze', 1, 'Balances oil and hydration'),
        (7, 'Brightening Cleanser 31', 'Skinalyze', 1, 'Brightens dull skin'),
        (8, 'Barrier Support Cleanser 36', 'Skinalyze', 1, 'Supports sensitive skin barrier'),
        (9, 'Hydrating Barrier Cream', 'Skinalyze', 2, 'Moisturizer for dry sensitive skin'),
        (10, 'Barrier Repair Cream 41', 'Skinalyze', 2, 'Moisturizer for dryness'),
        (11, 'Hydrating Moisturizer 46', 'Skinalyze', 2, 'Deep hydration support'),
        (12, 'Sensitive Relief Cream 51', 'Skinalyze', 2, 'Calms redness and irritation'),
        (13, 'Oil Free Moisturizer 56', 'Skinalyze', 2, 'Hydration without clogging pores'),
        (14, 'Firming Moisturizer 61', 'Skinalyze', 2, 'Supports elasticity and firmness'),
        (15, 'Glow Repair Cream 66', 'Skinalyze', 2, 'Improves dullness and texture'),
        (16, 'Daily Moisture Cream 71', 'Skinalyze', 2, 'Daily hydration support'),
        (17, 'Calming Barrier Cream 76', 'Skinalyze', 2, 'Barrier care for irritation'),
        (18, 'Calming Barrier Serum', 'Skinalyze', 3, 'Serum for redness and irritation'),
        (19, 'Brightening Serum 81', 'Skinalyze', 3, 'Targets dark spots'),
        (20, 'Pore Refining Serum 86', 'Skinalyze', 3, 'Minimizes pores'),
        (21, 'Texture Renewal Serum 91', 'Skinalyze', 3, 'Improves uneven texture'),
        (22, 'Acne Repair Serum 96', 'Skinalyze', 3, 'Targets acne prone skin'),
        (23, 'Hydrating Serum 101', 'Skinalyze', 3, 'Boosts hydration'),
        (24, 'Calming Serum 106', 'Skinalyze', 3, 'Soothes redness'),
        (25, 'Firming Peptide Serum 111', 'Skinalyze', 3, 'Improves firmness'),
        (26, 'Daily Glow Serum 116', 'Skinalyze', 3, 'Improves dullness'),
        (27, 'Blackhead Control Serum 121', 'Skinalyze', 3, 'Controls blackheads'),
        (28, 'Sensitive Repair Serum 126', 'Skinalyze', 3, 'Repairs irritated skin'),
        (29, 'Balancing Glow Toner', 'Skinalyze', 4, 'Toner for combination skin'),
        (30, 'Glow Renewal Toner 131', 'Skinalyze', 4, 'Brightening toner'),
        (31, 'Hydrating Toner 136', 'Skinalyze', 4, 'Hydration support toner'),
        (32, 'Oil Balancing Toner 141', 'Skinalyze', 4, 'Controls excess oil'),
        (33, 'Pore Care Toner 146', 'Skinalyze', 4, 'Refines pores'),
        (34, 'Texture Refining Toner 156', 'Skinalyze', 4, 'Improves texture'),
        (35, 'Daily Fresh Toner 161', 'Skinalyze', 4, 'Daily refreshing toner'),
        (36, 'Daily Protection Sunscreen 166', 'Skinalyze', 5, 'UV protection for sensitive skin'),
        (37, 'Oil Control Sunscreen 171', 'Skinalyze', 5, 'Sunscreen for oily skin'),
        (38, 'Hydrating Sunscreen 176', 'Skinalyze', 5, 'Hydrating UV protection'),
        (39, 'Brightening Sunscreen 181', 'Skinalyze', 5, 'Brightening daily UV care'),
        (40, 'Sensitive Shield Sunscreen 186', 'Skinalyze', 5, 'Gentle sunscreen for irritation'),
        (41, 'Matte Finish Sunscreen 191', 'Skinalyze', 5, 'Controls shine and protects skin'),
        (42, 'Barrier Defense Sunscreen 196', 'Skinalyze', 5, 'Protects sensitive skin barrier'),
    ]
    cursor.executemany('INSERT INTO product (product_id, product_name, brand, category_id, description) VALUES (?, ?, ?, ?, ?)', products)
    
    # Insert product_ingredient relationships
    product_ingredients = [
        (5, 1),
        (6, 2),
        (7, 3),
        (8, 4),
        (9, 1),
        (10, 2),
        (11, 3),
        (12, 4),
    ]
    cursor.executemany('INSERT INTO product_ingredient (product_id, ingredient_id) VALUES (?, ?)', product_ingredients)
    
    # Insert product_skin_issue relationships
    product_issues = [
        (5, 1),
        (6, 2),
        (7, 3),
        (8, 4),
        (9, 1),
        (10, 2),
        (11, 3),
        (12, 4),
    ]
    cursor.executemany('INSERT INTO product_skin_issue (product_id, issue_id) VALUES (?, ?)', product_issues)
    
    # Insert product_skin_type relationships
    product_types = [
        (5, 1),
        (5, 3),
        (6, 2),
        (6, 4),
        (7, 1),
        (7, 3),
        (8, 2),
        (8, 4),
        (9, 1),
        (10, 2),
        (11, 1),
        (11, 3),
        (12, 4),
    ]
    cursor.executemany('INSERT INTO product_skin_type (product_id, skin_type_id) VALUES (?, ?)', product_types)
    
    conn.commit()
    conn.close()
    
    print(f"✓ Database initialized successfully at {DB_PATH}")

if __name__ == '__main__':
    init_database()
