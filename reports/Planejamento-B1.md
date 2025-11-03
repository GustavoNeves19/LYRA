# 📝 Relatório Técnico Automatizado do Planejamento B1

## 🤖 Análise Estatística Acelerada por Agente de IA (Projeto LYRA)

Este documento apresenta o diagnóstico e a análise do **Planejamento B1**, classificado pelo **LYRA** como um **Cenário Crítico e de Baixa Preditividade**. O foco é identificar a falha estatística e documentar as métricas de risco.

### 🚀 Etapa 1: Carregamento e Identificação das Variáveis

(Conteúdo da Etapa 1 permanece inalterado)

![Imagem de Identificação de Variáveis: Identificacao-features.png](../img/Planejamento%20B1/Identificacao-features.png)

* **Variáveis Independentes (Fatores):** `Tempo_shaker_min`, `Tempo_Ultrassom_min`, `Temperatura_C`.
* **Variáveis Dependentes (Respostas):** `CFT_mg_GAE_g`, `FT_mg_QE_g`, `DPPH_umol_TE_g`, `ABTS_umol_TE_g`.

---

### 🧠 Etapa 2: Orquestração e Análise Automatizada (Gráficos de Pareto Críticos)

Nesta etapa, o LYRA executa a análise de significância (Pareto) e $R^2$ para todas as variáveis, resultando em um diagnóstico de risco generalizado.

#### 2.1 Análise Crítica da Variável `CFT_mg_GAE_g`

![Gráfico de Pareto: Pareto-CFT.png](../img/Planejamento%20B1/Pareto-CFT.png)

O Gráfico de Pareto mostra que a maioria dos termos está abaixo da linha de corte de significância, com barras de Soma dos Quadrados baixas.

* **Diagnóstico do LYRA:** A análise inicial indica: **"Não foram encontradas características significativas para 'CFT\_mg\_GAE\_g'. A análise se encerra aqui."** Não há base estatística para gerar um modelo.

#### 2.2 Análise Crítica da Variável `DPPH_umol_TE_g`

![Gráfico de Pareto: Pareto-DPPH.png](../img/Planejamento%20B1/Pareto-DPPH.png)

O termo mais influente é a interação `Tempo_shaker_min:Tempo_Ultrassom_min`.

* **Resultado e Diagnóstico:** $\text{R}^2 = \mathbf{0.34\%}$ (abaixo de 50%). O processo de desejabilidade **não será executado**.

#### 2.3 Análise Crítica da Variável `ABTS_umol_TE_g`

![Gráfico de Pareto: Pareto-ABTS.png](../img/Planejamento%20B1/Pareto-ABTS.png)

As variáveis `Tempo_Ultrassom_min` e `Temperatura_C` mostram alguma contribuição.

* **Resultado e Diagnóstico:** $\text{R}^2 = \mathbf{17.11\%}$ (abaixo de 50%). O processo de desejabilidade **não será executado**.

#### 2.4 Análise Crítica da Variável `FT_mg_QE_g`

![Gráfico de Pareto: Pareto-FT.png](../img/Planejamento%20B1/Pareto-FT.png)

A variável `Temperatura_C` é a mais proeminente, mas a contribuição total é baixa.

* **Resultado e Diagnóstico:** $\text{R}^2 = \mathbf{9.16\%}$ (abaixo de 50\%). O processo de desejabilidade **não será executado**.

---
### 🧠 Etapa 3: Análise de Variância (ANOVA) e Geração de Insights da IA

#### 3.1 Análise Crítica: `CFT_mg_GAE_g` (Falha Total de Significância)

![Tabela ANOVA CFT: Analise-Inicial--IA-CFT.png](../img/Planejamento%20B1/Analise-Inicial--IA-CFT.png)

* **Insight da IA:** A ANOVA completa mostra que **nenhum termo** (principal, quadrático ou de interação) alcançou significância ($\text{p-valor} \leq 0.10$). O $\text{p-valor}$ mais próximo é o de $\text{Temperatura\_C}$ (0.122), ainda assim não significativo.
* **Consequência:** O modelo não tem base estatística para ser gerado.

| Métrica | Valor | *Insight de Risco* |
| :--- | :--- | :--- |
| $\text{R}^2 (\%)$ | Não Informado | Modelo inválido; falta de ajuste. |
| **Significativo?** | Falso | A regressão não explica o modelo. |

