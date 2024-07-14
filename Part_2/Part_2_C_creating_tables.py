import sqlite3
import pandas as pd


db = sqlite3.connect("QHO429.db")


create_tables_sql = """
CREATE TABLE IF NOT EXISTS review_marks (
    mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rating TEXT CHECK (rating IN ('*', '**', '***', '****', '*****')) NOT NULL,
    comment TEXT NOT NULL,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS shopper_product_review (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shopper_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    mark_id INTEGER NOT NULL,
    FOREIGN KEY (shopper_id) REFERENCES shoppers(shopper_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (mark_id) REFERENCES review_marks(mark_id)
);

CREATE TABLE IF NOT EXISTS shopper_seller_review (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shopper_id INTEGER NOT NULL,
    seller_id INTEGER NOT NULL,
    mark_id INTEGER NOT NULL,
    FOREIGN KEY (shopper_id) REFERENCES shoppers(shopper_id),
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id),
    FOREIGN KEY (mark_id) REFERENCES review_marks(mark_id)
);
"""

cursor = db.cursor()
cursor.executescript(create_tables_sql)
db.commit()