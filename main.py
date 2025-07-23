import streamlit as st

# --- 스타일 ------------------------------------------------------------
st.markdown(
    """
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
        from {opacity:0;transform:translateY(80px) scale(0.97);} 
        to {opacity:1;transform:none;}
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
    /* 싸움존 스타일 */
    #fight-zone {
        width: 600px;
        height: 300px;
        border: 3px solid #fff;
        border-radius: 1em;
        margin: 0 auto;
        position: relative;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# 1) 싸움존 캔버스 + 물리 시뮬 -------------------------------------------
# ----------------------------------------------------------------------

# 싸움존 라벨
st.markdown("""
<div style='text-align:center; margin-top:2em;'>
  <div style='font-size:2em; font-weight:bold; color:#fff; text-shadow:0 0 12px #00fff9;'>
    코끼리 vs 티라노 싸움존
  </div>
</div>
""", unsafe_allow_html=True)

# 캔버스 삽입 (fight-zone 내부)
st.markdown("""
<div id='fight-zone'>
  <canvas id='fight-canvas'></canvas>
</div>
<script>
// fight-zone 사이즈 동기화
function resizeFight() {
  const zone = document.getElementById('fight-zone');
  const canvas = document.getElementById('fight-canvas');
  canvas.width = zone.clientWidth;
  canvas.height = zone.clientHeight;
}
window.addEventListener('resize', resizeFight);
resizeFight();

const canvas = document.getElementById('fight-canvas');
const ctx = canvas.getContext('2d');

// 공 데이터 (사이즈 축소)
const balls = [
  {name:'티라노', img:'https://static.turbosquid.com/Preview/001304/868/KG/Z.jpg', x:150,y:100,r:40, vx:0,vy:0, mass:8, col:'#00ffc2', drag:false},
  {name:'코끼리', img:'https://images.freeimages.com/images/large-previews/f73/african-elephant-1335138.jpg', x:450,y:150,r:48, vx:0,vy:0, mass:7.5, col:'#e1e100', drag:false}
];
balls.forEach(b=>{const im=new Image(); im.src=b.img; b.im=im});

const G=0.25, FRI=0.988, BOUNCE=0.85; let quake=0;
let dragIdx=null, startPos=null;

canvas.addEventListener('pointerdown',e=>{
  const rect=canvas.getBoundingClientRect(); let mx=e.clientX-rect.left, my=e.clientY-rect.top;
  for(let i=balls.length-1;i>=0;i--){const b=balls[i]; if(Math.hypot(mx-b.x,my-b.y)<b.r){
    dragIdx=i; b.drag=true; startPos={x:mx,y:my,t:performance.now()}; break; }}
});
canvas.addEventListener('pointermove',e=>{ if(dragIdx!==null){const rect=canvas.getBoundingClientRect();
  balls[dragIdx].x=e.clientX-rect.left; balls[dragIdx].y=e.clientY-rect.top; }});
canvas.addEventListener('pointerup',e=>{ if(dragIdx!==null){const b=balls[dragIdx]; const rect=canvas.getBoundingClientRect();
  const mx=e.clientX-rect.left, my=e.clientY-rect.top; const dt=(performance.now()-startPos.t)/1000+0.001;
  b.vx=(mx-startPos.x)/dt*0.06; b.vy=(my-startPos.y)/dt*0.06; b.drag=false; dragIdx=null; }});

function boom(){ quake=30; }
function step(){
  balls.forEach(b=>{ if(!b.drag){ b.vy+=G; b.x+=b.vx; b.y+=b.vy; b.vx*=FRI; b.vy*=FRI;
    if(b.x-b.r<0){b.x=b.r; b.vx*=-BOUNCE;} if(b.x+b.r>canvas.width){b.x=canvas.width-b.r; b.vx*=-BOUNCE;}
    if(b.y-b.r<0){b.y=b.r; b.vy*=-BOUNCE;} if(b.y+b.r>canvas.height){b.y=canvas.height-b.r; b.vy*=-BOUNCE;}
  }});
  for(let i=0;i<balls.length;i++){ for(let j=i+1;j<balls.length;j++){const a=balls[i], b=balls[j];
    const dx=b.x-a.x, dy=b.y-a.y, dist=Math.hypot(dx,dy);
    if(dist<a.r+b.r){ const overlap=a.r+b.r-dist; const nx=dx/dist, ny=dy/dist; const tot=a.mass+b.mass;
      a.x-=nx*overlap*(b.mass/tot); a.y-=ny*overlap*(b.mass/tot);
      b.x+=nx*overlap*(a.mass/tot); b.y+=ny*overlap*(a.mass/tot);
      const p=2*(a.vx*nx+a.vy*ny-b.vx*nx-b.vy*ny)/tot;
      a.vx-=(p*b.mass*nx); a.vy-=(p*b.mass*ny);
      b.vx+=(p*a.mass*nx); b.vy+=(p*a.mass*ny);
      a.vx*=BOUNCE; a.vy*=BOUNCE; b.vx*=BOUNCE; b.vy*=BOUNCE; boom(); }
  }}
}
function draw(){ ctx.clearRect(0,0,canvas.width,canvas.height);
  balls.forEach(b=>{ ctx.save(); ctx.beginPath(); ctx.arc(b.x,b.y,b.r,0,2*Math.PI); ctx.closePath();
    ctx.shadowColor=b.col; ctx.shadowBlur=36; ctx.clip(); ctx.drawImage(b.im,b.x-b.r,b.y-b.r,b.r*2,b.r*2);
    ctx.restore(); ctx.beginPath(); ctx.arc(b.x,b.y,b.r,0,2*Math.PI); ctx.strokeStyle="#fff";
    ctx.lineWidth=3; ctx.globalAlpha=0.8; ctx.stroke(); ctx.globalAlpha=1; ctx.font="bold 1.1em sans-serif";
    ctx.textAlign="center"; ctx.fillStyle="#fff"; ctx.fillText(b.name,b.x,b.y+b.r+22);
  }); }
function loop(){ step(); draw(); if(quake>0){ const s=Math.sin(Date.now()*0.12)*quake*1.2; canvas.style.transform=`translate(${s}px,${-s/2}px)`; quake--; } else canvas.style.transform=""; requestAnimationFrame(loop);} loop();
</script>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# 2) 아래쪽: 공룡 사전 & 설명 카드 (변경 없음)
# ----------------------------------------------------------------------

dino_data = [
    {"name":"티라노사우르스","img":"https://static.turbosquid.com/Preview/001304/868/KG/Z.jpg","desc":"티라노사우루스(Tyrannosaurus)는 백악기 후기에 북아메리카에서 살았던 육식공룡의 왕. 길이 약 12m, 키 4m, 무게 6~9톤. 압도적인 턱 힘과 사냥 실력으로 악명이 높았다."},
    {"name":"알로사우르스","img":"https://tse1.mm.bing.net/th/id/OIP.jNBXbE7eq0QdKu0uGOrr-AHaEr?rs=1&pid=ImgDetMain&o=7&rm=3","desc":"알로사우루스(Allosaurus)는 쥐라기 후기의 포식자로, 약 8.5m 길이에 재빠른 움직임이 특징. 당시 '톱 포식자' 중 하나로 평가받았다."},
    {"name":"파키케팔로사우르스","img":"https://tse1.mm.bing.net/th/id/OIP.6A_YOwXpMtd2fHy-QrI20QHaE7?rs=1&pid=ImgDetMain&o=7&rm=3","desc":"파키케팔로사우루스(Pachycephalosaurus)는 두개골이 25cm 두께로 매우 단단해, 머리로 박치기 싸움을 벌였던 초식공룡. 백악기 후기 북미에서 발견됨."},
    {"name":"안킬로사우르스","img":"https://png.pngtree.com/thumb_back/fw800/background/20230612/pngtree-3d-animation-of-an-extinct-dinosaur-image_2920885.jpg","desc":"안킬로사우르스(Ankylosaurus)는 전신이 갑옷처럼 덮여 있고, 꼬리에는 곤봉이 달린 방어의 대명사. 천적도 함부로 건드리지 못했던 강인한 초식공룡."},
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

# --- 코끼리 vs 티라노 설명/이미지 카드 ---
