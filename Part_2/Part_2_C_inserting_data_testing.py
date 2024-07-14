import sqlite3
import pandas as pd


db = sqlite3.connect("QHO429.db")

cursor = db.cursor()


insert_data_sql = """
INSERT INTO review_marks (rating, comment) VALUES ('*****', 'Excellent product, worth buying');
INSERT INTO review_marks (rating, comment) VALUES ('*', 'I dont recommend');
INSERT INTO review_marks (rating, comment) VALUES ('***', 'Slow delivery');
INSERT INTO review_marks (rating, comment) VALUES ('*', 'Awful seller');
INSERT INTO review_marks (rating, comment) VALUES ('****', 'Great seller');
INSERT INTO review_marks (rating, comment) VALUES ('**', 'Moody seller');

INSERT INTO shopper_product_review (shopper_id, product_id, mark_id) VALUES (10000, 3000000, 13);
INSERT INTO shopper_product_review (shopper_id, product_id, mark_id) VALUES (10001, 3000021, 14);
INSERT INTO shopper_product_review (shopper_id, product_id, mark_id) VALUES (10000, 3000021, 15);

INSERT INTO shopper_seller_review (shopper_id, seller_id, mark_id) VALUES (10000, 200000, 16);
INSERT INTO shopper_seller_review (shopper_id, seller_id, mark_id) VALUES (10001, 200001, 17);
INSERT INTO shopper_seller_review (shopper_id, seller_id, mark_id) VALUES (10000, 200000, 18);
"""


cursor.executescript(insert_data_sql)
db.commit()


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
