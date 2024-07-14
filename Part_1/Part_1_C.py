import sqlite3
import pandas as pd

db = sqlite3.connect("QHO429.db")

sql_query = """
SELECT
se.seller_account_ref AS "Seller Account Ref",  -- sellers
se.seller_name AS "Seller Name", -- sellers
p.product_code AS "Product Code", -- products
p.product_description AS "Product Description", -- products
IFNULL(COUNT(DISTINCT op.order_id), 0) AS "No of Orders", -- count the unique orders numbers / ordered_products
IFNULL(SUM(op.quantity), 0) AS "Total Quantity Sold",  -- ordered_products
'£' || IFNULL(ROUND(SUM(op.quantity * op.price), 2), 0) AS "Total Value of Sales" -- ordered_products
FROM
sellers se
LEFT JOIN products p ON 1=1  -- sellers table + products table
LEFT JOIN ordered_products op ON op.product_id = p.product_id AND op.seller_id = se.seller_id  -- ordered_products + products and ordered_products + sellers
GROUP BY
se.seller_account_ref,
se.seller_name,
p.product_code,
p.product_description
ORDER BY "Total Quantity Sold";

"""

df = pd.read_sql_query(sql_query, db)

db.close()

print(df)
