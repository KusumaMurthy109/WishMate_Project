# Import Modules
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
import pandas as pd
import csv
import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from rekognition import Rekognition
from linksrecommender import LinksRecommender
from readfile import ReadFile


import pymongo
from profiledb import ProfileDB
from wishlistdb import WishlistDB


profile_db = ProfileDB()
wishlist_db = WishlistDB()


# class to call the popup function
class PopupWindow(Widget):
   def btn(self):
       popContent()
 # class to build GUI for a popup window
class P(FloatLayout):
   pass
 # function that displays the content
def popContent():
   show = P()
   window = Popup(title = "popup", content = show,
                  size_hint = (None, None), size = (300, 300), background_color = "#D587F7")
   window.open()
 # class to accept user info and validate it
global_var1 = []
class loginWindow(Screen):
   email = ObjectProperty(None)
   pwd = ObjectProperty(None)
   button = ObjectProperty(None)
   cancolor = get_color_from_hex('#ECA1E7')
   def validate(self):


       #Checks to see if user is in the database (if they made an account)
       if profile_db.userLogin(self.email.text, self.pwd.text) is False:
           popContent()


       else:
            # switching the current screen to display validation result
           global_var1.insert(0,self.email.text)
           sm.current = 'wishlistdata'
            # reset TextInput widget
           self.email.text = ""
           self.pwd.text = ""
          
   def togglevisibility(self):
       if self.pwd.password == True:
           self.pwd.password = False
           self.button.text = "Hide"
       elif self.pwd.password == False:
           self.pwd.password = True
           self.button.text = "Show"


 
# class to accept sign up info  
class signupWindow(Screen):


   first_name2 = ObjectProperty(None)
   last_name2 = ObjectProperty(None)
   email = ObjectProperty(None)
   zipcode = ObjectProperty(None)
   pwd = ObjectProperty(None)
   def signupbtn(self):
        # creating a DataFrame of the info
       user = pd.DataFrame([[self.first_name2.text, self.last_name2.text, self.email.text, self.zipcode.text, self.pwd.text, "Empty"]],
                           columns = ['First Name', 'Last Name', 'Email', 'Zipcode', 'Password', 'WishList'])
      
       #Adds profile to database
       profile_db.createAccount(self.email.text, self.pwd.text, self.first_name2.text, self.last_name2.text, self.zipcode.text)


       if self.email.text != "":
           if self.email.text not in users['Email'].unique():
                # if email does not exist already then append to the csv file
               # change current screen to log in the user now 
               user.to_csv('login.csv', mode = 'a', header = False, index = False)
               sm.current = 'login'
               self.first_name2.text = ""
               self.last_name2.text = ""
               self.email.text = ""
               self.zipcode.text = ""
               self.pwd.text = ""
       else:
           # if values are empty or invalid show pop up
           popContent()
class wishListWindow(Screen):
   pass
   '''
   def wishlist(self):
       window = GridLayout(cols=1)
       list_of_gifts = Label(text="Enter wishlist: ")
       window.add_widget(list_of_gifts)
       user_input = TextInput(multiline=True)
       window.add_widget(user_input)
       button = Button(text="Next")
       button.bind(on_press=self.callback)
       window.add_widget(button)
       self.add_widget(window)
       return
   def callback(self, instance):
       self.list_of_gifts.text = "Thank you for inputting your wish list!"
       wish_list = [self.user_input.text]
       print(wish_list)
       #return wish_list   
   '''
