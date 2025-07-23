import streamlit as st
import streamlit.components.v1 as components

import time
st.title("볼풀")

if "nogravity" not in st.session_state:
    st.session_state.nogravity = False
if "balls_n" not in st.session_state:
    st.session_state.balls_n = 10
if "fight_mode" not in st.session_state:
    st.session_state.fight_mode = False

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("공 추가 (+1)"):
        st.session_state.balls_n += 1
with col2:
    if st.button("공 삭제 (-1)", disabled=(st.session_state.balls_n<=1)):
        if st.session_state.balls_n > 1:
            st.session_state.balls_n -= 1
with col3:
    if st.button("무중력 ON/OFF"):
        st.session_state.nogravity = not st.session_state.nogravity
with col4:
    if st.button("싸움 모드 ON/OFF"):
        st.session_state.fight_mode = not st.session_state.fight_mode

nogravity = st.session_state.nogravity
balls_n = st.session_state.balls_n
fight_mode = st.session_state.fight_mode

html_code = f"""
<html>
  <head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.2/p5.min.js"></script>
    <style>
      html, body {{ margin:0; padding:0; overflow:hidden; }}
      #canvas-container {{ width: 100vw; height: 100vh; }}
      .gravity-indicator {{
        position: absolute; top: 10px; left: 10px; z-index: 10;
        background: #222; color: #fff; padding: 7px 16px; border-radius: 18px; font-size: 18px; opacity: 0.7;
      }}
      .fight-indicator {{
        position: absolute; top: 50px; left: 10px; z-index: 10;
        background: #900; color: #fff; padding: 7px 16px; border-radius: 18px; font-size: 18px; opacity: 0.7;
        display: {'block' if fight_mode else 'none'};
      }}
    </style>
  </head>
  <body>
    <div id="canvas-container"></div>
    <div class="gravity-indicator" id="grav_ind">{'🛰️ 무중력 모드' if nogravity else '🌎 중력 ON'}</div>
    <div class="fight-indicator" id="fight_ind">⚔️ 싸움 모드</div>
    <script>
      let balls = [];
      let gravity = {0 if nogravity else 1.0};
      let dragging = false;
      let dragIndex = -1;
      let offsetX = 0, offsetY = 0;

      // 무적 쿨타임(ms)
      const INVULN_TIME = 500;

      function randomColor() {{
        let r = Math.floor(120+Math.random()*135);
        let g = Math.floor(120+Math.random()*135);
        let b = Math.floor(120+Math.random()*135);
        return [r,g,b,220];
      }}

      function addBall() {{
        let [r,g,b,a] = randomColor();
        balls.push({{
            x: random(width*0.2, width*0.8), 
            y: random(height*0.1, height*0.7), 
            vx: random(-2,2), vy: random(-2,2), 
            r: 32,
            m: 1,
            color: [r,g,b,a],
            angle: random(0, TWO_PI),
            av: random(-0.05,0.05),
            hp: 10,
            alive: true,
            last_hit: -10000,   // 마지막 데미지 프레임(ms)
        }});
      }}

      function setup() {{
        let c = createCanvas(window.innerWidth, window.innerHeight);
        c.parent('canvas-container');
        for(let i=0; i<{balls_n}; i++) {{
          addBall();
        }}
      }}

      function draw() {{
        background(245,245,255);
        gravity = {0 if nogravity else 1.0};
        let now = millis();

        // 공 갯수 동기화
        while (balls.length < {balls_n}) addBall();
        while (balls.length > {balls_n}) balls.pop();

        // 물리
        for(let i=0; i<balls.length; i++) {{
          let b = balls[i];
          if (!b.alive) continue;
          if (!dragging || dragIndex !== i) {{
            b.vy += gravity * 0.25;
            b.x += b.vx;
            b.y += b.vy;
            b.angle += b.av;
            if (b.angle > TWO_PI) b.angle -= TWO_PI;
            if (b.angle < 0) b.angle += TWO_PI;
            b.av *= 0.995;
          }}
          let hitWall = false;
          if(b.x < b.r) {{ b.x = b.r; b.vx *= -0.85; hitWall = true; }}
          if(b.x > width - b.r) {{ b.x = width - b.r; b.vx *= -0.85; hitWall = true; }}
          if(b.y < b.r) {{ b.y = b.r; b.vy *= -0.85; hitWall = true; }}
          if(b.y > height - b.r) {{ b.y = height - b.r; b.vy *= -0.85; hitWall = true; }}
          if(hitWall && {str(fight_mode).lower()}) {{
            b.av += random(-0.15,0.15);
          }}
          if (dragging && dragIndex === i) {{
            b.x = mouseX + offsetX;
            b.y = mouseY + offsetY;
            b.vx = movedX * 0.25;
            b.vy = movedY * 0.25;
            b.av = 0;
          }}
        }}

        // ==== 싸움모드 충돌 처리 ====
        for(let i=0; i<balls.length; i++) {{
          let b1 = balls[i];
          if (!b1.alive) continue;
          for(let j=i+1; j<balls.length; j++) {{
            let b2 = balls[j];
            if (!b2.alive) continue;
            let dx = b2.x - b1.x;
            let dy = b2.y - b1.y;
            let dist2 = dx*dx + dy*dy;
            let minDist = b1.r + b2.r;
            if (dist2 < minDist*minDist) {{
              let dist = sqrt(dist2) || 0.01;
              let overlap = 0.5 * (dist - minDist);
              b1.x += overlap * dx / dist;
              b1.y += overlap * dy / dist;
              b2.x -= overlap * dx / dist;
              b2.y -= overlap * dy / dist;

              // 탄성 충돌
              let nx = dx / dist, ny = dy / dist;
              let tx = -ny, ty = nx;
              let v1n = b1.vx*nx + b1.vy*ny;
              let v1t = b1.vx*tx + b1.vy*ty;
              let v2n = b2.vx*nx + b2.vy*ny;
              let v2t = b2.vx*tx + b2.vy*ty;
              let v1n_new = v2n, v2n_new = v1n;
              b1.vx = v1n_new*nx + v1t*tx;
              b1.vy = v1n_new*ny + v1t*ty;
              b2.vx = v2n_new*nx + v2t*tx;
              b2.vy = v2n_new*ny + v2t*ty;

              b1.av += random(-0.08,0.08);
              b2.av += random(-0.08,0.08);

              if ({str(fight_mode).lower()}) {{
                // === 판정 ===
                // 약점: 0~0.8*2PI  | 강점: 0.8*2PI~2PI
                // 강점이 상대 약점 때렸을 때만 데미지, 무적시X
                let angle12 = atan2(b2.y-b1.y, b2.x-b1.x) - b1.angle;
                if(angle12 < 0) angle12 += TWO_PI;
                if(angle12 > TWO_PI) angle12 -= TWO_PI;

                let angle21 = atan2(b1.y-b2.y, b1.x-b2.x) - b2.angle;
                if(angle21 < 0) angle21 += TWO_PI;
                if(angle21 > TWO_PI) angle21 -= TWO_PI;

                // b1 강점(빨강): 0.8*2PI~2PI
                let atk1 = (angle12 > 0.8*2*PI && angle12 <= 2*PI);
                // b2 약점(파랑): 0~0.8*2PI
                let weak2 = (angle21 >= 0 && angle21 < 0.8*2*PI);

                // b2 강점(빨강): 0.8*2PI~2PI
                let atk2 = (angle21 > 0.8*2*PI && angle21 <= 2*PI);
                // b1 약점(파랑): 0~0.8*2PI
                let weak1 = (angle12 >= 0 && angle12 < 0.8*2*PI);

                // b1이 b2 약점 때림 (b1 강점 ↔ b2 약점)
                if (atk1 && weak2) {{
                  if (now - b2.last_hit > {int(0.5*1000)}) {{
                    b2.hp -= 1;
                    b2.last_hit = now;
                    b2.av += random(-0.25,0.25);
                  }}
                }}
                // b2가 b1 약점 때림
                if (atk2 && weak1) {{
                  if (now - b1.last_hit > {int(0.5*1000)}) {{
                    b1.hp -= 1;
                    b1.last_hit = now;
                    b1.av += random(-0.25,0.25);
                  }}
                }}
              }}
            }}
          }}
        }}

        // HP 0이하 공 제거
        for(let i=0; i<balls.length; i++) {{
          let b = balls[i];
          if (!b.alive) continue;
          if (b.hp <= 0) b.alive = false;
        }}

        // ======= 그리기 =======
        for(let i=0; i<balls.length; i++) {{
          let b = balls[i];
          if (!b.alive) continue;
          let now = millis();
          push();
          translate(b.x, b.y);
          rotate(b.angle);

          // 무적일 때 불투명도 ↓
          let invuln = (now - b.last_hit < {int(0.5*1000)});
          let alpha = invuln ? 120 : 220;

          // 본체
          fill(b.color[0], b.color[1], b.color[2], alpha);
          stroke(40,80,140,180*alpha/220);
          strokeWeight(3);
          ellipse(0, 0, b.r*2, b.r*2);

          // 약점(파란색) 0~0.8*2PI
          if ({str(fight_mode).lower()}) {{
            noStroke();
            fill(40,80,255,alpha);
            arc(0,0,b.r*2,b.r*2,0,0.8*2*PI,PIE);
            // 강점(빨간색) 0.8*2PI~2PI
            fill(255,80,80,alpha);
            arc(0,0,b.r*2,b.r*2,0.8*2*PI,2*PI,PIE);
          }}

          // 중앙 HP
          fill(32,32,32,240);
          noStroke();
          textAlign(CENTER, CENTER);
          textSize(b.r*0.85);
          text(b.hp, 0, 4);
          pop();
        }}
      }}

      function mousePressed() {{
        for(let i=balls.length-1; i>=0; i--) {{
          let b = balls[i];
          if (!b.alive) continue;
          let d = dist(mouseX, mouseY, b.x, b.y);
          if (d < b.r) {{
            dragging = true;
            dragIndex = i;
            offsetX = b.x - mouseX;
            offsetY = b.y - mouseY;
            break;
          }}
        }}
      }}

      function mouseReleased() {{
        dragging = false;
        dragIndex = -1;
      }}

      function touchStarted() {{ mousePressed(); }}
      function touchEnded() {{ mouseReleased(); }}

      function windowResized() {{
        resizeCanvas(window.innerWidth, window.innerHeight);
      }}
    </script>
  </body>
</html>
"""

components.html(html_code, height=700, scrolling=False)
