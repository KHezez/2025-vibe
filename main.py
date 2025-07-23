import streamlit as st

# --- 스타일 ---
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
    .dino-img, .elephant-img {
        width: 260px;
        height: 160px;
        object-fit: cover;
        border-radius: 1em;
        box-shadow: 0 0 32px #7ef9ff22;
        margin-right: 2em;
        transition: transform 0.35s cubic-bezier(.33,2,.22,.8), box-shadow 0.3s;
        cursor: pointer;
    }
    .dino-img:hover, .elephant-img:hover {
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
    /* vs 카드 */
    .vs-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        background: rgba(32,32,32,0.97);
        border-radius: 1.5em;
        box-shadow: 0 4px 32px #000a;
        padding: 2.3em 1.3em 2em 1.3em;
        margin-bottom: 2em;
        opacity: 0;
        animation: fadeInUp 1.2s ease-out 1.3s forwards;
    }
    .vs-title {
        font-size: 2.1em;
        font-weight: bold;
        color: #fff;
        margin-bottom: 0.6em;
        text-shadow: 0 0 18px #00fff988, 0 0 60px #fff5;
        letter-spacing: 1.5px;
        text-align: center;
    }
    .vs-desc {
        font-size: 1.1em;
        color: #fff;
        margin-bottom: 1.7em;
        text-shadow: 0 0 7px #00fff944;
        text-align: center;
        line-height: 1.7em;
    }
    /* 오버레이 캔버스 위치 고정 (전체 화면 덮음) */
    #gravity-overlay {
        position: fixed;
        top: 0; left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none; /* 기본값: 클릭 막음 */
        z-index: 9001;
    }
    #gravity-overlay.active {
        pointer-events: auto; /* 캔버스 위에서만 마우스 허용 */
    }
    </style>
""", unsafe_allow_html=True)

# --- 캔버스 오버레이 (사이트 전체 덮는 방식) ---
st.components.v1.html("""
<canvas id='gravity-overlay' width='1280' height='720'></canvas>
<script>

