import streamlit as st

# ----- 기존 공룡 카드 -----
st.markdown("""
    <style>
    body, .stApp { background-color: #111 !important; color: #fff !important; }
    .dino-card { display: flex; align-items: center; background: rgba(20,20,20,0.98); border-radius: 1.5em; margin-bottom: 2.5em; box-shadow: 0 4px 24px #0008; transition: box-shadow 0.3s; padding: 2em 1em; opacity: 0; animation: fadeInUp 1.2s ease-out forwards;}
    .dino-img { width: 260px; height: 160px; object-fit: cover; border-radius: 1em; box-shadow: 0 0 32px #7ef9ff22; margin-right: 2em; transition: none; cursor: pointer;}
    .dino-title { font-size: 2.1em; font-weight: bold; margin-bottom: 0.6em; color: #fff; text-shadow: 0 0 16px #fff7, 0 0 24px #00fff933; letter-spacing: 1.5px;}
    .dino-desc { font-size: 1.12em; color: #fff; text-shadow: 0 0 7px #00fff944;}
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(80px) scale(0.97);} to { opacity: 1; transform: none;}}
    </style>
""", unsafe_allow_html=True)

dino_data = [
    {
        "name": "티라노사우르스",
        "img": "https://static.turbosquid.com/Preview/001304/868/KG/Z.jpg",
        "desc": "티라노사우루스(Tyrannosaurus)는 백악기 후기에 북아메리카에서 살았던 육식공룡의 왕. 길이 약 12m, 키 4m, 무게 6~9톤. 압도적인 턱 힘과 사냥 실력으로 악명이 높았다."
    },
    {
        "name": "알로사우루스",
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
    st.markdown(f"""
        <div class="dino-card" style="animation-delay: {idx * 0.3}s">
            <img src="{dino['img']}" class="dino-img" alt="{dino['name']}"/>
            <div>
                <div class="dino-title">{dino['name']}</div>
                <div class="dino-desc">{dino['desc']}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ----- 코끼리 vs 티라노 카드 -----
st.markdown("""
    <style>
    .battle-card {
        background: linear-gradient(120deg, #1b232a 60%, #2c1e19 100%);
        border-radius: 2em;
        margin: 30px 0 50px 0;
        box-shadow: 0 0 36px #001f3f33;
        padding: 2.5em 1.5em 2em 1.5em;
        color: #fff;
        position: relative;
        overflow: visible;
        animation: fadeInUp 1.5s 1s cubic-bezier(.23,1.3,.44,1) both;
    }
    .battle-title {
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 0.5em;
        color: #ffee75;
        text-shadow: 0 0 16px #fff6, 0 0 36px #ff8;
        text-align: center;
        letter-spacing: 2px;
    }
    .battle-desc {
        font-size: 1.17em;
        color: #fff;
        margin-bottom: 1.4em;
        text-shadow: 0 0 10px #cfd9f1cc;
        text-align: center;
    }
    .ele-img-wrap {
        display: flex; justify-content: center; align-items: center; margin-bottom: 0.7em;
    }
    .ele-img {
        width: 320px; height: 210px; object-fit: cover; border-radius: 1.5em;
        box-shadow: 0 0 48px #ffe47822;
        margin: 0 10px;
        cursor: pointer;
        transition: none;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="battle-card">
        <div class="battle-title">🐘 코끼리 vs 티라노 🦖</div>
        <div class="battle-desc">
            실제 연구 결과, <b>코끼리와 티라노사우루스의 체급</b>은 거의 비슷하다.<br>
            둘 다 5~7톤급으로, <b>50:50</b> 승부.<br>
            <span style="color:#ffee75; font-weight:600; text-shadow: 0 0 14px #fffa;">
            결국 먼저 때리는 쪽이 이기는 결말!</span>
        </div>
        <div class="ele-img-wrap">
            <img src="https://images.freeimages.com/images/large-previews/f73/african-elephant-1335138.jpg"
                 id="ele-img"
                 class="ele-img"
                 title="클릭하면… 춤추는 코끼리!"/>
        </div>
    </div>
""", unsafe_allow_html=True)

# ---- JS for 코끼리 춤 ----
# 좌우반전 5번 (0.1초마다), 이후 정상 이미지로 복귀!
st.markdown("""
    <script>
    const eleImg = window.parent.document.getElementById("ele-img");
    if(eleImg){
        eleImg.onclick = async function(){
            let normal = "https://images.freeimages.com/images/large-previews/f73/african-elephant-1335138.jpg";
            let dance = "https://c.pxhere.com/images/1a/37/e8e2a84f85469d24299d6f795fae-1422613.jpg!d";
            eleImg.src = dance;
            eleImg.style.transform = "scaleX(1)";
            let flip = 1;
            for(let i=0; i<5; i++){
                await new Promise(r=>setTimeout(r,100));
                flip *= -1;
                eleImg.style.transform = "scaleX(" + flip + ")";
            }
            // 마지막에 원래대로
            await new Promise(r=>setTimeout(r,100));
            eleImg.src = normal;
            eleImg.style.transform = "scaleX(1)";
        }
    }
    </script>
""", unsafe_allow_html=True)

# ----- 제작자 표기 -----
st.markdown('<div style="text-align:center; opacity:0.7; margin-top:2em; font-size:1.2em;">by monday ✨</div>', unsafe_allow_html=True)
