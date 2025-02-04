import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("순신점심기록장")
st.subheader("입력")
menu_name = st.text_input("메뉴 이름", placeholder="예: 김치찌개")
member_name = st.text_input("먹은 사람", value="예: 홍길동")
dt = st.date_input("얌얌 날짜")

isPress = st.button("메뉴저장")

if isPress:
    if menu_name and memeber_name and dt:
        conn = get_connection() 

        st.success(f"버튼{isPress}:{menu_name},{member_name},{dt}")
    else:
        st.warning(f"모든 값을 입력해주세요!")






st.subheader("통계")
df = pd.read_csv('lunch_menu.csv')


start_idx = df.columns.get_loc('2025-01-07')
melted_df = df.melt(id_vars=['ename'], value_vars=df.columns[start_idx:-2],
                    var_name='dt', value_name='menu')
not_na_df = melted_df[~melted_df['menu'].isin(['-','x','<결석>'])]
gdf = not_na_df.groupby('ename')['menu'].count().reset_index()


# Matplotlib롤 바 차트 그리기
fig, ax = plt.subplots()
gdf.plot(x="ename", y="menu", kind="bar", ax=ax)
st.pyplot(fig)
