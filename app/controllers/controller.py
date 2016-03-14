"""
    Controller for Prof_Index
    Author: Pratyush More

    This module holds the Controller
    component of the app.
"""
from app.models.database_controller import DatabaseConnector
import hashlib

class Controller:
    def __init__(self):
        self.data = DatabaseConnector()

    WRONG_CREDENTIALS = "Failed Login. Please check your entered credentials."

    def search_prof(self, name, param='name'):
        result = self.data.search_professor(param, name)
        if (result == "Professor not found"):
            return (False, "")
        return (True, result)

    def authenticate(self, email, password):
        hashed_pw = self.hash_password(password)
        isSuccess = self.data.authenticate(email, hashed_pw)
        return isSuccess

    def get_all_professors(self):
        return self.data.get_all_professors()

    def get_all_professor_names(self):
        professor = self.get_all_professors()
        print([prof.name for prof in professor])
        return [prof.name for prof in professor]

    def add_professor(self, prof_details):
        password = prof_details["password"]
        hashed_pw = self.hash_password(password)
        prof_details["password"] = hashed_pw
        self.data.add_professor(prof_details)

    def hash_password(self, password):
        hasher = hashlib.sha1()
        hasher.update(password)
        hashed_pw = hasher.hexdigest()
        return hashed_pw

    def update_value(self,email, param, value):
        if param == "password":
            value = self.hash_password(value)
        self.data.update_professor(email, param, value)
