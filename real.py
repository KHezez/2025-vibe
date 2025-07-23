import streamlit as st
import streamlit.components.v1 as components

gravity = st.slider("중력 세기", 0.1, 3.0, 1.0, 0.1)

html_code = f"""
<html>
  <head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.2/p5.min.js"></script>
    <style>
      html, body {{ margin:0; padding:0; overflow:hidden; }}
      #canvas-container {{ width: 100vw; height: 100vh; }}
    </style>
  </head>
  <body>
    <div id="canvas-container"></div>
    <script>
      let balls = [];
      let gravity = {gravity};

      function setup() {{
        createCanvas(window.innerWidth, window.innerHeight).parent('canvas-container');
        for(let i=0; i<10; i++) {{
          balls.push({{x: random(width), y: random(height/2), vx: random(-2,2), vy: random(-2,2), r: 20}});
        }}
      }}

      function draw() {{
        background(255);
        for(let b of balls) {{
          b.vy += gravity * 0.1;
          b.x += b.vx;
          b.y += b.vy;

          // 벽 충돌
          if(b.x < b.r) {{ b.x = b.r; b.vx *= -0.9; }}
          if(b.x > width - b.r) {{ b.x = width - b.r; b.vx *= -0.9; }}
          if(b.y < b.r) {{ b.y = b.r; b.vy *= -0.9; }}
          if(b.y > height - b.r) {{ b.y = height - b.r; b.vy *= -0.9; }}

          ellipse(b.x, b.y, b.r*2, b.r*2);
        }}
      }}

      function mousePressed() {{
        // 드래그 기능(간단 버전)
        // (여기에 클릭한 공만 따로 드래그 처리 추가)
      }}
    </script>
  </body>
</html>
"""

components.html(html_code, height=600, width=1000)
