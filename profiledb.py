import pymongo

class ProfileDB:

    def __init__(self):
        self._client = pymongo.MongoClient("mongodb+srv://annalin260:12345@cluster0.rtdi4fq.mongodb.net/")
        self._profile_db = self._client["WishMate_Profiles"]
        self._wishlist_db = self._client["WishMate_Wishlists"]
        self.userCol = self._profile_db["Users"]

    #WishMate_Profiles Database
    def createAccount(self, username, password, firstname, lastname, zipcode):
        try:
            self.userCol.insert_one({"_id": username,
                                     "First Name": firstname,
                                     "Last Name": lastname,
                                     "Zipcode": zipcode,
                                     "Password": password})
            return True
        
        except pymongo.errors.DuplicateKeyError:
            return False

    #WishMate_Profiles Database
    def userLogin(self, username, password):
        cursor = self.userCol.find({"_id": username, "Password": password})
        documents = list(cursor)
        if len(documents) == 0:
            return False
        
        else:
            return True