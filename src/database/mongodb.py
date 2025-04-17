from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class MongoDB:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client['clash_royale']
        
        self.players = self.db['players']
        self.battles = self.db['battles']
        self.decks = self.db['decks']
        
    def insert_player(self, player_data):
        return self.players.insert_one(player_data)
    
    def insert_battle(self, battle_data):
        return self.battles.insert_one(battle_data)
    
    def insert_deck(self, deck_data):
        return self.decks.insert_one(deck_data)
    
    def get_player(self, player_tag):
        return self.players.find_one({'tag': player_tag})
    
    def get_battle(self, battle_id):
        return self.battles.find_one({'_id': battle_id})
    
    def get_deck(self, deck_id):
        return self.decks.find_one({'_id': deck_id})
    
    def close(self):
        self.client.close() 