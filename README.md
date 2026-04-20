# 🎓 LYRA

> Sistema inteligente para análise estatística automatizada de planejamentos experimentais, com geração de relatórios técnicos em português usando IA.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-orange)](https://streamlit.io/)
[![LLM](https://img.shields.io/badge/LLM-Gemini%202.5%20Flash-red)](https://ai.google.dev/)
[![Orquestração](https://img.shields.io/badge/Orquestração-LangChain-green)](https://www.langchain.com/)

---

## 📌 Sobre o projeto

O **LYRA** é uma aplicação desenvolvida para automatizar a interpretação de resultados estatísticos oriundos de **Planejamento de Experimentos (DOE)**, com foco em:

- ajuste de **modelos de regressão polinomial**
- geração de **ANOVA**
- seleção automática de **features significativas**
- avaliação da qualidade preditiva do modelo
- execução de **desejabilidade global**
- geração de **relatórios técnicos automatizados com IA**

A proposta do projeto é reduzir o esforço manual de análise e documentação técnica, transformando saídas estatísticas em relatórios claros, estruturados e reutilizáveis.

---

## 🎯 Objetivo

O principal objetivo do LYRA é apoiar pesquisadores, analistas e profissionais que trabalham com experimentação e otimização de processos, automatizando etapas que normalmente exigem:

- interpretação estatística manual
- consolidação de métricas do modelo
- identificação de variáveis relevantes
- análise de preditividade
- elaboração de relatórios técnicos

Com isso, o usuário passa mais tempo analisando decisões e menos tempo escrevendo documentação.

---

## 🚀 Principais funcionalidades

### 1. Upload e preparação de dados

O sistema permite o envio de arquivos **CSV** e **XLSX**, realizando:

- leitura dos dados
- limpeza automática dos nomes das colunas
- conversão numérica
- separação entre variáveis independentes e dependentes

### 2. Ajuste do modelo estatístico

Para cada variável resposta, o LYRA:

- monta um modelo com termos lineares, quadráticos e de interação
- ajusta regressão via **OLS**
- calcula a **ANOVA**
- identifica os termos estatisticamente significativos

### 3. Geração do gráfico de Pareto

O sistema gera visualizações para apoiar a leitura da importância relativa dos termos do modelo, destacando:

- soma dos quadrados
- significância estatística
- linha de corte de significância

### 4. Redução automática do modelo

Após avaliar os p-valores, o sistema:

- remove termos não significativos
- ajusta um modelo reduzido
- preserva apenas as features relevantes

### 5. Avaliação de qualidade do modelo

O LYRA calcula métricas como:

- **R²**
- **R² máximo**
- **F_reg**
- **F_tab_reg**
- **F_lof**
- **F_tab_lof**
- **Significativo**
- **Predição Ajustada (LoF)**

### 6. Desejabilidade global

Se o modelo atender ao critério mínimo de qualidade, o sistema executa uma etapa de otimização por desejabilidade, permitindo:

- definição de intervalo desejável
- definição da densidade de busca
- geração dos melhores cenários dentro do espaço experimental

### 7. Geração de relatório com IA

Ao final da análise, o projeto utiliza **LangChain + Gemini 2.5 Flash** para transformar os resultados em um relatório técnico em português, com:

- sumário por variável
- tabela ANOVA
- interpretação do modelo
- métricas
- cenários de otimização
- texto final estruturado

---

## 🧠 Fluxo da aplicação

```text
Upload do arquivo
   ↓
Limpeza e preparação dos dados
   ↓
Identificação de variáveis independentes e dependentes
   ↓
Ajuste do modelo completo
   ↓
ANOVA + seleção de features significativas
   ↓
Ajuste do modelo reduzido
   ↓
Avaliação de R², significância e LoF
   ↓
Execução de desejabilidade (quando aplicável)
   ↓
Geração de relatório final com IA
```

---

## 📊 Técnicas e conceitos aplicados

O projeto trabalha com conceitos estatísticos e analíticos como:

- DOE (Design of Experiments)
- Regressão polinomial
- ANOVA
- Seleção de variáveis significativas
- Lack-of-Fit (LoF)
- Desejabilidade unidirecional
- Otimização de respostas

---

## 🛠️ Tecnologias utilizadas

### Interface

- Streamlit

### Processamento e análise de dados

- pandas
- numpy
- matplotlib
- statsmodels
- scipy

### IA e geração textual

- LangChain
- Google Gemini 2.5 Flash
- langchain-google-genai

### Configuração

- python-dotenv

---

## 📁 Estrutura do projeto

```text
LYRA/
├── app.py
├── requirements.txt
├── README.md
├── .env
├── src/
│   ├── __init__.py
│   ├── llm_api.py
│   └── analysis_pipeline.py
└── img/
    ├── Main/
    ├── Planejamento-A1/
    └── Planejamento B1/
```

### Descrição dos arquivos principais

`app.py`

Arquivo principal da aplicação Streamlit. Responsável por:

- renderizar a interface
- receber o arquivo do usuário
- executar o pipeline de análise
- acionar a geração do relatório final com IA

`src/analysis_pipeline.py`

Contém a lógica estatística central do projeto:

- carregamento e limpeza dos dados
- ajuste dos modelos
- geração da ANOVA
- seleção de features
- cálculo das métricas
- desejabilidade
- pipeline principal de análise

`src/llm_api.py`

Responsável pela integração com o modelo de linguagem:

- carrega a variável `GOOGLE_API_KEY`
- inicializa o Gemini
- monta o prompt técnico
- envia os resultados da análise para geração do relatório

---

## ⚙️ Requisitos

- Python 3.10 ou superior
- chave válida da API do Google Gemini
- ambiente virtual recomendado

---

## 🔐 Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
GOOGLE_API_KEY="SUA_CHAVE_AQUI"
```

---

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/GustavoNeves19/LYRA.git
cd LYRA
```

### 2. Crie e ative um ambiente virtual

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure a chave da API

Crie o arquivo `.env` conforme mostrado acima.

### 5. Execute a aplicação

```bash
streamlit run app.py
```

---

## 🧪 Formato esperado dos dados

O sistema espera um arquivo com estrutura compatível com o pipeline atual.

### Regras gerais

- a leitura usa `header=1`, então o cabeçalho efetivo deve estar na segunda linha
- deve existir uma coluna chamada `Ensaio`
- as 3 colunas após `Ensaio` são tratadas como variáveis independentes
- as colunas restantes são consideradas variáveis dependentes
- os dados devem ser numéricos ou convertíveis para numérico

### Exemplo conceitual

- Linha 1: metadados / título / observações
- Linha 2: `Ensaio | Tempo_Shaker | Tempo_Ultrassom | Temperatura | CFT | FT | ...`
- Linha 3+: dados experimentais

---

## 🖥️ Como usar

1. Execute a aplicação com `streamlit run app.py`
2. Faça upload do arquivo `.csv` ou `.xlsx`
3. Revise as variáveis identificadas na interface
4. Ajuste os parâmetros no menu lateral:
   - R² mínimo para rodar desejabilidade
   - intervalo de desejabilidade
   - número de pontos por variável-base
5. Clique em **“Iniciar Análise Completa e Gerar Relatório”**
6. Aguarde a execução das etapas estatísticas
7. Consulte:
   - gráficos
   - métricas
   - cenários otimizados
   - relatório final gerado pela IA
   - prompt técnico usado na geração

---

## 📈 Saídas geradas pelo sistema

O LYRA pode produzir, por variável resposta:

- lista de features significativas e não significativas
- tabela ANOVA serializada
- resumo textual do modelo reduzido
- métricas estatísticas
- mensagem sobre aplicabilidade da desejabilidade
- espaço de busca das variáveis
- função Python do modelo
- função Python da desejabilidade
- tabela com combinações otimizadas
- relatório final textual consolidado

---

## ✅ Regras de decisão implementadas

### Seleção de features

Termos são considerados significativos quando:

- `p-valor <= 0.10`

### Execução da desejabilidade

A desejabilidade só é executada quando:

- `R² >= limiar definido pelo usuário`

Caso contrário, o sistema retorna uma mensagem indicando que o processo de otimização não será executado.

---

## 📍 Diferenciais do projeto

- interface simples para uso prático
- automatização do fluxo estatístico
- integração entre análise quantitativa e geração textual
- relatórios técnicos em português
- apoio à tomada de decisão em processos experimentais
- redução do tempo de documentação manual

---

## ⚠️ Limitações atuais

- o pipeline atual assume exatamente 3 variáveis independentes
- o formato do arquivo precisa seguir a estrutura esperada pelo carregador
- a desejabilidade atual é unidirecional
- a execução do relatório depende de chave válida da API Gemini
- datasets muito fora do padrão podem exigir adaptação do pré-processamento

---

## 🔮 Melhorias futuras

Sugestões de evolução do projeto:

- suporte a número variável de fatores
- exportação do relatório em PDF ou DOCX
- histórico de análises
- painel de comparação entre respostas
- suporte a múltiplos tipos de desejabilidade
- validação mais robusta do arquivo de entrada
- logs de execução e rastreabilidade analítica
- deploy em ambiente web compartilhado

---

## 👨‍💻 Autor

Gustavo Neves

Projeto desenvolvido com foco em automação de análise estatística, otimização experimental e geração inteligente de documentação técnica.

---

## 📄 Licença

Defina aqui a licença do projeto.

Exemplo:

`MIT License`

Ou, se ainda não houver uma licença definida, mantenha:

`Todos os direitos reservados.`
