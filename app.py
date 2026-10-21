import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Zombie Tsunami Market Update HD", layout="centered")

st.markdown("<h1 style='text-align: center; color: #76ba1b;'>🧟 ZOMBIE TSUNAMI - MARKET & TERRAIN UPDATE 🌊</h1>", unsafe_allow_html=True)

game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; padding: 0; background-color: #0d1b2a; display: flex; justify-content: center; align-items: center; font-family: 'Arial Black', sans-serif; height: 100vh; overflow: hidden; user-select: none; }
        #gameContainer {
            position: relative;
            width: 800px;
            height: 450px;
            border: 4px solid #76ba1b;
            border-radius: 12px;
            box-shadow: 0 8px 30px rgba(118, 186, 27, 0.4);
            overflow: hidden;
            background: #111;
        }
        canvas {
            display: block;
            width: 100%;
            height: 100%;
        }

        /* GUI MENU OVERLAY */
        #menuOverlay {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-sizing: border-box;
            padding: 15px;
            pointer-events: auto;
            z-index: 10;
        }

        /* Logo Zombie Tsunami */
        .logo-container {
            position: absolute;
            top: 15px;
            left: 50%;
            transform: translateX(-50%);
            text-align: center;
        }
        .logo-title {
            font-size: 42px;
            color: #76ba1b;
            text-shadow: 3px 3px 0px #000, -2px -2px 0px #000, 2px -2px 0px #000, -2px 2px 0px #000, 0px 5px 10px rgba(0,0,0,0.8);
            letter-spacing: 2px;
            transform: rotate(-3deg);
            margin: 0;
            line-height: 1;
        }
        .logo-sub {
            font-size: 32px;
            color: #ff3d00;
            text-shadow: 2px 2px 0px #000, -2px -2px 0px #000, 2px -2px 0px #000, 0px 4px 8px rgba(0,0,0,0.8);
            letter-spacing: 3px;
            transform: rotate(2deg);
            margin-top: -5px;
        }

        .top-right-btns {
            position: absolute;
            top: 15px;
            right: 15px;
        }
        .btn-icon {
            width: 42px;
            height: 42px;
            background: #424242;
            border: 3px solid #fff;
            border-radius: 8px;
            color: #fff;
            font-size: 22px;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: 0 4px 0 #111;
        }

        .side-menu-right {
            position: absolute;
            right: 15px;
            top: 90px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .btn-side {
            width: 170px;
            height: 42px;
            background: linear-gradient(135deg, #e91e63, #c2185b);
            border: 3px solid #000;
            border-radius: 8px;
            color: #fff;
            font-size: 18px;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            padding-left: 12px;
            box-shadow: 3px 4px 0 #000;
            cursor: pointer;
            transform: rotate(2deg);
            text-shadow: 1px 1px 2px #000;
        }
        .btn-side:nth-child(2) { transform: rotate(-2deg); background: linear-gradient(135deg, #f57c00, #e65100); }
        .btn-side:active { transform: scale(0.96); }
        .btn-side span { margin-right: 10px; font-size: 20px; }

        .btn-play {
            position: absolute;
            bottom: 25px;
            right: 20px;
            width: 180px;
            height: 80px;
            background: linear-gradient(180deg, #ff9800 0%, #ff3d00 100%);
            border: 4px solid #fff;
            outline: 4px solid #000;
            border-radius: 14px;
            color: #fff;
            font-size: 38px;
            font-weight: 900;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: 0 8px 0 #801300, 0 12px 15px rgba(0,0,0,0.5);
            text-shadow: 3px 3px 0 #000;
            transform: rotate(-3deg);
        }
        .btn-play:hover { transform: rotate(-3deg) scale(1.05); }
        .btn-play:active { transform: rotate(-3deg) translateY(6px); box-shadow: 0 2px 0 #801300; }

        .best-score-box {
            position: absolute;
            bottom: 20px;
            left: 20px;
            background: rgba(0, 0, 0, 0.65);
            border: 3px solid #fff;
            border-radius: 10px;
            padding: 8px 16px;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .best-score-title { font-size: 15px; color: #ddd; margin: 0; }
        .best-score-val { font-size: 26px; color: #ffeb3b; font-weight: bold; margin: 0; }

        /* MARKET MODAL POPUP */
        #marketModal {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.85);
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 100;
            padding: 20px;
            box-sizing: border-box;
        }
        .market-box {
            width: 680px;
            height: 380px;
            background: #1e272e;
            border: 4px solid #fbc02d;
            border-radius: 16px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            box-shadow: 0 0 30px rgba(251, 192, 45, 0.4);
        }
        .market-header {
            background: #fbc02d;
            color: #000;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 24px;
            font-weight: bold;
        }
        .close-btn {
            background: #d32f2f;
            color: #fff;
            border: 2px solid #fff;
            border-radius: 50%;
            width: 32px;
            height: 32px;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            font-size: 18px;
        }
        .market-tabs {
            display: flex;
            background: #0f171e;
            border-bottom: 2px solid #333;
        }
        .tab-btn {
            flex: 1;
            padding: 12px;
            text-align: center;
            color: #aaa;
            font-size: 18px;
            cursor: pointer;
            border-right: 1px solid #222;
            font-weight: bold;
        }
        .tab-btn.active {
            background: #1e272e;
            color: #76ba1b;
            border-bottom: 3px solid #76ba1b;
        }
        .market-content {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            gap: 20px;
            justify-content: center;
            align-items: center;
        }
        .shop-item {
            width: 200px;
            height: 220px;
            background: #2f3640;
            border: 3px solid #485460;
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            padding: 15px;
            box-sizing: border-box;
            position: relative;
        }
        .shop-item.coming-soon {
            filter: brightness(0.4);
        }
        .cs-tag {
            position: absolute;
            top: 80px;
            background: #ff1744;
            color: #fff;
            padding: 4px 12px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 4px;
            transform: rotate(-10deg);
        }
        .shop-img {
            font-size: 48px;
            margin-top: 10px;
        }
        .shop-title {
            color: #fff;
            font-size: 16px;
            margin-top: 5px;
        }
        .buy-btn {
            background: #4cd137;
            color: #000;
            border: none;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            cursor: pointer;
            font-size: 15px;
            box-shadow: 0 4px 0 #44bd32;
            width: 100%;
        }
        .buy-btn.equipped {
            background: #00a8ff;
            color: #fff;
            box-shadow: 0 4px 0 #0097e6;
        }
        .buy-btn:disabled {
            background: #718093;
            box-shadow: none;
            cursor: not-allowed;
            color: #ccc;
        }
    </style>
</head>
<body>
    <div id="gameContainer">
        <!-- CANVAS TRÒ CHƠI -->
        <canvas id="gameCanvas" width="800" height="450"></canvas>

        <!-- MENU OVERLAY UI -->
        <div id="menuOverlay">
            <div class="logo-container">
                <h1 class="logo-title">ZOMBIE</h1>
                <div class="logo-sub">TSUNAMI</div>
            </div>

            <div class="top-right-btns">
                <div class="btn-icon">⚙️</div>
            </div>

            <div class="side-menu-right">
                <div class="btn-side"><span>🧪</span> MISSION</div>
                <div class="btn-side" id="openMarketBtn"><span>🪙</span> MARKET</div>
            </div>

            <div class="best-score-box">
                <div>
                    <div class="best-score-title">Best score:</div>
                    <div class="best-score-val">🧠 <span id="bestScoreText">0</span></div>
                </div>
            </div>

            <div class="btn-play" id="playBtn">PLAY</div>
        </div>

        <!-- CỬA HÀNG MARKET MODAL -->
        <div id="marketModal">
            <div class="market-box">
                <div class="market-header">
                    <div>🛒 MARKET (Xu: 🪙 <span id="marketCoinText">0</span>)</div>
                    <div class="close-btn" id="closeMarketBtn">✖</div>
                </div>
                <div class="market-tabs">
                    <div class="tab-btn active" id="tabOutfits">TRANG PHỤC</div>
                    <div class="tab-btn" id="tabHats">PHỤ KIỆN</div>
                </div>
                
                <!-- CONTENT TRANG PHỤC -->
                <div class="market-content" id="contentOutfits">
                    <!-- Item 1: Mummy -->
                    <div class="shop-item">
                        <div class="shop-img">🩹</div>
                        <div class="shop-title">Xác Ướp (Mummy)</div>
                        <button class="buy-btn" id="buyMummyBtn">300 Xu</button>
                    </div>
                    <!-- Item 2: Coming Soon -->
                    <div class="shop-item coming-soon">
                        <div class="shop-img">🧟</div>
                        <div class="shop-title">???</div>
                        <div class="cs-tag">COMING SOON</div>
                        <button class="buy-btn" disabled>Khóa</button>
                    </div>
                </div>

                <!-- CONTENT PHỤ KIỆN -->
                <div class="market-content" id="contentHats" style="display: none;">
                    <!-- Hat 1: Cowboy -->
                    <div class="shop-item">
                        <div class="shop-img">🤠</div>
                        <div class="shop-title">Mũ Cao Bồi</div>
                        <button class="buy-btn" id="buyHatBtn">200 Xu</button>
                    </div>
                    <!-- Hat 2: Pumpkin -->
                    <div class="shop-item">
                        <div class="shop-img">🎃</div>
                        <div class="shop-title">Đầu Bí Ngô</div>
                        <button class="buy-btn" id="buyPumpkinBtn">200 Xu</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const menuOverlay = document.getElementById('menuOverlay');
        const playBtn = document.getElementById('playBtn');
        const bestScoreText = document.getElementById('bestScoreText');

        // Market elements
        const marketModal = document.getElementById('marketModal');
        const openMarketBtn = document.getElementById('openMarketBtn');
        const closeMarketBtn = document.getElementById('closeMarketBtn');
        const marketCoinText = document.getElementById('marketCoinText');
        const tabOutfits = document.getElementById('tabOutfits');
        const tabHats = document.getElementById('tabHats');
        const contentOutfits = document.getElementById('contentOutfits');
        const contentHats = document.getElementById('contentHats');

        const buyMummyBtn = document.getElementById('buyMummyBtn');
        const buyHatBtn = document.getElementById('buyHatBtn');
        const buyPumpkinBtn = document.getElementById('buyPumpkinBtn');

        let gameState = 'MENU'; 
        let score = 0;
        let bestScore = localStorage.getItem('zt_best_score') || 0;
        bestScoreText.innerText = bestScore;

        let totalCoins = parseInt(localStorage.getItem('zt_total_coins') || '0');
        let equippedOutfit = localStorage.getItem('zt_equipped_outfit') || 'NONE'; // 'NONE', 'MUMMY'
        let equippedHat = localStorage.getItem('zt_equipped_hat') || 'NONE';       // 'NONE', 'HAT', 'PUMPKIN'
        let ownedItems = JSON.parse(localStorage.getItem('zt_owned_items') || '[]');

        function saveUserData() {
            localStorage.setItem('zt_total_coins', totalCoins);
            localStorage.setItem('zt_equipped_outfit', equippedOutfit);
            localStorage.setItem('zt_equipped_hat', equippedHat);
            localStorage.setItem('zt_owned_items', JSON.stringify(ownedItems));
            updateMarketUI();
        }

        function updateMarketUI() {
            marketCoinText.innerText = totalCoins;

            // Mummy Outfit UI
            if (ownedItems.includes('MUMMY')) {
                if (equippedOutfit === 'MUMMY') {
                    buyMummyBtn.innerText = 'Đang Mặc';
                    buyMummyBtn.className = 'buy-btn equipped';
                } else {
                    buyMummyBtn.innerText = 'Mặc Vào';
                    buyMummyBtn.className = 'buy-btn';
                }
            } else {
                buyMummyBtn.innerText = '300 Xu';
            }

            // Cowboy Hat UI
            if (ownedItems.includes('HAT')) {
                if (equippedHat === 'HAT') {
                    buyHatBtn.innerText = 'Đang Đội';
                    buyHatBtn.className = 'buy-btn equipped';
                } else {
                    buyHatBtn.innerText = 'Đội Vào';
                    buyHatBtn.className = 'buy-btn';
                }
            } else {
                buyHatBtn.innerText = '200 Xu';
            }

            // Pumpkin Hat UI
            if (ownedItems.includes('PUMPKIN')) {
                if (equippedHat === 'PUMPKIN') {
                    buyPumpkinBtn.innerText = 'Đang Đội';
                    buyPumpkinBtn.className = 'buy-btn equipped';
                } else {
                    buyPumpkinBtn.innerText = 'Đội Vào';
                    buyPumpkinBtn.className = 'buy-btn';
                }
            } else {
                buyPumpkinBtn.innerText = '200 Xu';
            }
        }

        // TAB SWITCH
        tabOutfits.addEventListener('click', () => {
            tabOutfits.classList.add('active');
            tabHats.classList.remove('active');
            contentOutfits.style.display = 'flex';
            contentHats.style.display = 'none';
        });
        tabHats.addEventListener('click', () => {
            tabHats.classList.add('active');
            tabOutfits.classList.remove('active');
            contentHats.style.display = 'flex';
            contentOutfits.style.display = 'none';
        });

        openMarketBtn.addEventListener('click', () => {
            updateMarketUI();
            marketModal.style.display = 'flex';
        });
        closeMarketBtn.addEventListener('click', () => {
            marketModal.style.display = 'none';
        });

        // MUA VÀ TRANG BỊ
        buyMummyBtn.addEventListener('click', () => {
            if (!ownedItems.includes('MUMMY')) {
                if (totalCoins >= 300) {
                    totalCoins -= 300;
                    ownedItems.push('MUMMY');
                    equippedOutfit = 'MUMMY';
                } else {
                    alert('Bạn không đủ xu! Hãy chơi nhặt thêm xu nhé.');
                }
            } else {
                equippedOutfit = equippedOutfit === 'MUMMY' ? 'NONE' : 'MUMMY';
            }
            saveUserData();
        });

        buyHatBtn.addEventListener('click', () => {
            if (!ownedItems.includes('HAT')) {
                if (totalCoins >= 200) {
                    totalCoins -= 200;
                    ownedItems.push('HAT');
                    equippedHat = 'HAT';
                } else {
                    alert('Bạn không đủ xu!');
                }
            } else {
                equippedHat = equippedHat === 'HAT' ? 'NONE' : 'HAT';
            }
            saveUserData();
        });

        buyPumpkinBtn.addEventListener('click', () => {
            if (!ownedItems.includes('PUMPKIN')) {
                if (totalCoins >= 200) {
                    totalCoins -= 200;
                    ownedItems.push('PUMPKIN');
                    equippedHat = 'PUMPKIN';
                } else {
                    alert('Bạn không đủ xu!');
                }
            } else {
                equippedHat = equippedHat === 'PUMPKIN' ? 'NONE' : 'PUMPKIN';
            }
            saveUserData();
        });

        let currentCoins = 0;
        let speed = 4.5;
        let frame = 0;

        const gravity = 0.65;
        const defaultGroundY = 330;

        let zombies = [{ x: 180, y: defaultGroundY - 20, vy: 0, isGrounded: true, legAngle: 0 }];
        let humans = [];
        let obstacles = [];
        let pits = [];
        let powerups = [];
        let coinTrails = [];
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

        function startGame() {
            resetGame();
            gameState = 'PLAYING';
            menuOverlay.style.display = 'none';
        }

        playBtn.addEventListener('click', startGame);

        function handleInput() {
            if (gameState === 'GAMEOVER') {
                gameState = 'MENU';
                menuOverlay.style.display = 'flex';
            } else if (gameState === 'PLAYING') {
                zombies.forEach((z, idx) => {
                    if (z.isGrounded) {
                        z.vy = -13.5 - (idx * 0.04);
                        z.isGrounded = false;
                    }
                });
            }
        }

        window.addEventListener('keydown', (e) => { 
            if (e.code === 'Space' || e.code === 'ArrowUp') {
                if (gameState === 'MENU' && marketModal.style.display !== 'flex') startGame();
                else handleInput();
            }
        });
        canvas.addEventListener('touchstart', (e) => { e.preventDefault(); handleInput(); });
        canvas.addEventListener('mousedown', () => { if (gameState === 'PLAYING') handleInput(); });

        function resetGame() {
            score = 0;
            currentCoins = 0;
            speed = 4.5;
            frame = 0;
            zombies = [{ x: 180, y: defaultGroundY - 20, vy: 0, isGrounded: true, legAngle: 0 }];
            humans = [];
            obstacles = [];
            pits = [];
            powerups = [];
            coinTrails = [];
            particles = [];
            tsunamiActive = false;
            tsunamiTimer = 0;
        }

        function isOverPit(x, width = 50) {
            return pits.some(p => (x + width > p.x) && (x < p.x + p.width));
        }

        function update() {
            frame++;
            bgOffset += (gameState === 'MENU' ? 1.5 : speed);

            if (gameState !== 'PLAYING') return;

            speed = 4.5 + Math.floor(frame / 600) * 0.4;

            if (tsunamiActive) {
                tsunamiTimer--;
                if (tsunamiTimer <= 0) tsunamiActive = false;
            }

            // Spawn Hố
            if (frame % 230 === 0 && Math.random() > 0.35) {
                let pitWidth = 80 + Math.random() * 70;
                pits.push({ x: 850, width: pitWidth });
            }

            // Spawn Chuỗi Đồng Xu Nối Liền (5 - 8 Xu)
            if (frame % 160 === 0 && Math.random() < 0.6) {
                let count = 5 + Math.floor(Math.random() * 4); // 5 - 8 xu
                let startX = 850;
                let coinY = defaultGroundY - 40 - (Math.random() > 0.5 ? 40 : 0); // Đôi khi bay cao
                for(let c = 0; c < count; c++) {
                    coinTrails.push({ x: startX + c * 24, y: coinY, collected: false });
                }
            }

            // Spawn Powerup Sóng Thần
            if (frame % 950 === 0 && !tsunamiActive && Math.random() < 0.5) {
                let spawnX = 850;
                if (!isOverPit(spawnX, 40)) {
                    powerups.push({ x: spawnX, y: defaultGroundY - 60, r: 18, collected: false });
                }
            }

            // Spawn Người & Vật cản
            if (frame % 115 === 0) {
                let spawnX = 850;
                if (!isOverPit(spawnX, 150)) {
                    let rand = Math.random();
                    if (rand < 0.32) {
                        let gender = Math.random() > 0.5 ? 'MALE' : 'FEMALE';
                        humans.push({ x: spawnX, y: defaultGroundY - 20, gender: gender, eaten: false });
                    } else if (rand < 0.65) {
                        obstacles.push({ x: spawnX, y: defaultGroundY - 45, w: 90, h: 42, type: 'CAR', reqZombies: 4, peopleInside: 3, cooldown: 0 });
                    } else if (rand < 0.82) {
                        obstacles.push({ x: spawnX, y: defaultGroundY - 62, w: 125, h: 58, type: 'BUS', reqZombies: 6, peopleInside: 6, cooldown: 0 });
                    } else if (rand < 0.87) {
                        obstacles.push({ x: spawnX, y: defaultGroundY - 85, w: 130, h: 55, type: 'HELI', reqZombies: 8, peopleInside: 8, cooldown: 0 });
                    } else {
                        obstacles.push({ x: spawnX, y: defaultGroundY - 40, w: 40, h: 40, type: 'BOMB' });
                    }
                }
            }

            pits.forEach(p => p.x -= speed);
            pits = pits.filter(p => p.x + p.width > -50);

            // Cập nhật Chuỗi Đồng Xu
            coinTrails.forEach(c => {
                c.x -= speed;
                if (!c.collected) {
                    zombies.forEach(z => {
                        if (Math.abs(z.x - c.x) < 20 && Math.abs(z.y - c.y) < 25) {
                            c.collected = true;
                            currentCoins += 1;
                            totalCoins += 1;
                            saveUserData();
                            addParticles(c.x, c.y, '#fbc02d', 6);
                        }
                    });
                }
            });
            coinTrails = coinTrails.filter(c => c.x > -30 && !c.collected);

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

            // XỬ LÝ ZOMBIE & TÉ HỐ TRỪ DẦN DẦN
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
                        if (!onPit && z.y >= defaultGroundY - 20) {
                            z.y = defaultGroundY - 20;
                            z.vy = 0;
                            z.isGrounded = true;
                        } else if (onPit) {
                            z.isGrounded = false;
                        }
                    }
                }

                z.legAngle += z.isGrounded ? 0.22 : 0.08;

                // TÉ HỐ BỊ TRỪ DẦN DẦN KHI RƠI KHỎI MÀN HÌNH
                if (z.y > canvas.height + 30) {
                    addParticles(z.x, canvas.height - 10, '#76ba1b', 12);
                    zombies.splice(i, 1);
                }
            }

            if (zombies.length === 0) {
                gameState = 'GAMEOVER';
                if (score > bestScore) {
                    bestScore = score;
                    localStorage.setItem('zt_best_score', bestScore);
                    bestScoreText.innerText = bestScore;
                }
                return;
            }

            // SÓNG THẦN CÀN QUÉT NGƯỜI VÀ XE CỘ
            humans.forEach((h) => {
                h.x -= speed;
                let leader = zombies[0];

                // Nếu có Sóng Thần -> Tự động cuốn sạch người từ xa
                if (tsunamiActive) {
                    if (h.x < 350 && !h.eaten) {
                        h.eaten = true;
                        score += 1;
                        currentCoins += 5;
                        totalCoins += 5;
                        saveUserData();
                        addParticles(h.x, h.y - 10, '#00e5ff', 15);
                        if (zombies.length < 30) {
                            let tail = zombies[zombies.length - 1];
                            zombies.push({ x: tail.x - 22, y: tail.y, vy: 0, isGrounded: true, legAngle: 0 });
                        }
                    }
                } else {
                    if (!h.eaten && leader && Math.abs(leader.x - h.x) < 35 && Math.abs(leader.y - h.y) < 60) {
                        h.eaten = true;
                        score += 1;
                        currentCoins += 5;
                        totalCoins += 5;
                        saveUserData();
                        addParticles(h.x, h.y - 10, '#76ba1b', 15);
                        if (zombies.length < 30) {
                            let tail = zombies[zombies.length - 1];
                            zombies.push({ x: tail.x - 22, y: tail.y, vy: 0, isGrounded: tail.isGrounded, legAngle: 0 });
                        }
                    }
                }
            });

            obstacles.forEach((obs, obsIdx) => {
                obs.x -= speed;
                if (obs.cooldown > 0) obs.cooldown--;

                if (tsunamiActive) {
                    if (Math.abs(zombies[0].x - obs.x) < 120) {
                        addParticles(obs.x + obs.w/2, obs.y, '#00e5ff', 30);
                        if (obs.type === 'CAR' || obs.type === 'BUS' || obs.type === 'HELI') {
                            score += obs.peopleInside;
                            currentCoins += obs.peopleInside * 10;
                            totalCoins += obs.peopleInside * 10;
                            saveUserData();
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
                                    currentCoins += obs.peopleInside * 10;
                                    totalCoins += obs.peopleInside * 10;
                                    saveUserData();
                                    for (let k = 0; k < obs.peopleInside; k++) {
                                        if (zombies.length < 30) {
                                            let tail = zombies[zombies.length - 1];
                                            zombies.push({ x: tail.x - 22, y: tail.y, vy: 0, isGrounded: true, legAngle: 0 });
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
                                            if (score > bestScore) {
                                                bestScore = score;
                                                localStorage.setItem('zt_best_score', bestScore);
                                                bestScoreText.innerText = bestScore;
                                            }
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

            particles.forEach(p => { p.x += p.vx; p.y += p.vy; p.life--; });
            particles = particles.filter(p => p.life > 0);
        }

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
            }

            for (let tIdx = 0; tIdx < 2; tIdx++) {
                let treeX = (80 + tIdx * 450 - bgOffset * 0.8) % 900;
                if (treeX < -100) treeX += 900;
                ctx.fillStyle = '#5d4037'; ctx.fillRect(treeX, 180, 16, 120);
                ctx.fillStyle = '#2e7d32'; ctx.beginPath();
                ctx.arc(treeX - 20, 170, 28, 0, Math.PI*2); ctx.arc(treeX + 35, 170, 28, 0, Math.PI*2); ctx.arc(treeX + 8, 150, 32, 0, Math.PI*2); ctx.fill();
            }
        }

        function drawBackground() {
            drawBeachMap();

            ctx.fillStyle = '#261c14';
            ctx.fillRect(0, defaultGroundY, canvas.width, canvas.height - defaultGroundY);
            ctx.fillStyle = '#37474f';
            ctx.fillRect(0, defaultGroundY, canvas.width, 12);
            ctx.fillStyle = '#455a64';
            ctx.fillRect(0, defaultGroundY + 12, canvas.width, canvas.height - defaultGroundY - 12);

            pits.forEach(p => {
                ctx.fillStyle = '#110a06';
                ctx.fillRect(p.x, defaultGroundY, p.width, canvas.height - defaultGroundY);

                ctx.fillStyle = '#1a100a';
                ctx.fillRect(p.x - 6, defaultGroundY, 6, canvas.height - defaultGroundY);
                ctx.fillRect(p.x + p.width, defaultGroundY, 6, canvas.height - defaultGroundY);
            });

            ctx.strokeStyle = '#fbc02d'; ctx.lineWidth = 4;
            let dashWidth = 30; let dashGap = 20;
            let startX = - (bgOffset % (dashWidth + dashGap));
            for (let x = startX; x < canvas.width; x += dashWidth + dashGap) {
                if (!isOverPit(x, dashWidth)) {
                    ctx.beginPath(); ctx.moveTo(x, defaultGroundY + 45); ctx.lineTo(x + dashWidth, defaultGroundY + 45); ctx.stroke();
                }
            }

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

        function drawZombie(z) {
            ctx.save();
            ctx.translate(z.x, z.y);

            // BỘ ĐỒ XÁC ƯỚP (MUMMY)
            if (equippedOutfit === 'MUMMY') {
                ctx.strokeStyle = '#eceff1'; ctx.lineWidth = 5;
                ctx.beginPath(); 
                ctx.moveTo(-4, 6); ctx.lineTo(-4 + Math.sin(z.legAngle)*7, 18); 
                ctx.moveTo(4, 6); ctx.lineTo(4 - Math.sin(z.legAngle)*7, 18); 
                ctx.stroke();

                ctx.fillStyle = '#cfd8dc'; ctx.fillRect(-8, -5, 16, 14);
                ctx.fillStyle = '#cfd8dc'; ctx.beginPath(); ctx.arc(0, -15, 16, 0, Math.PI * 2); ctx.fill();
                
                // Mắt đỏ xác ướp
                ctx.fillStyle = '#111'; ctx.fillRect(-8, -20, 16, 8);
                ctx.fillStyle = '#ff1744'; ctx.beginPath(); ctx.arc(4, -16, 3.5, 0, Math.PI * 2); ctx.fill();

                // Dải băng quấn
                ctx.strokeStyle = '#90a4ae'; ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(-15, -12); ctx.lineTo(15, -8);
                ctx.moveTo(-12, -22); ctx.lineTo(12, -18);
                ctx.moveTo(-7, -2); ctx.lineTo(7, 2);
                ctx.stroke();
            } else {
                // ZOMBIE THƯỜNG
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
            }

            // PHỤ KIỆN MŨ
            if (equippedHat === 'HAT') {
                ctx.fillStyle = '#795548';
                ctx.fillRect(-18, -31, 36, 4);
                ctx.fillRect(-10, -42, 20, 12);
            } else if (equippedHat === 'PUMPKIN') {
                ctx.fillStyle = '#ff6f00';
                ctx.beginPath(); ctx.arc(0, -31, 12, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = '#33691e'; ctx.fillRect(-2, -46, 4, 6);
                ctx.fillStyle = '#000';
                ctx.beginPath(); ctx.moveTo(-6, -34); ctx.lineTo(-2, -34); ctx.lineTo(-4, -30); ctx.fill();
                ctx.beginPath(); ctx.moveTo(2, -34); ctx.lineTo(6, -34); ctx.lineTo(4, -30); ctx.fill();
            }

            ctx.restore();
        }

        function drawCoin(c) {
            ctx.save();
            ctx.translate(c.x, c.y);
            ctx.fillStyle = '#fbc02d'; ctx.beginPath(); ctx.arc(0, 0, 9, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#fff59d'; ctx.beginPath(); ctx.arc(0, 0, 6, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#f57f17'; ctx.font = 'bold 10px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('$', 0, 3.5);
            ctx.restore();
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

            if (gameState === 'MENU') {
                let demoZ = { x: 220, y: defaultGroundY - 20, legAngle: frame * 0.2 };
                drawZombie(demoZ);
                return;
            }

            coinTrails.forEach(c => drawCoin(c));
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

            // HUD UI trong khi chơi
            ctx.fillStyle = 'rgba(0,0,0,0.5)'; ctx.fillRect(15, 12, 170, 70);
            ctx.fillStyle = '#fbc02d'; ctx.font = 'bold 22px sans-serif'; ctx.textAlign = 'left'; ctx.fillText(`🪙 ${totalCoins}`, 25, 40);
            ctx.fillStyle = '#76ba1b'; ctx.fillText(`🧠 x${zombies.length}`, 25, 70);

            if (gameState === 'GAMEOVER') {
                ctx.fillStyle = 'rgba(0,0,0,0.85)'; ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#ff1744'; ctx.font = 'bold 42px sans-serif'; ctx.textAlign = 'center';
                ctx.fillText('GAME OVER', 400, 180);
                ctx.fillStyle = '#ffffff'; ctx.font = '22px sans-serif';
                ctx.fillText(`Số người nuốt chửng: ${score}`, 400, 230);
                ctx.fillText(`Xu thu thập được: 🪙 +${currentCoins}`, 400, 260);
                ctx.fillText('Nhấn Space / Chạm để quay về Menu', 400, 295);
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
