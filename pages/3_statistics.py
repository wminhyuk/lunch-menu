import streamlit as st
import pandas as pd
from lunch_menu.db import select_table

st.subheader("통계")

select_df = select_table()

gdf = select_df.groupby('ename')['menu'].count().reset_index()
gdf
