import os, sqlite3
from init_db import init_database_with_real_data
print('db exists', os.path.exists('skincare.db'))
print('init', init_database_with_real_data())
conn=sqlite3.connect('skincare.db')
cur=conn.cursor()
print('tables', cur.execute("select name from sqlite_master where type='table' order by name").fetchall())
print('skin type count', cur.execute('select count(*) from skin_type').fetchone()[0])
print('skin issue count', cur.execute('select count(*) from skin_issue').fetchone()[0])
print('product count', cur.execute('select count(*) from product').fetchone()[0])
print('product_skin_type count', cur.execute('select count(*) from product_skin_type').fetchone()[0])
print('product_skin_issue count', cur.execute('select count(*) from product_skin_issue').fetchone()[0])
q='''SELECT DISTINCT p.product_id, p.product_name, c.category_name
FROM product p
JOIN category c ON p.category_id = c.category_id
JOIN product_skin_type pst ON p.product_id = pst.product_id
JOIN product_skin_issue psi ON p.product_id = psi.product_id
WHERE pst.skin_type_id = ? AND psi.issue_id IN (?,?)
ORDER BY c.category_id, p.product_name'''
rows=cur.execute(q,(2,1,2)).fetchall()
print('query count', len(rows))
print('sample', rows[:10])
conn.close()
