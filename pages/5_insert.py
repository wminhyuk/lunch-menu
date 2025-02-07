import streamlit as st
import pandas as pd
from lunch_menu.db import get_connection
from lunch_menu.db import db_name
from lunch_menu.db import insert_menu
from lunch_menu.db import select_table

members = {"SEO": 5, "TOM": 1, "cho": 2, "hyun": 3, "nuni": 10, "JERRY": 4, "jacob": 7, "jiwon": 6, "lucas": 9, "heejin": 8}

st.subheader("벌크 인서트")
if st.button("한방에 인서트"):
    df = pd.read_csv('lunch_menu.csv')
    start_idx = df.columns.get_loc('2025-01-07')
    melted_df = df.melt(id_vars=['ename'], value_vars=df.columns[start_idx:-2],
                        var_name='dt', value_name='menu')
    not_na_df = melted_df[~melted_df['menu'].isin(['-','x','<결석>'])]
    total_count = len(not_na_df)  # 총 건수
    success_count = sum(insert_menu(row['menu'], members[row['ename']], row['dt']) for _, row in not_na_df.iterrows())
    for _, row in not_na_df.iterrows():
        m_id = members[row['ename']]
        insert_menu(row['menu'], m_id, row['dt'])

    if success_count == total_count:
        st.success(f"벌크 인서트 성공!")
    else:
        fail_count = total_count - success_count
        st.error(f"벌크 인서트 총 {total_count}건 중 {fail_count}건 실패")
