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
    return new_id



def register(self):
      username_input = self.ids.user_field.text
      password_input = self.ids.password_field.text
      confirm_password = self.ids.confirm_field.text
      email_input = self.ids.email_field.text
      if password_input == confirm_password:   
          hashed_password = hash_password(confirm_password)
          user_id = save_user(username_input, email_input, hashed_password)
          MDApp.get_running_app().current_user_id = user_id
      else:
          print("Passwords do not match")







#register() 
#save_user("Moti", "motimod223@gmail.com", "730459")    

      