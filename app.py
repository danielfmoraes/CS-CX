import streamlit as st
import pandas as pd
import plotly.express as px
import os

from utils.generate_data import generate_data
from utils.health_score import calculate_health_score
from utils.nrr import calculate_nrr
from utils.market_api import get_market_trends

st.set_page_config(layout="wide")

st.title("📊 Plataforma de Inteligência de Mercado e Receita")
st.caption("Da operação reativa à máquina previsível de crescimento")

# =========================
# CACHE + LOAD DATA
# =========================
@st.cache_data
def load_data():
    if os.path.exists("data/simulated_data.csv"):
        return pd.read_csv("data/simulated_data.csv")
    else:
        return generate_data()

df = load_data()

# APPLY MODELS
df = calculate_health_score(df)
nrr = calculate_nrr(df)

# =========================
# FORMATADOR DE NÚMEROS
# =========================
def humanize_number(x):
    if x >= 1_000_000:
        return f"{x/1_000_000:.1f} mi"
    elif x >= 1_000:
        return f"{x/1_000:.1f} mil"
    else:
        return str(x)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("Navegação")
section = st.sidebar.radio("Ir para:", [
    "Torre de Controle de Receita",
    "Excelência Operacional CX",
    "Crescimento CS",
    "Inteligência de Mercado"
])

# =========================
# 1. RECEITA
# =========================
if section == "Torre de Controle de Receita":
    st.header("💰 Torre de Controle de Receita")

    total_revenue = df["revenue"].sum()
    churn_risk = df["churn_risk"].mean() * 100
    expansion_rate = df["expansion_opportunity"].mean() * 100

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Receita Total", humanize_number(total_revenue))
    col2.metric("Risco de Churn", f"{churn_risk:.1f}%")
    col3.metric("Potencial de Expansão", f"{expansion_rate:.1f}%")
    col4.metric("NRR", f"{nrr}%")

    st.markdown("### 📊 Receita por Segmento")
    fig = px.bar(df, x="segment", y="revenue", color="segment",
                 labels={"segment": "Segmento", "revenue": "Receita"})
    st.plotly_chart(fig, use_container_width=True)
    st.info("🔗 Integração futura via API: CRM, ERP, plataformas de suporte")

    st.markdown("### ❤️ Health Score dos Clientes")
    fig_health = px.histogram(df, x="health_label", color="health_label",
                              labels={"health_label": "Status"})
    st.plotly_chart(fig_health, use_container_width=True)
    st.info("🔗 Health Score pode ser alimentado em tempo real via APIs")

# =========================
# 2. CX
# =========================
elif section == "Excelência Operacional CX":
    st.header("⚙️ Excelência Operacional CX")

    st.markdown("### 🎯 Relação entre Tickets e NPS")

    fig = px.scatter(
        df,
        x="tickets",
        y="nps",
        color="health_label",
        size="revenue",
        hover_data=["client"],
        labels={"tickets": "Tickets", "nps": "NPS"}
    )
    st.plotly_chart(fig, use_container_width=True)
    st.info("🔗 Dados operacionais integráveis via API de atendimento (Zendesk, etc.)")

    sla = df["sla_breach"].mean() * 100
    st.metric("SLA Breach", f"{sla:.1f}%")

    st.markdown("### 🚨 Clientes Críticos")
    risk_df = df[df["health_label"] == "Critical"]
    st.dataframe(risk_df[["client", "segment", "tickets", "nps", "revenue"]].head(10))

# =========================
# 3. CS
# =========================
elif section == "Crescimento CS":
    st.header("📈 Crescimento e Expansão")

    expansion_df = df[df["expansion_opportunity"] == 1]

    st.markdown("### 🎯 Oportunidades de Expansão")
    fig = px.histogram(expansion_df, x="segment", color="segment")
    st.plotly_chart(fig, use_container_width=True)
    st.info("🔗 Dados podem ser conectados ao CRM para ação automatizada")

    st.markdown("### 💎 Top Contas para Expansão")
    st.dataframe(
        expansion_df.sort_values("revenue", ascending=False)[
            ["client", "segment", "revenue", "health_label"]
        ].head(10)
    )

    st.markdown("### ⚠️ Contas em Risco")
    churn_df = df[df["churn_risk"] == 1]
    st.dataframe(
        churn_df.sort_values("revenue", ascending=False)[
            ["client", "segment", "revenue", "health_label"]
        ].head(10)
    )

# =========================
# 4. MERCADO
# =========================
elif section == "Inteligência de Mercado":
    st.header("🕵️ Inteligência de Mercado")

    trends = get_market_trends()

    if not trends.empty:
        # Corrige problema de tipos
        for col in trends.columns[1:]:
            trends[col] = pd.to_numeric(trends[col], errors="coerce")

        trends_melt = trends.melt(id_vars="date", var_name="Categoria", value_name="Volume")

        fig = px.line(
            trends_melt,
            x="date",
            y="Volume",
            color="Categoria",
            labels={"date": "Data"}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Sem dados de mercado disponíveis")

    st.markdown("### ⚠️ Principais Dores do Mercado")
    pain_points = pd.DataFrame({
        "issue": ["Atendimento lento", "Suporte ruim", "Atrasos"],
        "volume": [120, 95, 80]
    })

    fig2 = px.bar(pain_points, x="issue", y="volume",
                  labels={"issue": "Problema", "volume": "Volume"})
    st.plotly_chart(fig2, use_container_width=True)

    st.info(
        "💡 Insight: aumento de reclamações + crescimento de busca indica oportunidade de posicionamento estratégico.\n"
        "🔗 Integração futura com APIs de mercado permite atualização em tempo real."
    )