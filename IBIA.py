import sqlite3
import hashlib
from datetime import date
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivymd.uix.list import OneLineListItem 
def create_table(): 
   conn = sqlite3.connect('ostofit.db')
   cursor = conn.cursor()
   print("HERE")
   cursor.execute('''
       CREATE TABLE IF NOT EXISTS users (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           username_input TEXT NOT NULL,
           email_input TEXT UNIQUE NOT NULL,
           hashed_password TEXT NOT NULL
           
       )
   ''')
   cursor.execute('''
       CREATE TABLE IF NOT EXISTS workouts (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           user_id INTEGER,
           exercise_name TEXT,
           reps INTEGER,
           weight REAL,
           date TEXT,
           FOREIGN KEY(user_id) REFERENCES users(id)
                  
           
       )
   ''')
   conn.commit()
   conn.close()

create_table()
print("Database saved succesfully")   



KV = '''
ScreenManager:
    LoginScreen:
    RegisterScreen:

<LoginScreen>:
    name: 'login'
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "10dp"
        MDLabel:
            text: "Ostofit Login"
            halign: "center"
            font_style: "H4"
        MDTextField:
            id: login_email
            hint_text: "Email"
        MDTextField:
            id: login_password
            hint_text: "Password"
            password: True
        MDRaisedButton:
            text: "Login"
            pos_hint: {"center_x": .5}
        MDFlatButton:
            text: "Don't have an account? Register"
            pos_hint: {"center_x": .5}
            on_release: root.login_user()

<RegisterScreen>:
    name: 'register'
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "10dp"
        MDLabel:
            text: "Create Account"
            halign: "center"
            font_style: "H4"
        MDTextField:
            id: user_field
            hint_text: "Username"
        MDTextField:
            id: email_field
            hint_text: "Email"
        MDTextField:
            id: password_field
            hint_text: "Password"
            password: True
        MDTextField:
            id: confirm_field
            hint_text: "Confirm Password"
            password: True
        MDRaisedButton:
            text: "Register"
            pos_hint: {"center_x": .5}
            on_release: root.register_user() # Matches method name below
        MDFlatButton:
            text: "Back to Login"
            pos_hint: {"center_x": .5}
            on_release: root.manager.current = 'login'
'''








def hash_password(hashed_password):
   # Create a new sha256 hash object
   sha_signature = hashlib.sha256(hashed_password.encode()).hexdigest()
   return sha_signature





def save_user(username_input, email_input, hashed_password):
    conn = sqlite3.connect('ostofit.db')
    cursor = conn.cursor()
    cursor.execute('''
            INSERT INTO users (username_input, email_input, hashed_password)
            VALUES (?, ?, ?)
            ''', (username_input, email_input, hashed_password))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


class LoginScreen(Screen):
   def login_user(self):
    email = self.ids.email_login.text
    password = self.ids.password_login.text
    if password == "" or email == "":
       print("Fill out all fields")
       return
    
    hashed_attempt = hash_password(password)

    conn = sqlite3.connect('ostofit.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email_input = ? AND hashed_password = ?", (email, hashed_attempt))
    user = cursor.fetchone()
    conn.close()

    if user:
       MDApp.get_running_app().current_user_id = user[0]
       print(f"Login Successful User ID: {user[0]}")
    else:
       print("Invaild User Info")
       



class RegisterScreen(Screen):
   def register_user(self):
      username_input = self.ids.user_field.text
      password_input = self.ids.password_field.text
      confirm_password = self.ids.confirm_field.text
      email_input = self.ids.email_field.text
      if password_input == confirm_password and password_input != "":   
          hashed_password = hash_password(confirm_password)
          user_id = save_user(username_input, email_input, hashed_password)
          MDApp.get_running_app().current_user_id = user_id
          print(f"Account created successfully, {user_id}")
      else:
          print("Passwords do not match")


class OstofitApp(MDApp):
   current_user_id = None

   def build(self):
      return Builder.load_string(KV)
if __name__ == '__main__':
   OstofitApp().run()







#register() 
#save_user("Moti", "motimod223@gmail.com", "730459")    



#create_table()     