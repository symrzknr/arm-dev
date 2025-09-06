import streamlit as st
import pandas as pd

df = pd.DataFrame({"column_1": [1,2,3,4], "column_2": [4,3,2,1]})

st.title("Streamlit app running on docker")
st.dataframe(df)
st.dataframe(df)