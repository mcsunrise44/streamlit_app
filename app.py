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
                       df['全国・都道府県'].unique())

df = df[df['全国・都道府県'].isin(vesitable_series)]

df.drop('表章項目 コード',axis=1,inplace=True)
df.drop('表章項目 補助コード',axis=1,inplace=True)
df.drop('表章項目',axis=1,inplace=True)
df.drop('男女別 コード',axis=1,inplace=True)
df.drop('男女別 補助コード',axis=1,inplace=True)
df.drop('人口 コード',axis=1,inplace=True)
df.drop('人口 補助コード',axis=1,inplace=True)
df.drop('全国・都道府県 コード',axis=1,inplace=True)
df.drop('全国・都道府県 補助コード',axis=1,inplace=True)
df.drop('/時間軸（年）',axis=1,inplace=True)

df.columns = df.columns.str.replace('\ufeff', '', regex=False).str.strip()
st.dataframe(df)

