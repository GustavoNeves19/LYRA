# src/analysis_pipeline.py

import itertools
import numpy as np
import pandas as pd
import streamlit as st
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import f
from matplotlib.patches import Patch
import matplotlib.pyplot as plt


# ==============================================================================
# 1. FUNÇÕES DE CARREGAMENTO E LIMPEZA DE DADOS (Migrado de data_loader.py)
# ==============================================================================

def clean_name(name):
    """Remove caracteres especiais e espaços de um nome de coluna."""
    name = str(name).strip()
    name = name.replace(' (min)', '_min').replace(' ºC', '_C').replace(' (mg GAE/g)', '_mg_GAE_g').replace(' ( mg QE/g)', '_mg_QE_g').replace(' (µmol TE/g)', '_umol_TE_g').replace(' ', '_').replace('.', '').replace('(', '').replace(')', '').replace('º', '')
    return name

def load_and_clean_data(file):
    """
    Lê um arquivo de dados, limpa nomes de colunas e identifica
    dinamicamente variáveis independentes e dependentes.
    """
    try:
        # Carrega o arquivo com a primeira linha de dados como cabeçalho
        if file.name.endswith('.xlsx'):
            # Ajuste: Header é geralmente a 2ª linha (índice 1) para dados de DOE
            df = pd.read_excel(file, header=1)
        else:
            df = pd.read_csv(file, header=1)
        
        # O DataFrame já está carregado corretamente a partir do header=1
        # Remoção da primeira linha duplicada, se o arquivo for XLSX/CSV padrão
        df = df.iloc[0:].copy() 
        
        # Limpa os nomes das colunas
        column_mapping = {col: clean_name(col) for col in df.columns}
        df.rename(columns=column_mapping, inplace=True)
        
        # Converte o DataFrame para tipo numérico, tratando erros e removendo NaN
        df = df.apply(pd.to_numeric, errors='coerce').dropna()
        
        # O "Ensaio" agora será o nosso ponto de referência para identificar
        # as variáveis independentes e dependentes de forma dinâmica
        ensaio_col_index = df.columns.get_loc('Ensaio')
        
        # As variáveis independentes são as que vêm logo depois da coluna Ensaio
        # Assume-se que há 3 independentes após 'Ensaio' (índices: +1, +2, +3)
        independent_cols = df.columns[ensaio_col_index + 1 : ensaio_col_index + 4].tolist()
        
        # As variáveis dependentes são as restantes (índices: +4 em diante)
        dependent_cols = df.columns[ensaio_col_index + 4:].tolist()
        
        return df, independent_cols, dependent_cols
    
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        st.info("Verifique se o arquivo possui a estrutura esperada (linha de cabeçalho correta e dados numéricos).")
        return None, None, None


# ==============================================================================
# 2. FUNÇÕES DE ANÁLISE ESTATÍSTICA (Migrado de analysis.py)
# ==============================================================================

# Nota: A função 'plot_pareto' foi mantida com o plot, mas não retorna o modelo reduzido. 
# Para uso no pipeline, usaremos 'selecionar_features_significativas' e 'ajustar_modelo'.

def plot_pareto(df, target: str, features: list, alpha=0.1):
    """Gera o gráfico de Pareto e retorna a tabela ANOVA (função de UI/Visualização)."""
    formula = target + " ~ " + " + ".join(features)
    modelo = ols(formula, data=df).fit()
    anova_df = sm.stats.anova_lm(modelo, typ=2).dropna()
    anova_df["significativo"] = anova_df["PR(>F)"] <= alpha
    anova_sorted = anova_df.sort_values("sum_sq", ascending=False)
    
    # Lógica de plotagem (Mantida, pois pode ser chamada pelo app.py)
    num_significativas = anova_sorted["significativo"].sum()
    cores = ["tab:blue" if sig else "lightgray" for sig in anova_sorted["significativo"]]
    
    plt.figure(figsize=(10, 6))
    plt.barh(anova_sorted.index, anova_sorted["sum_sq"], color=cores)
    plt.xlabel("Soma dos Quadrados (sum_sq)")
    plt.title(f"Gráfico de Pareto - Variável Resposta: {target.upper()}")
    plt.gca().invert_yaxis()
    plt.grid(False)
    
    if num_significativas < len(anova_sorted):
        plt.axhline(
            y=len(anova_sorted) - num_significativas + 0.5,
            color='red', linestyle='--', linewidth=2, label='Corte de Significância'
        )
        plt.legend(handles=[
            Patch(color='tab:blue', label='Significativo', alpha=0.7),
            Patch(color='lightgray', label='Não Significativo'),
            Patch(color='red', linestyle='--', label='Corte de Significância')
        ])
    plt.tight_layout()
    
    return anova_sorted # Retorna apenas a tabela ANOVA para fins de visualização

