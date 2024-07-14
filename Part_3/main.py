import sqlite3
db = sqlite3.connect('QHO429.db')

# ---------------------------------------------------------------------------- #
#                                    PART A                                    #
# ---------------------------------------------------------------------------- #
#A i
def welcome_shopper_id():
    #retrive data by the cursor
    cursor = db.cursor()
    #user input of shopper_id
    shopper_id = int(input("Please input your shopper ID: \n"))
    #sql shopper- getting shopper_id - defining query
    sql_shopper_id = "SELECT shopper_first_name, shopper_surname  FROM shoppers WHERE shopper_id = ?"
    #execution of the query including shopper_id inputed by Python
    cursor.execute(sql_shopper_id, (shopper_id,)) 
    #take first row from the query
    shopper_name_surname=cursor.fetchone()         
    #if shopper_id is correct with database welcome promot and return shopper_id, if not exit         
    if shopper_name_surname:
            print(f"Welcome, {shopper_name_surname[0]} {shopper_name_surname[1]}!\n")
            return shopper_id
    else:
            print("No shopper ID. Exit the program.\n\n")
            return False

#A ii
#display whole menu options
def print_menu():
    print("ORIONCO - SHOPPER MAIN MENU\n\n"
          "1. Display your order history\n"
          "2. Add an item to your basket\n"
          "3. View your basket\n"
          "4. Change the quantity of an item in your basket\n"
          "5. Remove an item from your basket\n"
          "6. Checkout\n"
          "7. Exit")

#A Option 1- Display your order history
def display_order_history(shopper_id):
    #retrive data by the cursor
    cursor = db.cursor()
    #sql query - with order history
    order_history = \
            "SELECT " \
            "op.order_id AS 'Order ID', " \
            "STRFTIME('%d-%m-%Y', o.order_date) AS 'Order Date', " \
            "p.product_description AS 'Description', " \
            "se.seller_name AS 'Seller Name', " \
            "'£' || ROUND(op.price, 2) AS 'Price', " \
            "op.quantity AS 'Qty', " \
            "op.ordered_product_status AS 'Order Status' " \
            "FROM shoppers s " \
            "INNER JOIN shopper_orders o ON s.shopper_id = o.shopper_id " \
            "INNER JOIN ordered_products op ON o.order_id = op.order_id " \
            "INNER JOIN products p ON op.product_id = p.product_id " \
            "INNER JOIN sellers se ON op.seller_id = se.seller_id " \
            "WHERE s.shopper_id = ? " \
            "ORDER BY o.order_date DESC;"
    #execution of query including shopper id
    cursor.execute(order_history, (shopper_id,))
    #execution of the query including shopper_id inputed by Python
    whole_order_history = cursor.fetchall()
    # if is any order for user print, if not return notification
    if whole_order_history: 
            table_name=("Order ID", "Order Date", "  Product Description  ", "  Seller  ", "  Price", "Qty", "Order status")
            print(table_name)
            for row in whole_order_history:
                print(row)
    else:
            print("No order placed for this costumer!")


#A iii
def shopper_basket(shopper_id):
    #retrive data by the cursor
    cursor = db.cursor()
    
    # checking if shopper basket is in database
    check_the_basket = \
        "SELECT * FROM shopper_baskets " \
        "WHERE shopper_id = ? AND DATE(basket_created_date_time) = DATE('now') " \
        "ORDER BY basket_created_date_time DESC " \
        "LIMIT 1;"
        
    # execution of the query with shopper id
    cursor.execute(check_the_basket, (shopper_id,))
    basket = cursor.fetchone()
    
    # if basket was created today
    if basket:
        print("Resuming previous basket")
    # if basket wasn't created today, create a new basket
    else:
        create_new_basket = \
            "INSERT INTO shopper_baskets (shopper_id, basket_created_date_time) " \
            "VALUES (?, DATETIME('now'));"
        # execution of the query 
        cursor.execute(create_new_basket, (shopper_id,))
        db.commit()
        print("New basket created for shopper.")
        
        # take all rows from database
        cursor.execute(check_the_basket, (shopper_id,))
        basket = cursor.fetchone()

    return basket
