import streamlit as st
st.title('나의 첫 웹서비으ㅓ 어ㅓ러ㅏ')
name = st.text_input('이름을 입력해주세요:::')
menu = st.selectbox('좋아하는 음식을 선택해주세요:', ['망고빙수','아몬드봉봉','벌레'])
if st.button ('인사말 생성'):
  st.write(name+'님!'+menu+'를 좋아하네요')
  