class createWishWindow(Screen):
   wishlist_input = ObjectProperty(None)
   wishlist_input_file = ObjectProperty(None)
   wishlist_name = ObjectProperty(None)
   def save_wishlist(self):


       user_email = global_var1[0]
       wishlist_db.createWishlist(user_email, self.wishlist_name.text) #creates a new wishlist (name cannot duplicate within a user)


       wishlist = self.wishlist_input.text
       items = wishlist.split("\n")
      
       wishlist_db.addItems(user_email, self.wishlist_name.text, items) #adds items to the wishlist


       i=0
       df = pd.read_csv("login.csv")
       wishlist = self.wishlist_input.text
       with open('login.csv', 'r+') as file:
           reader = csv.DictReader(file)
           rows = list(reader)
           for row in rows:
               if row['Email'] == global_var1[0]:
                   value = i
                   break
               i+=1
       df.loc[value, 'WishList'] = wishlist
       df.to_csv("login.csv", index=False)


       # Clear the wishlist input after saving
       self.wishlist_input.text = ""
       self.wishlist_name.text = ""


   def update_wishlist(self):
       user_email = global_var1[0]
       wishlist = self.wishlist_input.text
       items = wishlist.split("\n")
       wishlist_db.addItems(user_email, self.wishlist_name.text, items) #updates items to the wishlist
       # Clear the wishlist input after saving
       self.wishlist_input.text = ""
       self.wishlist_name.text = ""


