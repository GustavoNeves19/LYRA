import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np  


# 1. Funções do LLM (Agente Inteligente)
from src.llm_api import generate_final_prompt, get_llm_response

# 2. Funções do Pipeline de Análise e Desejabilidade
from src.analysis_pipeline import (
    load_and_clean_data, 
    plot_pareto, 
    selecionar_features_significativas, 
    ajustar_modelo, 
    avaliar_modelo_anova, 
    run_global_desejabilidade_if_applicable,
)

# -------------------------------------------------------
# Título
# -------------------------------------------------------
st.title("LYRA: Análise de Fatores de Planejamento")
st.markdown("---")

# -------------------------------------------------------
# Entradas globais de configuração (químico informa)
# -------------------------------------------------------
with st.sidebar:
    st.header("Parâmetros do Processo")
    r2_min_percent = st.number_input(
        "R² mínimo (%) para rodar desejabilidade",
        min_value=0, max_value=100, value=50, step=1
    )
    d_min, d_max = st.slider(
        "Intervalo de desejabilidade",
        min_value=0.0, max_value=1.0, value=(0.65, 0.85), step=0.01
    )
    n_points = st.number_input(
        "Pontos por variável-base (linspace)",
        min_value=5, max_value=50, value=15, step=1
    )
    st.caption("O agente usará esses parâmetros na etapa de desejabilidade.")

# -------------------------------------------------------
# Etapa 1 — Carregamento
# -------------------------------------------------------
st.header("1. Carregamento e Preparação dos Dados")
uploaded_file = st.file_uploader("Escolha um arquivo Excel/CSV", type=["csv", "xlsx"])

