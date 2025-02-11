import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from lunch_menu.db import get_connection
from lunch_menu.db import db_name
from lunch_menu.db import insert_menu
from lunch_menu.db import select_table


st.subheader("차트")

select_df = select_table()
gdf = select_df.groupby('ename')['menu'].count().reset_index()
# https://docs.streamlit.io/develop/api-reference/charts/st.pyplot
try:
    fig, ax = plt.subplots()
    gdf.plot(x="ename", y="menu", kind="bar", ax=ax)
    st.pyplot(fig)
except Exception as e:
    st.warning(f"차트를 그리기에 충분한 데이터가 없습니다")
    print(f"Exception:{e}")