# This class is to view wishlists near the user.
class othersWishWindow(Screen):
    def __init__(self, **kwargs):
        super(othersWishWindow, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')  # Create a vertical box layout

        # Create a button
        button = Button(text='Load Data', size_hint=(None, None), size=(300, 50),
                        pos_hint={'center_x': 0.5, 'y': 0.90})
        button.bind(on_press=self.load_data)  # Bind the button press to load_data method
        self.layout.add_widget(button)  # Add the button to the layout

        # Spacer to push the button to the top
        self.layout.add_widget(Label())

        self.label_container = BoxLayout(orientation='vertical', padding=(50, 0, 0, 0))  # Create a container for labels with left indentation
        self.layout.add_widget(self.label_container)  # Add the label container to the layout

        self.add_widget(self.layout)

    def load_data(self, instance):
        wishlist_db.wishlistNearMe(global_var1[0])
        # Clear previous labels
        self.label_container.clear_widgets()

        # Open and read the data file
        try:
            with open("wishlistsnearme.txt", 'r') as file:
                for line in file:
                    label = Label(text=line.strip(), font_size=30, size_hint_y=None, height=200)  # Set fixed height for each label
                    self.label_container.add_widget(label)  # Add each label to the container
        except FileNotFoundError:
            label = Label(text="File not found!", font_size=30, size_hint_y=None, height=50)
            self.label_container.add_widget(label)



# This class is to view the wishlists of your profile.
class printWishWindow(Screen):
    def __init__(self, **kwargs):
        super(printWishWindow, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')  # Create a vertical box layout

        # Create a button
        button = Button(text='Load Data', size_hint=(None, None), size=(300, 50),
                        pos_hint={'center_x': 0.5, 'y': 0.90})
        button.bind(on_press=self.load_data)  # Bind the button press to load_data method
        self.layout.add_widget(button)  # Add the button to the layout

        # Spacer to push the button to the top
        self.layout.add_widget(Label())

        self.label_container = BoxLayout(orientation='vertical', padding=(50, 0, 0, 0))  # Create a container for labels with left indentation
        self.layout.add_widget(self.label_container)  # Add the label container to the layout

        self.add_widget(self.layout)

    def load_data(self, instance):
        wishlist_db.showWishlist(global_var1[0])
        # Clear previous labels
        self.label_container.clear_widgets()

        # Open and read the data file
        try:
            with open("mywishlist.txt", 'r') as file:
                for line in file:
                    label = Label(text=line.strip(), font_size=30, size_hint_y=None, height=200)  # Set fixed height for each label
                    self.label_container.add_widget(label)  # Add each label to the container
        except FileNotFoundError:
            label = Label(text="File not found!", font_size=30, size_hint_y=None, height=50)
            self.label_container.add_widget(label)









# class to display validation result
class logDataWindow(Screen):
   pass




class wordWindow(Screen):
   wishlist_input = ObjectProperty(None)
   wishlist_name = ObjectProperty(None)
   def save_wishlist(self):


       user_email = global_var1[0]
       wishlist_db.createWishlist(user_email, self.wishlist_name.text) #creates a new wishlist (name cannot duplicate within a user)


       wishlist = self.wishlist_input.text
       items = wishlist.split("\n")
      
       wishlist_db.addItems(user_email, self.wishlist_name.text, items) #adds items to the wishlist

       # Clear the wishlist input after saving
       self.wishlist_input.text = ""
       self.wishlist_name.text = ""


   def update_wishlist(self):
       user_email = global_var1[0]
       wishlist = self.wishlist_input.text
       items = wishlist.split("\n")
       wishlist_db.addItems(user_email, self.wishlist_name.text, items) #updates items to the wishlist
       # Clear the wishlist input after saving
       self.wishlist_input.text = ""
       self.wishlist_name.text = ""
       
class uploadWindow(Screen):
   wishlist_name = ObjectProperty(None)
   def option_selected(self, option):
       if option == 'c':
           self.capture_image()
       elif option == 'u':
           self.upload_image()


   def capture_image(self):
       self.r = Rekognition()
       r = self.r
       r.camera()
       file_path = "images"
       s3 = "s3://hack-ku-2024/"


       instruction = f"aws s3 cp {file_path} {s3} --recursive"
       subprocess.run(instruction, shell=True)


       camera_wishlist_path = "camera_wishlist.txt"
       with open(camera_wishlist_path, "w") as camera_wishlist:
           photo = 'image1.png'
           bucket = 'hack-ku-2024'
           result = self.r.image_lable_recognizer(photo, bucket)
           camera_wishlist.write(','.join(result))
       camera_wishlist.close()
  
       lr = LinksRecommender()


       read_file = ReadFile()


       word_list = read_file.read('camera_wishlist.txt')






       link_n_wishlist = open("link_n_wishlist.txt", "w")


       for word in word_list:
           big_list = []
           links = lr.links(word)

           big_list.append(word)
           num = 0
           for link in links:
               num += 1
               big_list.append(link)
               if num == 4:
                   break
          
           link_n_wishlist.write(f'{str(big_list)}\n')
      
       link_n_wishlist.close()

       filepath = open("link_n_wishlist.txt", "r")

       for line in filepath:
          line_len = len(line)
          new_line = line[1:line_len - 1].split(",")
          new_line_len = len(new_line)
          item_string = new_line[0]
          item_string += ": " + ", ".join(new_line[1: new_line_len - 1])

          item = [item_string]

          wishlist_db.addItems(global_var1[0], self.wishlist_name.text, item)


   def upload_image(self):
       self.r = Rekognition()
       # Your upload logic here
       file_path = "images"
       s3 = "s3://hack-ku-2024/"


       instruction = f"aws s3 cp {file_path} {s3} --recursive"
       subprocess.run(instruction, shell=True)


       camera_wishlist_path = "camera_wishlist.txt"
       with open(camera_wishlist_path, "w") as camera_wishlist:
           photo = 'jeacket.png'
           bucket = 'hack-ku-2024'
           result = self.r.image_lable_recognizer(photo, bucket)
           camera_wishlist.write(','.join(result))
       camera_wishlist.close()
  
       lr = LinksRecommender()


       read_file = ReadFile()


       word_list = read_file.read('camera_wishlist.txt')






       link_n_wishlist = open("link_n_wishlist.txt", "w")


       for word in word_list:
           big_list = []
           links = lr.links(word)
           big_list.append(word)
           num = 0
           for link in links:
               num += 1
               big_list.append(link)
               if num == 4:
                   break
           link_n_wishlist.write(f'{str(big_list)}\n')
      
       link_n_wishlist.close()
       filepath = open("link_n_wishlist.txt", "r")

       for line in filepath:
          line_len = len(line)
          new_line = line[1:line_len - 1].split(",")
          new_line_len = len(new_line)
          item_string = new_line[0]
          item_string += ": " + ", ".join(new_line[1: new_line_len - 1])

          item = [item_string]

          wishlist_db.addItems(global_var1[0], self.wishlist_name.text, item)

class cameraWindow(Screen):
   wishlist_input_pic = ObjectProperty(None)
   wishlist_name = ObjectProperty(None)
   wishlist_name = ObjectProperty(None)
   def option_selected(self, option):
       if option == 'c':
           self.capture_image()
       elif option == 'u':
           self.upload_image()


   def capture_image(self):
       self.r = Rekognition()
       # Your capture logic here
       r = self.r
       r.camera()
       file_path = "images"
       s3 = "s3://hack-ku-2024/"


       instruction = f"aws s3 cp {file_path} {s3} --recursive"
       subprocess.run(instruction, shell=True)


       camera_wishlist_path = "camera_wishlist.txt"
       with open(camera_wishlist_path, "w") as camera_wishlist:
           photo = 'image1.png'
           bucket = 'hack-ku-2024'
           result = self.r.image_lable_recognizer(photo, bucket)
           camera_wishlist.write(','.join(result))
       camera_wishlist.close()
  
       lr = LinksRecommender()


       read_file = ReadFile()


       word_list = read_file.read('camera_wishlist.txt')






       link_n_wishlist = open("link_n_wishlist.txt", "w")


       for word in word_list:
           big_list = []
           links = lr.links(word)

           big_list.append(word)
           num = 0
           for link in links:
               num += 1
               big_list.append(link)
               if num == 4:
                   break
          
           link_n_wishlist.write(f'{str(big_list)}\n')
      
       link_n_wishlist.close()

       filepath = open("link_n_wishlist.txt", "r")

       for line in filepath:
          line_len = len(line)
          new_line = line[1:line_len - 1].split(",")
          new_line_len = len(new_line)
          item_string = new_line[0]
          item_string += ": " + ", ".join(new_line[1: new_line_len - 1])

          item = [item_string]

          wishlist_db.addItems(global_var1[0], self.wishlist_name.text, item)
    


   def upload_image(self):
       self.r = Rekognition()
       # Your upload logic here
       file_path = "images"
       s3 = "s3://hack-ku-2024/"


       instruction = f"aws s3 cp {file_path} {s3} --recursive"
       subprocess.run(instruction, shell=True)


       camera_wishlist_path = "camera_wishlist.txt"
       with open(camera_wishlist_path, "w") as camera_wishlist:
           photo = 'jeacket.png'
           bucket = 'hack-ku-2024'
           result = self.r.image_lable_recognizer(photo, bucket)
           camera_wishlist.write(','.join(result))
       camera_wishlist.close()
  
       lr = LinksRecommender()


       read_file = ReadFile()


       word_list = read_file.read('camera_wishlist.txt')






       link_n_wishlist = open("link_n_wishlist.txt", "w")


       for word in word_list:
           big_list = []
           links = lr.links(word)

           big_list.append(word)
           num = 0
           for link in links:
               num += 1
               big_list.append(link)
               if num == 4:
                   break
          
           link_n_wishlist.write(f'{str(big_list)}\n')
      
       link_n_wishlist.close()


       filepath = open("link_n_wishlist.txt", "r")

       for line in filepath:
          line_len = len(line)
          new_line = line[1:line_len - 1].split(",")
          new_line_len = len(new_line)
          item_string = new_line[0]
          item_string += ": " + ", ".join(new_line[1: new_line_len - 1])

          item = [item_string]

          wishlist_db.addItems(global_var1[0], self.wishlist_name.text, item) 
    
 # class for managing screens
class windowManager(ScreenManager):
   pass






 # kv file
kv = Builder.load_file('login.kv')
sm = windowManager()
 # reading all the data stored
users=pd.read_csv('login.csv')
 # adding screens
sm.add_widget(loginWindow(name='login'))
sm.add_widget(signupWindow(name='signup'))
sm.add_widget(logDataWindow(name='logdata'))
sm.add_widget(wishListWindow(name='wishlistdata'))
sm.add_widget(createWishWindow(name='createwish'))
sm.add_widget(printWishWindow(name='printwishlist'))
sm.add_widget(othersWishWindow(name='wishlistnearme'))


sm.add_widget(wordWindow(name='wishlistwords'))
sm.add_widget(uploadWindow(name='uploadpic'))
sm.add_widget(cameraWindow(name='takepic'))
 # class that builds gui
class loginMain(App):
   def build(self):
       Window.clearcolor = (60/255,54/255,76/255,1)
       return sm
 # driver function
loginMain().run()
