### 🎯 **Objetivo Geral**

Criar uma base de dados NoSQL (MongoDB) para armazenar **batalhas**, **jogadores** e **decks**, visando possibilitar **consultas analíticas** para **balanceamento do jogo**.

---

### 🧩 **Contexto e Dados**

- **Tema**: Jogos com sistema de deck (Clash Royale/Hearthstone).
    
- **Decks**: Cada jogador monta um deck com 8 cartas (sem repetição).
    
- **Balanceamento**: Feito com base nas vitórias/derrotas ao longo do tempo.
    

Você poderá usar:

- A **API oficial do Clash Royale** (recomendado para dados reais).
    

---

### 🧱 **Modelagem esperada (MongoDB)**

Deve armazenar:

- **Jogadores**:
    
    - Nickname
        
    - Tempo de jogo
        
    - Nível
        
    - Troféus
        
- **Batalhas**:
    
    - Timestamp
        
    - Deck de cada jogador
        
    - Torres derrubadas de cada lado
        
    - Vencedor
        
    - Troféus de cada jogador no momento da partida
        

---

### 🔍 **Consultas obrigatórias**

1. **% de vitórias/derrotas com uma carta específica** em certo período.
    
2. **Decks completos com mais de X% de vitórias** em certo período.
    
3. **Derrotas com combo de cartas específicas** em certo período.
    
4. **Vitórias com carta X**, onde:
    
    - Vencedor tem **Z% menos troféus**
        
    - Duração da partida < 2min
        
    - Perdedor **derrubou 2+ torres**
        
5. **Combos de N cartas com mais de Y% de vitórias** em certo período.
    

---

### 🧠 **Consultas extras (3 novas)**

Você precisa propor mais 3 consultas relevantes. Exemplos possíveis:

- Média de troféus dos vencedores por carta.
    
- Cartas mais usadas em derrotas consecutivas.
    
- Cartas que aparecem mais em decks com 3 ou mais vitórias seguidas.
    

---

### 📊 **Entrega e Pontuação**

| Critério                             | Valor   |
| ------------------------------------ | ------- |
| Modelagem do BD                      | 1.5 pts |
| Consultas em linguagem do MongoDB    | 4 pts   |
| Acesso por linguagem de programação  | 1.5 pts |
| Interface gráfica para os resultados | 1.5 pts |
| Dados reais (API)                    | 1.5 pts |
| Bônus: Uso do MongoDB Atlas          | 1.0 pt  |

### ✅ **Resumo das responsabilidades**

- Montar o banco com dados reais ou simulados.
    
- Implementar as 5 consultas + 3 suas.
    
- Criar uma interface para visualizar os resultados.
    
- Fazer a apresentação nos dias **15/04 e 16/04**.