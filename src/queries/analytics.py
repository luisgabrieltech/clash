from src.database.mongodb import MongoDB
from datetime import datetime, timedelta

class ClashAnalytics:
    def __init__(self):
        self.db = MongoDB()
    
    def consulta_1_taxa_vitoria_carta(self, nome_carta, data_inicio, data_fim):
        pipeline = [
            {
                '$match': {
                    'timestamp': {'$gte': data_inicio, '$lte': data_fim}
                }
            },
            {
                '$unwind': '$teams'
            },
            {
                '$match': {
                    'teams.deck': nome_carta
                }
            },
            {
                '$project': {
                    'player_tag': '$teams.player_tag',
                    'is_winner': {'$eq': ['$winner', '$teams.player_tag']},
                    'deck': '$teams.deck'
                }
            },
            {
                '$group': {
                    '_id': '$player_tag',
                    'total_partidas': {'$sum': 1},
                    'vitorias': {'$sum': {'$cond': ['$is_winner', 1, 0]}}
                }
            },
            {
                '$project': {
                    'taxa_vitoria': {
                        '$multiply': [
                            {'$divide': ['$vitorias', '$total_partidas']},
                            100
                        ]
                    },
                    'total_partidas': 1,
                    'vitorias': 1
                }
            }
        ]
        return list(self.db.battles.aggregate(pipeline))
    
    def consulta_2_decks_vencedores(self, taxa_vitoria_min, data_inicio, data_fim):
        pipeline = [
            {
                '$match': {
                    'timestamp': {'$gte': data_inicio, '$lte': data_fim}
                }
            },
            {
                '$unwind': '$teams'
            },
            {
                '$project': {
                    'deck': '$teams.deck',
                    'player_tag': '$teams.player_tag',
                    'is_winner': {'$eq': ['$winner', '$teams.player_tag']},
                    'deck_str': {'$reduce': {
                        'input': '$teams.deck',
                        'initialValue': '',
                        'in': {'$concat': ['$$value', ',', '$$this']}
                    }}
                }
            },
            {
                '$group': {
                    '_id': '$deck_str',
                    'deck': {'$first': '$deck'},
                    'total_partidas': {'$sum': 1},
                    'vitorias': {'$sum': {'$cond': ['$is_winner', 1, 0]}}
                }
            },
            {
                '$project': {
                    'deck': 1,
                    'total_partidas': 1,
                    'vitorias': 1,
                    'taxa_vitoria': {
                        '$multiply': [
                            {'$divide': ['$vitorias', '$total_partidas']},
                            100
                        ]
                    }
                }
            },
            {
                '$match': {
                    'taxa_vitoria': {'$gte': taxa_vitoria_min},
                    'total_partidas': {'$gte': 2}
                }
            },
            {
                '$sort': {'taxa_vitoria': -1}
            }
        ]
        return list(self.db.battles.aggregate(pipeline))
    
    def consulta_3_derrotas_combo(self, cartas, data_inicio, data_fim):
        pipeline = [
            {
                '$match': {
                    'timestamp': {'$gte': data_inicio, '$lte': data_fim}
                }
            },
            {
                '$unwind': '$teams'
            },
            {
                '$match': {
                    'teams.deck': {'$all': cartas},
                    '$expr': {'$ne': ['$winner', '$teams.player_tag']}
                }
            },
            {
                '$group': {
                    '_id': {
                        'deck': '$teams.deck',
                        'player': '$teams.player_tag'
                    },
                    'total_derrotas': {'$sum': 1},
                    'arena': {'$first': '$arena'},
                    'tipo_batalha': {'$first': '$type'}
                }
            },
            {
                '$sort': {'total_derrotas': -1}
            }
        ]
        return list(self.db.battles.aggregate(pipeline))
    
    def consulta_4_vitorias_especiais(self, nome_carta, diferenca_trofeus_percentual, data_inicio, data_fim):
        pipeline = [
            {
                '$match': {
                    'timestamp': {'$gte': data_inicio, '$lte': data_fim},
                    'duration': {'$lt': 120}
                }
            },
            {
                '$unwind': '$teams'
            },
            {
                '$match': {
                    'teams.deck': nome_carta,
                    '$expr': {'$eq': ['$winner', '$teams.player_tag']}
                }
            }
        ]
        
        resultados = list(self.db.battles.aggregate(pipeline))
        
        if not resultados:
            return {
                'mensagem': 'Nenhuma vitória especial encontrada com os critérios especificados',
                'criterios': {
                    'carta': nome_carta,
                    'diferenca_trofeus': diferenca_trofeus_percentual,
                    'periodo_inicio': data_inicio.isoformat(),
                    'periodo_fim': data_fim.isoformat()
                }
            }
        
        resultados_filtrados = []
        for batalha in resultados:
            vencedor_trofeus = batalha['teams'].get('trophies', 0)
            vencedor_deck = batalha['teams'].get('deck', [])
            vencedor_tag = batalha['teams'].get('player_tag')
            
            pipeline_perdedor = [
                {
                    '$match': {
                        '_id': batalha['_id']
                    }
                },
                {
                    '$unwind': '$teams'
                },
                {
                    '$match': {
                        'teams.player_tag': {'$ne': vencedor_tag},
                        'teams.crowns': {'$gte': 2}
                    }
                }
            ]
            
            perdedor = list(self.db.battles.aggregate(pipeline_perdedor))
            if perdedor:
                perdedor = perdedor[0]['teams']
                perdedor_trofeus = perdedor.get('trophies', 0)
                
                if perdedor_trofeus > 0:
                    diferenca = ((perdedor_trofeus - vencedor_trofeus) / perdedor_trofeus) * 100
                    
                    if diferenca >= diferenca_trofeus_percentual:
                        resultado = {
                            'timestamp': batalha['timestamp'].isoformat(),
                            'arena': batalha.get('arena', ''),
                            'type': batalha.get('type', ''),
                            'duration': batalha.get('duration', 0),
                            'vencedor': {
                                'tag': vencedor_tag,
                                'deck': vencedor_deck,
                                'trofeus': vencedor_trofeus
                            },
                            'perdedor': {
                                'tag': perdedor.get('player_tag', ''),
                                'deck': perdedor.get('deck', []),
                                'trofeus': perdedor_trofeus,
                                'torres': perdedor.get('crowns', 0)
                            },
                            'diferenca_trofeus': round(diferenca, 2)
                        }
                        resultados_filtrados.append(resultado)
        
        if not resultados_filtrados:
            return {
                'mensagem': 'Nenhuma vitória especial encontrada com os critérios especificados',
                'criterios': {
                    'carta': nome_carta,
                    'diferenca_trofeus': diferenca_trofeus_percentual,
                    'periodo_inicio': data_inicio.isoformat(),
                    'periodo_fim': data_fim.isoformat()
                }
            }
        
        return resultados_filtrados
    
    def consulta_5_combos_vencedores(self, num_cartas, taxa_vitoria_min, data_inicio, data_fim):
        pipeline = [
            {
                '$match': {
                    'timestamp': {'$gte': data_inicio, '$lte': data_fim}
                }
            },
            {
                '$unwind': '$teams'
            },
            {
                '$project': {
                    'deck': '$teams.deck',
                    'is_winner': {'$eq': ['$winner', '$teams.player_tag']},
                    'arena': 1,
                    'type': 1
                }
            },
            {
                '$unwind': '$deck'
            },
            {
                '$group': {
                    '_id': '$deck',
                    'total_partidas': {'$sum': 1},
                    'vitorias': {'$sum': {'$cond': ['$is_winner', 1, 0]}},
                    'arenas': {'$addToSet': '$arena'},
                    'tipos_batalha': {'$addToSet': '$type'}
                }
            },
            {
                '$project': {
                    'carta': '$_id',
                    'total_partidas': 1,
                    'vitorias': 1,
                    'taxa_vitoria': {
                        '$multiply': [
                            {'$divide': ['$vitorias', '$total_partidas']},
                            100
                        ]
                    },
                    'arenas': 1,
                    'tipos_batalha': 1
                }
            },
            {
                '$match': {
                    'taxa_vitoria': {'$gte': taxa_vitoria_min},
                    'total_partidas': {'$gte': 2}
                }
            },
            {
                '$sort': {'taxa_vitoria': -1}
            },
            {
                '$limit': num_cartas
            }
        ]
        return list(self.db.battles.aggregate(pipeline))
    
    def close(self):
        self.db.close() 