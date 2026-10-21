import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Zombie Tsunami Authentic Edition", layout="centered")

st.markdown("<h1 style='text-align: center; color: #76ba1b;'>🧟 ZOMBIE TSUNAMI - AUTHENTIC EDITION 🌊</h1>", unsafe_allow_html=True)

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
        canvas { display: block; width: 100%; height: 100%; }

        /* GUI MENU OVERLAY */
        #menuOverlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            display: flex; flex-direction: column; justify-content: space-between;
            box-sizing: border-box; padding: 15px; pointer-events: auto; z-index: 10;
        }

        .logo-container { position: absolute; top: 15px; left: 50%; transform: translateX(-50%); text-align: center; }
        .logo-title {
            font-size: 44px; color: #76ba1b;
            text-shadow: 3px 3px 0px #000, -2px -2px 0px #000, 2px -2px 0px #000, -2px 2px 0px #000, 0px 5px 10px rgba(0,0,0,0.8);
            letter-spacing: 2px; transform: rotate(-3deg); margin: 0; line-height: 1;
        }
        .logo-sub {
            font-size: 34px; color: #ff3d00;
            text-shadow: 2px 2px 0px #000, -2px -2px 0px #000, 2px -2px 0px #000, 0px 4px 8px rgba(0,0,0,0.8);
            letter-spacing: 3px; transform: rotate(2deg); margin-top: -5px;
        }

        .top-right-btns { position: absolute; top: 15px; right: 15px; display: flex; gap: 10px; z-index: 20; }
        .btn-icon {
            width: 42px; height: 42px; background: #424242; border: 3px solid #fff; border-radius: 8px;
            color: #fff; font-size: 22px; display: flex; justify-content: center; align-items: center; cursor: pointer;
            box-shadow: 0 4px 0 #111;
        }
        .btn-icon:active { transform: translateY(2px); box-shadow: 0 2px 0 #111; }

        .side-menu-right { position: absolute; right: 15px; top: 90px; display: flex; flex-direction: column; gap: 12px; }
        .btn-side {
            width: 170px; height: 42px; background: linear-gradient(135deg, #e91e63, #c2185b);
            border: 3px solid #000; border-radius: 8px; color: #fff; font-size: 18px; font-weight: bold;
            display: flex; align-items: center; justify-content: flex-start; padding-left: 12px;
            box-shadow: 3px 4px 0 #000; cursor: pointer; transform: rotate(2deg); text-shadow: 1px 1px 2px #000;
        }
        .btn-side:nth-child(2) { transform: rotate(-2deg); background: linear-gradient(135deg, #f57c00, #e65100); }
        .btn-side:active { transform: scale(0.96); }
        .btn-side span { margin-right: 10px; font-size: 20px; }

        .btn-play {
            position: absolute; bottom: 25px; right: 20px; width: 180px; height: 80px;
            background: linear-gradient(180deg, #ff9800 0%, #ff3d00 100%);
            border: 4px solid #fff; outline: 4px solid #000; border-radius: 14px;
            color: #fff; font-size: 38px; font-weight: 900; display: flex; justify-content: center; align-items: center;
            cursor: pointer; box-shadow: 0 8px 0 #801300, 0 12px 15px rgba(0,0,0,0.5);
            text-shadow: 3px 3px 0 #000; transform: rotate(-3deg);
        }
        .btn-play:hover { transform: rotate(-3deg) scale(1.05); }
        .btn-play:active { transform: rotate(-3deg) translateY(6px); box-shadow: 0 2px 0 #801300; }

        .best-score-box {
            position: absolute; bottom: 20px; left: 20px; background: rgba(0, 0, 0, 0.65);
            border: 3px solid #fff; border-radius: 10px; padding: 8px 16px; color: #fff; display: flex; align-items: center; gap: 10px;
        }
        .best-score-title { font-size: 15px; color: #ddd; margin: 0; }
        .best-score-val { font-size: 26px; color: #ffeb3b; font-weight: bold; margin: 0; }

        /* MODAL POPUPS */
        .modal-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.85);
            display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 100;
            padding: 20px; box-sizing: border-box;
        }
        .modal-box {
            width: 680px; height: 380px; background: #1e272e; border: 4px solid #fbc02d; border-radius: 16px;
            display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 0 30px rgba(251, 192, 45, 0.4);
        }
        .modal-header { background: #fbc02d; color: #000; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; font-size: 24px; font-weight: bold; }
        .close-btn { background: #d32f2f; color: #fff; border: 2px solid #fff; border-radius: 50%; width: 32px; height: 32px; display: flex; justify-content: center; align-items: center; cursor: pointer; font-size: 18px; }
        
        .market-tabs { display: flex; background: #0f171e; border-bottom: 2px solid #333; }
        .tab-btn { flex: 1; padding: 12px; text-align: center; color: #aaa; font-size: 18px; cursor: pointer; border-right: 1px solid #222; font-weight: bold; }
        .tab-btn.active { background: #1e272e; color: #76ba1b; border-bottom: 3px solid #76ba1b; }
        .market-content { flex: 1; padding: 20px; overflow-y: auto; display: flex; gap: 20px; justify-content: center; align-items: center; }
        
        .shop-item { width: 200px; height: 220px; background: #2f3640; border: 3px solid #485460; border-radius: 12px; display: flex; flex-direction: column; align-items: center; justify-content: space-between; padding: 15px; box-sizing: border-box; position: relative; }
        .shop-item.coming-soon { filter: brightness(0.4); }
        .cs-tag { position: absolute; top: 80px; background: #ff1744; color: #fff; padding: 4px 12px; font-size: 14px; font-weight: bold; border-radius: 4px; transform: rotate(-10deg); }
        .shop-img { font-size: 48px; margin-top: 10px; }
        .shop-title { color: #fff; font-size: 16px; margin-top: 5px; }
        .buy-btn { background: #4cd137; color: #000; border: none; padding: 8px 16px; border-radius: 20px; font-weight: bold; cursor: pointer; font-size: 15px; box-shadow: 0 4px 0 #44bd32; width: 100%; }
        .buy-btn.equipped { background: #00a8ff; color: #fff; box-shadow: 0 4px 0 #0097e6; }
        .buy-btn:disabled { background: #718093; box-shadow: none; cursor: not-allowed; color: #ccc; }

        .mission-list { flex: 1; padding: 20px; display: flex; flex-direction: column; gap: 15px; overflow-y: auto; }
        .mission-card { background: #2f3640; border: 3px solid #485460; border-radius: 12px; display: flex; align-items: center; padding: 12px 18px; gap: 15px; }
        .mission-icon { width: 50px; height: 50px; background: #111; border: 2px solid #fff; border-radius: 10px; display: flex; justify-content: center; align-items: center; font-size: 28px; }
        .mission-info { flex: 1; color: #fff; }
        .mission-title { font-size: 16px; font-weight: bold; margin-bottom: 6px; }
        .mission-progress { font-size: 14px; color: #ffeb3b; }
        .collect-btn { background: #fbc02d; color: #000; border: none; padding: 10px 18px; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer; box-shadow: 0 4px 0 #f57f17; }
        .collect-btn:disabled { background: #718093; box-shadow: none; cursor: not-allowed; color: #aaa; }
    </style>
</head>
<body>
    <audio id="bgMusic" loop preload="auto">
        <source src="https://ia801503.us.archive.org/15/items/zombie-tsunami-theme-song/Zombie%20Tsunami%20Theme%20Song.mp3" type="audio/mpeg">
    </audio>

    <div id="gameContainer">
        <canvas id="gameCanvas" width="800" height="450"></canvas>

        <div id="menuOverlay">
            <div class="logo-container">
                <h1 class="logo-title">ZOMBIE</h1>
                <div class="logo-sub">TSUNAMI</div>
            </div>

            <div class="top-right-btns">
                <div class="btn-icon" id="musicToggleBtn" title="Bật/Tắt Nhạc">🔊</div>
                <div class="btn-icon">⚙️</div>
            </div>

            <div class="side-menu-right">
                <div class="btn-side" id="openMissionBtn"><span>🧪</span> MISSION</div>
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

        <!-- MARKET MODAL -->
        <div id="marketModal" class="modal-overlay">
            <div class="modal-box">
                <div class="modal-header">
                    <div>🛒 MARKET (Xu: 🪙 <span id="marketCoinText">0</span>)</div>
                    <div class="close-btn" id="closeMarketBtn">✖</div>
                </div>
                <div class="market-tabs">
                    <div class="tab-btn active" id="tabOutfits">TRANG PHỤC</div>
                    <div class="tab-btn" id="tabHats">PHỤ KIỆN</div>
                </div>
                
                <div class="market-content" id="contentOutfits">
                    <div class="shop-item">
                        <div class="shop-img">🩹</div>
                        <div class="shop-title">Xác Ướp (Mummy)</div>
                        <button class="buy-btn" id="buyMummyBtn">300 Xu</button>
                    </div>
                    <div class="shop-item coming-soon">
                        <div class="shop-img">🧟</div>
                        <div class="shop-title">???</div>
                        <div class="cs-tag">COMING SOON</div>
                        <button class="buy-btn" disabled>Khóa</button>
                    </div>
                </div>

                <div class="market-content" id="contentHats" style="display: none;">
                    <div class="shop-item">
                        <div class="shop-img">🤠</div>
                        <div class="shop-title">Mũ Cao Bồi</div>
                        <button class="buy-btn" id="buyHatBtn">200 Xu</button>
                    </div>
                    <div class="shop-item">
                        <div class="shop-img">🎃</div>
                        <div class="shop-title">Đầu Bí Ngô</div>
                        <button class="buy-btn" id="buyPumpkinBtn">200 Xu</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- MISSION MODAL -->
        <div id="missionModal" class="modal-overlay">
            <div class="modal-box">
                <div class="modal-header">
                    <div>📜 MISSIONS</div>
                    <div class="close-btn" id="closeMissionBtn">✖</div>
                </div>
                <div class="mission-list">
                    <div class="mission-card">
                        <div class="mission-icon">🧟</div>
                        <div class="mission-info">
                            <div class="mission-title">Ăn thịt tổng cộng 100 người (Thưởng 100 Xu)</div>
                            <div class="mission-progress">Tiến độ: <span id="m1Progress">0</span>/100</div>
                        </div>
                        <button class="collect-btn" id="m1Btn" disabled>COLLECT</button>
                    </div>

                    <div class="mission-card">
                        <div class="mission-icon">🧠</div>
                        <div class="mission-info">
                            <div class="mission-title">Ăn thịt 10 người trong 1 màn chơi (Thưởng 50 Xu)</div>
                            <div class="mission-progress">Tiến độ: Kỷ lục <span id="m2Progress">0</span>/10</div>
                        </div>
                        <button class="collect-btn" id="m2Btn" disabled>COLLECT</button>
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

        const bgMusic = document.getElementById('bgMusic');
        const musicToggleBtn = document.getElementById('musicToggleBtn');
        let isMuted = false;

        function playMusic() {
            if (!isMuted) {
                bgMusic.play().catch(e => console.log("Audio play blocked: " + e));
            }
        }

        function stopMusic() {
            bgMusic.pause();
            bgMusic.currentTime = 0;
        }

        musicToggleBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            isMuted = !isMuted;
            if (isMuted) {
                bgMusic.pause();
                musicToggleBtn.innerText = '🔇';
            } else {
                musicToggleBtn.innerText = '🔊';
                if (gameState === 'PLAYING') bgMusic.play();
            }
        });

        const marketModal = document.getElementById('marketModal');
        const openMarketBtn = document.getElementById('openMarketBtn');
        const closeMarketBtn = document.getElementById('closeMarketBtn');
        const marketCoinText = document.getElementById('marketCoinText');

        const missionModal = document.getElementById('missionModal');
        const openMissionBtn = document.getElementById('openMissionBtn');
        const closeMissionBtn = document.getElementById('closeMissionBtn');

        const m1Progress = document.getElementById('m1Progress');
        const m2Progress = document.getElementById('m2Progress');
        const m1Btn = document.getElementById('m1Btn');
        const m2Btn = document.getElementById('m2Btn');

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
        let totalEatenHumans = parseInt(localStorage.getItem('zt_total_eaten') || '0');
        let maxSingleRunEaten = parseInt(localStorage.getItem('zt_max_single_eaten') || '0');

        let m1Claimed = localStorage.getItem('zt_m1_claimed') === 'true';
        let m2Claimed = localStorage.getItem('zt_m2_claimed') === 'true';

        let equippedOutfit = localStorage.getItem('zt_equipped_outfit') || 'NONE';
        let equippedHat = localStorage.getItem('zt_equipped_hat') || 'NONE';
        let ownedItems = JSON.parse(localStorage.getItem('zt_owned_items') || '[]');

        function saveUserData() {
            localStorage.setItem('zt_total_coins', totalCoins);
            localStorage.setItem('zt_total_eaten', totalEatenHumans);
            localStorage.setItem('zt_max_single_eaten', maxSingleRunEaten);
            localStorage.setItem('zt_m1_claimed', m1Claimed);
            localStorage.setItem('zt_m2_claimed', m2Claimed);
            localStorage.setItem('zt_equipped_outfit', equippedOutfit);
            localStorage.setItem('zt_equipped_hat', equippedHat);
            localStorage.setItem('zt_owned_items', JSON.stringify(ownedItems));
            updateMarketUI();
            updateMissionUI();
        }

        function updateMarketUI() {
            marketCoinText.innerText = totalCoins;
            if (ownedItems.includes('MUMMY')) {
                buyMummyBtn.innerText = equippedOutfit === 'MUMMY' ? 'Đang Mặc' : 'Mặc Vào';
                buyMummyBtn.className = equippedOutfit === 'MUMMY' ? 'buy-btn equipped' : 'buy-btn';
            } else buyMummyBtn.innerText = '300 Xu';

            if (ownedItems.includes('HAT')) {
                buyHatBtn.innerText = equippedHat === 'HAT' ? 'Đang Đội' : 'Đội Vào';
                buyHatBtn.className = equippedHat === 'HAT' ? 'buy-btn equipped' : 'buy-btn';
            } else buyHatBtn.innerText = '200 Xu';

            if (ownedItems.includes('PUMPKIN')) {
                buyPumpkinBtn.innerText = equippedHat === 'PUMPKIN' ? 'Đang Đội' : 'Đội Vào';
                buyPumpkinBtn.className = equippedHat === 'PUMPKIN' ? 'buy-btn equipped' : 'buy-btn';
            } else buyPumpkinBtn.innerText = '200 Xu';
        }

        function updateMissionUI() {
            m1Progress.innerText = Math.min(totalEatenHumans, 100);
            if (m1Claimed) {
                m1Btn.innerText = 'ĐÃ NHẬN'; m1Btn.disabled = true;
            } else if (totalEatenHumans >= 100) {
                m1Btn.innerText = 'NHẬN 100 XU'; m1Btn.disabled = false;
            } else {
                m1Btn.innerText = 'CHƯA ĐẠT'; m1Btn.disabled = true;
            }

            m2Progress.innerText = Math.min(maxSingleRunEaten, 10);
            if (m2Claimed) {
                m2Btn.innerText = 'ĐÃ NHẬN'; m2Btn.disabled = true;
            } else if (maxSingleRunEaten >= 10) {
                m2Btn.innerText = 'NHẬN 50 XU'; m2Btn.disabled = false;
            } else {
                m2Btn.innerText = 'CHƯA ĐẠT'; m2Btn.disabled = true;
            }
        }

        m1Btn.addEventListener('click', () => {
            if (!m1Claimed && totalEatenHumans >= 100) {
                m1Claimed = true; totalCoins += 100; saveUserData();
            }
        });

        m2Btn.addEventListener('click', () => {
            if (!m2Claimed && maxSingleRunEaten >= 10) {
                m2Claimed = true; totalCoins += 50; saveUserData();
            }
        });

        tabOutfits.addEventListener('click', () => {
            tabOutfits.classList.add('active'); tabHats.classList.remove('active');
            contentOutfits.style.display = 'flex'; contentHats.style.display = 'none';
        });
        tabHats.addEventListener('click', () => {
            tabHats.classList.add('active'); tabOutfits.classList.remove('active');
            contentHats.style.display = 'flex'; contentOutfits.style.display = 'none';
        });

        openMarketBtn.addEventListener('click', () => { updateMarketUI(); marketModal.style.display = 'flex'; });
        closeMarketBtn.addEventListener('click', () => { marketModal.style.display = 'none'; });

        openMissionBtn.addEventListener('click', () => { updateMissionUI(); missionModal.style.display = 'flex'; });
        closeMissionBtn.addEventListener('click', () => { missionModal.style.display = 'none'; });

        buyMummyBtn.addEventListener('click', () => {
            if (!ownedItems.includes('MUMMY')) {
                if (totalCoins >= 300) { totalCoins -= 300; ownedItems.push('MUMMY'); equippedOutfit = 'MUMMY'; }
                else alert('Bạn không đủ xu!');
            } else equippedOutfit = equippedOutfit === 'MUMMY' ? 'NONE' : 'MUMMY';
            saveUserData();
        });

        buyHatBtn.addEventListener('click', () => {
            if (!ownedItems.includes('HAT')) {
                if (totalCoins >= 200) { totalCoins -= 200; ownedItems.push('HAT'); equippedHat = 'HAT'; }
                else alert('Bạn không đủ xu!');
            } else equippedHat = equippedHat === 'HAT' ? 'NONE' : 'HAT';
            saveUserData();
        });

        buyPumpkinBtn.addEventListener('click', () => {
            if (!ownedItems.includes('PUMPKIN')) {
                if (totalCoins >= 200) { totalCoins -= 200; ownedItems.push('PUMPKIN'); equippedHat = 'PUMPKIN'; }
                else alert('Bạn không đủ xu!');
            } else equippedHat = equippedHat === 'PUMPKIN' ? 'NONE' : 'PUMPKIN';
            saveUserData();
        });

        let currentCoins = 0;
        let speed = 4.5;
        let frame = 0;

        const gravity = 0.65;
        const defaultGroundY = 330;

        let zombies = [{ x: 180, y: defaultGroundY - 20, vy: 0, isGrounded: true, legAngle: 0, variant: 0 }];
        let humans = [];
        let obstacles = [];
        let pits = [];
        let powerups = [];
        let coinTrails = [];
        let particles = [];
        let bgOffset = 0;

        let tsunamiActive = false; let tsunamiTimer = 0;
        let giantActive = false; let giantTimer = 0;

        function addParticles(x, y, color, count = 12) {
            for(let i=0; i<count; i++) {
                particles.push({
                    x: x, y: y,
                    vx: (Math.random() - 0.5) * 8, vy: (Math.random() - 0.5) * 8,
                    life: 25, color: color
                });
            }
        }

        function startGame() {
            resetGame();
            gameState = 'PLAYING';
            menuOverlay.style.display = 'none';
            playMusic();
        }

        playBtn.addEventListener('click', startGame);

        function handleInput() {
            playMusic();
            if (gameState === 'GAMEOVER') {
                gameState = 'MENU';
                menuOverlay.style.display = 'flex';
                stopMusic();
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
                if (gameState === 'MENU' && marketModal.style.display !== 'flex' && missionModal.style.display !== 'flex') startGame();
                else handleInput();
            }
        });
        canvas.addEventListener('touchstart', (e) => { e.preventDefault(); handleInput(); });
        canvas.addEventListener('mousedown', () => { handleInput(); });

        function resetGame() {
            score = 0; currentCoins = 0; speed = 4.5; frame = 0;
            zombies = [{ x: 180, y: defaultGroundY - 20, vy: 0, isGrounded: true, legAngle: 0, variant: 0 }];
            humans = []; obstacles = []; pits = []; powerups = []; coinTrails = []; particles = [];
            tsunamiActive = false; tsunamiTimer = 0;
            giantActive = false; giantTimer = 0;
        }

        function isOverPit(x, width = 20) {
            return pits.some(p => (x + width > p.x) && (x < p.x + p.width));
        }

        function triggerGameOver() {
            gameState = 'GAMEOVER';
            stopMusic();
            if (score > bestScore) { bestScore = score; localStorage.setItem('zt_best_score', bestScore); bestScoreText.innerText = bestScore; }
        }

        function update() {
            frame++;
            bgOffset += (gameState === 'MENU' ? 1.5 : speed);

            if (gameState !== 'PLAYING') return;

            speed = 4.5 + Math.floor(frame / 600) * 0.4;

            if (tsunamiActive) { tsunamiTimer--; if (tsunamiTimer <= 0) tsunamiActive = false; }
            if (giantActive) { giantTimer--; if (giantTimer <= 0) giantActive = false; }

            // Spawn Hố
            if (frame % 230 === 0 && Math.random() > 0.35) {
                let pitWidth = 85 + Math.random() * 65;
                pits.push({ x: 850, width: pitWidth });
            }

            // Spawn Xu
            if (frame % 160 === 0 && Math.random() < 0.6) {
                let count = 5 + Math.floor(Math.random() * 4);
                let startX = 850;
                let coinY = defaultGroundY - 40 - (Math.random() > 0.5 ? 40 : 0);
                for(let c = 0; c < count; c++) {
                    coinTrails.push({ x: startX + c * 24, y: coinY, collected: false });
                }
            }

            // Spawn Hộp ?
            if (frame % 850 === 0 && !tsunamiActive && !giantActive && Math.random() < 0.6) {
                let spawnX = 850;
                if (!isOverPit(spawnX, 40)) {
                    powerups.push({ x: spawnX, y: defaultGroundY - 60, w: 38, h: 38, collected: false });
                }
            }

            // Spawn Chướng ngại vật
            if (frame % 115 === 0) {
                let spawnX = 850;
                if (!isOverPit(spawnX, 150)) {
                    let rand = Math.random();
                    if (rand < 0.32) {
                        let gender = Math.random() > 0.5 ? 'MALE' : 'FEMALE';
                        humans.push({ x: spawnX, y: defaultGroundY - 20, gender: gender, eaten: false });
                    } else if (rand < 0.62) {
                        obstacles.push({ x: spawnX, y: defaultGroundY - 45, w: 90, h: 42, type: 'CAR', reqZombies: 4, peopleInside: 3, hitCooldown: 0 });
                    } else if (rand < 0.80) {
                        obstacles.push({ x: spawnX, y: defaultGroundY - 62, w: 125, h: 58, type: 'BUS', reqZombies: 6, peopleInside: 6, hitCooldown: 0 });
                    } else if (rand < 0.88) {
                        obstacles.push({ x: spawnX, y: defaultGroundY - 85, w: 150, h: 55, type: 'HELI', reqZombies: 8, peopleInside: 8, hitCooldown: 0 });
                    } else {
                        obstacles.push({ x: spawnX, y: defaultGroundY - 45, w: 42, h: 42, type: 'BOMB' });
                    }
                }
            }

            pits.forEach(p => p.x -= speed);
            pits = pits.filter(p => p.x + p.width > -50);

            // Xu
            coinTrails.forEach(c => {
                c.x -= speed;
                if (!c.collected) {
                    zombies.forEach(z => {
                        if (Math.abs(z.x - c.x) < 25 && Math.abs(z.y - c.y) < 30) {
                            c.collected = true;
                            currentCoins += 1; totalCoins += 1; saveUserData();
                            addParticles(c.x, c.y, '#fbc02d', 6);
                        }
                    });
                }
            });
            coinTrails = coinTrails.filter(c => c.x > -30 && !c.collected);

            // Ăn Hộp Bổ Trợ
            powerups.forEach((pw) => {
                pw.x -= speed;
                let leader = zombies[0];
                if (!pw.collected && leader && Math.abs(leader.x - pw.x) < 35 && Math.abs(leader.y - pw.y) < 40) {
                    pw.collected = true;
                    if (Math.random() < 0.5) {
                        tsunamiActive = true; tsunamiTimer = 260; giantActive = false;
                        addParticles(pw.x, pw.y, '#00e5ff', 35);
                    } else {
                        giantActive = true; giantTimer = 260; tsunamiActive = false;
                        addParticles(pw.x, pw.y, '#76ba1b', 35);
                    }
                }
            });
            powerups = powerups.filter(p => p.x > -50 && !p.collected);

            // VA CHẠM XE & MÁY BAY
            let isBlockedByVehicle = false;

            for (let obsIdx = obstacles.length - 1; obsIdx >= 0; obsIdx--) {
                let obs = obstacles[obsIdx];
                obs.x -= speed;
                if (obs.hitCooldown > 0) obs.hitCooldown--;

                if (tsunamiActive || giantActive) {
                    if (Math.abs(zombies[0].x - obs.x) < 130) {
                        addParticles(obs.x + obs.w/2, obs.y, giantActive ? '#e040fb' : '#00e5ff', 30);
                        if (obs.type === 'CAR' || obs.type === 'BUS' || obs.type === 'HELI') {
                            score += obs.peopleInside; currentCoins += obs.peopleInside * 10; totalCoins += obs.peopleInside * 10;
                            totalEatenHumans += obs.peopleInside;
                            if (score > maxSingleRunEaten) maxSingleRunEaten = score;
                            saveUserData();
                            for (let k = 0; k < obs.peopleInside; k++) {
                                if (zombies.length < 30) {
                                    let tail = zombies[zombies.length - 1];
                                    let newVariant = Math.floor(Math.random() * 3);
                                    zombies.push({ x: tail.x - 20, y: tail.y, vy: 0, isGrounded: true, legAngle: 0, variant: newVariant });
                                }
                            }
                        } else if (obs.type === 'BOMB') { score += 2; }
                        obstacles.splice(obsIdx, 1);
                    }
                } else {
                    if (obs.type === 'CAR' || obs.type === 'BUS' || obs.type === 'HELI') {
                        let leader = zombies[0];
                        if (leader && leader.x + 15 >= obs.x && leader.x - 15 <= obs.x + obs.w && leader.y > obs.y - 10) {
                            if (zombies.length >= obs.reqZombies) {
                                addParticles(obs.x + obs.w/2, obs.y + obs.h/2, '#ff9800', 35);
                                score += obs.peopleInside; currentCoins += obs.peopleInside * 10; totalCoins += obs.peopleInside * 10;
                                totalEatenHumans += obs.peopleInside;
                                if (score > maxSingleRunEaten) maxSingleRunEaten = score;
                                saveUserData();
                                for (let k = 0; k < obs.peopleInside; k++) {
                                    if (zombies.length < 30) {
                                        let tail = zombies[zombies.length - 1];
                                        let newVariant = Math.floor(Math.random() * 3);
                                        zombies.push({ x: tail.x - 22, y: tail.y, vy: 0, isGrounded: true, legAngle: 0, variant: newVariant });
                                    }
                                }
                                obstacles.splice(obsIdx, 1);
                            } else {
                                isBlockedByVehicle = true;
                                if (obs.hitCooldown === 0) {
                                    obs.hitCooldown = 25;
                                    let victim = zombies.pop();
                                    if (victim) addParticles(victim.x, victim.y, '#ff1744', 25);
                                    if (zombies.length === 0) { triggerGameOver(); return; }
                                }
                            }
                        }
                    } else if (obs.type === 'BOMB') {
                        let bombCenterX = obs.x + 21; let bombCenterY = obs.y + 21;
                        for (let i = zombies.length - 1; i >= 0; i--) {
                            let z = zombies[i];
                            let dist = Math.hypot(z.x - bombCenterX, z.y - bombCenterY);
                            if (dist < 90) { 
                                addParticles(bombCenterX, bombCenterY, '#ff1744', 35);
                                zombies.splice(i, 1); obstacles.splice(obsIdx, 1); break;
                            }
                        }
                    }
                }
            }

            // XỬ LÝ HỐ RƠI VỰC CHUẨN NGUYÊN TÁC
            for (let i = zombies.length - 1; i >= 0; i--) {
                let z = zombies[i];

                if (tsunamiActive) {
                    z.y = defaultGroundY - 110 + Math.sin(frame * 0.15 + i * 0.4) * 8;
                    z.vy = 0; z.isGrounded = true;
                } else if (giantActive) {
                    z.y = defaultGroundY - 35; z.vy = 0; z.isGrounded = true;
                } else {
                    z.vy += gravity; z.y += z.vy;
                    let onPit = isOverPit(z.x, 10);
                    let standingOnVehicle = false;

                    obstacles.forEach((obs) => {
                        if (obs.type === 'CAR' || obs.type === 'BUS' || obs.type === 'HELI') {
                            if (z.x >= obs.x - 8 && z.x <= obs.x + obs.w + 8) {
                                let roofY = obs.y - 16;
                                if (z.y >= roofY - 5 && z.y <= obs.y + 12 && z.vy >= 0) {
                                    z.y = roofY; z.vy = 0; z.isGrounded = true; standingOnVehicle = true;
                                }
                            }
                        }
                    });

                    if (!standingOnVehicle) {
                        if (!onPit && z.y >= defaultGroundY - 20) {
                            z.y = defaultGroundY - 20; z.vy = 0; z.isGrounded = true;
                        } else if (onPit) { 
                            z.isGrounded = false; // Bắt buộc rơi xuống hố nếu không nhảy
                        }
                    }
                }

                z.legAngle += z.isGrounded ? 0.22 : 0.08;
                if (isBlockedByVehicle && i === 0) z.x = Math.max(100, z.x - speed);
                
                // Rơi xuống đáy vực thì chết hẳn
                if (z.y > canvas.height + 30) { 
                    addParticles(z.x, canvas.height - 10, '#76ba1b', 14); 
                    zombies.splice(i, 1); 
                }
            }

            if (zombies.length === 0) {
                triggerGameOver();
                return;
            }

            // Ăn người
            humans.forEach((h) => {
                h.x -= speed;
                let leader = zombies[0];

                if (tsunamiActive || giantActive) {
                    if (h.x < 450 && !h.eaten) {
                        h.eaten = true; score += 1; currentCoins += 5; totalCoins += 5;
                        totalEatenHumans += 1;
                        if (score > maxSingleRunEaten) maxSingleRunEaten = score;
                        saveUserData();
                        addParticles(h.x, h.y - 10, giantActive ? '#e040fb' : '#00e5ff', 15);
                        if (zombies.length < 30) {
                            let tail = zombies[zombies.length - 1];
                            let newVariant = Math.floor(Math.random() * 3);
                            zombies.push({ x: tail.x - 20, y: tail.y, vy: 0, isGrounded: true, legAngle: 0, variant: newVariant });
                        }
                    }
                } else {
                    if (!h.eaten && leader && Math.abs(leader.x - h.x) < 35 && Math.abs(leader.y - h.y) < 60) {
                        h.eaten = true; score += 1; currentCoins += 5; totalCoins += 5;
                        totalEatenHumans += 1;
                        if (score > maxSingleRunEaten) maxSingleRunEaten = score;
                        saveUserData();
                        addParticles(h.x, h.y - 10, '#76ba1b', 15);
                        if (zombies.length < 30) {
                            let tail = zombies[zombies.length - 1];
                            let newVariant = Math.floor(Math.random() * 3);
                            zombies.push({ x: tail.x - 22, y: tail.y, vy: 0, isGrounded: tail.isGrounded, legAngle: 0, variant: newVariant });
                        }
                    }
                }
            });

            humans = humans.filter(h => h.x > -50 && !h.eaten);
            obstacles = obstacles.filter(o => o.x > -180);

            particles.forEach(p => { p.x += p.vx; p.y += p.vy; p.life--; });
            particles = particles.filter(p => p.life > 0);
        }

        // VẼ MAP BÃI BIỂN
        function drawBeachMap() {
            let skyGrad = ctx.createLinearGradient(0, 0, 0, 220);
            skyGrad.addColorStop(0, '#00b0ff'); skyGrad.addColorStop(1, '#80d8ff');
            ctx.fillStyle = skyGrad; ctx.fillRect(0, 0, canvas.width, 220);

            ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
            let cloudX = (300 - bgOffset * 0.15) % 900; if (cloudX < -100) cloudX += 900;
            ctx.beginPath(); ctx.arc(cloudX, 50, 22, 0, Math.PI*2); ctx.arc(cloudX + 30, 42, 30, 0, Math.PI*2); ctx.arc(cloudX + 65, 50, 22, 0, Math.PI*2); ctx.fill();

            let seaGrad = ctx.createLinearGradient(0, 190, 0, 310);
            seaGrad.addColorStop(0, '#0097a7'); seaGrad.addColorStop(0.5, '#00acc1'); seaGrad.addColorStop(1, '#26c6da');
            ctx.fillStyle = seaGrad; ctx.fillRect(0, 190, canvas.width, 120);

            for (let b = 0; b < 3; b++) {
                let boatX = (150 + b * 280 - bgOffset * 0.3) % 900; if (boatX < -50) boatX += 900;
                ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.moveTo(boatX, 215); ctx.lineTo(boatX + 10, 200); ctx.lineTo(boatX + 10, 215); ctx.fill();
                ctx.fillStyle = '#8d6e63'; ctx.fillRect(boatX + 2, 215, 16, 4);
            }

            ctx.fillStyle = '#ffe082'; ctx.fillRect(0, 280, canvas.width, 50);

            for (let hIdx = 0; hIdx < 3; hIdx++) {
                let houseX = (180 + hIdx * 300 - bgOffset * 0.6) % 900; if (houseX < -120) houseX += 900;
                ctx.fillStyle = hIdx % 2 === 0 ? '#b2dfdb' : '#ffcdd2'; ctx.fillRect(houseX, 210, 80, 70);
                ctx.fillStyle = '#e57373'; ctx.beginPath(); ctx.moveTo(houseX - 8, 210); ctx.lineTo(houseX + 40, 165); ctx.lineTo(houseX + 88, 210); ctx.fill();
                ctx.fillStyle = '#ffffff'; ctx.fillRect(houseX + 12, 220, 22, 22);
                ctx.fillStyle = '#5d4037'; ctx.fillRect(houseX + 46, 240, 20, 40);
            }

            for (let tIdx = 0; tIdx < 2; tIdx++) {
                let treeX = (90 + tIdx * 460 - bgOffset * 0.8) % 900; if (treeX < -100) treeX += 900;
                ctx.strokeStyle = '#6d4c41'; ctx.lineWidth = 14; ctx.beginPath(); ctx.moveTo(treeX, 310); ctx.quadraticCurveTo(treeX - 15, 230, treeX + 15, 160); ctx.stroke();
                ctx.fillStyle = '#2e7d32';
                for (let a = 0; a < 5; a++) {
                    let ang = (a * Math.PI) / 2.5 - 0.2; ctx.beginPath(); ctx.ellipse(treeX + 15 + Math.cos(ang)*28, 160 + Math.sin(ang)*18, 28, 10, ang, 0, Math.PI*2); ctx.fill();
                }
            }
        }

        function drawBackground() {
            drawBeachMap();

            ctx.fillStyle = '#212121'; ctx.fillRect(0, defaultGroundY, canvas.width, 16);
            ctx.fillStyle = '#37474f'; ctx.fillRect(0, defaultGroundY + 16, canvas.width, canvas.height - defaultGroundY - 16);

            pits.forEach(p => {
                ctx.fillStyle = '#0a0a0a'; ctx.fillRect(p.x, defaultGroundY, p.width, canvas.height - defaultGroundY);
                ctx.fillStyle = '#263238'; ctx.fillRect(p.x - 8, defaultGroundY, 8, canvas.height - defaultGroundY); ctx.fillRect(p.x + p.width, defaultGroundY, 8, canvas.height - defaultGroundY);
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
                ctx.beginPath(); ctx.moveTo(-100, defaultGroundY + 50); ctx.lineTo(-100, 180);
                ctx.bezierCurveTo(waveX - 120, 160, waveX - 40, 130, waveX, 170);
                ctx.bezierCurveTo(waveX + 30, 200, waveX + 50, 270, waveX + 20, defaultGroundY + 50);
                ctx.closePath(); ctx.fill();
            }
        }

        function drawGiantMonster() {
            ctx.save();
            let gX = 180; let gY = defaultGroundY - 50;
            let brainGrad = ctx.createRadialGradient(gX - 12, gY - 25, 8, gX, gY, 68);
            brainGrad.addColorStop(0, '#eeff41'); brainGrad.addColorStop(0.6, '#76ba1b'); brainGrad.addColorStop(1, '#1b5e20');
            ctx.fillStyle = brainGrad; ctx.beginPath(); ctx.arc(gX, gY - 10, 68, 0, Math.PI * 2); ctx.fill();

            let eyes = [
                {x: gX - 32, y: gY - 28, r: 18}, {x: gX + 10, y: gY - 35, r: 20},
                {x: gX + 38, y: gY - 12, r: 15}, {x: gX - 8, y: gY - 5, r: 24}
            ];
            eyes.forEach(e => {
                ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.arc(e.x, e.y, e.r, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = '#00e5ff'; ctx.beginPath(); ctx.arc(e.x + 3, e.y, e.r * 0.55, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = '#000000'; ctx.beginPath(); ctx.arc(e.x + 4, e.y, e.r * 0.25, 0, Math.PI*2); ctx.fill();
            });

            ctx.fillStyle = '#1b5e20'; ctx.beginPath(); ctx.ellipse(gX + 15, gY + 28, 32, 14, 0.1, 0, Math.PI * 2); ctx.fill();

            let laserGrad = ctx.createLinearGradient(gX + 40, gY - 10, 800, gY - 10);
            laserGrad.addColorStop(0, '#ffffff'); laserGrad.addColorStop(0.2, '#ff007f'); laserGrad.addColorStop(0.7, '#e040fb'); laserGrad.addColorStop(1, '#ffffff');
            ctx.strokeStyle = laserGrad; ctx.lineWidth = 22 + Math.sin(frame * 0.4) * 6;
            ctx.beginPath(); ctx.moveTo(gX + 40, gY - 10); ctx.lineTo(800, gY - 10); ctx.stroke();
            ctx.restore();
        }

        // HÀM VẼ ZOMBIE NGUYÊN TÁC CHUẨN 100% (ẢNH 1)
        function drawZombie(z, scale = 1, offsetX = 0, offsetY = 0) {
            ctx.save();
            ctx.translate(z.x + offsetX, z.y + offsetY);
            ctx.scale(scale, scale);

            let isNearHuman = humans.some(h => h.x - z.x > 0 && h.x - z.x < 100);
            let v = z.variant || 0;

            let shirtColor = v === 0 ? '#1e272e' : (v === 1 ? '#d63031' : '#f1c40f');
            let pantColor = v === 0 ? '#4b382a' : (v === 1 ? '#880e4f' : '#2d3436');

            if (equippedOutfit === 'MUMMY') {
                ctx.strokeStyle = '#d7ccc8'; ctx.lineWidth = 5;
                ctx.beginPath(); ctx.moveTo(-4, 6); ctx.lineTo(-4 + Math.sin(z.legAngle)*7, 18); ctx.moveTo(4, 6); ctx.lineTo(4 - Math.sin(z.legAngle)*7, 18); ctx.stroke();
                ctx.fillStyle = '#efebe9'; ctx.fillRect(-9, -5, 18, 14);
                ctx.fillStyle = '#d7ccc8'; ctx.beginPath(); ctx.arc(0, -15, 16, 0, Math.PI * 2); ctx.fill();
                ctx.fillStyle = '#111111'; ctx.fillRect(-10, -21, 20, 9);
                ctx.fillStyle = '#ff1744'; ctx.beginPath(); ctx.arc(-2, -16, 3, 0, Math.PI * 2); ctx.arc(6, -16, 3, 0, Math.PI * 2); ctx.fill();
            } else {
                // Đôi chân ngắn chạy tung tăng
                ctx.strokeStyle = '#76ba1b'; ctx.lineWidth = 5;
                ctx.beginPath(); ctx.moveTo(-5, 6); ctx.lineTo(-5 + Math.sin(z.legAngle)*8, 18); ctx.moveTo(5, 6); ctx.lineTo(5 - Math.sin(z.legAngle)*8, 18); ctx.stroke();

                // Bàn chân tròn
                ctx.fillStyle = '#558b2f';
                ctx.beginPath(); ctx.arc(-5 + Math.sin(z.legAngle)*8, 19, 3.5, 0, Math.PI*2); ctx.arc(5 - Math.sin(z.legAngle)*8, 19, 3.5, 0, Math.PI*2); ctx.fill();

                // Quần đùi xắn
                ctx.fillStyle = pantColor; ctx.fillRect(-8, 2, 16, 7);
                // Áo ngắn tay
                ctx.fillStyle = shirtColor; ctx.fillRect(-9, -6, 18, 10);

                // Đầu zombie hình quả lê xanh mướt (Hình 1)
                ctx.fillStyle = '#76ba1b';
                ctx.beginPath();
                ctx.ellipse(0, -16, 17, 15, 0.1, 0, Math.PI * 2);
                ctx.fill();

                // Mắt lồi to siêu ngộ nghĩnh
                ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.arc(8, -18, 10, 0, Math.PI * 2); ctx.fill();
                ctx.fillStyle = '#00e5ff'; ctx.beginPath(); ctx.arc(9, -18, 5.5, 0, Math.PI * 2); ctx.fill();
                ctx.fillStyle = '#111111'; ctx.beginPath(); ctx.arc(10, -18, 2.5, 0, Math.PI * 2); ctx.fill();
                ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.arc(8, -20, 1.5, 0, Math.PI * 2); ctx.fill(); // Bóng mắt
                
                // Mồm & Răng cưa nhọn
                if (isNearHuman) {
                    ctx.fillStyle = '#111111'; ctx.beginPath(); ctx.arc(10, -8, 8, 0, Math.PI*2); ctx.fill();
                    ctx.fillStyle = '#ffffff';
                    ctx.beginPath(); ctx.moveTo(6, -11); ctx.lineTo(8, -5); ctx.lineTo(10, -11); ctx.fill();
                } else {
                    ctx.fillStyle = '#1b5e20'; ctx.beginPath(); ctx.arc(8, -8, 5, 0, Math.PI); ctx.fill();
                    ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.moveTo(5, -8); ctx.lineTo(7, -4); ctx.lineTo(9, -8); ctx.fill();
                }

                // Đôi tay giơ về trước vươn ra (Hình 1)
                ctx.strokeStyle = '#76ba1b'; ctx.lineWidth = 4;
                ctx.beginPath(); ctx.moveTo(3, -2); ctx.lineTo(16, 2); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(3, 1); ctx.lineTo(15, 6); ctx.stroke();
            }

            if (equippedHat === 'HAT') {
                ctx.fillStyle = '#795548'; ctx.fillRect(-18, -33, 36, 4); ctx.fillRect(-10, -44, 20, 12);
            } else if (equippedHat === 'PUMPKIN') {
                ctx.fillStyle = '#ff6f00'; ctx.beginPath(); ctx.arc(0, -33, 12, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = '#33691e'; ctx.fillRect(-2, -48, 4, 6);
            }

            ctx.restore();
        }

        function drawMysteryBox(pw) {
            ctx.save();
            ctx.translate(pw.x + pw.w/2, pw.y + pw.h/2 + Math.sin(frame * 0.1) * 4);
            ctx.rotate(-0.08);

            ctx.fillStyle = '#dcdde1'; ctx.fillRect(-pw.w/2 + 4, -pw.h/2 + 4, pw.w, pw.h);
            ctx.fillStyle = '#ffffff'; ctx.fillRect(-pw.w/2, -pw.h/2, pw.w, pw.h);
            ctx.strokeStyle = '#2f3640'; ctx.lineWidth = 3; ctx.strokeRect(-pw.w/2, -pw.h/2, pw.w, pw.h);

            ctx.fillStyle = '#00a8ff'; ctx.font = '900 26px sans-serif'; ctx.textAlign = 'center';
            ctx.fillText('?', 0, 9);
            ctx.restore();
        }

        function drawBomb(o) {
            ctx.save(); ctx.translate(o.x + 21, o.y + 21);
            let bombGrad = ctx.createRadialGradient(-4, -4, 2, 0, 0, 20);
            bombGrad.addColorStop(0, '#555'); bombGrad.addColorStop(0.7, '#222'); bombGrad.addColorStop(1, '#000');
            ctx.fillStyle = bombGrad; ctx.beginPath(); ctx.arc(0, 0, 19, 0, Math.PI*2); ctx.fill();

            ctx.fillStyle = '#111';
            for (let a = 0; a < 8; a++) {
                let angle = (a * Math.PI) / 4; ctx.beginPath(); ctx.arc(Math.cos(angle) * 19, Math.sin(angle) * 19, 4, 0, Math.PI*2); ctx.fill();
            }

            let glowGrad = ctx.createRadialGradient(0, 0, 2, 0, 0, 10);
            glowGrad.addColorStop(0, '#ffffff'); glowGrad.addColorStop(0.5, '#ff1744'); glowGrad.addColorStop(1, '#b71c1c');
            ctx.fillStyle = glowGrad; ctx.beginPath(); ctx.arc(0, 0, 10 + Math.sin(frame * 0.3) * 2, 0, Math.PI*2); ctx.fill();
            ctx.restore();
        }

        function drawCoin(c) {
            ctx.save(); ctx.translate(c.x, c.y);
            ctx.fillStyle = '#fbc02d'; ctx.beginPath(); ctx.arc(0, 0, 9, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#fff59d'; ctx.beginPath(); ctx.arc(0, 0, 6, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#f57f17'; ctx.font = 'bold 10px sans-serif'; ctx.textAlign = 'center'; ctx.fillText('$', 0, 3.5);
            ctx.restore();
        }

        function drawHuman(h) {
            ctx.save(); ctx.translate(h.x, h.y);
            ctx.fillStyle = '#ffcc80'; ctx.beginPath(); ctx.arc(0, -16, 7, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = h.gender === 'MALE' ? '#5d4037' : '#fbc02d'; ctx.beginPath(); ctx.arc(0, -19, 7, Math.PI, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#000'; ctx.beginPath(); ctx.arc(-2.5, -16, 1.2, 0, Math.PI*2); ctx.arc(2.5, -16, 1.2, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = h.gender === 'MALE' ? '#1e88e5' : '#e91e63'; ctx.fillRect(-5, -9, 10, 10);
            ctx.restore();
        }

        // BẢNG BÓNG THOẠI HÌNH ZOMBIE CHUẨN 100% NGUYÊN TÁC (ẢNH 2)
        function drawZombieRequirementBadge(x, y, reqCount) {
            ctx.save();
            ctx.translate(x, y);

            // Bảng đen viền cam bóng thoại
            ctx.fillStyle = '#111111';
            ctx.beginPath();
            ctx.roundRect(0, 0, 85, 42, 10);
            ctx.fill();
            ctx.strokeStyle = '#ff9800'; ctx.lineWidth = 3; ctx.stroke();

            // Đuôi bóng thoại chỉ xuống chướng ngại vật
            ctx.fillStyle = '#111111';
            ctx.beginPath();
            ctx.moveTo(18, 42); ctx.lineTo(26, 50); ctx.lineTo(34, 42);
            ctx.fill();

            // Đầu Zombie thu nhỏ trong bảng
            ctx.fillStyle = '#76ba1b';
            ctx.beginPath(); ctx.arc(20, 21, 11, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.arc(23, 20, 4.5, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#111'; ctx.beginPath(); ctx.arc(24, 20, 2, 0, Math.PI * 2); ctx.fill();

            // Tỷ số Zombie (Hiện có / Yêu cầu)
            ctx.fillStyle = '#ffffff'; ctx.font = '900 16px sans-serif';
            ctx.fillText(`${zombies.length}`, 38, 26);
            ctx.fillStyle = '#ff3d00';
            ctx.fillText(`/${reqCount}`, 56, 26);
            ctx.restore();
        }

        function drawCar(o) {
            ctx.save(); ctx.translate(o.x, o.y);
            ctx.fillStyle = '#d32f2f'; ctx.fillRect(0, 15, o.w, 18);
            ctx.fillStyle = '#b71c1c'; ctx.fillRect(14, 3, 52, 13);
            ctx.fillStyle = '#81d4fa'; ctx.fillRect(18, 5, 18, 9); ctx.fillRect(42, 5, 20, 9);
            ctx.fillStyle = '#111'; ctx.beginPath(); ctx.arc(18, 33, 8, 0, Math.PI*2); ctx.arc(o.w - 18, 33, 8, 0, Math.PI*2); ctx.fill();
            
            drawZombieRequirementBadge(3, -52, o.reqZombies);
            ctx.restore();
        }

        function drawBus(o) {
            ctx.save(); ctx.translate(o.x, o.y);
            ctx.fillStyle = '#fbc02d'; ctx.fillRect(0, 0, o.w, 48);
            ctx.fillStyle = '#f57f17'; ctx.fillRect(0, 28, o.w, 5);
            ctx.fillStyle = '#81d4fa'; for(let k=0; k<4; k++) ctx.fillRect(10 + (k * 26), 7, 18, 16);
            ctx.fillStyle = '#111'; ctx.beginPath(); ctx.arc(22, 48, 9, 0, Math.PI*2); ctx.arc(o.w - 22, 48, 9, 0, Math.PI*2); ctx.fill();
            
            drawZombieRequirementBadge(20, -52, o.reqZombies);
            ctx.restore();
        }

        // MÁY BAY CHUẨN Z.AIRLINE NGUYÊN TÁC (ẢNH 2)
        function drawHelicopter(o) {
            ctx.save(); ctx.translate(o.x, o.y);
            
            // Thân máy bay màu trắng
            ctx.fillStyle = '#ffffff';
            ctx.beginPath();
            ctx.moveTo(0, 28);
            ctx.bezierCurveTo(0, -10, 45, -18, 125, -10);
            ctx.lineTo(150, 28);
            ctx.lineTo(0, 28);
            ctx.fill();

            // Sọc màu xanh lá đặc trưng Z.Airline
            ctx.fillStyle = '#76ba1b';
            ctx.fillRect(40, 6, 100, 10);

            // Cửa sổ phi công kính xám mờ
            ctx.fillStyle = '#263238';
            ctx.beginPath(); ctx.arc(22, 10, 8, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.arc(20, 8, 2.5, 0, Math.PI*2); ctx.fill();

            // Cửa sổ hành khách dạng chữ nhật bo góc
            ctx.fillStyle = '#263238';
            for(let i=0; i<4; i++) {
                ctx.fillRect(52 + i * 16, 8, 10, 9);
            }

            // Động cơ phản lực phía dưới cánh
            ctx.fillStyle = '#607d8b';
            ctx.fillRect(80, 24, 34, 16);
            ctx.fillStyle = '#111111'; ctx.beginPath(); ctx.arc(97, 40, 6, 0, Math.PI*2); ctx.fill();

            // Chữ Z.AIRLINE nguyên tác (Ảnh 2)
            ctx.fillStyle = '#33691e';
            ctx.font = '900 14px sans-serif';
            ctx.fillText("Z.AIRLINE", 56, -1);

            // Bảng yêu cầu Zombie
            drawZombieRequirementBadge(32, -55, o.reqZombies);
            ctx.restore();
        }

        function draw() {
            drawBackground();

            if (gameState === 'MENU') {
                let demoZ = { x: 220, y: defaultGroundY - 20, legAngle: frame * 0.2, variant: 0 };
                drawZombie(demoZ);
                return;
            }

            coinTrails.forEach(c => drawCoin(c));
            powerups.forEach(pw => drawMysteryBox(pw));
            humans.forEach(h => drawHuman(h));

            obstacles.forEach(o => {
                if (o.type === 'BOMB') drawBomb(o);
                else if (o.type === 'CAR') drawCar(o);
                else if (o.type === 'BUS') drawBus(o);
                else if (o.type === 'HELI') drawHelicopter(o);
            });

            if (giantActive) {
                drawGiantMonster();
            } else {
                zombies.forEach((z, idx) => {
                    let depthScale = 1 - Math.min(idx * 0.012, 0.25);
                    let offsetY = (idx % 2 === 1) ? -Math.min(idx * 1.8, 18) : 0;
                    let offsetX = (idx % 3 === 2) ? -6 : 0;
                    drawZombie(z, depthScale, offsetX, offsetY);
                });
            }

            particles.forEach(p => { ctx.fillStyle = p.color; ctx.fillRect(p.x, p.y, 4, 4); });

            // HUD UI
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
