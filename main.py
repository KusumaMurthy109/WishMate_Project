import pymongo
from bson import ObjectId
from profiledb import ProfileDB
from wishlistdb import WishlistDB 

def main():
    profile_db = ProfileDB()
    wishlist_db = WishlistDB()

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

            if profile_db.createAccount(username, password, firstname, lastname, zipcode):
                x = False
                print(f"Hi {firstname}! Your profile has been created.")
            
            else:
                print("Username Taken. Try Again.")

    elif user_input == "E":
        y = True
        while y:
            username = input("\nEnter Username: ")
            password = input("Enter Password: ")
        
            if profile_db.userLogin(username, password):
                y = False
                print("Login in Successful.")
        
            else:
                print("Invalid Username and/or Password. Try Again")

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
            wishlist_db.createWishlist(username, new_wishlist)

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
            
            wishlist_db.addItems(username, existing_wishlist, items)
        
        #Removes item from existing wishlist.
        elif user_choice == 3:
            existing_wishlist = input("Existing Wishlist: ")
            remove_item = input("Item to Remove: ")
            wishlist_db.removeItem(username, existing_wishlist, remove_item)

        #Prints existing wishlist.
        elif user_choice == 4:
            existing_wishlist = input("Existing Wishlist: ")
            wishlist_db.showWishlist(username, existing_wishlist)
        
        #Find public wishlists in the same area.
        elif user_choice == 5:
            collection_name = "Users"
            collection = profile_db.get_collection("Users")
            document_id = ObjectId(username)
            document = collection.find_one({"_id": document_id})
            zipcode = document.get({"Zipcode"})
            print(zipcode)

        #Exists program.
        elif user_choice == 6:
            check = False
            print("Exiting WishMate ... :)")
    
        #Invalid inputs.
        else:
            print("Invalid input. Please try again :)\n")

if __name__ == "__main__":
    main()