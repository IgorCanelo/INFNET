import streamlit as st
import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt

# Caminhos para os arquivos
dados_originais = r"C:/Users/Igor/Desktop/IGOR/Scripts/INFNET/data/dados_originais.xls"
dados_formatados = r"C:/Users/Igor/Desktop/IGOR/Scripts/INFNET/data/dados_formatados.xlsx"


@st.cache_data
def load_data(file_path):
    return pd.read_excel(file_path)

df = load_data(dados_formatados)


def initialize_session_state():
    """Inicializa o Session State com valores padrão."""
    if 'categoria_selecionada' not in st.session_state:
        st.session_state.categoria_selecionada = []
    if 'mostrar_detalhes' not in st.session_state:
        st.session_state.mostrar_detalhes = False
    if 'seleciona_colunas' not in st.session_state:
        st.session_state.seleciona_colunas = []


def initial():
    st.title("Motivo da viagem dos visitantes internacionais com destino à Cidade do Rio de Janeiro entre 1994-2003")
    st.write("O objetivo do Dashboard desenvolvido é entender o padrão de comportamento dos visitantes internacionais à uma das cidades mais conhecidas e visitadas no Brasil.")
    st.markdown("### As funcionalidades implementadas serão:")
    st.markdown("""
    - Download dos dados originais
    - Filtros nos dados
    - Download dos dados filtrados
    - Funcionalidade 4
    """)


def download_csv():
    st.header("Download dos dados originais:")
    with open(dados_originais, "rb") as file:
        file_data = file.read()
    st.download_button(
        label="Baixar dados",
        data=file_data,
        file_name='dados_originais.xls',
        mime='application/vnd.ms-excel'
    )


def table(df):
    st.header("Dados:")
    st.dataframe(df, use_container_width=True)



def line_chart(df):
    st.header("Gráfico ao longo dos anos a quantidade de visitas de lazer no RJ")
    
    # Ajuste dos dados
    df_melted = df.melt(id_vars=['Motivos'], var_name='Ano', value_name='Valor')
    df_melted['Ano'] = pd.to_numeric(df_melted['Ano'], errors='coerce')
    df_melted.dropna(subset=['Valor'], inplace=True)
    a = df_melted[df_melted["Motivos"] == "Lazer"]
    df_novo = a[['Ano', 'Valor']]
    df_novo['Ano'] = df_novo['Ano'].astype(str)

    # Gráfico de linha
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='Ano', y='Valor', data=df_novo, marker='o')
    plt.title('Gráfico de Linha - Lazer', fontsize=16)
    plt.xlabel('Ano', fontsize=12)
    plt.ylabel('Valor (%)', fontsize=12)

    st.pyplot(plt)



def pie_chart(df):
    st.header("Gráfico de pizza dos top 3 motivos de viagem para o RJ no ano de 2003")
    
    # Ajuste dos dados
    df_melted2 = df.melt(id_vars=['Motivos'], var_name='Ano', value_name='Valor')
    df_melted2['Ano'] = pd.to_numeric(df_melted2['Ano'], errors='coerce')
    df_melted2.dropna(subset=['Valor'], inplace=True)
    df_melted2['Ano'] = df_melted2['Ano'].astype(str)
    df_final = df_melted2[df_melted2["Ano"] == "2003"]
    df_final['Valor'] = df_final['Valor'].str.replace(',', '.')
    df_final['Valor'] = pd.to_numeric(df_final['Valor'], errors='coerce')
    df_final2 = df_final[df_final["Valor"] >= 10]

    # Gráfico de pizza
    plt.figure(figsize=(10, 6))
    plt.pie(df_final2['Valor'], labels=df_final2['Motivos'], autopct='%1.1f%%', startangle=140)
    plt.tight_layout()
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(plt)




