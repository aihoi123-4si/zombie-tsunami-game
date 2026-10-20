import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Zombie Tsunami Tropical HD", layout="centered")

st.markdown("<h1 style='text-align: center; color: #76ba1b;'>🧟 ZOMBIE TSUNAMI TROPICAL 🧟</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Nhấn <b>Space</b> hoặc <b>Chạm màn hình</b> để nhảy né vật cản và nuốt chửng người dân!</p>", unsafe_allow_html=True)

game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; padding: 0; background-color: #0d1b2a; display: flex; justify-content: center; align-items: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        canvas { border: 4px solid #76ba1b; border-radius: 12px; box-shadow: 0 8px 30px rgba(118, 186, 27, 0.4); background: #111; }
    </style>
</head>
<body>
    <canvas id="gameCanvas" width="800" height="450"></canvas>
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        let gameState = 'START';
        let score = 0;
        let coins = 67;
        let speed = 4;
        let frame = 0;

        // Zombie Horde
        let zombies = [{ x: 150, y: 320, vy: 0, isGrounded: true, legAngle: 0 }];
        const gravity = 0.65;

        let humans = [];
        let obstacles = [];
        let particles = [];
        let bgOffset = 0;

        function addParticles(x, y, color, count = 10) {
            for(let i=0; i<count; i++) {
                particles.push({
                    x: x, y: y,
                    vx: (Math.random() - 0.5) * 6,
                    vy: (Math.random() - 0.5) * 6,
                    life: 25, color: color
                });
            }
        }

        function handleInput() {
            if (gameState === 'START' || gameState === 'GAMEOVER') {
                resetGame();
                gameState = 'PLAYING';
            } else if (gameState === 'PLAYING') {
                zombies.forEach((z, idx) => {
                    if (z.isGrounded) {
                        z.vy = -13 - (idx * 0.15);
                        z.isGrounded = false;
                    }
                });
            }
        }

        window.addEventListener('keydown', (e) => { if (e.code === 'Space' || e.code === 'ArrowUp') handleInput(); });
        canvas.addEventListener('touchstart', (e) => { e.preventDefault(); handleInput(); });
        canvas.addEventListener('mousedown', handleInput);

        function resetGame() {
            score = 0;
            speed = 4;
            frame = 0;
            zombies = [{ x: 150, y: 320, vy: 0, isGrounded: true, legAngle: 0 }];
            humans = [];
            obstacles = [];
            particles = [];
        }

        function update() {
            if (gameState !== 'PLAYING') return;

            frame++;
            speed = 4 + Math.floor(frame / 600) * 0.5;
            bgOffset = (bgOffset + speed) % 800;

            // Update Zombies
            zombies.forEach((z, index) => {
                z.vy += gravity;
                z.y += z.vy;
                let groundY = 320;
                if (z.y >= groundY) {
                    z.y = groundY;
                    z.vy = 0;
                    z.isGrounded = true;
                }
                z.legAngle += 0.2;
            });

            // Spawn Entities
            if (frame % 110 === 0) {
                if (Math.random() > 0.45) {
                    humans.push({ x: 850, y: 320, eaten: false });
                } else {
                    obstacles.push({ x: 850, y: 310, w: 35, h: 40, type: Math.random() > 0.5 ? 'BOMB' : 'CAR' });
                }
            }

            // Update Humans
            humans.forEach((h) => {
                h.x -= speed;
                let leader = zombies[0];
                if (!h.eaten && leader && Math.abs(leader.x - h.x) < 30 && Math.abs(leader.y - h.y) < 35) {
                    h.eaten = true;
                    score += 1;
                    coins += 1;
                    addParticles(h.x, h.y, '#76ba1b', 12);
                    if (zombies.length < 10) {
                        let tail = zombies[zombies.length - 1];
                        zombies.push({ x: tail.x - 28, y: 320, vy: 0, isGrounded: true, legAngle: 0 });
                    }
                }
            });

            // Update Obstacles
            obstacles.forEach((obs) => {
                obs.x -= speed;
                zombies.forEach((z, zIdx) => {
                    if (Math.abs(z.x - obs.x) < 25 && z.y > obs.y - 25) {
                        addParticles(z.x, z.y, '#ff4444', 15);
                        zombies.splice(zIdx, 1);
                    }
                });
            });

            // Clean up
            humans = humans.filter(h => h.x > -50 && !h.eaten);
            obstacles = obstacles.filter(o => o.x > -50);

            if (zombies.length === 0) {
                gameState = 'GAMEOVER';
            }

            particles.forEach(p => { p.x += p.vx; p.y += p.vy; p.life--; });
            particles = particles.filter(p => p.life > 0);
        }

        // Vẽ Background Bãi Biển
        function drawBackground() {
            // Sky
            let skyGrad = ctx.createLinearGradient(0, 0, 0, 250);
            skyGrad.addColorStop(0, '#1e88e5');
            skyGrad.addColorStop(1, '#90caf9');
            ctx.fillStyle = skyGrad;
            ctx.fillRect(0, 0, canvas.width, 250);

            // Sea
            let seaGrad = ctx.createLinearGradient(0, 220, 0, 340);
            seaGrad.addColorStop(0, '#00838f');
            seaGrad.addColorStop(1, '#00acc1');
            ctx.fillStyle = seaGrad;
            ctx.fillRect(0, 220, canvas.width, 120);

            // Beach Sand
            ctx.fillStyle = '#ffe082';
            ctx.fillRect(0, 310, canvas.width, 30);

            // Clouds
            ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
            ctx.beginPath();
            ctx.arc(150 - (bgOffset*0.3)%900, 60, 30, 0, Math.PI*2);
            ctx.arc(180 - (bgOffset*0.3)%900, 50, 40, 0, Math.PI*2);
            ctx.arc(220 - (bgOffset*0.3)%900, 60, 30, 0, Math.PI*2);
            ctx.fill();

            // Houses in Background
            let houseX = 500 - (bgOffset*0.7)%800;
            ctx.fillStyle = '#e0f2f1';
            ctx.fillRect(houseX, 230, 90, 70); // body
            ctx.fillStyle = '#e57373';
            ctx.beginPath(); // Roof
            ctx.moveTo(houseX - 10, 230);
            ctx.lineTo(houseX + 45, 180);
            ctx.lineTo(houseX + 100, 230);
            ctx.fill();

            // Palm Tree
            let treeX = 100 - (bgOffset*0.8)%800;
            ctx.fillStyle = '#5d4037';
            ctx.fillRect(treeX, 210, 14, 100);
            ctx.fillStyle = '#2e7d32';
            ctx.beginPath();
            ctx.arc(treeX - 15, 200, 25, 0, Math.PI*2);
            ctx.arc(treeX + 30, 200, 25, 0, Math.PI*2);
            ctx.arc(treeX + 7, 185, 30, 0, Math.PI*2);
            ctx.fill();

            // Traffic Light Post
            let poleX = 350 - bgOffset;
            ctx.fillStyle = '#37474f';
            ctx.fillRect(poleX, 150, 8, 190);
            ctx.fillRect(poleX - 15, 150, 35, 6);
            // Light box
            ctx.fillStyle = '#fbc02d';
            ctx.fillRect(poleX + 10, 160, 20, 45);
            ctx.fillStyle = '#4caf50'; // Green light
            ctx.beginPath(); ctx.arc(poleX + 20, 195, 6, 0, Math.PI*2); ctx.fill();

            // Road & Asphalt
            ctx.fillStyle = '#546e7a';
            ctx.fillRect(0, 340, canvas.width, 110);
            ctx.fillStyle = '#37474f';
            ctx.fillRect(0, 340, canvas.width, 8);

            // Yellow Road Line
            ctx.strokeStyle = '#fbc02d';
            ctx.lineWidth = 4;
            ctx.setLineDash([30, 20]);
            ctx.beginPath();
            ctx.moveTo(-bgOffset % 50, 380);
            ctx.lineTo(canvas.width, 380);
            ctx.stroke();
            ctx.setLineDash([]);
        }

        // Vẽ Zombie Chuẩn Zombie Tsunami (Đầu to xanh, mắt lồi, áo đỏ)
        function drawZombie(z) {
            ctx.save();
            ctx.translate(z.x, z.y);

            // Legs
            ctx.strokeStyle = '#1a237e';
            ctx.lineWidth = 5;
            ctx.beginPath();
            ctx.moveTo(-4, 10);
            ctx.lineTo(-4 + Math.sin(z.legAngle)*8, 22);
            ctx.moveTo(4, 10);
            ctx.lineTo(4 - Math.sin(z.legAngle)*8, 22);
            ctx.stroke();

            // Body (Shirt)
            ctx.fillStyle = '#c62828'; // Áo đỏ
            ctx.fillRect(-10, -2, 20, 14);

            // Head (Green Big Head)
            ctx.fillStyle = '#76ba1b';
            ctx.beginPath();
            ctx.ellipse(0, -16, 18, 16, 0, 0, Math.PI * 2);
            ctx.fill();

            // Big Eye
            ctx.fillStyle = '#ffffff';
            ctx.beginPath();
            ctx.arc(6, -18, 8, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#283593';
            ctx.beginPath();
            ctx.arc(8, -18, 3.5, 0, Math.PI * 2);
            ctx.fill();

            // Mouth & Tooth
            ctx.fillStyle = '#1b5e20';
            ctx.beginPath();
            ctx.arc(6, -10, 5, 0, Math.PI);
            ctx.fill();
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(5, -10, 3, 3);

            ctx.restore();
        }

        function draw() {
            drawBackground();

            if (gameState === 'START') {
                ctx.fillStyle = 'rgba(0,0,0,0.5)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#76ba1b';
                ctx.font = 'bold 36px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('ZOMBIE TSUNAMI', 400, 180);
                ctx.fillStyle = '#ffffff';
                ctx.font = '20px sans-serif';
                ctx.fillText('Nhấn Space hoặc Chạm vào màn hình để bắt đầu', 400, 230);
                return;
            }

            // Draw Humans
            humans.forEach(h => {
                ctx.fillStyle = '#ffcc80';
                ctx.beginPath(); ctx.arc(h.x, h.y - 12, 9, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = '#e91e63';
                ctx.fillRect(h.x - 7, h.y - 3, 14, 18);
            });

            // Draw Obstacles
            obstacles.forEach(o => {
                if (o.type === 'BOMB') {
                    ctx.fillStyle = '#212121';
                    ctx.beginPath(); ctx.arc(o.x + 15, o.y + 15, 16, 0, Math.PI*2); ctx.fill();
                    ctx.fillStyle = '#ff1744';
                    ctx.font = 'bold 12px sans-serif';
                    ctx.fillText('💣', o.x + 6, o.y + 20);
                } else {
                    ctx.fillStyle = '#d32f2f';
                    ctx.fillRect(o.x, o.y, o.w, o.h);
                    ctx.fillStyle = '#90caf9';
                    ctx.fillRect(o.x + 4, o.y + 4, 10, 10);
                }
            });

            // Draw Zombies
            zombies.forEach(z => drawZombie(z));

            // Particles
            particles.forEach(p => {
                ctx.fillStyle = p.color;
                ctx.fillRect(p.x, p.y, 4, 4);
            });

            // UI HUD (Top Bar like Zombie Tsunami)
            ctx.fillStyle = 'rgba(0,0,0,0.4)';
            ctx.fillRect(15, 12, 160, 70);
            ctx.fillStyle = '#fbc02d';
            ctx.font = 'bold 22px sans-serif';
            ctx.textAlign = 'left';
            ctx.fillText(`🪙 ${coins}`, 25, 40);
            ctx.fillStyle = '#76ba1b';
            ctx.fillText(`🧠 x${zombies.length}`, 25, 70);

            if (gameState === 'GAMEOVER') {
                ctx.fillStyle = 'rgba(0,0,0,0.75)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#ff1744';
                ctx.font = 'bold 42px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('GAME OVER', 400, 190);
                ctx.fillStyle = '#ffffff';
                ctx.font = '22px sans-serif';
                ctx.fillText(`Số người nuốt chửng: ${score}`, 400, 240);
                ctx.fillText('Nhấn Space / Chạm để chơi lại', 400, 280);
            }
        }

        function loop() {
            update();
            draw();
            requestAnimationFrame(loop);
        }
        loop();
    </script>
</body>
</html>
"""

components.html(game_code, height=480)
