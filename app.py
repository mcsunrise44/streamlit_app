import streamlit as st
import pandas as pd

st.title('都道府県別総人口')

df = pd.read_csv(
    'FEH_00200524_260130121431.csv',
    encoding='utf-8-sig'
)

with st.sidebar:
    st.subheader('抽出条件')
    population = st.selectbox('都道府県を選択してください',
                              df['全国・都道府県'].unique())

df = df[df['全国・都道府県'] == population]

df = df[['男女別', '全国・都道府県', 
         '2005年', '2010年', '2015年', '2020年',
         '2021年', '2022年', '2023年', '2024年']]

df.columns = df.columns.str.replace('\ufeff', '', regex=False).str.strip()
st.dataframe(df)

st.subheader('男女別人口推移')
year_cols = ['2005年','2010年','2015年','2020年',
             '2021年','2022年','2023年','2024年']
for c in year_cols:
    df[c] = df[c].str.replace(',', '').astype(int)

df_long = df.melt(
    id_vars=['全国・都道府県', '男女別'],
    value_vars=year_cols,
    var_name='年',
    value_name='人口（人）'
)

pivot_df = df_long.pivot_table(
    index=['全国・都道府県', '男女別'],
    columns='年',
    values='人口（人）',
    aggfunc='sum'
)

df_long = df_long[df_long['男女別'] != '男女計']

st.bar_chart(
    df_long,
    x='年',
    y='人口（人）',
    color='男女別'
)
