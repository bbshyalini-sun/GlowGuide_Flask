import os
import re
import pandas as pd
import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'skincare_system',
    'charset': 'utf8mb4'
}

CATEGORY_MAP = {
    'moisturiser': 2, 'moisturizer': 2, 'tinted moisturizers': 2, 'spray moisturizer': 2, 'cream': 2,
    'cleanser': 1, 'face wash': 1, 'gel cleanser': 1, 'foam cleanser': 1,
    'serum': 3, 'essence': 3, 'treatment': 3, 'ampoule': 3,
    'toner': 4, 'toners & astringents': 4, 'liquid exfoliant': 4,
    'sunscreen': 5, 'sun care': 5, 'sun protection': 5, 'sunscreen milk': 5
}

ISSUE_KEYWORDS = {
    1: ['acne', 'salicylic', 'benzoyl', 'blemish', 'pimple', 'blackhead', 'pore'],
    2: ['dry', 'dryness', 'flaking', 'nourishing', 'rich cream', 'shea butter'],
    3: ['oil control', 'sebum', 'matte', 'shiny', 'clay', 'witch hazel'],
    4: ['redness', 'calm', 'soothe', 'cica', 'centella', 'inflammation'],
    5: ['fine lines', 'peptide', 'aging', 'youthful', 'collagen'],
    6: ['wrinkle', 'retinol', 'firming', 'renewing', 'bakuchiol'],
    7: ['sensitive', 'reactive', 'hypoallergenic', 'toleriane', 'soothing', 'allantoin'],
    8: ['dehydrated', 'dehydration', 'hyaluronic', 'hydration', 'thirst', 'panthenol'],
    9: ['dark spot', 'arbutin', 'brightening', 'pigment', 'fade', 'niacinamide', 'licorice'],
    10: ['dull', 'vitamin c', 'glow', 'radiance', 'ascorbic', 'ferment'],
    11: ['blackhead', 'pore', 'clarify'],
    12: ['hyperpigmentation', 'dark spot', 'brighten'],
    13: ['blackhead', 'pore', 'clarify'],
    14: ['irritation', 'sensitive', 'soothe', 'calm']
}

TYPE_KEYWORDS = {
    1: ['oily', 'matte', 'sebum', 'gel', 'bha', 'salicylic', 'foam'],
    2: ['dry', 'cream', 'rich', 'balm', 'butter', 'hyaluronic', 'moisturising'],
    3: ['combination', 'all skin types', 'balanced', 'fluid'],
    4: ['sensitive', 'gentle', 'unscented', 'fragrance-free', 'calming', 'cica', 'allantoin']
}

DATA_FILES = ['skincare_products_clean.csv', 'skincare_products.csv', '1-200.csv']


def normalize_text(value):
    if not isinstance(value, str):
        return ''
    return re.sub(r'[^a-z0-9]+', ' ', value.lower()).strip()


def get_category_id(raw_category):
    raw_text = normalize_text(str(raw_category))
    for keyword, cat_id in CATEGORY_MAP.items():
        if keyword in raw_text:
            return cat_id
    return None


def query(conn, sql, params=None, dictionary=True):
    cursor = conn.cursor(dictionary=dictionary)
    cursor.execute(sql, params or ())
    result = cursor.fetchall()
    cursor.close()
    return result


def execute(conn, sql, params=None):
    cursor = conn.cursor()
    cursor.execute(sql, params or ())
    conn.commit()
    cursor.close()


def get_existing_product_names(conn):
    rows = query(conn, 'SELECT product_name FROM product')
    return {row['product_name'] for row in rows}


def load_dataset():
    frames = []
    for file_name in DATA_FILES:
        if os.path.exists(file_name):
            try:
                df = pd.read_csv(file_name, dtype=str, keep_default_na=False, encoding='utf-8')
            except Exception:
                df = pd.read_csv(file_name, dtype=str, keep_default_na=False)
            frames.append(df)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True, sort=False)


def insert_product(conn, name, brand, category_id, description):
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO product (product_name, brand, category_id, description) VALUES (%s, %s, %s, %s)',
        (name, brand, category_id, description)
    )
    product_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    return product_id


def clean_ingredient_name(text):
    value = normalize_text(text)
    value = re.sub(r'\s+', ' ', value).strip()
    return value


def parse_ingredient_names(raw_text):
    if not isinstance(raw_text, str):
        return []
    parts = re.split(r'[,
/]+', raw_text)
    names = []
    for part in parts:
        item = clean_ingredient_name(part)
        if len(item) >= 3 and not item.isdigit():
            names.append(item)
    return list(dict.fromkeys(names))