# ---------------------------------------------------------------------------- #
#                                    PART B                                    #
# ---------------------------------------------------------------------------- #
# -------------------- function taken from assigment brief ------------------- #
def _display_options(all_options, title, type):
    option_num = 1
    option_list = []
    print("\n", title, "\n")
    for option in all_options:
        code = option[0]
        desc = option[1]
        print("{0}.\t{1}".format(option_num, desc))
        option_num += 1
        option_list.append(code)
    selected_option = 0
    while selected_option > len(option_list) or selected_option == 0:
        prompt = "Enter the number against the " + type + " you want to choose: "
        try:
            selected_option = int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if selected_option <= 0 or selected_option > len(option_list):
            print("Invalid option. Please enter a valid number.")
    return option_list[selected_option - 1]
# ---------------------------------------------------------------------------- #
def display_categories():
    # retrieve data by the cursor
    cursor = db.cursor()
    # SQL query - with list of categories
    categories_sql = \
    "SELECT category_id, category_description "\
    "FROM categories"
    # execution of the query with categories
    cursor.execute(categories_sql)
    # take all rows from database
    all_categories = cursor.fetchall()
    #create a list of categories to display
    categories_to_display=[]
    #store categories to later on print them out
    for categories in all_categories:
        categories_to_display.append(categories)
    #sending the categories to the display_option function
    selected_category_id = _display_options(categories_to_display, "Select a Category", "category")
    return selected_category_id  

# ---------------------------------------------------------------------------- #
def display_products(selected_category_id):
    # retrieve data by the cursor
    cursor = db.cursor()
    # SQL query - with list of product description
    products_sql = \
        "SELECT product_id, product_description " \
        "FROM products " \
        "WHERE product_status = 'Available' AND category_id = ?" 


    # execution of the query with products
    cursor.execute(products_sql, (selected_category_id,))
    # take all rows from the database
    all_products = cursor.fetchall()
    # touple becouse no duplicates
    products_to_display = [(product_id, product_description) for product_id, product_description in all_products]

    # display throught the function
    selected_product_id = _display_options(products_to_display, "Select a Product", "product")
    return selected_product_id

# ---------------------------------------------------------------------------- #
def display_sellers(selected_product_id):
    # retrieve data by the cursor
    cursor = db.cursor()
    # SQL query - with distinct seller name and price
    sellers_sql = \
        "SELECT DISTINCT s.seller_id, s.seller_name, op.price "\
        "FROM sellers s "\
        "INNER JOIN ordered_products op ON s.seller_id = op.seller_id "\
        "WHERE op.product_id = ?"\

    
    # execution of the query with products and product_id in place of ?
    cursor.execute(sellers_sql, (selected_product_id,))
    # execution of all rows of the database
    all_sellers = cursor.fetchall()

    # create the list of sellers and their prices to display
    seller_price_to_display = []
    # for each row add to the list the seller_id, seller name, and price
    for seller_id, seller_name, price in all_sellers:
        seller_price_to_display.append((seller_id, f"{seller_name} - £{price:.2f}"))

    # display options and get the selected seller ID
    selected_seller_id = _display_options(seller_price_to_display, "Select a Seller", "seller")

    return selected_seller_id
# ---------------------------------------------------------------------------- #

def quantity_for_option_2(selected_product_id, selected_seller_id):
    # retrieve data by the cursor
    cursor = db.cursor()
    # SQL query to retrieve the quantity for the selected product and seller
    quantity_sql = \
        "SELECT quantity FROM ordered_products "\
        "WHERE seller_id = ? AND product_id = ?"

    # execution of the query with seller_id and product_id in place of ?
    cursor.execute(quantity_sql, (selected_seller_id, selected_product_id))

    # take all records from the query
    quantity_amount = cursor.fetchone()

    # quantity can be zero so check for it
    if quantity_amount is None or quantity_amount[0] <= 0:
        print("Product unavailable")
        return None

    # quantity is the amount from the database
    available_quantity = quantity_amount[0]

    # loop with user validation
    while True:
        quantity_input = input(f"How many do you want to buy? (available qty: {available_quantity}): ")
        try:
            # I want numeric input
            quantity = int(quantity_input)
            # smaller or equal zero
            if quantity <= 0:
                print("Choose more than 0.")
            # if quantity is bigger than current one
            elif quantity > available_quantity:
                print(f"Qty shouldn't be bigger than stock {available_quantity}.")
            else:
                break
        # typo validation
        except ValueError:
            print("Just numeric input.")
    
    return quantity
