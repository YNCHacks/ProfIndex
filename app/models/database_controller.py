"""
    Database Controller module for Prof_Index
    Author: Sean Saito

    The Controller for the database, to be interfaced with the
    controller component of the app.
"""

### Imports ###
from professor import Professor
import os, json

### Global variables ###
json_file_path = "app/static/json/professors.json"

class DatabaseConnector:
    """
    This class implements model functions to be used by the controller
    It handles queries for users and CRUD methods on the database.
    """
    def __init__(self):
        self.database = self.load_database()

    def load_database(self):
        """ Loads json database into memory """
        print "[DatabaseConnector::load_database] Loading database"
        try:
            with open(json_file_path, "r+") as fp:
                store = json.load(fp)
                fp.close()
                return store
        except:
            print "[DatabaseConnector::load_database] Error in loading database"
            return

    def write_to_database(self):
        """ Writes to database """
        print "[DatabaseConnector::write_to_database] Writing to database"
        try:
            with open(json_file_path, "w+") as fp:
                fp.write(json.dumps(self.database))
                fp.close()
                return True
        except:
            print "[DatabaseConnector::write_to_database] Failed to write to database"
            return False

    def convert_to_professor(self, prof_details):
        """
        Converts a json object of professor details into a Professor
        object.

        Args:
            prof_details (dict)     : JSON object of valid Professor attributes
        Returns
            A Professor object
        """
        try:
            return Professor(prof_details)
        except:
            print "[DatabaseConnector::convert_to_professor] error in converting to Professor object"
            return

    def search_professor(self, param, value):
        """
        Searches professor based on parameter and value.
        For login authentication, param should be 'email' and value should be
        the password associated to that account.

        Args:
            param (str)                        : A valid Professor attribute
            value (str or int or bool)         : Value of parameter
        Returns
            A Professor object if found, string if not
        """
        for key, item in self.database.items():
            if item[param] == value:
                return self.convert_to_professor(item)
        return "Professor not found"

    def authenticate(self, email, password):
        """
        Matches email with password.
        Returns a tuple based on success.

        Args:
            email (str)
            password (str)
        Returns:
            Tuple of (bool, Professor object or '')
        """
        if email not in self.database:
            return (False, "")

        if self.database[email]["password"] == password:
            return (True, self.convert_to_professor(self.database[email]))
        else:
            return (False, "")

    def get_all_professors(self):
        """ Returns array of all Professor objects """
        return [self.convert_to_professor(professor) for professor in self.database.items()]

    def update_professor(self, email, param, value):
        """
        Updates details of a professor. Example usage is for updating
        the availability of a professor.

        Example:
            DatabaseConnector.update_professor("abc@xyz.edu", "availability", False)

        """
        if email not in self.database:
            print "[DatabaseConnector::update_professor] Professor not found"
            return False

        try:
            self.database[email][param] = value
            print "[DatabaseConnector::update_professor] Updated Professor"
            self.write_to_database()
            return True
        except:
            print "[DatabaseConnector::update_professor] Failed to update Professor"
            return False

    def add_professor(self, prof_details):
        """
        Adds new professor entry to memory, then writes to database.

        Args:
            prof_details (dict)     : dictionary with valid professor params
        Returns:
            bool        : indicates success

        """
        new_professor = ""
        try:
            new_professor = Professor(prof_details)
        except:
            print "[DatabaseConnector::add_professor] Invalid parameters"
            return False

        self.database[new_professor.email] = new_professor.get_json()

        try:
            self.write_to_database()
            print "[DatabaseConnector::add_professor] Added professor"
            return True
        except:
            print "[DatabaseConnector::add_professor] Failed to add professor"
            return False
