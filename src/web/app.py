from flask import Flask, render_template, request
from src.queries.analytics import ClashAnalytics
from datetime import datetime, timedelta
import os
import traceback

app = Flask(__name__)

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def index():
    return render_template('analytics.html', results=None)

@app.route('/consulta', methods=['POST'])
def consulta():
    analytics = ClashAnalytics()
    
    try:
        data_inicio = datetime.fromisoformat(request.form.get('data_inicio'))
        data_fim = datetime.fromisoformat(request.form.get('data_fim'))
        
        carta = request.form.get('carta', 'The Log')
        taxa_minima = float(request.form.get('taxa_minima', 60))
        combo_str = request.form.get('combo', 'The Log, Miner')
        combo = [c.strip() for c in combo_str.split(',')]
        carta_especial = request.form.get('carta_especial', 'The Log')
        diff_trofeus = float(request.form.get('diff_trofeus', 25))
        num_cartas = int(request.form.get('num_cartas', 3))
        taxa_vitoria = float(request.form.get('taxa_vitoria', 55))
        
        results = {}
        
        if 'submit_consulta_1' in request.form:
            resultados = analytics.consulta_1_taxa_vitoria_carta(carta, data_inicio, data_fim)
            if resultados:
                total_partidas = sum(r['total_partidas'] for r in resultados)
                total_vitorias = sum(r['vitorias'] for r in resultados)
                taxa_vitoria_media = (total_vitorias / total_partidas * 100) if total_partidas > 0 else 0
                
                results['consulta_1'] = {
                    'carta': carta,
                    'taxa_vitoria': round(taxa_vitoria_media, 2),
                    'total_partidas': total_partidas,
                    'total_vitorias': total_vitorias,
                    'detalhes': resultados,
                    'periodo': {
                        'inicio': data_inicio.isoformat(),
                        'fim': data_fim.isoformat()
                    }
                }
            else:
                results['consulta_1'] = {
                    'erro': f'Nenhum resultado encontrado para a carta {carta} no período especificado'
                }
        elif 'submit_consulta_2' in request.form:
            results['consulta_2'] = analytics.consulta_2_decks_vencedores(taxa_minima, data_inicio, data_fim)
        elif 'submit_consulta_3' in request.form:
            results['consulta_3'] = analytics.consulta_3_derrotas_combo(combo, data_inicio, data_fim)
        elif 'submit_consulta_4' in request.form:
            resultados = analytics.consulta_4_vitorias_especiais(carta_especial, diff_trofeus, data_inicio, data_fim)
            
            if resultados:
                results['consulta_4'] = resultados
            else:
                results['consulta_4'] = {
                    'mensagem': 'Nenhuma vitória especial encontrada com os critérios especificados',
                    'criterios': {
                        'carta': carta_especial,
                        'diferenca_trofeus': diff_trofeus,
                        'periodo_inicio': data_inicio.isoformat(),
                        'periodo_fim': data_fim.isoformat()
                    }
                }
        elif 'submit_consulta_5' in request.form:
            results['consulta_5'] = analytics.consulta_5_combos_vencedores(num_cartas, taxa_vitoria, data_inicio, data_fim)
    except Exception as e:
        print(f"Erro na consulta: {str(e)}")
        print(traceback.format_exc())
        results['erro'] = {
            'mensagem': str(e),
            'traceback': traceback.format_exc()
        }
    finally:
        analytics.close()
    
    return render_template('analytics.html', results=results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 