import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="CottonQual | Qualidade HVI", layout="wide")

st.markdown(
    """
    <style>
    :root {
        --cq-ink: #203630;
        --cq-muted: #65766f;
        --cq-green: #176f63;
        --cq-coral: #c96f55;
        --cq-line: #dce5df;
        --cq-paper: #f4f7f4;
    }
    html, body, [class*="css"] {
        font-family: "Aptos", "Segoe UI", sans-serif;
        color: var(--cq-ink);
    }
    [data-testid="stAppViewContainer"] { background: var(--cq-paper); }
    [data-testid="stMainBlockContainer"] {
        max-width: 1460px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] { background: #183b35; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] label { color: #edf4ef; }
    [data-testid="stSidebar"] [data-testid="stSelectbox"] > label {
        color: #b8cec4;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    .cq-brand {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin: 0.5rem 0 2.3rem;
    }
    .cq-mark {
        display: grid;
        width: 2.7rem;
        height: 2.7rem;
        place-items: center;
        border: 1px solid #79a99a;
        border-radius: 7px;
        color: #d9eee4;
        font-size: 0.9rem;
        font-weight: 800;
        letter-spacing: 0.04em;
    }
    .cq-brand-name { color: #f4f7f4; font-size: 0.9rem; font-weight: 800; }
    .cq-brand-note {
        display: block;
        margin-top: 0.15rem;
        color: #a9c1b6;
        font-size: 0.63rem;
        font-weight: 700;
        letter-spacing: 0.12em;
    }
    h1, h2, h3 { color: var(--cq-ink); letter-spacing: 0; }
    h1 { font-size: 2.15rem !important; font-weight: 750 !important; }
    h2 { margin-top: 1.5rem !important; font-size: 1.35rem !important; }
    h3 { font-size: 1.05rem !important; }
    [data-testid="stMarkdownContainer"] p { color: var(--cq-muted); }
    [data-testid="stMetric"] {
        padding: 1rem 1.1rem;
        border: 1px solid var(--cq-line);
        border-top: 3px solid var(--cq-green);
        border-radius: 6px;
        background: #fff;
    }
    [data-testid="stMetricLabel"] { color: var(--cq-muted); font-size: 0.82rem; }
    [data-testid="stMetricValue"] {
        color: var(--cq-ink);
        font-size: 1.35rem !important;
        line-height: 1.2;
    }
    [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        border-color: var(--cq-line);
        border-radius: 5px;
    }
    [data-testid="stNumberInput"] input:focus {
        border-color: var(--cq-green);
        box-shadow: 0 0 0 1px var(--cq-green);
    }
    [data-testid="stButton"] button,
    [data-testid="stDownloadButton"] button {
        border-radius: 5px;
        font-weight: 650;
    }
    [data-testid="stDownloadButton"] button {
        border-color: var(--cq-green);
        color: var(--cq-green);
    }
    [data-testid="stAlert"] { border-radius: 5px; }
    hr { border-color: var(--cq-line); }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    '<div class="cq-brand"><span class="cq-mark">CQ</span>'
    '<div><span class="cq-brand-name">COTTONQUAL</span>'
    '<span class="cq-brand-note">HVI QUALITY LAB</span></div></div>',
    unsafe_allow_html=True,
)

st.title(":material/eco: CottonQual")
st.caption("DIAGNÓSTICO TÊXTIL · QUALIDADE HVI")

# Sidebar - Seleção de Funcionalidade
menu = st.sidebar.selectbox(
    "Módulo de análise",
    [
        "Análise de Lote Manual", 
        "Importar Laudo HVI (CSV/Excel)", 
        "Otimizador de Blending (Mistura)", 
        "Simulador de Preço Comercial"
    ]
)

# ==========================================
# MÓDULO 1: ANÁLISE DE LOTE MANUAL
# ==========================================
if menu == "Análise de Lote Manual":
    st.header(":material/search: Classificação e diagnóstico")
    
    col1, col2 = st.columns(2)
    
    with col1:
        mic = st.number_input("Micronaire (MIC) [3.5 - 4.9 ideal]:", min_value=2.0, max_value=6.0, value=4.2, step=0.1)
        len_mm = st.number_input("Comprimento UHML (mm) [> 28mm ideal]:", min_value=20.0, max_value=35.0, value=29.5, step=0.1)
        str_gtex = st.number_input("Resistência STR (g/tex) [> 30 ideal]:", min_value=15.0, max_value=45.0, value=31.0, step=0.5)

    with col2:
        ui_pct = st.number_input("Uniformidade UI (%) [> 82% ideal]:", min_value=70.0, max_value=90.0, value=83.5, step=0.5)
        trash_cnt = st.number_input("Contagem de Impurezas (Trash Count):", min_value=0, max_value=100, value=15)
        rd_color = st.number_input("Reflectância Rd (%):", min_value=50.0, max_value=90.0, value=75.0, step=0.5)

    st.subheader(":material/analytics: Diagnóstico têxtil")
    
    alertas = []
    
    if mic < 3.5:
        alertas.append("**Micronaire baixo:** Risco de fibras imaturas, formação de *neps* e manchas no tingimento.")
    elif mic > 4.9:
        alertas.append("**Micronaire alto:** Fibras grosseiras podem reduzir a resistência do fio.")
    else:
        alertas.append("**Micronaire:** Faixa adequada de maturidade e finura.")

    if len_mm < 28.0:
        alertas.append("**Comprimento curto:** Recomendado para fios mais grossos (Open-End).")
    else:
        alertas.append("**Comprimento:** Adequado para fios de alta qualidade (Anel / Comb).")

    if str_gtex < 29.0:
        alertas.append("**Resistência baixa:** Pode haver maior taxa de quebra de fios na fiação.")
    else:
        alertas.append("**Resistência:** Boa capacidade para suportar velocidades elevadas no urdume.")

    for alert in alertas:
        st.write(alert)

# ==========================================
# MÓDULO 2: IMPORTAR LAUDO HVI (CSV/EXCEL)
# ==========================================
elif menu == "Importar Laudo HVI (CSV/Excel)":
    st.header(":material/upload_file: Laudos HVI")
    st.markdown("Importação e análise de resultados de laboratório Uster ou Spinlab.")

    uploaded_file = st.file_uploader("Arraste seu arquivo CSV ou Excel (.xlsx) aqui", type=["csv", "xlsx", "xls"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.success(f"Arquivo `{uploaded_file.name}` carregado. {len(df)} fardos ou lotes encontrados.")
            
            with st.expander("Visualizar dados originais"):
                st.dataframe(df)

            st.markdown("---")
            st.subheader(":material/tune: Mapeamento de colunas")
            st.write("Ajuste os seletores abaixo caso os nomes do cabeçalho da sua planilha sejam diferentes:")

            c1, c2, c3, c4 = st.columns(4)
            cols = list(df.columns)

            # Tenta pre-selecionar caso as colunas padrão existam
            def get_default_idx(name):
                for idx, col in enumerate(cols):
                    if name.lower() in str(col).lower():
                        return idx
                return 0

            col_mic = c1.selectbox("Coluna Micronaire (MIC):", cols, index=get_default_idx("mic"))
            col_len = c2.selectbox("Coluna Comprimento (UHML):", cols, index=get_default_idx("comp"))
            col_str = c3.selectbox("Coluna Resistência (STR):", cols, index=get_default_idx("res"))
            col_ui = c4.selectbox("Coluna Uniformidade (UI):", cols, index=get_default_idx("uni"))

            st.markdown("---")
            st.subheader(":material/analytics: Médias do estoque")

            avg_mic = df[col_mic].mean()
            avg_len = df[col_len].mean()
            avg_str = df[col_str].mean()
            avg_ui = df[col_ui].mean()

            k1, k2, k3, k4 = st.columns(4)
            k1.metric("MIC médio", f"{avg_mic:.2f}")
            k2.metric("Comprimento", f"{avg_len:.2f} mm")
            k3.metric("Resistência", f"{avg_str:.2f} g/tex")
            k4.metric("Uniformidade", f"{avg_ui:.2f} %")

            # Classificação individual
            def classificar_fardo(val):
                if val < 3.5:
                    return "Baixo (Imaturo)"
                elif val > 4.9:
                    return "Alto (Grosseiro)"
                else:
                    return "Ideal"

            df['Status_MIC'] = df[col_mic].apply(classificar_fardo)

            # Gráficos
            st.markdown("---")
            st.subheader(":material/monitoring: Análise gráfica da qualidade")
            
            g1, g2 = st.columns(2)

            with g1:
                fig_scatter = px.scatter(
                    df, 
                    x=col_mic, 
                    y=col_len, 
                    color='Status_MIC',
                    title="Dispersão: Micronaire vs Comprimento",
                    labels={col_mic: "Micronaire", col_len: "Comprimento (mm)"},
                    color_discrete_map={"Ideal": "#176f63", "Baixo (Imaturo)": "#d2a344", "Alto (Grosseiro)": "#c96f55"},
                    template="plotly_white",
                )
                fig_scatter.update_traces(
                    marker={
                        "size": 9,
                        "opacity": 0.9,
                        "line": {"width": 1, "color": "#F4F7F4"},
                    },
                )
                fig_scatter.update_layout(
                    height=390,
                    margin={"l": 12, "r": 8, "t": 55, "b": 82},
                    font={"family": "Aptos, Segoe UI, sans-serif", "color": "#203630", "size": 12},
                    title={"font": {"size": 15, "color": "#203630"}, "x": 0, "xanchor": "left"},
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    legend={
                        "title": None,
                        "orientation": "h",
                        "x": 0.5,
                        "xanchor": "center",
                        "y": -0.25,
                        "yanchor": "top",
                        "font": {"size": 10},
                    },
                )
                fig_scatter.update_xaxes(showgrid=False, zeroline=False, linecolor="#DCE5DF")
                fig_scatter.update_yaxes(showgrid=True, gridcolor="#E2EAE5", zeroline=False, linecolor="#DCE5DF")
                st.plotly_chart(fig_scatter, width="stretch", config={"displayModeBar": False})

            with g2:
                fig_pie = px.pie(
                    df, 
                    names='Status_MIC', 
                    title="Categorias de micronaire",
                    color='Status_MIC',
                    color_discrete_map={"Ideal": "#176f63", "Baixo (Imaturo)": "#d2a344", "Alto (Grosseiro)": "#c96f55"},
                    hole=0.48,
                    template="plotly_white",
                )
                fig_pie.update_traces(
                    textposition="inside",
                    textinfo="percent",
                    textfont={"size": 12, "color": "#FFFFFF"},
                    marker={"line": {"color": "#F4F7F4", "width": 3}},
                    sort=False,
                )
                fig_pie.update_layout(
                    height=390,
                    margin={"l": 8, "r": 8, "t": 55, "b": 82},
                    font={"family": "Aptos, Segoe UI, sans-serif", "color": "#203630", "size": 12},
                    title={"font": {"size": 15, "color": "#203630"}, "x": 0, "xanchor": "left"},
                    paper_bgcolor="rgba(0,0,0,0)",
                    legend={
                        "title": None,
                        "orientation": "h",
                        "x": 0.5,
                        "xanchor": "center",
                        "y": -0.18,
                        "yanchor": "top",
                        "font": {"size": 10},
                    },
                    annotations=[
                        {
                            "text": f"{len(df)}<br>amostras",
                            "x": 0.5,
                            "y": 0.5,
                            "showarrow": False,
                            "font": {"size": 13, "color": "#203630"},
                        }
                    ],
                )
                st.plotly_chart(fig_pie, width="stretch", config={"displayModeBar": False})

            # Exportação do Resultado
            st.markdown("---")
            st.subheader(":material/download: Exportar relatório")
            
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Baixar CSV processado",
                icon=":material/download:",
                data=csv_data,
                file_name="laudo_hvi_processado.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}. Verifique se os dados contêm apenas valores numéricos nas colunas selecionadas.")
    else:
        st.info("A planilha deve conter colunas numéricas de micronaire, comprimento, resistência e uniformidade.")

# ==========================================
# MÓDULO 3: OTIMIZADOR DE BLENDING (MISTURA)
# ==========================================
elif menu == "Otimizador de Blending (Mistura)":
    st.header(":material/tune: Otimizador de mistura")
    st.markdown("Calcule os indicadores ponderados de três lotes para planejar a composição da mistura.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Lote A · Premium")
        prop_a = st.slider("Proporção Lote A (%)", 0, 100, 40)
        mic_a = st.number_input("MIC A", value=4.2, key="mic_a")
        len_a = st.number_input("Comprimento A (mm)", value=30.0, key="len_a")

    with col2:
        st.subheader("Lote B · Intermediário")
        prop_b = st.slider("Proporção Lote B (%)", 0, 100 - prop_a, 40)
        mic_b = st.number_input("MIC B", value=3.8, key="mic_b")
        len_b = st.number_input("Comprimento B (mm)", value=27.5, key="len_b")

    with col3:
        prop_c = 100 - (prop_a + prop_b)
        st.subheader("Lote C · Econômico")
        st.write(f"**Proporção Lote C:** {prop_c}%")
        mic_c = st.number_input("MIC C", value=4.8, key="mic_c")
        len_c = st.number_input("Comprimento C (mm)", value=26.0, key="len_c")

    # Cálculos Ponderados
    mic_final = (prop_a * mic_a + prop_b * mic_b + prop_c * mic_c) / 100
    len_final = (prop_a * len_a + prop_b * len_b + prop_c * len_c) / 100

    st.markdown("---")
    st.subheader(":material/monitoring: Indicadores da mistura")
    
    col_r1, col_r2 = st.columns(2)
    col_r1.metric("Micronaire Médio da Mistura", f"{mic_final:.2f}")
    col_r2.metric("Comprimento Médio da Mistura", f"{len_final:.2f} mm")

    if 3.8 <= mic_final <= 4.5 and len_final >= 28.0:
        st.success("Mistura dentro dos parâmetros definidos para fios de alta resistência.")
    else:
        st.warning("Revise as proporções: a mistura pode ficar fora dos parâmetros desejados para fiação.")

# ==========================================
# MÓDULO 4: SIMULADOR DE PREÇO COMERCIAL
# ==========================================
elif menu == "Simulador de Preço Comercial":
    st.header(":material/payments: Simulador de preço")
    
    preco_base = st.number_input("Preço Base do Algodão (R$/arroba):", value=150.0)
    mic_lote = st.number_input("Micronaire do Lote:", value=3.2)
    
    desconto = 0.0
    if mic_lote < 3.5:
        desconto = 0.08  # 8% de desconto
    elif mic_lote > 4.9:
        desconto = 0.05  # 5% de desconto
    
    preco_final = preco_base * (1 - desconto)
    
    st.metric(
        label="Preço Ajustado por Arroba", 
        value=f"R$ {preco_final:.2f}", 
        delta=f"-{desconto*100:.1f}% Desconto" if desconto > 0 else "Sem Desconto"
    )