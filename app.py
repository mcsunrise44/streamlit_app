import streamlit as st
import pandas as pd

st.title('2023年度野菜別収穫量/出荷量')

df = pd.read_csv(
    'FEH_00500215_260126105748.csv',
    encoding='utf-8-sig'
)

with st.sidebar:
    st.subheader('抽出条件')
    vesitable_series = st.multiselect('野菜を選択してください（複数選択可）',
                       df['品目'].unique())
    st.subheader('色分け')
    color = st.selectbox('分類を選択してください',
                      ['作付面積【ha】', '収穫量【t】', '出荷量【t】'])
    
df = df[df['品目'].isin(vesitable_series)]
df.drop('(F005-05-2-002)品目 コード',axis=1,inplace=True)
df.drop('(F005-05-2-002)品目 補助コード',axis=1,inplace=True)
df.drop('作付面積、収穫量及び出荷量',axis=1,inplace=True)

st.dataframe(df)

df.columns = df.columns.str.replace('\ufeff', '', regex=False).str.strip()
df = df.sort_values('収穫量【t】', ascending=False)

st.bar_chart(
    df,
    x="出荷量【t】",
    y="収穫量【t】",
    color="品目",
    stack=False
)