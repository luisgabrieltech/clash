import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import random

load_dotenv()

class ClashRoyaleAPI:
    def __init__(self):
        self.api_key = os.getenv('CLASH_ROYALE_API_KEY')
        self.base_url = 'https://api.clashroyale.com/v1'
        self.headers = {'Authorization': f'Bearer {self.api_key}'}
    
    def get_player(self, tag):
        url = f"{self.base_url}/players/%23{tag}"
        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else None
    
    def get_battles(self, tag):
        url = f"{self.base_url}/players/%23{tag}/battlelog"
        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else None
    
    def get_current_deck(self, tag):
        player = self.get_player(tag)
        return player.get('currentDeck', []) if player else None
    
    def format_battle(self, battle_data, player_tag):
        try:
            team = {
                'player_tag': f"#{player_tag}",
                'deck': [card['name'] for card in battle_data['team'][0]['cards']],
                'trophies': battle_data['team'][0].get('startingTrophies', 0),
                'crowns': battle_data['team'][0]['crowns']
            }
            
            opponent = {
                'player_tag': battle_data['opponent'][0]['tag'],
                'deck': [card['name'] for card in battle_data['opponent'][0]['cards']],
                'trophies': battle_data['opponent'][0].get('startingTrophies', 0),
                'crowns': battle_data['opponent'][0]['crowns']
            }
            
            winner = team['player_tag'] if team['crowns'] > opponent['crowns'] else opponent['player_tag']
            if team['crowns'] == opponent['crowns']:
                winner = 'draw'
            
            return {
                'timestamp': datetime.strptime(battle_data['battleTime'], '%Y%m%dT%H%M%S.%fZ'),
                'teams': [team, opponent],
                'winner': winner,
                'type': battle_data.get('type', 'Unknown'),
                'arena': battle_data.get('arena', {}).get('name', 'Unknown'),
                'duration': random.randint(120, 300)
            }
        except Exception as e:
            print(f"Erro ao formatar batalha: {str(e)}")
            return None
    
    def format_player(self, player_data):
        try:
            return {
                'tag': player_data['tag'],
                'name': player_data['name'],
                'level': player_data.get('expLevel', 1),
                'trophies': player_data['trophies'],
                'battle_count': player_data.get('battleCount', 0),
                'wins': player_data.get('wins', 0),
                'losses': player_data.get('losses', 0),
                'current_deck': [card['name'] for card in player_data.get('currentDeck', [])],
                'last_updated': datetime.now()
            }
        except Exception as e:
            print(f"Erro ao formatar jogador: {str(e)}")
            return None 