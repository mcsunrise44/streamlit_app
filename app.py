import streamlit as st
import pandas as pd

st.title('都道府県，男女別人口－総人口，日本人人口')

df = pd.read_csv(
    'FEH_00200524_260130121431.csv',
    encoding='utf-8-sig'
)

with st.sidebar:
    st.subheader('抽出条件')
    vesitable_series = st.multiselect('条件を選択してください（複数選択可）',
                       df['全国・都道府県 コード'].unique())
    st.subheader('色分け')
    color = st.selectbox('分類を選択してください',
                      ['男女別 コード','人口 コード','2005年','2010年','2015年','2020年','2021年','2022年','2023年','2024年'])
    
df = df[df['全国・都道府県 コード'].isin(vesitable_series)]

df.columns = df.columns.str.replace('\ufeff', '', regex=False).str.strip()
st.dataframe(df)

