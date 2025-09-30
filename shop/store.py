import sqlite3 
conn = sqlite3.connect("shoping.db")
cursor = conn.cursor()




cursor.execute ('''CREATE TABLE IF NOT EXISTS products (
                    product_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price REAL NOT NULL)''')

cursor.execute ('''CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE)''' )

cursor.execute ('''CREATE TABLE IF NOT EXISTS orders ( 
                order_id INTEGER PRIMARY KEY, 
                customer_id INTEGER NOT NULL, 
                product_id INTEGER NOT NULL, 
                quantity INTEGER NOT NULL, 
                order_date DATE NOT NULL, 
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id), 
                FOREIGN KEY (product_id) REFERENCES products(product_id) )''')

while True:
    print("1 Додавання продуктів")
    print("2 Додавання продуктів")
    print("3 Замовлення товарів")
    print("4 Сумарний обсяг продажів:")
    print("5 Кількість замовлень на кожного клієнта:")
    print("6 Середній чек замовлення:")
    print("7 Найбільш популярна категорія товарів")
    print("8 загальна кількість товарів кожної категорії")
    print("9 Оновлення цін")
    print("10 Створення Python скрипта для виконання SQL-запитів")

    shop = input()
    if shop == "1":
        name = input("Введіть назву")
        category = input("Введіть категорію")
        price = float(input("Введіть ціну"))
        cursor.execute("INSERT INTO products(name,category,price) VALUES (?,?,?)", (name,category,price))
        conn.commit()

    elif shop == "2":
        first_name = input("Введіть Імя")
        last_name = input("Введіть прізвище")
        email = input("Введіть емейл")
        cursor.execute("INSERT INTO customers(first_name,last_name,email) VALUES(?,?,?)", (first_name,last_name,email))
        conn.commit()
    
    elif shop =="3":
        customer_id = int(input("Введіть ід покупця"))
        product_id = int(input("Введіть ід продукту"))
        quantity = int(input("Кількість"))
        order_date = input("рік/місяць/день")
        cursor.execute("INSERT INTO orders(customer_id,product_id,quantity,order_date) VALUES (?,?,?,?)", (customer_id,product_id,quantity,order_date))
        conn.commit()
    elif shop =="4":
        cursor.execute('''SELECT SUM(orders.quantity * products.price)
                       AS total_sales
                       FROM orders
                       JOIN products ON orders.product_id = products.product_id''')
        total_sales = cursor.fetchone()[0]
        print(f"обсяг продажів {total_sales}")
        conn.commit()
    elif shop=="5":
        cursor.execute('''SELECT customers.first_name, customers.last_name, COUNT(orders.order_id)
                       FROM customers
                       INNER JOIN orders ON customers.customer_id = orders.customer_id
                       GROUP BY customers.customer_id,customers.first_name,customers.last_name''')
        results = cursor.fetchall()
        for cust in results:
            print(f"Клієнт{cust[0]} {cust[1]} кількість замовлень {cust[2]}")
        conn.commit()
    elif shop == "6":
        cursor.execute('''SELECT AVG (orders.quantity * products.price) AS av_order
                       FROM orders
                       INNER JOIN products ON orders.product_id = products.product_id''')
        av_order = cursor.fetchone()[0]
        print(f"Середній чек {round(av_order,2)}")
        conn.commit()
    elif shop == "7":
        cursor.execute('''SELECT products.category, COUNT(order_id) AS order_count
                       FROM products
                       JOIN orders ON products.product_id = orders.product_id
                       GROUP BY products.category
                       ORDER BY order_count DESC
                       LIMIT 1''')
        prod_category = cursor.fetchone()
        if prod_category:
            print(f"Найбільш популярна категорія {prod_category[0]} з кількістю замовлень {prod_category[1]}")
        else:
            print("Немає даних")
        conn.commit()
    elif shop=="10":
        break
    
    elif shop =="8":
        cursor.execute('''SELECT category, COUNT(*) AS pr_count
                       FROM products
                       GROUP BY category''')
        categ=cursor.fetchall()
        if categ:
            for c in categ:
                print(f"Категорія {c[0]} Кількість товару {c[1]}")
        else:
            print("Немає продуктів")
        conn.commit()
    elif shop=="9":
        product_id = int(input("Введіть ід продукту"))
        new_price = float(input("Введіть ціну"))
        cursor.execute('''UPDATE products SET price = ? WHERE product_id = ?''', (new_price,product_id))
        if cursor.rowcount > 0:
            print(f"Ціна для продукту {product_id} оновлена до {new_price}")
        else:
            print(f"Продукт {product_id} не знайдено")
        conn.commit()
conn.close()