def selecionar_features_significativas(modelo, p_thresh=0.1):
    """Seleciona as features significativas e não significativas com base nos p-valores."""
    anova = sm.stats.anova_lm(modelo, typ=2).dropna()
    # Lista de termos significativos (incluindo o Intercept, se presente)
    significantes = anova[anova['PR(>F)'] <= p_thresh].index.tolist()
    # Termos não significativos
    insignificantes = anova[anova['PR(>F)'] > p_thresh].index.tolist()
    return significantes, insignificantes, anova

def ajustar_modelo(df, target, features):
    """Ajusta um modelo de regressão OLS e retorna o modelo e a ANOVA completa (ANOVA Typ 2)."""
    # Excluímos o Intercept da lista de features para evitar duplicação na fórmula OLS
    features = [f for f in features if f != 'Intercept']
    
    if not features:
        return None, None
        
    formula = target + " ~ " + " + ".join(features)
    modelo = ols(formula, data=df).fit()
    anova_df = sm.stats.anova_lm(modelo, typ=2)
    return modelo, anova_df

def extrair_variaveis_originais(modelo):
    """
    Extrai as variáveis originais utilizadas em um modelo statsmodels (considerando termos quadráticos e interações).
    """
    nomes = modelo.model.exog_names
    variaveis = set()
    for nome in nomes:
        if nome == "Intercept":
            continue
        elif nome.startswith("I("):
            termo = nome[2:-1]
            tokens = termo.replace("**", " ").split()
            # Pega o primeiro token como variável base
            variaveis.add(tokens[0])
        elif ":" in nome:
            # Adiciona ambas as partes da interação
            variaveis.update(nome.split(":"))
        else:
            variaveis.add(nome)
    return sorted(variaveis)

