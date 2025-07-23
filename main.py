import streamlit as st

# --- 페이지 기본 스타일 ---
st.markdown("""
    <style>
    body, .stApp {
        background-color: #111 !important;
        color: #fff !important;
    }
    .dino-card {
        display: flex;
        align-items: center;
        background: rgba(20,20,20,0.98);
        border-radius: 1.5em;
        margin-bottom: 2.5em;
        box-shadow: 0 4px 24px #0008;
        transition: box-shadow 0.3s;
        padding: 2em 1em;
        opacity: 0;
        animation: fadeInUp 1.2s ease-out forwards;
    }
    .dino-img {
        width: 260px;
        height: 160px;
        object-fit: cover;
        border-radius: 1em;
        box-shadow: 0 0 32px #7ef9ff22;
        margin-right: 2em;
        transition: transform 0.35s cubic-bezier(.33,2,.22,.8), box-shadow 0.3s;
        cursor: pointer;
    }
    .dino-img:hover {
        transform: scale(1.13) rotate(-2deg);
        box-shadow: 0 0 64px #00fff9cc, 0 0 32px #fffb;
        z-index: 2;
    }
    .dino-title {
        font-size: 2.1em;
        font-weight: bold;
        margin-bottom: 0.6em;
        color: #fff;
        text-shadow: 0 0 16px #fff7, 0 0 24px #00fff933;
        letter-spacing: 1.5px;
    }
    .dino-desc {
        font-size: 1.12em;
        color: #fff;
        text-shadow: 0 0 7px #00fff944;
    }
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(80px) scale(0.97);
        }
        to {
            opacity: 1;
            transform: none;
        }
    }
    </style>
""", unsafe_allow_html=True)

dino_data = [
    {
        "name": "티라노사우르스",
        "img": "https://static.turbosquid.com/Preview/001304/868/KG/Z.jpg",
        "desc": "티라노사우루스(Tyrannosaurus)는 백악기 후기에 북아메리카에서 살았던 육식공룡의 왕. 길이 약 12m, 키 4m, 무게 6~9톤. 압도적인 턱 힘과 사냥 실력으로 악명이 높았다."
    },
    {
        "name": "알로사우르스",
        "img": "https://tse1.mm.bing.net/th/id/OIP.jNBXbE7eq0QdKu0uGOrr-AHaEr?rs=1&pid=ImgDetMain&o=7&rm=3",
        "desc": "알로사우루스(Allosaurus)는 쥐라기 후기의 포식자로, 약 8.5m 길이에 재빠른 움직임이 특징. 당시 '톱 포식자' 중 하나로 평가받았다."
    },
    {
        "name": "파키케팔로사우르스",
        "img": "https://tse1.mm.bing.net/th/id/OIP.6A_YOwXpMtd2fHy-QrI20QHaE7?rs=1&pid=ImgDetMain&o=7&rm=3",
        "desc": "파키케팔로사우루스(Pachycephalosaurus)는 두개골이 25cm 두께로 매우 단단해, 머리로 박치기 싸움을 벌였던 초식공룡. 백악기 후기 북미에서 발견됨."
    },
    {
        "name": "안킬로사우르스",
        "img": "https://png.pngtree.com/thumb_back/fw800/background/20230612/pngtree-3d-animation-of-an-extinct-dinosaur-image_2920885.jpg",
        "desc": "안킬로사우루스(Ankylosaurus)는 전신이 갑옷처럼 덮여 있고, 꼬리에는 곤봉이 달린 방어의 대명사. 천적도 함부로 건드리지 못했던 강인한 초식공룡."
    },
]

st.markdown('<div style="text-align:center; font-size:3em; font-weight:bold; margin-bottom:0.7em; color:#fff; text-shadow:0 0 20px #00fff9, 0 0 60px #fff3;">🦖 공룡 사전</div>', unsafe_allow_html=True)

for idx, dino in enumerate(dino_data):
    # 각 카드에 순차적 fade-in 딜레이를 주고싶으면 animation-delay 추가 가능
    st.markdown(f"""
        <div class="dino-card" style="animation-delay: {idx * 0.3}s">
            <img src="{dino['img']}" class="dino-img" alt="{dino['name']}"/>
            <div>
                <div class="dino-title">{dino['name']}</div>
                <div class="dino-desc">{dino['desc']}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="text-align:center; opacity:0.7; margin-top:2em; font-size:1.2em;">by monday ✨</div>', unsafe_allow_html=True)
