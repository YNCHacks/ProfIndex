"""
    Professor Class Module for Prof_Index
    Author: Sean Saito

    This module holds the Professor Class and the Model
    component of the app.
"""

### Imports ###
import os, json

### Global variables ###
json_file_path = "app/static/json/professors.json"

### Classes ###
class Professor:

    def __init__(self, prof_details):
        """
        The constructor of the Professor class. The object is constructed
        based on parameters passed through prof_details.

        Args:
            prof_details (dict)     :   Dictionary containing details of professor.
            Note: prof_details should have the following fields and types

            {
                "name": string | name of professor
                "id":   string | id of professor
                "password": string | hashed password,
                "email": string,
                "picture_url": string | url to profile picture of professor,
                "availability": boolean | indicates professor availability,
                "office": string | room number of office,
                "office_hours": string | office hours of professor
            }
        """
        self.name = prof_details["name"]
        self.id = prof_details["id"]
        self.password = prof_details["password"]
        self.email = prof_details["email"]
        self.picture_url = prof_details["picture_url"]
        self.availability = prof_details["availability"]
        self.office = prof_details["office"]
        self.office_hours = prof_details["office_hours"]

    def get_json():
        """
        Return professor attributes in json form
        """
        return {
            "name": self.name,
            "id": self.id,
            "password": self.password,
            "email": self.email,
            "picture_url": self.picture_url,
            "availability": self.availability,
            "office": self.office,
            "office_hours": self.office_hours
        }

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
        for item in self.database.items():
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

        if self.database["email"]["password"] == password:
            return (True, self.convert_to_professor(self.database["email"]))
        else:
            return (False, "")

    def get_all_professors(self):
        """ Returns array of all Professor objects """
        return [self.convert_to_professor(professor) for professor in self.database.items()]

    def update_professor(self, email, param, value):
        """ Updates details of a professor. Used for updating availability """
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
