from database.mongodb import MongoDB
from api.clash_royale import ClashRoyaleAPI
from datetime import datetime

def convert_battle_to_db_format(battle_data, player_tag):
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
            'arena': battle_data.get('arena', {}).get('name', 'Unknown')
        }
    except Exception as e:
        print(f"Erro ao converter batalha: {str(e)}")
        return None

def populate_from_api():
    db = MongoDB()
    api = ClashRoyaleAPI()
    
    player_tags = [
        'QVGLY2QRY',
        'YL22YRYU9',
        '8UJQQJ9Y',
        'PQVVVLVJR',
        'P8R92C2RG',
        'RVJJ8V98',
        'G8CCCG99C',
        '2Y2YVYJ8',
        'PG8RYRG0',
        'Y2YPVV8'
    ]
    
    total_battles = 0
    
    for tag in player_tags:
        print(f"\nBuscando dados do jogador #{tag}...")
        
        player_info = api.get_player_info(tag)
        if player_info:
            player_data = {
                'tag': f"#{tag}",
                'name': player_info['name'],
                'level': player_info.get('expLevel', 1),
                'trophies': player_info['trophies'],
                'battle_count': player_info.get('battleCount', 0),
                'wins': player_info.get('wins', 0),
                'losses': player_info.get('losses', 0),
                'current_deck': [card['name'] for card in player_info.get('currentDeck', [])],
                'last_updated': datetime.now()
            }
            
            db.players.update_one(
                {'tag': player_data['tag']},
                {'$set': player_data},
                upsert=True
            )
            print(f"Jogador {player_info['name']} atualizado/inserido com sucesso!")
            
            battles = api.get_player_battles(tag)
            if battles:
                print(f"Encontradas {len(battles)} batalhas recentes.")
                for battle in battles:
                    try:
                        battle_data = convert_battle_to_db_format(battle, tag)
                        if battle_data:
                            existing_battle = db.battles.find_one({
                                'timestamp': battle_data['timestamp'],
                                'teams.player_tag': battle_data['teams'][0]['player_tag']
                            })
                            
                            if not existing_battle:
                                db.battles.insert_one(battle_data)
                                total_battles += 1
                                print(f"Nova batalha inserida! Tipo: {battle_data['type']}, Arena: {battle_data['arena']}")
                    except Exception as e:
                        print(f"Erro ao processar batalha: {str(e)}")
                        continue
                    
                print("Todas as batalhas foram processadas!")
            
    db.close()
    print(f"\nPopulação do banco de dados concluída! Total de novas batalhas inseridas: {total_battles}")

if __name__ == "__main__":
    populate_from_api() 