def bar_chart(df):
    st.header("Gráfico de barras dos motivos de viagem para o RJ no ano de 2003")
    
    # Ajuste dos dados
    df_melted3 = df.melt(id_vars=['Motivos'], var_name='Ano', value_name='Valor')
    df_melted3['Ano'] = pd.to_numeric(df_melted3['Ano'], errors='coerce')
    df_melted3.dropna(subset=['Valor'], inplace=True)
    df_melted3['Ano'] = df_melted3['Ano'].astype(str)
    df_melted3['Valor'] = df_melted3['Valor'].str.replace(',', '.')
    df_melted3['Valor'] = pd.to_numeric(df_melted3['Valor'], errors='coerce')
    df_final3 = df_melted3[df_melted3["Ano"] == "2003"]

    # Criar o gráfico de barras
    plt.figure(figsize=(8, 4))
    sns.barplot(x='Motivos', y='Valor', data=df_final3)
    plt.xticks(rotation=45)
    plt.title('Motivos de Viagem (2003)')
    plt.xlabel('Motivos')
    plt.ylabel('Valor')

    st.pyplot(plt)




def scatter_plot(df):
    st.header("Scatter Plot dos motivos de viagem para o RJ de 1994 a 2003 ")
    
    # Ajuste dos dados
    df_melted4 = df.melt(id_vars=['Motivos'], var_name='Ano', value_name='Valor')
    df_melted4['Ano'] = pd.to_numeric(df_melted4['Ano'], errors='coerce')
    df_melted4.dropna(subset=['Valor'], inplace=True)
    df_melted4['Ano'] = df_melted4['Ano'].astype(str)
    df_melted4['Valor'] = df_melted4['Valor'].str.replace(',', '.')
    df_melted4['Valor'] = pd.to_numeric(df_melted4['Valor'], errors='coerce')

    x = df_melted4['Motivos']
    y = df_melted4['Valor']

    # Criar o gráfico de scatter plot
    plt.figure(figsize=(8, 4))
    sns.scatterplot(x=x, y=y)
    plt.xticks(rotation=45)
    plt.title('Scatter Plot: Motivos vs. Valor')
    plt.xlabel('Motivos')
    plt.ylabel('Valor')

    st.pyplot(plt)



def mean_lazer(df):
    st.header("Média dos valores de lazer no periodo inteiro")

    # Ajuste dos dados
    df_melted5 = df.melt(id_vars=['Motivos'], var_name='Ano', value_name='Valor')
    df_melted5['Ano'] = pd.to_numeric(df_melted5['Ano'], errors='coerce')
    df_melted5.dropna(subset=['Valor'], inplace=True)
    df_melted5['Ano'] = df_melted5['Ano'].astype(str)
    df_melted5['Valor'] = df_melted5['Valor'].str.replace(',', '.')
    df_melted5['Valor'] = pd.to_numeric(df_melted5['Valor'], errors='coerce')
    df_final5 = df_melted5[df_melted5["Motivos"] == "Lazer"]

    media = df_final5['Valor'].mean()
    st.metric(label="Média dos valores de Lazer", value=f"{media:.2f}")


def mean_negocios(df):
    st.header("Média dos valores de negócios no periodo inteiro")

    # Ajuste dos dados
    df_melted5 = df.melt(id_vars=['Motivos'], var_name='Ano', value_name='Valor')
    df_melted5['Ano'] = pd.to_numeric(df_melted5['Ano'], errors='coerce')
    df_melted5.dropna(subset=['Valor'], inplace=True)
    df_melted5['Ano'] = df_melted5['Ano'].astype(str)
    df_melted5['Valor'] = df_melted5['Valor'].str.replace(',', '.')
    df_melted5['Valor'] = pd.to_numeric(df_melted5['Valor'], errors='coerce')
    df_final5 = df_melted5[df_melted5["Motivos"] == "Negócios"]

    media_negocios = df_final5['Valor'].mean()
    st.metric(label="Média dos valores de Negócios", value=f"{media_negocios:.2f}")



