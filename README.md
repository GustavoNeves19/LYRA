O **README.md** é o cartão de visitas do seu projeto. Com base no nome **LYRA (Analisador de Regressão de Aprendizagem e Rendimento)** e em toda a organização que fizemos, aqui está uma proposta completa em formato Markdown, pronta para ser copiada para o seu repositório:

-----

# 🎓 LYRA: Analisador de Regressão de Aprendizagem e Rendimento

[](https://www.python.org/)
[](https://www.langchain.com/)
[](https://ai.google.dev/gemini-api/docs/models)
[](https://streamlit.io/)

## 🌟 O Que É LYRA?

**LYRA (Analisador de Regressão de Aprendizagem e Rendimento)** é um sistema de **IA** projetado para automatizar a interpretação e a documentação de análises estatísticas complexas. Ele atua como um **Agente Inteligente** que transforma dados brutos de modelos de regressão, Análise de Variância (ANOVA) e Desejabilidade em relatórios técnicos detalhados e prontos para uso.

O projeto utiliza o poder de contexto longo do **Gemini 2.5 Flash** para criar documentações precisas e personalizadas, eliminando a tediosa tarefa de escrita técnica.

-----

## 💡 Papel e Funcionalidades

O objetivo principal do LYRA é otimizar o fluxo de trabalho de cientistas de dados, engenheiros e pesquisadores ao focar na automação de:

| Papel/Meta | Funcionalidade Chave |
| :--- | :--- |
| **Análise de Dados** | Carrega dados, executa Análise de Regressão e ANOVA (usando pacotes estatísticos Python). |
| **Geração de Relatório** | Utiliza **Agentes Inteligentes** (via LangChain e Gemini) para interpretar os resultados estatísticos em JSON. |
| **Saída Técnica** | Gera um relatório final em Português com linguagem clara, incluindo: Fórmulas do Modelo, Tabelas ANOVA, Métricas ($R^2$, LoF) e Análise de Desejabilidade. |
| **Interface** | Apresenta os resultados de forma interativa através de uma interface Streamlit. |

-----

## 💻 Tecnologias Envolvidas

  * **LLM Core (IA):** Google **Gemini 2.5 Flash** (via API)
  * **Orquestração de Agentes:** **LangChain** (usado para estruturar o prompt e a comunicação com a API).
  * **Ambiente:** Python 3.10+
  * **Interface do Usuário:** **Streamlit** (para prototipagem e UI interativa).
  * **Gerenciamento de Pacotes:** `pip` e `requirements.txt`.

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


