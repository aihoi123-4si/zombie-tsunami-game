
import streamlit as st
import streamlit.components.v1 as components
 
st.set_page_config(page_title="Zombie Tsunami Perfect Edition", layout="centered")
st.markdown("<h1 style='text-align: center; color: #76ba1b;'>🧟 ZOMBIE TSUNAMI - PERFECT EDITION ⚡</h1>", unsafe_allow_html=True)
 
game_code = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body{margin:0;padding:0;background:#0d1b2a;display:flex;justify-content:center;align-items:center;font-family:'Arial Black',sans-serif;height:100vh;overflow:hidden;user-select:none}
#gameContainer{position:relative;width:800px;height:450px;border:4px solid #76ba1b;border-radius:12px;box-shadow:0 8px 30px rgba(118,186,27,.4);overflow:hidden;background:#111}
canvas{display:block;width:100%;height:100%}
#menuOverlay{position:absolute;top:0;left:0;width:100%;height:100%;box-sizing:border-box;padding:15px;z-index:10}
.logo-container{position:absolute;top:15px;left:50%;transform:translateX(-50%);text-align:center}
.logo-title{font-size:44px;color:#76ba1b;text-shadow:3px 3px 0 #000,-2px -2px 0 #000,2px -2px 0 #000,-2px 2px 0 #000;letter-spacing:2px;transform:rotate(-3deg);margin:0;line-height:1}
.logo-sub{font-size:34px;color:#ff3d00;text-shadow:2px 2px 0 #000,-2px -2px 0 #000,2px -2px 0 #000;letter-spacing:3px;transform:rotate(2deg);margin-top:-5px}
.top-right-btns{position:absolute;top:15px;right:15px;display:flex;gap:10px;z-index:20}
.btn-icon{width:42px;height:42px;background:#424242;border:3px solid #fff;border-radius:8px;color:#fff;font-size:22px;display:flex;justify-content:center;align-items:center;cursor:pointer;box-shadow:0 4px 0 #111}
.btn-icon:active{transform:translateY(2px);box-shadow:0 2px 0 #111}
.side-menu-right{position:absolute;right:15px;top:90px;display:flex;flex-direction:column;gap:12px}
.btn-side{width:170px;height:42px;background:linear-gradient(135deg,#e91e63,#c2185b);border:3px solid #000;border-radius:8px;color:#fff;font-size:18px;display:flex;align-items:center;padding-left:12px;box-shadow:3px 4px 0 #000;cursor:pointer;transform:rotate(2deg);text-shadow:1px 1px 2px #000}
.btn-side:nth-child(2){transform:rotate(-2deg);background:linear-gradient(135deg,#f57c00,#e65100)}
.btn-side:active{transform:scale(.96)}
.btn-side span{margin-right:10px;font-size:20px}
.btn-play{position:absolute;bottom:25px;right:20px;width:180px;height:80px;background:linear-gradient(180deg,#ff9800,#ff3d00);border:4px solid #fff;outline:4px solid #000;border-radius:14px;color:#fff;font-size:38px;font-weight:900;display:flex;justify-content:center;align-items:center;cursor:pointer;box-shadow:0 8px 0 #801300,0 12px 15px rgba(0,0,0,.5);text-shadow:3px 3px 0 #000;transform:rotate(-3deg)}
.btn-play:hover{transform:rotate(-3deg) scale(1.05)}
.btn-play:active{transform:rotate(-3deg) translateY(6px);box-shadow:0 2px 0 #801300}
.best-score-box{position:absolute;bottom:20px;left:20px;background:rgba(0,0,0,.65);border:3px solid #fff;border-radius:10px;padding:8px 16px;color:#fff}
.best-score-title{font-size:15px;color:#ddd}
.best-score-val{font-size:26px;color:#ffeb3b;font-weight:bold}
.modal-overlay{position:absolute;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.85);display:none;flex-direction:column;align-items:center;justify-content:center;z-index:100;padding:20px;box-sizing:border-box}
.modal-box{width:720px;height:400px;background:#1e272e;border:4px solid #fbc02d;border-radius:16px;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 0 30px rgba(251,192,45,.4)}
.modal-header{background:#fbc02d;color:#000;padding:10px 20px;display:flex;justify-content:space-between;align-items:center;font-size:22px;font-weight:bold}
.close-btn{background:#d32f2f;color:#fff;border:2px solid #fff;border-radius:50%;width:32px;height:32px;display:flex;justify-content:center;align-items:center;cursor:pointer;font-size:18px}
.market-tabs{display:flex;background:#0f171e;border-bottom:2px solid #333}
.tab-btn{flex:1;padding:10px;text-align:center;color:#aaa;font-size:16px;cursor:pointer;border-right:1px solid #222;font-weight:bold}
.tab-btn.active{background:#1e272e;color:#76ba1b;border-bottom:3px solid #76ba1b}
.market-content{flex:1;padding:15px;overflow-y:auto;display:flex;gap:15px;justify-content:center;align-items:center}
.shop-item{width:210px;height:230px;background:#2f3640;border:3px solid #485460;border-radius:12px;display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:12px;box-sizing:border-box;position:relative}
.shop-item.coming-soon{filter:brightness(.4)}
.cs-tag{position:absolute;top:80px;background:#ff1744;color:#fff;padding:4px 12px;font-size:14px;font-weight:bold;border-radius:4px;transform:rotate(-10deg)}
.shop-img{font-size:42px;margin-top:5px}
.shop-title{color:#fff;font-size:14px;text-align:center;font-weight:bold}
.shop-desc{color:#aaa;font-size:11px;text-align:center}
.buy-btn{background:#4cd137;color:#000;border:none;padding:8px 12px;border-radius:20px;font-weight:bold;cursor:pointer;font-size:14px;box-shadow:0 4px 0 #44bd32;width:100%}
.buy-btn.equipped{background:#fbc02d;box-shadow:0 4px 0 #f57f17}
.buy-btn.maxed,.buy-btn:disabled{background:#718093;color:#ccc;box-shadow:none;cursor:not-allowed}
.mission-list{flex:1;padding:20px;display:flex;flex-direction:column;gap:15px;overflow-y:auto}
.mission-card{background:#2f3640;border:3px solid #485460;border-radius:12px;display:flex;align-items:center;padding:12px 18px;gap:15px}
.mission-icon{width:50px;height:50px;background:#111;border:2px solid #fff;border-radius:10px;display:flex;justify-content:center;align-items:center;font-size:28px}
.mission-info{flex:1;color:#fff}
.mission-title{font-size:16px;font-weight:bold;margin-bottom:6px}
.mission-progress{font-size:14px;color:#ffeb3b}
.collect-btn{background:#fbc02d;color:#000;border:none;padding:10px 18px;border-radius:8px;font-weight:bold;font-size:16px;cursor:pointer;box-shadow:0 4px 0 #f57f17}
.collect-btn:disabled{background:#718093;box-shadow:none;cursor:not-allowed;color:#aaa}
</style>
</head>
<body>
<audio id="bgMusic" loop preload="auto">
  <source src="https://ia801503.us.archive.org/15/items/zombie-tsunami-theme-song/Zombie%20Tsunami%20Theme%20Song.mp3" type="audio/mpeg">
</audio>
 
<div id="gameContainer">
<canvas id="gameCanvas" width="800" height="450"></canvas>
 
<div id="menuOverlay">
  <div class="logo-container"><h1 class="logo-title">ZOMBIE</h1><div class="logo-sub">TSUNAMI</div></div>
  <div class="top-right-btns">
    <div class="btn-icon" id="musicToggleBtn" title="Bật/Tắt Nhạc">🔊</div>
    <div class="btn-icon">⚙️</div>
  </div>
  <div class="side-menu-right">
    <div class="btn-side" id="openMissionBtn"><span>🧪</span> MISSION</div>
    <div class="btn-side" id="openMarketBtn"><span>🪙</span> MARKET</div>
  </div>
  <div class="best-score-box">
    <div class="best-score-title">Best score:</div>
    <div class="best-score-val">🧠 <span id="bestScoreText">0</span></div>
  </div>
  <div class="btn-play" id="playBtn">PLAY</div>
</div>
 
<div id="marketModal" class="modal-overlay"><div class="modal-box">
  <div class="modal-header"><div>🛒 MARKET (Xu: 🪙 <span id="marketCoinText">0</span>)</div><div class="close-btn" id="closeMarketBtn">✖</div></div>
  <div class="market-tabs">
    <div class="tab-btn active" id="tabOutfits">TRANG PHỤC</div>
    <div class="tab-btn" id="tabHats">PHỤ KIỆN</div>
    <div class="tab-btn" id="tabPowers">SỨC MẠNH</div>
  </div>
  <div class="market-content" id="contentOutfits">
    <div class="shop-item"><div class="shop-img">🩹</div><div class="shop-title">Xác Ướp (Mummy)</div><div class="shop-desc">Trang phục cao cấp</div><button class="buy-btn" id="buyMummyBtn">300 Xu</button></div>
    <div class="shop-item coming-soon"><div class="shop-img">🧟</div><div class="shop-title">???</div><div class="cs-tag">COMING SOON</div><button class="buy-btn" disabled>Khóa</button></div>
  </div>
  <div class="market-content" id="contentHats" style="display:none">
    <div class="shop-item"><div class="shop-img">🤠</div><div class="shop-title">Mũ Cao Bồi</div><div class="shop-desc">Phụ kiện phong cách</div><button class="buy-btn" id="buyHatBtn">200 Xu</button></div>
    <div class="shop-item"><div class="shop-img">🎃</div><div class="shop-title">Đầu Bí Ngô</div><div class="shop-desc">Phụ kiện Halloween</div><button class="buy-btn" id="buyPumpkinBtn">200 Xu</button></div>
  </div>
  <div class="market-content" id="contentPowers" style="display:none">
    <div class="shop-item"><div class="shop-img">🧠</div><div class="shop-title">Zombie Ban Đầu</div><div class="shop-desc">Cấp hiện tại: <span id="p1LevelLabel">1</span>/3</div><button class="buy-btn" id="buyPower1Btn">50 Xu</button></div>
    <div class="shop-item"><div class="shop-img">⏱️</div><div class="shop-title">Thời Gian Bổ Trợ</div><div class="shop-desc">Cấp hiện tại: <span id="p2LevelLabel">1</span>/3</div><button class="buy-btn" id="buyPower2Btn">50 Xu</button></div>
  </div>
</div></div>
 
<div id="missionModal" class="modal-overlay"><div class="modal-box">
  <div class="modal-header"><div>📜 MISSIONS</div><div class="close-btn" id="closeMissionBtn">✖</div></div>
  <div class="mission-list">
    <div class="mission-card"><div class="mission-icon">🧟</div><div class="mission-info"><div class="mission-title">Ăn thịt tổng cộng 100 người (Thưởng 100 Xu)</div><div class="mission-progress">Tiến độ: <span id="m1Progress">0</span>/100</div></div><button class="collect-btn" id="m1Btn" disabled>COLLECT</button></div>
    <div class="mission-card"><div class="mission-icon">🧠</div><div class="mission-info"><div class="mission-title">Ăn thịt 10 người trong 1 màn chơi (Thưởng 50 Xu)</div><div class="mission-progress">Tiến độ: Kỷ lục <span id="m2Progress">0</span>/10</div></div><button class="collect-btn" id="m2Btn" disabled>COLLECT</button></div>
  </div>
</div></div>
</div>
 
<script>
// ---------- Storage an toàn (iframe Streamlit có thể chặn localStorage) ----------
const store = {
  getItem(k){ try { return localStorage.getItem(k); } catch(e){ return null; } },
  setItem(k,v){ try { localStorage.setItem(k,v); } catch(e){} }
};
 
const $ = id => document.getElementById(id);
const canvas = $('gameCanvas'), ctx = canvas.getContext('2d');
const menuOverlay = $('menuOverlay'), playBtn = $('playBtn'), bestScoreText = $('bestScoreText');
const bgMusic = $('bgMusic'), musicToggleBtn = $('musicToggleBtn');
let isMuted = false;
 
// ---------- Âm thanh ----------
const AudioCtx = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;
function initAudio(){ if(!audioCtx) audioCtx = new AudioCtx(); if(audioCtx.state==='suspended') audioCtx.resume(); }
const SFX = {
  jump:   ['sine',280,580,.12,.2,'exponentialRampToValueAtTime'],
  eat:    ['triangle',150,350,.1,.3,'exponentialRampToValueAtTime'],
  coin:   ['sine',988,1318,.18,.18,'setValueAtTime'],
  powerup:['square',300,900,.25,.25,'exponentialRampToValueAtTime'],
  explode:['sawtooth',120,30,.35,.4,'linearRampToValueAtTime']
};
function playSound(type){
  if(isMuted) return; initAudio(); if(!audioCtx) return;
  const [wave,f1,f2,dur,vol,ramp] = SFX[type]; const now = audioCtx.currentTime;
  const osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
  osc.type = wave; osc.frequency.setValueAtTime(f1, now);
  if(ramp==='setValueAtTime') osc.frequency.setValueAtTime(f2, now+.08); else osc.frequency[ramp](f2, now+dur);
  gain.gain.setValueAtTime(vol, now); gain.gain.linearRampToValueAtTime(.01, now+dur);
  osc.connect(gain); gain.connect(audioCtx.destination); osc.start(now); osc.stop(now+dur);
}
function playMusic(){ if(!isMuted) bgMusic.play().catch(()=>{}); }
function stopMusic(){ bgMusic.pause(); bgMusic.currentTime = 0; }
musicToggleBtn.addEventListener('click', e => {
  e.stopPropagation(); isMuted = !isMuted;
  if(isMuted){ bgMusic.pause(); musicToggleBtn.innerText='🔇'; }
  else { musicToggleBtn.innerText='🔊'; if(gameState==='PLAYING') playMusic(); }
});
 
// ---------- Dữ liệu người chơi ----------
let gameState = 'MENU', score = 0, distance = 0;
let bestScore = parseInt(store.getItem('zt_best_score') || '0');
bestScoreText.innerText = bestScore;
let totalCoins = parseInt(store.getItem('zt_total_coins') || '0');
let totalEatenHumans = parseInt(store.getItem('zt_total_eaten') || '0');
let maxSingleRunEaten = parseInt(store.getItem('zt_max_single_eaten') || '0');
let m1Claimed = store.getItem('zt_m1_claimed') === 'true';
let m2Claimed = store.getItem('zt_m2_claimed') === 'true';
let equippedOutfit = store.getItem('zt_equipped_outfit') || 'NONE';
let equippedHat = store.getItem('zt_equipped_hat') || 'NONE';
let ownedItems = []; try { ownedItems = JSON.parse(store.getItem('zt_owned_items') || '[]'); } catch(e){}
let power1Level = parseInt(store.getItem('zt_p1_level') || '1');
let power2Level = parseInt(store.getItem('zt_p2_level') || '1');
 
const MAP_LIST = ['BEACH','CITY','VILLAGE'];
let currentMap = 'BEACH', mapTimer = 0, shakeDuration = 0;
function triggerShake(d = 12){ shakeDuration = d; }
 
function saveUserData(){
  store.setItem('zt_total_coins', totalCoins); store.setItem('zt_total_eaten', totalEatenHumans);
  store.setItem('zt_max_single_eaten', maxSingleRunEaten); store.setItem('zt_m1_claimed', m1Claimed);
  store.setItem('zt_m2_claimed', m2Claimed); store.setItem('zt_equipped_outfit', equippedOutfit);
  store.setItem('zt_equipped_hat', equippedHat); store.setItem('zt_owned_items', JSON.stringify(ownedItems));
  store.setItem('zt_p1_level', power1Level); store.setItem('zt_p2_level', power2Level);
  updateMarketUI(); updateMissionUI();
}
 
// ---------- Market / Mission UI ----------
function setItemBtn(btn, key, equippedVal, owned, priceText, onText, offText){
  if(owned){ btn.innerText = equippedVal ? onText : offText; btn.className = equippedVal ? 'buy-btn equipped' : 'buy-btn'; }
  else { btn.innerText = priceText; btn.className = 'buy-btn'; }
}
function setPowerBtn(btn, label, lvl){
  label.innerText = lvl;
  if(lvl >= 3){ btn.innerText='ĐÃ TỐI ĐA'; btn.className='buy-btn maxed'; btn.disabled=true; }
  else { btn.innerText='50 Xu'; btn.className='buy-btn'; btn.disabled=false; }
}
function updateMarketUI(){
  $('marketCoinText').innerText = totalCoins;
  setItemBtn($('buyMummyBtn'),'MUMMY',equippedOutfit==='MUMMY',ownedItems.includes('MUMMY'),'300 Xu','Đang Mặc','Mặc Vào');
  setItemBtn($('buyHatBtn'),'HAT',equippedHat==='HAT',ownedItems.includes('HAT'),'200 Xu','Đang Đội','Đội Vào');
  setItemBtn($('buyPumpkinBtn'),'PUMPKIN',equippedHat==='PUMPKIN',ownedItems.includes('PUMPKIN'),'200 Xu','Đang Đội','Đội Vào');
  setPowerBtn($('buyPower1Btn'),$('p1LevelLabel'),power1Level);
  setPowerBtn($('buyPower2Btn'),$('p2LevelLabel'),power2Level);
}
function setMissionBtn(btn, prog, claimed, value, goal, reward){
  prog.innerText = Math.min(value, goal);
  if(claimed){ btn.innerText='ĐÃ NHẬN'; btn.disabled=true; }
  else if(value >= goal){ btn.innerText='NHẬN '+reward+' XU'; btn.disabled=false; }
  else { btn.innerText='CHƯA ĐẠT'; btn.disabled=true; }
}
function updateMissionUI(){
  setMissionBtn($('m1Btn'),$('m1Progress'),m1Claimed,totalEatenHumans,100,100);
  setMissionBtn($('m2Btn'),$('m2Progress'),m2Claimed,maxSingleRunEaten,10,50);
}
function buyPower(which){
  const lvl = which===1 ? power1Level : power2Level;
  if(lvl >= 3) return;
  if(totalCoins < 50){ alert('Bạn không đủ 50 xu!'); return; }
  totalCoins -= 50; if(which===1) power1Level++; else power2Level++; saveUserData();
}
$('buyPower1Btn').addEventListener('click', () => buyPower(1));
$('buyPower2Btn').addEventListener('click', () => buyPower(2));
$('m1Btn').addEventListener('click', () => { if(!m1Claimed && totalEatenHumans>=100){ m1Claimed=true; totalCoins+=100; saveUserData(); } });
$('m2Btn').addEventListener('click', () => { if(!m2Claimed && maxSingleRunEaten>=10){ m2Claimed=true; totalCoins+=50; saveUserData(); } });
 
const tabs = [['tabOutfits','contentOutfits'],['tabHats','contentHats'],['tabPowers','contentPowers']];
tabs.forEach(([t,c]) => $(t).addEventListener('click', () => {
  tabs.forEach(([t2,c2]) => { $(t2).classList.toggle('active', t2===t); $(c2).style.display = c2===c ? 'flex' : 'none'; });
  updateMarketUI();
}));
$('openMarketBtn').addEventListener('click', () => { updateMarketUI(); $('marketModal').style.display='flex'; });
$('closeMarketBtn').addEventListener('click', () => { $('marketModal').style.display='none'; });
$('openMissionBtn').addEventListener('click', () => { updateMissionUI(); $('missionModal').style.display='flex'; });
$('closeMissionBtn').addEventListener('click', () => { $('missionModal').style.display='none'; });
 
function buyOrToggle(item, price, kind){
  if(!ownedItems.includes(item)){
    if(totalCoins < price){ alert('Bạn không đủ xu!'); return; }
    totalCoins -= price; ownedItems.push(item);
    if(kind==='outfit') equippedOutfit = item; else equippedHat = item;
  } else if(kind==='outfit') equippedOutfit = equippedOutfit===item ? 'NONE' : item;
  else equippedHat = equippedHat===item ? 'NONE' : item;
  saveUserData();
}
$('buyMummyBtn').addEventListener('click', () => buyOrToggle('MUMMY',300,'outfit'));
$('buyHatBtn').addEventListener('click', () => buyOrToggle('HAT',200,'hat'));
$('buyPumpkinBtn').addEventListener('click', () => buyOrToggle('PUMPKIN',200,'hat'));
 
// ---------- Trạng thái game ----------
let currentCoins = 0, speed = 4.5, frame = 0;
const gravity = 0.65, defaultGroundY = 330;
let zombies=[], humans=[], obstacles=[], pits=[], powerups=[], coinTrails=[], particles=[], bgOffset=0;
let tsunamiActive=false, tsunamiTimer=0, giantActive=false, giantTimer=0;
 
function addParticles(x,y,color,count=12){
  for(let i=0;i<count;i++) particles.push({x,y,vx:(Math.random()-.5)*8,vy:(Math.random()-.5)*8,life:25,color});
}
function startGame(){ resetGame(); gameState='PLAYING'; menuOverlay.style.display='none'; playMusic(); }
playBtn.addEventListener('click', startGame);
 
function handleInput(){
  playMusic();
  if(gameState==='GAMEOVER'){ gameState='MENU'; menuOverlay.style.display='block'; stopMusic(); }
  else if(gameState==='PLAYING'){
    zombies.forEach((z,idx) => {
      if(z.isGrounded) setTimeout(() => {
        if(z.isGrounded){ z.vy = -13.5 - idx*0.02; z.isGrounded=false; playSound('jump'); }
      }, idx*45);
    });
  }
}
window.addEventListener('keydown', e => {
  if(e.code==='Space' || e.code==='ArrowUp'){
    e.preventDefault();
    if(gameState==='MENU'){
      if($('marketModal').style.display!=='flex' && $('missionModal').style.display!=='flex') startGame();
    } else handleInput();
  }
});
canvas.addEventListener('touchstart', e => { e.preventDefault(); handleInput(); });
canvas.addEventListener('mousedown', handleInput);
 
function switchRandomMap(){
  const a = MAP_LIST.filter(m => m !== currentMap); currentMap = a[Math.floor(Math.random()*a.length)];
}
function resetGame(){
  score=0; currentCoins=0; speed=4.5; frame=0; distance=0;
  zombies = [];
  for(let i=0;i<power1Level;i++) zombies.push({x:180-i*22,y:defaultGroundY-20,vy:0,isGrounded:true,legAngle:i*.5,variant:i%3});
  humans=[]; obstacles=[]; pits=[]; powerups=[]; coinTrails=[]; particles=[];
  tsunamiActive=false; tsunamiTimer=0; giantActive=false; giantTimer=0;
  currentMap = MAP_LIST[Math.floor(Math.random()*MAP_LIST.length)]; mapTimer=0;
}
function isOverPit(x,w=20){ return pits.some(p => x+w>p.x && x<p.x+p.width); }
function triggerGameOver(){
  gameState='GAMEOVER'; stopMusic();
  if(score > bestScore){ bestScore=score; store.setItem('zt_best_score',bestScore); bestScoreText.innerText=bestScore; }
  saveUserData();
}
function addZombie(spacing){
  if(zombies.length >= 35) return;
  const tail = zombies[zombies.length-1];
  zombies.push({x:tail.x-spacing,y:tail.y,vy:0,isGrounded:true,legAngle:0,variant:Math.floor(Math.random()*3)});
}
function eatReward(n, mult){
  score += n; currentCoins += n*mult; totalCoins += n*mult; totalEatenHumans += n;
  if(score > maxSingleRunEaten) maxSingleRunEaten = score;
}
 
// ---------- Update ----------
function update(){
  frame++;
  bgOffset += (gameState==='MENU' ? 1.5 : speed);
  if(gameState!=='PLAYING') return;
 
  distance += speed/10;
  if(frame % 30 === 0) saveUserData();
 
  mapTimer++; if(mapTimer>=1200){ mapTimer=0; switchRandomMap(); }
  speed = 4.5 + Math.floor(frame/600)*0.4;
  const bonusDuration = power2Level===1 ? 360 : (power2Level===2 ? 480 : 600);
 
  if(tsunamiActive && --tsunamiTimer<=0) tsunamiActive=false;
  if(giantActive && --giantTimer<=0) giantActive=false;
 
  if(frame%280===0 && Math.random()>.35) pits.push({x:850,width:110+Math.random()*30});
 
  if(frame%160===0 && Math.random()<.6){
    const count = 5+Math.floor(Math.random()*4), coinY = defaultGroundY-40-(Math.random()>.5?40:0);
    for(let c=0;c<count;c++) coinTrails.push({x:850+c*24,y:coinY,collected:false});
  }
  if(frame%850===0 && !tsunamiActive && !giantActive && Math.random()<.6 && !isOverPit(850,40))
    powerups.push({x:850,y:defaultGroundY-60,w:38,h:38,collected:false});
 
  if(frame%130===0 && !isOverPit(850,200)){
    const r = Math.random(), X = 850;
    if(r<.32) humans.push({x:X,y:defaultGroundY-20,gender:Math.random()>.5?'MALE':'FEMALE',eaten:false,panic:false,step:0});
    else if(r<.60) obstacles.push({x:X,y:defaultGroundY-48,w:100,h:48,type:'CAR',reqZombies:4,peopleInside:3,hitCooldown:0});
    else if(r<.78) obstacles.push({x:X,y:defaultGroundY-62,w:160,h:62,type:'BUS',reqZombies:6,peopleInside:6,hitCooldown:0});
    else if(r<.88) obstacles.push({x:X,y:defaultGroundY-78,w:210,h:68,type:'HELI',reqZombies:8,peopleInside:8,hitCooldown:0});
    else obstacles.push({x:X,y:defaultGroundY-45,w:45,h:45,type:'BOMB'});
  }
 
  pits.forEach(p => p.x -= speed); pits = pits.filter(p => p.x+p.width > -50);
 
  coinTrails.forEach(c => {
    c.x -= speed;
    if(!c.collected && zombies.some(z => Math.abs(z.x-c.x)<25 && Math.abs(z.y-c.y)<30)){
      c.collected=true; currentCoins++; totalCoins++; playSound('coin'); addParticles(c.x,c.y,'#fbc02d',6);
    }
  });
  coinTrails = coinTrails.filter(c => c.x>-30 && !c.collected);
 
  // Hộp bí ẩn: zombie nào chạm cũng nhặt được
  powerups.forEach(pw => {
    pw.x -= speed;
    const picker = zombies.find(z => Math.abs(z.x-pw.x)<35 && Math.abs(z.y-pw.y)<40);
    if(!pw.collected && picker){
      pw.collected=true; playSound('powerup'); triggerShake(16);
      if(Math.random()<.5){ tsunamiActive=true; tsunamiTimer=bonusDuration; giantActive=false; addParticles(pw.x,pw.y,'#00e5ff',35); }
      else { giantActive=true; giantTimer=bonusDuration; tsunamiActive=false; addParticles(pw.x,pw.y,'#76ba1b',35); }
    }
  });
  powerups = powerups.filter(p => p.x>-50 && !p.collected);
 
  let blocked = false;
  for(let oi=obstacles.length-1; oi>=0; oi--){
    const obs = obstacles[oi]; obs.x -= speed; if(obs.hitCooldown>0) obs.hitCooldown--;
    const isVeh = obs.type!=='BOMB';
    if(tsunamiActive || giantActive){
      if(Math.abs(zombies[0].x-obs.x)<140){
        playSound('explode'); triggerShake(10);
        addParticles(obs.x+obs.w/2,obs.y,giantActive?'#e040fb':'#00e5ff',30);
        if(isVeh){ eatReward(obs.peopleInside,10); for(let k=0;k<obs.peopleInside;k++) addZombie(20); }
        else score += 2;
        obstacles.splice(oi,1);
      }
    } else if(isVeh){
      const leader = zombies[0];
      const above = leader && leader.y < obs.y-12;
      if(leader && !above && leader.x+8>=obs.x && leader.x-12<=obs.x+obs.w && leader.y>=obs.y-15){
        if(zombies.length >= obs.reqZombies){
          playSound('explode'); triggerShake(15); addParticles(obs.x+obs.w/2,obs.y+obs.h/2,'#ff9800',35);
          eatReward(obs.peopleInside,10); for(let k=0;k<obs.peopleInside;k++) addZombie(22);
          obstacles.splice(oi,1);
        } else {
          blocked = true;
          if(obs.hitCooldown===0){
            obs.hitCooldown=30; playSound('explode'); triggerShake(8);
            const v = zombies.pop(); if(v) addParticles(v.x,v.y,'#ff1744',25);
            if(zombies.length===0){ triggerGameOver(); return; }
          }
        }
      }
    } else {
      // BOM: bán kính nhỏ -> nhảy qua là né được
      const bx=obs.x+22, by=obs.y+22;
      for(let i=zombies.length-1;i>=0;i--){
        const z=zombies[i];
        if(Math.hypot(z.x-bx,z.y-by)<40){
          playSound('explode'); triggerShake(20); addParticles(bx,by,'#ff1744',45);
          zombies.splice(i,1); obstacles.splice(oi,1); break;
        }
      }
    }
  }
  if(zombies.length===0){ triggerGameOver(); return; }
 
  // Vật lý từng zombie
  for(let i=zombies.length-1;i>=0;i--){
    const z = zombies[i];
    if(tsunamiActive){ z.y = defaultGroundY-110+Math.sin(frame*.15+i*.4)*8; z.vy=0; z.isGrounded=true; }
    else if(giantActive){ z.y = defaultGroundY-35; z.vy=0; z.isGrounded=true; }
    else {
      z.vy += gravity; z.y += z.vy;
      const onPit = isOverPit(z.x,8); let onVeh=false;
      obstacles.forEach(obs => {
        if(obs.type!=='BOMB' && z.x>=obs.x-5 && z.x<=obs.x+obs.w+5){
          const roofY = obs.y-18;
          if(z.y>=roofY-5 && z.y<=obs.y+12 && z.vy>=0){ z.y=roofY; z.vy=0; z.isGrounded=true; onVeh=true; }
        }
      });
      if(!onVeh){
        if(!onPit && z.y>=defaultGroundY-20){ z.y=defaultGroundY-20; z.vy=0; z.isGrounded=true; }
        else if(onPit) z.isGrounded=false;
      }
    }
    z.legAngle += z.isGrounded ? .22 : .08;
    if(blocked && i===0) z.x = Math.max(100, z.x-speed);
    if(z.y > canvas.height+30){ addParticles(z.x,canvas.height-10,'#76ba1b',12); zombies.splice(i,1); }
  }
  if(zombies.length===0){ triggerGameOver(); return; }
 
  // Đội hình: đầu đàn tự về vị trí chuẩn, các con khác bám theo
  zombies.forEach((z,i) => {
    if(i===0){ z.x += (180-z.x)*.05; return; }
    const ring = Math.ceil(Math.sqrt(i));
    const slot = zombies[0].x - ring*18 + (i%3)*7;
    z.x += (slot-z.x)*.12;
  });
 
  // Người: hoảng loạn bỏ chạy, cả đàn đều ăn được
  humans.forEach(h => {
    h.x -= speed;
    const leader = zombies[0];
    if(leader && h.x>leader.x && h.x-leader.x<280) h.panic = true;
    if(h.panic){ h.x += 2.2; h.step += .4; }
    if(h.eaten) return;
    const power = tsunamiActive || giantActive;
    const eater = power ? (h.x<450 ? zombies[0] : null)
                        : zombies.find(z => Math.abs(z.x-h.x)<30 && Math.abs(z.y-h.y)<50);
    if(eater){
      h.eaten = true; eatReward(1,5); playSound('eat');
      addParticles(h.x,h.y-10,giantActive?'#e040fb':(tsunamiActive?'#00e5ff':'#76ba1b'),15);
      addZombie(20);
    }
  });
  humans = humans.filter(h => h.x>-50 && !h.eaten);
  obstacles = obstacles.filter(o => o.x>-200);
  particles.forEach(p => { p.x+=p.vx; p.y+=p.vy; p.life--; });
  particles = particles.filter(p => p.life>0);
}
 
// ---------- Vẽ map ----------
function drawBeachMap(){
  let g = ctx.createLinearGradient(0,0,0,220); g.addColorStop(0,'#0288d1'); g.addColorStop(1,'#81d4fa');
  ctx.fillStyle=g; ctx.fillRect(0,0,800,220);
  ctx.fillStyle='rgba(255,255,255,.9)';
  let cx=(300-bgOffset*.15)%900; if(cx<-100) cx+=900;
  ctx.beginPath(); ctx.arc(cx,50,22,0,7); ctx.arc(cx+30,42,30,0,7); ctx.arc(cx+65,50,22,0,7); ctx.fill();
  let sg = ctx.createLinearGradient(0,170,0,295); sg.addColorStop(0,'#00838f'); sg.addColorStop(.5,'#00acc1'); sg.addColorStop(1,'#4dd0e1');
  ctx.fillStyle=sg; ctx.fillRect(0,170,800,125);
  ctx.fillStyle='rgba(255,255,255,.7)'; ctx.beginPath();
  for(let x=0;x<800;x+=22) ctx.arc(x,260+Math.sin((x+bgOffset*2.5)*.06)*4,9,0,7);
  ctx.fill();
  const hs=380;
  for(let hx=-(bgOffset*.45%hs); hx<800+hs; hx+=hs){
    ctx.fillStyle='#ffccbc'; ctx.fillRect(hx,195,90,85);
    ctx.fillStyle='#37474f'; ctx.fillRect(hx+32,230,24,50);
    ctx.fillStyle='#e1f5fe'; ctx.fillRect(hx+12,210,18,18); ctx.fillRect(hx+60,210,18,18);
    ctx.fillStyle='#c62828'; ctx.beginPath(); ctx.moveTo(hx-8,195); ctx.lineTo(hx+45,145); ctx.lineTo(hx+98,195); ctx.fill();
  }
  ctx.fillStyle='#e0a96d'; ctx.fillRect(0,295,800,35);
  const us=320;
  for(let ux=-(bgOffset*.6%us); ux<800+us; ux+=us){
    ctx.fillStyle='#ff1744'; ctx.beginPath(); ctx.arc(ux,260,26,Math.PI,Math.PI*2); ctx.fill();
    ctx.strokeStyle='#4e342e'; ctx.lineWidth=4; ctx.beginPath(); ctx.moveTo(ux,260); ctx.lineTo(ux,298); ctx.stroke();
    ctx.fillStyle='#29b6f6'; ctx.fillRect(ux+25,285,28,10);
  }
  let tx=(200-bgOffset*.75)%900; if(tx<-100) tx+=900;
  ctx.strokeStyle='#5d4037'; ctx.lineWidth=16; ctx.lineCap='round';
  ctx.beginPath(); ctx.moveTo(tx,305); ctx.quadraticCurveTo(tx-22,220,tx+25,145); ctx.stroke();
  ctx.fillStyle='#1b5e20';
  for(let a=0;a<6;a++){ const an=a*Math.PI/3; ctx.beginPath(); ctx.ellipse(tx+25+Math.cos(an)*36,145+Math.sin(an)*22,38,14,an,0,7); ctx.fill(); }
}
function drawCityMap(){
  let g = ctx.createLinearGradient(0,0,0,220); g.addColorStop(0,'#1a237e'); g.addColorStop(1,'#4a148c');
  ctx.fillStyle=g; ctx.fillRect(0,0,800,220);
  for(let b=0;b<6;b++){
    let bx=(b*200-bgOffset*.2)%1200; if(bx<-150) bx+=1200;
    const bh=100+(b*40)%100;
    ctx.fillStyle='#263238'; ctx.fillRect(bx,220-bh,100,bh); ctx.fillStyle='#ffeb3b';
    for(let r=0;r<Math.floor(bh/18);r++) for(let c=0;c<3;c++) if((b+r+c)%2===0) ctx.fillRect(bx+12+c*26,220-bh+10+r*18,12,10);
  }
  ctx.fillStyle='#37474f'; ctx.fillRect(0,295,800,35);
}
function drawVillageMap(){
  let g = ctx.createLinearGradient(0,0,0,220); g.addColorStop(0,'#f57c00'); g.addColorStop(1,'#ffb300');
  ctx.fillStyle=g; ctx.fillRect(0,0,800,220);
  const hs=350;
  for(let hx=-(bgOffset*.45%hs); hx<800+hs; hx+=hs){
    ctx.fillStyle='#5d4037'; ctx.fillRect(hx,215,80,80);
    ctx.fillStyle='#3e2723'; ctx.fillRect(hx+28,245,24,50);
    ctx.fillStyle='#ff8f00'; ctx.beginPath(); ctx.moveTo(hx-10,215); ctx.lineTo(hx+40,160); ctx.lineTo(hx+90,215); ctx.fill();
  }
  ctx.fillStyle='#558b2f'; ctx.fillRect(0,295,800,35);
}
function drawBackground(){
  ctx.clearRect(0,0,800,450); ctx.save();
  if(shakeDuration>0){ shakeDuration--; ctx.translate((Math.random()-.5)*10,(Math.random()-.5)*10); }
  if(currentMap==='BEACH') drawBeachMap(); else if(currentMap==='CITY') drawCityMap(); else drawVillageMap();
 
  ctx.fillStyle='#3e2723'; ctx.fillRect(0,defaultGroundY,800,120);
  ctx.fillStyle='#212121'; ctx.fillRect(0,defaultGroundY,800,16);
  ctx.fillStyle='#37474f'; ctx.fillRect(0,defaultGroundY+16,800,450-defaultGroundY-16);
  pits.forEach(p => {
    ctx.fillStyle='#0a0a0a'; ctx.fillRect(p.x,defaultGroundY,p.width,450-defaultGroundY);
    ctx.fillStyle='#111'; ctx.fillRect(p.x-6,defaultGroundY,6,450-defaultGroundY); ctx.fillRect(p.x+p.width,defaultGroundY,6,450-defaultGroundY);
  });
  ctx.strokeStyle='#fbc02d'; ctx.lineWidth=4;
  for(let x=-(bgOffset%50); x<800; x+=50) if(!isOverPit(x,30)){ ctx.beginPath(); ctx.moveTo(x,defaultGroundY+45); ctx.lineTo(x+30,defaultGroundY+45); ctx.stroke(); }
 
  if(tsunamiActive){
    const wx = zombies[0] ? zombies[0].x+40 : 250;
    let wg = ctx.createLinearGradient(0,30,0,defaultGroundY+50);
    wg.addColorStop(0,'#fff'); wg.addColorStop(.25,'#80d8ff'); wg.addColorStop(.65,'#0097a7'); wg.addColorStop(1,'#002f6c');
    ctx.fillStyle=wg; ctx.beginPath(); ctx.moveTo(-100,defaultGroundY+50); ctx.lineTo(-100,90);
    ctx.bezierCurveTo(wx-180,50,wx-30,10,wx+35,100); ctx.bezierCurveTo(wx+90,170,wx+110,260,wx+40,defaultGroundY+50);
    ctx.closePath(); ctx.fill();
    ctx.fillStyle='#fff';
    for(let b=0;b<8;b++){ ctx.beginPath(); ctx.arc(wx+12+b*11,95-b*5,16-b*1.3,0,7); ctx.fill(); }
  }
}
 
// ---------- Vẽ nhân vật / vật thể ----------
function drawGiantMonster(){
  const gX=180, gY=defaultGroundY-50;
  let bg = ctx.createRadialGradient(gX-12,gY-25,8,gX,gY,72); bg.addColorStop(0,'#ccff90'); bg.addColorStop(.5,'#76ba1b'); bg.addColorStop(1,'#1b5e20');
  ctx.fillStyle=bg; ctx.beginPath(); ctx.arc(gX,gY-10,72,0,7); ctx.fill();
  ctx.fillStyle='#111'; ctx.fillRect(gX-18,gY-78,36,6); ctx.fillRect(gX-11,gY-105,22,27);
  ctx.fillStyle='#b71c1c'; ctx.fillRect(gX-11,gY-84,22,5);
  ctx.fillStyle='#fbc02d'; ctx.fillRect(gX-22,gY+52,16,12); ctx.fillRect(gX+6,gY+52,16,12);
  [[-35,-32,20],[12,-40,22],[42,-14,16],[-10,-8,26]].forEach(([dx,dy,r]) => {
    const ex=gX+dx, ey=gY+dy;
    ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(ex,ey,r,0,7); ctx.fill();
    ctx.fillStyle='#00e5ff'; ctx.beginPath(); ctx.arc(ex+3,ey,r*.55,0,7); ctx.fill();
    ctx.fillStyle='#000'; ctx.beginPath(); ctx.arc(ex+4,ey,r*.25,0,7); ctx.fill();
    ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(ex+1,ey-3,2,0,7); ctx.fill();
  });
  ctx.fillStyle='#110022'; ctx.beginPath(); ctx.ellipse(gX+18,gY+28,30,16,.1,0,7); ctx.fill();
  ctx.fillStyle='#fff'; ctx.beginPath(); ctx.moveTo(gX,gY+20); ctx.lineTo(gX+6,gY+30); ctx.lineTo(gX+12,gY+20); ctx.fill();
  ctx.strokeStyle='#4a148c'; ctx.lineWidth=14; ctx.lineCap='round';
  ctx.beginPath(); ctx.moveTo(gX+35,gY+30); ctx.bezierCurveTo(gX+80,gY+40,gX+130,gY+10,gX+180,gY+25); ctx.stroke();
  let lg = ctx.createLinearGradient(gX+30,gY-20,800,gY-20);
  lg.addColorStop(0,'#fff'); lg.addColorStop(.15,'#ff007f'); lg.addColorStop(.7,'#e040fb'); lg.addColorStop(1,'#fff');
  ctx.strokeStyle=lg; ctx.lineWidth=26+Math.sin(frame*.4)*6;
  ctx.beginPath(); ctx.moveTo(gX+30,gY-25); ctx.lineTo(800,gY-25); ctx.stroke();
}
function drawHuman(h){
  ctx.save(); ctx.translate(h.x,h.y);
  const m = h.gender==='MALE';
  ctx.fillStyle='#ffcc80'; ctx.beginPath(); ctx.arc(0,-16,7,0,7); ctx.fill();
  ctx.fillStyle=m?'#5d4037':'#fbc02d'; ctx.beginPath(); ctx.arc(0,-19,7,Math.PI,Math.PI*2); ctx.fill();
  ctx.fillStyle='#000'; ctx.beginPath(); ctx.arc(-2.5,-16,1.2,0,7); ctx.arc(2.5,-16,1.2,0,7); ctx.fill();
  ctx.fillStyle=m?'#1e88e5':'#e91e63'; ctx.fillRect(-5,-9,10,8);
  ctx.fillStyle=m?'#283593':'#ad1457'; ctx.fillRect(-5,-1,10,7);
  if(h.panic){
    ctx.strokeStyle='#ffcc80'; ctx.lineWidth=2; ctx.beginPath();
    ctx.moveTo(-5,-8); ctx.lineTo(-9,-16+Math.sin(h.step)*3); ctx.moveTo(5,-8); ctx.lineTo(9,-16-Math.sin(h.step)*3); ctx.stroke();
    ctx.fillStyle='#ff1744'; ctx.font='bold 16px sans-serif'; ctx.textAlign='center'; ctx.fillText('!',0,-30+Math.sin(h.step)*2);
  }
  ctx.restore();
}
function drawZombie(z,scale=1,ox=0,oy=0){
  ctx.save(); ctx.translate(z.x+ox,z.y+oy); ctx.scale(scale,scale);
  const near = humans.some(h => h.x-z.x>0 && h.x-z.x<110), v = z.variant||0;
  const shirt = v===0?'#1e272e':(v===1?'#d63031':'#f1c40f'), pant = v===0?'#4b382a':(v===1?'#880e4f':'#2d3436');
  const s = Math.sin(z.legAngle);
  if(equippedOutfit==='MUMMY'){
    ctx.strokeStyle='#d7ccc8'; ctx.lineWidth=5; ctx.beginPath();
    ctx.moveTo(-4,6); ctx.lineTo(-4+s*7,18); ctx.moveTo(4,6); ctx.lineTo(4-s*7,18); ctx.stroke();
    ctx.fillStyle='#efebe9'; ctx.fillRect(-9,-5,18,14);
    ctx.fillStyle='#d7ccc8'; ctx.beginPath(); ctx.arc(0,-15,16,0,7); ctx.fill();
    ctx.fillStyle='#111'; ctx.fillRect(-10,-21,20,9);
    ctx.fillStyle='#ff1744'; ctx.beginPath(); ctx.arc(-2,-16,3,0,7); ctx.arc(6,-16,3,0,7); ctx.fill();
  } else {
    ctx.strokeStyle='#76ba1b'; ctx.lineWidth=5; ctx.beginPath();
    ctx.moveTo(-5,6); ctx.lineTo(-5+s*8,18); ctx.moveTo(5,6); ctx.lineTo(5-s*8,18); ctx.stroke();
    ctx.fillStyle='#558b2f'; ctx.beginPath(); ctx.arc(-5+s*8,19,3.5,0,7); ctx.arc(5-s*8,19,3.5,0,7); ctx.fill();
    ctx.fillStyle=pant; ctx.fillRect(-8,2,16,7);
    ctx.fillStyle=shirt; ctx.fillRect(-9,-6,18,10);
    ctx.fillStyle='#76ba1b'; ctx.beginPath(); ctx.ellipse(0,-16,17,15,.1,0,7); ctx.fill();
    ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(8,-18,10,0,7); ctx.fill();
    ctx.fillStyle='#00e5ff'; ctx.beginPath(); ctx.arc(9,-18,5.5,0,7); ctx.fill();
    ctx.fillStyle='#111'; ctx.beginPath(); ctx.arc(10,-18,2.5,0,7); ctx.fill();
    ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(8,-20,1.5,0,7); ctx.fill();
    if(near){
      ctx.fillStyle='#111'; ctx.beginPath(); ctx.arc(13,-8,12,0,7); ctx.fill();
      ctx.fillStyle='#fff'; ctx.beginPath(); ctx.moveTo(7,-14); ctx.lineTo(10,-6); ctx.lineTo(13,-14); ctx.moveTo(11,-2); ctx.lineTo(14,-10); ctx.lineTo(17,-2); ctx.fill();
    } else {
      ctx.fillStyle='#1b5e20'; ctx.beginPath(); ctx.arc(8,-8,5,0,Math.PI); ctx.fill();
      ctx.fillStyle='#fff'; ctx.beginPath(); ctx.moveTo(5,-8); ctx.lineTo(7,-4); ctx.lineTo(9,-8); ctx.fill();
    }
    ctx.strokeStyle='#76ba1b'; ctx.lineWidth=4; ctx.beginPath(); ctx.moveTo(3,-2); ctx.lineTo(16,2); ctx.moveTo(3,1); ctx.lineTo(15,6); ctx.stroke();
  }
  if(equippedHat==='HAT'){ ctx.fillStyle='#795548'; ctx.fillRect(-18,-33,36,4); ctx.fillRect(-10,-44,20,12); }
  else if(equippedHat==='PUMPKIN'){ ctx.fillStyle='#ff6f00'; ctx.beginPath(); ctx.arc(0,-33,12,0,7); ctx.fill(); ctx.fillStyle='#33691e'; ctx.fillRect(-2,-48,4,6); }
  ctx.restore();
}
function drawMysteryBox(pw){
  ctx.save(); ctx.translate(pw.x+pw.w/2,pw.y+pw.h/2+Math.sin(frame*.1)*4); ctx.rotate(-.08);
  ctx.fillStyle='#dcdde1'; ctx.fillRect(-pw.w/2+4,-pw.h/2+4,pw.w,pw.h);
  ctx.fillStyle='#fff'; ctx.fillRect(-pw.w/2,-pw.h/2,pw.w,pw.h);
  ctx.strokeStyle='#2f3640'; ctx.lineWidth=3; ctx.strokeRect(-pw.w/2,-pw.h/2,pw.w,pw.h);
  ctx.fillStyle='#00a8ff'; ctx.font='900 26px sans-serif'; ctx.textAlign='center'; ctx.fillText('?',0,9);
  ctx.restore();
}
function drawBomb(o){
  ctx.save(); ctx.translate(o.x+22,o.y+22);
  let bg = ctx.createRadialGradient(-4,-4,2,0,0,22); bg.addColorStop(0,'#555'); bg.addColorStop(.7,'#222'); bg.addColorStop(1,'#000');
  ctx.fillStyle=bg; ctx.beginPath(); ctx.arc(0,0,21,0,7); ctx.fill();
  ctx.fillStyle='#111';
  for(let a=0;a<8;a++){ const an=a*Math.PI/4; ctx.beginPath(); ctx.arc(Math.cos(an)*21,Math.sin(an)*21,4.5,0,7); ctx.fill(); }
  let gg = ctx.createRadialGradient(0,0,2,0,0,12); gg.addColorStop(0,'#fff'); gg.addColorStop(.5,'#ff1744'); gg.addColorStop(1,'#b71c1c');
  ctx.fillStyle=gg; ctx.beginPath(); ctx.arc(0,0,11+Math.sin(frame*.3)*2,0,7); ctx.fill();
  ctx.restore();
}
function drawCoin(c){
  ctx.save(); ctx.translate(c.x,c.y);
  ctx.fillStyle='#fbc02d'; ctx.beginPath(); ctx.arc(0,0,9,0,7); ctx.fill();
  ctx.fillStyle='#fff59d'; ctx.beginPath(); ctx.arc(0,0,6,0,7); ctx.fill();
  ctx.fillStyle='#f57f17'; ctx.font='bold 10px sans-serif'; ctx.textAlign='center'; ctx.fillText('$',0,3.5);
  ctx.restore();
}
function drawBadge(x,y,req){
  ctx.save(); ctx.translate(x,y);
  const ok = zombies.length >= req;
  ctx.fillStyle='#111'; ctx.beginPath(); ctx.roundRect(0,0,85,42,10); ctx.fill();
  ctx.strokeStyle = ok ? '#76ba1b' : '#ff9800'; ctx.lineWidth=3; ctx.stroke();
  ctx.fillStyle='#111'; ctx.beginPath(); ctx.moveTo(18,42); ctx.lineTo(26,50); ctx.lineTo(34,42); ctx.fill();
  ctx.fillStyle='#76ba1b'; ctx.beginPath(); ctx.arc(20,21,11,0,7); ctx.fill();
  ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(23,20,4.5,0,7); ctx.fill();
  ctx.fillStyle='#111'; ctx.beginPath(); ctx.arc(24,20,2,0,7); ctx.fill();
  ctx.fillStyle='#fff'; ctx.font='900 16px sans-serif'; ctx.textAlign='left'; ctx.fillText(`${zombies.length}`,38,26);
  ctx.fillStyle = ok ? '#76ba1b' : '#ff3d00'; ctx.fillText(`/${req}`,56,26);
  ctx.restore();
}
function drawCar(o){
  ctx.save(); ctx.translate(o.x,o.y);
  ctx.fillStyle='#d32f2f'; ctx.fillRect(0,18,o.w,22);
  ctx.fillStyle='#b71c1c'; ctx.fillRect(16,3,58,16);
  ctx.fillStyle='#81d4fa'; ctx.fillRect(20,5,20,11); ctx.fillRect(48,5,22,11);
  ctx.fillStyle='#111'; ctx.beginPath(); ctx.arc(20,40,9,0,7); ctx.arc(o.w-20,40,9,0,7); ctx.fill();
  drawBadge(5,-55,o.reqZombies); ctx.restore();
}
function drawBus(o){
  ctx.save(); ctx.translate(o.x,o.y);
  ctx.fillStyle='#fbc02d'; ctx.fillRect(0,0,o.w,56);
  ctx.fillStyle='#f57f17'; ctx.fillRect(0,32,o.w,6);
  ctx.fillStyle='#81d4fa'; for(let k=0;k<5;k++) ctx.fillRect(12+k*28,8,20,20);
  ctx.fillStyle='#111'; ctx.beginPath(); ctx.arc(24,56,10,0,7); ctx.arc(o.w-24,56,10,0,7); ctx.fill();
  drawBadge(35,-58,o.reqZombies); ctx.restore();
}
function drawHelicopter(o){
  ctx.save(); ctx.translate(o.x,o.y);
  ctx.fillStyle='#fff'; ctx.beginPath(); ctx.moveTo(0,36); ctx.bezierCurveTo(-5,-14,60,-28,170,-18); ctx.lineTo(210,36); ctx.lineTo(0,36); ctx.fill();
  ctx.fillStyle='#76ba1b'; ctx.fillRect(50,6,145,14);
  ctx.fillStyle='#263238'; ctx.beginPath(); ctx.arc(26,14,11,0,7); ctx.fill();
  ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(24,12,3.5,0,7); ctx.fill();
  ctx.fillStyle='#263238'; for(let i=0;i<6;i++) ctx.fillRect(64+i*20,9,14,13);
  ctx.fillStyle='#2e7d32'; ctx.font='900 17px sans-serif'; ctx.textAlign='left'; ctx.fillText('Z.AIRLINE',75,-3);
  ctx.fillStyle='#cfd8dc'; ctx.fillRect(110,32,55,24);
  ctx.fillStyle='#111'; ctx.beginPath(); ctx.arc(125,58,10,0,7); ctx.arc(148,58,10,0,7); ctx.fill();
  drawBadge(55,-62,o.reqZombies); ctx.restore();
}
 
function draw(){
  drawBackground();
  if(gameState==='MENU'){
    drawZombie({x:220,y:defaultGroundY-20,legAngle:frame*.2,variant:0});
    ctx.restore(); return;
  }
  coinTrails.forEach(drawCoin); powerups.forEach(drawMysteryBox); humans.forEach(drawHuman);
  obstacles.forEach(o => {
    if(o.type==='BOMB') drawBomb(o); else if(o.type==='CAR') drawCar(o);
    else if(o.type==='BUS') drawBus(o); else drawHelicopter(o);
  });
  if(giantActive) drawGiantMonster();
  else zombies.forEach((z,idx) => {
    drawZombie(z, 1-Math.min(idx*.012,.25), (idx%3===2)?-6:0, (idx%2===1)?-Math.min(idx*1.8,18):0);
  });
  particles.forEach(p => { ctx.fillStyle=p.color; ctx.fillRect(p.x,p.y,4,4); });
  ctx.restore();
 
  // HUD
  ctx.fillStyle='rgba(0,0,0,.5)'; ctx.fillRect(15,12,170,98);
  ctx.textAlign='left'; ctx.font='bold 22px sans-serif';
  ctx.fillStyle='#fbc02d'; ctx.fillText(`🪙 ${totalCoins}`,25,40);
  ctx.fillStyle='#76ba1b'; ctx.fillText(`🧠 x${zombies.length}`,25,70);
  ctx.fillStyle='#fff'; ctx.fillText(`📏 ${Math.floor(distance)} m`,25,100);
 
  let mapName = '🌊 Map: Bãi Biển';
  if(currentMap==='CITY') mapName='🌆 Map: Thành Phố'; else if(currentMap==='VILLAGE') mapName='🌾 Map: Làng Quê';
  ctx.fillStyle='rgba(0,0,0,.5)'; ctx.fillRect(630,12,155,35);
  ctx.fillStyle='#80d8ff'; ctx.font='bold 15px sans-serif'; ctx.textAlign='center'; ctx.fillText(mapName,707,35);
 
  if(tsunamiActive || giantActive){
    const t = (tsunamiActive?tsunamiTimer:giantTimer), full = power2Level===1?360:(power2Level===2?480:600);
    ctx.fillStyle='rgba(0,0,0,.5)'; ctx.fillRect(300,12,200,16);
    ctx.fillStyle = tsunamiActive ? '#00e5ff' : '#e040fb'; ctx.fillRect(302,14,196*t/full,12);
  }
 
  if(gameState==='GAMEOVER'){
    ctx.fillStyle='rgba(0,0,0,.85)'; ctx.fillRect(0,0,800,450);
    ctx.textAlign='center';
    ctx.fillStyle='#ff1744'; ctx.font='bold 42px sans-serif'; ctx.fillText('GAME OVER',400,160);
    ctx.fillStyle='#fff'; ctx.font='22px sans-serif';
    ctx.fillText(`Số người nuốt chửng: ${score}`,400,210);
    ctx.fillText(`Quãng đường: ${Math.floor(distance)} m`,400,240);
    ctx.fillText(`Xu thu thập được: 🪙 +${currentCoins}`,400,270);
    ctx.fillText('Nhấn Space / Chạm để quay về Menu',400,315);
  }
}
 
function loop(){ update(); draw(); requestAnimationFrame(loop); }
updateMarketUI(); updateMissionUI();
loop();
</script>
</body>
</html>
"""
 
components.html(game_code, height=480, scrolling=False)
