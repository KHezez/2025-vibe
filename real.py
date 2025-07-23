import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 초기값 저장용 (세션 상태)
if 'page' not in st.session_state:
    st.session_state.page = 'menu'
if 'ball1' not in st.session_state:
    st.session_state.ball1 = None
if 'ball2' not in st.session_state:
    st.session_state.ball2 = None
if 'started' not in st.session_state:
    st.session_state.started = False

# 1. 메인 메뉴
if st.session_state.page == 'menu':
    st.title("⚪ Ball Battle Arena")
    if st.button("1대1 배틀 시작!"):
        st.session_state.page = 'arena'
        # 경기장 리셋
        st.session_state.ball1 = {
            'pos': np.array([0.3, 0.5]),  # x, y (0~1)
            'vel': np.array([0.01, 0.008]),
            'color': '#FF4466'
        }
        st.session_state.ball2 = {
            'pos': np.array([0.7, 0.5]),
            'vel': np.array([-0.012, 0.007]),
            'color': '#3377FF'
        }
        st.session_state.started = False
    st.write("---")
    st.caption("나중에 모드/설정/캐릭터 추가 가능 👾")

# 2. 아레나 화면
if st.session_state.page == 'arena':
    st.title("⚔️ 1 vs 1 Ball Arena")
    st.write("**SPACEBAR 없이 버튼으로만 진행**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← 메뉴로"):
            st.session_state.page = 'menu'
    with col2:
        if st.button("Start" if not st.session_state.started else "Stop"):
            st.session_state.started = not st.session_state.started
    with col3:
        if st.button("Next Step"):
            st.session_state.started = False  # 일시정지 후 1스텝

    # 위치 업데이트(움직이기)
    def update_balls():
        for ball in [st.session_state.ball1, st.session_state.ball2]:
            ball['pos'] += ball['vel']
            # 벽 반사 (0~1 경계)
            for i in range(2):
                if ball['pos'][i] <= 0.05 or ball['pos'][i] >= 0.95:
                    ball['vel'][i] *= -1
                    ball['pos'][i] = np.clip(ball['pos'][i], 0.05, 0.95)

    # 프레임 갱신 (실시간 대신 버튼 누를때마다)
    if st.session_state.started or st.button("프레임 진행"):
        update_balls()

    # 경기장 시각화 (matplotlib)
    fig, ax = plt.subplots(figsize=(5,5))
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    ax.set_facecolor('white')
    ax.add_patch(plt.Rectangle((0,0),1,1, fill=False, edgecolor='black', lw=4))

    # 공 그리기
    for ball in [st.session_state.ball1, st.session_state.ball2]:
        circle = plt.Circle(ball['pos'], 0.05, color=ball['color'])
        ax.add_patch(circle)
    ax.set_xticks([]); ax.set_yticks([])
    st.pyplot(fig)

    st.caption("버튼으로 프레임 갱신 (Start 누르면 자동, Next Step은 1스텝만)")

    # 공 위치 정보 표시 (테스트용)
    with st.expander("공 위치/속도 정보 보기 (테스트용)"):
        st.write("Ball 1:", st.session_state.ball1)
        st.write("Ball 2:", st.session_state.ball2)
