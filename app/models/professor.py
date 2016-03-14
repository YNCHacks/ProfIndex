"""
    Professor Class Module for Prof_Index
    Author: Sean Saito

    This module holds the Professor Class and the Model
    component of the app.
"""

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

    def get_json(self):
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
