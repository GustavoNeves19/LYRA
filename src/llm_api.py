# src/llm_api.py

import json
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.exceptions import OutputParserException 

# Importa a exceção correta do Google para capturar erros de API
from google.api_core.exceptions import GoogleAPICallError 

load_dotenv() 

# Carrega a chave de API do Gemini da variável de ambiente GOOGLE_API_KEY
api_key_gemini = os.getenv("GOOGLE_API_KEY") 

# Inicializa o modelo do Gemini com as configurações de contexto longo
llm = ChatGoogleGenerativeAI(
    # Modelo atual recomendado para velocidade e contexto longo
    model="gemini-2.5-flash", 
    google_api_key=api_key_gemini,
    # Define o limite máximo de tokens de saída para o relatório detalhado (15.000)
    max_output_tokens=15000, 
    # Temperatura baixa (0.2) para garantir que a saída seja técnica e pouco criativa
    temperature=0.2 
)

def generate_final_prompt(analises):
    """
    Cria o prompt dinâmico completo, estruturando a SystemMessage e a HumanMessage
    com as regras detalhadas de formatação para o relatório estatístico.
    """
    # Converte o dicionário de análises para uma string JSON formatada
    json_analises = json.dumps(analises, indent=2)
    
    # Define a persona e as instruções do Agente Inteligente LYRA
    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessage(content="Você é um assistente especializado em análise de dados e estatística. Sua tarefa é gerar relatórios técnicos detalhados com base em análises de variância (ANOVA) e modelos de regressão."),
        HumanMessage(content=f"""
                Gere um relatório analítico e técnico em português, com uma linguagem clara e precisa, consolidando as análises estatísticas a seguir.
                Aqui estão os resultados das análises, em formato JSON:
                ```json
                {json_analises}
                ```
                REGRAS DE FORMATAÇÃO (obrigatórias):

                Uma seção por variável: "### Análise: <variável>".

                Sumário (em linha única) com: R², Significativo?, Preditivo (LoF)?.

                Mapear de metricas: "R2 (%)", "Significativo", "Predicao Ajustada". Se ausente, "Não informado".

                Tabela ANOVA por termo (se houver anova_completa), com colunas:
                Termo | Soma dos Quadrados | gl | F | p-valor | Significativo?

                Mapear nomes possíveis: sum_sq→Soma dos Quadrados; df→gl; F→F; PR(>F) ou pvalue→p-valor.

                Significativo? = p-valor <= 0.10.

                Limitar a no MÁXIMO 8 linhas mais relevantes (se houver mais).

                Seleção de features:

                Se pareto.significativo estiver vazio/inexistente: escrever a linha
                "Não foram encontradas features significativas para <variável>. Nenhum modelo foi gerado."
                e PULAR Fórmula/Métricas/Desejabilidade para esta variável.

                Fórmula do modelo (somente se houver modelo):

                Mostrar fórmula em uma única linha legível com intercepto e termos (coef * termo).

                Se desejabilidade.modelo_funcao_py existir, exibir bloco de código com essa função.

                Métricas do modelo (se metricas existir): tabela compacta com
                R2 (%), R2_max (%), F_reg, F_tab_reg, F_lof, F_tab_lof, Significativo, Predicao Ajustada.

                Desejabilidade (se bloco desejabilidade existir):

                Se aplica for false/ausente: imprimir apenas mensagem.

                Se aplica for true:
                a) Mostrar mensagem.
                b) Se houver, listar "Espaços de busca" em tabela: Variável | min | max | n.
                c) Se houver, exibir blocos de código de modelo_funcao_py e desejabilidade_funcao_py.
                d) Se houver resultados, exibir TABELA com no MÁXIMO 20 linhas, ordenada como fornecida,
                mostrando colunas originais + "<target>_previsto" + "desejabilidade" (ou nome presente no JSON).

                NUNCA inventar valores/colunas. Manter nomes exatamente como no JSON.
        """)
    ])
                    
    return prompt_template


def get_llm_response(prompt_template, analises_data):
    """
    Envia o prompt formatado para o modelo Gemini e trata erros de API.
    """
    # Verifica se a inicialização do LLM falhou (geralmente por falta da chave de API)
    if not llm or not llm.client:
        return "Erro: O modelo de linguagem não foi inicializado. Verifique a chave de API."
    
    try:
        # Formata o prompt com os dados da análise (converte o template em mensagens de Chat)
        messages = prompt_template.format_messages(json_analises=json.dumps(analises_data, indent=2))
        
        # Invoca o modelo e retorna a resposta
        response = llm.invoke(messages)
        
        if response:
            return response.content
        else:
            return "Erro: A resposta da LLM está vazia."
            
    # Captura erros de comunicação com a API (ex: 404, cota excedida, chave inválida)
    except GoogleAPICallError as e:
        return f"Erro na API do Google (Gemini): {e}"
    # Captura erros de parsing do LangChain (se a saída não for texto simples, por exemplo)
    except OutputParserException as e:
        return f"Erro de formatação/parsing da saída: {e}"
    # Captura qualquer outra exceção genérica
    except Exception as e:
        return f"Erro desconhecido ao conectar com a IA: {e}"