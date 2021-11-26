#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from requests.auth import HTTPBasicAuth
from .enums import Endpoints, ReportFormat, DataType, Sorting
import warnings

BASE_URI = 'https://api.nal.usda.gov/fdc/v1'
"""The base URI for all USDA FDC API endpoints."""


class FdcApiError(BaseException):
    """
    Base class for all FDC API errors
    """


class FdcApiRateExceededError(FdcApiError):
    """
    FDC API rate limit has been exceeded for this key.
    """

    def __init__(self):
        super().__init__('API rate limit has been exceeded.')


class FdcInvalidApiKeyError(FdcApiError):
    """
    Supplied FDC API key is invalid.
    """

    def __init__(self):
        super().__init__("A invalid Data.gov API key has been supplied. "
                         "Get one at https://fdc.nal.usda.gov/api-key-signup.html")


def api_request(url, api_key, **parameters):
    r"""
    Perform a GET request to an API endpoint.
    
    Params:
        url (str): URL to perform a request to.
        api_key (str): API Key to use for request
        **parameters: GET parameters to send along with the request.
    
    Raises:
        requests.exceptions.HTTPError: If a request has a HTTP 4xx or 5xx status code.
        ValueError: If the API responds with an error on a GET parameter.
        FdcApiRateExceededError: If the API rate limit has been exceeded for a given API key.
        FdcInvalidApiKeyError: If the API key is invalid.
        FdcApiError: If the API returned any error.

    Returns:
        dict: Parsed JSON data.
    """

    auth = HTTPBasicAuth(api_key, "")
    r = requests.get(url, params=parameters, auth=auth)

    try:
        data = r.json()
    except ValueError:  # Server did not even return a JSON for the error
        r.raise_for_status()
    
    # The JSON error data when the API rate limit is exceeded is in a
    # different format than on parameter errors. This will handle both.
    if 'errors' in data:
        err = data['errors']['error'][0]
    elif 'error' in data:  # API rate limit exceeded error format
        err = data['error']
    else:
        return data

    if err == "OVER_RATE_LIMIT":
        raise FdcApiRateExceededError()
    elif err == "API_KEY_INVALID":
        raise FdcInvalidApiKeyError()
    else:
        raise FdcApiError("{0}: {1}".format(r.status_code, err))


class ClientBase(object):
    """
    Base class for Data.gov API clients.
    """

    def __init__(self, api_key):
        """
        Params:
            api_key (str): FDC API key to use for all requests.
        """

        self.key = api_key

    def build_uri(self, endpoint, fdc_id=''):
        """
        Build a valid URI for a specific endpoint.
        
        Params:
            endpoint (usda.enums.Endpoints): An endpoing on the client's API.
            fdc_id (str): FDC ID for /food requests. Default is None.

        Returns:
            str: BASE_URL + Endpoint 
        """

        endpoint = endpoint.value.format(fdc_id) if fdc_id else endpoint.value
        return '/'.join([BASE_URI, endpoint])

    def run_request(self, endpoint, fdc_id='', **kwargs):
        """
        Execute a request and return an API response.
        
        Params:
            endpoint (usda.enums.Endpoints): An endpoint on the client's API.
            fdc_id (str): FDC Food ID for use in /food requests
            kwargs: endpoint specific parameters

        Raises:
            requests.exceptions.HTTPError: If a response has a HTTP 4xx or
                5xx status code.
            FdcApiError: If a FDC request API returns an error.

        Returns:
            dict: JSON reponse from API
        """

        if endpoint == Endpoints.food:
            assert fdc_id, "FDC ID is required to run a '{}' request".format(endpoint.value)
        else:
            fdc_id = ''
        return api_request(self.build_uri(endpoint, fdc_id), self.key, **kwargs)

    def process_args(self, **kwargs):
        """
        Process and validate parameters used for any endpoint

        Returns:
            dict: params to use for endpoint request
        """

        data = {}
        if 'format' in kwargs:
            report_format = kwargs['format']
            assert isinstance(report_format, ReportFormat), \
                "'format' arg should be an instance of usda.enums.ReportFormat. format object was {} instead".format(type(report_format))
            data['format'] = report_format.value

        if 'nutrients' in kwargs:
            nutrients = kwargs["nutrients"] 
            if nutrients:
                assert isinstance(nutrients, list), "Expected to recieve a list of nutrient ids"
                assert len(nutrients) <= 25, "Expected to recieve a list of up to 25 nutrient numbers. Received {} instead".format(len(nutrients))
                data['nutrients'] = list(map(int, nutrients))

        if 'fdcIds' in kwargs:
            fdc_ids = kwargs['fdcIds']
            if fdc_ids:
                assert isinstance(fdc_ids, list), "Expected to recieve a list of FDC ids"
                assert len(fdc_ids) <= 20, "Expected to recieve a list of up to 20 FDC IDs. Received {} instead".format(len(fdc_ids))
                data['fdcIds'] = list(map(str, fdc_ids))

        if 'dataType' in kwargs:
            data_type_enums = kwargs['dataType']
            if data_type_enums:
                data_type = []
                for dt in data_type_enums:
                    assert isinstance(dt, DataType), \
                        "'dataType' should be a list of usda.enums.DataType enums. '{}' not understood.".format(type(dt))
                    data_type.append(dt.value)
                data['dataType'] = data_type

        if 'pageSize' in kwargs:
            page_size = kwargs['pageSize']
            assert page_size >= 1, "pageSize must be at least 1, pageSize was {} instead".format(page_size)
            if page_size > 200:
                warnings.warn("Maximum pageSize is 200. pageSize passed is {}".format(page_size))
            data['pageSize'] = page_size

        if 'pageNumber' in kwargs:
            page_num = kwargs['pageNumber']
            assert page_num >= 1, "pageNumber must be at least 1, pageNumber supplies was {} instead".format(page_num)
            data['pageNumber'] = page_num

        if 'sortBy' in kwargs:
            sort_by = kwargs['sortBy']
            assert isinstance(sort_by, Sorting), "'sortBy' should be an instance of usda.enums.Sorting. sortBy object was {} instead".format(type(sort_by))
            data['sortBy'] = sort_by.value

        if 'query' in kwargs:
            data['query'] = kwargs['query']

        if 'brandOwner' in kwargs:
            brand = kwargs['brandOwner']
            if brand:
                data['brandOwner'] = brand

        if 'reverse' in kwargs:
            data['sortOrder'] = 'asc' if not kwargs['reverse'] else 'desc'

        return data



