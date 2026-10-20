import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Zombie Tsunami Pit Jump HD", layout="centered")

st.markdown("<h1 style='text-align: center; color: #76ba1b;'>🧟 ZOMBIE TSUNAMI - VÁCH NGĂN 🧟</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Nhấn <b>Space</b> hoặc <b>Chạm màn hình</b> để nhảy qua các <b>vực thẳm / vách ngăn</b>, né vật cản và nuốt chửng người dân!</p>", unsafe_allow_html=True)

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
        let coins = 0;
        let speed = 4.5;
        let frame = 0;

        const gravity = 0.65;
        const groundY = 340;

        // Zombie Horde
        let zombies = [{ x: 160, y: groundY - 20, vy: 0, isGrounded: true, legAngle: 0 }];

        let humans = [];
        let obstacles = [];
        let pits = []; // Danh sách các vực thẳm / vách ngăn
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
                        z.vy = -13 - (idx * 0.12);
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
            coins = 0;
            speed = 4.5;
            frame = 0;
            zombies = [{ x: 160, y: groundY - 20, vy: 0, isGrounded: true, legAngle: 0 }];
            humans = [];
            obstacles = [];
            pits = [];
            particles = [];
        }

        // Kiểm tra vị trí x có nằm trên vực không
        function isOverPit(x) {
            return pits.some(p => x > p.x && x < p.x + p.width);
        }

        function update() {
            if (gameState !== 'PLAYING') return;

            frame++;
            speed = 4.5 + Math.floor(frame / 500) * 0.4;
            bgOffset += speed;

            // Spawn Vực Thẳm (Pits)
            if (frame % 220 === 0 && Math.random() > 0.3) {
                pits.push({ x: 850, width: 110 + Math.random() * 40 });
            }

            // Spawn Humans & Obstacles (chỉ tạo ở vùng có đường)
            if (frame % 110 === 0) {
                let spawnX = 850;
                if (!isOverPit(spawnX) && !isOverPit(spawnX + 60)) {
                    if (Math.random() > 0.45) {
                        humans.push({ x: spawnX, y: groundY - 20, eaten: false });
                    } else {
                        obstacles.push({ x: spawnX, y: groundY - 40, w: 55, h: 35, type: Math.random() > 0.5 ? 'BOMB' : 'CAR' });
                    }
                }
            }

            // Move Pits
            pits.forEach(p => p.x -= speed);
            pits = pits.filter(p => p.x + p.width > -50);

            // Update Zombies
            for (let i = zombies.length - 1; i >= 0; i--) {
                let z = zombies[i];
                z.vy += gravity;
                z.y += z.vy;

                let onPit = isOverPit(z.x);

                if (!onPit && z.y >= groundY - 20) {
                    z.y = groundY - 20;
                    z.vy = 0;
                    z.isGrounded = true;
                } else if (onPit) {
                    z.isGrounded = false; // Rơi xuống vực nếu đang trên vực
                }

                z.legAngle += 0.2;

                // Nếu zombie rơi quá sâu dưới vực -> Bị tiêu diệt
                if (z.y > canvas.height + 40) {
                    addParticles(z.x, canvas.height - 20, '#76ba1b', 10);
                    zombies.splice(i, 1);
                }
            }

            // Update Humans
            humans.forEach((h) => {
                h.x -= speed;
                let leader = zombies[0];
                if (!h.eaten && leader && Math.abs(leader.x - h.x) < 30 && Math.abs(leader.y - h.y) < 35) {
                    h.eaten = true;
                    score += 1;
                    coins += 5;
                    addParticles(h.x, h.y, '#76ba1b', 12);
                    if (zombies.length < 10) {
                        let tail = zombies[zombies.length - 1];
                        zombies.push({ x: tail.x - 26, y: tail.y, vy: 0, isGrounded: tail.isGrounded, legAngle: 0 });
                    }
                }
            });

            // Update Obstacles
            obstacles.forEach((obs) => {
                obs.x -= speed;
                zombies.forEach((z, zIdx) => {
                    if (Math.abs(z.x - obs.x) < 25 && z.y > obs.y - 20) {
                        addParticles(z.x, z.y, '#ff4444', 15);
                        zombies.splice(zIdx, 1);
                    }
                });
            });

            humans = humans.filter(h => h.x > -50 && !h.eaten);
            obstacles = obstacles.filter(o => o.x > -50);

            if (zombies.length === 0) {
                gameState = 'GAMEOVER';
            }

            particles.forEach(p => { p.x += p.vx; p.y += p.vy; p.life--; });
            particles = particles.filter(p => p.life > 0);
        }

        // Vẽ Background & Mặt đường có vách vực
        function drawBackground() {
            // Sky
            let skyGrad = ctx.createLinearGradient(0, 0, 0, 250);
            skyGrad.addColorStop(0, '#1976d2');
            skyGrad.addColorStop(1, '#64b5f6');
            ctx.fillStyle = skyGrad;
            ctx.fillRect(0, 0, canvas.width, 250);

            // Sea
            let seaGrad = ctx.createLinearGradient(0, 200, 0, 340);
            seaGrad.addColorStop(0, '#00838f');
            seaGrad.addColorStop(1, '#00acc1');
            ctx.fillStyle = seaGrad;
            ctx.fillRect(0, 200, canvas.width, 140);

            // Beach Sand
            ctx.fillStyle = '#ffe082';
            ctx.fillRect(0, 300, canvas.width, 40);

            // House in Background
            let houseX = 520 - (bgOffset*0.6)%800;
            ctx.fillStyle = '#e0f2f1';
            ctx.fillRect(houseX, 220, 90, 80);
            ctx.fillStyle = '#e57373';
            ctx.beginPath();
            ctx.moveTo(houseX - 10, 220);
            ctx.lineTo(houseX + 45, 170);
            ctx.lineTo(houseX + 100, 220);
            ctx.fill();

            // Palm Tree
            let treeX = 120 - (bgOffset*0.8)%800;
            ctx.fillStyle = '#5d4037';
            ctx.fillRect(treeX, 200, 14, 110);
            ctx.fillStyle = '#2e7d32';
            ctx.beginPath();
            ctx.arc(treeX - 15, 190, 25, 0, Math.PI*2);
            ctx.arc(treeX + 30, 190, 25, 0, Math.PI*2);
            ctx.arc(treeX + 7, 175, 30, 0, Math.PI*2);
            ctx.fill();

            // --- VẼ ĐƯỜNG VÀ VẠCH VỰC THẲM ---
            // 1. Lớp đất đá bên dưới
            ctx.fillStyle = '#261c14';
            ctx.fillRect(0, groundY, canvas.width, canvas.height - groundY);

            // 2. Mặt đường Asphalt
            ctx.fillStyle = '#37474f';
            ctx.fillRect(0, groundY, canvas.width, 12);
            ctx.fillStyle = '#455a64';
            ctx.fillRect(0, groundY + 12, canvas.width, canvas.height - groundY - 12);

            // 3. Cắt tỉa tạo các Vực Thẳm (Pits)
            pits.forEach(p => {
                ctx.clearRect(p.x, groundY, p.width, canvas.height - groundY);
                // Vẽ vách đá 2 bên vực
                ctx.fillStyle = '#1a100a';
                ctx.fillRect(p.x - 6, groundY, 6, canvas.height - groundY);
                ctx.fillRect(p.x + p.width, groundY, 6, canvas.height - groundY);
            });

            // Vạch kẻ đường (Tránh vẽ đè lên vực)
            ctx.strokeStyle = '#fbc02d';
            ctx.lineWidth = 4;
            let dashWidth = 30;
            let dashGap = 20;
            let startX = - (bgOffset % (dashWidth + dashGap));

            for (let x = startX; x < canvas.width; x += dashWidth + dashGap) {
                if (!isOverPit(x) && !isOverPit(x + dashWidth)) {
                    ctx.beginPath();
                    ctx.moveTo(x, groundY + 45);
                    ctx.lineTo(x + dashWidth, groundY + 45);
                    ctx.stroke();
                }
            }
        }

        // Vẽ Zombie
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

            // Body
            ctx.fillStyle = '#c62828';
            ctx.fillRect(-10, -2, 20, 14);

            // Head
            ctx.fillStyle = '#76ba1b';
            ctx.beginPath();
            ctx.ellipse(0, -16, 18, 16, 0, 0, Math.PI * 2);
            ctx.fill();

            // Eye
            ctx.fillStyle = '#ffffff';
            ctx.beginPath();
            ctx.arc(6, -18, 8, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#283593';
            ctx.beginPath();
            ctx.arc(8, -18, 3.5, 0, Math.PI * 2);
            ctx.fill();

            // Mouth
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
                ctx.fillStyle = 'rgba(0,0,0,0.55)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#76ba1b';
                ctx.font = 'bold 36px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('ZOMBIE TSUNAMI', 400, 180);
                ctx.fillStyle = '#ffffff';
                ctx.font = '20px sans-serif';
                ctx.fillText('Nhấn Space / Chạm màn hình để nhảy qua Vách Ngăn!', 400, 230);
                return;
            }

            // Humans
            humans.forEach(h => {
                ctx.fillStyle = '#ffcc80';
                ctx.beginPath(); ctx.arc(h.x, h.y - 12, 9, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = '#e91e63';
                ctx.fillRect(h.x - 7, h.y - 3, 14, 18);
            });

            // Obstacles
            obstacles.forEach(o => {
                if (o.type === 'BOMB') {
                    ctx.fillStyle = '#212121';
                    ctx.beginPath(); ctx.arc(o.x + 15, o.y + 15, 16, 0, Math.PI*2); ctx.fill();
                    ctx.fillStyle = '#ff1744';
                    ctx.font = 'bold 14px sans-serif';
                    ctx.fillText('💣', o.x + 6, o.y + 20);
                } else {
                    ctx.fillStyle = '#e53935';
                    ctx.fillRect(o.x, o.y + 10, o.w, 20);
                    ctx.fillStyle = '#b71c1c';
                    ctx.beginPath();
                    ctx.roundRect(o.x + 10, o.y, 35, 12, [6, 6, 0, 0]);
                    ctx.fill();
                    ctx.fillStyle = '#90caf9';
                    ctx.fillRect(o.x + 14, o.y + 2, 12, 9);
                    ctx.fillRect(o.x + 28, o.y + 2, 14, 9);
                    ctx.fillStyle = '#212121';
                    ctx.beginPath();
                    ctx.arc(o.x + 12, o.y + 30, 6, 0, Math.PI*2);
                    ctx.arc(o.x + 43, o.y + 30, 6, 0, Math.PI*2);
                    ctx.fill();
                }
            });

            // Zombies
            zombies.forEach(z => drawZombie(z));

            // Particles
            particles.forEach(p => {
                ctx.fillStyle = p.color;
                ctx.fillRect(p.x, p.y, 4, 4);
            });

            // HUD UI
            ctx.fillStyle = 'rgba(0,0,0,0.45)';
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
