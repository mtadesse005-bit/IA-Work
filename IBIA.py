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


# I had Gemini build the user GUI as Kivy was too complicated for me to do but I did have to  fix some ID issues
KV = '''
ScreenManager:
    LoginScreen:
    RegisterScreen:
    WorkoutScreen:
    HistoryScreen:

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
            id: email_login
            hint_text: "Email"
        MDTextField:
            id: password_login
            hint_text: "Password"
            password: True
        MDRaisedButton:
            text: "Login"
            pos_hint: {"center_x": .5}
            on_release: root.login_user()  
        MDFlatButton:
            text: "Don't have an account? Register"
            pos_hint: {"center_x": .5}
            on_release: root.manager.current = 'register'

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
            on_release: root.register_user()
        MDFlatButton:
            text: "Back to Login"
            pos_hint: {"center_x": .5}
            on_release: root.manager.current = 'login'

<WorkoutScreen>:
    name: 'workout'
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "15dp"

        MDLabel:
            text: "Log Exercise"
            halign: "center"
            font_style: "H4"
            size_hint_y: None
            height: self.texture_size[1]

        MDTextField:
            id: exercise_name
            hint_text: "Exercise Name (e.g. Squat)"
            mode: "rectangle"

        MDTextField:
            id: reps_field
            hint_text: "Reps"
            input_filter: "int"
            mode: "rectangle"

        MDTextField:
            id: weight_field
            hint_text: "Weight (kg)"
            input_filter: "float"
            mode: "rectangle"

        MDRaisedButton:
            text: "SAVE WORKOUT"
            pos_hint: {"center_x": .5}
            size_hint_x: 0.8
            on_release: root.add_workout()

        MDFlatButton:
            text: "View History"
            pos_hint: {"center_x": .5}
            on_release: root.manager.current = 'history'

        MDFlatButton:
            text: "Logout"
            pos_hint: {"center_x": .5}
            on_release: root.manager.current = 'login'

        Widget:

<HistoryScreen>:
    name: 'history'
    on_enter: root.load_history()
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Workout History"
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
        
        ScrollView:
            MDList:
                id: history_list
'''

# hashed password the following login function I used code from a previous coding project

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# For these functions below I used Gemini to convert my input code into Kivy. Also I asked Gemini to give me examples and explain meanings such as "class", "ScreenManager, and "self".
def save_user(username, email, hashed_password):
    conn = sqlite3.connect('ostofit.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username_input, email_input, hashed_password) VALUES (?, ?, ?)', 
                   (username, email, hashed_password))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def save_workout(user_id, exercise, reps, weight):
    conn = sqlite3.connect('ostofit.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO workouts (user_id, exercise_name, reps, weight, date) VALUES (?, ?, ?, ?, date("now"))', 
                   (user_id, exercise, reps, weight))
    conn.commit()
    conn.close()

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
            self.manager.current = 'workout'
        else:
            print("Invalid credentials")

class RegisterScreen(Screen):
    def register_user(self):
        username = self.ids.user_field.text
        password = self.ids.password_field.text
        confirm = self.ids.confirm_field.text
        email = self.ids.email_field.text
        if password == confirm and password != "":   
            hashed = hash_password(confirm)
            user_id = save_user(username, email, hashed)
            MDApp.get_running_app().current_user_id = user_id
            self.manager.current = 'login' 
        else:
            print("Passwords do not match or field is empty")

class WorkoutScreen(Screen):
    def add_workout(self):
        user_id = MDApp.get_running_app().current_user_id
        ex_name = self.ids.exercise_name.text
        reps = self.ids.reps_field.text
        weight = self.ids.weight_field.text
        if ex_name == "" or reps == "" or weight == "":
            print("Please fill out everything")
            return
        save_workout(user_id, ex_name, int(reps), float(weight))
        self.ids.exercise_name.text = ""
        self.ids.reps_field.text = ""
        self.ids.weight_field.text = ""
        print("Workout Saved!")

class HistoryScreen(Screen):
    def go_back(self):
        self.manager.current = 'workout'

    def load_history(self):
        self.ids.history_list.clear_widgets()
        user_id = MDApp.get_running_app().current_user_id
        conn = sqlite3.connect('ostofit.db')
        cursor = conn.cursor()
        cursor.execute("SELECT exercise_name, reps, weight, date FROM workouts WHERE user_id = ? ORDER BY id DESC", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            display_text = f"{row[0]}: {row[1]} reps @ {row[2]}kg ({row[3]})"
            self.ids.history_list.add_widget(OneLineListItem(text=display_text))

class OstofitApp(MDApp):
    current_user_id = None
    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    OstofitApp().run()
  