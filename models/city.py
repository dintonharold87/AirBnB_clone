#!/usr/bin/env python3
# This classes that inherits from BaseModel

from models.base_model import BaseModel


class City(BaseModel):
    """A class on the city of a country"""
    state_id = ""
    name = ""