def avaliar_modelo_anova(modelo, df, target, alpha=0.10):
    """
    Calcula e retorna as métricas de qualidade do modelo em um dicionário.
    Inclui métricas de Falta de Ajuste (Lack-of-Fit - LoF).
    """
    df = df.copy()
    variaveis_originais = extrair_variaveis_originais(modelo)
    
    # 1. Agrupamento e Cálculo de Média
    # Agrupamento pelos níveis das variáveis originais (para calcular LoF/PE)
    try:
        grupos = df.groupby(variaveis_originais)
    except Exception:
        # Se as variáveis originais não formam grupos (ex: regressão contínua pura),
        # o cálculo LoF/PE não é apropriado, ou o agrupamento falha.
        # Retornamos métricas padrão sem LoF
        return {
            "R2 (%)": modelo.rsquared * 100, 
            "Significativo": modelo.f_pvalue <= alpha,
            "Predicao Ajustada": "Não Aplicável (dados contínuos)"
        }


    df["y_medio"] = grupos[target].transform("mean")
    df["y_predito"] = modelo.fittedvalues

    # 2. Cálculo das Somas dos Quadrados (SS)
    SSPE = np.sum((df[target] - df["y_medio"])**2) # Pure Error (Erro Puro)
    SSLoF = np.sum((df["y_medio"] - df["y_predito"])**2) # Lack of Fit (Falta de Ajuste)
    SSE = SSPE + SSLoF # Soma dos Quadrados do Erro (Residuo)
    SSR = np.sum((df["y_predito"] - df[target].mean())**2) # Soma dos Quadrados da Regressão
    SST = SSR + SSE # Soma dos Quadrados Total

    # 3. Graus de Liberdade (gl)
    N = len(df)
    r = grupos.ngroups # Número de grupos/níveis únicos
    p = len(modelo.params) # Número de parâmetros no modelo (incluindo intercepto)
    gl_PE = N - r # gl do Erro Puro
    gl_LoF = r - p # gl da Falta de Ajuste
    gl_Res = gl_PE + gl_LoF # gl do Resíduo (Erro)
    gl_Reg = p - 1 # gl da Regressão
    gl_Total = N - 1

    # 4. Quadrados Médios (MS)
    MSPE = SSPE / gl_PE if gl_PE > 0 else np.nan
    MSLoF = SSLoF / gl_LoF if gl_LoF > 0 else np.nan
    MSReg = SSR / gl_Reg if gl_Reg > 0 else np.nan
    MSRes = SSE / gl_Res if gl_Res > 0 else np.nan

    # 5. Testes F
    F_lof = MSLoF / MSPE if MSPE > 0 and not np.isnan(MSLoF) else np.nan
    F_tab_lof = f.ppf(1 - alpha, gl_LoF, gl_PE) if gl_PE > 0 and gl_LoF > 0 else np.nan
    F_reg = MSReg / MSRes if MSRes > 0 and gl_Reg > 0 else np.nan
    F_tab_reg = f.ppf(1 - alpha, gl_Reg, gl_Res) if gl_Res > 0 and gl_Reg > 0 else np.nan

    # 6. R²
    R2 = modelo.rsquared * 100 # R² do Modelo
    R2_max = (1 - (SSPE / SST)) * 100 if SST != 0 else np.nan # R² Máximo (Ajuste Ideal)

    metricas = {
        "R2 (%)": R2, "R2_max (%)": R2_max,
        "F_reg": F_reg, "F_tab_reg": F_tab_reg,
        "F_lof": F_lof, "F_tab_lof": F_tab_lof,
        # Lógica Booleana de Decisão
        "Significativo": bool(F_reg > F_tab_reg) if not np.isnan(F_reg) else False,
        "Predicao Ajustada": bool(F_lof < F_tab_lof) if not np.isnan(F_lof) else None
    }
    
    # Adicionar dados de ANOVA completa e resumo de parâmetros para o LLM
    # A tabela ANOVA completa (Tipo 2)
    anova_completa = sm.stats.anova_lm(modelo, typ=2).fillna(np.nan).to_dict("index")
    
    # Resumo de Parâmetros (Coeficientes)
    params_summary = modelo.params.to_dict()

    return metricas, anova_completa, params_summary


# ==============================================================================
# 3. FUNÇÕES DE DESEJABILIDADE (Migrado de desejabilidade.py)
# ==============================================================================

# ---------------------------
# Helpers de parsing do modelo
# ---------------------------

def _base_vars_from_model(modelo):
    """
    Extrai variáveis-base (originais) a partir de exog_names,
    tratando I(x**2) e interações a:b.
    """
    base = set()
    for name in modelo.model.exog_names:
        if name == "Intercept":
            continue
        if name.startswith("I("):
            inner = name[2:-1]  # ex: tempo**2
            var = inner.replace("**", " ").split()[0]
            base.add(var)
        elif ":" in name:
            a, b = name.split(":")
            base.add(a); base.add(b)
        else:
            base.add(name)
    return sorted(base)