# ---------------------------------------------------------------------------- #
def adding_product_to_the_basket(shopper_id, selected_product_id, selected_seller_id, quantity): 
    # retrieve data by the cursor
    cursor = db.cursor()

    # checking basket from today
    basket = shopper_basket(shopper_id)

    # gathering basket_id 
    basket_id = basket[0]

    # SQL query to retrieve the price
    seller_price_query = \
        "SELECT price " \
        "FROM ordered_products " \
        "WHERE product_id = ? AND seller_id = ?;"
    #execution of the query + in place of ? product_id and seller_id
    cursor.execute(seller_price_query, (selected_product_id, selected_seller_id))

    # take all records from the query
    price_database = cursor.fetchone()

    # price = NULL
    if price_database is None:
        print("Price not found.")
        return

    # taking price from database
    price = price_database[0]

    # checking if item is in the basket 
    check_product_in_basket_query = \
        "SELECT quantity " \
        "FROM basket_contents " \
        "WHERE basket_id = ? AND product_id = ? AND seller_id = ?;"
    
    cursor.execute(check_product_in_basket_query, (basket_id, selected_product_id, selected_seller_id))
    existing_product = cursor.fetchone()
     # if item is in the basket add 1 more
    if existing_product:
        new_quantity = existing_product[0] + quantity
        update_quantity_query = \
            "UPDATE basket_contents " \
            "SET quantity = ? " \
            "WHERE basket_id = ? AND product_id = ? AND seller_id = ?;"
        cursor.execute(update_quantity_query, (new_quantity, basket_id, selected_product_id, selected_seller_id))
    # if item is not in the basket add new item to the basket
    else:
        insert_product_to_basket_query = \
            "INSERT INTO basket_contents (basket_id, product_id, seller_id, quantity, price) " \
            "VALUES (?, ?, ?, ?, ?);"
        cursor.execute(insert_product_to_basket_query, (basket_id, selected_product_id, selected_seller_id, quantity, price))
        print("Added to the basket.")

    db.commit()


# ---------------------------------------------------------------------------- #
def display_the_basket(shopper_id):
    # retrieve data by the cursor
    cursor = db.cursor()

    # take a current basket from shopper
    basket = shopper_basket(shopper_id)
    basket_id = basket[0]

    # SQL query which showing of basket
    basket_query = \
        "SELECT bc.product_id, p.product_description, bc.seller_id, se.seller_name, bc.quantity, bc.price " \
        "FROM basket_contents bc " \
        "INNER JOIN sellers se ON bc.seller_id = se.seller_id " \
        "INNER JOIN products p ON bc.product_id = p.product_id " \
        "WHERE bc.basket_id = ?;"
    

    # execution of the basket
    cursor.execute(basket_query, (basket_id,))

    # take all records from the query
    all_basket_data = cursor.fetchall()

    #if basket is empty -display information about empty basket
    if not all_basket_data:
        print("Your basket is empty.")
        return []

    # basket as a list from databse
    basket_list = []
    for x in all_basket_data:
        product_id, product_description, seller_id, seller_name, quantity, price = x
        basket_list.append({
            "Product ID": product_id,
            "Product Description": product_description,
            "Seller ID": seller_id,
            "Seller Name": seller_name,
            "Quantity": quantity,
            "Price": price,
        })

    # print out the basket 
    print("Basket List:")
    for y, i in enumerate(basket_list, start=1):
        print(f"{y}. {i}")

    # Total price of the products from basket 
    total_price = sum(i["Price"] * i["Quantity"] for i in basket_list)
    print("Total Price:", total_price)

    return basket_list

    
# ---------------------------------------------------------------------------- #
#                                    PART C                                    #
# ---------------------------------------------------------------------------- #
# --------------------------------- option 4 --------------------------------- #


