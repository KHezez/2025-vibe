import streamlit as st
import random

# 간단한 타이틀 + CSS로 색상 강조
st.markdown(
    """
    <style>
    .title {
        font-size: 2.5em;
        color: #ff914d;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
        text-shadow: 2px 2px 8px #ffd8b5;
    }
    </style>
    <div class="title">🍚 오늘 뭐 먹지? 메뉴 추천기</div>
    """,
    unsafe_allow_html=True
)

menu_list = [
    "김치찌개", "된장찌개", "비빔밥", "치킨", "피자", "라면", "삼겹살", "돈까스",
    "떡볶이", "순두부찌개", "초밥", "제육볶음", "불고기", "냉면", "파스타", "햄버거"
]

if st.button("메뉴 추천받기! 🍴"):
    menu = random.choice(menu_list)
    st.success(f"오늘의 메뉴는... **{menu}** 어떰? 😎")

st.caption("by monday. 오늘도 든든하게 먹어라~")
