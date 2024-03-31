import json
import os
import platform
from collections import defaultdict
class Restaurant:
    def __init__(self):
        self.inventory = {'stock': {}}
        self.recipes = {}
        self.usedstock = []
        self.sales=[]
        self.employees={}
        self.orders=[]
    
    def load_data(self):
        folder_path = "Files"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        try:
            with open(os.path.join(folder_path, 'Stock.txt'), 'r') as file:
                self.inventory = json.load(file)
        except FileNotFoundError:
            print("Stock File not available")

        try:
            with open(os.path.join(folder_path, 'Ingredients.txt'), 'r') as file:
                self.recipes = json.load(file)
        except FileNotFoundError:
            print("Ingredients File not available")

        try:
            with open(os.path.join(folder_path, 'Used_Stock.txt'), 'r') as s:
                self.usedstock = json.load(s)
        except FileNotFoundError:
            with open(os.path.join(folder_path, 'Used_Stock.txt'), 'w') as s:
                json.dump([], s)
                self.usedstock = []

        try:
            with open(os.path.join(folder_path, 'Sales.txt'), 'r') as f:
                self.sales = json.load(f)
        except FileNotFoundError:
            self.sales = []

        try:
            with open(os.path.join(folder_path, 'employee.txt'), 'r') as e:
                self.employees = json.load(e)
        except FileNotFoundError:
            self.employees = {}
    
    def save_data(self):
        folder_path = "Files"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        with open(os.path.join(folder_path, 'Stock.txt'), 'w') as file:
            json.dump(self.inventory, file)

        with open(os.path.join(folder_path, 'Ingredients.txt'), 'w') as file:
            json.dump(self.recipes, file)

        with open(os.path.join(folder_path, 'Used_Stock.txt'), 'w') as f:
            json.dump(self.usedstock, f)

        with open(os.path.join(folder_path, 'sales.txt'), 'w') as s:
            json.dump(self.sales, s)

        with open(os.path.join(folder_path, 'employee.txt'), 'w') as e:
            json.dump(self.employees, e)
    
    def add_inventory(self, item):
        quantity=self.get_integer_input("Enter the quantity: ")
        if item in self.inventory['stock']:
            self.inventory['stock'][item]["quantity"] += quantity
            print(f"The {item} updated by quantity {quantity}")
        else:
            pricepg = self.get_float_input("Enter price per grams: ")
            self.inventory['stock'][item] = {
                "quantity": quantity,
                "unit": "grams",
                "price_per_grams": pricepg
            }
            print(f"The {item} added by quantity of {quantity}")
        self.save_data()
    
    def remove_inventory(self, ingredients_list, quantity):
        for ingredient_data in ingredients_list:
            ingredient = ingredient_data['name']
            ingredient_quantity = ingredient_data['quantity']
            if ingredient in self.inventory['stock'] and self.inventory['stock'][ingredient]["quantity"] >= float(ingredient_quantity) * quantity:
                self.inventory['stock'][ingredient]["quantity"] -= float(ingredient_quantity) * quantity
                found = False
                for item1 in self.usedstock:
                    if item1['name'] == ingredient:
                        item1['quantity_used'] += float(ingredient_quantity) * quantity
                        found = True
                        break
                if not found:
                    self.usedstock.append({
                        "name": ingredient,
                        "quantity_used": float(ingredient_quantity) * quantity,
                        "unit": self.inventory['stock'][ingredient]["unit"]
                    })
            elif ingredient in self.inventory['stock'] and self.inventory['stock'][ingredient]["quantity"] < float(ingredient_quantity) * quantity:
                print(f"The available stock for {ingredient} is {self.inventory['stock'][ingredient]['quantity']} whereas required is {float(ingredient_quantity) * quantity} ")
                return 0
            else:
                print(f"There is no stock for {ingredient}")
                return 0
        self.save_data()
    
    def delete_inventory(self):
        while True:
            item=input("Enter the name to remove stock: ").lower()
            if item in self.inventory['stock']:
                self.inventory['stock'].pop(item)
                print(f"The {item} has been removed from Stock.")
                break
            elif item =='b':
                break
            else:
                print(f"No {item} found")
                print("Press b to go back!")
        self.clear_screen()
        self.save_data()

    def display_menu(self, item):
        if item in self.recipes['menu']:
            print(f"{item.capitalize()} Menu:")
            for i, menu_item in enumerate(self.recipes['menu'][item], 1):
                print(f"{i}: {menu_item['name']} PKR {menu_item['price']}")
            while True:
                choice = self.get_integer_input("Enter your choice or 0 to go back: ")
                if 1 <= choice <= len(self.recipes['menu'][item]):
                    selected_item = self.recipes['menu'][item][choice - 1]
                    if 'ingredients' in selected_item:
                        return selected_item['name'], selected_item['price'], selected_item['ingredients']
                    else:
                        return selected_item['name'], selected_item['price'], {}
                elif choice==0:
                    self.clear_screen()
                    return None,None,None
                
                else:
                    print("Invalid size choice.")
        else:
            print("Item not found in the menu.")
            return None, None, None
    
    def add_recipe(self, item):
        if item in self.recipes['menu']:
            print(f"Recipe for {item} already exists.")
        else:
            new_recipe = []
            num_variations = self.get_integer_input(f"Enter the number of variations for {item}: ")
            for _ in range(num_variations):
                size = input("Enter the size (small,medium,large): ")
                price = self.get_integer_input(f"Enter price of {item} for {size}: ")
                no_of_ingredients = self.get_integer_input("Enter the number of ingredients: ")
                ingredients = []
                for i in range(1,no_of_ingredients+1):
                    ingredient_name = input(f"Enter {i} name of ingredient: ")
                    ingredient_quantity = self.get_float_input(f"Enter quantity of {ingredient_name}: ")
                    ingredient_unit = input(f"Enter unit of {ingredient_name}: ")
                    ingredients.append({
                        "name": ingredient_name,
                        "quantity": ingredient_quantity,
                        "unit": ingredient_unit,
                    })
                new_recipe.append({
                    "name": size,
                    "price": price,
                    "ingredients": ingredients
                })
            self.recipes['menu'][item] = new_recipe
            print(f"Recipe Added for {item} having Variations: {num_variations} Successfully!")
            self.save_data()
    
    def remove_recipe(self,item):
        if item in self.recipes['menu']:
            self.recipes['menu'].pop(item)
            print(f"Recipe for {item} Deleted Sucessfully")
        else:
            print(f"Recipe does not exsit for {item}")
        self.save_data()
    
    def change_recipe(self, item):
        if item not in self.recipes['menu']:
            print(f"Recipe for {item} does not exist.")
            return
        print(f"Available Sizes for {item}:")
        for i, size_info in enumerate(self.recipes['menu'][item], 1):
            print(f"{i}: {size_info['name']} - PKR {size_info['price']}")
        while True:
            size_choice = self.get_integer_input("Enter the number of the size you want to modify: ")
            if size_choice < 1 or size_choice > len(self.recipes['menu'][item]):
                print("Invalid size choice.")
            else:
                break
        current_recipe = self.recipes['menu'][item][size_choice - 1]
        print(f"\nCurrent Ingredients for {current_recipe['name']} {item}:")
        for i, ingredient in enumerate(current_recipe['ingredients'], 1):
            print(f"{i}: {ingredient['name']} - {ingredient['quantity']} {ingredient['unit']}")
        while True:
            ingredient_choice = self.get_integer_input("Enter the number of the ingredient you want to modify (or 0 to exit): ")
            if ingredient_choice == 0:
                break
            elif ingredient_choice < 1 or ingredient_choice > len(current_recipe['ingredients']):
                print("Invalid choice.")
            else:
                break
        selected_ingredient = current_recipe['ingredients'][ingredient_choice - 1]
        new_quantity = self.get_float_input(f"Enter new quantity for {selected_ingredient['name']}: ")
        selected_ingredient['quantity'] = new_quantity
        print(f"Ingredients for {item} {size_info['name']} updated Successfully.")
        self.save_data()
    
    def change_price(self, item):
        if item not in self.recipes['menu']:
            print(f"{item} does not exist.")
            return
        print(f"Available Sizes for {item}:")
        for i, size_info in enumerate(self.recipes['menu'][item], 1):
            print(f"{i}: {size_info['name']} - PKR {size_info['price']}")
        print("0: Go back")
        while True:
            size_choice = self.get_integer_input("Enter the number of the size you want to change the price for: ")
            if size_choice == 0:
                self.clear_screen()
                return
            elif size_choice < 1 or size_choice > len(self.recipes['menu'][item]):
                print("Invalid size choice.")
            else:
                break
        current_recipe = self.recipes['menu'][item][size_choice - 1]
        print(f"\nCurrent price for {current_recipe['name']} {item}: PKR {current_recipe['price']}")
        new_price = self.get_integer_input("Enter the new price: ")
        current_recipe['price'] = new_price
        print(f"Price for {item} {size_info['name']} updated successfully.")
        self.save_data()   
    
    def order(self, item, quantity,product,orders):
        if item and quantity:
            for menu_item in self.recipes['menu'][product]:
                if menu_item['name'] == item:
                    total_price = menu_item['price'] * quantity
                    if self.remove_inventory(menu_item['ingredients'], quantity)!=0:
                        self.sales.append((product, item, quantity, total_price))
                        self.save_data()
                        print(f"You have added {quantity} {item} {product}.")  
                        orders.append((product, item,quantity, total_price))
                    break
        else:
            print("Invalid order.")
  
    def print_order(self,orders):
        print("Item-----------------------Quanity--------------------Price (PKR)")
        order_summary = {}
        for name, size, quantity, price in orders:
            item = f"{name} {size}"
            if item in order_summary:
                order_summary[item]['quantity'] += quantity
                order_summary[item]['price'] += price
            else:
                order_summary[item] = {'quantity': quantity, 'price': price}
        for item, summary in order_summary.items():
            print(f"{item:<30}{summary['quantity']:<28}{summary['price']:<10}")
        total=0
        for i,j,k,l in orders:
            total+=l
        print(f"\nTotal Price to Pay: {total}")
    
    def calculate_unit(self, item, size):
        for menu_item in self.recipes["menu"][item]:
            if menu_item["name"] == size:
                total_cost = 0
                sell_cost = menu_item["price"]
                for ingredient in menu_item["ingredients"]:
                    ingredient_name = ingredient["name"]
                    ingredient_quantity = float(ingredient["quantity"])
                    price_per_unit = self.inventory["stock"][ingredient_name]["price_per_grams"]
                    total_cost += ingredient_quantity * price_per_unit        
                print(f"The total cost for making a {item} {size} is {total_cost} and its selling price is {sell_cost}")
                while True:
                    user=input("Press b to go back: ").lower()
                    if user=="b":
                        print("Going Back")
                        break
                    else:
                        print("Wrong input")
            
    def profit_loss(self):
        total_cost=0
        for item in self.usedstock:
            name = item['name']
            quantity_used =float( item['quantity_used'])
            price_per_gram = float(self.inventory['stock'][name]['price_per_grams'])
            total_cost += quantity_used * price_per_gram
        other_expenses=self.get_integer_input("Enter other expenses: ")
        total_items = 0
        total_amount = 0
        for item in self.sales:
            total_items += item[2] 
            total_amount += item[3]
        total_pay=0
        for pay in self.employees.values():
            total_pay += int(pay["pay"])
        new=total_cost+other_expenses+total_pay
        net=total_amount-new
        print("Summary of Expenses:")
        print(f"Total items used in stock: {total_items}   Total cost: {total_cost:<25,.2f}")
        print(f"Other expenses: {other_expenses:<28,.2f}")
        print(f"Total pay given to employees: {total_pay:<14,.2f}")
        print(f"Total Expenses: {new:<25,.2f}")
        print(f"Total Sales: {total_amount:<28,.2f}")
        print(f"Net: {net:<36,.2f}")

        while True:
            user=input("Press b to go back: ").lower()
            if user=="b":
                print("Going Back")
                break
            else:
                print("Wrong input")
    
    def display_available_items(self):
        print("Available Categories:")
        index = 1
        category_map = {}
        for category in self.recipes['menu'].keys():
            print(f"{index}-{category.capitalize()}")
            category_map[index] = category
            index += 1
        
        while True:
            choice = self.get_integer_input("Enter your choice or 0 to go back: ")
            if choice == 0:
                break
            elif choice in category_map:
                return category_map[choice]
            else:
                print("Invalid choice. Please enter a valid category number.")
        
    def create_account(self):
        while True:
            username = input("Enter username for new account: ")
            if username in self.employees:
                print(f"Account with username '{username}' already exists")
            else:
                roles = {1: "Waiter", 2: "Admin",3: "Chef"}
                print("Available Roles:")
                for number, role in roles.items():
                    print(f"{number}-{role}")
                role_choice = self.get_integer_input(f"Enter the number corresponding to the role for user '{username}': ")
                if role_choice in roles:
                    role = roles[role_choice]
                    password = input("Enter password: ")
                    pay = self.get_integer_input("Enter pay: ")
                    self.employees[username] = {"role": role, "pay": pay, "password": password}
                    print(f"Account of '{username}' created successfully with role '{role}'!")
                    self.save_data()
                    break 
                else:
                    print("Wrong Input")
            print("Invalid role choice or input. Account creation failed.")
    
    def login(self, username, password):
        if username in self.employees:
            if self.employees[username]["password"] == password:
                print(f"Login successful! \nWelcome, {username}.")
                role=self.employees[username]["role"]
                if role == "Waiter":
                    return Waiter(username, role, self.employees[username]["pay"], password)
                elif role == "Admin":
                    return Admin(username, role, self.employees[username]["pay"], password)
                elif role == "Chef":
                    return Chef(username, role, self.employees[username]["pay"], password)
            else:
                print("Incorrect password. Please try again.")
        else:
            print("User not found. Please check the username.")
    
    def get_integer_input(self,prompt):
        while True:
            user_input = input(prompt)
            if user_input.isdigit():
                return int(user_input)
            else:
                print("Invalid input. Please enter an integer.")
    
    def get_float_input(self,prompt):
       while True:
        user_input = input(prompt)
        try:
            numeric_value = float(user_input) 
            return numeric_value
        except ValueError:
            print("Invalid input. Please enter a valid number.") 
    
    def change_password(self, username, old_password):
        self.clear_screen()
        if username in self.employees:
            if self.employees[username]['password'] == old_password:
                new_password=input("Enter new password: ")
                self.employees[username]['password'] = new_password
                print("Password changed successfully!")
            else:
                print("Incorrect old password. Password change failed.")
        else:
            print(f"User {username} not found. Password change failed.")
        self.save_data()
    
    def display_orders(self):
        item_totals = defaultdict(lambda: [0, 0])
        for order in self.sales:
            item_name, size, quantity, price = order
            item_totals[(item_name, size)][0] += quantity
            item_totals[(item_name, size)][1] += price

        total_q=0
        total_p=0
        print("Item\t\tSize\t\tQuantity\tPrice(PKR)")
        for (item_name, size), (total_quantity, total_price) in item_totals.items():
            total_q+=total_quantity
            total_p+=total_price
            print(f"{item_name:<15}{size:<20}{total_quantity:<15}{total_price:<10}")
        print(f"Total Quantity: {total_q} Total Price: {total_p}")
        while True:
            user=input("Press b to go back: ").lower()
            if user=="b":
                print("Going Back")
                self.clear_screen()
                return
            else:
                print("Wrong input")
    
    def clear_screen(self):
        os.system('cls' if platform.system() == 'Windows' else 'clear')
    
    def display_inventory(self):
        self.clear_screen()
        print("Current Inventory:")
        while True:
            print("Item                 Quantity               Price(PKR)")
            for item, details in self.inventory['stock'].items():
                quantity = f"{details['quantity']:.1f} {details['unit']}"
                price = f"{details['price_per_grams']:.2f} per {details['unit']}"
                print(f"{item.capitalize():<20} {quantity:<20} {price:<20}")
            user=input("Press b to go back: ").lower()
            if user=='b':
                self.clear_screen()
                break
            else:
                print("Wrong Input")

    def delete_employee(self,username1):
        while True:
            username = input("Enter the username of the employee you want to delete or Press b to go back: ")
            if username in self.employees and self.employees[username]["role"]=="Admin" and username==username1:
                print(f"{username} can not delete his own account.")
            elif username in self.employees:
                del self.employees[username]
                print(f"The employee '{username}' has been successfully deleted.")
                self.save_data()  
                break
            elif username=='b' or username=='B':
                self.clear_screen()
                break
            else:
                print(f"The employee '{username}' was not found.")
                
    def update_price_per_grams(self):
        while True:
            ingredient_name = input("Enter the name of the ingredient you want to update or b to go back: ").lower()
            if ingredient_name in self.inventory['stock']:
                new_price_per_grams = self.get_float_input(f"Enter the new price per grams for {ingredient_name}: ")
                self.inventory['stock'][ingredient_name]["price_per_grams"] = new_price_per_grams
                print(f"Price per grams for {ingredient_name} updated successfully.")
            elif ingredient_name=='b':
                break
            else:
                print(f"Ingredient {ingredient_name} not found in the stock.")
        