def selected_item(basket_list):
    #check if it is only one product in basket
    if len(basket_list) == 1:
        return basket_list[0]
    #if multiple products
    else:
        #while for validation
        while True:
            try:
                #adding product in the basket
                item_to_change = int(input("Which product do you want to change? Numerical input: ")) - 1
                #if input is valid
                if item_to_change < 0 or item_to_change >= len(basket_list):
                    raise IndexError
                return basket_list[item_to_change]
            except (ValueError, IndexError):
                print("Please enter number.")

def new_quantity(selected_item):
    #validation loop
    while True:
        try:
            #new quantity of the product
            new_quantity = int(input(f"Change quantity for {selected_item['Product Description']} (Qty in basket: {selected_item['Quantity']}): "))
            #if input is valid 
            if new_quantity < 1:
                raise ValueError
            return new_quantity
        except ValueError:
            print("Please enter number.")

def update_basket_quantity(shopper_id, selected_item, new_quantity):
    # retrieve data by the cursor
    cursor = db.cursor()
    #updating quantity of the prduct, and date of the basket 
    update_quantity_query = \
        "UPDATE basket_contents "  \
        "SET quantity = ? "  \
        "WHERE basket_id = (SELECT basket_id FROM shopper_baskets WHERE shopper_id = ? AND DATE(basket_created_date_time) = DATE('now')) " \
        "AND product_id = ? AND seller_id = ?; "
    #execute the query
    cursor.execute(update_quantity_query, (new_quantity, shopper_id, selected_item['Product ID'], selected_item['Seller ID']))
    #update databse
    db.commit()
    print(f"Quantity updated for {selected_item['Product Description']}.")

def quantity_of_item_basket(shopper_id):
    #display the basket 
    basket_list = display_the_basket(shopper_id)
    if not basket_list:
        print("You have an empty basket!")



def remove_product_from_basket(shopper_id):
     # display the bakset
    basket_list = display_the_basket(shopper_id)
     #if basket is empty
    if not basket_list:
        print("Your basket is empty!")
        return


    product_to_delete = selected_item(basket_list)

    # remove the item
    while True:
        try:
            quantity_to_remove = int(input(f"How many {product_to_delete['Product Description']} do you want to remove? (Qty in basket: {product_to_delete['Quantity']}): "))
            if quantity_to_remove < 1 or quantity_to_remove > product_to_delete['Quantity']:
                print(f"Please enter number betwen 1 and {product_to_delete['Quantity']}.")
            else:
                break
        except ValueError:
            print("Just numerical input.")

    # confiramtion of the cancellation
    confirm = input(f"Are you sure you want to remove {quantity_to_remove} {product_to_delete['Product Description']} from the basket? (Y/N): ").strip().lower()
    if confirm != 'y':
        print("Deletation of the item cancelled")
        return

    # retrive data for the coursor
    cursor = db.cursor()

    # delete the item from basket
    if quantity_to_remove == product_to_delete['Quantity']:
        # SQL delete item from the basket
        remove_item_query = \
            "DELETE FROM basket_contents " \
            "WHERE basket_id = (SELECT basket_id FROM shopper_baskets WHERE shopper_id = ? AND DATE(basket_created_date_time) = DATE('now')) " \
            "AND product_id = ? AND seller_id = ?;"
        cursor.execute(remove_item_query, (shopper_id, product_to_delete['Product ID'], product_to_delete['Seller ID']))
    else:
        # reduce the item qty from a basket
        new_quantity = product_to_delete['Quantity'] - quantity_to_remove
        update_quantity_query = \
            "UPDATE basket_contents " \
            "SET quantity = ? " \
            "WHERE basket_id = (SELECT basket_id FROM shopper_baskets WHERE shopper_id = ? AND DATE(basket_created_date_time) = DATE('now')) " \
            "AND product_id = ? AND seller_id = ?;"
        cursor.execute(update_quantity_query, (new_quantity, shopper_id, product_to_delete['Product ID'], product_to_delete['Seller ID']))

    # save in databse
    db.commit()
    print(f"{quantity_to_remove} {product_to_delete['Product Description']} removed from the basket.")

    # check the basket
    display_the_basket(shopper_id)



# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
#                                    PART D                                    #
# ---------------------------------------------------------------------------- #
def generate_order_id():

    cursor = db.cursor()
    # take list last of the order_id from ordered_products
    last_order_id_query = "SELECT MAX(order_id) FROM ordered_products;"
    #execution
    cursor.execute(last_order_id_query)
    last_order_id = cursor.fetchone()[0]


    #add + 1 to order_id to generate new one for new basket and order
    order_id = last_order_id + 1

    return order_id


def check_out(shopper_id):
    #retrive data for cursor
    cursor = db.cursor()

    
    #display basket
    basket_list = display_the_basket(shopper_id)
    #if basket is empty
    if not basket_list:
            print("Your basket is empty!")
            return

    #confirmation of the checkout
    proceed = input("Do you want to proceed to checkout? (y/N): ").strip().lower()
    if proceed != 'y':
            print("Checkout canceled.")
            return

    #taking from previous table new order_id
    order_id = generate_order_id()

    #add new order in shopper_orders
    insert_order_query = \
            "INSERT INTO shopper_orders (order_id, shopper_id, order_date, order_status) " \
            "VALUES (?, ?, DATE('now'), 'Placed');"
    cursor.execute(insert_order_query, (order_id, shopper_id))

    #move basket to ordered_products
    for item in basket_list:
            insert_ordered_product_query = \
                "INSERT INTO ordered_products (order_id, product_id, seller_id, price, quantity, ordered_product_status) " \
                "VALUES (?, ?, ?, ?, ?, 'Placed');"
            cursor.execute(insert_ordered_product_query, (order_id, item['Product ID'], item['Seller ID'], item['Price'], item['Quantity']))

    #delete the baskets
    delete_basket_contents_query = \
            "DELETE FROM basket_contents " \
            "WHERE basket_id = (SELECT basket_id FROM shopper_baskets WHERE shopper_id = ? AND DATE(basket_created_date_time) = DATE('now'));"
    cursor.execute(delete_basket_contents_query, (shopper_id,))

    delete_basket_query = \
            "DELETE FROM shopper_baskets " \
            "WHERE shopper_id = ? AND DATE(basket_created_date_time) = DATE('now');"
    cursor.execute(delete_basket_query, (shopper_id,))

    #commit changes
    db.commit()
    print("Checkout completed, your order has been placed.")


# Add the new option to the choice function
def choice(choice_num, shopper_id):
    if choice_num == 1:
        display_order_history(shopper_id)
    elif choice_num == 2:
        option_nb_two(shopper_id)
    elif choice_num == 3:
        display_the_basket(shopper_id)
    elif choice_num == 4:
        option_nb_four(shopper_id)
    elif choice_num == 5:
        remove_product_from_basket(shopper_id)
    elif choice_num == 6:
        check_out(shopper_id)
    elif choice_num == 7:
        print("Exiting the program.")
        return False
    else:
        print("Please select a number between 1 and 7.")
    return True

# ---------------------------------------------------------------------------- #
#functions which operate in menu option nb 2
def option_nb_two(shopper_id):
    selected_category_id = display_categories()
    if selected_category_id:
        selected_product_id = display_products(selected_category_id)
        if selected_product_id:
            selected_seller_id = display_sellers(selected_product_id)
            if selected_seller_id:
                quantity = quantity_for_option_2(selected_product_id, selected_seller_id)
                if quantity is not None:
                    adding_product_to_the_basket(shopper_id, selected_product_id, selected_seller_id, quantity)
                    return True

# ---------------------------------------------------------------------------- #
#functions which operate in menu option nb 4
def option_nb_four(shopper_id):
    basket_list = display_the_basket(shopper_id)
    if not basket_list:
        print("You have an empty basket!")
        return
    chosen_item = selected_item(basket_list)
    new_quantity_input = new_quantity(chosen_item)
    update_basket_quantity(shopper_id, chosen_item, new_quantity_input)
    display_the_basket(shopper_id)

# ---------------------------------------------------------------------------- #
def user_choice_input():
    while True:
        user_input = input("Please select an option: ")
        try:
            return int(user_input)
        except ValueError:
            print("Just numeric input.")

def main():
    shopper_id = welcome_shopper_id()  
    while shopper_id:
            print_menu()  
            user_choice = user_choice_input()
            if user_choice is not None and not choice(user_choice, shopper_id):
                break

if __name__ == "__main__":
    main()