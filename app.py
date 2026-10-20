import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Zombie Tsunami Solid Vehicles & Rare Tsunami", layout="centered")

st.markdown("<h1 style='text-align: center; color: #76ba1b;'>🧟 ZOMBIE TSUNAMI - SOLID VEHICLES 🧟</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Xe cộ là khối cứng không đi xuyên qua được! Vách ngăn cao thấp ngẫu nhiên và Vòng tròn Sóng Thần cực hiếm!</p>", unsafe_allow_html=True)

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

        // Zombie Horde
        let zombies = [{ x: 160, y: defaultGroundY - 20, vy: 0, isGrounded: true, legAngle: 0 }];

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
            zombies = [{ x: 160, y: defaultGroundY - 20, vy: 0, isGrounded: true, legAngle: 0 }];
            humans = [];
            obstacles = [];
            pits = [];
            powerups = [];
            particles = [];
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

            // Xử lý Sóng Thần
            if (tsunamiActive) {
                tsunamiTimer--;
                if (tsunamiTimer <= 0) tsunamiActive = false;
            }

            // Spawn Hố / Vách Ngăn Cao Thấp Ngẫu Nhiên
            if (frame % 230 === 0 && Math.random() > 0.35) {
                let pitWidth = 80 + Math.random() * 75; // Bề rộng hố ngẫu nhiên
                let pitDepthOffset = Math.floor(Math.random() * 20); // Độ sâu/cao ngẫu nhiên
                pits.push({ x: 850, width: pitWidth, depthOffset: pitDepthOffset });
            }

            // Spawn Vòng Tròn Bổ Trợ Sóng Thần (HIẾM HƠN)
            if (frame % 850 === 0 && !tsunamiActive && Math.random() < 0.6) {
                let spawnX = 850;
                if (!isOverPit(spawnX)) {
                    powerups.push({ x: spawnX, y: defaultGroundY - 60, r: 18, collected: false });
                }
            }

            // Spawn Chướng ngại vật & Người
            if (frame % 115 === 0) {
                let spawnX = 850;
                if (!isOverPit(spawnX) && !isOverPit(spawnX + 130)) {
                    let rand = Math.random();
                    if (rand < 0.3) {
                        let gender = Math.random() > 0.5 ? 'MALE' : 'FEMALE';
                        humans.push({ x: spawnX, y: defaultGroundY - 20, gender: gender, eaten: false, armAngle: 0 });
                    } else if (rand < 0.65) {
                        // Xe Hơi (Cần 4 zombie)
                        obstacles.push({ x: spawnX, y: defaultGroundY - 45, w: 95, h: 45, type: 'CAR', reqZombies: 4, peopleInside: 3, cooldown: 0 });
                    } else if (rand < 0.85) {
                        // Xe Buýt (Cần 8 zombie)
                        obstacles.push({ x: spawnX, y: defaultGroundY - 65, w: 135, h: 65, type: 'BUS', reqZombies: 8, peopleInside: 6, cooldown: 0 });
                    } else {
                        // Bom 3D
                        obstacles.push({ x: spawnX, y: defaultGroundY - 40, w: 40, h: 40, type: 'BOMB' });
                    }
                }
            }

            pits.forEach(p => p.x -= speed);
            pits = pits.filter(p => p.x + p.width > -50);

            // Update Vòng Tròn Bổ Trợ Sóng Thần
            powerups.forEach((pw) => {
                pw.x -= speed;
                let leader = zombies[0];
                if (!pw.collected && leader && Math.abs(leader.x - pw.x) < 30 && Math.abs(leader.y - pw.y) < 35) {
                    pw.collected = true;
                    tsunamiActive = true;
                    tsunamiTimer = 240;
                    addParticles(pw.x, pw.y, '#00e5ff', 30);
                    for(let k=0; k<3; k++) {
                        if (zombies.length < 20) {
                            let tail = zombies[zombies.length - 1];
                            zombies.push({ x: tail.x - 24, y: tail.y, vy: 0, isGrounded: true, legAngle: 0 });
                        }
                    }
                }
            });
            powerups = powerups.filter(p => p.x > -50 && !p.collected);

            // Update Zombies & Physics (Xe là khối rắn SOLID BLOCK)
            for (let i = zombies.length - 1; i >= 0; i--) {
                let z = zombies[i];

                if (tsunamiActive) {
                    z.y = defaultGroundY - 110 + Math.sin(frame * 0.15 + i * 0.4) * 8;
                    z.vy = 0;
                    z.isGrounded = true;
                } else {
                    z.vy += gravity;
                    z.y += z.vy;

                    let onPit = isOverPit(z.x);
                    let standingOnVehicle = false;

                    // Kiểm tra nhảy đáp lên mui xe
                    obstacles.forEach((obs) => {
                        if (obs.type === 'CAR' || obs.type === 'BUS') {
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

                // Zombie rơi hố -> trừ zombie
                if (z.y > canvas.height + 30) {
                    addParticles(z.x, canvas.height - 10, '#76ba1b', 10);
                    zombies.splice(i, 1);
                }
            }

            // TỰ ĐỘNG THUA NGAY KHI HẾT ZOMBIE
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
                    addParticles(h.x, h.y, '#76ba1b', 12);
                    if (zombies.length < 25) {
                        let tail = zombies[zombies.length - 1];
                        zombies.push({ x: tail.x - 24, y: tail.y, vy: 0, isGrounded: tail.isGrounded, legAngle: 0 });
                    }
                }
            });

            // Update Obstacles & Xử lý khối xe vững chắc (CHỐNG ĐI XUYÊN)
            obstacles.forEach((obs, obsIdx) => {
                obs.x -= speed;
                if (obs.cooldown > 0) obs.cooldown--;

                if (tsunamiActive) {
                    if (Math.abs(zombies[0].x - obs.x) < 100) {
                        addParticles(obs.x + obs.w/2, obs.y, '#00e5ff', 25);
                        obstacles.splice(obsIdx, 1);
                        score += 5;
                        coins += 10;
                    }
                } else {
                    if (obs.type === 'CAR' || obs.type === 'BUS') {
                        // Kiểm tra va chạm phía trước xe (Frontal Collision)
                        for (let i = zombies.length - 1; i >= 0; i--) {
                            let z = zombies[i];
                            // Nếu zombie tông thẳng vào mặt trước/thân xe (không nằm trên nóc)
                            if (z.x + 12 > obs.x && z.x - 12 < obs.x + 20 && z.y > obs.y + 10) {
                                if (zombies.length >= obs.reqZombies) {
                                    // Đủ Zombie -> Phá xe thành công!
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
                                    break;
                                } else {
                                    // Không đủ Zombie -> Xe chặn cứng (Solid Block) & Mất 1 zombie!
                                    if (obs.cooldown === 0) {
                                        obs.cooldown = 20; // Tránh mất dồn liên tục trong 1 frame
                                        addParticles(z.x, z.y, '#ff4444', 20);
                                        zombies.splice(i, 1); // Loại bỏ zombie va chạm
                                        // Đẩy xe lùi lại nhẹ để thể hiện lực cản
                                        obs.x += 15;
                                        // Kiểm tra nếu hết zombie -> Thua ngay!
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

        // Render Map
        function drawBackground() {
            let skyGrad = ctx.createLinearGradient(0, 0, 0, 240);
            skyGrad.addColorStop(0, '#1976d2');
            skyGrad.addColorStop(1, '#64b5f6');
            ctx.fillStyle = skyGrad;
            ctx.fillRect(0, 0, canvas.width, 240);

            // Mây & Chim
            ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
            let cloudX = (300 - bgOffset * 0.2) % 900;
            if (cloudX < -100) cloudX += 900;
            ctx.beginPath();
            ctx.arc(cloudX, 60, 25, 0, Math.PI*2);
            ctx.arc(cloudX + 30, 50, 35, 0, Math.PI*2);
            ctx.arc(cloudX + 70, 60, 25, 0, Math.PI*2);
            ctx.fill();

            // Sea
            let seaGrad = ctx.createLinearGradient(0, 210, 0, 330);
            seaGrad.addColorStop(0, '#00838f');
            seaGrad.addColorStop(1, '#00acc1');
            ctx.fillStyle = seaGrad;
            ctx.fillRect(0, 210, canvas.width, 120);

            // Beach Sand
            ctx.fillStyle = '#ffe082';
            ctx.fillRect(0, 290, canvas.width, 40);

            // Nhà Mái Đỏ
            for (let hIdx = 0; hIdx < 3; hIdx++) {
                let houseX = (220 + hIdx * 280 - bgOffset * 0.6) % 900;
                if (houseX < -120) houseX += 900;
                ctx.fillStyle = '#e0f2f1'; ctx.fillRect(houseX, 210, 80, 80);
                ctx.fillStyle = '#e57373'; ctx.beginPath();
                ctx.moveTo(houseX - 10, 210); ctx.lineTo(houseX + 40, 160); ctx.lineTo(houseX + 90, 210); ctx.fill();
            }

            // Cây Dừa
            for (let tIdx = 0; tIdx < 2; tIdx++) {
                let treeX = (80 + tIdx * 450 - bgOffset * 0.8) % 900;
                if (treeX < -100) treeX += 900;
                ctx.fillStyle = '#5d4037'; ctx.fillRect(treeX, 180, 16, 120);
                ctx.fillStyle = '#2e7d32'; ctx.beginPath();
                ctx.arc(treeX - 20, 170, 28, 0, Math.PI*2);
                ctx.arc(treeX + 35, 170, 28, 0, Math.PI*2);
                ctx.arc(treeX + 8, 150, 32, 0, Math.PI*2); ctx.fill();
            }

            // Ground & Asphalt
            ctx.fillStyle = '#261c14';
            ctx.fillRect(0, defaultGroundY, canvas.width, canvas.height - defaultGroundY);
            ctx.fillStyle = '#37474f';
            ctx.fillRect(0, defaultGroundY, canvas.width, 12);
            ctx.fillStyle = '#455a64';
            ctx.fillRect(0, defaultGroundY + 12, canvas.width, canvas.height - defaultGroundY - 12);

            // Cut Pits (Vách ngăn cao thấp ngẫu nhiên)
            pits.forEach(p => {
                let depth = defaultGroundY + (p.depthOffset || 0);
                ctx.clearRect(p.x, depth, p.width, canvas.height - depth);
                ctx.fillStyle = '#1a100a';
                ctx.fillRect(p.x - 6, depth, 6, canvas.height - depth);
                ctx.fillRect(p.x + p.width, depth, 6, canvas.height - depth);
            });

            // Road Lines
            ctx.strokeStyle = '#fbc02d'; ctx.lineWidth = 4;
            let dashWidth = 30; let dashGap = 20;
            let startX = - (bgOffset % (dashWidth + dashGap));
            for (let x = startX; x < canvas.width; x += dashWidth + dashGap) {
                if (!isOverPit(x)) {
                    ctx.beginPath(); ctx.moveTo(x, defaultGroundY + 45); ctx.lineTo(x + dashWidth, defaultGroundY + 45); ctx.stroke();
                }
            }

            // Hiệu ứng Sóng Thần
            if (tsunamiActive) {
                let waveX = zombies[0] ? zombies[0].x + 40 : 250;
                let waveGrad = ctx.createLinearGradient(0, 100, 0, defaultGroundY + 50);
                waveGrad.addColorStop(0, '#00b0ff');
                waveGrad.addColorStop(0.5, '#0077c2');
                waveGrad.addColorStop(1, '#002984');
                ctx.fillStyle = waveGrad;

                ctx.beginPath();
                ctx.moveTo(-100, defaultGroundY + 50);
                ctx.lineTo(-100, 180);
                ctx.bezierCurveTo(waveX - 120, 160, waveX - 40, 130, waveX, 170);
                ctx.bezierCurveTo(waveX + 30, 200, waveX + 50, 270, waveX + 20, defaultGroundY + 50);
                ctx.closePath();
                ctx.fill();

                // Bọt Nước Trắng
                ctx.fillStyle = '#ffffff';
                for (let f = 0; f < 18; f++) {
                    let foamX = waveX - 40 + Math.sin(frame * 0.3 + f) * 25;
                    let foamY = 165 + Math.cos(frame * 0.2 + f) * 15;
                    let foamR = 10 + (f % 5) * 4;
                    ctx.beginPath(); ctx.arc(foamX, foamY, foamR, 0, Math.PI * 2); ctx.fill();
                }
            }
        }

        // Vẽ Vòng Tròn Bổ Trợ Sóng Thần (Sphere)
        function drawPowerup(pw) {
            ctx.save();
            ctx.translate(pw.x, pw.y + Math.sin(frame * 0.1) * 5);

            ctx.fillStyle = '#ffee58';
            ctx.beginPath(); ctx.arc(0, 0, pw.r + 3, 0, Math.PI * 2); ctx.fill();

            let sphereGrad = ctx.createRadialGradient(-4, -4, 2, 0, 0, pw.r);
            sphereGrad.addColorStop(0, '#80d8ff');
            sphereGrad.addColorStop(0.7, '#0091ea');
            sphereGrad.addColorStop(1, '#01579b');
            ctx.fillStyle = sphereGrad;
            ctx.beginPath(); ctx.arc(0, 0, pw.r, 0, Math.PI * 2); ctx.fill();

            ctx.fillStyle = '#ffffff';
            ctx.font = 'bold 16px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('🌊', 0, 6);

            ctx.restore();
        }

        // Vẽ Zombie
        function drawZombie(z) {
            ctx.save();
            ctx.translate(z.x, z.y);

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

        // Vẽ Con Người
        function drawHuman(h) {
            ctx.save();
            ctx.translate(h.x, h.y);
            ctx.fillStyle = '#ffcc80'; ctx.beginPath(); ctx.arc(0, -18, 8, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = h.gender === 'MALE' ? '#5d4037' : '#fbc02d'; ctx.beginPath(); ctx.arc(0, -21, 8, Math.PI, Math.PI*2); ctx.fill();
            ctx.fillStyle = h.gender === 'MALE' ? '#1e88e5' : '#e91e63'; ctx.fillRect(-6, -10, 12, 12);
            ctx.restore();
        }

        // Vẽ Bom 3D
        function drawBomb(o) {
            ctx.save();
            ctx.translate(o.x + 20, o.y + 20);
            let bombGrad = ctx.createRadialGradient(-4, -4, 2, 0, 0, 18);
            bombGrad.addColorStop(0, '#666'); bombGrad.addColorStop(0.6, '#222'); bombGrad.addColorStop(1, '#000');
            ctx.fillStyle = bombGrad; ctx.beginPath(); ctx.arc(0, 0, 18, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#ff1744'; ctx.font = 'bold 12px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('💣', 0, 4);
            ctx.restore();
        }

        // Vẽ Xe Hơi Đỏ Thể Thao Đẹp Chi Tiết
        function drawCar(o) {
            ctx.save();
            ctx.translate(o.x, o.y);

            // Thân xe dưới
            ctx.fillStyle = '#d32f2f';
            ctx.fillRect(0, 18, o.w, 20);

            // Mui xe trên
            ctx.fillStyle = '#b71c1c';
            ctx.fillRect(16, 4, 60, 14);

            // Kính xe sáng bóng
            ctx.fillStyle = '#81d4fa';
            ctx.fillRect(22, 7, 20, 10);
            ctx.fillRect(48, 7, 22, 10);

            // Đèn pha trước
            ctx.fillStyle = '#ffeb3b';
            ctx.fillRect(0, 22, 4, 8);

            // Bánh xe có mâm đĩa
            ctx.fillStyle = '#111';
            ctx.beginPath();
            ctx.arc(22, 38, 9, 0, Math.PI*2);
            ctx.arc(o.w - 22, 38, 9, 0, Math.PI*2);
            ctx.fill();
            ctx.fillStyle = '#9e9e9e';
            ctx.beginPath();
            ctx.arc(22, 38, 3, 0, Math.PI*2);
            ctx.arc(o.w - 22, 38, 3, 0, Math.PI*2);
            ctx.fill();

            // Người thò đầu hoảng sợ
            ctx.fillStyle = '#ffcc80'; ctx.beginPath(); ctx.arc(45, -8, 8, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#000'; ctx.beginPath(); ctx.arc(45, -5, 3, 0, Math.PI*2); ctx.fill();

            // Bảng bóng thoại (0/4)
            ctx.fillStyle = '#111'; ctx.fillRect(18, -48, 58, 26);
            ctx.fillStyle = '#ff3d00'; ctx.font = 'bold 16px sans-serif'; ctx.textAlign = 'center';
            ctx.fillText(`0/${o.reqZombies}`, 47, -30);

            ctx.restore();
        }

        // Vẽ Xe Buýt Vàng Rực Rỡ Chi Tiết
        function drawBus(o) {
            ctx.save();
            ctx.translate(o.x, o.y);

            // Thân xe buýt
            ctx.fillStyle = '#fbc02d'; ctx.fillRect(0, 0, o.w, 54);
            ctx.fillStyle = '#f57f17'; ctx.fillRect(0, 32, o.w, 6); // Sọc trang trí

            // Ô cửa kính xe buýt
            ctx.fillStyle = '#81d4fa';
            for(let k=0; k<4; k++) {
                ctx.fillRect(12 + (k * 28), 8, 20, 18);
            }

            // Đèn pha
            ctx.fillStyle = '#ffeb3b'; ctx.fillRect(0, 40, 5, 8);

            // Bánh xe buýt
            ctx.fillStyle = '#111';
            ctx.beginPath();
            ctx.arc(26, 54, 10, 0, Math.PI*2);
            ctx.arc(o.w - 26, 54, 10, 0, Math.PI*2);
            ctx.fill();

            // Bảng bóng thoại (0/8)
            ctx.fillStyle = '#111'; ctx.fillRect(38, -45, 60, 28);
            ctx.fillStyle = '#ff3d00'; ctx.font = 'bold 16px sans-serif'; ctx.textAlign = 'center';
            ctx.fillText(`0/${o.reqZombies}`, 68, -25);

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
