import sys
import os

import json

from PySide6.QtWidgets import QWidget

DB_NAME = "wildlife.json"

class DBController(QWidget):
    def __init__(self, parent):
        self._parent = parent

        home_dir = self._parent.home_dir
        self.DB_path = home_dir + "\\Database\\" + DB_NAME

        self._DB = None

        self._init_database()
        self.load_users()
    
    def _init_database(self):
        try:
            with open(self.DB_path, "r") as file:
                data = json.load(file)
        except json.JSONDecodeError as E:
            print(f'Unable To Parse Database: {E}')
            sys.exit(1)
        except Exception as E:
            print(f'Unable To Load Database in the Given Path: {self.DB_path}')
            sys.exit(1)
            
        if "WildLifeDB" in data:
            self._DB = data["WildLifeDB"]
            print('Database Initialised!')
        else:
            raise Exception("Database 'WildLifeDB' Not Found in given path!")
    
    def load_users(self):
        try:
            users = self.fetch_users()
            for user in users.values():
                if user["Level"] == "Admin":
                    self.Admin = user
                    break
        except KeyError:
            print("Cannot Fetch Admin from Database!")
            sys.exit(1)
    
    def fetch_users(self):
        return self._DB["Users"]
    
    def fetch_settings(self):
        return self._DB["Settings"]
    
    def fetch_cameras(self):
        return self._DB["Cameras"]
    
    def fetch_models(self):
        return self._DB["Models"]
    
    def fetch_engine_data(self):
        return self._DB["AppEngine"]
    
    def save_settings(self, setting: str, data: dict):
        self._DB[setting] = data

        data = {} 
        data["WildLifeDB"] = self._DB

        with open(self.DB_path, "w") as file:
            json.dump(data, file, indent=4)
            print("DB Updated!")
        return True
            