def ensure_ingredient_exists(conn, ingredient_name):
    if not ingredient_name:
        return None
    cursor = conn.cursor()
    cursor.execute('SELECT ingredient_id FROM ingredient WHERE ingredient_name = %s', (ingredient_name,))
    row = cursor.fetchone()
    if row:
        ingredient_id = row[0]
    else:
        cursor.execute(
            'INSERT INTO ingredient (ingredient_name, description) VALUES (%s, %s)',
            (ingredient_name, 'Imported ingredient from dataset')
        )
        ingredient_id = cursor.lastrowid
        conn.commit()
    cursor.close()
    return ingredient_id


def insert_ingredient_links(conn, product_id, ingredients_text, product_name):
    candidates = parse_ingredient_names(ingredients_text)
    if not candidates:
        return
    cursor = conn.cursor()
    for ingredient_name in candidates:
        ingredient_id = ensure_ingredient_exists(conn, ingredient_name)
        if ingredient_id:
            cursor.execute(
                'INSERT IGNORE INTO product_ingredient (product_id, ingredient_id) VALUES (%s, %s)',
                (product_id, ingredient_id)
            )
    conn.commit()
    cursor.close()


def insert_skin_mappings(conn, product_id, text, category_id):
    cursor = conn.cursor()
    matched_type = False
    for skin_type_id, keywords in TYPE_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            cursor.execute(
                'INSERT IGNORE INTO product_skin_type (product_id, skin_type_id) VALUES (%s, %s)',
                (product_id, skin_type_id)
            )
            matched_type = True
    matched_issue = False
    for issue_id, keywords in ISSUE_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            cursor.execute(
                'INSERT IGNORE INTO product_skin_issue (product_id, issue_id) VALUES (%s, %s)',
                (product_id, issue_id)
            )
            matched_issue = True
    if not matched_type:
        cursor.execute(
            'INSERT IGNORE INTO product_skin_type (product_id, skin_type_id) VALUES (%s, %s)',
            (product_id, 3)
        )
    if not matched_issue:
        fallback_id = 10 if category_id == 5 else 8
        cursor.execute(
            'INSERT IGNORE INTO product_skin_issue (product_id, issue_id) VALUES (%s, %s)',
            (product_id, fallback_id)
        )
    conn.commit()
    cursor.close()


def insert_dataset_product(conn, row, existing_names):
    product_name = str(row.get('product_name', '')).strip()
    if not product_name or product_name in existing_names:
        return None
    category_raw = str(row.get('product_type', '') or row.get('category', '')).strip()
    category_id = get_category_id(category_raw)
    if not category_id:
        return None
    brand = str(row.get('brand', '')).strip() or None
    description = f'Imported automated formulation. Source registry: dataset'
    product_id = insert_product(conn, product_name, brand, category_id, description)
    ingredient_source = str(row.get('ingredients', '') or row.get('clean_ingreds', '')).strip()
    insert_ingredient_links(conn, product_id, ingredient_source, product_name)
    text = normalize_text(' '.join([product_name, category_raw, ingredient_source]))
    insert_skin_mappings(conn, product_id, text, category_id)
    existing_names.add(product_name)
    return product_id


def find_candidates(df, existing_names, category_id=None, keyword_list=None):
    results = []
    for _, row in df.iterrows():
        name = str(row.get('product_name', '')).strip()
        if not name or name in existing_names:
            continue
        category_raw = str(row.get('product_type', '') or row.get('category', '')).strip()
        this_category_id = get_category_id(category_raw)
        if not this_category_id:
            continue
        if category_id is not None and this_category_id != category_id:
            continue
        text = normalize_text(' '.join([name, category_raw, str(row.get('ingredients', ''))]))
        if keyword_list is None or any(keyword in text for keyword in keyword_list):
            results.append((row, this_category_id, text))
    return results


def ensure_skin_type_minimums(conn, df):
    existing_names = get_existing_product_names(conn)
    skin_types = query(conn, 'SELECT skin_type_id FROM skin_type')
    for skin_type in skin_types:
        skin_type_id = skin_type['skin_type_id']
        count = query(conn, 'SELECT COUNT(DISTINCT product_id) AS cnt FROM product_skin_type WHERE skin_type_id = %s', (skin_type_id,))[0]['cnt']
        needed = max(0, 5 - count)
        if needed == 0:
            continue
        candidates = find_candidates(df, existing_names, keyword_list=TYPE_KEYWORDS.get(skin_type_id, []))
        for row, category_id, text in candidates:
            if needed <= 0:
                break
            current_category_count = query(conn, 'SELECT COUNT(*) AS cnt FROM product WHERE category_id = %s', (category_id,))[0]['cnt']
            if current_category_count >= 40:
                continue
            if insert_dataset_product(conn, row, existing_names):
                needed -= 1