def _prepare_design_df_from_base(grid_df, modelo, df_ref):
    """
    A partir de um DF com variáveis-base, cria as colunas exigidas pelo modelo
    (I(x**2), interações, etc.), preservando nomes idênticos aos do modelo.
    """
    X = grid_df.copy()

    # Garante que todas as variáveis-base existam
    for b in _base_vars_from_model(modelo):
        if b not in X.columns:
            if b in df_ref.columns:
                X[b] = df_ref[b].mean()
            else:
                X[b] = 0.0  # fallback

    # Cria termos do modelo
    for name in modelo.model.exog_names:
        if name == "Intercept":
            continue
        if name in X.columns:
            continue

        if name.startswith("I("):
            # exemplo: I(tempo**2)
            # Eval permite calcular termos como x**2 diretamente
            expr = name[2:-1]
            X[name] = eval(expr, {}, {col: X[col] for col in X.columns})
        elif ":" in name:
            a, b = name.split(":")
            if a not in X.columns and a in df_ref.columns:
                X[a] = df_ref[a].mean()
            if b not in X.columns and b in df_ref.columns:
                X[b] = df_ref[b].mean()
            X[name] = X[a] * X[b]
        else:
            if name not in X.columns:
                if name in df_ref.columns:
                    X[name] = df_ref[name].mean()
                else:
                    X[name] = 0.0

    # Reordenar (opcional)
    needed = [c for c in modelo.model.exog_names if c != "Intercept"]
    cols = [c for c in needed if c in X.columns] + [c for c in X.columns if c not in needed]
    return X[cols]

def _predict_from_base_grid(modelo, base_grid_df, df_ref):
    """
    Recebe DF com variáveis-base e retorna predições após construir termos.
    """
    design = _prepare_design_df_from_base(base_grid_df, modelo, df_ref)
    return modelo.predict(design)

# ---------------------------
# Funções de desejabilidade
# ---------------------------

def _desejabilidade_scaler(y, L, T, s=1.0, direction="higher"):
    """
    Desejabilidade unidirecional (0..1).
    direction: 'higher' (quanto maior melhor; s controla forma) ou 'between' (L..T ótimo).
    """
    y = float(y)
    if T == L:
        return 0.0
    # O seu código original foca em "higher", simplificando a lógica
    # para ser compatível com a função _make_desirability_function_code
    
    if y < L:
        return 0.0
    if y > T:
        return 1.0
    return ((y - L) / (T - L)) ** s

def _make_model_function_code(target, modelo):
    """
    Gera código Python de uma função do modelo:
    def modelo_<target>(x): ...  # x: dict com variáveis-base
    """
    lines = []
    fname = f"modelo_{target}".replace(" ", "_")
    lines.append(f"def {fname}(x):")
    lines.append("    \"\"\"")
    lines.append("    x: dict com variáveis-base (ex.: {'tempo_shaker': ..., 'tempo_ultrassom': ..., 'temperatura': ...})")
    lines.append("    Retorna a predição do modelo para os valores em x.")
    lines.append("    \"\"\"")
    intercept = float(modelo.params.get("Intercept", 0.0))
    lines.append(f"    y = {intercept:.10f}")

    base_vars = _base_vars_from_model(modelo)
    for name, coef in modelo.params.items():
        if name == "Intercept":
            continue
        coef = float(coef)
        if name.startswith("I("):
            inner = name[2:-1]  # ex: tempo_shaker**2
            expr = inner
            for b in base_vars:
                # Substitui a variável de coluna pela chave do dicionário de entrada
                expr = expr.replace(b, f"x['{b}']") 
            lines.append(f"    y += ({coef:.10f}) * ({expr})")
        elif ":" in name:
            a, b = name.split(":")
            lines.append(f"    y += ({coef:.10f}) * (x['{a}'] * x['{b}'])")
        else:
            lines.append(f"    y += ({coef:.10f}) * (x['{name}'])")

    lines.append("    return y")
    return "\n".join(lines)

def _make_desirability_function_code(target, L, T):
    """
    Gera código Python da função de desejabilidade (versão simplificada para 'higher'):
    def desejabilidade_<target>(y, L=<min>, T=<max>, s=1): ...
    """
    fname = f"desejabilidade_{target}".replace(" ", "_")
    return f"""def {fname}(y, L={L:.10f}, T={T:.10f}, s=1):
    \"\"\"
    Desejabilidade unidirecional para {target} (0..1).
    L: limite inferior (min observado no dataset)
    T: limite superior (max observado no dataset)
    s: parâmetro de forma (default=1)
    \"\"\"
    y = float(y)
    if T == L:
        return 0.0
    if y < L:
        return 0.0
    if y > T:
        return 1.0
    return ((y - L) / (T - L)) ** s
"""

