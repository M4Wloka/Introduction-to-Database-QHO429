import sqlite3
import pandas as pd


shopper_id = input("Please enter the shopper ID: ")


db = sqlite3.connect("QHO429.db")


sql_query = """
SELECT
s.shopper_first_name AS "Shopper First Name", 
s.shopper_surname AS "Shopper Surname", 
op.order_id AS "Order ID", 
STRFTIME('%d-%m-%Y', o.order_date) AS "Order Date", 
p.product_description AS "Description", 
se.seller_name AS "Seller Name", 
op.quantity AS "Qty", 
'£' || ROUND(op.price, 2) AS "Price", 
op.ordered_product_status AS "Order Status"
FROM shoppers s
INNER JOIN shopper_orders o ON s.shopper_id = o.shopper_id
INNER JOIN ordered_products op ON o.order_id = op.order_id
INNER JOIN products p ON op.product_id = p.product_id
INNER JOIN sellers se ON op.seller_id = se.seller_id
WHERE s.shopper_id = ?
ORDER BY o.order_date DESC;
"""


df = pd.read_sql_query(sql_query, db, params=(shopper_id,))


db.close()


print(df)
