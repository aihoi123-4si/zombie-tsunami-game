
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Zombie Tsunami Fixed City & Safe Spawning HD", layout="centered")

st.markdown("<h1 style='text-align: center; color: #76ba1b;'>🧟 ZOMBIE TSUNAMI - DUAL MAPS FIX 🏙️🌊</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Đã sửa lỗi Map Thành Phố, giảm tỷ lệ Trực Thăng cực hiếm và lọc tuyệt đối không cho vật phẩm/xe xuất hiện trên hố!</p>", unsafe_allow_html=True)

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
        const defaultGroundY = 330;

        // Quản lý Map (BEACH / CITY)
        let currentMap = Math.random() > 0.5 ? 'BEACH' : 'CITY';
        let mapBannerTimer = 0;

        // Zombie Horde
        let zombies = [{ x: 180, y: defaultGroundY - 20, vy: 0, isGrounded: true, legAngle: 0 }];

        let humans = [];
        let obstacles = [];
        let pits = [];
        let powerups = [];
        let particles = [];
        let bgOffset = 0;

        // Trạng thái Sóng Thần
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
                        z.vy = -13.5 - (idx * 0.05);
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
            currentMap = Math.random() > 0.5 ? 'BEACH' : 'CITY';
            mapBannerTimer = 120;
            zombies = [{ x: 180, y: defaultGroundY - 20, vy: 0, isGrounded: true, legAngle: 0 }];
            humans = [];
            obstacles = [];
            pits = [];
            powerups = [];
            particles = [];
            tsunamiActive = false;
            tsunamiTimer = 0;
        }

        function isOverPit(x, width = 50) {
            return pits.some(p => (x + width > p.x) && (x < p.x + p.width));
        }

        function update() {
            if (gameState !== 'PLAYING') return;

            frame++;
            speed = 4.5 + Math.floor(frame / 600) * 0.4;
            bgOffset += speed;

            // Đổi map sau mỗi 20 giây (1200 frames)
            if (frame > 0 && frame % 1200 === 0) {
                currentMap = currentMap === 'BEACH' ? 'CITY' : 'BEACH';
                mapBannerTimer = 120;
            }
            if (mapBannerTimer > 0) mapBannerTimer--;

            // Sóng Thần
            if (tsunamiActive) {
                tsunamiTimer--;
                if (tsunamiTimer <= 0) tsunamiActive = false;
            }

            // Spawn Hố (Vách ngăn)
            if (frame % 230 === 0 && Math.random() > 0.35) {
                let pitWidth = 80 + Math.random() * 70;
                let pitDepthOffset = Math.floor(Math.random() * 20);
                pits.push({ x: 850, width: pitWidth, depthOffset: pitDepthOffset });
            }

            // Spawn Vòng Tròn Sóng Thần (Cam kết không nằm trên hố)
            if (frame % 950 === 0 && !tsunamiActive && Math.random() < 0.5) {
                let spawnX = 850;
                if (!isOverPit(spawnX, 40)) {
                    powerups.push({ x: spawnX, y: defaultGroundY - 60, r: 18, collected: false });
                }
            }

            // Spawn Chướng ngại vật, Phương tiện & Người (Cam kết KHÔNG BAO GIỜ nằm trên hố)
            if (frame % 115 === 0) {
                let spawnX = 850;
                if (!isOverPit(spawnX, 150)) {
                    let rand = Math.random();
                    if (rand < 0.32) {
                        let gender = Math.random() > 0.5 ? 'MALE' : 'FEMALE';
                        humans.push({ x: spawnX, y: defaultGroundY - 20, gender: gender, eaten: false, armAngle: 0 });
                    } else if (rand < 0.65) {
                        // Xe Hơi (4 zombie)
                        obstacles.push({ x: spawnX, y: defaultGroundY - 45, w: 95, h: 45, type: 'CAR', reqZombies: 4, peopleInside: 3, cooldown: 0 });
                    } else if (rand < 0.82) {
                        // Xe Buýt (6 zombie)
                        obstacles.push({ x: spawnX, y: defaultGroundY - 65, w: 135, h: 65, type: 'BUS', reqZombies: 6, peopleInside: 6, cooldown: 0 });
                    } else if (rand < 0.87) {
                        // TRỰC THĂNG QUÂN SỰ (Cực kỳ hiếm, ít hơn xe buýt - 8 zombie)
                        obstacles.push({ x: spawnX, y: defaultGroundY - 90, w: 140, h: 60, type: 'HELI', reqZombies: 8, peopleInside: 8, cooldown: 0 });
                    } else {
                        // Bom 3D
                        obstacles.push({ x: spawnX, y: defaultGroundY - 40, w: 40, h: 40, type: 'BOMB' });
                    }
                }
            }

            pits.forEach(p => p.x -= speed);
            pits = pits.filter(p => p.x + p.width > -50);

            // Update Vòng Tròn Sóng Thần
            powerups.forEach((pw) => {
                pw.x -= speed;
                let leader = zombies[0];
                if (!pw.collected && leader && Math.abs(leader.x - pw.x) < 30 && Math.abs(leader.y - pw.y) < 35) {
                    pw.collected = true;
                    tsunamiActive = true;
                    tsunamiTimer = 260;
                    addParticles(pw.x, pw.y, '#00e5ff', 30);
                }
            });
            powerups = powerups.filter(p => p.x > -50 && !p.collected);

            // Update Zombies
            for (let i = zombies.length - 1; i >= 0; i--) {
                let z = zombies[i];

                if (tsunamiActive) {
                    z.y = defaultGroundY - 110 + Math.sin(frame * 0.15 + i * 0.4) * 8;
                    z.vy = 0;
                    z.isGrounded = true;
                } else {
                    z.vy += gravity;
                    z.y += z.vy;

                    let onPit = isOverPit(z.x, 10);
                    let standingOnVehicle = false;

                    obstacles.forEach((obs) => {
                        if (obs.type === 'CAR' || obs.type === 'BUS' || obs.type === 'HELI') {
                            if (z.x >= obs.x - 8 && z.x <= obs.x + obs.w + 8) {
                                let roofY = obs.y - 18;
                                if (z.y >= roofY - 5 && z.y <= obs.y + 12 && z.vy >= 0) {
                                    z.y = roofY;
                                    z.vy = 0;
                                    z.isGrounded = true;
                                    standingOnVehicle = true;
                                }
                            }
                        }
                    });

                    if (!standingOnVehicle) {
                        if (!onPit && z.y >= defaultGroundY - 20) {
                            z.y = defaultGroundY - 20;
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

            if (zombies.length === 0) {
                gameState = 'GAMEOVER';
                return;
            }

            // Update Humans
            humans.forEach((h) => {
                h.x -= speed;
                h.armAngle += 0.15;
                let leader = zombies[0];
                if (!h.eaten && leader && Math.abs(leader.x - h.x) < 35 && Math.abs(leader.y - h.y) < 60) {
                    h.eaten = true;
                    score += 1;
                    coins += 5;
                    addParticles(h.x, h.y - 10, '#76ba1b', 15);
                    if (zombies.length < 30) {
                        let tail = zombies[zombies.length - 1];
                        zombies.push({ x: tail.x - 22, y: tail.y, vy: 0, isGrounded: tail.isGrounded, legAngle: 0 });
                    }
                }
            });

            // Update Obstacles
            obstacles.forEach((obs, obsIdx) => {
                obs.x -= speed;
                if (obs.cooldown > 0) obs.cooldown--;

                if (tsunamiActive) {
                    if (Math.abs(zombies[0].x - obs.x) < 110) {
                        addParticles(obs.x + obs.w/2, obs.y, '#00e5ff', 30);
                        addParticles(obs.x + obs.w/2, obs.y, '#76ba1b', 20);

                        if (obs.type === 'CAR' || obs.type === 'BUS' || obs.type === 'HELI') {
                            score += obs.peopleInside;
                            coins += obs.peopleInside * 10;
                            for (let k = 0; k < obs.peopleInside; k++) {
                                if (zombies.length < 30) {
                                    let tail = zombies[zombies.length - 1];
                                    zombies.push({ x: tail.x - 22, y: tail.y, vy: 0, isGrounded: true, legAngle: 0 });
                                }
                            }
                        } else if (obs.type === 'BOMB') {
                            score += 2;
                        }

                        obstacles.splice(obsIdx, 1);
                    }
                } else {
                    if (obs.type === 'CAR' || obs.type === 'BUS' || obs.type === 'HELI') {
                        for (let i = zombies.length - 1; i >= 0; i--) {
                            let z = zombies[i];
                            if (z.x + 12 > obs.x && z.x - 12 < obs.x + 20 && z.y > obs.y + 10) {
                                if (zombies.length >= obs.reqZombies) {
                                    addParticles(obs.x + obs.w/2, obs.y + obs.h/2, '#ff9800', 35);
                                    score += obs.peopleInside;
                                    coins += obs.peopleInside * 10;
                                    for (let k = 0; k < obs.peopleInside; k++) {
                                        if (zombies.length < 30) {
                                            let tail = zombies[zombies.length - 1];
                                            zombies.push({ x: tail.x - 22, y: tail.y, vy: 0, isGrounded: tail.isGrounded, legAngle: 0 });
                                        }
                                    }
                                    obstacles.splice(obsIdx, 1);
                                    break;
                                } else {
                                    if (obs.cooldown === 0) {
                                        obs.cooldown = 20;
                                        addParticles(z.x, z.y, '#ff4444', 20);
                                        zombies.splice(i, 1);
                                        obs.x += 15;
                                        if (zombies.length === 0) {
                                            gameState = 'GAMEOVER';
                                            return;
                                        }
                                    }
                                }
                            }
                        }
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

            humans = humans.filter(h => h.x > -50 && !h.eaten);
            obstacles = obstacles.filter(o => o.x > -160);

            if (zombies.length === 0) {
                gameState = 'GAMEOVER';
            }

            particles.forEach(p => { p.x += p.vx; p.y += p.vy; p.life--; });
            particles = particles.filter(p => p.life > 0);
        }

        // --- MAP BÃI BIỂN (BEACH) ---
        function drawBeachMap() {
            let skyGrad = ctx.createLinearGradient(0, 0, 0, 240);
            skyGrad.addColorStop(0, '#1976d2'); skyGrad.addColorStop(1, '#64b5f6');
            ctx.fillStyle = skyGrad; ctx.fillRect(0, 0, canvas.width, 240);

            ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
            let cloudX = (300 - bgOffset * 0.2) % 900;
            if (cloudX < -100) cloudX += 900;
            ctx.beginPath();
            ctx.arc(cloudX, 60, 25, 0, Math.PI*2);
            ctx.arc(cloudX + 30, 50, 35, 0, Math.PI*2);
            ctx.arc(cloudX + 70, 60, 25, 0, Math.PI*2); ctx.fill();

            let seaGrad = ctx.createLinearGradient(0, 210, 0, 330);
            seaGrad.addColorStop(0, '#00838f'); seaGrad.addColorStop(1, '#00acc1');
            ctx.fillStyle = seaGrad; ctx.fillRect(0, 210, canvas.width, 120);

            ctx.fillStyle = '#ffe082'; ctx.fillRect(0, 290, canvas.width, 40);

            for (let hIdx = 0; hIdx < 3; hIdx++) {
                let houseX = (220 + hIdx * 280 - bgOffset * 0.6) % 900;
                if (houseX < -120) houseX += 900;
                ctx.fillStyle = '#e0f2f1'; ctx.fillRect(houseX, 200, 85, 90);
                ctx.fillStyle = '#8d6e63'; ctx.fillRect(houseX + 60, 150, 12, 30);
                ctx.fillStyle = '#e57373'; ctx.beginPath();
                ctx.moveTo(houseX - 10, 200); ctx.lineTo(houseX + 42, 145); ctx.lineTo(houseX + 95, 200); ctx.fill();
                ctx.fillStyle = '#81d4fa'; ctx.fillRect(houseX + 12, 215, 22, 22);
                ctx.fillStyle = '#6d4c41'; ctx.fillRect(houseX + 48, 240, 22, 50);
            }

            for (let tIdx = 0; tIdx < 2; tIdx++) {
                let treeX = (80 + tIdx * 450 - bgOffset * 0.8) % 900;
                if (treeX < -100) treeX += 900;
                ctx.fillStyle = '#5d4037'; ctx.fillRect(treeX, 180, 16, 120);
                ctx.fillStyle = '#2e7d32'; ctx.beginPath();
                ctx.arc(treeX - 20, 170, 28, 0, Math.PI*2); ctx.arc(treeX + 35, 170, 28, 0, Math.PI*2); ctx.arc(treeX + 8, 150, 32, 0, Math.PI*2); ctx.fill();
            }
        }

        // --- MAP THÀNH PHỐ (CITY SKYLINE - ĐÃ SỬA LỖI KÉO DÀI TỈ LỆ) ---
        function drawCityMap() {
            let skyGrad = ctx.createLinearGradient(0, 0, 0, 240);
            skyGrad.addColorStop(0, '#7986cb'); skyGrad.addColorStop(1, '#c5cae9');
            ctx.fillStyle = skyGrad; ctx.fillRect(0, 0, canvas.width, 240);

            // Mây thành phố
            ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
            let cloudX = (200 - bgOffset * 0.15) % 900;
            if (cloudX < -100) cloudX += 900;
            ctx.beginPath();
            ctx.arc(cloudX, 55, 25, 0, Math.PI*2); ctx.arc(cloudX + 35, 48, 32, 0, Math.PI*2); ctx.arc(cloudX + 70, 55, 25, 0, Math.PI*2); ctx.fill();

            // Các tòa cao ốc chọc trời phía xa (Tỷ lệ chuẩn, không kéo dài)
            for (let b = 0; b < 6; b++) {
                let bX = (b * 160 - bgOffset * 0.25) % 960;
                if (bX < -160) bX += 960;
                ctx.fillStyle = b % 2 === 0 ? '#5c6bc0' : '#7986cb';
                ctx.fillRect(bX, 80 + (b % 2)*25, 120, 210);

                // Cửa sổ cao ốc
                ctx.fillStyle = 'rgba(255, 255, 255, 0.35)';
                for(let w = 0; w < 3; w++) {
                    ctx.fillRect(bX + 16 + w*32, 100 + (b % 2)*25, 14, 160);
                }
            }

            // Cầu vượt cong thành phố (Overpass Bridge) đúng tỷ lệ
            let bridgeX = (300 - bgOffset * 0.5) % 900;
            if (bridgeX < -250) bridgeX += 900;
            ctx.fillStyle = '#455a64'; ctx.fillRect(bridgeX + 90, 180, 24, 120); // Trụ cầu
            ctx.fillStyle = '#546e7a';
            ctx.beginPath();
            ctx.moveTo(bridgeX - 120, 205);
            ctx.quadraticCurveTo(bridgeX + 100, 145, bridgeX + 320, 215);
            ctx.lineTo(bridgeX + 320, 235);
            ctx.quadraticCurveTo(bridgeX + 100, 165, bridgeX - 120, 225);
            ctx.fill();

            // Người kêu cứu trên cầu
            ctx.fillStyle = '#ffcc80'; ctx.beginPath(); ctx.arc(bridgeX + 105, 145, 6, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#e91e63'; ctx.fillRect(bridgeX + 102, 151, 6, 10);

            // Tòa nhà gạch đỏ cổ kính bên trái có cầu thang thoát hiểm
            for (let r = 0; r < 2; r++) {
                let redX = (r * 500 - bgOffset * 0.7) % 900;
                if (redX < -220) redX += 900;
                ctx.fillStyle = '#795548'; ctx.fillRect(redX, 130, 170, 180);
                ctx.fillStyle = '#212121';
                for(let row=0; row<2; row++) {
                    for(let col=0; col<3; col++) {
                        ctx.fillRect(redX + 18 + col*48, 150 + row*55, 26, 38);
                    }
                }
                // Cầu thang thoát hiểm
                ctx.strokeStyle = '#111'; ctx.lineWidth = 3;
                ctx.strokeRect(redX + 125, 150, 32, 100);
                ctx.beginPath(); ctx.moveTo(redX + 125, 180); ctx.lineTo(redX + 157, 180); ctx.moveTo(redX + 125, 210); ctx.lineTo(redX + 157, 210); ctx.stroke();
            }
        }

        // Render Background & Mặt đường
        function drawBackground() {
            if (currentMap === 'BEACH') {
                drawBeachMap();
            } else {
                drawCityMap();
            }

            // Mặt Đường & Đất
            ctx.fillStyle = '#261c14';
            ctx.fillRect(0, defaultGroundY, canvas.width, canvas.height - defaultGroundY);
            ctx.fillStyle = '#37474f';
            ctx.fillRect(0, defaultGroundY, canvas.width, 12);
            ctx.fillStyle = '#455a64';
            ctx.fillRect(0, defaultGroundY + 12, canvas.width, canvas.height - defaultGroundY - 12);

            // Hố / Vách ngăn
            pits.forEach(p => {
                let depth = defaultGroundY + (p.depthOffset || 0);
                ctx.clearRect(p.x, depth, p.width, canvas.height - depth);
                ctx.fillStyle = '#1a100a';
                ctx.fillRect(p.x - 6, depth, 6, canvas.height - depth);
                ctx.fillRect(p.x + p.width, depth, 6, canvas.height - depth);
            });

            // Vạch kẻ đường
            ctx.strokeStyle = '#fbc02d'; ctx.lineWidth = 4;
            let dashWidth = 30; let dashGap = 20;
            let startX = - (bgOffset % (dashWidth + dashGap));
            for (let x = startX; x < canvas.width; x += dashWidth + dashGap) {
                if (!isOverPit(x)) {
                    ctx.beginPath(); ctx.moveTo(x, defaultGroundY + 45); ctx.lineTo(x + dashWidth, defaultGroundY + 45); ctx.stroke();
                }
            }

            // Sóng Thần
            if (tsunamiActive) {
                let waveX = zombies[0] ? zombies[0].x + 40 : 250;
                let waveGrad = ctx.createLinearGradient(0, 100, 0, defaultGroundY + 50);
                waveGrad.addColorStop(0, '#00b0ff'); waveGrad.addColorStop(0.5, '#0077c2'); waveGrad.addColorStop(1, '#002984');
                ctx.fillStyle = waveGrad;
                ctx.beginPath();
                ctx.moveTo(-100, defaultGroundY + 50); ctx.lineTo(-100, 180);
                ctx.bezierCurveTo(waveX - 120, 160, waveX - 40, 130, waveX, 170);
                ctx.bezierCurveTo(waveX + 30, 200, waveX + 50, 270, waveX + 20, defaultGroundY + 50);
                ctx.closePath(); ctx.fill();

                ctx.fillStyle = '#ffffff';
                for (let f = 0; f < 18; f++) {
                    let foamX = waveX - 40 + Math.sin(frame * 0.3 + f) * 25;
                    let foamY = 165 + Math.cos(frame * 0.2 + f) * 15;
                    let foamR = 10 + (f % 5) * 4;
                    ctx.beginPath(); ctx.arc(foamX, foamY, foamR, 0, Math.PI * 2); ctx.fill();
                }
            }

            // Banner đổi map
            if (mapBannerTimer > 0) {
                ctx.fillStyle = 'rgba(0,0,0,0.75)';
                ctx.fillRect(190, 15, 420, 45);
                ctx.fillStyle = '#fbc02d';
                ctx.font = 'bold 22px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText(currentMap === 'BEACH' ? '🌊 MAP: TROPICAL BEACH 🌊' : '🏙️ MAP: CITY SKYLINE 🏙️', 400, 45);
            }
        }

        function drawPowerup(pw) {
            ctx.save();
            ctx.translate(pw.x, pw.y + Math.sin(frame * 0.1) * 5);
            ctx.fillStyle = '#ffee58'; ctx.beginPath(); ctx.arc(0, 0, pw.r + 3, 0, Math.PI * 2); ctx.fill();
            let sphereGrad = ctx.createRadialGradient(-4, -4, 2, 0, 0, pw.r);
            sphereGrad.addColorStop(0, '#80d8ff'); sphereGrad.addColorStop(0.7, '#0091ea'); sphereGrad.addColorStop(1, '#01579b');
            ctx.fillStyle = sphereGrad; ctx.beginPath(); ctx.arc(0, 0, pw.r, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#ffffff'; ctx.font = 'bold 16px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('🌊', 0, 6);
            ctx.restore();
        }

        function drawZombie(z) {
            ctx.save();
            ctx.translate(z.x, z.y);
            ctx.strokeStyle = '#76ba1b'; ctx.lineWidth = 5;
            ctx.beginPath(); ctx.moveTo(-4, 8); ctx.lineTo(-4 + Math.sin(z.legAngle)*8, 20); ctx.moveTo(4, 8); ctx.lineTo(4 - Math.sin(z.legAngle)*8, 20); ctx.stroke();
            ctx.fillStyle = '#fbc02d'; ctx.fillRect(-8, 4, 16, 8);
            ctx.fillStyle = '#8d2626'; ctx.fillRect(-9, -4, 18, 10);
            ctx.fillStyle = '#76ba1b'; ctx.beginPath(); ctx.arc(0, -16, 17, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#000000'; ctx.beginPath(); ctx.arc(7, -18, 10, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.arc(7, -18, 8.5, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#d32f2f'; ctx.beginPath(); ctx.arc(9, -18, 4, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#000000'; ctx.beginPath(); ctx.arc(9.5, -18, 2, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#1b5e20'; ctx.beginPath(); ctx.arc(8, -8, 6, 0, Math.PI); ctx.fill();
            ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.moveTo(5, -8); ctx.lineTo(7, -4); ctx.lineTo(9, -8); ctx.fill();
            ctx.strokeStyle = '#76ba1b'; ctx.lineWidth = 4;
            ctx.beginPath(); ctx.moveTo(2, -2); ctx.lineTo(14, 2); ctx.stroke();
            ctx.restore();
        }

        function drawHuman(h) {
            ctx.save();
            ctx.translate(h.x, h.y);
            ctx.fillStyle = '#ffcc80'; ctx.beginPath(); ctx.arc(0, -18, 8, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = h.gender === 'MALE' ? '#5d4037' : '#fbc02d'; ctx.beginPath(); ctx.arc(0, -21, 8, Math.PI, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#000'; ctx.beginPath(); ctx.arc(-3, -18, 1.5, 0, Math.PI*2); ctx.arc(3, -18, 1.5, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = h.gender === 'MALE' ? '#1e88e5' : '#e91e63'; ctx.fillRect(-6, -10, 12, 12);
            ctx.restore();
        }

        function drawBomb(o) {
            ctx.save();
            ctx.translate(o.x + 20, o.y + 20);
            let bombGrad = ctx.createRadialGradient(-4, -4, 2, 0, 0, 18);
            bombGrad.addColorStop(0, '#666'); bombGrad.addColorStop(0.6, '#222'); bombGrad.addColorStop(1, '#000');
            ctx.fillStyle = bombGrad; ctx.beginPath(); ctx.arc(0, 0, 18, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#ff1744'; ctx.font = 'bold 12px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('💣', 0, 4);
            ctx.restore();
        }

        function drawCar(o) {
            ctx.save();
            ctx.translate(o.x, o.y);
            ctx.fillStyle = '#d32f2f'; ctx.fillRect(0, 18, o.w, 20);
            ctx.fillStyle = '#b71c1c'; ctx.fillRect(16, 4, 60, 14);
            ctx.fillStyle = '#81d4fa'; ctx.fillRect(22, 7, 20, 10); ctx.fillRect(48, 7, 22, 10);
            ctx.fillStyle = '#ffeb3b'; ctx.fillRect(0, 22, 4, 8);
            ctx.fillStyle = '#111'; ctx.beginPath(); ctx.arc(22, 38, 9, 0, Math.PI*2); ctx.arc(o.w - 22, 38, 9, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#111'; ctx.fillRect(18, -48, 58, 26);
            ctx.fillStyle = '#ff3d00'; ctx.font = 'bold 16px sans-serif'; ctx.textAlign = 'center';
            ctx.fillText(`0/${o.reqZombies}`, 47, -30);
            ctx.restore();
        }

        function drawBus(o) {
            ctx.save();
            ctx.translate(o.x, o.y);
            ctx.fillStyle = '#fbc02d'; ctx.fillRect(0, 0, o.w, 54);
            ctx.fillStyle = '#f57f17'; ctx.fillRect(0, 32, o.w, 6);
            ctx.fillStyle = '#81d4fa';
            for(let k=0; k<4; k++) ctx.fillRect(12 + (k * 28), 8, 20, 18);
            ctx.fillStyle = '#111'; ctx.beginPath(); ctx.arc(26, 54, 10, 0, Math.PI*2); ctx.arc(o.w - 26, 54, 10, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#111'; ctx.fillRect(38, -45, 60, 28);
            ctx.fillStyle = '#ff3d00'; ctx.font = 'bold 16px sans-serif'; ctx.textAlign = 'center';
            ctx.fillText(`0/${o.reqZombies}`, 68, -25);
            ctx.restore();
        }

        function drawHelicopter(o) {
            ctx.save();
            ctx.translate(o.x, o.y);
            ctx.fillStyle = '#3e4a36'; ctx.beginPath(); ctx.ellipse(70, 30, 60, 24, 0, 0, Math.PI * 2); ctx.fill();
            ctx.fillRect(110, 22, 45, 12);
            ctx.fillStyle = '#111'; ctx.fillRect(150, 10, 6, 30);
            ctx.fillStyle = '#81d4fa'; ctx.fillRect(25, 18, 28, 16); ctx.fillRect(60, 20, 14, 12); ctx.fillRect(80, 20, 14, 12);
            ctx.fillStyle = '#111'; ctx.fillRect(65, 0, 8, 10);
            let bladeW = 110 + Math.sin(frame * 0.5) * 20;
            ctx.fillRect(70 - bladeW/2, 0, bladeW, 4);
            ctx.strokeStyle = '#222'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(35, 50); ctx.lineTo(35, 58); ctx.lineTo(105, 58); ctx.lineTo(105, 50); ctx.stroke();
            ctx.fillStyle = '#ffffff'; ctx.font = 'bold 11px monospace'; ctx.fillText('T-315', 70, 34);
            ctx.fillStyle = '#111'; ctx.fillRect(40, -42, 60, 28);
            ctx.fillStyle = '#ff3d00'; ctx.font = 'bold 16px sans-serif'; ctx.textAlign = 'center';
            ctx.fillText(`0/${o.reqZombies}`, 70, -22);
            ctx.restore();
        }

        function draw() {
            drawBackground();

            if (gameState === 'START') {
                ctx.fillStyle = 'rgba(0,0,0,0.6)'; ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#76ba1b'; ctx.font = 'bold 36px sans-serif'; ctx.textAlign = 'center';
                ctx.fillText('ZOMBIE TSUNAMI', 400, 180);
                ctx.fillStyle = '#ffffff'; ctx.font = '20px sans-serif';
                ctx.fillText('Nhấn Space / Chạm màn hình để bắt đầu chơi!', 400, 230);
                return;
            }

            powerups.forEach(pw => drawPowerup(pw));
            humans.forEach(h => drawHuman(h));

            obstacles.forEach(o => {
                if (o.type === 'BOMB') drawBomb(o);
                else if (o.type === 'CAR') drawCar(o);
                else if (o.type === 'BUS') drawBus(o);
                else if (o.type === 'HELI') drawHelicopter(o);
            });

            zombies.forEach(z => drawZombie(z));

            particles.forEach(p => {
                ctx.fillStyle = p.color;
                ctx.fillRect(p.x, p.y, 4, 4);
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
