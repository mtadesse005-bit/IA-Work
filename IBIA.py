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
           hashed_password TEXT NOT NULL,
           
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
           FOREIGN KEY(user_id) REFERENCES user(id)
                  
           
       )
   ''')
   conn.commit()
   conn.close()

   create_table()
   print("Database saved succesfully")                              


