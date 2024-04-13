import pymongo

'''
Adding to Database and User Input
'''
myclient = pymongo.MongoClient("mongodb+srv://annalin260:12345@cluster0.rtdi4fq.mongodb.net/")

mydb = myclient["WishMate"]
user_col = mydb["Users"] #contains collection of users
wishlist_col = mydb["Wishlists"] #contains collection of wishlists (not user specific)

print("\nWelcome to WishMate! ------")
user_input = input("Existing or New User: ") #inputs either E or N

#Asks new users to create a profile.
if user_input == "N":
    x = True
    while x:
        #Profile info
        print("\nCreate Your Profile ------")
        username = input("Username: ")
        password = input("Password: ")
        firstname = input("First Name: ")
        lastname = input("Last Name: ")
        zipcode = int(input("ZipCode: "))

        #Adds new user to the User Collection after ensuring username hasn't been taken.
        try:
            user_col.insert_one({"_id": username, 
                                "First Name": firstname,
                                "Last Name": lastname,
                                "Zipcode": zipcode,
                                "Password": password})
            print(f"Hi {firstname}! Your profile is created.\n")
            x = False
        #If username is taken, user needs to try again.
        except:
            print("Username Taken. Try Again.")

#Login for exiting users.
elif user_input == "E":
    y = True
    while y:
        username = input("\nEnter Username: ")
        password = input("Enter Password: ")
        cursor = user_col.find({"_id": username, "Password": password})
        #Validates username and password.
        documents = list(cursor)
        if len(documents) == 0:
            print("Username and/or Password Incorrect. Try Again.")
        else:
            y = False
    
check = True
while check:

    print("\nChoice ------ ")
    print("1. Create New Wishlist")
    print("2. Add to Existing Wishlist")
    print("3. Remove Item from Existing Wishlist")
    print("4. Show My Wishlist")
    print("5. Show Wishlists Near Me")
    print("6. Exit Program\n")

    user_choice = int(input("Enter choice: "))

    #Creates new wishlist.
    if user_choice == 1:
        new_wishlist = input("New Wishlist: ")
        wishlist_col.insert_one({"_id": username,
                                "Wishlist": new_wishlist,})
    
    #Adds item to existing wishlist.
    elif user_choice == 2:
        existing_wishlist = input("Existing Wishlist: ")
        items = []
        print("Items to Add (Enter Twice to Finish):")
        while True:
            item = input()
            if item == "":
                break
            items.append(item)
        wishlist_col.update_one({"_id": username,"Wishlist": existing_wishlist},
                            {"$push": {"Items": {"$each": items}}}) 

    #Removes item from existing wishlist.
    elif user_choice == 3:
        existing_wishlist = input("Existing Wishlist: ")
        remove_item = input("Item to Remove: ")
        wishlist_col.update_one({"_id": username,"Wishlist": existing_wishlist},
                            {"$pull": {"Items": remove_item}})
    
    #Prints existing wishlist.
    elif user_choice == 4:
        existing_wishlist = input("Existing Wishlist: ")
        cursor = wishlist_col.find({"_id": username, "Wishlist": existing_wishlist})
        print(f"\n{existing_wishlist}:")
        for document in cursor:
            items = document.get("Items", [])
            for item in items:
                print(f"- {item}")
        print('')

    elif user_choice == 5:
        neigh_user = user_col.find({})

    #Exists program.
    elif user_choice == 6:
        check = False
        print("Exiting WishMate ... :)")
    
    #Invalid inputs.
    else:
        print("Invalid input. Please try again :)\n")