if uploaded_file:
    # CHAMADA ATUALIZADA: load_and_clean_data vem de src.analysis_pipeline
    df, independent_vars, dependent_vars = load_and_clean_data(uploaded_file)

    if df is not None and len(df):
        st.success("Dados carregados e limpos com sucesso!")
        st.subheader("Visualização do Dataset")
        st.dataframe(df.head())

        st.subheader("Variáveis Identificadas")
        st.write("Variáveis Independentes:", independent_vars) 
        st.write("Variáveis Dependentes:", dependent_vars)

        st.markdown("---")
        st.header("2. Orquestração e Análise Automatizada")
        st.info("O agente irá agora executar as análises para todas as variáveis dependentes.")

        if st.button("Iniciar Análise Completa e Gerar Relatório"):
            resultados_analises = []

            # Loop por variável alvo
            for target_var in dependent_vars:
                st.subheader(f"Analisando: {target_var}")

                # Features completas: termos lineares, quadráticos e interações
                # (assumindo exatamente 3 independentes)
                features_completas = [
                    independent_vars[0], f"I({independent_vars[0]}**2)",
                    independent_vars[1], f"I({independent_vars[1]}**2)",
                    independent_vars[2], f"I({independent_vars[2]}**2)",
                    f"{independent_vars[0]}:{independent_vars[1]}",
                    f"{independent_vars[0]}:{independent_vars[2]}",
                    f"{independent_vars[1]}:{independent_vars[2]}",
                ]
                
                # --- Inicialização de Variáveis ---
                # Garante que essas variáveis existam antes do bloco if/else
                summary = "Não foram encontradas features significativas para a variável. Nenhum modelo foi gerado."
                metricas = {}
                desejabilidade_block = {}
                
                # --- Pareto (modelo completo) ---
                modelo_completo, anova_sorted = ajustar_modelo(df, target_var, features_completas)
                
                # Gera e exibe o gráfico (plot_pareto usa o modelo para criar o gráfico)
                try:
                    plot_pareto(df, target_var, features_completas)
                    st.pyplot(plt.gcf())
                    plt.close() # Limpa o buffer
                except Exception as e:
                    st.warning(f"Não foi possível gerar o Gráfico de Pareto para {target_var}. Erro: {e}")


                # --- Seleção de features significativas ---
                significantes, nao_significantes, anova_df_temp = selecionar_features_significativas(modelo_completo)

                # --- Serialização da ANOVA (Modelo Completo/Pareto) ---
                # Esta serialização é feita incondicionalmente, usando o anova_df_temp
                anova_resultados_serializaveis = (
                    anova_df_temp.reset_index()
                    .rename(columns={"index": "term"})
                    # CORREÇÃO DE NAMEERROR: np.nan agora está definido
                    .replace({pd.NA: None, np.nan: None}) 
                    .to_dict("records")
                )


                # Caso NÃO haja features significativas: (usa os valores padrao/inicializados)
                if not significantes:
                    st.warning(f"Não foram encontradas features significativas para '{target_var}'. A análise se encerra aqui.")
                    # O 'summary' e 'desejabilidade_block' usam os valores iniciais (de "Não foram encontradas...")
                
                # Caso HAJA features significativas: (sobrescreve os valores)
                else:
                    # --- Modelo reduzido com as significantes ---
                    st.success(f"Features significativas encontradas: {', '.join(significantes)}")
                    modelo_reduzido, _ = ajustar_modelo(df, target_var, significantes)

                    # Summary textual do statsmodels
                    summary = modelo_reduzido.summary().as_text()

                    # --- Métricas ANOVA do modelo reduzido ---
                    metricas, anova_completa_final, params_summary = avaliar_modelo_anova(modelo_reduzido, df, target_var)

                    # --- Desejabilidade (dinâmica) ---
                    des_out = run_global_desejabilidade_if_applicable(
                        modelo_reduzido=modelo_reduzido,
                        df=df,
                        target=target_var,
                        d_interval=(d_min, d_max),
                        n_points=int(n_points),
                        s=1.0,
                        top_k=50,
                        r2_threshold=float(r2_min_percent) / 100.0,
                        direction="higher",
                        desej_col_name="desejabilidade"
                    )

                    # Exibe mensagem de desejabilidade na UI
                    st.info(des_out["mensagem"])
                    if des_out["aplica_desejabilidade"] and des_out["resultado_df"] is not None:
                        st.subheader("Top resultados no intervalo de desejabilidade:")
                        # O resultado_df é uma lista de dicts (serializável), converte para DF para exibição na UI
                        st.dataframe(pd.DataFrame(des_out["resultado_df"])) 

                    # Monta bloco de Desejabilidade
                    desejabilidade_block = {
                        "aplica": des_out["aplica_desejabilidade"],
                        "r2": des_out["r2"],
                        "mensagem": des_out["mensagem"],
                        "search_spaces": des_out["search_spaces"],
                        "modelo_funcao_py": des_out["model_function_code"],
                        "desejabilidade_funcao_py": des_out["desirability_function_code"],
                        "resultados": des_out["resultado_df"] # Já é serializável/lista
                    }

                # --- Agrega resultado desta variável ao JSON final ---
                # Todas as variáveis agora estão garantidas
                resultados_analises.append({
                    "variavel": target_var,
                    "pareto": {
                        "significativo": significantes,
                        "nao_significativo": nao_significantes
                    },
                    "anova_completa": anova_resultados_serializaveis,
                    "modelo_reduzido_summary": summary,
                    "metricas": metricas,
                    "desejabilidade": desejabilidade_block
                })

            # ---------------------------------------------------
            # Etapa 3 — Geração do relatório (LLM)
            # ---------------------------------------------------
            st.markdown("---")
            st.header("3. Geração do Relatório com IA")
            st.info("As análises foram concluídas. O agente está construindo o relatório final.")

            # generate_final_prompt e get_llm_response de src.llm_api
            prompt_template = generate_final_prompt(resultados_analises)

            # Garante que o spinner e a mensagem de sucesso sejam controlados
            with st.spinner("Aguarde. O Agente LYRA está processando e escrevendo o relatório com alta complexidade..."):
                response_text = get_llm_response(prompt_template, resultados_analises)

            # A MENSAGEM FINAL É EXIBIDA APÓS O SPINNER
            if response_text and not response_text.startswith("Erro:") and not response_text.startswith("AVISO:"):
                st.success("Relatório Concluído!")
            else:
                # Exibe a mensagem de erro ou aviso (retornado pelo llm_api.py)
                st.error(response_text)


            st.subheader("Relatório Final Gerado")
            # O Agente LLM retorna a mensagem de erro/aviso se a API falhar
            st.markdown(response_text) 

            st.subheader("Prompt Gerado (Para Verificação)")
            prompt_final = prompt_template.format(json_analises=json.dumps(resultados_analises, indent=2))
            st.text_area("Prompt", prompt_final, height=300)
