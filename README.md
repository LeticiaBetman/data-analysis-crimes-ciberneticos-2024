# 📊 Análise de Operações Policiais — Brasil 2024

Este projeto realiza uma análise exploratória dos dados de operações policiais no Brasil ao longo de 2024.  
O script processa dados em formato Parquet, calcula estatísticas, detecta outliers, gera indicadores avançados e cria gráficos automáticos para apoiar estudos e apresentações.

---

## 🧠 Funcionalidades

O script gera automaticamente:

### ✔️ Estatísticas descritivas  
- Informações gerais de todas as variáveis numéricas e categóricas.

### ✔️ Detecção de Outliers  
Usando o método IQR para:  
- `qtd_de_operacoes`  
- `prisoes_em_flagrante`  
- `mbas_expedidos`

### ✔️ Indicadores Avançados  
- **Eficiência:** prisões por operação  
- **Vítimas por operação:** casos de abuso resgatados / operações

### ✔️ Geração Automática de Gráficos  

#### 📈 Tendência Mensal (com média móvel)
- Tendência de operações ao longo do ano  
- Média móvel de 3 meses (MM3)

#### 🟦 Z-Score de Operações por UF
- Identifica estados acima/abaixo da média nacional

#### ⚙️ Eficiência Média por Estado
- Relação Prisões / Operações

#### 🗺️ Total de Operações por UF
- Gráfico vertical  
- Gráfico horizontal (para visualização mais limpa)

Todos os gráficos são salvos automaticamente na pasta `graficos/`.

---

## 🚀 Como Executar

### 1️⃣ Instale as dependências

```bash
pip install pandas numpy matplotlib pyarrow
```

### 2️⃣ Verifique se o arquivo de dados está no local correto
outputs/crimes_2024_clean.parquet

### 3️⃣ Execute o script
python analise_operacoes.py


Após a execução, os gráficos estarão disponíveis em:

graficos/

### 🧩 Tecnologias Utilizadas

- Python 3.x
- Pandas
- NumPy
- Matplotlib
- PyArrow (para leitura do Parquet)

📌 Observações

O projeto foi estruturado com funções separadas para manter clareza e organização.

Caso queira alterar o arquivo de entrada ou o diretório de saída, basta modificar as constantes no início do script:

INPUT = "outputs/crimes_2024_clean.parquet"
OUTPUT_DIR = "graficos"

🧑‍💻 Autora

Projeto desenvolvido por Letícia Rodrigues Betman.
Aberto para melhorias, sugestões e contribuições!
