import json
import mysql.connector

#=====================
# DB Example:

# ---products:  // DB
#     ---products: // Table
#         ---Id
#         ---Maker
#         ---Image
#         ---....
#     ---ratings:
#         ---Id
#         ---ProductId
#         ---Rating
#=====================

# Read the JSON file
with open("products.json", "r") as f:
    data = json.load(f)
try:
    # Connect to the MySQL database
    con = mysql.connector.connect(
        user='user',
        password='password',
        host='localhost',
        port=3306,
        database='products'
    )
    if con.is_connected():
        print("Connected to MySQL database!")
except Exception as e:
    print("Cannot connect to MySQL database:", e)

# Iterate over the data and insert product information and ratings
for item in data:
    cursor = con.cursor()
    try:
        #Insert product information
        sql_product = "INSERT INTO products (Id, Maker, Image, Url, Title, Description) VALUES (%s, %s, %s, %s, %s, %s)"
        values_product = (item['Id'], item['Maker'], item['img'], item['Url'], item['Title'], item['Description'])
        cursor.execute(sql_product, values_product)
        con.commit()
        #Retrieve the inserted product's ID
        product_id = item['Id']
        # Insert ratings for the product
        for rating in item['Ratings']:
            sql_rating = "INSERT INTO ratings (ProductId, Rating) VALUES (%s, %s)"
            values_rating = (product_id, rating)
            cursor.execute(sql_rating, values_rating)
            con.commit()
        print("Inserted data for:", item['Id'])
    except Exception as e:
        print("Error inserting data for", item['Id'], ":", e)
    # Close the cursor
    cursor.close()
# Close the connection
con.close()
