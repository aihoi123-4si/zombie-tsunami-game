import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Zombie Tsunami Close-up & Tsunami HD", layout="centered")

st.markdown("<h1 style='text-align: center; color: #76ba1b;'>🧟 ZOMBIE TSUNAMI - SÓNG THẦN 🧟</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Góc nhìn gần sống động, vách ngăn đa dạng cao thấp và kỹ năng <b>Sóng Thần</b> hủy diệt!</p>", unsafe_allow_html=True)

game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; padding: 0; background-color: #0d1b2a; display: flex; justify-content: center; align-items: center; font-family: sans-serif; }
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
        const groundY = 330;

        // Zombie Horde
        let zombies = [{ x: 140, y: groundY - 20, vy: 0, isGrounded: true, legAngle: 0 }];

        let humans = [];
        let obstacles = [];
        let pits = [];
        let particles = [];
        let bgOffset = 0;
        let cameraX = 0; 

        // Hiệu ứng Sóng Thần (Tsunami Power-up)
        let tsunamiActive = false;
        let tsunamiTimer = 0;

        function addParticles(x, y, color, count = 12) {
            for(let i=0; i<count; i++) {
                particles.push({
                    x: x, y: y,
                    vx: (Math.random() - 0.5) * 8,
                    vy: (Math.random() - 0.5) * 8,
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
                        z.vy = -13.5 - (idx * 0.08);
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
            zombies = [{ x: 140, y: groundY - 20, vy: 0, isGrounded: true, legAngle: 0 }];
            humans = [];
            obstacles = [];
            pits = [];
            particles = [];
            cameraX = 0;
            tsunamiActive = false;
            tsunamiTimer = 0;
        }

        function isOverPit(x) {
            return pits.some(p => x > p.x && x < p.x + p.width);
        }

        function update() {
            if (gameState !== 'PLAYING') return;

            frame++;
            speed = 4.5 + Math.floor(frame / 600) * 0.4;
            bgOffset += speed;

            // Kích hoạt sóng thần ngẫu nhiên mỗi khi đạt mốc thời gian hoặc điểm
            if (!tsunamiActive && frame > 0 && frame % 600 === 0) {
                tsunamiActive = true;
                tsunamiTimer = 200; // Thời gian duy trì sóng thần
                // Tăng thêm quân số khi vào sóng thần
                for(let k=0; k<5; k++) {
                    let tail = zombies[zombies.length - 1];
                    zombies.push({ x: tail.x - 24, y: tail.y, vy: 0, isGrounded: true, legAngle: 0 });
                }
            }

            if (tsunamiActive) {
                tsunamiTimer--;
                if (tsunamiTimer <= 0) tsunamiActive = false;
            }

            // Spawn Vách Ngăn (Hố) lúc rộng lúc hẹp ngẫu nhiên
            if (frame % 220 === 0 && Math.random() > 0.3) {
                let pitWidth = 80 + Math.random() * 70; // Độ rộng hố lúc cao lúc thấp/khác nhau
                pits.push({ x: cameraX + 850, width: pitWidth });
            }

            // Spawn Chướng ngại vật & Người
            if (frame % 110 === 0) {
                let spawnX = cameraX + 850;
                if (!isOverPit(spawnX) && !isOverPit(spawnX + 130)) {
                    let rand = Math.random();
                    if (rand < 0.3) {
                        let gender = Math.random() > 0.5 ? 'MALE' : 'FEMALE';
                        humans.push({ x: spawnX, y: groundY - 20, gender: gender, eaten: false, armAngle: 0 });
                    } else if (rand < 0.65) {
                        obstacles.push({ x: spawnX, y: groundY - 45, w: 90, h: 45, type: 'CAR', reqZombies: 4, peopleInside: 3, hit: false });
                    } else if (rand < 0.85) {
                        obstacles.push({ x: spawnX, y: groundY - 65, w: 130, h: 65, type: 'BUS', reqZombies: 8, peopleInside: 6, hit: false });
                    } else {
                        obstacles.push({ x: spawnX, y: groundY - 40, w: 40, h: 40, type: 'BOMB' });
                    }
                }
            }

            pits = pits.filter(p => p.x + p.width > cameraX - 50);

            // Update Zombies & Physics
            for (let i = zombies.length - 1; i >= 0; i--) {
                let z = zombies[i];
                
                if (tsunamiActive) {
                    // Trạng thái Sóng Thần: Bay lướt qua mọi chướng ngại vật
                    z.y = groundY - 50 + Math.sin(frame * 0.2 + i * 0.5) * 20;
                    z.vy = 0;
                    z.isGrounded = true;
                } else {
                    z.vy += gravity;
                    z.y += z.vy;

                    let onPit = isOverPit(z.x);
                    let standingOnVehicle = false;

                    obstacles.forEach((obs) => {
                        if (obs.type === 'CAR' || obs.type === 'BUS') {
                            if (z.x >= obs.x - 10 && z.x <= obs.x + obs.w + 10) {
                                let roofY = obs.y - 18;
                                if (z.y >= roofY && z.y <= obs.y + 10 && z.vy >= 0) {
                                    z.y = roofY;
                                    z.vy = 0;
                                    z.isGrounded = true;
                                    standingOnVehicle = true;
                                }
                            }
                        }
                    });

                    if (!standingOnVehicle) {
                        if (!onPit && z.y >= groundY - 20) {
                            z.y = groundY - 20;
                            z.vy = 0;
                            z.isGrounded = true;
                        } else if (onPit) {
                            z.isGrounded = false;
                        }
                    }
                }

                z.legAngle += 0.2;

                if (z.y > canvas.height + 30) {
                    addParticles(z.x, canvas.height - 10, '#76ba1b', 10);
                    zombies.splice(i, 1);
                }
            }

            // Góc nhìn Camera đặt gần lại hơn (zoom sát nhân vật chính hơn)
            if (zombies.length > 0) {
                cameraX = zombies[0].x - 110; 
            }

            // Update Humans
            humans.forEach((h) => {
                h.armAngle += 0.15;
                let leader = zombies[0];
                if (!h.eaten && leader && Math.abs(leader.x - h.x) < 30 && Math.abs(leader.y - h.y) < 35) {
                    h.eaten = true;
                    score += 1;
                    coins += 5;
                    addParticles(h.x, h.y, '#76ba1b', 12);
                    if (zombies.length < 25) {
                        let tail = zombies[zombies.length - 1];
                        zombies.push({ x: tail.x - 24, y: tail.y, vy: 0, isGrounded: tail.isGrounded, legAngle: 0 });
                    }
                }
            });

            // Update Obstacles
            obstacles.forEach((obs, obsIdx) => {
                if (tsunamiActive) {
                    // Sóng thần cuốn phăng mọi chướng ngại vật
                    if (Math.abs(zombies[0].x - obs.x) < 80) {
                        addParticles(obs.x + obs.w/2, obs.y, '#1e88e5', 20);
                        obstacles.splice(obsIdx, 1);
                        score += 5;
                    }
                } else {
                    if (obs.type === 'CAR' || obs.type === 'BUS') {
                        zombies.forEach((z) => {
                            if (z.x + 12 > obs.x && z.x - 12 < obs.x + obs.w && z.y > obs.y + 5) {
                                if (zombies.length >= obs.reqZombies) {
                                    if (!obs.hit) {
                                        obs.hit = true;
                                        addParticles(obs.x + obs.w/2, obs.y + obs.h/2, '#ff9800', 30);
                                        score += obs.peopleInside;
                                        coins += obs.peopleInside * 10;
                                        for (let k = 0; k < obs.peopleInside; k++) {
                                            if (zombies.length < 25) {
                                                let tail = zombies[zombies.length - 1];
                                                zombies.push({ x: tail.x - 24, y: tail.y, vy: 0, isGrounded: tail.isGrounded, legAngle: 0 });
                                            }
                                        }
                                        obstacles.splice(obsIdx, 1);
                                    }
                                } else {
                                    if (!obs.hit) {
                                        obs.hit = true;
                                        addParticles(z.x, z.y, '#ff4444', 20);
                                        zombies.shift();
                                    }
                                }
                            }
                        });
                    } else if (obs.type === 'BOMB') {
                        zombies.forEach((z, zIdx) => {
                            if (Math.abs(z.x - (obs.x + 20)) < 22 && Math.abs(z.y - (obs.y + 20)) < 25) {
                                addParticles(obs.x + 20, obs.y + 20, '#ff1744', 25);
                                zombies.splice(zIdx, 1);
                                obstacles.splice(obsIdx, 1);
                            }
                        });
                    }
                }
            });

            humans = humans.filter(h => h.x > cameraX - 50 && !h.eaten);
            obstacles = obstacles.filter(o => o.x > cameraX - 160);

            if (zombies.length === 0) {
                gameState = 'GAMEOVER';
            }

            particles.forEach(p => { p.x += p.vx; p.y += p.vy; p.life--; });
            particles = particles.filter(p => p.life > 0);
        }

        // Render Map Bãi Biển
        function drawBackground() {
            let skyGrad = ctx.createLinearGradient(0, 0, 0, 240);
            skyGrad.addColorStop(0, '#1976d2');
            skyGrad.addColorStop(1, '#64b5f6');
            ctx.fillStyle = skyGrad;
            ctx.fillRect(0, 0, canvas.width, 240);

            let seaGrad = ctx.createLinearGradient(0, 210, 0, 330);
            seaGrad.addColorStop(0, '#00838f');
            seaGrad.addColorStop(1, '#00acc1');
            ctx.fillStyle = seaGrad;
            ctx.fillRect(0, 210, canvas.width, 120);

            ctx.fillStyle = '#ffe082';
            ctx.fillRect(0, 290, canvas.width, 40);

            // Ground & Asphalt
            ctx.fillStyle = '#261c14';
            ctx.fillRect(0, groundY, canvas.width, canvas.height - groundY);
            ctx.fillStyle = '#37474f';
            ctx.fillRect(0, groundY, canvas.width, 12);
            ctx.fillStyle = '#455a64';
            ctx.fillRect(0, groundY + 12, canvas.width, canvas.height - groundY - 12);

            // Pits (Vách ngăn lúc cao lúc thấp)
            pits.forEach(p => {
                let drawX = p.x - cameraX;
                ctx.clearRect(drawX, groundY, p.width, canvas.height - groundY);
                ctx.fillStyle = '#1a100a';
                ctx.fillRect(drawX - 6, groundY, 6, canvas.height - groundY);
                ctx.fillRect(drawX + p.width, groundY, 6, canvas.height - groundY);
            });

            // Road Lines
            ctx.strokeStyle = '#fbc02d';
            ctx.lineWidth = 4;
            let dashWidth = 30;
            let dashGap = 20;
            let startX = - (cameraX % (dashWidth + dashGap));

            for (let x = startX; x < canvas.width; x += dashWidth + dashGap) {
                if (!isOverPit(x + cameraX)) {
                    ctx.beginPath();
                    ctx.moveTo(x, groundY + 45);
                    ctx.lineTo(x + dashWidth, groundY + 45);
                    ctx.stroke();
                }
            }

            // Hiệu ứng Sóng Thần phủ nước biển lên màn hình nếu đang kích hoạt
            if (tsunamiActive) {
                ctx.fillStyle = 'rgba(0, 150, 255, 0.25)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 28px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('🌊 TSUNAMI WAVE ACTIVE! 🌊', 400, 60);
            }
        }

        function drawZombie(z) {
            ctx.save();
            ctx.translate(z.x - cameraX, z.y);

            ctx.strokeStyle = '#1a237e'; ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.moveTo(-4, 10); ctx.lineTo(-4 + Math.sin(z.legAngle)*7, 20);
            ctx.moveTo(4, 10); ctx.lineTo(4 - Math.sin(z.legAngle)*7, 20);
            ctx.stroke();

            ctx.fillStyle = tsunamiActive ? '#00e5ff' : '#c62828'; 
            ctx.fillRect(-10, -2, 20, 14);
            ctx.fillStyle = '#76ba1b'; ctx.beginPath(); ctx.arc(0, -16, 16, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.arc(6, -18, 7, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#283593'; ctx.beginPath(); ctx.arc(8, -18, 3, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#1b5e20'; ctx.beginPath(); ctx.arc(6, -10, 5, 0, Math.PI); ctx.fill();
            ctx.fillStyle = '#ffffff'; ctx.fillRect(5, -10, 3, 3);

            ctx.restore();
        }

        function drawHuman(h) {
            ctx.save();
            ctx.translate(h.x - cameraX, h.y);
            ctx.fillStyle = '#ffcc80'; ctx.beginPath(); ctx.arc(0, -18, 8, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = h.gender === 'MALE' ? '#5d4037' : '#fbc02d'; ctx.beginPath(); ctx.arc(0, -21, 8, Math.PI, Math.PI*2); ctx.fill();
            ctx.fillStyle = h.gender === 'MALE' ? '#1e88e5' : '#e91e63'; ctx.fillRect(-6, -10, 12, 12);
            ctx.restore();
        }

        function drawBomb(o) {
            ctx.save();
            ctx.translate(o.x - cameraX + 20, o.y + 20);
            ctx.fillStyle = '#222'; ctx.beginPath(); ctx.arc(0, 0, 18, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#ff1744'; ctx.font = 'bold 12px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('💣', 0, 4);
            ctx.restore();
        }

        function drawCar(o) {
            ctx.save();
            ctx.translate(o.x - cameraX, o.y);
            ctx.fillStyle = '#d32f2f'; ctx.fillRect(0, 16, o.w, 24);
            ctx.fillStyle = '#b71c1c'; ctx.fillRect(15, 2, 55, 16);
            ctx.fillStyle = '#111'; ctx.beginPath(); ctx.arc(20, 40, 9, 0, Math.PI*2); ctx.arc(o.w - 20, 40, 9, 0, Math.PI*2); ctx.fill();
            
            ctx.fillStyle = '#111'; ctx.fillRect(15, -50, 60, 28);
            ctx.fillStyle = '#ff3d00'; ctx.font = 'bold 16px sans-serif'; ctx.textAlign = 'center';
            ctx.fillText(`0/${o.reqZombies}`, 45, -30);
            ctx.restore();
        }

        function draw() {
            drawBackground();

            if (gameState === 'START') {
                ctx.fillStyle = 'rgba(0,0,0,0.6)'; ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#76ba1b'; ctx.font = 'bold 36px sans-serif'; ctx.textAlign = 'center';
                ctx.fillText('ZOMBIE TSUNAMI', 400, 180);
                ctx.fillStyle = '#ffffff'; ctx.font = '20px sans-serif';
                ctx.fillText('Nhấn Space / Chạm màn hình để bắt đầu!', 400, 230);
                return;
            }

            humans.forEach(h => drawHuman(h));
            obstacles.forEach(o => {
                if (o.type === 'BOMB') drawBomb(o);
                else if (o.type === 'CAR') drawCar(o);
                else if (o.type === 'BUS') {
                    ctx.save();
                    ctx.translate(o.x - cameraX, o.y);
                    ctx.fillStyle = '#fbc02d'; ctx.fillRect(0, 0, o.w, 55);
                    ctx.fillStyle = '#111'; ctx.fillRect(35, -45, 60, 28);
                    ctx.fillStyle = '#ff3d00'; ctx.font = 'bold 16px sans-serif'; ctx.textAlign = 'center';
                    ctx.fillText(`0/${o.reqZombies}`, 65, -25);
                    ctx.restore();
                }
            });

            zombies.forEach(z => drawZombie(z));

            particles.forEach(p => {
                ctx.fillStyle = p.color;
                ctx.fillRect(p.x - cameraX, p.y, 4, 4);
            });

            // HUD UI
            ctx.fillStyle = 'rgba(0,0,0,0.5)'; ctx.fillRect(15, 12, 160, 70);
            ctx.fillStyle = '#fbc02d'; ctx.font = 'bold 22px sans-serif'; ctx.textAlign = 'left'; ctx.fillText(`🪙 ${coins}`, 25, 40);
            ctx.fillStyle = '#76ba1b'; ctx.fillText(`🧠 x${zombies.length}`, 25, 70);

            if (gameState === 'GAMEOVER') {
                ctx.fillStyle = 'rgba(0,0,0,0.85)'; ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#ff1744'; ctx.font = 'bold 42px sans-serif'; ctx.textAlign = 'center';
                ctx.fillText('GAME OVER', 400, 190);
                ctx.fillStyle = '#ffffff'; ctx.font = '22px sans-serif';
                ctx.fillText(`Số người nuốt chửng: ${score}`, 400, 240);
                ctx.fillText('Nhấn Space / Chạm để chơi lại', 400, 260);
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
