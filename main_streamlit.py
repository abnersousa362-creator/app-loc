import streamlit as st
import pandas as pd
import os

# --- Título do app ---
st.set_page_config(page_title="App Loc", page_icon="🔍")
st.title("🔧 App Loc - Localizador de Peças")

# --- Carregar catálogo ---
if os.path.exists("catalogo.csv"):
    df = pd.read_csv("catalogo.csv")
else:
    st.error("❌ Arquivo catalogo.csv não encontrado. Envie-o para o mesmo diretório do app.")
    st.stop()

# --- Campo de busca ---
part_number = st.text_input("Digite o Part Number para buscar:")

# --- Executar busca ---
if part_number:
    resultados = df[df.astype(str).apply(lambda x: x.str.contains(part_number, case=False, na=False)).any(axis=1)]
    
    if not resultados.empty:
        st.success(f"✅ {len(resultados)} resultado(s) encontrado(s):")
        st.dataframe(resultados)
    else:
        st.warning("Nenhum resultado encontrado para esse Part Number.")
else:
    st.info("Digite um código ou parte do Part Number acima para buscar.")
