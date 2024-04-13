import pymongo

class WishlistDB:

    def __init__(self):
        '''
        Define member variables.
        '''
        self._client = pymongo.MongoClient("mongodb+srv://annalin260:12345@cluster0.rtdi4fq.mongodb.net/")
        self._wishlist_db = self._client["WishMate_Wishlists"]
        self._profile_db = self._client["WishMate_Profiles"]
        self.profileCol = self._profile_db["Users"]
        self.useridCol = None
    
    
    def findUser(self, username):
        '''
        Validates that user has a collection in the wishlist database.
        '''
        collection = self._wishlist_db.get_collection(username)
        if collection is not None:
            return True
        else:
            return False

    def createWishlist(self, username, new_wishlist):
        '''
        Creates a new wishlist.
        '''
        if self.findUser(username):
            self.useridCol = self._wishlist_db[username]
            self.useridCol.insert_one({"_id": new_wishlist})
        
        else:
            self._wishlist_db = self._client["WishMate_Wishlists"]
            self._wishlist_db.create_collection(username)
            self.useridCol.insert_one({"_id": new_wishlist})

    #WishMate_Wishlists Database
    def addItems(self, username, existing_wishlist, items):
        if self.findUser(username):
            self.useridCol = self._wishlist_db[username]
            self.useridCol.update_one({"_id": existing_wishlist},
                                    {"$push": {"Items": {"$each": items}}})
    
    #WishMate_Wishlists Database
    def removeItem(self, username, existing_wishlist, item):
        if self.findUser(username):
            self.useridCol = self._wishlist_db[username]
            self.useridCol.update_one({"_id": existing_wishlist},
                                    {"$pull": {"Items": item}})
    
    #WishMate_Wishlists Database
    def showWishlist(self, username):
        wishlist_items = []

        # Check if the user exists in the database
        if self.findUser(username):
            # Fetch the wishlist collection for the user
            user_collection = self._wishlist_db.get_collection(username)

            # If the collection exists
            if user_collection is not None:
                # Find all documents in the collection
                for doc in user_collection.find():
                    # Get the wishlist name
                    wishlist_name = doc.get("_id")

                    # Get the items for the wishlist
                    items = doc.get("Items", [])

                    # Add each item to the wishlist_items list
                    for item in items:
                        wishlist_items.append(item)

        return wishlist_items

        '''
        self.useridCol = self._wishlist_db[username]
        if self.findUser(username):

            #Finds all wishlists that user has in the database.
            for doc in self._wishlist_db[username].find():
                wishlist_name = doc.get("_id")

                cursor = self.useridCol.find({"_id": wishlist_name})
                print(f"\n{wishlist_name}:")
                #name = wishlist_name
                #item_list = []
                for document in cursor:
                    items = document.get("Items", [])
                    for item in items:
                        print(f"- {item}")
                        #item_list.append(item)
                #item_string = ",".join(item_list)
                print('')
        '''

    #WishMate_Wishlists Database
    def wishlistNearMe(self, username):
        #Searches database to find zipcode of user.
        document = self.profileCol.find_one({"_id": username})
        myzipcode = document.get("Zipcode")
        print(f"------ Wishlists in {myzipcode} ------")

        #Searches the profile database to find users with the same zipcode, and adds their username to a list.
        users_nearme = self.profileCol.find({"Zipcode": myzipcode})
        user_list = []
        for user in users_nearme:
            user_list.append(user["_id"])

        if len(user_list) > 1:
            #Shows wishlists all users in user_list if they have a wishlist.
            wishlist_col = self._wishlist_db.list_collection_names()
            for user in user_list:
                if (user in wishlist_col) and (user != username):
                    print(f"{user}'s Wishlist ------")
                    self.showWishlist(user)

        elif (len(user_list) == 1) and (user_list[0] == username):
            print("There are no wishlists near you.")