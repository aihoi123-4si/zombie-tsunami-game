import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Zombie Tsunami Refined Edition", layout="centered")

st.markdown("<h1 style='text-align: center; color: #76ba1b;'>🧟 ZOMBIE TSUNAMI - REFINED EDITION ⚡</h1>", unsafe_allow_html=True)

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
            width: 720px; height: 400px; background: #1e272e; border: 4px solid #fbc02d; border-radius: 16px;
            display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 0 30px rgba(251, 192, 45, 0.4);
        }
        .modal-header { background: #fbc02d; color: #000; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; font-size: 22px; font-weight: bold; }
        .close-btn { background: #d32f2f; color: #fff; border: 2px solid #fff; border-radius: 50%; width: 32px; height: 32px; display: flex; justify-content: center; align-items: center; cursor: pointer; font-size: 18px; }
        
        .market-tabs { display: flex; background: #0f171e; border-bottom: 2px solid #333; }
        .tab-btn { flex: 1; padding: 10px; text-align: center; color: #aaa; font-size: 16px; cursor: pointer; border-right: 1px solid #222; font-weight: bold; }
        .tab-btn.active { background: #1e272e; color: #76ba1b; border-bottom: 3px solid #76ba1b; }
        .market-content { flex: 1; padding: 15px; overflow-y: auto; display: flex; gap: 15px; justify-content: center; align-items: center; }
        
        .shop-item { width: 210px; height: 230px; background: #2f3640; border: 3px solid #485460; border-radius: 12px; display: flex; flex-direction: column; align-items: center; justify-content: space-between; padding: 12px; box-sizing: border-box; position: relative; }
        .shop-item.coming-soon { filter: brightness(0.4); }
        .cs-tag { position: absolute; top: 80px; background: #ff1744; color: #fff; padding: 4px 12px; font-size: 14px; font-weight: bold; border-radius: 4px; transform: rotate(-10deg); }
        .shop-img { font-size: 42px; margin-top: 5px; }
        .shop-title { color: #fff; font-size: 14px; text-align: center; margin-top: 2px; font-weight: bold; }
        .shop-desc { color: #aaa; font-size: 11px; text-align: center; }
        .buy-btn { background: #4cd137; color: #000; border: none; padding: 8px 12px; border-radius: 20px; font-weight: bold; cursor: pointer; font-size: 14px; box-shadow: 0 4px 0 #44bd32; width: 100%; }
        .buy-btn.maxed { background: #718093; color: #fff; box-shadow: none; cursor: not-allowed; }
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
                    <div class="tab-btn" id="tabPowers">SỨC MẠNH</div>
                </div>
                
                <div class="market-content" id="contentOutfits">
                    <div class="shop-item">
                        <div class="shop-img">🩹</div>
                        <div class="shop-title">Xác Ướp (Mummy)</div>
                        <div class="shop-desc">Trang phục cao cấp</div>
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
                        <div class="shop-desc">Phụ kiện phong cách</div>
                        <button class="buy-btn" id="buyHatBtn">200 Xu</button>
                    </div>
                    <div class="shop-item">
                        <div class="shop-img">🎃</div>
                        <div class="shop-title">Đầu Bí Ngô</div>
                        <div class="shop-desc">Phụ kiện Halloween</div>
                        <button class="buy-btn" id="buyPumpkinBtn">200 Xu</button>
                    </div>
                </div>

                <div class="market-content" id="contentPowers" style="display: none;">
                    <div class="shop-item">
                        <div class="shop-img">🧠</div>
                        <div class="shop-title">Zombie Ban Đầu</div>
                        <div class="shop-desc">Cấp hiện tại: <span id="p1LevelLabel">1</span>/3</div>
                        <button class="buy-btn" id="buyPower1Btn">50 Xu</button>
                    </div>
                    <div class="shop-item">
                        <div class="shop-img">⏱️</div>
                        <div class="shop-title">Thời Gian Bổ Trợ</div>
                        <div class="shop-desc">Cấp hiện tại: <span id="p2LevelLabel">1</span>/3</div>
                        <button class="buy-btn" id="buyPower2Btn">50 Xu</button>
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

        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        let audioCtx = null;

        function initAudio() {
            if (!audioCtx) audioCtx = new AudioCtx();
            if (audioCtx.state === 'suspended') audioCtx.resume();
        }

        function playSound(type) {
            if (isMuted) return;
            initAudio();
            if (!audioCtx) return;

            let now = audioCtx.currentTime;

            if (type === 'jump') {
                let osc = audioCtx.createOscillator();
                let gain = audioCtx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(280, now);
                osc.frequency.exponentialRampToValueAtTime(580, now + 0.12);
                gain.gain.setValueAtTime(0.2, now);
                gain.gain.linearRampToValueAtTime(0.01, now + 0.12);
                osc.connect(gain); gain.connect(audioCtx.destination);
                osc.start(now); osc.stop(now + 0.12);
            } else if (type === 'eat') {
                let osc = audioCtx.createOscillator();
                let gain = audioCtx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(150, now);
                osc.frequency.exponentialRampToValueAtTime(350, now + 0.1);
                gain.gain.setValueAtTime(0.3, now);
                gain.gain.linearRampToValueAtTime(0.01, now + 0.1);
                osc.connect(gain); gain.connect(audioCtx.destination);
                osc.start(now); osc.stop(now + 0.1);
            } else if (type === 'coin') {
                let osc = audioCtx.createOscillator();
                let gain = audioCtx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(988, now);
                osc.frequency.setValueAtTime(1318, now + 0.08);
                gain.gain.setValueAtTime(0.18, now);
                gain.gain.linearRampToValueAtTime(0.01, now + 0.18);
                osc.connect(gain); gain.connect(audioCtx.destination);
                osc.start(now); osc.stop(now + 0.18);
            } else if (type === 'powerup') {
                let osc = audioCtx.createOscillator();
                let gain = audioCtx.createGain();
                osc.type = 'square';
                osc.frequency.setValueAtTime(300, now);
                osc.frequency.exponentialRampToValueAtTime(900, now + 0.25);
                gain.gain.setValueAtTime(0.25, now);
                gain.gain.linearRampToValueAtTime(0.01, now + 0.25);
                osc.connect(gain); gain.connect(audioCtx.destination);
                osc.start(now); osc.stop(now + 0.25);
            } else if (type === 'explode') {
                let osc = audioCtx.createOscillator();
                let gain = audioCtx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(120, now);
                osc.frequency.linearRampToValueAtTime(30, now + 0.35);
                gain.gain.setValueAtTime(0.4, now);
                gain.gain.linearRampToValueAtTime(0.01, now + 0.35);
                osc.connect(gain); gain.connect(audioCtx.destination);
                osc.start(now); osc.stop(now + 0.35);
            }
        }

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
        const tabPowers = document.getElementById('tabPowers');
        const contentOutfits = document.getElementById('contentOutfits');
        const contentHats = document.getElementById('contentHats');
        const contentPowers = document.getElementById('contentPowers');

        const buyMummyBtn = document.getElementById('buyMummyBtn');
        const buyHatBtn = document.getElementById('buyHatBtn');
        const buyPumpkinBtn = document.getElementById('buyPumpkinBtn');
        const buyPower1Btn = document.getElementById('buyPower1Btn');
        const buyPower2Btn = document.getElementById('buyPower2Btn');
        const p1LevelLabel = document.getElementById('p1LevelLabel');
        const p2LevelLabel = document.getElementById('p2LevelLabel');

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

        let power1Level = parseInt(localStorage.getItem('zt_p1_level') || '1'); 
        let power2Level = parseInt(localStorage.getItem('zt_p2_level') || '1'); 

        const MAP_LIST = ['BEACH', 'CITY', 'VILLAGE'];
        let currentMap = 'BEACH'; 
        let mapTimer = 0; 
        let shakeDuration = 0;

        function triggerShake(duration = 12) {
            shakeDuration = duration;
        }

        function saveUserData() {
            localStorage.setItem('zt_total_coins', totalCoins);
            localStorage.setItem('zt_total_eaten', totalEatenHumans);
            localStorage.setItem('zt_max_single_eaten', maxSingleRunEaten);
            localStorage.setItem('zt_m1_claimed', m1Claimed);
            localStorage.setItem('zt_m2_claimed', m2Claimed);
            localStorage.setItem('zt_equipped_outfit', equippedOutfit);
            localStorage.setItem('zt_equipped_hat', equippedHat);
            localStorage.setItem('zt_owned_items', JSON.stringify(ownedItems));
            localStorage.setItem('zt_p1_level', power1Level);
            localStorage.setItem('zt_p2_level', power2Level);
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

            p1LevelLabel.innerText = power1Level;
            if (power1Level >= 3) {
                buyPower1Btn.innerText = 'ĐÃ TỐI ĐA';
                buyPower1Btn.className = 'buy-btn maxed';
                buyPower1Btn.disabled = true;
            } else {
                buyPower1Btn.innerText = '50 Xu';
                buyPower1Btn.className = 'buy-btn';
                buyPower1Btn.disabled = false;
            }

            p2LevelLabel.innerText = power2Level;
            if (power2Level >= 3) {
                buyPower2Btn.innerText = 'ĐÃ TỐI ĐA';
                buyPower2Btn.className = 'buy-btn maxed';
                buyPower2Btn.disabled = true;
            } else {
                buyPower2Btn.innerText = '50 Xu';
                buyPower2Btn.className = 'buy-btn';
                buyPower2Btn.disabled = false;
            }
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

        buyPower1Btn.addEventListener('click', () => {
            if (power1Level < 3) {
                if (totalCoins >= 50) {
                    totalCoins -= 50; power1Level++; saveUserData();
                } else alert('Bạn không đủ 50 xu!');
            }
        });

        buyPower2Btn.addEventListener('click', () => {
            if (power2Level < 3) {
                if (totalCoins >= 50) {
                    totalCoins -= 50; power2Level++; saveUserData();
                } else alert('Bạn không đủ 50 xu!');
            }
        });

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
            tabOutfits.classList.add('active'); tabHats.classList.remove('active'); tabPowers.classList.remove('active');
            contentOutfits.style.display = 'flex'; contentHats.style.display = 'none'; contentPowers.style.display = 'none';
        });
        tabHats.addEventListener('click', () => {
            tabHats.classList.add('active'); tabOutfits.classList.remove('active'); tabPowers.classList.remove('active');
            contentHats.style.display = 'flex'; contentOutfits.style.display = 'none'; contentPowers.style.display = 'none';
        });
        tabPowers.addEventListener('click', () => {
            tabPowers.classList.add('active'); tabOutfits.classList.remove('active'); tabHats.classList.remove('active');
            contentPowers.style.display = 'flex'; contentOutfits.style.display = 'none'; contentHats.style.display = 'none';
            updateMarketUI();
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

        let zombies = [];
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
                let jumped = false;
                zombies.forEach((z, idx) => {
                    if (z.isGrounded) {
                        z.vy = -13.5 - (idx * 0.04);
                        z.isGrounded = false;
                        jumped = true;
                    }
                });
                if (jumped) playSound('jump');
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

        function switchRandomMap() {
            let available = MAP_LIST.filter(m => m !== currentMap);
            currentMap = available[Math.floor(Math.random() * available.length)];
        }

        function resetGame() {
            score = 0; currentCoins = 0; speed = 4.5; frame = 0;
            
            let initialCount = power1Level; 
            zombies = [];
            for (let i = 0; i < initialCount; i++) {
                zombies.push({ x: 180 - (i * 22), y: defaultGroundY - 20, vy: 0, isGrounded: true, legAngle: i * 0.5, variant: i % 3 });
            }

            humans = []; obstacles = []; pits = []; powerups = []; coinTrails = []; particles = [];
            tsunamiActive = false; tsunamiTimer = 0;
            giantActive = false; giantTimer = 0;

            currentMap = MAP_LIST[Math.floor(Math.random() * MAP_LIST.length)];
            mapTimer = 0;
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

            mapTimer++;
            if (mapTimer >= 1200) {
                mapTimer = 0;
                switchRandomMap();
            }

            speed = 4.5 + Math.floor(frame / 600) * 0.4;

            let bonusDuration = power2Level === 1 ? 360 : (power2Level === 2 ? 480 : 600);

            if (tsunamiActive) { tsunamiTimer--; if (tsunamiTimer <= 0) tsunamiActive = false; }
            if (giantActive) { giantTimer--; if (giantTimer <= 0) giantActive = false; }

            if (frame % 250 === 0 && Math.random() > 0.35) {
                let pitWidth = 85 + Math.random() * 65;
                pits.push({ x: 850, width: pitWidth });
            }

            if (frame % 160 === 0 && Math.random() < 0.6) {
                let count = 5 + Math.floor(Math.random() * 4);
                let startX = 850;
                let coinY = defaultGroundY - 40 - (Math.random() > 0.5 ? 40 : 0);
                for(let c = 0; c < count; c++) {
                    coinTrails.push({ x: startX + c * 24, y: coinY, collected: false });
                }
            }

            if (frame % 850 === 0 && !tsunamiActive && !giantActive && Math.random() < 0.6) {
                let spawnX = 850;
                if (!isOverPit(spawnX, 40)) {
                    powerups.push({ x: spawnX, y: defaultGroundY - 60, w: 38, h: 38, collected: false });
                }
            }

            if (frame % 130 === 0) {
                let spawnX = 850;
                if (!isOverPit(spawnX, 170)) {
                    let rand = Math.random();
                    if (rand < 0.32) {
                        let gender = Math.random() > 0.5 ? 'MALE' : 'FEMALE';
                        humans.push({ x: spawnX, y: defaultGroundY - 20, gender: gender, eaten: false });
                    } else if (rand < 0.60) {
                        obstacles.push({ x: spawnX, y: defaultGroundY - 45, w: 90, h: 42, type: 'CAR', reqZombies: 4, peopleInside: 3, hitCooldown: 0 });
                    } else if (rand < 0.78) {
                        obstacles.push({ x: spawnX, y: defaultGroundY - 55, w: 145, h: 52, type: 'BUS', reqZombies: 6, peopleInside: 6, hitCooldown: 0 });
                    } else if (rand < 0.88) {
                        obstacles.push({ x: spawnX, y: defaultGroundY - 82, w: 195, h: 62, type: 'HELI', reqZombies: 8, peopleInside: 8, hitCooldown: 0 });
                    } else {
                        obstacles.push({ x: spawnX, y: defaultGroundY - 45, w: 42, h: 42, type: 'BOMB' });
                    }
                }
            }

            pits.forEach(p => p.x -= speed);
            pits = pits.filter(p => p.x + p.width > -50);

            coinTrails.forEach(c => {
                c.x -= speed;
                if (!c.collected) {
                    zombies.forEach(z => {
                        if (Math.abs(z.x - c.x) < 25 && Math.abs(z.y - c.y) < 30) {
                            c.collected = true;
                            currentCoins += 1; totalCoins += 1; saveUserData();
                            playSound('coin');
                            addParticles(c.x, c.y, '#fbc02d', 6);
                        }
                    });
                }
            });
            coinTrails = coinTrails.filter(c => c.x > -30 && !c.collected);

            powerups.forEach((pw) => {
                pw.x -= speed;
                let leader = zombies[0];
                if (!pw.collected && leader && Math.abs(leader.x - pw.x) < 35 && Math.abs(leader.y - pw.y) < 40) {
                    pw.collected = true;
                    playSound('powerup');
                    triggerShake(16);
                    if (Math.random() < 0.5) {
                        tsunamiActive = true; tsunamiTimer = bonusDuration; giantActive = false;
                        addParticles(pw.x, pw.y, '#00e5ff', 35);
                    } else {
                        giantActive = true; giantTimer = bonusDuration; tsunamiActive = false;
                        addParticles(pw.x, pw.y, '#76ba1b', 35);
                    }
                }
            });
            powerups = powerups.filter(p => p.x > -50 && !p.collected);

            let isBlockedByVehicle = false;

            for (let obsIdx = obstacles.length - 1; obsIdx >= 0; obsIdx--) {
                let obs = obstacles[obsIdx];
                obs.x -= speed;
                if (obs.hitCooldown > 0) obs.hitCooldown--;

                if (tsunamiActive || giantActive) {
                    if (Math.abs(zombies[0].x - obs.x) < 140) {
                        playSound('explode');
                        triggerShake(10);
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
                        // SỬA HITBOX THU NHỎ & KHÔNG TÍNH KHU VỰC NÓC XE
                        let isAboveRoof = leader && leader.y < obs.y - 12; // Nếu zombie nhảy trên cao hơn nóc xe -> KHÔNG DỊNH HITBOX NGANG
                        let hitFrontMargin = 5; // Thu nhỏ hitbox va chạm phía trước
                        let hitBackMargin = 10;

                        if (leader && !isAboveRoof && (leader.x + hitFrontMargin >= obs.x && leader.x - hitBackMargin <= obs.x + obs.w) && leader.y >= obs.y - 10) {
                            if (zombies.length >= obs.reqZombies) {
                                playSound('explode');
                                triggerShake(15);
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
                                    obs.hitCooldown = 30;
                                    playSound('explode');
                                    triggerShake(8);
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
                            if (dist < 65) { 
                                playSound('explode');
                                triggerShake(18);
                                addParticles(bombCenterX, bombCenterY, '#ff1744', 35);
                                zombies.splice(i, 1); obstacles.splice(obsIdx, 1); break;
                            }
                        }
                    }
                }
            }

            for (let i = zombies.length - 1; i >= 0; i--) {
                let z = zombies[i];

                if (tsunamiActive) {
                    z.y = defaultGroundY - 110 + Math.sin(frame * 0.15 + i * 0.4) * 8;
                    z.vy = 0; z.isGrounded = true;
                } else if (giantActive) {
                    z.y = defaultGroundY - 35; z.vy = 0; z.isGrounded = true;
                } else {
                    z.vy += gravity; z.y += z.vy;
                    let onPit = isOverPit(z.x, 8);
                    let standingOnVehicle = false;

                    obstacles.forEach((obs) => {
                        if (obs.type === 'CAR' || obs.type === 'BUS' || obs.type === 'HELI') {
                            if (z.x >= obs.x - 5 && z.x <= obs.x + obs.w + 5) {
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
                            z.isGrounded = false; 
                        }
                    }
                }

                z.legAngle += z.isGrounded ? 0.22 : 0.08;
                if (isBlockedByVehicle && i === 0) z.x = Math.max(100, z.x - speed);
                
                if (z.y > canvas.height + 30) { 
                    addParticles(z.x, canvas.height - 10, '#76ba1b', 12); 
                    zombies.splice(i, 1); 
                }
            }

            if (zombies.length === 0) {
                triggerGameOver();
                return;
            }

            humans.forEach((h) => {
                h.x -= speed;
                let leader = zombies[0];

                if (tsunamiActive || giantActive) {
                    if (h.x < 450 && !h.eaten) {
                        h.eaten = true; score += 1; currentCoins += 5; totalCoins += 5;
                        totalEatenHumans += 1;
                        if (score > maxSingleRunEaten) maxSingleRunEaten = score;
                        saveUserData();
                        playSound('eat');
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
                        playSound('eat');
                        addParticles(h.x, h.y - 10, '#76ba1b', 15);
                        if (zombies.length < 30) {
                            let tail = zombies[zombies.length - 1];
                            let newVariant = Math.floor(Math.random() * 3);
                            zombies.push({ x: tail.x - 22, y: tail.y, vy: 0, isGrounded: h.isGrounded, legAngle: 0, variant: newVariant });
                        }
                    }
                }
            });

            humans = humans.filter(h => h.x > -50 && !h.eaten);
            obstacles = obstacles.filter(o => o.x > -200);

            particles.forEach(p => { p.x += p.vx; p.y += p.vy; p.life--; });
            particles = particles.filter(p => p.life > 0);
        }

        // MAP BÃI BIỂN ĐÃ BỎ LÂU ĐÀI CÁT
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

            ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
            ctx.beginPath();
            for (let x = 0; x < canvas.width; x += 20) {
                ctx.arc(x, 276 + Math.sin((x + bgOffset * 2) * 0.05) * 3, 8, 0, Math.PI * 2);
            }
            ctx.fill();

            ctx.fillStyle = '#ffe082'; ctx.fillRect(0, 280, canvas.width, 50);

            let umbrellaSpacing = 400;
            let startU = - (bgOffset * 0.6 % umbrellaSpacing);
            for (let ux = startU; ux < canvas.width + umbrellaSpacing; ux += umbrellaSpacing) {
                ctx.fillStyle = '#e91e63'; ctx.beginPath(); ctx.arc(ux, 240, 30, Math.PI, Math.PI * 2); ctx.fill();
                ctx.fillStyle = '#ffffff'; ctx.fillRect(ux - 6, 240, 12, -28);
                ctx.strokeStyle = '#795548'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(ux, 240); ctx.lineTo(ux, 280); ctx.stroke();
                ctx.fillStyle = '#00bcd4'; ctx.fillRect(ux + 20, 270, 25, 8);
            }

            for (let tIdx = 0; tIdx < 2; tIdx++) {
                let treeX = (120 + tIdx * 450 - bgOffset * 0.8) % 900; if (treeX < -100) treeX += 900;
                ctx.strokeStyle = '#6d4c41'; ctx.lineWidth = 14; ctx.beginPath(); ctx.moveTo(treeX, 310); ctx.quadraticCurveTo(treeX - 18, 230, treeX + 18, 160); ctx.stroke();
                ctx.fillStyle = '#3e2723'; ctx.beginPath(); ctx.arc(treeX + 12, 168, 6, 0, Math.PI*2); ctx.arc(treeX + 22, 165, 6, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = '#2e7d32';
                for (let a = 0; a < 5; a++) {
                    let ang = (a * Math.PI) / 2.5 - 0.2; ctx.beginPath(); ctx.ellipse(treeX + 18 + Math.cos(ang)*32, 160 + Math.sin(ang)*20, 32, 12, ang, 0, Math.PI*2); ctx.fill();
                }
            }

            // Chỉ giữ lại Sao biển rải rác, đã BỎ LÂU ĐÀI CÁT
            let itemSpacing = 300;
            let startItem = - (bgOffset % itemSpacing);
            for (let ix = startItem; ix < canvas.width + itemSpacing; ix += itemSpacing) {
                ctx.fillStyle = '#ff3d00'; ctx.beginPath(); ctx.arc(ix + 50, 292, 5, 0, Math.PI*2); ctx.fill();
            }
        }

        function drawCityMap() {
            let skyGrad = ctx.createLinearGradient(0, 0, 0, 220);
            skyGrad.addColorStop(0, '#5c3d75'); skyGrad.addColorStop(0.5, '#95508c'); skyGrad.addColorStop(1, '#e08ba0');
            ctx.fillStyle = skyGrad; ctx.fillRect(0, 0, canvas.width, 220);

            ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
            let cloudX = (200 - bgOffset * 0.1) % 900; if (cloudX < -100) cloudX += 900;
            ctx.beginPath(); ctx.arc(cloudX, 40, 18, 0, Math.PI*2); ctx.arc(cloudX + 25, 35, 24, 0, Math.PI*2); ctx.fill();

            let bridgeWidth = 600;
            let startBridgeX = - (bgOffset * 0.5 % bridgeWidth);
            for (let bx = startBridgeX; bx < canvas.width + bridgeWidth; bx += bridgeWidth) {
                ctx.strokeStyle = '#546e7a'; ctx.lineWidth = 14;
                ctx.beginPath(); ctx.moveTo(bx, 210); ctx.quadraticCurveTo(bx + 300, 140, bx + 600, 210); ctx.stroke();
                ctx.strokeStyle = '#37474f'; ctx.lineWidth = 4;
                ctx.beginPath(); ctx.moveTo(bx, 216); ctx.quadraticCurveTo(bx + 300, 146, bx + 600, 216); ctx.stroke();
            }

            for (let b = 0; b < 6; b++) {
                let bX = (b * 220 - bgOffset * 0.25) % 1320; if (bX < -160) bX += 1320;
                let bH = 100 + (b * 40) % 90;
                ctx.fillStyle = '#263238'; ctx.fillRect(bX, 220 - bH, 110, bH);
                ctx.fillStyle = '#ffeb3b';
                for (let r = 0; r < Math.floor(bH / 16); r++) {
                    for (let c = 0; c < 3; c++) {
                        if ((b + r + c) % 2 === 0) ctx.fillRect(bX + 12 + c * 30, 220 - bH + 10 + r * 16, 14, 8);
                    }
                }
            }

            let redBuildingWidth = 450;
            let startRedX = - (bgOffset * 0.6 % redBuildingWidth);
            for (let rxPos = startRedX; rxPos < canvas.width + redBuildingWidth; rxPos += redBuildingWidth) {
                ctx.fillStyle = '#b71c1c'; ctx.fillRect(rxPos, 110, 150, 170);
                ctx.fillStyle = '#331a00';
                for(let rx=0; rx<3; rx++) {
                    for(let ry=0; ry<4; ry++) {
                        ctx.fillRect(rxPos + 15 + rx * 42, 130 + ry * 35, 28, 22);
                    }
                }
            }

            ctx.fillStyle = '#455a64'; ctx.fillRect(0, 280, canvas.width, 50);
        }

        function drawVillageMap() {
            let skyGrad = ctx.createLinearGradient(0, 0, 0, 220);
            skyGrad.addColorStop(0, '#f9a825'); skyGrad.addColorStop(0.6, '#f57c00'); skyGrad.addColorStop(1, '#ff8f00');
            ctx.fillStyle = skyGrad; ctx.fillRect(0, 0, canvas.width, 220);

            ctx.fillStyle = 'rgba(255, 236, 179, 0.7)';
            let cloudX = (250 - bgOffset * 0.12) % 900; if (cloudX < -100) cloudX += 900;
            ctx.beginPath(); ctx.arc(cloudX, 45, 20, 0, Math.PI*2); ctx.arc(cloudX + 30, 40, 28, 0, Math.PI*2); ctx.fill();

            ctx.fillStyle = '#558b2f';
            ctx.beginPath();
            ctx.moveTo(0, 220); ctx.quadraticCurveTo(200, 160, 400, 220);
            ctx.quadraticCurveTo(600, 170, 800, 220); ctx.lineTo(800, 280); ctx.lineTo(0, 280); ctx.fill();

            let houseSpacing = 380;
            let startH = - (bgOffset * 0.5 % houseSpacing);
            for (let hx = startH; hx < canvas.width + houseSpacing; hx += houseSpacing) {
                ctx.fillStyle = '#8d6e63'; ctx.fillRect(hx, 200, 95, 80);
                ctx.fillStyle = '#5d4037'; ctx.fillRect(hx + 35, 235, 25, 45);
                ctx.fillStyle = '#3e2723'; ctx.fillRect(hx + 10, 220, 18, 18);
                ctx.fillStyle = '#fbc02d';
                ctx.beginPath(); ctx.moveTo(hx - 12, 200); ctx.lineTo(hx + 47, 155); ctx.lineTo(hx + 107, 200); ctx.fill();
                ctx.strokeStyle = '#f57f17'; ctx.lineWidth = 3;
                ctx.beginPath(); ctx.moveTo(hx - 12, 200); ctx.lineTo(hx + 47, 155); ctx.lineTo(hx + 107, 200); ctx.stroke();
            }

            let fenceSpacing = 280;
            let startF = - (bgOffset * 0.8 % fenceSpacing);
            for (let fx = startF; fx < canvas.width + fenceSpacing; fx += fenceSpacing) {
                ctx.fillStyle = '#fbc02d'; ctx.beginPath(); ctx.arc(fx + 20, 265, 18, Math.PI, Math.PI*2); ctx.fillRect(fx + 2, 265, 36, 15); ctx.fill();
                ctx.strokeStyle = '#e65100'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(fx + 20, 235); ctx.lineTo(fx + 20, 280); ctx.stroke();
            }

            ctx.fillStyle = '#c0ca33'; ctx.fillRect(0, 280, canvas.width, 50);

            ctx.strokeStyle = '#afb42b'; ctx.lineWidth = 2;
            for (let lx = 0; lx < canvas.width; lx += 15) {
                let rx = (lx - bgOffset * 0.9) % canvas.width; if (rx < 0) rx += canvas.width;
                ctx.beginPath(); ctx.moveTo(rx, 290); ctx.lineTo(rx - 4, 275); ctx.moveTo(rx, 290); ctx.lineTo(rx + 4, 272); ctx.stroke();
            }
        }

        function drawBackground() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            ctx.save();
            if (shakeDuration > 0) {
                shakeDuration--;
                let shakeX = (Math.random() - 0.5) * 10;
                let shakeY = (Math.random() - 0.5) * 10;
                ctx.translate(shakeX, shakeY);
            }

            if (currentMap === 'BEACH') {
                drawBeachMap();
            } else if (currentMap === 'CITY') {
                drawCityMap();
            } else if (currentMap === 'VILLAGE') {
                drawVillageMap();
            }

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
                let waveGrad = ctx.createLinearGradient(0, 80, 0, defaultGroundY + 50);
                waveGrad.addColorStop(0, '#00e5ff'); waveGrad.addColorStop(0.4, '#0097a7'); waveGrad.addColorStop(1, '#002f6c');
                ctx.fillStyle = waveGrad;
                ctx.beginPath(); 
                ctx.moveTo(-100, defaultGroundY + 50); 
                ctx.lineTo(-100, 160);
                ctx.bezierCurveTo(waveX - 140, 130, waveX - 40, 100, waveX + 10, 150);
                ctx.bezierCurveTo(waveX + 50, 190, waveX + 70, 260, waveX + 30, defaultGroundY + 50);
                ctx.closePath(); 
                ctx.fill();

                ctx.fillStyle = '#ffffff';
                ctx.beginPath(); ctx.arc(waveX + 10, 150, 18 + Math.sin(frame*0.3)*4, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(waveX - 10, 140, 14, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(waveX + 25, 165, 12, 0, Math.PI*2); ctx.fill();
            }
        }

        function drawGiantMonster() {
            let gX = 180; let gY = defaultGroundY - 50;

            let brainGrad = ctx.createRadialGradient(gX - 12, gY - 25, 8, gX, gY, 72);
            brainGrad.addColorStop(0, '#ccff90'); brainGrad.addColorStop(0.5, '#76ba1b'); brainGrad.addColorStop(1, '#1b5e20');
            ctx.fillStyle = brainGrad; ctx.beginPath(); ctx.arc(gX, gY - 10, 72, 0, Math.PI * 2); ctx.fill();

            ctx.fillStyle = '#111111';
            ctx.fillRect(gX - 18, gY - 78, 36, 6);
            ctx.fillRect(gX - 11, gY - 105, 22, 27);
            ctx.fillStyle = '#b71c1c'; ctx.fillRect(gX - 11, gY - 84, 22, 5);

            ctx.fillStyle = '#fbc02d';
            ctx.fillRect(gX - 22, gY + 52, 16, 12);
            ctx.fillRect(gX + 6, gY + 52, 16, 12);

            let eyes = [
                {x: gX - 35, y: gY - 32, r: 20}, {x: gX + 12, y: gY - 40, r: 22},
                {x: gX + 42, y: gY - 14, r: 16}, {x: gX - 10, y: gY - 8, r: 26}
            ];
            eyes.forEach(e => {
                ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.arc(e.x, e.y, e.r, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = '#00e5ff'; ctx.beginPath(); ctx.arc(e.x + 3, e.y, e.r * 0.55, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = '#000000'; ctx.beginPath(); ctx.arc(e.x + 4, e.y, e.r * 0.25, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.arc(e.x + 1, e.y - 3, 2, 0, Math.PI*2); ctx.fill();
            });

            ctx.fillStyle = '#110022'; 
            ctx.beginPath(); ctx.ellipse(gX + 18, gY + 28, 30, 16, 0.1, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#ffffff';
            ctx.beginPath(); ctx.moveTo(gX, gY + 20); ctx.lineTo(gX + 6, gY + 30); ctx.lineTo(gX + 12, gY + 20); ctx.fill();

            ctx.strokeStyle = '#4a148c'; ctx.lineWidth = 14; ctx.lineCap = 'round';
            ctx.beginPath();
            ctx.moveTo(gX + 35, gY + 30);
            ctx.bezierCurveTo(gX + 80, gY + 40, gX + 130, gY + 10, gX + 180, gY + 25);
            ctx.stroke();

            let laserGrad = ctx.createLinearGradient(gX + 30, gY - 20, 800, gY - 20);
            laserGrad.addColorStop(0, '#ffffff'); laserGrad.addColorStop(0.15, '#ff007f'); laserGrad.addColorStop(0.7, '#e040fb'); laserGrad.addColorStop(1, '#ffffff');
            ctx.strokeStyle = laserGrad; ctx.lineWidth = 26 + Math.sin(frame * 0.4) * 6;
            ctx.beginPath(); ctx.moveTo(gX + 30, gY - 25); ctx.lineTo(800, gY - 25); ctx.stroke();
        }

        function drawHuman(h) {
            ctx.save(); ctx.translate(h.x, h.y);
            ctx.fillStyle = '#ffcc80'; ctx.beginPath(); ctx.arc(0, -16, 7, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = h.gender === 'MALE' ? '#5d4037' : '#fbc02d'; ctx.beginPath(); ctx.arc(0, -19, 7, Math.PI, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#000'; ctx.beginPath(); ctx.arc(-2.5, -16, 1.2, 0, Math.PI*2); ctx.arc(2.5, -16, 1.2, 0, Math.PI*2); ctx.fill();
            
            ctx.fillStyle = h.gender === 'MALE' ? '#1e88e5' : '#e91e63'; ctx.fillRect(-5, -9, 10, 8);
            
            ctx.fillStyle = h.gender === 'MALE' ? '#283593' : '#ad1457';
            ctx.fillRect(-5, -1, 10, 7);
            ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 1;
            ctx.strokeRect(-5, -1, 10, 7);

            ctx.restore();
        }

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
                ctx.strokeStyle = '#76ba1b'; ctx.lineWidth = 5;
                ctx.beginPath(); ctx.moveTo(-5, 6); ctx.lineTo(-5 + Math.sin(z.legAngle)*8, 18); ctx.moveTo(5, 6); ctx.lineTo(5 - Math.sin(z.legAngle)*8, 18); ctx.stroke();

                ctx.fillStyle = '#558b2f';
                ctx.beginPath(); ctx.arc(-5 + Math.sin(z.legAngle)*8, 19, 3.5, 0, Math.PI*2); ctx.arc(5 - Math.sin(z.legAngle)*8, 19, 3.5, 0, Math.PI*2); ctx.fill();

                ctx.fillStyle = pantColor; ctx.fillRect(-8, 2, 16, 7);
                ctx.fillStyle = shirtColor; ctx.fillRect(-9, -6, 18, 10);

                ctx.fillStyle = '#76ba1b';
                ctx.beginPath();
                ctx.ellipse(0, -16, 17, 15, 0.1, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.arc(8, -18, 10, 0, Math.PI * 2); ctx.fill();
                ctx.fillStyle = '#00e5ff'; ctx.beginPath(); ctx.arc(9, -18, 5.5, 0, Math.PI * 2); ctx.fill();
                ctx.fillStyle = '#111111'; ctx.beginPath(); ctx.arc(10, -18, 2.5, 0, Math.PI * 2); ctx.fill();
                ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.arc(8, -20, 1.5, 0, Math.PI * 2); ctx.fill();
                
                if (isNearHuman) {
                    ctx.fillStyle = '#111111'; ctx.beginPath(); ctx.arc(10, -8, 8, 0, Math.PI*2); ctx.fill();
                    ctx.fillStyle = '#ffffff';
                    ctx.beginPath(); ctx.moveTo(6, -11); ctx.lineTo(8, -5); ctx.lineTo(10, -11); ctx.fill();
                } else {
                    ctx.fillStyle = '#1b5e20'; ctx.beginPath(); ctx.arc(8, -8, 5, 0, Math.PI); ctx.fill();
                    ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.moveTo(5, -8); ctx.lineTo(7, -4); ctx.lineTo(9, -8); ctx.fill();
                }

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

        function drawZombieRequirementBadge(x, y, reqCount) {
            ctx.save();
            ctx.translate(x, y);

            ctx.fillStyle = '#111111';
            ctx.beginPath();
            ctx.roundRect(0, 0, 85, 42, 10);
            ctx.fill();
            ctx.strokeStyle = '#ff9800'; ctx.lineWidth = 3; ctx.stroke();

            ctx.fillStyle = '#111111';
            ctx.beginPath();
            ctx.moveTo(18, 42); ctx.lineTo(26, 50); ctx.lineTo(34, 42);
            ctx.fill();

            ctx.fillStyle = '#76ba1b';
            ctx.beginPath(); ctx.arc(20, 21, 11, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.arc(23, 20, 4.5, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#111'; ctx.beginPath(); ctx.arc(24, 20, 2, 0, Math.PI * 2); ctx.fill();

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
            ctx.fillStyle = '#81d4fa'; 
            for(let k=0; k<5; k++) ctx.fillRect(10 + (k * 26), 7, 18, 16);
            ctx.fillStyle = '#111'; ctx.beginPath(); ctx.arc(22, 48, 9, 0, Math.PI*2); ctx.arc(o.w - 22, 48, 9, 0, Math.PI*2); ctx.fill();
            
            drawZombieRequirementBadge(30, -52, o.reqZombies);
            ctx.restore();
        }

        function drawHelicopter(o) {
            ctx.save(); ctx.translate(o.x, o.y);
            
            ctx.fillStyle = '#ffffff';
            ctx.beginPath();
            ctx.moveTo(0, 32);
            ctx.bezierCurveTo(-5, -12, 55, -24, 160, -15);
            ctx.lineTo(195, 32);
            ctx.lineTo(0, 32);
            ctx.fill();

            ctx.fillStyle = '#76ba1b';
            ctx.fillRect(45, 6, 135, 12);

            ctx.fillStyle = '#263238';
            ctx.beginPath(); ctx.arc(24, 12, 10, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.arc(22, 10, 3, 0, Math.PI*2); ctx.fill();

            ctx.fillStyle = '#263238';
            for(let i=0; i<6; i++) {
                ctx.fillRect(58 + i * 18, 9, 12, 11);
            }

            ctx.fillStyle = '#2e7d32';
            ctx.font = '900 16px sans-serif';
            ctx.fillText("Z.AIRLINE", 68, -2);

            ctx.fillStyle = '#cfd8dc';
            ctx.fillRect(100, 28, 50, 22);
            ctx.fillStyle = '#111111'; 
            ctx.beginPath(); ctx.arc(115, 52, 9, 0, Math.PI*2); ctx.arc(135, 52, 9, 0, Math.PI*2); ctx.fill();

            drawZombieRequirementBadge(45, -58, o.reqZombies);
            ctx.restore();
        }

        function draw() {
            drawBackground();

            if (gameState === 'MENU') {
                let demoZ = { x: 220, y: defaultGroundY - 20, legAngle: frame * 0.2, variant: 0 };
                drawZombie(demoZ);
                ctx.restore();
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

            ctx.restore(); 

            ctx.fillStyle = 'rgba(0,0,0,0.5)'; ctx.fillRect(15, 12, 170, 70);
            ctx.fillStyle = '#fbc02d'; ctx.font = 'bold 22px sans-serif'; ctx.textAlign = 'left'; ctx.fillText(`🪙 ${totalCoins}`, 25, 40);
            ctx.fillStyle = '#76ba1b'; ctx.fillText(`🧠 x${zombies.length}`, 25, 70);

            let mapNameText = '🌊 Map: Bãi Biển';
            if (currentMap === 'CITY') mapNameText = '🌆 Map: Thành Phố';
            else if (currentMap === 'VILLAGE') mapNameText = '🌾 Map: Làng Quê';

            ctx.fillStyle = 'rgba(0,0,0,0.5)'; ctx.fillRect(630, 12, 155, 35);
            ctx.fillStyle = '#80d8ff'; ctx.font = 'bold 15px sans-serif'; ctx.textAlign = 'center';
            ctx.fillText(mapNameText, 707, 35);

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
