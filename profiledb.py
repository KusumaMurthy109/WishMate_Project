import pymongo

class ProfileDB:
    '''
    Creates ProfileDB class that connects to WishMate_Profiles Database.
    '''

    def __init__(self):
        '''
        Define Member Variables.
        '''
        self._client = pymongo.MongoClient("mongodb+srv://annalin260:12345@cluster0.rtdi4fq.mongodb.net/")
        self._profile_db = self._client["WishMate_Profiles"]
        self._wishlist_db = self._client["WishMate_Wishlists"]
        self.userCol = self._profile_db["Users"]

    def createAccount(self, username, password, firstname, lastname, zipcode):
        '''
        Creates an account for new users.
        '''
        #Validates that user is a new user to the database. Returns True if accounts is successfully created.
        try:
            self.userCol.insert_one({"_id": username,
                                     "First Name": firstname,
                                     "Last Name": lastname,
                                     "Zipcode": zipcode,
                                     "Password": password})
            return True
        
        except pymongo.errors.DuplicateKeyError:
            return False

    def userLogin(self, username, password):
        '''
        Validates user login.
        '''
        #Validates user's username and password upon login. Returns True if login successful.
        cursor = self.userCol.find({"_id": username, "Password": password})
        documents = list(cursor)
        if len(documents) == 0:
            return False
        
        else:
            return True
