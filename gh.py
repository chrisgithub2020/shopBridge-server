import sqlite3

conn = sqlite3.connect("shopBridge.db")
cur = conn.cursor()

# cur.execute("""
#             CREATE TABLE Consumers (
#     id TEXT PRIMARY KEY, 
#     first_name TEXT NOT NULL,
#     last_name TEXT NOT NULL,
#     contact TEXT NOT NULL,
#     email TEXT UNIQUE NOT NULL,
#     password TEXT NOT NULL,
#     address TEXT NOT NULL)

# """
# )

# cur.execute("""
# CREATE TABLE Sellers (
#      id TEXT PRIMARY KEY,
#      store_name TEXT NOT NULL,
#      email TEXT NOT NULL,
#      contact TEXT NOT NULL,
#      seller_name TEXT NOT NULL,
#      password TEXT NOT NULL,
#      photo TEXT,
#      id_card_number TEXT NOT NULL)
# """)

# cur.execute("""
# CREATE TABLE Products (
#     id TEXT PRIMARY KEY,
#     seller_id TEXT NOT NULL,
#     product_name VARCHAR(255) NOT NULL,
#     product_description TEXT,
#     main_category VARCHAR(100),
#     sub_category VARCHAR(100),
#     price DECIMAL(10, 2),
#     quantity INT,
#     photos TEXT,
#     FOREIGN KEY (seller_id) REFERENCES Sellers(id)
# );

# """)

# cur.execute("""
# CREATE TABLE Orders (
#     order_id TEXT PRIMARY KEY,
#     seller_id TEXT,
#     consumer_id TEXT,
#     product_id TEXT,
#     date_ordered DATE,
#     date_received DATE,
#     amount_paid DECIMAL(10, 2),
#     address VARCHAR(255),
#     quantity TEXT,
#     FOREIGN KEY (seller_id) REFERENCES Sellers(id),
#     FOREIGN KEY (consumer_id) REFERENCES Consumers(id),
#     FOREIGN KEY (product_id) REFERENCES Products(id)
# );

# """)
id = "b4cebabc-cb96-4d2e-95c9-65fe2893ecde"

# cur.execute("""
# CREATE TABLE Restock (
#     id TEXT PRIMARY KEY,
#     product_id TEXT,
#     seller_id TEXT,
#     date DATE,
#     FOREIGN KEY (product_id) REFERENCES Products(id),
#     FOREIGN KEY (seller_id) REFERENCES Sellers(id)
# );

# """)

# cur.execute(f"""UPDATE Orders SET date_received="none" WHERE order_id="{id}";""")
# conn.commit()
cur.execute("SELECT * FROM Orders;")
# conn.commit()
print(cur.fetchall())

"('b4cebabc-cb96-4d2e-95c9-65fe2893ecde', '4c609bb0-b294-44ff-84b0-4d5648138deb', 'f14928a7-d6a4-4ae7-8f0d-4bf686de493f', '975162a3-4ff8-4b42-8e3f-d99b1ea91ff7', '2024-12-02 23:15:32', 'dispatch', 191.5, 'Sowutuom')"