def mean_visitas_amigos(df):
    st.header("Média dos valores de Visita a familiares/amigos no periodo inteiro")

    # Ajuste dos dados
    df_melted5 = df.melt(id_vars=['Motivos'], var_name='Ano', value_name='Valor')
    df_melted5['Ano'] = pd.to_numeric(df_melted5['Ano'], errors='coerce')
    df_melted5.dropna(subset=['Valor'], inplace=True)
    df_melted5['Ano'] = df_melted5['Ano'].astype(str)
    df_melted5['Valor'] = df_melted5['Valor'].str.replace(',', '.')
    df_melted5['Valor'] = pd.to_numeric(df_melted5['Valor'], errors='coerce')
    df_final5 = df_melted5[df_melted5["Motivos"] == "Visita a familiares/amigos"]

    media_amigos = df_final5['Valor'].mean()
    st.metric(label="Média dos valores de Visita a familiares/amigos", value=f"{media_amigos:.2f}")


def filter_data(df):

    # Seleção da categoria filtrada
    st.subheader("Selecione a categoria (motivo) desejada para filtrar os dados")
    categorias = df["Motivos"].unique()
    st.session_state.categoria_selecionada = st.multiselect(
        'Escolha a Categoria',
        categorias,
        default=st.session_state.categoria_selecionada
    )
    df_filtrado = df[df['Motivos'].isin(st.session_state.categoria_selecionada)]
    
    st.session_state.mostrar_detalhes = st.checkbox(
        'Mostrar detalhes da categoria selecionada',
        value=st.session_state.mostrar_detalhes
    )
    
    if st.session_state.mostrar_detalhes:
        with st.spinner('Carregando dados...'):
            time.sleep(3)
            st.write('Dados Detalhados:')
            st.dataframe(df_filtrado)

    # Seleção das colunas filtradas
    st.subheader("Selecione as colunas desejadas para filtrar os dados")
    colunas = df.columns
    st.session_state.seleciona_colunas = [
        coluna for coluna in colunas
        if st.checkbox(f'Mostrar coluna: {coluna}', value=coluna in st.session_state.seleciona_colunas)
    ]
    
    if st.session_state.seleciona_colunas:
        st.write('Dados com colunas selecionadas:')
        st.dataframe(df_filtrado[st.session_state.seleciona_colunas])
    else:
        st.write('Nenhuma coluna selecionada.')

    # Download dos dados filtrados em CSV
    st.subheader("Download dos dados filtrados")
    if not df_filtrado.empty:
        if st.button('Baixar Dados Filtrados'):
            progresso = st.progress(0)
            csv = df_filtrado.to_csv(index=False)
            for i in range(100):
                time.sleep(0.01)
                progresso.progress(i + 1)
    
            st.write("Processamento concluído! Agora você pode baixar o arquivo.")
            st.download_button(
                label="Download Dados Filtrados",
                data=csv,
                file_name='dados_filtrados.csv',
                mime='text/csv'
            )


def colors():
    # Seletor de cores
    cor_fundo = st.color_picker('Escolha a cor de fundo do painel', '#060000')
    cor_fonte = st.color_picker('Escolha a cor das fontes', '#FFFFFF')

    # Aplicar estilo com CSS
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {cor_fundo};
        }}
        .stApp [data-testid="stSidebar"] {{
            background-color: {cor_fundo};
        }}
        .stApp {{
            color: {cor_fonte};
        }}
        </style>
        """, unsafe_allow_html=True)

    # Retornar as cores selecionadas
    return cor_fundo, cor_fonte


if __name__ == "__main__":
    initialize_session_state()
    colors()
    initial()
    download_csv()
    table(df)
    bar_chart(df)
    line_chart(df)
    pie_chart(df)
    scatter_plot(df)
    mean_lazer(df)
    mean_negocios(df)
    mean_visitas_amigos(df)
    filter_data(df)
