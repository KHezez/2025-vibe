import streamlit as st
import streamlit.components.v1 as components

st.title("볼풀: 공끼리 충돌 (by fury X monday)")

# 무중력 버튼 토글 변수
if "nogravity" not in st.session_state:
    st.session_state.nogravity = False

if st.button("무중력 ON/OFF"):
    st.session_state.nogravity = not st.session_state.nogravity

nogravity = st.session_state.nogravity

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
    </style>
  </head>
  <body>
    <div id="canvas-container"></div>
    <div class="gravity-indicator" id="grav_ind">{'🛰️ 무중력 모드' if nogravity else '🌎 중력 ON'}</div>
    <script>
      let balls = [];
      let gravity = {0 if nogravity else 1.0};
      let dragging = false;
      let dragIndex = -1;
      let offsetX = 0, offsetY = 0;

      function setup() {{
        let c = createCanvas(window.innerWidth, window.innerHeight);
        c.parent('canvas-container');
        for(let i=0; i<10; i++) {{
          balls.push({{
            x: random(width*0.2, width*0.8), 
            y: random(height*0.1, height*0.7), 
            vx: random(-2,2), vy: random(-2,2), 
            r: 32,
            m: 1
          }});
        }}
      }}

      function draw() {{
        background(245,245,255);
        gravity = {0 if nogravity else 1.0};

        // 물리 연산 (중력, 벽)
        for(let i=0; i<balls.length; i++) {{
          let b = balls[i];

          // Apply gravity and velocity
          if (!dragging || dragIndex !== i) {{
            b.vy += gravity * 0.25;
            b.x += b.vx;
            b.y += b.vy;
          }}

          // 벽 충돌
          if(b.x < b.r) {{ b.x = b.r; b.vx *= -0.85; }}
          if(b.x > width - b.r) {{ b.x = width - b.r; b.vx *= -0.85; }}
          if(b.y < b.r) {{ b.y = b.r; b.vy *= -0.85; }}
          if(b.y > height - b.r) {{ b.y = height - b.r; b.vy *= -0.85; }}

          // 드래그 중이면 마우스 따라감
          if (dragging && dragIndex === i) {{
            b.x = mouseX + offsetX;
            b.y = mouseY + offsetY;
            b.vx = movedX * 0.25;
            b.vy = movedY * 0.25;
          }}
        }}

        // ======= 공끼리 충돌 처리 =======
        for(let i=0; i<balls.length; i++) {{
          for(let j=i+1; j<balls.length; j++) {{
            let b1 = balls[i], b2 = balls[j];
            let dx = b2.x - b1.x;
            let dy = b2.y - b1.y;
            let dist2 = dx*dx + dy*dy;
            let minDist = b1.r + b2.r;
            if (dist2 < minDist*minDist) {{
              let dist = sqrt(dist2) || 0.01;
              // 겹침 해소 (둘의 중심선을 따라 각자 절반씩)
              let overlap = 0.5 * (dist - minDist);
              b1.x += overlap * dx / dist;
              b1.y += overlap * dy / dist;
              b2.x -= overlap * dx / dist;
              b2.y -= overlap * dy / dist;

              // 1차원 탄성충돌 (속도 교환, 질량=1)
              let nx = dx / dist, ny = dy / dist;
              let tx = -ny, ty = nx;
              // 속도를 접선, 법선 분해
              let v1n = b1.vx*nx + b1.vy*ny;
              let v1t = b1.vx*tx + b1.vy*ty;
              let v2n = b2.vx*nx + b2.vy*ny;
              let v2t = b2.vx*tx + b2.vy*ty;
              // 법선속도 교환, 접선 유지
              let v1n_new = v2n, v2n_new = v1n;
              // 다시 합성
              b1.vx = v1n_new*nx + v1t*tx;
              b1.vy = v1n_new*ny + v1t*ty;
              b2.vx = v2n_new*nx + v2t*tx;
              b2.vy = v2n_new*ny + v2t*ty;
            }}
          }}
        }}
        // =============================

        // 공 그리기
        for(let i=0; i<balls.length; i++) {{
          let b = balls[i];
          fill(80, 160, 255, 220);
          stroke(40,80,140,180);
          strokeWeight(3);
          ellipse(b.x, b.y, b.r*2, b.r*2);
        }}
      }}

      function mousePressed() {{
        for(let i=balls.length-1; i>=0; i--) {{ // 위에있는 공 우선
          let b = balls[i];
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
