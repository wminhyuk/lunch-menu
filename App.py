import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import psycopg
import os
from dotenv import load_dotenv
from datetime import datetime

members = {"SEO": 5, "TOM": 1, "cho": 2, "hyun": 3, "nuni": 10, "JERRY": 4, "jacob": 7, "jiwon": 6, "lucas": 9, "heejin": 8}

load_dotenv()
db_name = os.getenv("DB_NAME")
DB_CONFIG = {
    "user": os.getenv("DB_USERNAME"),
    "dbname": os.getenv("DB_NAME"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT") 
            }

def get_connection():
    return psycopg.connect(**DB_CONFIG)

def insert_menu(menu_name, member_id, dt):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
                "INSERT INTO lunch_menu (menu_name, member_id, dt) VALUES (%s, %s, %s);",
                (menu_name, member_id, dt)
                )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Exception:{e}")
        return False



st.title(f"순신점심기록장!{db_name}")
st.subheader("입력")
menu_name = st.text_input("메뉴 이름", placeholder="예: 김치찌개")
#member_name = st.text_input("먹은 사람", value="예: 홍길동")
member_name = st.selectbox(
        "먹은 사람",
        options=list(members.keys()),
        index=list(members.keys()).index('TOM')
        )
member_id = members[member_name]
dt = st.date_input("얌얌 날짜")

isPress = st.button("메뉴저장")

if isPress:
    if menu_name and member_id and dt:
        if insert_menu(menu_name, member_id, dt):
            st.success(f"입력성공")
        else:
            st.error(f"입력실패")

    else:
        st.warning(f"모든 값을 입력해주세요!")


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
#conn.commit()
cursor.close()
conn.close()

#selected_df = pd. DataFrame([[1,2,3]],[4,5,6], columns=['a','b','c'])
select_df = pd.DataFrame(rows, columns=['menu', 'ename', 'dt'])
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
    for _, row in not_na_df.iterrows():
        m_id = members[row['ename']]
        insert_menu(row['menu'], m_id, row['dt'])

    st.success(f"벌크 인서트 성공")

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
