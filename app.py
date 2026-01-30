import streamlit as st
import pandas as pd

st.title('都道府県別・男女別総人口')

df = pd.read_csv(
    'FEH_00200524_260130121431.csv',
    encoding='utf-8-sig'
)

with st.sidebar:
    st.subheader('抽出条件')
    population = st.selectbox('都道府県を選択してください',
                              df['全国・都道府県'])

df = df[df['全国・都道府県'] == population]

df = df[['男女別', '全国・都道府県', 
         '2005年', '2010年', '2015年', '2020年',
         '2021年', '2022年', '2023年', '2024年']]

df.columns = df.columns.str.replace('\ufeff', '', regex=False).str.strip()
st.dataframe(df)

st.subheader('男女別人口')
year_cols = ['2005年','2010年','2015年','2020年',
             '2021年','2022年','2023年','2024年']
for c in year_cols:
    df[c] = df[c].str.replace(',', '').astype(int)

df_long = df.melt(
    id_vars=['全国・都道府県', '男女別'],
    value_vars=year_cols,
    var_name='year',
    value_name='population'
)

pivot_df = df_long.pivot_table(
    index=['全国・都道府県', '男女別'],
    columns='year',
    values='population',
    aggfunc='sum'
)
st.bar_chart(
    df_long,
    x='year',
    y='population',
    color='男女別'
)
