import streamlit as st
import streamlit.components.v1 as components

st.title("볼풀: 보스 강점 판정 FIX! (by fury X monday)")

if "nogravity" not in st.session_state:
    st.session_state.nogravity = False
if "balls_n" not in st.session_state:
    st.session_state.balls_n = 10
if "fight_mode" not in st.session_state:
    st.session_state.fight_mode = False
if "boss" not in st.session_state:
    st.session_state.boss = False

col1, col2, col3, col4, col5 = st.columns(5)
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
with col5:
    boss_btn = st.empty()
    if not st.session_state.boss:
        if boss_btn.button("보스 추가"):
            st.session_state.boss = True
    else:
        if boss_btn.button("보스 삭제"):
            st.session_state.boss = False

nogravity = st.session_state.nogravity
balls_n = st.session_state.balls_n
fight_mode = st.session_state.fight_mode
boss = st.session_state.boss

EXPLOSION_IMG = "https://png.pngtree.com/png-clipart/20190705/original/pngtree-fire-explosion-blast-flame-png-transparent-png-image_4199261.jpg"
EXPLOSION_SOUND = "https://files.catbox.moe/wwyaov.mp3"
HIT_SOUND = "https://files.catbox.moe/pqw80a.mp3"

html_code = f"""
<html>
  <head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.2/p5.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.2/addons/p5.sound.min.js"></script>
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
      .boss-indicator {{
        position: absolute; top: 90px; left: 10px; z-index: 10;
        background: #fb0; color: #000; padding: 7px 16px; border-radius: 18px; font-size: 18px; opacity: 0.7;
        display: {'block' if boss else 'none'};
      }}
    </style>
  </head>
  <body>
    <div id="canvas-container"></div>
    <div class="gravity-indicator" id="grav_ind">{'🛰️ 무중력 모드' if nogravity else '🌎 중력 ON'}</div>
    <div class="fight-indicator" id="fight_ind">⚔️ 싸움 모드</div>
    <div class="boss-indicator" id="boss_ind">👹 보스 등장!</div>
    <script>
      let balls = [];
      let gravity = {0 if nogravity else 1.0};
      let dragging = false;
      let dragIndex = -1;
      let offsetX = 0, offsetY = 0;
      const INVULN_TIME = 500;
      let explosions = [];
      let explosionImg, explosionSound, hitSound;
      let explosionLoaded = false, soundLoaded = false, hitLoaded = false;
      let bossIdx = -1;
      let boss_stun = false;
      let boss_stun_start = -10000;
      const BOSS_STUN_TIME = 5000;

      function preload() {{
        explosionImg = loadImage("{EXPLOSION_IMG}", ()=>{{ explosionLoaded=true; }});
        explosionSound = loadSound("{EXPLOSION_SOUND}", ()=>{{ soundLoaded=true; }});
        hitSound = loadSound("{HIT_SOUND}", ()=>{{ hitLoaded=true; }});
      }}

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
            last_hit: -10000,
            isBoss: false,
            stun: false,
            stunStart: -10000
        }});
      }}

      function addBoss() {{
        balls.push({{
            x: width*0.5, 
            y: height*0.4, 
            vx: random(-1.1,1.1), vy: random(-1.1,1.1), 
            r: 54,
            m: 8,
            color: [220,100,60,230],
            angle: random(0, TWO_PI),
            av: random(-0.02,0.02),
            hp: 20,
            alive: true,
            last_hit: -10000,
            isBoss: true,
            stun: false,
            stunStart: -10000
        }});
        bossIdx = balls.length-1;
        boss_stun = false;
      }}

      function setup() {{
        let c = createCanvas(window.innerWidth, window.innerHeight);
        c.parent('canvas-container');
        for(let i=0; i<{balls_n}; i++) {{
          addBall();
        }}
        if ({str(boss).lower()}) {{
            addBoss();
        }}
        explosions = [];
        userStartAudio();
      }}

      function draw() {{
        background(245,245,255);
        gravity = {0 if nogravity else 1.0};
        let now = millis();

        // 공 동기화
        while (balls.length < {balls_n} + ({'1' if boss else '0'}) ) {{
            if ({str(boss).lower()} && !balls.some(b=>b.isBoss)) {{
                addBoss();
            }} else {{
                addBall();
            }}
        }}
        // 보스 삭제
        if (!{str(boss).lower()}) {{
            for(let i=balls.length-1; i>=0; i--) {{
                if(balls[i].isBoss) balls.splice(i,1);
            }}
            bossIdx = -1;
            boss_stun = false;
        }}

        while (balls.length > {balls_n} + ({'1' if boss else '0'})) balls.pop();

        // 물리
        for(let i=0; i<balls.length; i++) {{
          let b = balls[i];
          if (!b.alive) continue;
          if (b.isBoss) {{
              if(b.stun && now - b.stunStart > BOSS_STUN_TIME) {{
                  b.stun = false;
                  boss_stun = false;
              }}
          }}
          let m_fac = (b.isBoss?0.3:1.0);
          if (!dragging || dragIndex !== i) {{
            b.vy += gravity * 0.25 * m_fac;
            b.x += b.vx;
            b.y += b.vy;
            b.angle += b.av;
            if (b.angle > TWO_PI) b.angle -= TWO_PI;
            if (b.angle < 0) b.angle += TWO_PI;
            b.av *= 0.995;
          }}
          let hitWall = false;
          if(b.x < b.r) {{ b.x = b.r; b.vx *= -0.70; hitWall = true; }}
          if(b.x > width - b.r) {{ b.x = width - b.r; b.vx *= -0.70; hitWall = true; }}
          if(b.y < b.r) {{ b.y = b.r; b.vy *= -0.70; hitWall = true; }}
          if(b.y > height - b.r) {{ b.y = height - b.r; b.vy *= -0.70; hitWall = true; }}
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

        // ==== 충돌 ====
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
              let m1 = b1.isBoss ? 8 : 1;
              let m2 = b2.isBoss ? 8 : 1;
              b1.x += overlap * dx / dist * (m2/(m1+m2));
              b1.y += overlap * dy / dist * (m2/(m1+m2));
              b2.x -= overlap * dx / dist * (m1/(m1+m2));
              b2.y -= overlap * dy / dist * (m1/(m1+m2));

              // 탄성 충돌
              let nx = dx / dist, ny = dy / dist;
              let tx = -ny, ty = nx;
              let v1n = b1.vx*nx + b1.vy*ny;
              let v1t = b1.vx*tx + b1.vy*ty;
              let v2n = b2.vx*nx + b2.vy*ny;
              let v2t = b2.vx*tx + b2.vy*ty;
              let v1n_new = (v2n * m2 + v1n * (m1-m2)) / (m1+m2);
              let v2n_new = (v1n * m1 + v2n * (m2-m1)) / (m1+m2);
              b1.vx = v1n_new*nx + v1t*tx;
              b1.vy = v1n_new*ny + v1t*ty;
              b2.vx = v2n_new*nx + v2t*tx;
              b2.vy = v2n_new*ny + v2t*ty;

              b1.av += random(-0.08,0.08);
              b2.av += random(-0.08,0.08);

              if ({str(fight_mode).lower()}) {{
                let now = millis();
                // angle 기준점(충돌각, 각각의 공 기준)
                let angle12 = atan2(b2.y-b1.y, b2.x-b1.x) - b1.angle;
                if(angle12 < 0) angle12 += TWO_PI;
                if(angle12 > TWO_PI) angle12 -= TWO_PI;
                let angle21 = atan2(b1.y-b2.y, b1.x-b2.x) - b2.angle;
                if(angle21 < 0) angle21 += TWO_PI;
                if(angle21 > TWO_PI) angle21 -= TWO_PI;

                // === (1) 일반공 vs 일반공 ===
                if (!b1.isBoss && !b2.isBoss) {{
                    let atk1 = (angle12 > 0.8*2*PI && angle12 <= 2*PI);
                    let weak2 = (angle21 >= 0 && angle21 < 0.8*2*PI && !b2.stun);
                    let atk2 = (angle21 > 0.8*2*PI && angle21 <= 2*PI);
                    let weak1 = (angle12 >= 0 && angle12 < 0.8*2*PI && !b1.stun);

                    // 강점→약점 (일반공)
                    if (atk1 && weak2) {{
                        if (now - b2.last_hit > {int(0.5*1000)}) {{
                            b2.hp -= 1;
                            b2.last_hit = now;
                            b2.av += random(-0.25,0.25);
                            if (hitLoaded) hitSound.play();
                        }}
                    }}
                    if (atk2 && weak1) {{
                        if (now - b1.last_hit > {int(0.5*1000)}) {{
                            b1.hp -= 1;
                            b1.last_hit = now;
                            b1.av += random(-0.25,0.25);
                            if (hitLoaded) hitSound.play();
                        }}
                    }}
                    // 강점끼리 폭발
                    if (atk1 && atk2) {{
                        if (explosionLoaded) {{
                            explosions.push({{
                              x: (b1.x + b2.x)/2,
                              y: (b1.y + b2.y)/2,
                              start: now,
                              size: (b1.r+b2.r)*2.5,
                            }});
                        }}
                        if (soundLoaded) explosionSound.play();
                        b1.vx *= 5; b1.vy *= 5;
                        b2.vx *= 5; b2.vy *= 5;
                    }}
                }}

                // === (2) "보스 vs 일반공" (공격/수비 모두!)
                // (a) 보스가 일반공 약점 때림 (보스는 항상 전체 강점, 일반공 약점만 각도 판정)
                if (b1.isBoss && !b2.isBoss && !b2.stun) {{
                    let weak2 = (angle21 >= 0 && angle21 < 0.8*2*PI);
                    if (weak2 && (now - b2.last_hit > {int(0.5*1000)})) {{
                        b2.hp -= 1;
                        b2.last_hit = now;
                        b2.av += random(-0.25,0.25);
                        if (hitLoaded) hitSound.play();
                    }}
                }}
                if (!b1.isBoss && b2.isBoss && !b1.stun) {{
                    let weak1 = (angle12 >= 0 && angle12 < 0.8*2*PI);
                    if (weak1 && (now - b1.last_hit > {int(0.5*1000)})) {{
                        b1.hp -= 1;
                        b1.last_hit = now;
                        b1.av += random(-0.25,0.25);
                        if (hitLoaded) hitSound.play();
                    }}
                }}

                // (b) 강점끼리 폭발+보스 스턴
                if ( (b1.isBoss && !b2.isBoss) || (!b1.isBoss && b2.isBoss)) {{
                    // 보스/일반공 충돌각(일반공 기준 강점)
                    let normal = b1.isBoss ? b2 : b1;
                    let boss = b1.isBoss ? b1 : b2;
                    let norm_angle = b1.isBoss ? angle21 : angle12;
                    let normalAttack = (norm_angle > 0.8*2*PI && norm_angle <= 2*PI);

                    if (!boss.stun && normalAttack) {{
                        if (explosionLoaded) {{
                            explosions.push({{
                              x: (boss.x + normal.x)/2,
                              y: (boss.y + normal.y)/2,
                              start: now,
                              size: (boss.r+normal.r)*2.7,
                            }});
                        }}
                        if (soundLoaded) explosionSound.play();
                        boss.vx *= 2.5; boss.vy *= 2.5;
                        normal.vx *= 5; normal.vy *= 5;
                        boss.stun = true;
                        boss.stunStart = now;
                    }}

                    // (c) 스턴 중 보스 약점 때리기
                    if (boss.stun && normalAttack) {{
                        if (now - boss.last_hit > {int(0.5*1000)}) {{
                            boss.hp -= 1;
                            boss.last_hit = now;
                            boss.av += random(-0.18,0.18);
                            if (hitLoaded) hitSound.play();
                        }}
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

        // ======= 폭발 그리기 (fade out) =======
        let newExplosions = [];
        for(let i=0; i<explosions.length; i++) {{
          let e = explosions[i];
          let t = now - e.start;
          if (t < 500) {{
            push();
            let alpha = map(t,0,500,255,0);
            tint(255, alpha);
            imageMode(CENTER);
            image(explosionImg, e.x, e.y, e.size, e.size);
            pop();
            newExplosions.push(e);
          }}
        }}
        explosions = newExplosions;

        // ======= 공 그리기 =======
        for(let i=0; i<balls.length; i++) {{
          let b = balls[i];
          if (!b.alive) continue;
          let now = millis();
          push();
          translate(b.x, b.y);
          rotate(b.angle);

          let invuln = (now - b.last_hit < {int(0.5*1000)});
          let alpha = invuln ? 120 : 220;

          fill(b.color[0], b.color[1], b.color[2], alpha);
          stroke(40,80,140,180*alpha/220);
          strokeWeight(3);
          ellipse(0, 0, b.r*2, b.r*2);

          // 약점/강점
          if ({str(fight_mode).lower()}) {{
            noStroke();
            if (b.isBoss) {{
                if (b.stun) {{
                    fill(40,80,255,alpha);
                }} else {{
                    fill(255,80,80,alpha);
                }}
                arc(0,0,b.r*2,b.r*2,0,2*PI,PIE);
            }} else {{
                fill(40,80,255,alpha);
                arc(0,0,b.r*2,b.r*2,0,0.8*2*PI,PIE);
                fill(255,80,80,alpha);
                arc(0,0,b.r*2,b.r*2,0.8*2*PI,2*PI,PIE);
            }}
          }}

          fill(32,32,32,240);
          noStroke();
          textAlign(CENTER, CENTER);
          textSize(b.r*0.8);
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
