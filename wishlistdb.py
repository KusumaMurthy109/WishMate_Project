import pymongo


class WishlistDB:
   '''
   Creates a WishlistDB class that connects to WishMate_Wishlists database.
   '''

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
       Validates that user has a collection in the wishlist database. Returns True if user is found.
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

   def addItems(self, username, existing_wishlist, items):
      '''
      Adds items to an existing wishlist.
      '''
       if self.findUser(username):
           self.useridCol = self._wishlist_db[username]
           self.useridCol.update_one({"_id": existing_wishlist},
                                   {"$push": {"Items": {"$each": items}}})
  
   def removeItem(self, username, existing_wishlist, item):
      '''
      Removes an item from an existing wishlist.
      '''
       if self.findUser(username):
           self.useridCol = self._wishlist_db[username]
           self.useridCol.update_one({"_id": existing_wishlist},
                                   {"$pull": {"Items": item}})
  
   #WishMate_Wishlists Database
   def showWishlist(self, username):
      '''
      Writes all user wishlists to a txt file.
      '''
       f = open("mywishlist.txt", "w")


       self.useridCol = self._wishlist_db[username]
       if self.findUser(username):


           #Finds all wishlists that user has in the database.
           for doc in self._wishlist_db[username].find():
               wishlist_name = doc.get("_id")


               cursor = self.useridCol.find({"_id": wishlist_name})
               f.write(f"\n{wishlist_name}:\n")
               for document in cursor:
                   items = document.get("Items", [])
                   for item in items:
                       f.write(f"- {item}\n")
               f.write("\n")

   def wishlistNearMe(self, username):
      '''
      Writes all near by wishlists (by zipcode) to a txt file.
      '''
       #Searches database to find zipcode of user.
       file = "wishlistsnearme.txt"
       f = open(file, "w")


       document = self.profileCol.find_one({"_id": username})
       myzipcode = document.get("Zipcode")
       f.write(f"------ Wishlists in {myzipcode} ------\n")


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
                   f.write(f"{user}'s Wishlist ------")
                   self.useridCol = self._wishlist_db[user]
                   if self.findUser(user):


                       #Finds all wishlists that user has in the database.
                       for doc in self._wishlist_db[user].find():
                           wishlist_name = doc.get("_id")


                           cursor = self.useridCol.find({"_id": wishlist_name})
                           f.write(f"\n{wishlist_name}:\n")
                           for document in cursor:
                               items = document.get("Items", [])
                               for item in items:
                                   f.write(f"- {item}\n")
                           f.write("\n")


       elif (len(user_list) == 1) and (user_list[0] == username):
           f.write("There are no wishlists near you.")
