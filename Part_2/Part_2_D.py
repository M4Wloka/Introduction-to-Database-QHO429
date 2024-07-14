import sqlite3
import pandas as pd


db = sqlite3.connect("QHO429.db")


cursor = db.cursor()


create_views_sql = """
CREATE VIEW IF NOT EXISTS shopper_reviews_sellers AS
SELECT
    sh.shopper_first_name || ' ' || sh.shopper_surname AS "Shopper Name",
    s.seller_name AS "Seller Name", 
    sr.rating AS "Seller Rating", 
    sr.comment AS "Comment",
    sr.review_date AS "Review Date"
FROM 
    shopper_seller_review ss
LEFT JOIN 
    sellers s ON ss.seller_id = s.seller_id
LEFT JOIN 
    review_marks sr ON ss.mark_id = sr.mark_id
LEFT JOIN 
    shoppers sh ON ss.shopper_id = sh.shopper_id;

CREATE VIEW IF NOT EXISTS shopper_reviews_products AS
SELECT
    sh.shopper_first_name || ' ' || sh.shopper_surname AS "Shopper Name",
    p.product_description AS "Product Description",
    r.rating AS "Product Rating", 
    r.comment AS "Comment",
    r.review_date AS "Review Date"
FROM 
    shopper_product_review sp
LEFT JOIN 
    products p ON sp.product_id = p.product_id
LEFT JOIN 
    review_marks r ON sp.mark_id = r.mark_id
LEFT JOIN 
    shoppers sh ON sp.shopper_id = sh.shopper_id;
"""


cursor.executescript(create_views_sql)
db.commit()


query_seller_reviews = "SELECT * FROM shopper_reviews_sellers"
query_product_reviews = "SELECT * FROM shopper_reviews_products"


df_seller_reviews = pd.read_sql_query(query_seller_reviews, db)
df_product_reviews = pd.read_sql_query(query_product_reviews, db)


db.close()


print("Seller Reviews:")
print(df_seller_reviews)
print("\nProduct Reviews:")
print(df_product_reviews)
