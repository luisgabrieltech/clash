# 🎮 Projeto Clash Royale - Análise de Dados

Este projeto implementa um sistema de análise de dados para o jogo Clash Royale, utilizando a API oficial do jogo e MongoDB como banco de dados.

## 📋 Pré-requisitos

- Python 3.8+
- MongoDB
- Chave de API do Clash Royale

## 🚀 Configuração

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```
MONGODB_URI=sua_uri_do_mongodb
CLASH_ROYALE_API_KEY=sua_chave_api
```

## 📁 Estrutura do Projeto

```
clash/
├── src/
│   ├── api/           # Integração com a API do Clash Royale
│   ├── database/      # Configuração e operações do MongoDB
│   ├── models/        # Modelos de dados
│   ├── queries/       # Consultas analíticas
│   └── web/           # Interface web (Dash)
├── tests/             # Testes unitários
├── .env              # Variáveis de ambiente
├── requirements.txt  # Dependências
└── README.md        # Este arquivo
```

## 🎯 Funcionalidades

- Coleta de dados da API do Clash Royale
- Armazenamento em MongoDB
- Consultas analíticas para balanceamento
- Interface web para visualização dos dados

## 📊 Consultas Implementadas

1. % de vitórias/derrotas com uma carta específica
2. Decks completos com mais de X% de vitórias
3. Derrotas com combo de cartas específicas
4. Vitórias com carta X (com critérios específicos)
5. Combos de N cartas com mais de Y% de vitórias

## 🚀 Como Executar

1. Inicie o servidor MongoDB
2. Execute o script de coleta de dados:
```bash
python src/api/collector.py
```

3. Inicie a interface web:
```bash
python src/web/app.py
```

## 📝 Licença

Este projeto está sob a licença MIT. 