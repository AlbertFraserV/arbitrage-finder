import unittest
from src.main import findArbitrageOpportunities

class TestFindArbitrageOpportunities(unittest.TestCase):

    def test_find_arbitrage_opportunities(self):
        games = [
            {
                "id": "a512a48a58c4329048174217b2cc7ce0",
                "sport_key": "americanfootball_nfl",
                "sport_title": "NFL",
                "commence_time": "2023-01-01T18:00:00Z",
                "home_team": "Atlanta Falcons",
                "away_team": "Arizona Cardinals",
                "bookmakers": [
                    {
                        "key": "draftkings",
                        "title": "DraftKings",
                        "markets": [
                            {
                                "key": "player_pass_tds",
                                "outcomes": [
                                    {"name": "Over", "description": "David Blough", "price": -205, "point": 0.5},
                                    {"name": "Under", "description": "David Blough", "price": 150, "point": 0.5}
                                ]
                            }
                        ]
                    },
                    {
                        "key": "fanduel",
                        "title": "FanDuel",
                        "markets": [
                            {
                                "key": "player_pass_tds",
                                "outcomes": [
                                    {"name": "Over", "description": "David Blough", "price": -215, "point": 0.5},
                                    {"name": "Under", "description": "David Blough", "price": 164, "point": 0.5}
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
        expected_opportunities = [
            {
                'game_id': 'a512a48a58c4329048174217b2cc7ce0',
                'description': 'David Blough',
                'bookmakers': ['DraftKings', 'FanDuel'],
                'prices': [-205, -215]
            },
            {
                'game_id': 'a512a48a58c4329048174217b2cc7ce0',
                'description': 'David Blough',
                'bookmakers': ['DraftKings', 'FanDuel'],
                'prices': [150, 164]
            }
        ]

        result = findArbitrageOpportunities(games)
        self.assertEqual(result, expected_opportunities)

if __name__ == "__main__":
    unittest.main()