class Employee:
    def __init__(self,username,role,pay,password):
        self.username=username
        self.role=role
        self.pay=pay
        self.password=password
        
    def display_detials(self):
        print("Name: ",self.username)
        print("Role: ",self.role)
        print("Pay: PKR",self.pay)
        print("Password: ",self.password)

class Admin(Employee):
    def __init__(self, name,role,pay,password):
        super().__init__(name,role,pay,password)
    def display_detials(self):
        return super().display_detials()

    def AddStock(self,inventory):
        restaurant.add_inventory(inventory)
    def DeleteStock(self):
        restaurant.delete_inventory()
    def ProfitLoss(self):
        restaurant.profit_loss()
    def SalesRecord(self):
        restaurant.display_orders()
    def CreateAccount(self):
        restaurant.create_account()
    def DeleteAccount(self,account):
        restaurant.delete_employee(account)
    def StockPriceUpdate(self):
        restaurant.update_price_per_grams()
    def ChangeItemPrice(self,item):
        restaurant.change_price(item)
    def CalculateUnitPrice(self,item,subitem):
        restaurant.calculate_unit(item,subitem)

    def disp_funct(self):
        while True:
            print("----------Admin Menu------------")
            print("1-Personal Details")
            print("2-Change Password")
            print("3-Add Stock")
            print("4-Delete Stock")
            print("5-Show Stock")
            print("6-Change Price of Product")
            print("7-Unit Price of a Item")
            print("8-Change Price of a Ingredient")
            print("9-Profit Loss")
            print("10-Check Sales Record")
            print("11-Create Account for Workers")
            print("12-Delete Account for Workers")
            print("13-Exit")
            choice = restaurant.get_integer_input("Enter your choice: ")
            if choice == 13:
                restaurant.clear_screen()
                print(f"Logged Out as {self.username}")
                break
            elif choice==1:
                restaurant.clear_screen()
                self.display_detials() 
                if restaurant.get_integer_input("Press 0 to go back: ") == 0:
                    restaurant.clear_screen()
                    continue 
            elif choice == 2:
                restaurant.change_password(self.username,self.password)
                
            elif choice ==3:
                restaurant.clear_screen()
                user=input("Enter the name to add stock: ").lower()
                self.AddStock(user)
            elif choice==4:
                restaurant.clear_screen()
                self.DeleteStock()
            elif choice==5:
                restaurant.clear_screen()
                restaurant.display_inventory()
                restaurant.clear_screen()
            elif choice==6:
                restaurant.clear_screen()
                a=restaurant.display_available_items()
                restaurant.clear_screen()
                if self.ChangeItemPrice(a) == 0:
                    restaurant.clear_screen()
                    continue 
            elif choice==7:
                restaurant.clear_screen()
                a=restaurant.display_available_items()
                if a is None:
                    break
                restaurant.clear_screen()
                b,c,d=restaurant.display_menu(a)
                self.CalculateUnitPrice(a,b)
                restaurant.clear_screen()
            elif choice==8:
                restaurant.clear_screen()
                self.StockPriceUpdate()
            elif choice==9:
                restaurant.clear_screen()
                self.ProfitLoss()
                restaurant.clear_screen()
            elif choice==10:
                restaurant.clear_screen()
                self.SalesRecord()
                restaurant.clear_screen()
            elif choice==11:
                restaurant.clear_screen()
                self.CreateAccount()
            elif choice==12:
                restaurant.clear_screen()
                self.DeleteAccount(self.username)

