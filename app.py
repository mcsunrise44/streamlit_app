import streamlit as st
import pandas as pd

st.title('全国人口推移')

df = pd.read_csv('05k2-2.csv')