def to_serializable(df_or_none):
    """
    Converte DataFrame ou None para um formato serializável em JSON, 
    substituindo NaN por None.
    """
    if df_or_none is None:
        return []
    if isinstance(df_or_none, pd.DataFrame):
        return df_or_none.replace({np.nan: None}).to_dict("records")
    return df_or_none

# ----------------------------------------
# Pipeline dinâmico para desejabilidade
# ----------------------------------------

def run_global_desejabilidade_if_applicable(
    modelo_reduzido,
    df,
    target,
    d_interval=(0.65, 0.85),
    n_points=15,
    s=1.0,
    top_k=50,
    r2_threshold=0.50,
    direction="higher",
    desej_col_name="desejabilidade"
):
    """
    Executa a desejabilidade para um target **apenas** se R² >= r2_threshold,
    e retorna o dicionário estruturado para o LLM.
    """
    if modelo_reduzido is None:
        return {
            "aplica_desejabilidade": False,
            "r2": 0.0,
            "mensagem": "Não há modelo ajustado para a variável.",
            "resultado_df": None,
        }
        
    r2 = float(modelo_reduzido.rsquared)  # 0..1
    if r2 < r2_threshold:
        return {
            "aplica_desejabilidade": False,
            "r2": r2,
            "mensagem": (
                f"A variável '{target}' possui R² = {r2:.2%} (< {r2_threshold:.0%}). "
                "O processo de desejabilidade não será executado."
            ),
            "model_function_code": None,
            "desirability_function_code": None,
            "search_spaces": {},
            "resultado_df": None,
        }

    # R² >= threshold → preparar tudo
    base_vars = _base_vars_from_model(modelo_reduzido)

    # Espaços de busca a partir do dataset
    search_spaces = {}
    for v in base_vars:
        if v in df.columns:
            vmin = float(df[v].min())
            vmax = float(df[v].max())
            if not np.isfinite(vmin) or not np.isfinite(vmax):
                continue
            if np.isclose(vmin, vmax):
                vmin -= 1e-6
                vmax += 1e-6
            search_spaces[v] = (vmin, vmax, int(n_points))

    # Combinações
    grids = [np.linspace(vmin, vmax, n) for (vmin, vmax, n) in search_spaces.values()]
    combos = list(itertools.product(*grids)) if grids else []

    # Limites L/T do target (mínimo e máximo observados)
    L = float(df[target].min())
    T = float(df[target].max())
    if not np.isfinite(L) or not np.isfinite(T):
        L, T = 0.0, 1.0
    if np.isclose(L, T):
        L -= 1e-6
        T += 1e-6

    # Mensagens & códigos
    model_code = _make_model_function_code(target, modelo_reduzido)
    desir_code = _make_desirability_function_code(target, L, T)

    if not combos:
        return {
            "aplica_desejabilidade": True,
            "r2": r2,
            "mensagem": (
                f"'{target}' tem R² = {r2:.2%} (≥ {r2_threshold:.0%}), "
                "mas não foi possível gerar espaço de busca das variáveis-base."
            ),
            "model_function_code": model_code,
            "desirability_function_code": desir_code,
            "search_spaces": search_spaces,
            "resultado_df": None,
        }

    base_grid_df = pd.DataFrame(combos, columns=base_vars)

    # Predição
    yhat = _predict_from_base_grid(modelo_reduzido, base_grid_df, df)

    # Desejabilidade
    d_vals = yhat.apply(lambda yy: _desejabilidade_scaler(yy, L, T, s, direction=direction))

    # Filtragem por intervalo
    d_low, d_high = d_interval
    mask = (d_vals >= d_low) & (d_vals <= d_high)

    out = base_grid_df.copy()
    out[f"{target}_previsto"] = yhat.values
    out[desej_col_name] = d_vals.values
    out = out.loc[mask].sort_values(desej_col_name, ascending=False).reset_index(drop=True)

    msg = (
        f"A variável '{target}' possui R² = {r2:.2%} (≥ {r2_threshold:.0%}). "
        f"Desejabilidade executada com intervalo [{d_low:.2f}, {d_high:.2f}] "
        f"usando {n_points} pontos por variável-base."
    )

    if top_k is not None and len(out) > top_k:
        out = out.head(top_k)

    # Converte o DataFrame de resultados para um formato serializável (JSON)
    resultado_serializavel = to_serializable(out)

    return {
        "aplica_desejabilidade": True,
        "r2": r2,
        "mensagem": msg,
        "model_function_code": model_code,
        "desirability_function_code": desir_code,
        "search_spaces": search_spaces,
        "resultado_df": resultado_serializavel,
    }


