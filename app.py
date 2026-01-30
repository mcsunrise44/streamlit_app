import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts

st.title('人口推計 各年10月1日現在人口 令和２年国勢調査基準 統計表')

st.header('都道府県別総人口')
df = pd.read_csv(
    'FEH_00200524_260130121431.csv',
    encoding='utf-8-sig'
)

with st.sidebar:
    st.subheader('抽出条件')
    prefectures = st.selectbox('都道府県を選択してください',
                              df['全国・都道府県'].unique())
    
    chart_type = st.radio(
        'グラフ形式を選択してください',
        ['棒グラフ', '折れ線グラフ']
    )

df = df[df['全国・都道府県'] == prefectures]

df = df[['男女別', '全国・都道府県', 
         '2005年', '2010年', '2015年', '2020年',
         '2021年', '2022年', '2023年', '2024年']]

df.columns = df.columns.str.replace('\ufeff', '', regex=False).str.strip()

st.header(f'{prefectures}の男女別人口推移')
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

df_long = df_long[df_long['男女別'] != '男女計']

st.dataframe(df)

st.bar_chart(
    df_long,
    x='年',
    y='人口（人）',
    color='男女別'
)

st.line_chart(
    df_long,
    x='年',
    y='人口（人）',
    color='男女別'
)

