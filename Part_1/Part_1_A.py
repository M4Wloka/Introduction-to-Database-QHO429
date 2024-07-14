import sqlite3
import pandas as pd

db = sqlite3.connect("QHO429.db")

sql_query = """
SELECT 
IFNULL(shopper_first_name, 'Not known') AS "Shopper First Name", 
IFNULL(shopper_surname, 'Not known') AS "Shopper Surname", 
IFNULL(shopper_email_address, 'Not known') AS "Email address", 
IFNULL(gender, 'Not known') AS "Gender", 
IFNULL(STRFTIME('%d/%m/%Y', date_joined), 'Not known') AS "Date Joined", 
IFNULL((strftime('%Y', 'now') - strftime('%Y', date_of_birth)) - (strftime('%m-%d', 'now') < strftime('%m-%d', date_of_birth)), 'Not known') AS "Current Age" 
FROM shoppers 
WHERE gender = 'F' OR date_joined > DATE('2020-01-01') 
ORDER BY "Gender", "Current Age" DESC;
"""

df = pd.read_sql_query(sql_query, db)

db.close()

print(df)
