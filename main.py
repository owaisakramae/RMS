from RMS import Restaurant
restaurant = Restaurant()
restaurant.load_data()
print("---------- Welcome To Restaurant Management System ----------")
while True:
    print("1-Admin")
    print("2-Chef")
    print("3-Waiter")
    print("4-Exit")
    choice = restaurant.get_integer_input("Enter your choice: ")
    if choice == 1:
        restaurant.clear_screen()
        while True:
            username = input("Enter Admin username: ")
            password = input("Enter Admin password: ")
            restaurant.clear_screen()
            admin = restaurant.login(username, password)
            if admin is not None:
                admin.disp_funct()
                break
            else:
                print("Please try again.")
    elif choice == 2:
        restaurant.clear_screen()
        while True:
            username = input("Enter Chef username: ")
            password = input("Enter Chef password: ")
            restaurant.clear_screen()
            chef = restaurant.login(username, password)
            if chef is not None:
                chef.disp_funct()
                break  
            else:
                print("Please try again.")
    elif choice == 3:
        restaurant.clear_screen()
        while True:
            username = input("Enter Waiter username: ")
            password = input("Enter Waiter password: ")
            restaurant.clear_screen()
            waiter = restaurant.login(username, password)
            if waiter is not None:
                waiter.disp_funct()
                break
            else:
                print("Please try again.")
    elif choice== 4:
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please enter a valid option.")