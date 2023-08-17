import unittest
from unittest.mock import patch
from src.api_wrapper import theOddsApi

class TestTheOddsApi(unittest.TestCase):

    def test_init(self):
        api_key = "your_api_key"
        date_format = "iso"
        odds_format = "decimal"
        markets = "h2h, spreads"
        regions = "us, uk"

        api = theOddsApi(api_key, date_format, odds_format, markets, regions)

        self.assertEqual(api.api_key, api_key)
        self.assertEqual(api.date_format, date_format)
        self.assertEqual(api.odds_format, odds_format)
        self.assertEqual(api.markets, markets)
        self.assertEqual(api.regions, regions)

    def test_string_to_list(self):
        input_string = "item1, item2, item3"
        expected_output = ['item1', 'item2', 'item3']
        self.assertEqual(theOddsApi.stringToList(input_string), expected_output)

        input_list = ['item1', 'item2', 'item3']
        self.assertEqual(theOddsApi.stringToList(input_list), expected_output)

    def test_validate_elements(self):
        valid_elements = ['item1', 'item2', 'item3']
        elements = ['item1', 'item2']
        self.assertIsNone(theOddsApi.validate_elements(elements, valid_elements, 'element'))

        invalid_elements = ['item4']
        with self.assertRaises(ValueError):
            theOddsApi.validate_elements(invalid_elements, valid_elements, 'element')

    def test_validate_format(self):
        valid_formats = ['format1', 'format2']
        self.assertIsNone(theOddsApi.validate_format('format1', valid_formats, 'format'))

        with self.assertRaises(ValueError):
            theOddsApi.validate_format('format3', valid_formats, 'format')

    @patch('src.api_wrapper.theOddsApi.make_request')
    def test_get_sports_list(self, mock_make_request):
        api_key = "your_api_key"
        api = theOddsApi(api_key, "iso", "decimal", "h2h, spreads", "us, uk")
        
        # Mocking the response
        mock_response = {'some': 'data'}
        mock_make_request.return_value = mock_response

        sports_list = api.getSportsList()
        self.assertEqual(sports_list, mock_response) # Adjust this based on the actual expected output

    @patch('src.api_wrapper.theOddsApi.make_request')
    def test_get_odds(self, mock_make_request):
        api_key = "your_api_key"
        api = theOddsApi(api_key, "iso", "decimal", "h2h, spreads", "us, uk")
        
        # Mocking the response
        mock_response = {'some': 'odds_data'}
        mock_make_request.return_value = mock_response

        odds = api.getOdds(sport='americanfootball_nfl')
        self.assertEqual(odds, mock_response) # Adjust this based on the actual expected output


if __name__ == "__main__":
    unittest.main()
