import streamlit as st
from lunch_menu.db import insert_menu

st.set_page_config(page_title="Input", page_icon="🍽️")

st.markdown("# 🍽️ INPUT Menu")
st.sidebar.header("INPUT Menu")

## TODO - 메뉴 입력하기 부분 코드 이동시키기
members = {"SEO": 5, "TOM": 1, "cho": 2, "hyun": 3, "nuni": 10, "JERRY": 4, "jacob": 7, "jiwon": 6, "lucas": 9, "heejin": 8}

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
