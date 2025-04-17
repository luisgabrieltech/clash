import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class ClashRoyaleAPI:
    def __init__(self):
        self.api_key = os.getenv('CLASH_ROYALE_API_KEY')
        self.base_url = 'https://api.clashroyale.com/v1'
        self.headers = {'Authorization': f'Bearer {self.api_key}'}
    
    def get_player_info(self, player_tag):
        player_tag = player_tag.replace('#', '')
        url = f"{self.base_url}/players/%23{player_tag}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_player_battles(self, player_tag):
        player_tag = player_tag.replace('#', '')
        url = f"{self.base_url}/players/%23{player_tag}/battlelog"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_cards(self):
        url = f"{self.base_url}/cards"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        return None 