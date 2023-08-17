from src.api_wrapper import theOddsApi
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY')

oddsApi = theOddsApi(api_key, 'iso', 'american', ['h2h'], ['us', 'us2'])

def findArbitrageOpportunities(games):
    opportunities = []
    for game in games:
        bookmakers = game['bookmakers']
        for market_key in ['player_pass_tds']:
            outcomes_by_description = {}
            for bookmaker in bookmakers:
                for market in bookmaker['markets']:
                    if market['key'] == market_key:
                        for outcome in market['outcomes']:
                            description = outcome['description']
                            if description not in outcomes_by_description:
                                outcomes_by_description[description] = []
                            outcomes_by_description[description].append({
                                'name': outcome['name'],
                                'price': outcome['price'],
                                'bookmaker': bookmaker['title'],
                                'point': outcome['point']
                            })
            
            # Check for arbitrage opportunities for each player
            for description, outcomes in outcomes_by_description.items():
                if len(outcomes) < 2: # Skip if there's only one outcome
                    continue
                
                for i in range(len(outcomes)):
                    for j in range(i + 1, len(outcomes)):
                        outcome1 = outcomes[i]
                        outcome2 = outcomes[j]
                        
                        if outcome1['name'] == outcome2['name'] and outcome1['point'] == outcome2['point']:
                            if outcome1['price'] != outcome2['price']:
                                opportunity = {
                                    'game_id': game['id'],
                                    'description': description,
                                    'bookmakers': [outcome1['bookmaker'], outcome2['bookmaker']],
                                    'prices': [outcome1['price'], outcome2['price']]
                                }
                                opportunities.append(opportunity)
    
    return opportunities

active_sports = oddsApi.getSportsList(False)
for sport in active_sports:
    sport_key = sport['key']
    odds = oddsApi.getOdds(sport_key)
    if not odds:
        continue
    arbitrages = findArbitrageOpportunities(odds)

print(arbitrages)
