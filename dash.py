import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu #para trabalhar com menu
from query import conexao # Consulta no banco de dados

# ******* Primeira Consulta e Atualizacao *******
# Consulta SQL
query = "SELECT  * FROM tb_carro"

# Carregar os dados para a variavel df
df = conexao(query)

# Atualizacao - botao
if st.button("Atualizar Dados"):
    df = conexao(query)
# ***********************************
# Estrutura de Filtro Lateral
# sidebar - barra lateral
marca = st.sidebar.multiselect("Marca Selecionada",
                       options=df["marca"].unique(),
                       default=df["marca"].unique())

modelo = st.sidebar.multiselect("modelo Selecionada",
                       options=df["modelo"].unique(),
                       default=df["modelo"].unique())

ano = st.sidebar.multiselect("ano Selecionada",
                       options=df["ano"].unique(),
                       default=df["ano"].unique())

valor = st.sidebar.multiselect("valor Selecionada",
                       options=df["valor"].unique(),
                       default=df["valor"].unique())

cor = st.sidebar.multiselect("cor Selecionada",
                       options=df["cor"].unique(),
                       default=df["cor"].unique())

numero_Vendas = st.sidebar.multiselect("numero_Vendas Selecionada",
                       options=df["numero_Vendas"].unique(),
                       default=df["numero_Vendas"].unique())

min_vendas = int(df["numero_Vendas"].min())
max_vendas = int(df["numero_Vendas"].max())

vendas = st.sidebar.slider(
    "Intervalo de Numero de Vendas Selecionado",
    min_value=min_vendas,
    max_value=max_vendas,
    value=(min_vendas, max_vendas) # Valor inicial
    )

# ******* Verificacao da aplicacao dos Filtros
df_selecionado = df[
    (df["marca"].isin(marca)) &
    (df["modelo"].isin(modelo)) &
    (df["ano"].isin(ano)) &
    (df["valor"].isin(valor)) &
    (df["cor"].isin(cor)) &
    (df["numero_Vendas"] >= vendas[0]) & # 0 (min) maior ou = ao menor
    (df["numero_Vendas"] <= vendas[1]) # 1 (max) menor ou = ao menor max
]

# ******* DASHBOARD *********
# CARDS DE VALORES
def PaginaInicial():
    # Expande para selecionar as opcoes
    with st.expander("Tabela de Carros"):
        exibicao = st.multiselect("Filtro",
                                  df_selecionado.columns,
                                  default=[],
                                  key="Filtro_Exibicao"
                                  )
        
        if exibicao:
            st.write(df_selecionado[exibicao])

    if not df_selecionado.empty:
        total_Vendas = df_selecionado["numero_Vendas"].sum()
        media_valor = df_selecionado["valor"].mean()
        media_vendas = df_selecionado["numero_Vendas"].mean()


        card1, card2, card3 = st.columns(3, gap="large")
        with card1:
            st.info("Valor Total de Vendas", icon="🤣")
            st.metric(label="Total", value=f"{total_Vendas:,.0f}")
        with card2:
            st.info("Valor Medio dos Carros", icon="🤣")
            st.metric(label="Media", value=f"{media_valor:,.0f}")
        with card3:
            st.info("Valor Medio de Vendas", icon="🤣")
            st.metric(label="Media", value=f"{media_vendas:,.0f}")

    else:
        st.warning("Nenhum dados disponivel com os filtros selecionados")
    st.markdown("""-----""")

# ************ GRAFICOS **************
def graficos(df_selecionado):
    if df_selecionado.empty:
        st.warning("Nenhum dado disponivel para gerar os graficos")
        return
    
    graf1, graf2 = st.tabs(["Grafico de Barras",
                            "Grafico de Linhas"
                            ])

    with graf1:
        st.write("Grafico de Barras")
        valor = df_selecionado.groupby("marca").count()[["valor"]].sort_values(by="valor", ascending=False)

        fig1= px.bar(
            valor,
            x=valor.index,
            y="valor",
            orientation="h",
            title="Valores dos Carros",
            color_discrete_sequence=["#0083b8"]
        )

    st.plotly_chart(fig1, use_container_width=True)

    with graf2:
        st.write("Grafico de Linhas")
        valor_linhas = df_selecionado.groupby("modelo").count()[["valor"]]

        fig2 = px.line(
            valor_linhas,
            x=valor_linhas.index,
            y="valor",
            title="Valor por Modelo",
            color_discrete_sequence=["#e41c68"]
        )

    st.altair_chart(fig2, use_container_width=True)



PaginaInicial()
graficos(df_selecionado)


