import requests
from requests.exceptions import HTTPError
class theOddsApi:

    '''
    Sends a GET request to the specified URL with optional parameters, handling common HTTP error codes.

    Parameters:
        * `url` [String] - The URL to which the request is to be sent.
        * `params` [Dictionary, optional] - A dictionary containing any URL parameters to be included with the request.

    Returns:
        * Response object containing the server's response to the request if successful.
        * None if the request encountered an HTTP error or other exception.

    Raises:
        * Prints an error message to the console if an HTTP error or other exception occurs.
    '''
    @staticmethod
    def make_request(url, params=None):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status() # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            
            return response.json()
        except HTTPError as http_err:
            status_code = http_err.response.status_code

            if status_code == 400:
                print(f'Bad Request: {http_err}')
            elif status_code == 401:
                print(f'Unauthorized: {http_err}')
            elif status_code == 403:
                print(f'Forbidden: {http_err}')
            elif status_code == 404:
                print(f'Not Found: {http_err}')
            elif status_code == 500:
                print(f'Server Error: {http_err}')
            else:
                print(f'An HTTP error occurred: {http_err}')
            return None
        except Exception as err:
            print(f'An error occurred: {err}')
            return None

    '''
        Takes any comma delinieated string, checks if it is a string, and if it is and converts it to a list, 
        and strings all leading and trailing white space. If it is already a list, it does nothing and returns the same list
        with white space stripped out.

        Parameters:
            * `input` [string] - The string you which it itemize.
    '''
    @staticmethod
    def stringToList(input):
        if isinstance(input, str):
            output_list = [item.strip() for item in input.split(',')]
            return output_list
        elif isinstance(input, list):
            sanitized_list = [item.strip() for item in input]
            return sanitized_list
        else:
            raise TypeError(f"The variable type ")
        
    '''
        Validates if the elements in a list are within a set of valid elements and raises an error if not.

        Parameters:
            * `elements` [list] - List of elements to validate.
            * `valid_elements` [list] - List of valid elements.
            * `element_type` [string] - Description of the element type (e.g. 'market', 'region').
    '''
    @staticmethod
    def validate_elements(elements, valid_elements, element_type):
        for element in elements:
            if element not in valid_elements:
                valid_elements_string = ', '.join(valid_elements)
                raise ValueError(f"The '{element}' {element_type} is not valid. Valid {element_type}s: '{valid_elements_string}'")

    '''
        Validates if the input format is within the set of valid formats and raises an error if not.

        Parameters:
            * `input_format` [string] - The input format to validate.
            * `valid_formats` [list] - List of valid formats.
            * `format_type` [string] - Description of the format type (e.g. 'date format', 'odds format').
    '''
    @staticmethod
    def validate_format(input_format, valid_formats, format_type):
        if input_format not in valid_formats:
            valid_formats_string = ', '.join(valid_formats)
            raise ValueError(f"The {format_type} '{input_format}' is invalid. Valid {format_type}s: '{valid_formats_string}'")


    '''
        Initializes the class with the specified parameters, validates the formats, and sets the attributes.

        Parameters:
            * `api_key` [string] - The API key for accessing the service.
            * `date_format` [string] - The date format to be used ('iso' or 'unix').
            * `odds_format` [string] - The odds format to be used (e.g. 'decimal', 'fractional').
            * `markets` [string or list] - The markets to consider.
            * `regions` [string or list] - The regions to consider.
    '''
    def __init__(self, api_key, date_format, odds_format, markets, regions):
        self.base_url = "https://api.the-odds-api.com/v4"
        self.api_key = api_key
        self.valid_regions = ['us', 'us2', 'uk', 'au', 'eu']
        self.valid_markets = ['h2h', 'spreads', 'totals', 'outrights']
        self.valid_date_formats = ['iso', 'unix']
        self.valid_odds_format = ['decimal', 'american']

        self.validate_format(date_format, self.valid_date_formats, 'date format')
        self.date_format = date_format

        self.validate_format(odds_format, self.valid_odds_format, 'odds format')
        self.odds_format = odds_format
        
        markets_sanitized = self.stringToList(markets)
        self.validate_elements(markets_sanitized, self.valid_markets, 'market')
        self.markets = markets

        regions_sanitized = self.stringToList(regions)
        self.validate_elements(regions_sanitized, self.valid_regions, 'region')
        self.regions = regions


    '''
        Returns a list of supported sports.
        
        Parameters:
            * `active_sports_flag` [Boolean] - Whether to return all sports or just the active ones. False returns all sports.

        Returns:
            * Reponse object containing information on the supported sports.
    '''
    def getSportsList(self, active_sports_flag = True):
        if active_sports_flag:
            active_sports_flag = 'true'
        else:
            active_sports_flag = 'false'
        request_url = f"{self.base_url}/sports"
        data = {
            'apiKey': self.api_key,
            'all': active_sports_flag
        }
        sports_response = self.make_request(request_url, data)
        return sports_response
    
    '''
        Returns the odds for a specified sport or upcoming events.

        Parameters:
            * `sport` [String, optional] - Specifies the sport for which odds are to be retrieved. Defaults to 'upcoming'.
            * `event_ids` [String, optional] - A string containing event IDs for which odds are to be retrieved. Will be converted to a list using the stringToList method.
            * `bookmakers` [String, optional] - A string containing bookmaker IDs for which odds are to be retrieved. Will be converted to a list using the stringToList method.
            * `markets` [String, optional] - Specifies the markets for which odds are to be retrieved.

        Returns:
            * Response object containing odds information.
    '''
    def getOdds(self, sport = 'upcoming', event_ids = None, bookmakers = None):
        

        request_url = f"{self.base_url}/sports/{sport}/odds"
        params = {
            'apiKey': self.api_key,
            'regions': self.regions,
            'markets': self.markets
        }
        if event_ids:
            event_ids_list = self.stringToList(event_ids)
            params['eventIds'] = event_ids_list

        if bookmakers:
            bookmakers_list = self.stringToList(event_ids)
            params['bookmakers'] = bookmakers_list
        
        odds_response = self.make_request(request_url, params = params)
        if odds_response:
            return odds_response
        else:
            None
    
    def getScores(self, sport, days_from=None, event_ids=None):
        request_url = f"{self.base_url}/v4/sports/{sport}/scores/?apiKey={self.api_key}"

        params = {
            'apiKey': self.api_key,
            'daysFrom': days_from if days_from else '',
            'dateFormat': self.date_format,
            'eventIds': event_ids if event_ids else ''
        }

        scores_response = self.make_request(request_url, params=params)

        return scores_response

    
