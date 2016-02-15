"""
    Controller for Prof_Index
    Author: Pratyush More

    This module holds the Controller
    component of the app.
"""
from app.models.professor import *

class Controller:
    def __init__(self):
        self.data = DatabaseConnector()

    WRONG_CREDENTIALS = "Failed Login. Please check your entered credentials."
    
    def search_prof(self, name) :
        result = self.data.search_professor("name", name)
        return result

    def authenticate(email, password):
        isSuccess = self.data.authenticate(email, password)
        if isSuccess == true:
            return isSuccess[1]
        return WRONG_CREDENTIALS

    def get_all_professors():
        return self.data.get_all_professors()
