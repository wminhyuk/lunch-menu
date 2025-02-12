import streamlit as st
import requests
import lunch_menu.constants as const
import datetime 


st.set_page_config(page_title="API", page_icon="🍽️")

st.markdown("# 🍽️ API")
st.sidebar.header("나이계산기")

dt = st.date_input("생일입력", min_value=datetime.date(1900,1,1))
if st.button("메뉴 저장"):
    headers = {
        'accept' : 'application/json'            
        }
    r = requests.get(f'{const.API_AGE}/{dt}', headers=headers)
    if r.status_code == 200:
        # TODO age 받아 오는 부분을 만들어주세요.
        data = r.json()
        age = data['age']
        st.success(f"{dt} 일생의 나이는 {age} 입니다.")
    else:
        st.error(f"문제가 발생하였습니다. 관리자 문의:{r.status_code}")