def ensure_skin_issue_minimums(conn, df):
    existing_names = get_existing_product_names(conn)
    issues = query(conn, 'SELECT issue_id FROM skin_issue')
    for issue in issues:
        issue_id = issue['issue_id']
        count = query(conn, 'SELECT COUNT(DISTINCT product_id) AS cnt FROM product_skin_issue WHERE issue_id = %s', (issue_id,))[0]['cnt']
        needed = max(0, 5 - count)
        if needed == 0:
            continue
        candidates = find_candidates(df, existing_names, keyword_list=ISSUE_KEYWORDS.get(issue_id, []))
        for row, category_id, text in candidates:
            if needed <= 0:
                break
            current_category_count = query(conn, 'SELECT COUNT(*) AS cnt FROM product WHERE category_id = %s', (category_id,))[0]['cnt']
            if current_category_count >= 40:
                continue
            if insert_dataset_product(conn, row, existing_names):
                needed -= 1


def fill_category_capacity(conn, df):
    existing_names = get_existing_product_names(conn)
    categories = query(conn, 'SELECT category_id FROM category')
    for category in categories:
        category_id = category['category_id']
        current_count = query(conn, 'SELECT COUNT(*) AS cnt FROM product WHERE category_id = %s', (category_id,))[0]['cnt']
        need = max(0, 40 - current_count)
        if need == 0:
            continue
        candidates = find_candidates(df, existing_names, category_id=category_id)
        for row, _, _ in candidates:
            if need <= 0:
                break
            if insert_dataset_product(conn, row, existing_names):
                need -= 1


def prune_excess_products(conn):
    keep_ids = set()
    categories = query(conn, 'SELECT category_id FROM category')
    skin_types = query(conn, 'SELECT skin_type_id FROM skin_type')
    issues = query(conn, 'SELECT issue_id FROM skin_issue')

    for category in categories:
        keep_ids.update(get_top_ids(conn, 'SELECT product_id FROM product WHERE category_id = %s ORDER BY product_id ASC LIMIT 40', (category['category_id'],)))
    for skin_type in skin_types:
        keep_ids.update(get_top_ids(conn, 'SELECT product_id FROM product p JOIN product_skin_type pst ON p.product_id = pst.product_id WHERE pst.skin_type_id = %s ORDER BY p.product_id ASC LIMIT 5', (skin_type['skin_type_id'],)))
    for issue in issues:
        keep_ids.update(get_top_ids(conn, 'SELECT product_id FROM product p JOIN product_skin_issue psi ON p.product_id = psi.product_id WHERE psi.issue_id = %s ORDER BY p.product_id ASC LIMIT 5', (issue['issue_id'],)))

    all_ids = [row['product_id'] for row in query(conn, 'SELECT product_id FROM product')]
    remove_ids = [pid for pid in all_ids if pid not in keep_ids]

    print(f'Keeping {len(keep_ids)} products. Removing {len(remove_ids)} extra products.')
    if remove_ids:
        delete_rows(conn, 'product_skin_type', remove_ids)
        delete_rows(conn, 'product_skin_issue', remove_ids)
        delete_rows(conn, 'product_ingredient', remove_ids)
        delete_rows(conn, 'product', remove_ids)
        print(f'Removed {len(remove_ids)} products and cascaded related rows.')
    else:
        print('No products removed. The table already meets the required limits.')


def get_top_ids(conn, sql, params):
    return [row['product_id'] for row in query(conn, sql, params)]


def delete_rows(conn, table, ids):
    if not ids:
        return
    placeholders = ','.join(['%s'] * len(ids))
    execute(conn, f'DELETE FROM {table} WHERE product_id IN ({placeholders})', tuple(ids))


def main():
    conn = mysql.connector.connect(**DB_CONFIG)
    try:
        df = load_dataset()
        if df.empty:
            print('No dataset files found. Please add CSV sources and run again.')
            return
        ensure_skin_type_minimums(conn, df)
        ensure_skin_issue_minimums(conn, df)
        fill_category_capacity(conn, df)
        prune_excess_products(conn)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
