import sqlite3
import pandas as pd

db = sqlite3.connect("QHO429.db")

sql_query = """
SELECT
c.category_description AS "Category Description", 
p.product_code AS "Product Code", 
p.product_description AS "Product Description", 
IFNULL(ROUND(AVG(op.quantity), 2), 0) AS "Avg Qty Sold",
(SELECT IFNULL(ROUND(AVG(op_inner.quantity), 2), 0) 
 FROM ordered_products op_inner
 LEFT JOIN products p_inner ON op_inner.product_id = p_inner.product_id 
 WHERE c.category_id = p_inner.category_id 
 AND op_inner.ordered_product_status <> 'Cancelled') AS "Avg Qty Sold for Category"
FROM
categories c
LEFT JOIN
products p ON c.category_id = p.category_id 
LEFT JOIN
ordered_products op ON p.product_id = op.product_id 
AND op.ordered_product_status <> 'Cancelled'
GROUP BY
c.category_description, 
p.product_id 
HAVING
"Avg Qty Sold" < "Avg Qty Sold for Category"
ORDER BY
"Category Description", "Product Description";
"""

df = pd.read_sql_query(sql_query, db)

db.close()

print(df)
