import streamlit as st
import pandas as pd
import plotly.express as px
import os

from utils.generate_data import generate_data
from utils.health_score import calculate_health_score
from utils.nrr import calculate_nrr
from utils.market_api import get_market_trends

# =========================
# CONFIG
# =========================
st.set_page_config(layout="wide")

# =========================
# ESTILO
# =========================
st.markdown("""
<style>
body {
    background-color: #0B0F2A;
    color: white;
}
.stApp {
    background-color: #0B0F2A;
}
h1, h2, h3, h4 {
    color: white;
}
.stMetric {
    background-color: #111827;
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("🚀 Máquina de Crescimento Previsível")
st.caption("CS + CX + Dados = Receita")

# =========================
# DATA
# =========================
@st.cache_data
def load_data():
    if os.path.exists("data/simulated_data.csv"):
        return pd.read_csv("data/simulated_data.csv")
    else:
        return generate_data()

df = load_data()

# =========================
# MODELOS
# =========================
df = calculate_health_score(df)
nrr = calculate_nrr(df)

# =========================
# ORDEM + CORES HEALTH
# =========================
df["health_label"] = pd.Categorical(
    df["health_label"],
    categories=["Healthy", "At Risk", "Critical"],
    ordered=True
)

health_colors = {
    "Healthy": "#22C55E",   # Verde
    "At Risk": "#EAB308",   # Amarelo
    "Critical": "#EF4444"   # Vermelho
}

# =========================
# FORMATADOR
# =========================
def humanize(x):
    if x >= 1_000_000:
        return f"{x/1_000_000:.1f} mi"
    elif x >= 1_000:
        return f"{x/1_000:.1f} mil"
    return str(x)

# =========================
# KPI HEALTH
# =========================
total_clients = len(df)
critical_pct = (df["health_label"] == "Critical").mean() * 100
risk_pct = (df["health_label"] == "At Risk").mean() * 100

# =========================
# ALERTA EXECUTIVO
# =========================
if critical_pct > 15:
    st.error(f"🚨 ALERTA: {critical_pct:.1f}% da base em risco crítico")
elif risk_pct > 30:
    st.warning(f"⚠️ Atenção: {risk_pct:.1f}% da base em risco moderado")
else:
    st.success("✅ Base saudável e sob controle")

# =========================
# MENU
# =========================
st.sidebar.title("Navegação Estratégica")
section = st.sidebar.radio("Escolha:", [
    "Visão Executiva",
    "Excelência Operacional",
    "Crescimento e Expansão",
    "Inteligência de Mercado"
])

# =========================
# 1. VISÃO EXECUTIVA
# =========================
if section == "Visão Executiva":

    st.header("💰 Torre de Controle de Receita")

    total = df["revenue"].sum()
    churn = df["churn_risk"].mean() * 100
    expansion = df["expansion_opportunity"].mean() * 100

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Receita Total", humanize(total))
    c2.metric("Risco de Churn", f"{churn:.1f}%")
    c3.metric("Expansão", f"{expansion:.1f}%")
    c4.metric("NRR", f"{nrr}%")
    c5.metric("Clientes Críticos", f"{critical_pct:.1f}%")

    # RECEITA
    st.markdown("### 📊 Receita por Segmento")
    fig = px.bar(df, x="segment", y="revenue", color="segment")
    fig.update_layout(plot_bgcolor="#0B0F2A", paper_bgcolor="#0B0F2A", font_color="white")
    st.plotly_chart(fig, use_container_width=True)

    # HEALTH SCORE
    st.markdown("### ❤️ Health Score")
    fig2 = px.histogram(
        df,
        x="health_label",
        color="health_label",
        color_discrete_map=health_colors
    )
    fig2.update_layout(plot_bgcolor="#0B0F2A", paper_bgcolor="#0B0F2A", font_color="white")
    st.plotly_chart(fig2, use_container_width=True)

    st.info("🔗 Integração com CRM, ERP e atendimento via API")

# =========================
# 2. CX
# =========================
elif section == "Excelência Operacional":

    st.header("⚙️ Excelência Operacional CX")

    fig = px.scatter(
        df,
        x="tickets",
        y="nps",
        color="health_label",
        size="revenue",
        hover_data=["client"],
        color_discrete_map=health_colors
    )

    fig.update_layout(plot_bgcolor="#0B0F2A", paper_bgcolor="#0B0F2A", font_color="white")
    st.plotly_chart(fig, use_container_width=True)

    sla = df["sla_breach"].mean() * 100
    st.metric("SLA Breach", f"{sla:.1f}%")

    st.markdown("### 🚨 Clientes Críticos")
    st.dataframe(df[df["health_label"] == "Critical"].head(10))

# =========================
# 3. CS
# =========================
elif section == "Crescimento e Expansão":

    st.header("📈 Crescimento e Expansão")

    exp_df = df[df["expansion_opportunity"] == 1]

    fig = px.histogram(exp_df, x="segment", color="segment")
    fig.update_layout(plot_bgcolor="#0B0F2A", paper_bgcolor="#0B0F2A", font_color="white")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 💎 Top Expansão")
    st.dataframe(exp_df.sort_values("revenue", ascending=False).head(10))

    st.markdown("### ⚠️ Risco de Churn")
    st.dataframe(df[df["churn_risk"] == 1].head(10))

# =========================
# 4. MERCADO
# =========================
elif section == "Inteligência de Mercado":

    st.header("🕵️ Inteligência de Mercado")

    trends = get_market_trends()

    if not trends.empty:
        for col in trends.columns[1:]:
            trends[col] = pd.to_numeric(trends[col], errors="coerce")

        trends = trends.melt(id_vars="date", var_name="Categoria", value_name="Volume")

        fig = px.line(trends, x="date", y="Volume", color="Categoria")
        fig.update_layout(plot_bgcolor="#0B0F2A", paper_bgcolor="#0B0F2A", font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### ⚠️ Dores do Mercado")
    pain = pd.DataFrame({
        "problema": ["Atendimento lento", "Suporte ruim", "Atrasos"],
        "volume": [120, 95, 80]
    })

    fig2 = px.bar(pain, x="problema", y="volume")
    fig2.update_layout(plot_bgcolor="#0B0F2A", paper_bgcolor="#0B0F2A", font_color="white")
    st.plotly_chart(fig2, use_container_width=True)

    st.info("💡 Dados integráveis via APIs externas (Trends, Reclame Aqui, etc.)")