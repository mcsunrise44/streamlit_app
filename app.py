import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts

st.title('都道府県別・男女別人口推移と増減率分析用Webアプリ')

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

st.header(f'{prefectures}の男女別総人口推移表')

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

oldest_year = '2005年'
latest_year = '2024年'

male_2005 = df_long[
    (df_long['男女別'] == '男') & (df_long['年'] == oldest_year)
]['人口(千人)'].iloc[0]

male_2024 = df_long[
    (df_long['男女別'] == '男') & (df_long['年'] == latest_year)
]['人口(千人)'].iloc[0]

female_2005 = df_long[
    (df_long['男女別'] == '女') & (df_long['年'] == oldest_year)
]['人口(千人)'].iloc[0]

female_2024 = df_long[
    (df_long['男女別'] == '女') & (df_long['年'] == latest_year)
]['人口(千人)'].iloc[0]

male_rate_2005_2024 = (male_2024 - male_2005) / male_2005 * 100
female_rate_2005_2024 = (female_2024 - female_2005) / female_2005 * 100

st.header(f'{prefectures}の人口増減率の比較')

col1, col2 = st.columns(2)

col1.metric(
    '2005年度と2024年度の増減率（男）',
    f'{male_rate_2005_2024:+.2f} %'
)

col2.metric(
    '2005年度と2024年度の増減率（女）',
    f'{female_rate_2005_2024:+.2f} %'
)

st.divider()

st.header('結果の解釈・説明')

st.markdown(
    """
全国で見た場合、男の総人口は2005年から常に減少し続けており、女の総人口は2005年から2010年にかけて増加したもののそれ以降は減少し続けている。
また2005年度と2024年度を比較した人口増減率は男は:red[**-3.39%**]、女は:red[**-2.83%**]とどちらもマイナスである。
一方首都である東京都で見た場合、男の総人口・女の総人口ともに2020年から2021年に多少減少したものの、2005年から2024年にかけて増加傾向にある。
また2005年度と2024年度を比較した人口増減率は男は:green[**+11.09%**]、女は:green[**+14.35%**]とどちらも大幅に増加している。
このことから:red[**全国の総人口自体は減少傾向にあるが、都市部の総人口は増加傾向にあると解釈でき、
少子化問題や若者の都市部への流出が原因**]ではないかと考えられる。
    """)