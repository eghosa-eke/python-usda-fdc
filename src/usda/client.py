#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from usda.enums import ReportFormat, Endpoints, DataType, Sorting
from usda.domain import AbridgedFoodItem, BrandedFoodItem, FoundationFoodItem, \
    SRLegacyFoodItem, SurveyFoodItem, SampleFoodItem, SearchResult
from usda.base import ClientBase

DATA_TYPE_FOOD_ITEM = {
    "Branded": BrandedFoodItem,
    "Foundation": FoundationFoodItem,
    "SR Legacy": SRLegacyFoodItem,
    "Survey": SurveyFoodItem,
    "Sample": SampleFoodItem,
}

class UsdaClient(ClientBase):
    """
    Implements an interface to access the USDA FDC API client.
    """

    def __init__(self, fdc_api_key):
        """
        Params:
            fdc_api_key (str): A FDC API key.
        """

        super().__init__(fdc_api_key)

    def get_food(self, fdc_id, report_format=ReportFormat.abridged, nutrients=[], raw=False):
        """
        Get a Food Report for a given food item ID.
        
        Params:
            fdc_id (int,str): FDC id of the food to retrieve
            report_format (usda.enums.ReportFormat): 'abridged' for an abridged set of elements, 'full' for all elements. Default is 'abridged'
            nutrients (list): Optional. List of up to 25 nutrient numbers. Only the nutrient information for the specified nutrients will be returned.
            raw (bool): Whether to return the raw API response or FoodItem object. Default is False.

        Returns:
            dict, FoodItem: raw JSON response or FoodItem object
        """
       
        params = {'format': report_format, 'nutrients': nutrients}
        params = self.process_args(**params)
        res = self.run_request(Endpoints.food, fdc_id=str(fdc_id), **params)
        if raw:
            return res
        if report_format == ReportFormat.abridged:
            return AbridgedFoodItem.from_response_data(res)
        return DATA_TYPE_FOOD_ITEM[res["dataType"]].from_response_data(res)

    def get_foods(self, fdc_ids, report_format=ReportFormat.abridged, nutrients=[], raw=False):
        """
        Retrieves a list of food items by a list of up to 20 FDC IDs.
        
        Params:
            fdc_ids (list): list of FDC ids of the foods to retrieve
            report_format (usda.enums.ReportFormat): 'abridged' for an abridged set of elements, 'full' for all elements. Default is 'abridged'
            nutrients (list): Optional. List of up to 25 nutrient numbers. Only the nutrient information for the specified nutrients will be returned.
            raw (bool): Whether to return the raw API response or FoodItem object. Default is False.

        Returns:
            list: list of raw JSON food items or FoodItem objects
        """

        params = {'fdcIds': fdc_ids, 'format': report_format, 'nutrients': nutrients}
        params = self.process_args(**params)
        res = self.run_request(Endpoints.foods, **params)
        if raw:
            return res
        out = []
        for food in res:
            # print(food)
            food_item = AbridgedFoodItem
            if report_format != ReportFormat.abridged:
                food_item = DATA_TYPE_FOOD_ITEM[food['dataType']]
            out.append(food_item.from_response_data(food))

        return out

    def list_foods(self, data_type=[DataType.Foundation, DataType.SR], page_size=5, page_num=1,
                   sort_by=Sorting.description, reverse=False, raw=False):
        """
        Get a list of available food items in the database.
        Returns a paged list of foods, in the 'abridged' format
        
        Params:
            data_type (list): Optional. Filter on a specific data type; specify one or more values in the list.
            page_size (int): Optional. Maximum number of results to return for the current page. Default is 5.
            page_num (int): Optional. Page number to retrieve. 
                            The offset into the overall result set is expressed as (pageNumber * pageSize)
            sort_by (usda.enums.Sorting): Optional. Specify one of the possible values to sort by that field. Default is Sorting.description
            reverse (bool): The sort direction for the results. Only applicable if sortBy is specified. Default is False/'asc'
            raw (bool): Whether to return the raw API response or FoodItem object. Default is False.
        
        Returns:
            list: list of raw JSON food items, or AbridgedFoodItem's
        """

        params = {'dataType': data_type, 'pageSize': page_size,
                  'pageNumber': page_num, 'sortBy': sort_by, 'reverse': reverse}
        params = self.process_args(**params)
        res = self.run_request(Endpoints.list, **params)
        if raw:
            return res
        return [AbridgedFoodItem.from_response_data(food) for food in res]

    def search_foods(self, query, data_type=[DataType.Foundation, DataType.SR], page_size=25, page_num=1,
                     sort_by=Sorting.description, reverse=False, brand=None, raw=False):
        """
        Get a list of food items matching a specified query.
        
        Params:
            query (str): One or more search terms. The string may include search operators
            data_type (list): Optional. Filter on a specific data type; specify one or more values in the list.
            page_size (int): Optional. Maximum number of results to return for the current page. Default is 5.
            page_num (int): Optional. Page number to retrieve. 
                            The offset into the overall result set is expressed as (pageNumber * pageSize)
            sort_by (usda.enums.Sorting): Optional. Specify one of the possible values to sort by that field. Default is Sorting.description
            reverse (bool): The sort direction for the results. Only applicable if sortBy is specified. Default is False/'asc'
            brand (str): Optional. Filter results based on the brand owner of the food. Only applies to Branded Foods
            raw (bool): Whether to return the raw API response or FoodItem object. Default is False.
        
        Returns:
            dict, SearchResult: raw JSON response or SearchResult object
        """

        params = {'query': query, 'dataType': data_type, 'pageSize': page_size, 'pageNumber': page_num,
                  'sortBy': sort_by, 'reverse': reverse, 'brandOwner': brand}
        params = self.process_args(**params)
        res = self.run_request(Endpoints.search, **params)
        if raw:
            return res
        return SearchResult.from_response_data(res)