class Waiter(Employee):
    def __init__(self, name, role, pay, password):
        super().__init__(name, role, pay, password)
    def display_detials(self):
        return super().display_detials()
    
    def disp_funct(self):
        while True:
            print("----------Waiter Menu----------")
            print("1-Personal Details")
            print("2-Display Menu to Take Order")
            print("3-Change Password")
            print("4-Exit")
            choice = restaurant.get_integer_input("Enter your choice: ")
            if choice == 4:
                restaurant.clear_screen()
                print(f"Logged Out as {self.username}")
                break
            elif choice==1:
                restaurant.clear_screen()
                self.display_detials() 
                if restaurant.get_integer_input("Press 0 to go back: ") == 0:
                    restaurant.clear_screen()
                    continue    
            elif choice == 2:
                restaurant.clear_screen()
                while True:
                    cat=restaurant.display_available_items()
                    restaurant.clear_screen()
                    if cat is None: 
                        break
                    a,b,c=restaurant.display_menu(cat)
                    if a and b and c:
                        quantity = int(input("Enter the quantity: "))
                        restaurant.order(a, quantity,cat,orders)
                        add_more = input("Would you like to add more items? (y/n): ").lower()
                        if add_more != 'y':
                            restaurant.clear_screen()
                            restaurant.print_order(orders)
                            User_int=input("0=back and e=Main Menu:").lower()
                            if User_int=="0":
                                continue
                            elif User_int=='e':
                                break
                            else:
                                print("Wrong Input!")
                        else:
                            restaurant.clear_screen()
            elif choice == 3:
                restaurant.change_password(self.username,self.password)
                restaurant.clear_screen()
            else:
                print("Error! Invalid choice.")
    
