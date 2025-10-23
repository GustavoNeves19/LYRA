# 🎓 LYRA: Analisador de Regressão de Aprendizagem e Rendimento

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-LangChain-green)](https://www.langchain.com/)
[![Modelo LLM](https://img.shields.io/badge/Modelo-Gemini%202.5%20Flash-red)](https://ai.google.dev/gemini-api/docs/models)
[![Interface](https://img.shields.io/badge/Interface-Streamlit-orange)](https://streamlit.io/)

## 🌟 O Que É LYRA?

**LYRA (Analisador de Regressão de Aprendizagem e Rendimento)** é um sistema de **IA** projetado para automatizar a interpretação e a documentação de análises estatísticas complexas. Ele atua como um **Agente Inteligente** que transforma dados brutos de modelos de regressão, Análise de Variância (ANOVA) e Desejabilidade em relatórios técnicos detalhados e prontos para uso.

O projeto utiliza o poder de contexto longo do **Gemini 2.5 Flash** para criar documentações precisas e personalizadas, eliminando a tediosa tarefa de escrita técnica.

---

## 💡 Papel e Funcionalidades

O objetivo principal do LYRA é otimizar o fluxo de trabalho de cientistas de dados, engenheiros e pesquisadores ao focar na automação de:

| Papel/Meta | Funcionalidade Chave |
| :--- | :--- |
| **Análise de Dados** | Carrega dados, executa Análise de Regressão e ANOVA (usando pacotes estatísticos Python). |
| **Geração de Relatório** | Utiliza **Agentes Inteligentes** (via LangChain e Gemini) para interpretar os resultados estatísticos em JSON. |
| **Saída Técnica** | Gera um relatório final em Português com linguagem clara, incluindo: Fórmulas do Modelo, Tabelas ANOVA, Métricas ($R^2$, LoF) e Análise de Desejabilidade. |
| **Interface** | Apresenta os resultados de forma interativa através de uma interface Streamlit. |

---

## 🧠 Conceitos Fundamentais de Análise

O LYRA é especializado em projetos de Planejamento de Experimentos (DOE) e Regressão. A seguir, detalhamos os processos estatísticos e os modelos utilizados pelo Agente Inteligente:

### 📊 Gráfico de Pareto (Visualização de Significância)

Uma representação gráfica da **ANOVA** que ilustra a contribuição relativa de cada fator (termo) para a variação total do modelo.  
Ele ordena os termos pela magnitude da **Soma dos Quadrados (sum_sq)**, destacando o princípio de **Pareto** — poucos fatores são responsáveis pela maior parte do efeito.

#### 💡 Cenário de Aplicação  
Usado para a **Seleção de Features**, permitindo ao usuário identificar rapidamente quais fatores são mais importantes e quais podem ser descartados (**redução do modelo**).

#### 🎯 Resultado Esperado  
Um **gráfico de barras horizontais** onde termos significativos (p-valor ≤ 0.10) são destacados com uma cor diferente e uma **linha de corte (Corte de Significância)** é exibida.

![Imagem de Gráfico de Pareto com linha de corte e barras coloridas](./img/Grafico-Pareto.png)


## 📈 Modelo Polinomial (Regressão)

#### 🔍 O que é  
Um **modelo de regressão** é ajustado para descrever a relação entre variáveis de entrada (**fatores**) e uma variável de saída (**resposta**).  
O **modelo polinomial** é uma extensão da regressão linear que inclui termos de ordem superior, como **termos quadráticos e de interação**, para modelar **curvaturas** e **efeitos combinados**.

#### 💡 Cenário de Aplicação  
Ideal para **otimização de processos**, onde o resultado (por exemplo, rendimento ou qualidade) é influenciado por múltiplos fatores — como **tempo**, **temperatura** e **concentração**.  
Esse modelo auxilia a **encontrar o ponto ideal de operação**.

#### 🎯 Resultado Esperado  
Uma **equação matemática concisa** que permite **prever o valor da variável de saída (Y)** com base em quaisquer valores das **variáveis de entrada (X)**.
#### 🧮 Fórmula do Modelo Ajustado

$$
\hat{Y} = 45.1347 
- 0.2010\,(\text{tempo\_shaker}) 
+ 0.0010\,(\text{tempo\_shaker}^2) 
- 2.9841\,(\text{tempo\_ultrassom}) 
+ 2.2206\,(\text{temperatura}) 
+ 0.0147\,(\text{tempo\_shaker} \times \text{tempo\_ultrassom}) 
- 0.0134\,(\text{tempo\_shaker} \times \text{temperatura})
$$


![Imagem do Modelo Polinomial do Planejamento M1](./img/Modelo-Polinomial.png)



## 📊 Análise de Variância (ANOVA)

### 🔍 O que é  
É o **método estatístico** usado para decompor a variabilidade total nos dados, isolando a contribuição de cada termo do modelo (**fatores, interações, quadráticos**).  
O **LYRA** utiliza a ANOVA para determinar quais fatores são estatisticamente **significativos** para a variável de saída.

### 💡 Cenário de Aplicação  
Aplicada **imediatamente após o ajuste do Modelo Polinomial**, a ANOVA testa a **validade estatística do modelo**.  
O **Gráfico de Pareto** é uma representação visual inicial dessa análise, destacando a **magnitude da contribuição de cada fator**.

### 🎯 Resultado Esperado  
Uma **tabela de resultados** contendo:  
- **Soma dos Quadrados (SQ)**  
- **Graus de Liberdade (gl)**  
- **Valor F**  
- **p-valor** de cada termo  

Um **p-valor baixo (≤ 0.10)** indica que o termo é **estatisticamente significativo**.

![Imagem da ANOVA do  Planejamento M1](./img/Anova.png)

## Métricas de Qualidade do Modelo (R², LoF)

O LYRA calcula várias métricas para avaliar a qualidade preditiva do modelo final:

| Métrica | Conceito | Resultado Esperado |
| :--- | :--- | :--- |
| **$R^2$ (%)** | Coeficiente de determinação. Indica a porcentagem da variabilidade total dos dados que é explicada pelo modelo. | Quanto mais próximo de $100\%$, melhor o ajuste do modelo aos dados. |
| **Significância** | Baseado no teste F global. Indica se o modelo, como um todo, tem poder preditivo relevante. | O resultado deve ser **`True`** (Significativo). |
| **Predição Ajustada (LoF)** | *Lack-of-Fit* (LoF). Mede se o modelo é capaz de prever corretamente os dados em relação ao erro puro (Pure Error - PE). | O resultado deve ser **`True`** (Predição Ajustada), indicando que o modelo não falha em se ajustar à curvatura dos dados. |

## 🎯 Desejabilidade Global (Otimização)

### 🔍 O que é  
A **Desejabilidade** é uma técnica de **otimização multivariada** que transforma as respostas de múltiplas variáveis em um **único índice de desempenho**.  
O **LYRA** realiza uma **Desejabilidade Unidirecional** — ou seja, busca por **valores máximos** da variável de resposta com base nas predições do modelo.

### 💡 Cenário de Aplicação  
Aplicada para **encontrar a combinação ideal de fatores de entrada** (por exemplo, tempo e temperatura) que **maximiza a resposta** dentro de um **intervalo de desejabilidade pré-definido pelo usuário**.  
É uma etapa essencial na **fase final de otimização** do processo.

### 📈 Resultado Esperado  
Uma **tabela com as combinações de fatores** que produzem os **maiores valores de desejabilidade**, indicando o **ponto de operação ideal** do processo.  
Esses resultados servem como base para **decisões experimentais e ajustes operacionais**.


---

## 💻 Tecnologias Envolvidas

* **LLM Core (IA):** Google **Gemini 2.5 Flash** (via API)
* **Orquestração de Agentes:** **LangChain** (usado para estruturar o prompt e a comunicação com a API).
* **Ambiente:** Python 3.10+
* **Interface do Usuário:** **Streamlit** (para prototipagem e UI interativa).
* **Estatística:** `statsmodels` (ANOVA, OLS), `numpy`, `pandas`.
-----

## 📁 Estrutura do Projeto

A lógica do projeto é segregada para garantir modularidade e organização:

```
LYRA/
├── .env                  # Chaves secretas (GOOGLE_API_KEY, etc.)
├── app.py                # Ponto de entrada da aplicação (Interface Streamlit)
├── requirements.txt      # Lista de dependências do Python
├── src/                  # MÓDULOS DE LÓGICA
│   ├── llm_api.py        # Módulo de LLM: Contém a lógica de prompt (generate_final_prompt) e a chamada de API (get_llm_response)
│   ├── data_processing.py# Módulo de Dados: Contém as funções de carregamento, análise (ANOVA/Regressão) e deseabilidade.
│   └── __init__.py       # Marca 'src' como um pacote Python
├── data/                 # Armazenamento de dados
│   └── raw/              # Dados brutos de entrada
└── README.md
```

-----

## 🚀 Como Usar (Setup)

Siga os passos para configurar e executar o projeto em seu ambiente virtual:

### 1\. Clonar o Repositório

```bash
git clone https://github.com/GustavoNeves19/LYRA.git
cd LYRA
```

### 2\. Configurar o Ambiente

Certifique-se de que seu ambiente virtual (`venv` ou `conda`) está ativo.

```bash
# Se estiver usando venv:
python -m venv .venv
.\.venv\Scripts\activate  # (Windows)
source .venv/bin/activate # (Linux/macOS)
```

### 3\. Instalar Dependências

Instale todos os pacotes necessários:

```bash
pip install -r requirements.txt
```

### 4\. Configurar a API Key

Crie um arquivo chamado **`.env`** no diretório raiz do projeto e adicione sua chave de API do Gemini:

```
# Conteúdo do arquivo .env
GOOGLE_API_KEY="SUA_CHAVE_GEMINI_AQUI"
```

### 5\. Executar a Aplicação

Inicie a aplicação Streamlit no terminal:

```bash
streamlit run app.py
```

-----

## 📈 Resultados Mensuráveis e Tangíveis

O LYRA foi desenvolvido para fornecer valor claro e quantificável em projetos de análise estatística:

| Métrica de Valor | Descrição | Ganho Tangível |
| :--- | :--- | :--- |
| **Redução do Tempo de Relatório** | Tempo gasto na redação e formatação de relatórios técnicos de ANOVA. | **Redução de 80%** no tempo de documentação por modelo (de 30 min. para \< 5 min.). |
| **Aumento de Qualidade (Coerência)** | Consistência e precisão das tabelas e interpretações estatísticas. | **Taxa de erro ou inconsistência documental próxima a 0%**, mantendo a terminologia técnica padrão. |
| **Capacidade de Contexto** | Habilidade de processar e resumir grandes volumes de dados de análise. | Suporte nativo para geração de relatórios de **15.000 tokens** ou mais (usando o contexto longo do Gemini). |
| **Eficiência da Análise** | Otimização do tempo de cientistas de dados. | Permite que o analista passe de **foco em escrita** para **foco em otimização de modelo**. |

-----