#### 3.2 Análise Crítica: `DPPH_umol_TE_g` ($\text{R}^2 = 0.34\%$)

![Tabela ANOVA DPPH: Analise-Inicial-IA-DPPH.png](../img/Planejamento%20B1/Analise-Inicial-IA-DPPH.png)

![Fórmula e Métricas DPPH: Analise-Modelo-IA-DPPH.png](../img/Planejamento%20B1/Analise-Modelo-IA-DPPH.png)

* **Insight da IA:** O único termo minimamente significativo ($\text{p-valor} = 0.066$) é a interação **Tempo\_shaker\_min:Tempo\_Ultrassom\_min**. O baixo $\text{R}^2$ (apenas **0.34%**) mostra que, embora estatisticamente *existente*, esta interação é **irrelevante** na prática para a variação da resposta.
* **Modelo Gerado (Simplificado):**
    $$
    \text{DPPH\_umol\_TE\_g} = 66.0217 + (-0.0013 \times \text{Tempo\_shaker\_min:Tempo\_Ultrassom\_min})
    $$

#### 3.3 Análise Crítica: `FT_mg_QE_g` ($\text{R}^2 = 9.16\%$)

![Tabela ANOVA FT: Analise-Inicial-IA-FT.png](../img/Planejamento%20B1/Analise-Inicial-IA-FT.png)

![Fórmula e Métricas FT: Analise-modelo-IA-FT.png](../img/Planejamento%20B1/Analise-modelo-IA-FT.png)

* **Insight da IA:** O único termo significativo é a $\text{Temperatura\_C}$ ($\text{p-valor} = 0.055$). O $\text{R}^2$ de **9.16%** indica que $\text{Temperatura\_C}$ explica menos de 10% da variação total. O modelo limitado se resume a:
    $$
    \text{FT\_mg\_QE\_g} = 11.9558 + (0.1960 \times \text{Temperatura\_C})
    $$
* **Conclusão da IA:** A regressão é *Não Significativa* (`False`) no teste F global, apesar de o termo $\text{Temperatura\_C}$ ser individualmente significativo.

#### 3.4 Análise Crítica: `ABTS_umol_TE_g` ($\text{R}^2 = 17.11\%$)

![Tabela ANOVA ABTS: Analise-Inicial-IA-ABTS.png](../img/Planejamento%20B1/Analise-Inicial-IA-ABTS.png)

![Fórmula e Métricas ABTS: Analise-Modelo-IA-ABTS.png](../img/Planejamento%20B1/Analise-Modelo-IA-ABTS.png)

* **Insight da IA:** Esta resposta apresenta o maior número de termos significativos (incluindo $\text{Tempo\_Ultrassom\_min}$ e $\text{Temperatura\_C}$), mas ainda assim resulta em um $\text{R}^2$ de apenas **17.11%**.
* **Métricas de Risco:** O modelo é *Não Significativo* (`False`) e a $\text{Predicao Ajustada (LoF)}$ falhou (`False`). O LYRA confirma que o modelo é **inconfiável** e **não preditivo**.

---

### 🎯 Etapa 4: Otimização por Desejabilidade (Bloqueada)

O Agente de IA **bloqueia a Otimização** (Desejabilidade) em todas as variáveis, devido ao risco inerente de usar modelos com $\text{R}^2 < 50\%$ para prever o ponto ótimo de operação.

### ✅ Conclusão Crítica do Planejamento B1 pelo LYRA

O **Planejamento B1** é categorizado como um **Cenário de Risco Crítico e Falha Generalizada de Preditividade**.

* **Diagnóstico Final da IA:** A análise detalhada das ANOVAs revela que, mesmo onde há significância isolada (como em $\text{FT\_mg\_QE\_g}$ e $\text{ABTS\_umol\_TE\_g}$), a contribuição percentual dos fatores para a variação total do processo é negligenciável ($\text{R}^2$ máximo de 17.11%).
* **Recomendação do Sistema:** O sistema LYRA confirma que os fatores e/ou os limites escolhidos neste planejamento experimental **não são adequados** para modelar as respostas de maneira preditiva. **Recomenda-se uma revisão completa do planejamento,** focando na ampliação dos limites dos fatores ou na inclusão de novas variáveis que possam explicar a variação das respostas.
