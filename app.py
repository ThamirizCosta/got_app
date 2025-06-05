# app.py - Game of Thrones Deaths Analyzer
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Importa as classes
from DataLoader import DataLoader
from DataAnalise import DataAnalise

# 🎨 CONFIGURAÇÃO VISUAL AVANÇADA
st.set_page_config(
    page_title="GoT Deaths Analyzer",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 CSS CUSTOMIZADO - TEMA CLEAN E MODERNO
st.markdown("""
<style>
    /* Fundo limpo e moderno */
    .stApp {
        background: #FFFFFF;
    }
    
    /* Header personalizado - mais clean */
    .main-header {
        background: linear-gradient(135deg, #2C3E50, #3498DB);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(52, 152, 219, 0.15);
        border: none;
    }
    
    .main-header h1 {
        color: #FFFFFF;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: 1px;
    }
    
    .main-header p {
        color: #ECF0F1;
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        font-weight: 300;
    }
    
    /* Cards de métricas - design clean */
    .metric-card {
        background: #FFFFFF;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #E8E8E8;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        text-align: center;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    .metric-card h3 {
        color: #2C3E50;
        margin: 0 0 0.5rem 0;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    .metric-card p {
        color: #7F8C8D;
        margin: 0;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Seções personalizadas - mais sutis */
    .section-header {
        background: #F8F9FA;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #3498DB;
        margin: 1.5rem 0 1rem 0;
        border: 1px solid #E9ECEF;
    }
    
    .section-header h2 {
        color: #2C3E50;
        margin: 0;
        font-size: 1.4rem;
        font-weight: 600;
    }
    
    /* Tabela mais clean */
    .dataframe {
        background: #FFFFFF;
        border-radius: 8px;
        border: 1px solid #DEE2E6;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Sidebar clean */
    .css-1d391kg {
        background: #F8F9FA;
        border-right: 1px solid #DEE2E6;
    }
    
    /* Botões modernos */
    .stButton > button {
        background: #3498DB;
        color: #FFFFFF;
        border: none;
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(52, 152, 219, 0.2);
    }
    
    .stButton > button:hover {
        background: #2980B9;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
    }
    
    /* Avisos e alertas clean */
    .stAlert {
        border-radius: 8px;
        border: 1px solid #DEE2E6;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Inputs modernos */
    .stSelectbox > div > div, .stMultiSelect > div > div {
        background: #FFFFFF;
        border: 1px solid #CED4DA;
        border-radius: 6px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus, .stMultiSelect > div > div:focus {
        border-color: #3498DB;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
    }
    
    /* Texto principal */
    .main .block-container {
        color: #2C3E50;
    }
    
    /* Sidebar styling */
    .css-1d391kg .css-1v0mbdj {
        color: #2C3E50;
    }
</style>
""", unsafe_allow_html=True)

# 🎨 HEADER PRINCIPAL
st.markdown("""
<div class="main-header">
    <h1>⚔️ Game of Thrones Analytics</h1>
    <p>Análise de Dados dos Personagens</p>
</div>
""", unsafe_allow_html=True)

# 🔍 SIDEBAR DE CONFIGURAÇÕES
with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    
    # Configurações de exibição
    show_raw_data = st.checkbox("📋 Mostrar dados brutos", value=True)
    show_statistics = st.checkbox("📊 Mostrar estatísticas", value=True)
    show_charts = st.checkbox("📈 Mostrar gráficos", value=True)
    
    st.markdown("---")
    st.markdown("### 📊 Sobre os Dados")
    st.markdown("📚 **Fonte**: George R.R. Martin")
    st.markdown("🏰 **Universo**: A Song of Ice and Fire")
    st.markdown("⚔️ **Foco**: Análise de Mortalidade")

# 🔍 CARREGAMENTO DE DADOS
caminho_arquivo = "character-deaths.csv"

if not os.path.exists(caminho_arquivo):
    st.markdown('<div class="section-header"><h2>📁 Upload de Arquivo</h2></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.error("📁 Arquivo 'character-deaths.csv' não encontrado!")
        uploaded_file = st.file_uploader(
            "Faça upload do arquivo CSV",
            type=["csv"],
            help="Arquivo com dados dos personagens de Game of Thrones"
        )
        
        if uploaded_file is not None:
            with open(caminho_arquivo, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("✅ Arquivo carregado com sucesso!")
            st.rerun()
        else:
            st.stop()

# 🔍 PROCESSAMENTO DOS DADOS
@st.cache_data
def carregar_e_processar_dados(caminho):
    with st.spinner("🔄 Carregando dados dos Sete Reinos..."):
        loader = DataLoader(caminho, sep=";")
        df_raw = loader.load()
        
        if df_raw is None or df_raw.empty:
            return None, None
        
        analyzer = DataAnalise(df_raw.copy())
        try:
            df_processado, contagem_genero = analyzer.processar()
            return df_processado, contagem_genero
        except Exception as e:
            st.error(f"❌ Erro durante o processamento: {e}")
            return None, None

df_processado, contagem_genero = carregar_e_processar_dados(caminho_arquivo)

if df_processado is None:
    st.error("💀 Falha ao carregar os dados dos personagens.")
    st.stop()

# 🔍 ESTATÍSTICAS PRINCIPAIS
if show_statistics:
    st.markdown('<div class="section-header"><h2>📊 Resumo Executivo</h2></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{len(df_processado)}</h3>
            <p>Total de Personagens</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        mortes_total = df_processado['Morreu'].sum() if 'Morreu' in df_processado.columns else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>{mortes_total}</h3>
            <p>Mortes Registradas</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if contagem_genero:
            genero_principal = max(contagem_genero, key=contagem_genero.get)
            st.markdown(f"""
            <div class="metric-card">
                <h3>{genero_principal}</h3>
                <p>Gênero Predominante</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        if 'Death_Year' in df_processado.columns:
            ano_mortes = df_processado['Death_Year'].dropna()
            if not ano_mortes.empty:
                ano_mais_mortal = ano_mortes.mode().iloc[0] if not ano_mortes.mode().empty else "N/A"
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{ano_mais_mortal}</h3>
                    <p>Ano Mais Mortal</p>
                </div>
                """, unsafe_allow_html=True)

# 🔍 GRÁFICOS INTERATIVOS
if show_charts and not df_processado.empty:
    st.markdown('<div class="section-header"><h2>📈 Análises Visuais</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if contagem_genero:
            # Gráfico de pizza para gêneros
            fig_genero = px.pie(
                values=list(contagem_genero.values()),
                names=list(contagem_genero.keys()),
                title="Distribuição por Gênero",
                color_discrete_sequence=['#3498DB', '#E74C3C', '#2ECC71', '#F39C12']
            )
            fig_genero.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#2C3E50',
                title_font_color='#2C3E50',
                title_font_size=16,
                title_font_weight='bold'
            )
            st.plotly_chart(fig_genero, use_container_width=True)
    
    with col2:
        if 'Death_Year' in df_processado.columns:
            # Histograma de mortes por ano
            mortes_por_ano = df_processado[df_processado['Morreu'] == 1]['Death_Year'].dropna()
            if not mortes_por_ano.empty:
                fig_mortes = px.histogram(
                    x=mortes_por_ano,
                    title="Mortes por Ano",
                    nbins=20,
                    color_discrete_sequence=['#E74C3C']
                )
                fig_mortes.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#2C3E50',
                    title_font_color='#2C3E50',
                    title_font_size=16,
                    title_font_weight='bold',
                    xaxis_title="Ano",
                    yaxis_title="Número de Mortes"
                )
                st.plotly_chart(fig_mortes, use_container_width=True)

# 🔍 TABELA DE DADOS
if show_raw_data:
    st.markdown('<div class="section-header"><h2>📋 Dados dos Personagens</h2></div>', unsafe_allow_html=True)
    
    # Filtros interativos
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'Gender_Str' in df_processado.columns:
            generos_unicos = df_processado['Gender_Str'].dropna().unique()
            filtro_genero = st.multiselect(
                "Filtrar por Gênero:",
                options=generos_unicos,
                default=generos_unicos
            )
    
    with col2:
        if 'Morreu' in df_processado.columns:
            filtro_morreu = st.selectbox(
                "💀 Status:",
                options=["Todos", "Vivos", "Mortos"],
                index=0
            )
    
    with col3:
        if 'Nobility' in df_processado.columns:
            filtro_nobreza = st.selectbox(
                "👑 Nobreza:",
                options=["Todos", "Nobre", "Plebeu"],
                index=0
            )
    
    # Aplicar filtros
    df_filtrado = df_processado.copy()
    
    if 'Gender_Str' in df_processado.columns and filtro_genero:
        df_filtrado = df_filtrado[df_filtrado['Gender_Str'].isin(filtro_genero)]
    
    if 'Morreu' in df_processado.columns and filtro_morreu != "Todos":
        if filtro_morreu == "Vivos":
            df_filtrado = df_filtrado[df_filtrado['Morreu'] == 0]
        else:
            df_filtrado = df_filtrado[df_filtrado['Morreu'] == 1]
    
    if 'Nobility' in df_processado.columns and filtro_nobreza != "Todos":
        valor_nobreza = 1 if filtro_nobreza == "Nobre" else 0
        df_filtrado = df_filtrado[df_filtrado['Nobility'] == valor_nobreza]
    
    # Seleção de colunas
    colunas_disponiveis = df_filtrado.columns.tolist()
    colunas_padrao = ["Name", "Allegiances", "Gender_Str", "Nobility", "Death_Year", "Morreu", "Book of Death"]
    colunas_padrao = [col for col in colunas_padrao if col in colunas_disponiveis]
    
    colunas_selecionadas = st.multiselect(
        "Selecione as colunas para exibir:",
        options=colunas_disponiveis,
        default=colunas_padrao
    )
    
    if colunas_selecionadas:
        st.dataframe(
            df_filtrado[colunas_selecionadas],
            use_container_width=True,
            height=400
        )
        st.caption(f"Exibindo {len(df_filtrado)} de {len(df_processado)} personagens")
    else:
        st.warning("Selecione pelo menos uma coluna para exibir os dados.")

# 🔍 ESTATÍSTICAS DETALHADAS
if show_statistics:
    try:
        from ContadorMorte import ContadorMortes
        
        st.markdown('<div class="section-header"><h2>📈 Estatísticas Detalhadas</h2></div>', unsafe_allow_html=True)
        
        contador = ContadorMortes(df_processado)
        stats_mortes = contador.estatisticas_mortes()
        
        if "Erro" not in stats_mortes:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Estatísticas de Mortes")
                for key, value in stats_mortes.items():
                    if key != "Total de Mortes":
                        st.metric(key, value)
            
            with col2:
                if contagem_genero:
                    st.markdown("### Distribuição por Gênero")
                    for genero, count in contagem_genero.items():
                        percentage = (count / len(df_processado)) * 100
                        st.metric(f"{genero}", f"{count} ({percentage:.1f}%)")
        else:
            st.warning(f"Erro ao calcular estatísticas: {stats_mortes['Erro']}")
    
    except ImportError:
        st.info("Classe ContadorMortes não disponível para estatísticas detalhadas.")

# FOOTER
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1.5rem; color: #7F8C8D;">
    <p style="font-size: 0.9rem; margin: 0;">
        Baseado nas obras de George R.R. Martin - A Song of Ice and Fire
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="color: #FFD700; font-size: 1.1rem; font-weight: bold;">
    🏰 "Valar Morghulis - Todos os Homens Devem Morrer" 🏰
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style="color: #5F5F5C; font-size: 0.9rem;">
    📚 Baseado nas Crônicas de Gelo e Fogo de George R.R. Martin<br>
    ⚔️ Dados analisados com a precisão de um Maester da Cidadela
</p>
""", unsafe_allow_html=True)