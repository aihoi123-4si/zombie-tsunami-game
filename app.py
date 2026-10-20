
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Zombie Tsunami City Night HD", layout="centered")

st.markdown("<h1 style='text-align: center; color: #76ba1b;'>🧟 ZOMBIE TSUNAMI - CITY NIGHT 🧟</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Gom đủ đàn Zombie để **tông lật xe hơi (cần 4 zombie)** hoặc nhảy né chướng ngại vật!</p>", unsafe_allow_html=True)

game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; padding: 0; background-color: #0b132b; display: flex; justify-content: center; align-items: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        canvas { border: 4px solid #76ba1b; border-radius: 12px; box-shadow: 0 8px 30px rgba(118, 186, 27, 0.4); background: #0b132b; }
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
        let pits = [];
        let particles = [];
        let bgOffset = 0;

        function addParticles(x, y, color, count = 10) {
            for(let i=0; i<count; i++) {
                particles.push({
                    x: x, y: y,
                    vx: (Math.random() - 0.5) * 8,
                    vy: (Math.random() - 0.5) * 8,
                    life: 30, color: color
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
                        z.vy = -13.5 - (idx * 0.12);
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

        function isOverPit(x) {
            return pits.some(p => x > p.x && x < p.x + p.width);
        }

        function update() {
            if (gameState !== 'PLAYING') return;

            frame++;
            speed = 4.5 + Math.floor(frame / 500) * 0.4;
            bgOffset += speed;

            // Spawn Pits
            if (frame % 250 === 0 && Math.random() > 0.4) {
                pits.push({ x: 850, width: 110 + Math.random() * 40 });
            }

            // Spawn Entities
            if (frame % 120 === 0) {
                let spawnX = 850;
                if (!isOverPit(spawnX) && !isOverPit(spawnX + 130)) {
                    let rand = Math.random();
                    if (rand < 0.35) {
                        let gender = Math.random() > 0.5 ? 'MALE' : 'FEMALE';
                        humans.push({ x: spawnX, y: groundY - 20, gender: gender, eaten: false, armAngle: 0 });
                    } else if (rand < 0.7) {
                        // Xe hơi xám nâu kiểu cổ điển với cửa nóc thò người ra (Yêu cầu 4 Zombie để phá)
                        obstacles.push({ x: spawnX, y: groundY - 50, w: 90, h: 50, type: 'FLIP_CAR', reqZombies: 4, hit: false });
                    } else if (rand < 0.85) {
                        obstacles.push({ x: spawnX, y: groundY - 70, w: 140, h: 70, type: 'BUS', reqZombies: 8, hit: false });
                    } else {
                        obstacles.push({ x: spawnX, y: groundY - 40, w: 35, h: 40, type: 'BOMB' });
                    }
                }
            }

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
                    z.isGrounded = false;
                }

                z.legAngle += 0.2;

                if (z.y > canvas.height + 40) {
                    addParticles(z.x, canvas.height - 20, '#76ba1b', 10);
                    zombies.splice(i, 1);
                }
            }

            // Update Humans
            humans.forEach((h) => {
                h.x -= speed;
                h.armAngle += 0.15;
                let leader = zombies[0];
                if (!h.eaten && leader && Math.abs(leader.x - h.x) < 30 && Math.abs(leader.y - h.y) < 35) {
                    h.eaten = true;
                    score += 1;
                    coins += 5;
                    addParticles(h.x, h.y, '#76ba1b', 12);
                    if (zombies.length < 12) {
                        let tail = zombies[zombies.length - 1];
                        zombies.push({ x: tail.x - 26, y: tail.y, vy: 0, isGrounded: tail.isGrounded, legAngle: 0 });
                    }
                }
            });

            // Update Obstacles & Car Flipping Mechanics
            obstacles.forEach((obs, obsIdx) => {
                obs.x -= speed;
                if (obs.type === 'FLIP_CAR' || obs.type === 'BUS') {
                    let leader = zombies[0];
                    if (leader && Math.abs(leader.x - obs.x) < 35 && !obs.hit) {
                        if (zombies.length >= obs.reqZombies) {
                            // Đủ số lượng Zombie -> Tông nổ lật xe & cộng thêm zombie!
                            obs.hit = true;
                            addParticles(obs.x + obs.w/2, obs.y + obs.h/2, '#ff9800', 25);
                            score += obs.reqZombies;
                            coins += 20;
                            for (let k = 0; k < 2; k++) {
                                if (zombies.length < 12) {
                                    let tail = zombies[zombies.length - 1];
                                    zombies.push({ x: tail.x - 26, y: tail.y, vy: 0, isGrounded: tail.isGrounded, legAngle: 0 });
                                }
                            }
                            obstacles.splice(obsIdx, 1);
                        } else {
                            // Không đủ zombie -> Mất zombie khi đâm vào
                            obs.hit = true;
                            addParticles(leader.x, leader.y, '#ff4444', 15);
                            zombies.shift(); // Mất 1 zombie
                        }
                    }
                } else if (obs.type === 'BOMB') {
                    zombies.forEach((z, zIdx) => {
                        if (Math.abs(z.x - obs.x) < 20 && z.y > obs.y - 20) {
                            addParticles(z.x, z.y, '#ff4444', 15);
                            zombies.splice(zIdx, 1);
                        }
                    });
                }
            });

            humans = humans.filter(h => h.x > -50 && !h.eaten);
            obstacles = obstacles.filter(o => o.x > -150);

            if (zombies.length === 0) {
                gameState = 'GAMEOVER';
            }

            particles.forEach(p => { p.x += p.vx; p.y += p.vy; p.life--; });
            particles = particles.filter(p => p.life > 0);
        }

        // Background Thành Phố Ban Đêm
        function drawBackground() {
            // Sky gradient (Đêm tà)
            let skyGrad = ctx.createLinearGradient(0, 0, 0, 250);
            skyGrad.addColorStop(0, '#0b132b');
            skyGrad.addColorStop(1, '#1c2541');
            ctx.fillStyle = skyGrad;
            ctx.fillRect(0, 0, canvas.width, 250);

            // Buildings in Background with Lights
            ctx.fillStyle = '#141d36';
            for (let i = 0; i < 8; i++) {
                let bX = (i * 120 - (bgOffset * 0.3) % 120);
                ctx.fillRect(bX, 120, 80, 180);
                // Windows
                ctx.fillStyle = '#ffb74d';
                for (let wY = 130; wY < 260; wY += 20) {
                    for (let wX = bX + 10; wX < bX + 70; wX += 20) {
                        if ((wX + wY) % 3 === 0) ctx.fillRect(wX, wY, 10, 12);
                    }
                }
                ctx.fillStyle = '#141d36';
            }

            // Blue Overpass Bridge (Cầu vượt xanh nước biển như ảnh)
            ctx.fillStyle = '#1e3d59';
            let bridgeX = -(bgOffset * 0.6) % 300;
            for (let b = bridgeX - 300; b < canvas.width + 300; b += 160) {
                // Bridge Pillars & Arches
                ctx.beginPath();
                ctx.arc(b + 80, 260, 60, Math.PI, 0);
                ctx.lineWidth = 12;
                ctx.strokeStyle = '#17b978';
                ctx.stroke();
                ctx.fillRect(b, 200, 20, 100);
            }
            ctx.fillRect(0, 200, canvas.width, 16); // Bridge Deck

            // Traffic Light Post
            let poleX = 400 - (bgOffset % 800);
            ctx.fillStyle = '#333';
            ctx.fillRect(poleX, 150, 8, 190);
            ctx.fillStyle = '#fbc02d';
            ctx.fillRect(poleX - 10, 150, 28, 45);
            ctx.fillStyle = '#4caf50';
            ctx.beginPath(); ctx.arc(poleX + 4, 183, 6, 0, Math.PI*2); ctx.fill();

            // Ground & Dark Asphalt
            ctx.fillStyle = '#111827';
            ctx.fillRect(0, groundY, canvas.width, canvas.height - groundY);
            ctx.fillStyle = '#1f2937';
            ctx.fillRect(0, groundY, canvas.width, 12);

            // Cut Pits
            pits.forEach(p => {
                ctx.clearRect(p.x, groundY, p.width, canvas.height - groundY);
                ctx.fillStyle = '#050811';
                ctx.fillRect(p.x - 6, groundY, 6, canvas.height - groundY);
                ctx.fillRect(p.x + p.width, groundY, 6, canvas.height - groundY);
            });

            // Road Lines
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 3;
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

            ctx.strokeStyle = '#1a237e';
            ctx.lineWidth = 5;
            ctx.beginPath();
            ctx.moveTo(-4, 10);
            ctx.lineTo(-4 + Math.sin(z.legAngle)*8, 22);
            ctx.moveTo(4, 10);
            ctx.lineTo(4 - Math.sin(z.legAngle)*8, 22);
            ctx.stroke();

            ctx.fillStyle = '#3f51b5'; ctx.fillRect(-10, -2, 20, 14);
            ctx.fillStyle = '#76ba1b';
            ctx.beginPath(); ctx.ellipse(0, -16, 18, 16, 0, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#ffffff';
            ctx.beginPath(); ctx.arc(6, -18, 8, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#283593';
            ctx.beginPath(); ctx.arc(8, -18, 3.5, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#1b5e20';
            ctx.beginPath(); ctx.arc(6, -10, 5, 0, Math.PI); ctx.fill();
            ctx.fillStyle = '#ffffff'; ctx.fillRect(5, -10, 3, 3);

            ctx.restore();
        }

        // Vẽ Người Dân
        function drawHuman(h) {
            ctx.save();
            ctx.translate(h.x, h.y);

            ctx.fillStyle = '#ffcc80';
            ctx.beginPath(); ctx.arc(0, -18, 9, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = h.gender === 'MALE' ? '#5d4037' : '#fbc02d';
            ctx.beginPath(); ctx.arc(0, -21, 9, Math.PI, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#000';
            ctx.beginPath(); ctx.arc(-3, -18, 1.5, 0, Math.PI*2); ctx.arc(3, -18, 1.5, 0, Math.PI*2); ctx.fill();
            ctx.beginPath(); ctx.arc(0, -14, 3, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = h.gender === 'MALE' ? '#1e88e5' : '#e91e63';
            ctx.fillRect(-7, -9, 14, 12);
            ctx.strokeStyle = '#ffcc80'; ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(-6, -6); ctx.lineTo(-12, -18 + Math.sin(h.armAngle)*4);
            ctx.moveTo(6, -6); ctx.lineTo(12, -18 - Math.sin(h.armAngle)*4);
            ctx.stroke();

            ctx.restore();
        }

        // Vẽ Xe Hơi Cổ Có Người Thò Đầu Ra Cửa Nóc (Sunroof) & Bảng Yêu Cầu Zombie (0/4)
        function drawFlipCar(o) {
            ctx.save();
            ctx.translate(o.x, o.y);

            // Thân Xe Xám Nâu Cổ Đổi Kích Thước Giống Ảnh Mẫu
            ctx.fillStyle = '#4a3f35';
            ctx.beginPath();
            ctx.roundRect(0, 15, o.w, 28, [12, 12, 4, 4]);
            ctx.fill();

            // Mui Xe Bầu Dục
            ctx.fillStyle = '#362d26';
            ctx.beginPath();
            ctx.roundRect(15, 0, 55, 20, [15, 15, 0, 0]);
            ctx.fill();

            // Đèn Pha Đỏ Sau & Bánh Xe
            ctx.fillStyle = '#ff1744'; ctx.fillRect(2, 22, 6, 8);
            ctx.fillStyle = '#111';
            ctx.beginPath();
            ctx.arc(20, 42, 10, 0, Math.PI*2);
            ctx.arc(o.w - 20, 42, 10, 0, Math.PI*2);
            ctx.fill();

            // Cửa Nóc (Sunroof Open) & Người Dân Thò Người Ra Ngoại Hoảng Sợ
            ctx.fillStyle = '#111';
            ctx.fillRect(28, 0, 28, 4);

            // Người Thò Đầu Há Miệng To Đang Kêu Cứu (Mô phỏng chuẩn ảnh)
            ctx.fillStyle = '#ffcc80';
            ctx.beginPath(); ctx.arc(42, -14, 11, 0, Math.PI*2); ctx.fill(); // Đầu to
            ctx.fillStyle = '#5d4037'; ctx.beginPath(); ctx.arc(42, -18, 11, Math.PI, Math.PI*2); ctx.fill(); // Tóc
            // Mắt to tròn lồi
            ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(38, -16, 4, 0, Math.PI*2); ctx.arc(46, -16, 4, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#000'; ctx.beginPath(); ctx.arc(38, -16, 2, 0, Math.PI*2); ctx.arc(46, -16, 2, 0, Math.PI*2); ctx.fill();
            // Miệng há to đen thui
            ctx.fillStyle = '#000'; ctx.beginPath(); ctx.arc(42, -9, 5, 0, Math.PI*2); ctx.fill();
            // Tay giơ sang 2 bên
            ctx.strokeStyle = '#ffcc80'; ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.moveTo(34, -8); ctx.lineTo(24, -18);
            ctx.moveTo(50, -8); ctx.lineTo(60, -18);
            ctx.stroke();

            // BÓNG THOẠI YÊU CẦU ZOMBIE (Ví dụ: x/4)
            ctx.fillStyle = '#1a1a1a';
            ctx.beginPath();
            ctx.roundRect(15, -60, 60, 32, [8, 8, 8, 8]);
            ctx.fill();
            // Mũi tên bóng thoại
            ctx.beginPath();
            ctx.moveTo(40, -28); ctx.lineTo(48, -28); ctx.lineTo(42, -20); ctx.fill();

            // Chữ hiển thị số Zombie cần: (Số Zombie hiện tại / 4)
            ctx.fillStyle = '#ff9800';
            ctx.font = 'bold 18px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(`${zombies.length}/${o.reqZombies}`, 45, -38);

            ctx.restore();
        }

        function draw() {
            drawBackground();

            if (gameState === 'START') {
                ctx.fillStyle = 'rgba(0,0,0,0.65)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#76ba1b';
                ctx.font = 'bold 36px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('ZOMBIE TSUNAMI', 400, 180);
                ctx.fillStyle = '#ffffff';
                ctx.font = '20px sans-serif';
                ctx.fillText('Nhấn Space / Chạm màn hình để bắt đầu chơi!', 400, 230);
                return;
            }

            humans.forEach(h => drawHuman(h));

            obstacles.forEach(o => {
                if (o.type === 'BOMB') {
                    ctx.fillStyle = '#212121';
                    ctx.beginPath(); ctx.arc(o.x + 15, o.y + 15, 16, 0, Math.PI*2); ctx.fill();
                    ctx.fillStyle = '#ff1744'; ctx.font = 'bold 14px sans-serif'; ctx.fillText('💣', o.x + 6, o.y + 20);
                } else if (o.type === 'FLIP_CAR') {
                    drawFlipCar(o);
                } else if (o.type === 'BUS') {
                    ctx.fillStyle = '#fbc02d';
                    ctx.beginPath(); ctx.roundRect(o.x, o.y, o.w, 58, [8, 8, 0, 0]); ctx.fill();
                    ctx.fillStyle = '#1a1a1a';
                    ctx.beginPath(); ctx.roundRect(o.x + 40, o.y - 45, 60, 30, [6, 6, 6, 6]); ctx.fill();
                    ctx.fillStyle = '#ff9800'; ctx.font = 'bold 16px sans-serif'; ctx.textAlign = 'center';
                    ctx.fillText(`${zombies.length}/${o.reqZombies}`, o.x + 70, o.y - 25);
                }
            });

            zombies.forEach(z => drawZombie(z));

            particles.forEach(p => {
                ctx.fillStyle = p.color;
                ctx.fillRect(p.x, p.y, 4, 4);
            });

            // UI HUD
            ctx.fillStyle = 'rgba(0,0,0,0.55)';
            ctx.fillRect(15, 12, 160, 70);
            ctx.fillStyle = '#fbc02d';
            ctx.font = 'bold 22px sans-serif';
            ctx.textAlign = 'left';
            ctx.fillText(`🪙 ${coins}`, 25, 40);
            ctx.fillStyle = '#76ba1b';
            ctx.fillText(`🧠 x${zombies.length}`, 25, 70);

            if (gameState === 'GAMEOVER') {
                ctx.fillStyle = 'rgba(0,0,0,0.8)';
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