class Chef(Employee):
    def __init__(self, username, role, pay, password):
        super().__init__(username, role, pay, password)
    def display_detials(self):
        return super().display_detials()
    def AddRecipe(self,item):
        restaurant.add_recipe(item)
    def RemoveRecipe(self,item):
        restaurant.remove_recipe(item)
    def ChangeRecipe(self,item):
        restaurant.change_recipe(item)
    def disp_funct(self):
        while True:
            print("---------Chef Menu-----------")
            print("1-Personal Details")
            print("2-Change Password")
            print("3-Add Recipe")
            print("4-Remove Recipe")
            print("5-Change Recipe")
            print("6-Exit")
            choice = restaurant.get_integer_input("Enter your choice: ")
            if choice == 6:
                restaurant.clear_screen()
                print(f"Logged Out as {self.username}")
                break
            elif choice==1:
                restaurant.clear_screen()
                self.display_detials() 
                if restaurant.get_integer_input("Press 0 to go back: ") == 0:
                    restaurant.clear_screen()
                    continue    
            elif choice == 2:
                restaurant.change_password(self.username,self.password)
                restaurant.clear_screen()
            elif choice==3:
                restaurant.clear_screen()
                user_val=input("Enter name of recipe that you want to add: ").capitalize()
                self.AddRecipe(user_val)
            elif choice==4:
                restaurant.clear_screen()
                cat=restaurant.display_available_items()
                self.RemoveRecipe(cat)
            elif choice==5:
                restaurant.clear_screen()
                cat=restaurant.display_available_items()
                self.ChangeRecipe(cat)
            else:
                print("Invalid Input!")
    

restaurant = Restaurant()
restaurant.load_data()
orders=[]