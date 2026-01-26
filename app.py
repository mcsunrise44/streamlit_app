import streamlit as st
import pandas as pd

st.title('野菜収穫量/出荷量')

df = pd.read_csv('FEH_00500215_260126105748.csv')

with st.sidebar:
    st.subheader('抽出条件')
    a = st.multiselect('野菜の種類を選択してください',
                       df['(F005-05-2-002)品目'])