# ==============================================================================
# 4. FUNÇÃO DE ORQUESTRAÇÃO PRINCIPAL DO PIPELINE
# ==============================================================================

def run_analysis_pipeline(df, independent_cols, dependent_cols, termos_interacao, termos_quadraticos):
    """
    Executa o pipeline completo de análise para todas as variáveis dependentes.
    Retorna um dicionário estruturado contendo todos os resultados para o LLM.
    """
    resultados_llm = {}
    
    # 1. Preparar a lista completa de termos para o modelo polinomial completo
    full_features = independent_cols.copy()
    
    # Adicionar termos de interação (ex: 'A:B')
    if termos_interacao:
        full_features.extend([f"{col1}:{col2}" for i, col1 in enumerate(independent_cols) for col2 in independent_cols[i+1:]])
    
    # Adicionar termos quadráticos (ex: 'I(A**2)')
    if termos_quadraticos:
        full_features.extend([f"I({col}**2)" for col in independent_cols])

    # 2. Executar o pipeline para cada variável dependente
    for target in dependent_cols:
        
        # Etapa A: Modelo Polinomial Completo
        modelo_completo, anova_completa = ajustar_modelo(df, target, full_features)
        
        if modelo_completo is None:
            resultados_llm[target] = {
                "mensagem": "Modelo completo não pôde ser ajustado."
            }
            continue

        # Etapa B: Seleção de Features Significativas (Pareto)
        significantes, insignificantes, anova_pareto = selecionar_features_significativas(modelo_completo, p_thresh=0.10)
        
        # 3. Estrutura de Saída
        resultado_target = {
            "target": target,
            # Informações de Pareto para o LLM
            "pareto": {
                "significativo": significantes,
                "insignificante": insignificantes,
                "anova_completa": anova_completa.fillna(np.nan).to_dict("index")
            }
        }
        
        # 4. Ajuste do Modelo Reduzido (se houver features significativas)
        if significantes:
            # Remove o Intercept da lista de features para o ajuste
            features_reduzidas = [f for f in significantes if f != 'Intercept']
            
            # Se a única coisa significativa for o Intercept, não ajustamos
            if not features_reduzidas:
                resultados_llm[target] = resultado_target
                continue
            
            # Ajustar modelo reduzido
            modelo_reduzido, anova_reduzida = ajustar_modelo(df, target, features_reduzidas)
            
            # Avaliar o Modelo (Métricas R2, LoF, F_reg)
            metricas, anova_completa_final, params_summary = avaliar_modelo_anova(modelo_reduzido, df, target, alpha=0.10)
            
            # Executar Desejabilidade
            desejabilidade_result = run_global_desejabilidade_if_applicable(
                modelo_reduzido,
                df,
                target,
                d_interval=(0.65, 0.85), # Parâmetros fixos
                n_points=15,
            )

            # Consolidar Resultados
            resultado_target.update({
                "modelo_formula": modelo_reduzido.model.formula,
                "modelo_params": params_summary,
                "metricas": metricas,
                "anova_completa": anova_completa_final, # ANOVA completa do modelo reduzido
                "desejabilidade": desejabilidade_result
            })

        # Adicionar o resultado ao dicionário final
        resultados_llm[target] = resultado_target
        
    return resultados_llm