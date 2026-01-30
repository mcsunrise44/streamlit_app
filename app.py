import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts

st.title('人口推計 各年10月1日現在人口 令和２年国勢調査基準 統計表')

st.header('都道府県別 男女別 総人口推移表')
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

df = df[['男女別','全国・都道府県',
         '2005年','2010年','2015年','2020年',
         '2021年','2022年','2023年','2024年']]

df.columns = df.columns.str.replace('\ufeff', '', regex=False).str.strip()

year_cols = ['2005年','2010年','2015年','2020年',
             '2021年','2022年','2023年','2024年']
for c in year_cols:
    df[c] = df[c].str.replace(',', '').astype(int)

df_long = df.melt(
    id_vars=['全国・都道府県','男女別'],
    value_vars=year_cols,
    var_name='年',
    value_name='人口(千人)'
)

df_long = df_long[df_long['男女別'] != '男女計']

st.dataframe(df_long)

st.divider()

st.header(f'{prefectures}の男女別人口推移（{chart_type}）')

years = year_cols
male = df_long[df_long['男女別'] == '男']['人口(千人)'].tolist()
female = df_long[df_long['男女別'] == '女']['人口(千人)'].tolist()

series_type = 'bar' if chart_type == '棒グラフ' else 'line'

option = {
    'tooltip': {'trigger':'axis'},
    'legend': {'data':['男','女']},
    'xAxis': {
        'type': 'category',
        'data': years,
    },
    'yAxis': {
        'type': 'value',
        'name': '人口(千人)'
    },
    'series': [
        {
            'name': '男',
            'type': series_type,
            'data': male
        },
        {
            'name': '女',
            'type': series_type,
            'data': female
        }
    ]
}

st_echarts(option)

st.divider()