function resizeOverlay() {
    const canvas = document.getElementById('gravity-overlay');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

window.addEventListener('resize', resizeOverlay);
resizeOverlay();

const canvas = document.getElementById('gravity-overlay');
const ctx = canvas.getContext('2d');
canvas.classList.add('active'); // 마우스 이벤트 허용

// 공 정보
document.balls = [
  {
    name: '티라노',
    img: 'https://static.turbosquid.com/Preview/001304/868/KG/Z.jpg',
    x: 280, y: 260, r: 72,
    vx: 0, vy: 0,
    dragging: false, dragStart: null, dragLast: null,
    mass: 8.0,
    color: '#00ffc2'
  },
  {
    name: '코끼리',
    img: 'https://images.freeimages.com/images/large-previews/f73/african-elephant-1335138.jpg',
    x: 700, y: 320, r: 84,
    vx: 0, vy: 0,
    dragging: false, dragStart: null, dragLast: null,
    mass: 7.5,
    color: '#e1e100'
  }
];

for (const b of document.balls) {
  const image = new window.Image();
  image.src = b.img;
  b._img = image;
}

const g = 0.25;
const friction = 0.988;
const bounce = 0.85;
let earthquakeTimer = 0;

// --- 마우스 드래그 & 속도 적용 ---
let dragIdx = null;
let lastMouse = null;
canvas.addEventListener('mousedown', function(e) {
  const mx = e.clientX, my = e.clientY;
  for (let i=document.balls.length-1; i>=0; i--) {
    const b = document.balls[i];
    const dist = Math.hypot(mx-b.x, my-b.y);
    if (dist < b.r) {
      dragIdx = i;
      b.dragging = true;
      b.dragStart = {x: mx, y: my, time: Date.now()};
      b.dragLast = {x: mx, y: my, time: Date.now()};
      b.vx = 0; b.vy = 0;
      lastMouse = {x: mx, y: my};
      break;
    }
  }
});
canvas.addEventListener('mousemove', function(e) {
  if (dragIdx !== null) {
    const mx = e.clientX, my = e.clientY;
    const b = document.balls[dragIdx];
    b.x = mx;
    b.y = my;
    if (b.dragLast) b.dragLast = {x: mx, y: my, time: Date.now()};
    lastMouse = {x: mx, y: my};
  }
});
canvas.addEventListener('mouseup', function(e) {
  if (dragIdx !== null) {
    const b = document.balls[dragIdx];
    // 마우스 속도(가속도) 반영
    if (b.dragStart && b.dragLast && b.dragLast.time > b.dragStart.time) {
      const dx = b.dragLast.x - b.dragStart.x;
      const dy = b.dragLast.y - b.dragStart.y;
      const dt = (b.dragLast.time - b.dragStart.time) / 1000.0 + 0.001;
      b.vx = dx / dt * 0.06; // tuning 필요
      b.vy = dy / dt * 0.06;
    }
    b.dragging = false;
    dragIdx = null;
    b.dragStart = null;
    b.dragLast = null;
  }
});
canvas.addEventListener('mouseleave', function(e) {
  if (dragIdx !== null) {
    const b = document.balls[dragIdx];
    b.dragging = false;
    dragIdx = null;
    b.dragStart = null;
    b.dragLast = null;
  }
});

// --- 충돌 시 지진효과 ---
function triggerEarthquake() {
  if (earthquakeTimer <= 0) {
    earthquakeTimer = 30; // 0.5초 (60fps 기준)
  }
}

function update() {
  for (const b of document.balls) {
    if (!b.dragging) {
      b.vy += g;
      b.x += b.vx;
      b.y += b.vy;
      b.vx *= friction;
      b.vy *= friction;
      // 벽/바닥/천장 반사
      if (b.x-b.r < 0) { b.x = b.r; b.vx *= -bounce; }
      if (b.x+b.r > canvas.width) { b.x = canvas.width-b.r; b.vx *= -bounce; }
      if (b.y-b.r < 0) { b.y = b.r; b.vy *= -bounce; }
      if (b.y+b.r > canvas.height) { b.y = canvas.height-b.r; b.vy *= -bounce; }
    }
  }
  // 충돌 체크
  for (let i=0; i<document.balls.length; i++) {
    for (let j=i+1; j<document.balls.length; j++) {
      const a = document.balls[i], b = document.balls[j];
      const dx = b.x - a.x, dy = b.y - a.y;
      const dist = Math.hypot(dx,dy);
      if (dist < a.r + b.r) {
        // 오버랩 해소
        const angle = Math.atan2(dy, dx);
        const overlap = (a.r + b.r - dist) * 0.55;
        const totalMass = a.mass + b.mass;
        a.x -= Math.cos(angle) * overlap * (b.mass/totalMass);
        a.y -= Math.sin(angle) * overlap * (b.mass/totalMass);
        b.x += Math.cos(angle) * overlap * (a.mass/totalMass);
        b.y += Math.sin(angle) * overlap * (a.mass/totalMass);
        // 반사 속도(탄성 충돌)
        const nx = dx/dist, ny = dy/dist;
        const tx = -ny, ty = nx;
        // 속도 분해
        const va_n = a.vx*nx + a.vy*ny;
        const vb_n = b.vx*nx + b.vy*ny;
        const va_t = a.vx*tx + a.vy*ty;
        const vb_t = b.vx*tx + b.vy*ty;
        // new normal velocity (탄성 충돌 공식)
        const va_n_new = (va_n * (a.mass-b.mass) + 2*b.mass*vb_n)/(a.mass+b.mass);
        const vb_n_new = (vb_n * (b.mass-a.mass) + 2*a.mass*va_n)/(a.mass+b.mass);
        // 다시 합성
        a.vx = va_n_new*nx + va_t*tx;
        a.vy = va_n_new*ny + va_t*ty;
        b.vx = vb_n_new*nx + vb_t*tx;
        b.vy = vb_n_new*ny + vb_t*ty;
        // 튕김 튜닝
        a.vx *= bounce; a.vy *= bounce;
        b.vx *= bounce; b.vy *= bounce;
        triggerEarthquake();
      }
    }
  }
}

function drawBall(b) {
  ctx.save();
  ctx.beginPath();
  ctx.arc(b.x, b.y, b.r, 0, 2*Math.PI, false);
  ctx.closePath();
  // glow
  ctx.shadowColor = b.color;
  ctx.shadowBlur = 38;
  ctx.clip();
  ctx.drawImage(b._img, b.x-b.r, b.y-b.r, b.r*2, b.r*2);
  ctx.shadowBlur = 0;
  ctx.restore();
  // 테두리
  ctx.beginPath();
  ctx.arc(b.x, b.y, b.r, 0, 2*Math.PI, false);
  ctx.strokeStyle = "#fff";
  ctx.lineWidth = 3;
  ctx.globalAlpha = 0.8;
  ctx.stroke();
  ctx.globalAlpha = 1.0;
  // 이름
  ctx.font = "bold 1.15em sans-serif";
  ctx.textAlign = "center";
  ctx.shadowColor = "#222";
  ctx.shadowBlur = 20;
  ctx.fillStyle = "#fff";
  ctx.fillText(b.name, b.x, b.y+b.r+25);
  ctx.shadowBlur = 0;
}

function animate() {
  if (!canvas) return;
  // 화면 흔들림(지진효과)
  if (earthquakeTimer > 0) {
    const shake = Math.sin(Date.now()*0.12)*earthquakeTimer*1.2;
    canvas.style.transform = `translate(${shake}px, ${-shake/2}px)`;
    earthquakeTimer--;
  } else {
    canvas.style.transform = "";
  }
  ctx.clearRect(0,0,canvas.width,canvas.height);
  update();
  for (const b of document.balls) drawBall(b);
  requestAnimationFrame(animate);
}
animate();
</script>
""", height=800)

# --- 본문 카드/설명은 그대로 ---
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

# ... (위까지는 네가 보낸 코드와 동일)

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

# --- 코끼리 vs 티라노 설명/이미지 카드 ---
st.markdown(f"""
    <div class="vs-card">
        <div class="vs-title">🐘 코끼리 vs 티라노사우르스 🦖</div>
        <div class="vs-desc">
        코끼리(아프리카코끼리)는 오늘날 지상 최대의 육상동물로, <b>키 약 3.2~4m</b>, <b>무게 6~7톤</b>에 달하며, 힘과 방어력 모두 티라노에 필적한다.<br><br>
        <b>티라노사우르스</b>도 유사한 크기(길이 12m, 키 4m, 6~9톤)와 사나운 공격력을 가졌다. <br><br>
        실제 고생물학 연구에 따르면, 둘이 싸운다면 "누가 먼저 강하게 가격하느냐"가 승패를 좌우한다는 것이 정설.<br>
        <span style="color:#fff; text-shadow:0 0 8px #0ff, 0 0 18px #fff;">
        <b>즉, 체급·힘이 비슷해 일방적으로 누가 이긴다고 보기 어렵고, 진짜 50:50. 먼저 가격하는 쪽이 이긴다!</b>
        </span>
        <br><br>
        코끼리의 방어력과 체중, 그리고 엄청난 돌진력은 티라노의 이빨/턱 힘과 정면 대결에서 맞먹는다.<br>
        그래서 실제 동물학자·공룡학자들도 <b>"티라노와 코끼리, 절대 압승 불가! 먼저 맞는 쪽이 진다"</b>고 평가한다.
        </div>
        <img src="https://images.freeimages.com/images/large-previews/f73/african-elephant-1335138.jpg" class="elephant-img" alt="코끼리"/>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div style="text-align:center; opacity:0.7; margin-top:2em; font-size:1.2em;">by monday ✨</div>', unsafe_allow_html=True)
