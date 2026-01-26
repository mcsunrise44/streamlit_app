import streamlit as st
import pandas as pd

st.title('野菜収穫量/出荷量')

df = pd.read_csv('FEH_00500215_260126105748.csv')

with st.sidebar:
    st.subheader('抽出条件')
    vesitable_series = st.multiselect('野菜の種類を選択してください',
                       df['(F005-05-2-002)品目'])
    st.subheader('色分け')    
    color = st.selectbox('分類を選択してください',
                      ['作付面積【ha】', '収穫量【t】', '出荷量【t】'])
    
df = df[df['(F005-05-2-002)品目'].isin(vesitable_series)]

st.dataframe(df)
