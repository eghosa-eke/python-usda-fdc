#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum


class Endpoints(Enum):
    """USDA API available endpoints"""

    food = "food/{}"

    foods = "foods"

    list = "foods/list" 

    search = "foods/search"


class ReportFormat(Enum):
    """USDA API food report types"""

    full = "full"
    """
    Contains all the available nutrients.
    """

    abridged = "abridged"
    """
    Contains a shortened version of fod/nutrient info
    """

class DataType(Enum):
    """USDA Supported FoodItem Data Types"""

    Foundation = 'Foundation'
    SR = 'SR Legacy'   # USDA Standard Refernece
    Branded = 'Branded'
    FNDDS = 'Survey (FNDDS)'

class Sorting(Enum):
    """USDA result sort options"""

    dataType = 'dataType.keyword'
    description = 'lowercaseDescription.keyword'
    fdcId = 'fdcId'
    pub_date = 'publishedDate'