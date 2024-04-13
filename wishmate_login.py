# Import Modules
from kivy.app import App 
from kivy.uix.widget import Widget 
from kivy.uix.screenmanager import ScreenManager, Screen 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty 
from kivy.lang import Builder 
from kivy.uix.popup import Popup 
from kivy.uix.floatlayout import FloatLayout 
import pandas as pd 
import csv
print("Hi")
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
    def validate(self):
  
        # validating if the email already exists  
        if self.email.text not in users['Email'].unique(): 
            popContent()
        else:
  
            # switching the current screen to display validation result 
            global_var1.insert(0,self.email.text)
            sm.current = 'wishlistdata'
  
            # reset TextInput widget 
            self.email.text = "" 
            self.pwd.text = "" 
  
  
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
    def save_wishlist(self):
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
# class to display validation result 
class logDataWindow(Screen): 
    pass
  
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
  
# class that builds gui 
class loginMain(App): 
    def build(self): 
        return sm
  
# driver function 
loginMain().run()