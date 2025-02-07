import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from lunch_menu.db import get_connection
from lunch_menu.db import db_name
from lunch_menu.db import insert_menu
from lunch_menu.db import select_table

members = {"SEO": 5, "TOM": 1, "cho": 2, "hyun": 3, "nuni": 10, "JERRY": 4, "jacob": 7, "jiwon": 6, "lucas": 9, "heejin": 8}

st.title(f"순신점심기록장!")

st.subheader("확인")

# 함수로 빼서 db.py로 이동시키기...
select_df = select_table()
select_df

st.subheader("통계")
df = pd.read_csv('lunch_menu.csv')

start_idx = df.columns.get_loc('2025-01-07')
melted_df = df.melt(id_vars=['ename'], value_vars=df.columns[start_idx:-2],
                    var_name='dt', value_name='menu')
not_na_df = melted_df[~melted_df['menu'].isin(['-','x','<결석>'])]
#gdf = not_df.groupby('ename')['menu'].count().reset_index()
gdf = select_df.groupby('ename')['menu'].count().reset_index()

gdf


# Matplotlib롤 바 차트 그리기
try:
    fig, ax = plt.subplots()
    gdf.plot(x="ename", y="menu", kind="bar", ax=ax)
    st.pyplot(fig)
except Exception as e:
    st.warning(f"차트를 그리기에 충분한 데이터가 없습니다")
    print(f"Exception:{e}")

# TODO
# CSV 로드해서 한번에 다 디비에 INSERT 하는거
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




#if isPress2:
#    conn = get_connection()
#    cursor = conn.cursor()
#    df = pd.read_csv('lunch_menu.csv')
#    start_idx = df.columns.get_loc('2025-01-07')
#    for _, row in df.iterrows():  # 모든 행을 순회
#        for c in df.columns[start_idx:]:
#            cursor.execute(
#            "INSERT INTO lunch_menu (menu_name, member_name, dt) VALUES (%s, %s, %s);",
#                  (menu_name, member_name, dt)
#                 )
#    #conn.commit()
#    cursor.close()



# 점심 안먹은 인원색출
st.subheader("오늘 점심 메뉴를 정하지 않은 사람 ")
if st.button("색출하기"):
    today = datetime.today().strftime('%Y-%m-%d')
    query_today = """
    SELECT DISTINCT 
    l.menu_name,
    m.name,
    l.dt
    FROM
    lunch_menu l
    inner join member m on l.member_id = m.id
    WHERE l.dt = %s
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query_today, (today,))
    members_with_menu = {row[0] for row in cursor.fetchall()}
    cursor.close()
    conn.close()

    members_without_menu = set(members.keys()) - members_with_menu
    if members_without_menu:
        st.warning("범인:")
        st.write(", ".join(members_without_menu))
    else:
        st.success("모든 사람이 오늘 메뉴를 정했습니다!")
