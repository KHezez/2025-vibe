import streamlit as st

st.components.v1.html("""
<canvas id="myCanvas" width="400" height="200" style="background:#222"></canvas>
<script>
const canvas = document.getElementById('myCanvas');
const ctx = canvas.getContext('2d');
let x = 0;
function animate() {
  ctx.clearRect(0,0,400,200);
  ctx.beginPath();
  ctx.arc(50+x, 100, 24, 0, 2*Math.PI);
  ctx.fillStyle = "#0ff";
  ctx.shadowColor = "#0ff";
  ctx.shadowBlur = 22;
  ctx.fill();
  x += 1.5; if (x > 300) x = 0;
  requestAnimationFrame(animate);
}
animate();
</script>
""", height=210)
