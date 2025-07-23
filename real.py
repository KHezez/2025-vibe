import streamlit as st
import random
import time

# ===== 데이터 준비 =====
short_sentences = [
    "The sky is blue.",
    "I love pizza.",
    "Type as fast as you can.",
    "Python is fun.",
    "This is a short test."
]
word_pool = [
    "apple", "banana", "orange", "cat", "dog", "house", "river", "train", "car",
    "mouse", "keyboard", "window", "light", "night", "happy", "sad", "smile", "fire",
    "water", "book", "door", "game", "star", "sun", "moon", "love", "friend", "music"
]

# ===== 세션 상태 초기화 =====
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "done" not in st.session_state:
    st.session_state.done = False
if "target_text" not in st.session_state:
    st.session_state.target_text = ""
if "mode" not in st.session_state:
    st.session_state.mode = "Short Sentence"
if "theme" not in st.session_state:
    st.session_state.theme = "Light"
if "results" not in st.session_state:
    st.session_state.results = None

# ===== 테마 설정 =====
THEMES = {
    "Light": {
        "background": "#fafafa",
        "text": "#111",
        "input_bg": "#fff",
        "input_text": "#111"
    },
    "Black": {
        "background": "#23272f",
        "text": "#fafafa",
        "input_bg": "#292d36",
        "input_text": "#fafafa"
    }
}
theme = THEMES[st.session_state.theme]

# CSS 주입
st.markdown(
    f"""
    <style>
    body {{ background: {theme['background']} !important; color: {theme['text']} !important; }}
    .stTextInput > div > div > input {{ background-color: {theme['input_bg']} !important; color: {theme['input_text']} !important; }}
    .stTextInput > div > div > input:focus {{ background-color: #e0e0e0 !important; }}
    </style>
    """,
    unsafe_allow_html=True
)

# ===== 타이틀 & 테마 선택 =====
st.markdown(f"<h1 style='color: {theme['text']};'>영타 연습 웹사이트</h1>", unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])
with col2:
    new_theme = st.radio("테마 선택", ("Light", "Black"), index=0 if st.session_state.theme=="Light" else 1)
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.experimental_rerun()

# ===== 모드 선택 =====
mode = st.radio("모드 선택", ["Short Sentence", "Word", "15 Word Challenge"], index=["Short Sentence", "Word", "15 Word Challenge"].index(st.session_state.mode))
if mode != st.session_state.mode:
    st.session_state.mode = mode
    st.session_state.start_time = None
    st.session_state.done = False
    st.session_state.results = None
    st.session_state.target_text = ""

# ===== 타겟 텍스트 생성 =====
if not st.session_state.target_text or st.button("새로고침"):
    if st.session_state.mode == "Short Sentence":
        st.session_state.target_text = random.choice(short_sentences)
    elif st.session_state.mode == "Word":
        st.session_state.target_text = random.choice(word_pool)
    elif st.session_state.mode == "15 Word Challenge":
        st.session_state.target_text = " ".join(random.sample(word_pool, 15))
    st.session_state.start_time = None
    st.session_state.done = False
    st.session_state.results = None

# ===== 타이핑 입력 =====
st.markdown(f"<p style='color: {theme['text']}; font-size:1.2em;'><b>아래 텍스트를 입력하세요:</b></p>", unsafe_allow_html=True)
st.code(st.session_state.target_text, language="markdown")

input_key = "typing_input"
if st.session_state.done:
    user_input = ""
else:
    user_input = st.text_input("여기에 입력:", key=input_key, value="", disabled=st.session_state.done)

# ===== 타이머 및 결과 =====
if not st.session_state.done and user_input and st.session_state.start_time is None:
    st.session_state.start_time = time.time()

if not st.session_state.done and user_input == st.session_state.target_text:
    elapsed = time.time() - st.session_state.start_time
    char_count = len(st.session_state.target_text)
    word_count = len(st.session_state.target_text.split())
    wpm = (char_count/5) / (elapsed/60)
    accuracy = 100  # 정답만 체크
    st.session_state.done = True
    st.session_state.results = {
        "elapsed": elapsed,
        "wpm": wpm,
        "word_count": word_count,
        "char_count": char_count
    }
    st.success(f"🎉 완료! 시간: {elapsed:.2f}초 | WPM: {wpm:.2f} | 단어 수: {word_count}")
    st.balloons()
elif user_input and not st.session_state.done:
    # 실시간 오타 체크
    correct_chars = sum(1 for a, b in zip(user_input, st.session_state.target_text) if a == b)
    accuracy = correct_chars / len(st.session_state.target_text) * 100
    st.info(f"실시간 정확도: {accuracy:.2f}%")

if st.session_state.results:
    st.markdown("---")
    st.write("**결과 요약**")
    st.write(f"- 소요 시간: {st.session_state.results['elapsed']:.2f}초")
    st.write(f"- WPM: {st.session_state.results['wpm']:.2f}")
    st.write(f"- 단어 수: {st.session_state.results['word_count']}개")
    st.write(f"- 문자 수: {st.session_state.results['char_count']}자")

st.caption("mini monkeytype powered by Fury & monday")
