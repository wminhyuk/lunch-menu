import streamlit as st
import pandas as pd
from lunch_menu.db import insert_menu
from lunch_menu.db import get_connection

st.subheader("확인")
query = """
SELECT
	l.menu_name,
	m.name,
	l.dt
FROM
	lunch_menu l
	inner join member m
	on l.member_id = m.id
"""

conn = get_connection()
cursor = conn.cursor()
cursor.execute(query)
rows = cursor.fetchall()
cursor.close()
conn.close()

#selected_df = pd.DataFrame([[1,2,3],[4,5,6]], columns=['a','b','c'])
select_df = pd.DataFrame(rows, columns=['menu','ename','dt'])
select_df
