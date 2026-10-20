import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Zombie Tsunami Wide Dynamic Terrain HD", layout="centered")

st.markdown("<h1 style='text-align: center; color: #76ba1b;'>🧟 ZOMBIE TSUNAMI - WIDE DYNAMIC TERRAIN 🌊</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Đã xóa map thành phố, khôi phục góc nhìn rộng thoáng và tăng độ cao thấp chênh lệch rõ rệt cho các mảnh đất, hố!</p>", unsafe_allow_html=True)

game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; padding: 0; background-color: #0d1b2a; display: flex; justify-content: center; align-items: center; font-family: sans-serif; height: 100vh; overflow: hidden; }
        canvas { 
            border: 4px solid #76ba1b; 
            border-radius: 12px; 
            box-shadow: 0 8px 30px rgba(118, 186, 27, 0.4); 
            background: #111; 
            width: 800px; 
            height: 450px; 
        }
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

        let zombies = [{ x: 180, y: defaultGroundY - 20, vy: 0, isGrounded: true, legAngle: 0 }];

        let humans = [];
        let obstacles = [];
        let terrainSegments = []; // Danh sách các đoạn địa hình cao thấp khác nhau
        let pits = [];
        let powerups = [];
        let particles = [];
        let bgOffset = 0;

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
                        z.vy = -13.5 - (idx * 0.04);
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
            zombies = [{ x: 180, y: defaultGroundY - 20, vy: 0, isGrounded: true, legAngle: 0 }];
            humans = [];
            obstacles = [];
            pits = [];
            terrainSegments = [
                { x: 0, width: 900, groundY: defaultGroundY }
            ];
            powerups = [];
            particles = [];
            tsunamiActive = false;
            tsunamiTimer = 0;
        }

        function getGroundYAt(x) {
            let seg = terrainSegments.find(s => x >= s.x && x < s.x + s.width);
            return seg ? seg.groundY : defaultGroundY;
        }

        function isOverPit(x, width = 50) {
            return pits.some(p => (x + width > p.x) && (x < p.x + p.width));
        }

        function update() {
            if (gameState !== 'PLAYING') return;

            frame++;
            speed = 4.5 + Math.floor(frame / 600) * 0.4;
            bgOffset += speed;

            if (tsunamiActive) {
                tsunamiTimer--;
                if (tsunamiTimer <= 0) tsunamiActive = false;
            }

            // Tạo các bậc địa hình cao thấp chênh lệch rõ rệt
            if (terrainSegments.length > 0 && terrainSegments[terrainSegments.length - 1].x + terrainSegments[terrainSegments.length - 1].width < 900) {
                let lastSeg = terrainSegments[terrainSegments.length - 1];
                let nextX = lastSeg.x + lastSeg.width;
                let heights = [280, 310, 340, 370]; // Các cao độ chênh lệch rõ
                let randomH = heights[Math.floor(Math.random() * heights.length)];
                terrainSegments.push({ x: nextX, width: 350 + Math.random() * 250, groundY: randomH });
            }

            terrainSegments.forEach(s => s.x -= speed);
            terrainSegments = terrainSegments.filter(s => s.x + s.width > -100);

            // Spawn Hố
            if (frame % 220 === 0 && Math.random() > 0.3) {
                let pitWidth = 80 + Math.random() * 60;
                pits.push({ x: 850, width: pitWidth });
            }

            pits.forEach(p => p.x -= speed);
            pits = pits.filter(p => p.x + p.width > -50);

            // Spawn Sóng Thần
            if (frame % 950 === 0 && !tsunamiActive && Math.random() < 0.5) {
                let spawnX = 850;
                if (!isOverPit(spawnX, 40)) {
                    let gY = getGroundYAt(spawnX);
                    powerups.push({ x: spawnX, y: gY - 60, r: 18, collected: false });
                }
            }

            // Spawn Xe, Người, Bom (Tuyệt đối không trùng hố)
            if (frame % 110 === 0) {
                let spawnX = 850;
                if (!isOverPit(spawnX, 140)) {
                    let gY = getGroundYAt(spawnX);
                    let rand = Math.random();
                    if (rand < 0.32) {
                        let gender = Math.random() > 0.5 ? 'MALE' : 'FEMALE';
                        humans.push({ x: spawnX, y: gY - 20, gender: gender, eaten: false, armAngle: 0 });
                    } else if (rand < 0.65) {
                        obstacles.push({ x: spawnX, y: gY - 42, w: 75, h: 40, type: 'CAR', reqZombies: 4, peopleInside: 3, cooldown: 0 });
                    } else if (rand < 0.82) {
                        obstacles.push({ x: spawnX, y: gY - 58, w: 110, h: 55, type: 'BUS', reqZombies: 6, peopleInside: 6, cooldown: 0 });
                    } else if (rand < 0.87) {
                        obstacles.push({ x: spawnX, y: gY - 80, w: 115, h: 52, type: 'HELI', reqZombies: 8, peopleInside: 8, cooldown: 0 });
                    } else {
                        obstacles.push({ x: spawnX, y: gY - 38, w: 38, h: 38, type: 'BOMB' });
                    }
                }
            }

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

            for (let i = zombies.length - 1; i >= 0; i--) {
                let z = zombies[i];
                let currentGroundY = getGroundYAt(z.x);

                if (tsunamiActive) {
                    z.y = currentGroundY - 110 + Math.sin(frame * 0.15 + i * 0.4) * 8;
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
                                let roofY = obs.y - 16;
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
                        if (!onPit && z.y >= currentGroundY - 20) {
                            z.y = currentGroundY - 20;
                            z.vy = 0;
                            z.isGrounded = true;
                        } else if (onPit) {
                            z.isGrounded = false;
                        }
                    }
                }

                z.legAngle += z.isGrounded ? 0.22 : 0.08;

                if (z.y > canvas.height + 30) {
                    addParticles(z.x, canvas.height - 10, '#76ba1b', 10);
                    zombies.splice(i, 1);
                }
            }

            if (zombies.length === 0) {
                gameState = 'GAMEOVER';
                return;
            }

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
                        let tailGroundY = getGroundYAt(tail.x);
                        zombies.push({ x: tail.x - 22, y: tailGroundY - 20, vy: 0, isGrounded: true, legAngle: 0 });
                    }
                }
            });

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
                                    let tailGroundY = getGroundYAt(tail.x);
                                    zombies.push({ x: tail.x - 22, y: tailGroundY - 20, vy: 0, isGrounded: true, legAngle: 0 });
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
                                            let tailGroundY = getGroundYAt(tail.x);
                                            zombies.push({ x: tail.x - 22, y: tailGroundY - 20, vy: 0, isGrounded: true, legAngle: 0 });
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

        function drawBackground() {
            // Góc nhìn rộng thoáng đãng (Panorama)
            let skyGrad = ctx.createLinearGradient(0, 0, 0, 300);
            skyGrad.addColorStop(0, '#1565c0'); skyGrad.addColorStop(1, '#90caf9');
            ctx.fillStyle = skyGrad; ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Mây rộng trôi
            ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
            let cloudX1 = (250 - bgOffset * 0.15) % 950;
            if (cloudX1 < -150) cloudX1 += 950;
            ctx.beginPath(); ctx.arc(cloudX1, 70, 30, 0, Math.PI*2); ctx.arc(cloudX1 + 40, 60, 42, 0, Math.PI*2); ctx.arc(cloudX1 + 90, 70, 30, 0, Math.PI*2); ctx.fill();

            let cloudX2 = (650 - bgOffset * 0.15) % 950;
            if (cloudX2 < -150) cloudX2 += 950;
            ctx.beginPath(); ctx.arc(cloudX2, 110, 24, 0, Math.PI*2); ctx.arc(cloudX2 + 30, 102, 32, 0, Math.PI*2); ctx.arc(cloudX2 + 70, 110, 24, 0, Math.PI*2); ctx.fill();

            // Đồi núi phía xa xa (Parallax Hills)
            ctx.fillStyle = '#4caf50';
            let hillX = (100 - bgOffset * 0.3) % 900;
            if (hillX < -300) hillX += 900;
            ctx.beginPath();
            ctx.moveTo(hillX, 330);
            ctx.quadraticCurveTo(hillX + 180, 180, hillX + 360, 330);
            ctx.quadraticCurveTo(hillX + 540, 150, hillX + 720, 330);
            ctx.fill();

            // Vẽ các khối đất cao thấp chênh lệch rõ rệt
            terrainSegments.forEach(s => {
                ctx.fillStyle = '#261c14';
                ctx.fillRect(s.x, s.groundY, s.width, canvas.height - s.groundY);
                ctx.fillStyle = '#37474f';
                ctx.fillRect(s.x, s.groundY, s.width, 12);
                ctx.fillStyle = '#455a64';
                ctx.fillRect(s.x, s.groundY + 12, s.width, canvas.height - s.groundY - 12);

                // Vạch kẻ đường trên mặt đất
                ctx.strokeStyle = '#fbc02d'; ctx.lineWidth = 4;
                let dashWidth = 30; let dashGap = 20;
                let startX = s.x - (bgOffset % (dashWidth + dashGap));
                for (let x = startX; x < s.x + s.width; x += dashWidth + dashGap) {
                    if (x >= s.x && x + dashWidth <= s.x + s.width && !isOverPit(x, dashWidth)) {
                        ctx.beginPath(); ctx.moveTo(x, s.groundY + 45); ctx.lineTo(x + dashWidth, s.groundY + 45); ctx.stroke();
                    }
                }
            });

            // Vẽ Hố sâu thẳm
            pits.forEach(p => {
                let gY = getGroundYAt(p.x);
                ctx.fillStyle = '#110a06';
                ctx.fillRect(p.x, gY, p.width, canvas.height - gY);
                ctx.fillStyle = '#1a100a';
                ctx.fillRect(p.x - 6, gY, 6, canvas.height - gY);
                ctx.fillRect(p.x + p.width, gY, 6, canvas.height - gY);
            });

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
            ctx.strokeStyle = '#76ba1b'; ctx.lineWidth = 4.5;
            ctx.beginPath(); 
            ctx.moveTo(-4, 6); ctx.lineTo(-4 + Math.sin(z.legAngle)*7, 18); 
            ctx.moveTo(4, 6); ctx.lineTo(4 - Math.sin(z.legAngle)*7, 18); 
            ctx.stroke();

            ctx.fillStyle = '#fbc02d'; ctx.fillRect(-7, 2, 14, 7);
            ctx.fillStyle = '#8d2626'; ctx.fillRect(-8, -5, 16, 9);
            ctx.fillStyle = '#76ba1b'; ctx.beginPath(); ctx.arc(0, -15, 15, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#000000'; ctx.beginPath(); ctx.arc(6, -17, 9, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.arc(6, -17, 7.5, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#d32f2f'; ctx.beginPath(); ctx.arc(8, -17, 3.5, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#000000'; ctx.beginPath(); ctx.arc(8.5, -17, 1.5, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#1b5e20'; ctx.beginPath(); ctx.arc(7, -8, 5, 0, Math.PI); ctx.fill();
            ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.moveTo(4, -8); ctx.lineTo(6, -4); ctx.lineTo(8, -8); ctx.fill();
            ctx.strokeStyle = '#76ba1b'; ctx.lineWidth = 3.5;
            ctx.beginPath(); ctx.moveTo(2, -2); ctx.lineTo(12, 2); ctx.stroke();
            ctx.restore();
        }

        function drawHuman(h) {
            ctx.save();
            ctx.translate(h.x, h.y);
            ctx.fillStyle = '#ffcc80'; ctx.beginPath(); ctx.arc(0, -16, 7, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = h.gender === 'MALE' ? '#5d4037' : '#fbc02d'; ctx.beginPath(); ctx.arc(0, -19, 7, Math.PI, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#000'; ctx.beginPath(); ctx.arc(-2.5, -16, 1.2, 0, Math.PI*2); ctx.arc(2.5, -16, 1.2, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = h.gender === 'MALE' ? '#1e88e5' : '#e91e63'; ctx.fillRect(-5, -9, 10, 10);
            ctx.restore();
        }

        function drawBomb(o) {
            ctx.save();
            ctx.translate(o.x + 20, o.y + 20);
            let bombGrad = ctx.createRadialGradient(-4, -4, 2, 0, 0, 16);
            bombGrad.addColorStop(0, '#666'); bombGrad.addColorStop(0.6, '#222'); bombGrad.addColorStop(1, '#000');
            ctx.fillStyle = bombGrad; ctx.beginPath(); ctx.arc(0, 0, 16, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#ff1744'; ctx.font = 'bold 11px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('💣', 0, 4);
            ctx.restore();
        }

        function drawCar(o) {
            ctx.save();
            ctx.translate(o.x, o.y);
            ctx.fillStyle = '#d32f2f'; ctx.fillRect(0, 15, o.w, 18);
            ctx.fillStyle = '#b71c1c'; ctx.fillRect(14, 3, 52, 13);
            ctx.fillStyle = '#81d4fa'; ctx.fillRect(18, 5, 18, 9); ctx.fillRect(42, 5, 20, 9);
            ctx.fillStyle = '#ffeb3b'; ctx.fillRect(0, 19, 4, 7);
            ctx.fillStyle = '#111'; ctx.beginPath(); ctx.arc(18, 33, 8, 0, Math.PI*2); ctx.arc(o.w - 18, 33, 8, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#111'; ctx.fillRect(16, -42, 52, 24);
            ctx.fillStyle = '#ff3d00'; ctx.font = 'bold 15px sans-serif'; ctx.textAlign = 'center';
            ctx.fillText(`0/${o.reqZombies}`, 42, -25);
            ctx.restore();
        }

        function drawBus(o) {
            ctx.save();
            ctx.translate(o.x, o.y);
            ctx.fillStyle = '#fbc02d'; ctx.fillRect(0, 0, o.w, 48);
            ctx.fillStyle = '#f57f17'; ctx.fillRect(0, 28, o.w, 5);
            ctx.fillStyle = '#81d4fa';
            for(let k=0; k<4; k++) ctx.fillRect(10 + (k * 26), 7, 18, 16);
            ctx.fillStyle = '#111'; ctx.beginPath(); ctx.arc(22, 48, 9, 0, Math.PI*2); ctx.arc(o.w - 22, 48, 9, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#111'; ctx.fillRect(34, -40, 55, 26);
            ctx.fillStyle = '#ff3d00'; ctx.font = 'bold 15px sans-serif'; ctx.textAlign = 'center';
            ctx.fillText(`0/${o.reqZombies}`, 61, -22);
            ctx.restore();
        }

        function drawHelicopter(o) {
            ctx.save();
            ctx.translate(o.x, o.y);
            ctx.fillStyle = '#3e4a36'; ctx.beginPath(); ctx.ellipse(60, 25, 52, 20, 0, 0, Math.PI * 2); ctx.fill();
            ctx.fillRect(95, 18, 38, 10);
            ctx.fillStyle = '#111'; ctx.fillRect(130, 8, 5, 24);
            ctx.fillStyle = '#81d4fa'; ctx.fillRect(20, 14, 24, 14); ctx.fillRect(50, 16, 12, 10); ctx.fillRect(68, 16, 12, 10);
            ctx.fillStyle = '#111'; ctx.fillRect(55, 0, 6, 8);
            let bladeW = 95 + Math.sin(frame * 0.5) * 15;
            ctx.fillRect(58 - bladeW/2, 0, bladeW, 3);
            ctx.strokeStyle = '#222'; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(30, 42); ctx.lineTo(30, 48); ctx.lineTo(90, 48); ctx.lineTo(90, 42); ctx.stroke();
            ctx.fillStyle = '#ffffff'; ctx.font = 'bold 10px monospace'; ctx.fillText('T-315', 60, 28);
            ctx.fillStyle = '#111'; ctx.fillRect(35, -36, 50, 24);
            ctx.fillStyle = '#ff3d00'; ctx.font = 'bold 15px sans-serif'; ctx.textAlign = 'center';
            ctx.fillText(`0/${o.reqZombies}`, 60, -19);
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

components.html(game_code, height=480, scrolling=False)

