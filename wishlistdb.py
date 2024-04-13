import pymongo

class WishlistDB:

    def __init__(self):
        '''
        Define member variables.
        '''
        self._client = pymongo.MongoClient("mongodb+srv://annalin260:12345@cluster0.rtdi4fq.mongodb.net/")
        self._wishlist_db = self._client["WishMate_Wishlists"]
        self._profiledb = self._client["WishMate_Profiles"]
        self.userCol = None
    
    
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
            self.userCol = self._wishlist_db[username]
            self.userCol.insert_one({"_id": new_wishlist})
        
        else:
            self._wishlist_db = self._client["WishMate_Wishlists"]
            self._wishlist_db.create_collection(username)
            self.userCol.insert_one({"_id": new_wishlist})

    #WishMate_Wishlists Database
    def addItems(self, username, existing_wishlist, items):
        if self.findUser(username):
            self.userCol.update_one({"_id": existing_wishlist},
                                {"$push": {"Items": {"$each": items}}})
        
    
    #WishMate_Wishlists Database
    def removeItem(self, username, existing_wishlist, item):
        if self.findUser(username):
            self.userCol.update_one({"_id": existing_wishlist},
                                {"$pull": {"Items": item}})
    
    #WishMate_Wishlists Database
    def showWishlist(self, username, existing_wishlist):
        if self.findUser(username):
            cursor = self.userCol.find({"_id": existing_wishlist})
            print(f"\n{existing_wishlist}:")
            for document in cursor:
                items = document.get("Items", [])
                for item in items:
                    print(f"- {item}")
            print('')

    #WishMate_Wishlists Database
    def wishlistNearMe(self, zipcode):
        pass