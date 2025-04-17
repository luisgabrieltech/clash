import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.clash_api import ClashRoyaleAPI
from database.mongodb import MongoDB
import time
from datetime import datetime, timedelta

class DataCollector:
    def __init__(self):
        self.api = ClashRoyaleAPI()
        self.db = MongoDB()
    
    def collect_player_data(self, player_tag):
        """Coleta dados de um jogador e suas batalhas"""
        player_data = self.api.get_player(player_tag)
        if not player_data:
            print(f"Erro ao obter dados do jogador {player_tag}")
            return
        
        formatted_player = self.api.format_player_data(player_data)
        self.db.insert_player(formatted_player)
        print(f"Dados do jogador {formatted_player['name']} salvos com sucesso!")
        
        battles = self.api.get_player_battles(player_tag)
        if battles:
            battles_saved = 0
            for battle in battles:
                formatted_battle = self.api.format_battle_data(battle)
                if formatted_battle:  
                    self.db.insert_battle(formatted_battle)
                    battles_saved += 1
            print(f"Salvas {battles_saved} batalhas para o jogador {formatted_player['name']}")
    
    def collect_data_for_period(self, player_tags, days=7):
        """Coleta dados para uma lista de jogadores em um período específico"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        for tag in player_tags:
            print(f"\nColetando dados para o jogador {tag}")
            self.collect_player_data(tag)
            time.sleep(1) 
    
    def close(self):
        """Fecha as conexões"""
        self.db.close()

if __name__ == "__main__":
    player_tags = [
        "#2R2RVPCLV",  # Kadu
    ]
    
    collector = DataCollector()
    try:
        collector.collect_data_for_period(player_tags)
        print("\nColeta de dados concluída com sucesso!")
    finally:
        collector.close() 