# -*- coding: utf-8 -*-
from app.models.person import Person

def get_name():
    person = Person()
    return person.get_name()
