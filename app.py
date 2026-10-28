
import streamlit as st
 
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
 
if(typeof CanvasRenderingContext2D!=='undefined' && !CanvasRenderingContext2D.prototype.roundRect){
  CanvasRenderingContext2D.prototype.roundRect=function(x,y,w,h,r){ r=Array.isArray(r)?(r[0]||0):(r||0);
    this.moveTo(x+r,y); this.arcTo(x+w,y,x+w,y+h,r); this.arcTo(x+w,y+h,x,y+h,r); this.arcTo(x,y+h,x,y,r); this.arcTo(x,y,x+w,y,r); this.closePath(); };
}
const $ = id => document.getElementById(id);
const canvas = $('gameCanvas'), ctx = canvas.getContext('2d');
const menuOverlay = $('menuOverlay'), playBtn = $('playBtn'), bestScoreText = $('bestScoreText');
const bgMusic = $('bgMusic'), musicToggleBtn = $('musicToggleBtn');
let isMuted = false;
 
// ---------- Âm thanh ----------
const AudioCtx = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;
function initAudio(){ try{ if(!audioCtx && AudioCtx) audioCtx = new AudioCtx(); if(audioCtx && audioCtx.state==='suspended') audioCtx.resume(); }catch(e){ audioCtx=null; } }
const SFX = {
  jump:   ['sine',280,580,.12,.2,'exponentialRampToValueAtTime'],
  eat:    ['triangle',150,350,.1,.3,'exponentialRampToValueAtTime'],
  coin:   ['sine',988,1318,.18,.18,'setValueAtTime'],
  powerup:['square',300,900,.25,.25,'exponentialRampToValueAtTime'],
  shot:['square',700,200,.08,.12,'exponentialRampToValueAtTime'],
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
let currentCoins = 0, speed = 4.5, frame = 0, holding=false, paused=false, bullets=[], tutSpawned=false;
let tutorialDone = store.getItem('zt_tut')==='1';
const SOLID=['CAR','BUS','HELI','WALL'];
const buffs={magnet:0,shield:0,double:0};
let banner={t:'',life:0};
const bonusDur=()=>power2Level===1?360:(power2Level===2?480:600);
const gravity = 0.65, defaultGroundY = 330;
let zombies=[], humans=[], obstacles=[], pits=[], powerups=[], coinTrails=[], particles=[], bgOffset=0;
let tsunamiActive=false, tsunamiTimer=0, giantActive=false, giantTimer=0;
 
function addParticles(x,y,color,count=12){
  for(let i=0;i<count;i++) particles.push({x,y,vx:(Math.random()-.5)*8,vy:(Math.random()-.5)*8,life:25,color});
}
function startGame(){ resetGame(); gameState='PLAYING'; menuOverlay.style.display='none'; playMusic(); }
playBtn.addEventListener('click', startGame);
function togglePause(){ if(gameState!=='PLAYING') return; paused=!paused; if(paused) bgMusic.pause(); else playMusic(); }
 
function handleInput(){
  if(paused) return;
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
    } else { if(!e.repeat){ if(paused) togglePause(); else handleInput(); } holding=true; }
  }
  if(e.code==='KeyP' || e.code==='Escape') togglePause();
});
window.addEventListener('keyup', e => { if(e.code==='Space' || e.code==='ArrowUp') holding=false; });
window.addEventListener('mouseup', () => { holding=false; });
window.addEventListener('touchend', () => { holding=false; });
window.addEventListener('blur', () => { holding=false; if(gameState==='PLAYING' && !paused) togglePause(); });
function pointerDown(e){
  const r=canvas.getBoundingClientRect(), t=(e.touches&&e.touches[0])||e;
  const px=(t.clientX-r.left)*800/r.width, py=(t.clientY-r.top)*450/r.height;
  if(gameState==='PLAYING' && px>748 && py<52){ togglePause(); return; }
  if(paused){ togglePause(); return; }
  holding=true; handleInput();
}
canvas.addEventListener('touchstart', e => { e.preventDefault(); pointerDown(e); });
canvas.addEventListener('mousedown', pointerDown);
 
function switchRandomMap(){
  const a = MAP_LIST.filter(m => m !== currentMap); currentMap = a[Math.floor(Math.random()*a.length)];
}
function resetGame(){
  score=0; currentCoins=0; speed=4.5; frame=0; distance=0;
  zombies = [];
  for(let i=0;i<power1Level;i++) zombies.push({x:180-i*22,y:defaultGroundY-20,vy:0,isGrounded:true,legAngle:i*.5,variant:i%3});
  humans=[]; obstacles=[]; pits=[]; powerups=[]; coinTrails=[]; particles=[]; bullets=[]; paused=false; tutSpawned=false; buffs.magnet=buffs.shield=buffs.double=0; banner.life=0;
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
  score += n; { const gain=n*mult*(buffs.double>0?2:1); currentCoins += gain; totalCoins += gain; } totalEatenHumans += n;
  if(score > maxSingleRunEaten) maxSingleRunEaten = score;
}
 
// ---------- Update ----------
function update(){
  if(paused) return;
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
  for(const b in buffs) if(buffs[b]>0) buffs[b]--;
 
  if(frame%280===0 && Math.random()>.35) pits.push({x:850,width:110+Math.random()*30});
 
  if(frame%160===0 && Math.random()<.6){
    const count = 5+Math.floor(Math.random()*4), coinY = defaultGroundY-40-(Math.random()>.5?40:0);
    for(let c=0;c<count;c++) coinTrails.push({x:850+c*24,y:coinY,collected:false});
  }
  if(frame%600===0 && !tsunamiActive && !giantActive && Math.random()<.6 && !isOverPit(850,40))
    powerups.push({x:850,y:defaultGroundY-60,w:38,h:38,collected:false});
 
  if(frame%130===0 && !isOverPit(850,200)){
    const r = (frame===130 && !tutorialDone) ? .4 : Math.random(), X = 850, G = defaultGroundY;
    if(r<.26) humans.push({x:X,y:G-20,gender:Math.random()>.5?'MALE':'FEMALE',eaten:false,panic:false,step:0,cop:Math.random()<.25,cd:70,flash:0});
    else if(r<.46){ const tut=!tutorialDone&&!tutSpawned; if(tut) tutSpawned=true; obstacles.push({x:X,y:G-48,w:100,h:48,type:'CAR',reqZombies:tut?Math.max(1,power1Level):4,peopleInside:3,hitCooldown:0,tut}); }
    else if(r<.58) obstacles.push({x:X,y:G-62,w:160,h:62,type:'BUS',reqZombies:6,peopleInside:6,hitCooldown:0});
    else if(r<.66) obstacles.push({x:X,y:G-78,w:210,h:68,type:'HELI',reqZombies:8,peopleInside:8,hitCooldown:0});
    else if(r<.76) obstacles.push({x:X,y:G-45,w:45,h:45,type:'BOMB'});
    else if(r<.86) obstacles.push({x:X,y:G-22,w:64,h:22,type:'SPIKE'});
    else if(r<.94) obstacles.push({x:X,y:G-16,w:44,h:16,type:'SPRING',comp:0});
    else obstacles.push({x:X,y:G-72,w:36,h:72,type:'WALL',reqZombies:3,peopleInside:0,hitCooldown:0});
  }
 
  pits.forEach(p => p.x -= speed); pits = pits.filter(p => p.x+p.width > -50);
 
  coinTrails.forEach(c => {
    c.x -= speed;
    if(buffs.magnet>0 && zombies[0] && !c.collected){ const l=zombies[0], dx=l.x-c.x, dy=l.y-c.y, d=Math.hypot(dx,dy)||1; if(d<280){ c.x+=dx/d*9; c.y+=dy/d*9; } }
    if(!c.collected && zombies.some(z => Math.abs(z.x-c.x)<25 && Math.abs(z.y-c.y)<30)){
      c.collected=true; { const cm=buffs.double>0?2:1; currentCoins+=cm; totalCoins+=cm; } playSound('coin'); addParticles(c.x,c.y,'#fbc02d',6);
    }
  });
  coinTrails = coinTrails.filter(c => c.x>-30 && !c.collected);
 
  // Hộp bí ẩn: zombie nào chạm cũng nhặt được
  powerups.forEach(pw => {
    pw.x -= speed;
    const picker = zombies.find(z => Math.abs(z.x-pw.x)<35 && Math.abs(z.y-pw.y)<40);
    if(!pw.collected && picker){
      pw.collected=true; playSound('powerup'); triggerShake(16);
      const roll=Math.floor(Math.random()*6), dur=bonusDuration;
      if(roll===0){ tsunamiActive=true; tsunamiTimer=dur; giantActive=false; addParticles(pw.x,pw.y,'#00e5ff',35); banner={t:'🌊 TSUNAMI!',life:80}; }
      else if(roll===1){ giantActive=true; giantTimer=dur; tsunamiActive=false; addParticles(pw.x,pw.y,'#76ba1b',35); banner={t:'👹 ZOMBIE KHỔNG LỒ!',life:80}; }
      else if(roll===2){ buffs.magnet=dur; addParticles(pw.x,pw.y,'#ff5252',30); banner={t:'🧲 NAM CHÂM XU!',life:80}; }
      else if(roll===3){ buffs.shield=dur; addParticles(pw.x,pw.y,'#40c4ff',30); banner={t:'🛡️ KHIÊN BẢO VỆ!',life:80}; }
      else if(roll===4){ buffs.double=dur; addParticles(pw.x,pw.y,'#ffd740',30); banner={t:'💰 XU x2!',life:80}; }
      else { for(let q=0;q<6;q++) addZombie(20); addParticles(pw.x,pw.y,'#8bc34a',30); banner={t:'🧟 +6 ZOMBIE!',life:80}; }
    }
  });
  powerups = powerups.filter(p => p.x>-50 && !p.collected);
 
  let blocked = false;
  for(let oi=obstacles.length-1; oi>=0; oi--){
    const obs = obstacles[oi]; obs.x -= speed; if(obs.hitCooldown>0) obs.hitCooldown--;
    const isVeh = SOLID.includes(obs.type);
    if(tsunamiActive || giantActive){
      if(Math.abs(zombies[0].x-obs.x)<140 && obs.type!=='SPRING'){
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
            if(buffs.shield<=0){ const v = zombies.pop(); if(v) addParticles(v.x,v.y,'#ff1744',25); }
            if(zombies.length===0){ triggerGameOver(); return; }
          }
        }
      }
    } else if(obs.type==='SPIKE'){
      const i=zombies.findIndex(z=>z.y+19>defaultGroundY-14 && z.x>obs.x-8 && z.x<obs.x+obs.w+8);
      if(i>=0){ playSound('explode'); triggerShake(10); addParticles(zombies[i].x,zombies[i].y,'#ff1744',25); if(buffs.shield<=0) zombies.splice(i,1); obstacles.splice(oi,1); }
    } else if(obs.type==='SPRING'){
      if(obs.comp>0) obs.comp--;
      zombies.forEach(z=>{ if(z.vy>=0 && z.y+19>=defaultGroundY-6 && z.x>obs.x-6 && z.x<obs.x+obs.w+6){ z.vy=-19; z.isGrounded=false; obs.comp=10; playSound('jump'); } });
    } else {
      // BOM: bán kính nhỏ -> nhảy qua là né được
      const bx=obs.x+22, by=obs.y+22;
      for(let i=zombies.length-1;i>=0;i--){
        const z=zombies[i];
        if(Math.hypot(z.x-bx,z.y-by)<40){
          playSound('explode'); triggerShake(20); addParticles(bx,by,'#ff1744',45);
          if(buffs.shield<=0) zombies.splice(i,1); obstacles.splice(oi,1); break;
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
      z.vy += (holding && z.vy<0) ? gravity*.6 : gravity; z.y += z.vy;
      const onPit = isOverPit(z.x,8); let onVeh=false;
      obstacles.forEach(obs => {
        if(SOLID.includes(obs.type) && z.x>=obs.x-5 && z.x<=obs.x+obs.w+5){
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
    if(h.cop){
      h.cd--; if(h.flash>0) h.flash--;
      if(h.cd<=0 && h.x<760 && leader && h.x>leader.x+90 && !(tsunamiActive||giantActive)){ bullets.push({x:h.x-24,y:defaultGroundY-26}); h.cd=110; h.flash=6; playSound('shot'); }
    } else if(leader && h.x>leader.x && h.x-leader.x<280) h.panic = true;
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
  bullets.forEach(b=>b.x-=speed+7);
  for(let bi=bullets.length-1;bi>=0;bi--){
    const b=bullets[bi]; if(b.x<-20){ bullets.splice(bi,1); continue; }
    if(tsunamiActive||giantActive) continue;
    const zi=zombies.findIndex(z=>Math.abs(z.x-b.x)<12 && b.y>z.y-42 && b.y<z.y+18);
    if(zi>=0){ playSound('explode'); triggerShake(6); addParticles(zombies[zi].x,zombies[zi].y,'#ff1744',18); if(buffs.shield<=0) zombies.splice(zi,1); bullets.splice(bi,1); }
  }
  if(zombies.length===0){ triggerGameOver(); return; }
  humans = humans.filter(h => h.x>-50 && !h.eaten);
  obstacles = obstacles.filter(o => o.x>-200);
  if(!tutorialDone && tutSpawned && !obstacles.some(o=>o.tut)){ tutorialDone=true; store.setItem('zt_tut','1'); }
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
 
function rnd(k,n){ const v=Math.sin(k*127.1+n*311.7)*43758.5453; return v-Math.floor(v); }
function tiles(sp,w,fn){ const base=Math.floor(bgOffset*sp/w); for(let i=-1;i<=800/w+1;i++){ const k=base+i; fn(k*w-bgOffset*sp,k); } }
function cloud(x,y,sc,a){ ctx.fillStyle='rgba(255,255,255,'+a+')'; ctx.beginPath(); ctx.arc(x,y,16*sc,0,7); ctx.arc(x+20*sc,y-8*sc,22*sc,0,7); ctx.arc(x+44*sc,y,17*sc,0,7); ctx.arc(x+22*sc,y+6*sc,18*sc,0,7); ctx.fill(); }
function birds(col){
  ctx.strokeStyle=col; ctx.lineWidth=2; ctx.lineCap='round';
  for(let i=0;i<5;i++){
    const x=((900-(frame*1.3+i*70))%950+950)%950-60, y=70+i*14+Math.sin(frame*.05+i)*6, f=Math.sin(frame*.3+i)*4;
    ctx.beginPath(); ctx.moveTo(x-7,y-f); ctx.quadraticCurveTo(x-3,y-4,x,y); ctx.quadraticCurveTo(x+3,y-4,x+7,y-f); ctx.stroke();
  }
}
function winGrid(x,y,w,h,cols,rows,seed,lit,off){
  const cw=w/cols, ch=h/rows;
  for(let r=0;r<rows;r++) for(let c=0;c<cols;c++){
    ctx.fillStyle = rnd(seed*13+c,r)>.45 ? lit : off;
    ctx.fillRect(x+c*cw+cw*.2,y+r*ch+ch*.2,cw*.6,ch*.55);
  }
}
 
function drawCityMap(){
  let g=ctx.createLinearGradient(0,0,0,300); g.addColorStop(0,'#7fb8e0'); g.addColorStop(1,'#e2f3fa'); ctx.fillStyle=g; ctx.fillRect(0,0,800,330);
  let sg=ctx.createRadialGradient(640,80,5,640,80,130); sg.addColorStop(0,'rgba(255,255,230,.9)'); sg.addColorStop(1,'rgba(255,255,230,0)'); ctx.fillStyle=sg; ctx.fillRect(480,0,320,230);
  tiles(.05,280,(x,k)=>cloud(x+rnd(k,2)*120,26+rnd(k,1)*80,.7+rnd(k,3)*.7,.85));
  tiles(.08,70,(x,k)=>{ const h=60+rnd(k,1)*90; ctx.fillStyle='#a9c6dc'; ctx.fillRect(x,300-h,64,h+40); if(rnd(k,2)>.7) ctx.fillRect(x+30,300-h-26,3,26); });
  tiles(.16,90,(x,k)=>{ const h=50+rnd(k,4)*110; ctx.fillStyle='#8aa9c4'; ctx.fillRect(x,300-h,82,h+40); winGrid(x+4,300-h+6,74,h-10,4,Math.max(2,Math.floor(h/14)),k,'rgba(255,255,255,.35)','rgba(0,0,0,0)'); });
  tiles(.26,110,(x,k)=>{
    const h=50+rnd(k,5)*70, col=['#b78f9f','#c4a08a','#9e8fb5'][Math.floor(rnd(k,6)*3)];
    ctx.fillStyle=col; ctx.fillRect(x,300-h,98,h+40); ctx.fillStyle='rgba(0,0,0,.12)'; ctx.fillRect(x,300-h,98,5);
    winGrid(x+6,300-h+12,86,h-20,5,Math.max(2,Math.floor(h/16)),k+7,'#ffe9a8','rgba(40,40,70,.45)');
    if(rnd(k,7)>.6){ ctx.fillStyle='#6d5a4a'; ctx.fillRect(x+66,300-h-18,20,14); ctx.fillRect(x+70,300-h-4,2,5); ctx.fillRect(x+80,300-h-4,2,5); }
  });
  tiles(.4,360,(x0,k)=>{
    const x=x0+60+rnd(k,8)*40, type=Math.floor(rnd(k,9)*3), top=300-(230+rnd(k,10)*70);
    if(type===2){
      let bg=ctx.createLinearGradient(x,0,x+110,0); bg.addColorStop(0,'#5c8fb8'); bg.addColorStop(.5,'#9ccbe6'); bg.addColorStop(1,'#4d7fa6');
      ctx.fillStyle=bg; ctx.fillRect(x,top,110,300-top);
      ctx.strokeStyle='rgba(255,255,255,.3)'; ctx.lineWidth=1;
      for(let y=top+14;y<300;y+=14){ ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x+110,y); ctx.stroke(); }
      for(let c=1;c<5;c++){ ctx.beginPath(); ctx.moveTo(x+c*22,top); ctx.lineTo(x+c*22,300); ctx.stroke(); }
      ctx.fillStyle='#5a6b78'; ctx.fillRect(x+53,top-34,4,34); ctx.fillStyle='#ff5252'; ctx.beginPath(); ctx.arc(x+55,top-36,3+Math.sin(frame*.1)*1,0,7); ctx.fill();
    } else {
      const curved=type===0;
      let bg=ctx.createLinearGradient(x,0,x+120,0); bg.addColorStop(0,'#c9d6e0'); bg.addColorStop(.35,'#ffffff'); bg.addColorStop(1,'#aebdca');
      ctx.fillStyle=bg; ctx.beginPath(); ctx.moveTo(x,300); ctx.lineTo(x,top+(curved?18:0));
      if(curved) ctx.quadraticCurveTo(x+60,top-14,x+120,top+18); else ctx.lineTo(x+120,top);
      ctx.lineTo(x+120,300); ctx.closePath(); ctx.fill();
      ctx.fillStyle='rgba(90,110,130,.35)'; for(let y=top+24;y<300;y+=14) ctx.fillRect(x,y,120,4);
      ctx.fillStyle='rgba(255,255,255,.55)'; ctx.fillRect(x+8,top+20,6,300-top-20);
      if(type===1){
        ctx.fillStyle='#37474f'; ctx.fillRect(x+16,top-8,4,10); ctx.fillRect(x+100,top-8,4,10); ctx.fillRect(x+8,top-34,104,28);
        ctx.fillStyle='#76ba1b'; ctx.font='900 17px "Arial Black",sans-serif'; ctx.textAlign='center'; ctx.fillText('ZOMBIE',x+60,top-13);
      }
    }
  });
  ctx.fillStyle='#55627e'; ctx.fillRect(0,296,800,34);
  tiles(.7,170,(x,k)=>{
    const col=['#7a5f8a','#c98f5a','#5f8a7a','#a6675b'][Math.floor(rnd(k,11)*4)];
    ctx.fillStyle=col; ctx.fillRect(x,262,150,36);
    ctx.fillStyle='#fff6c0'; ctx.fillRect(x+10,274,52,18); ctx.fillStyle='#2f3349'; ctx.fillRect(x+100,268,26,30);
    for(let a=0;a<10;a++){ ctx.fillStyle=a%2?'#ffffff':'#e53935'; ctx.fillRect(x+4+a*14.2,262,14.2,9); }
  });
  tiles(.85,260,(x,k)=>{
    if(rnd(k,12)>.35){ const tx=x+120; ctx.fillStyle='#5d4037'; ctx.fillRect(tx-3,252,6,46);
      ctx.fillStyle='#3f8f3f'; ctx.beginPath(); ctx.arc(tx,242,20,0,7); ctx.arc(tx-14,252,14,0,7); ctx.arc(tx+14,252,14,0,7); ctx.fill();
      ctx.fillStyle='#57ab4f'; ctx.beginPath(); ctx.arc(tx-5,236,11,0,7); ctx.fill(); }
  });
  tiles(.8,300,(x,k)=>{
    const lx=x+100; ctx.fillStyle='#2f3349'; ctx.fillRect(lx,240,4,56); ctx.fillRect(lx,240,18,4);
    ctx.fillStyle='#fff6b0'; ctx.beginPath(); ctx.arc(lx+18,247,5,0,7); ctx.fill();
    if(rnd(k,13)>.5){
      const tx=x+230; ctx.fillStyle='#2f3349'; ctx.fillRect(tx,226,4,70); ctx.fillStyle='#1b1d2b'; ctx.fillRect(tx-5,214,14,28);
      const ph=Math.floor(frame/90+k)%3; ['#ff5252','#ffd740','#69f0ae'].forEach((c,i)=>{ ctx.fillStyle=i===ph?c:'#3a3d50'; ctx.beginPath(); ctx.arc(tx+2,221+i*8,3,0,7); ctx.fill(); });
    }
    ctx.fillStyle='#e53935'; ctx.fillRect(x+170,284,9,12); ctx.fillRect(x+168,282,13,4);
  });
  birds('#46566e');
}
 
function drawVillageMap(){
  let g=ctx.createLinearGradient(0,0,0,300); g.addColorStop(0,'#ff8f5a'); g.addColorStop(.5,'#ffc27a'); g.addColorStop(1,'#ffeab8'); ctx.fillStyle=g; ctx.fillRect(0,0,800,330);
  let sg=ctx.createRadialGradient(560,200,10,560,200,170); sg.addColorStop(0,'rgba(255,250,200,.95)'); sg.addColorStop(1,'rgba(255,220,150,0)'); ctx.fillStyle=sg; ctx.fillRect(300,30,520,270);
  ctx.fillStyle='#fff6c8'; ctx.beginPath(); ctx.arc(560,200,30,0,7); ctx.fill();
  tiles(.04,300,(x,k)=>cloud(x+rnd(k,2)*150,30+rnd(k,1)*70,.8+rnd(k,3)*.6,.55));
  const hill=(sp,y0,amp,col,f)=>{ ctx.fillStyle=col; ctx.beginPath(); ctx.moveTo(0,330);
    for(let x=0;x<=800;x+=16) ctx.lineTo(x,y0+Math.sin((x+bgOffset*sp)*f)*amp+Math.sin((x+bgOffset*sp)*f*2.3)*amp*.4);
    ctx.lineTo(800,330); ctx.fill(); };
  hill(.08,205,24,'#a07fa8',.011); hill(.16,235,18,'#7aa353',.014);
  tiles(.3,560,(x,k)=>{
    if(rnd(k,1)>.3){
      const wx=x+120; ctx.fillStyle='#ecdcbc'; ctx.beginPath(); ctx.moveTo(wx-18,262); ctx.lineTo(wx-10,170); ctx.lineTo(wx+10,170); ctx.lineTo(wx+18,262); ctx.fill();
      ctx.fillStyle='#a63d2f'; ctx.beginPath(); ctx.moveTo(wx-14,172); ctx.lineTo(wx,150); ctx.lineTo(wx+14,172); ctx.fill();
      ctx.fillStyle='#5d4037'; ctx.fillRect(wx-5,240,10,22);
      ctx.save(); ctx.translate(wx,168); ctx.rotate(frame*.03);
      for(let b=0;b<4;b++){ ctx.rotate(Math.PI/2); ctx.fillStyle='#8a6a44'; ctx.fillRect(-3,-52,6,52); ctx.fillStyle='rgba(255,245,220,.9)'; ctx.fillRect(3,-50,16,34); }
      ctx.restore(); ctx.fillStyle='#5d4037'; ctx.beginPath(); ctx.arc(wx,168,5,0,7); ctx.fill();
    }
  });
  tiles(.45,330,(x,k)=>{
    const t=Math.floor(rnd(k,2)*3), hx=x+40;
    if(t===0){
      ctx.fillStyle='#e0c291'; ctx.fillRect(hx,220,92,76);
      ctx.fillStyle='#a63d2f'; ctx.beginPath(); ctx.moveTo(hx-12,222); ctx.lineTo(hx+46,168); ctx.lineTo(hx+104,222); ctx.fill();
      ctx.fillStyle='#7a4a3a'; ctx.fillRect(hx+70,172,14,34);
      for(let q=0;q<3;q++){ const p=(frame*.5+q*20)%60; ctx.fillStyle='rgba(240,240,240,'+(.6-p/100)+')'; ctx.beginPath(); ctx.arc(hx+77+p*.2,168-p,5+p*.1,0,7); ctx.fill(); }
      ctx.fillStyle='#4e342e'; ctx.fillRect(hx+36,254,20,42);
      ctx.fillStyle='#ffe28a'; ctx.fillRect(hx+8,236,20,20); ctx.fillRect(hx+64,236,20,20);
      ctx.strokeStyle='#6d4c41'; ctx.lineWidth=2; ctx.strokeRect(hx+8,236,20,20); ctx.strokeRect(hx+64,236,20,20);
      ctx.beginPath(); ctx.moveTo(hx+18,236); ctx.lineTo(hx+18,256); ctx.moveTo(hx+74,236); ctx.lineTo(hx+74,256); ctx.stroke();
      ctx.fillStyle='#6d4c41'; ctx.fillRect(hx+6,256,24,5); ctx.fillRect(hx+62,256,24,5);
      ctx.fillStyle='#ff5252'; for(let f=0;f<4;f++){ ctx.beginPath(); ctx.arc(hx+10+f*6,255,2.2,0,7); ctx.arc(hx+66+f*6,255,2.2,0,7); ctx.fill(); }
    } else if(t===1){
      ctx.fillStyle='#a8322a'; ctx.fillRect(hx,212,104,84);
      ctx.fillStyle='#5d2a22'; ctx.beginPath(); ctx.moveTo(hx-8,214); ctx.lineTo(hx+20,176); ctx.lineTo(hx+84,176); ctx.lineTo(hx+112,214); ctx.fill();
      ctx.fillStyle='#f5efe6'; ctx.fillRect(hx+30,240,44,56); ctx.fillRect(hx+44,190,16,16);
      ctx.strokeStyle='#a8322a'; ctx.lineWidth=3; ctx.strokeRect(hx+30,240,44,56);
      ctx.beginPath(); ctx.moveTo(hx+30,240); ctx.lineTo(hx+74,296); ctx.moveTo(hx+74,240); ctx.lineTo(hx+30,296); ctx.stroke();
    } else {
      ctx.fillStyle='#b9a98f'; ctx.fillRect(hx,232,76,64);
      ctx.fillStyle='#c9a548'; ctx.beginPath(); ctx.moveTo(hx-12,238); ctx.quadraticCurveTo(hx+38,150,hx+88,238); ctx.fill();
      ctx.fillStyle='#4e342e'; ctx.fillRect(hx+28,258,20,38);
      ctx.fillStyle='#ffe28a'; ctx.beginPath(); ctx.arc(hx+14,252,7,0,7); ctx.arc(hx+62,252,7,0,7); ctx.fill();
      ctx.fillStyle='#8a8372'; for(let r=0;r<3;r++) for(let c=0;c<5;c++) ctx.fillRect(hx+3+c*14+(r%2)*6,272+r*8,10,4);
    }
  });
  tiles(.6,210,(x,k)=>{
    const tx=x+100+rnd(k,3)*40;
    if(rnd(k,4)>.4){
      if(rnd(k,5)>.5){ ctx.fillStyle='#5d4037'; ctx.fillRect(tx-4,248,8,48); ctx.fillStyle='#3e7d2a'; ctx.beginPath(); ctx.arc(tx,240,24,0,7); ctx.arc(tx-18,252,16,0,7); ctx.arc(tx+18,252,16,0,7); ctx.fill(); ctx.fillStyle='#5fa83a'; ctx.beginPath(); ctx.arc(tx-6,232,13,0,7); ctx.fill(); }
      else { ctx.fillStyle='#2e6b3a'; for(let i=0;i<3;i++){ ctx.beginPath(); ctx.moveTo(tx-20+i*3,272-i*20); ctx.lineTo(tx,236-i*20); ctx.lineTo(tx+20-i*3,272-i*20); ctx.fill(); } ctx.fillStyle='#5d4037'; ctx.fillRect(tx-3,272,6,24); }
    }
  });
  tiles(.75,300,(x,k)=>{
    if(rnd(k,6)>.5){
      const hx=x+200; ctx.fillStyle='#d9a93a'; ctx.beginPath(); ctx.moveTo(hx-24,296); ctx.quadraticCurveTo(hx-22,262,hx,258); ctx.quadraticCurveTo(hx+22,262,hx+24,296); ctx.fill();
      ctx.strokeStyle='#b8862a'; ctx.lineWidth=1.5; for(let l=0;l<4;l++){ ctx.beginPath(); ctx.moveTo(hx-18+l*10,292); ctx.lineTo(hx-14+l*9,268); ctx.stroke(); }
    } else if(rnd(k,7)>.6){
      const sx=x+150; ctx.strokeStyle='#6d4c41'; ctx.lineWidth=4; ctx.beginPath(); ctx.moveTo(sx,296); ctx.lineTo(sx,250); ctx.moveTo(sx-20,262); ctx.lineTo(sx+20,262); ctx.stroke();
      ctx.fillStyle='#e8c07a'; ctx.beginPath(); ctx.arc(sx,244,8,0,7); ctx.fill(); ctx.fillStyle='#8a6a44'; ctx.fillRect(sx-12,234,24,4); ctx.fillRect(sx-7,226,14,9);
    }
  });
  let gg=ctx.createLinearGradient(0,296,0,330); gg.addColorStop(0,'#7cc243'); gg.addColorStop(1,'#4f8f2a'); ctx.fillStyle=gg; ctx.fillRect(0,296,800,34);
  ctx.strokeStyle='#3f7a22'; ctx.lineWidth=2;
  tiles(1,18,(x,k)=>{ const y=310+rnd(k,9)*16, h=4+rnd(k,8)*6; ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x+2,y-h); ctx.stroke(); });
  tiles(.95,44,(x,k)=>{
    if(rnd(k,14)>.55){ const c=['#ff5252','#ffd740','#ffffff','#ff80ab'][Math.floor(rnd(k,15)*4)], y=304+rnd(k,16)*20;
      ctx.fillStyle='#3f7a22'; ctx.fillRect(x,y,2,8); ctx.fillStyle=c; ctx.beginPath(); ctx.arc(x+1,y,3.5,0,7); ctx.fill(); }
  });
  tiles(1,40,(x,k)=>{ ctx.fillStyle='#8d6e4a'; ctx.fillRect(x,276,6,22); });
  ctx.fillStyle='#a58660'; ctx.fillRect(0,282,800,4); ctx.fillRect(0,291,800,4);
  birds('#4a3a5a');
}
 
function drawBackground(){
  ctx.clearRect(0,0,800,450); ctx.save();
  if(shakeDuration>0){ shakeDuration--; ctx.translate((Math.random()-.5)*10,(Math.random()-.5)*10); }
  if(currentMap==='BEACH') drawBeachMap(); else if(currentMap==='CITY') drawCityMap(); else drawVillageMap();
 
  drawGround();
  pits.forEach(p => {
    ctx.fillStyle='#0a0a0a'; ctx.fillRect(p.x,defaultGroundY,p.width,450-defaultGroundY);
    ctx.fillStyle='#111'; ctx.fillRect(p.x-6,defaultGroundY,6,450-defaultGroundY); ctx.fillRect(p.x+p.width,defaultGroundY,6,450-defaultGroundY);
  });
 
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
 
// ================= ĐỒ HỌA MỚI =================
function drawGround(){
  const G=defaultGroundY, city=currentMap==='CITY';
  const lip = city?'#9a9db8':(currentMap==='BEACH'?'#d9b377':'#7cb342');
  const road = city?'#2e2b4b':(currentMap==='BEACH'?'#4a4a55':'#8a6a45');
  ctx.fillStyle=road; ctx.fillRect(0,G,800,62);
  ctx.fillStyle=lip; ctx.fillRect(0,G,800,13);
  ctx.fillStyle='rgba(255,255,255,.28)'; ctx.fillRect(0,G,800,3);
  ctx.fillStyle='rgba(0,0,0,.35)'; ctx.fillRect(0,G+13,800,3);
  ctx.strokeStyle='rgba(0,0,0,.35)'; ctx.lineWidth=2;
  for(let i=0;i<5;i++){ const x=((i*173-bgOffset)%900+900)%900-50; ctx.beginPath(); ctx.moveTo(x,G+20); ctx.lineTo(x+10,G+30); ctx.lineTo(x+4,G+38); ctx.lineTo(x+16,G+52); ctx.stroke(); }
  ctx.fillStyle=currentMap==='VILLAGE'?'#b89464':'#e8e8f0'; for(let x=-(bgOffset%90); x<800; x+=90) ctx.fillRect(x,G+36,48,4);
  ctx.fillStyle='#5a3b2a'; ctx.fillRect(0,G+62,800,450);
  ctx.fillStyle='#6b4733';
  for(let i=0;i<14;i++){ const x=((i*97-bgOffset*.9)%900+900)%900-50; ctx.beginPath(); ctx.ellipse(x,G+72+(i*37)%40,14+(i%3)*5,8,0,0,7); ctx.fill(); }
  ctx.fillStyle='rgba(0,0,0,.25)'; ctx.fillRect(0,G+62,800,4);
}
 
function outText(t,x,y,size,fill,align){
  ctx.font='900 '+size+'px "Arial Black",sans-serif'; ctx.textAlign=align||'left';
  ctx.lineWidth=5; ctx.lineJoin='round'; ctx.strokeStyle='#3a1500'; ctx.strokeText(t,x,y);
  ctx.fillStyle=fill; ctx.fillText(t,x,y);
}
 
function drawZombie(z,scale=1,ox=0,oy=0){
  const v=(z.variant||0)%3, mummy=equippedOutfit==='MUMMY';
  const skin=mummy?'#d8ccb4':'#8cc63f', skinD=mummy?'#b9ab90':'#5f9a25', skinL=mummy?'#efe6d2':'#b7e35a';
  const iris=['#7b3fd1','#2f8fe0','#ff8a1f'][v], shirt=['#3c5a9a','#8e3b7e','#c9a45a'][v], pant=['#4b5873','#5b4636','#6b6f3a'][v];
  const s=Math.sin(z.legAngle), air=!z.isGrounded, bob=air?0:Math.abs(s)*2;
  ctx.save(); ctx.translate(z.x+ox,z.y+19+oy); ctx.scale(scale*1.2,scale*1.2);
  ctx.fillStyle='rgba(0,0,0,.3)'; ctx.beginPath(); ctx.ellipse(0,1,15,4,0,0,7); ctx.fill();
  const leg=(p,col)=>{
    const fx=air?p*7:p*10, fy=air?-5:-2-Math.max(0,p)*5;
    ctx.strokeStyle=col; ctx.lineWidth=6; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(0,-14); ctx.lineTo(fx,fy); ctx.stroke();
    ctx.fillStyle=mummy?skinD:'#4a3a2a'; ctx.beginPath(); ctx.ellipse(fx+3,fy+1,5,3,0,0,7); ctx.fill();
  };
  leg(-s,skinD); leg(s,skin);
  ctx.fillStyle=mummy?'#e6dcc6':pant; ctx.fillRect(-8,-21,16,9);
  ctx.fillStyle=mummy?'#efe6d2':shirt; ctx.beginPath(); ctx.moveTo(-9,-33); ctx.quadraticCurveTo(0,-37,9,-33); ctx.lineTo(10,-19); ctx.lineTo(6,-17); ctx.lineTo(3,-20); ctx.lineTo(-1,-16); ctx.lineTo(-5,-19); ctx.lineTo(-10,-17); ctx.closePath(); ctx.fill();
  const arm=(ay,ph,col)=>{
    const hy=ay+3+ph*2; ctx.strokeStyle=col; ctx.lineWidth=5; ctx.lineCap='round';
    ctx.beginPath(); ctx.moveTo(3,ay); ctx.lineTo(19,hy); ctx.stroke(); ctx.fillStyle=col; ctx.beginPath(); ctx.arc(20,hy,3.5,0,7); ctx.fill();
  };
  arm(-29,-s,skinD); arm(-26,s,skin);
  ctx.save(); ctx.translate(3,-44-bob); ctx.rotate(.1);
  ctx.fillStyle=mummy?skinD:'#7a9a8a'; ctx.beginPath(); ctx.ellipse(-14,2,6,8,0,0,7); ctx.fill();
  let hg=ctx.createRadialGradient(-4,-8,3,0,0,22); hg.addColorStop(0,skinL); hg.addColorStop(1,skin);
  ctx.fillStyle=hg; ctx.strokeStyle=skinD; ctx.lineWidth=1.5; ctx.beginPath(); ctx.ellipse(0,0,19,17,0,0,7); ctx.fill(); ctx.stroke();
  ctx.fillStyle=skin; ctx.beginPath(); ctx.ellipse(10,9,10,7,0,0,7); ctx.fill();
  if(mummy){ ctx.strokeStyle='rgba(120,100,70,.7)'; ctx.lineWidth=2; for(let i=-2;i<3;i++){ ctx.beginPath(); ctx.moveTo(-16,i*6+2); ctx.lineTo(16,i*6-4); ctx.stroke(); } }
  ctx.fillStyle='#fff'; ctx.strokeStyle=skinD; ctx.lineWidth=1.5; ctx.beginPath(); ctx.arc(7,-3,10.5,0,7); ctx.fill(); ctx.stroke();
  ctx.fillStyle=mummy?'#e53935':iris; ctx.beginPath(); ctx.arc(9.5,-2.5,6.2,0,7); ctx.fill();
  ctx.fillStyle='#000'; ctx.beginPath(); ctx.arc(10.5,-2.5,3,0,7); ctx.fill();
  ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(8.5,-5,1.8,0,7); ctx.fill();
  ctx.strokeStyle=skinD; ctx.lineWidth=3.5; ctx.beginPath(); ctx.moveTo(-3,-12); ctx.lineTo(16,-8); ctx.stroke();
  const near=humans.some(h=>h.x-z.x>0&&h.x-z.x<110);
  if(near){
    ctx.fillStyle='#3a0d12'; ctx.beginPath(); ctx.ellipse(12,10,9,7,0,0,7); ctx.fill();
    ctx.fillStyle='#e88'; ctx.beginPath(); ctx.ellipse(12,13,5,3,0,0,7); ctx.fill();
    ctx.fillStyle='#fff'; ctx.beginPath(); ctx.moveTo(5,5); ctx.lineTo(8,11); ctx.lineTo(11,5); ctx.moveTo(13,5); ctx.lineTo(16,11); ctx.lineTo(19,5); ctx.fill();
  } else {
    ctx.strokeStyle='#2c5a14'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(4,11); ctx.quadraticCurveTo(12,15,19,9); ctx.stroke();
    ctx.fillStyle='#fff'; ctx.beginPath(); ctx.moveTo(8,12); ctx.lineTo(10,16); ctx.lineTo(12,12); ctx.moveTo(14,12); ctx.lineTo(16,15.5); ctx.lineTo(18,11); ctx.fill();
  }
  ctx.restore();
  const hy=-44-bob-15;
  if(equippedHat==='HAT'){
    ctx.fillStyle='#6d4c2f'; ctx.beginPath(); ctx.ellipse(3,hy+4,24,5,0,0,7); ctx.fill();
    ctx.fillStyle='#8d6238'; ctx.beginPath(); ctx.moveTo(-7,hy+3); ctx.quadraticCurveTo(-5,hy-14,3,hy-12); ctx.quadraticCurveTo(11,hy-14,13,hy+3); ctx.fill();
    ctx.fillStyle='#c62828'; ctx.fillRect(-7,hy-2,20,3);
  } else if(equippedHat==='PUMPKIN'){
    ctx.fillStyle='#ff7a00'; ctx.beginPath(); ctx.ellipse(3,hy-2,17,13,0,0,7); ctx.fill();
    ctx.strokeStyle='#c45500'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.ellipse(3,hy-2,8,13,0,0,7); ctx.stroke();
    ctx.fillStyle='#2e6b1a'; ctx.fillRect(1,hy-18,4,7);
  }
  ctx.restore();
}
 
function drawHuman(h){
  const m=h.gender==='MALE', cop=h.cop, pan=h.panic, st=h.step||0;
  ctx.save(); ctx.translate(h.x,h.y+20); ctx.scale(-1.15,1.15);
  ctx.fillStyle='rgba(0,0,0,.25)'; ctx.beginPath(); ctx.ellipse(0,1,10,3,0,0,7); ctx.fill();
  const sw=pan?Math.sin(st)*6:0;
  ctx.strokeStyle=cop?'#1c2f5e':(m?'#2b3a8c':'#6a1b4d'); ctx.lineWidth=5; ctx.lineCap='round';
  ctx.beginPath(); ctx.moveTo(-2,-12); ctx.lineTo(-2+sw,0); ctx.moveTo(2,-12); ctx.lineTo(2-sw,0); ctx.stroke();
  ctx.fillStyle=cop?'#2a4a8a':(m?'#e0562b':'#f06292'); ctx.fillRect(-6,-27,12,16);
  ctx.strokeStyle='#f2bf94'; ctx.lineWidth=4;
  if(cop){
    ctx.fillStyle='#ffd54f'; ctx.fillRect(-4,-24,3,3);
    ctx.beginPath(); ctx.moveTo(3,-23); ctx.lineTo(14,-22); ctx.stroke();
    ctx.fillStyle='#222'; ctx.fillRect(12,-25,11,4);
    if(h.flash>0){ ctx.fillStyle='#ffeb3b'; ctx.beginPath(); ctx.arc(26,-23,5,0,7); ctx.fill(); }
  } else {
    const up=pan?-10-Math.abs(Math.sin(st))*4:-4;
    ctx.beginPath(); ctx.moveTo(-5,-24); ctx.lineTo(-10,-24+up); ctx.moveTo(5,-24); ctx.lineTo(10,-24+up); ctx.stroke();
  }
  ctx.fillStyle='#f2bf94'; ctx.beginPath(); ctx.arc(0,-34,9,0,7); ctx.fill();
  if(cop){ ctx.fillStyle='#1c2f5e'; ctx.fillRect(-9,-45,18,6); ctx.fillRect(0,-40,12,2.5); }
  else { ctx.fillStyle=m?'#5d4037':'#e6b422'; ctx.beginPath(); ctx.arc(0,-36,9.5,Math.PI,0); ctx.fill(); }
  ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(2,-35,2.8,0,7); ctx.arc(6.5,-35,2.8,0,7); ctx.fill();
  ctx.fillStyle='#000'; ctx.beginPath(); ctx.arc(3,-35,1.2,0,7); ctx.arc(7.5,-35,1.2,0,7); ctx.fill();
  ctx.fillStyle='#600'; ctx.beginPath(); ctx.ellipse(4.5,-29.5,pan?2.5:2,pan?3.5:1.2,0,0,7); ctx.fill();
  ctx.restore();
  if(pan && !cop){ ctx.fillStyle='#ff1744'; ctx.font='bold 18px sans-serif'; ctx.textAlign='center'; ctx.fillText('!',h.x,h.y-30+Math.sin(st)*2); }
}
 
function miniHead(x,y,sc,f){
  ctx.save(); ctx.translate(x,y); ctx.scale(f*sc,sc);
  ctx.fillStyle='#8cc63f'; ctx.beginPath(); ctx.ellipse(0,0,15,13,0,0,7); ctx.fill();
  ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(5,-2,8,0,7); ctx.fill();
  ctx.fillStyle='#7b3fd1'; ctx.beginPath(); ctx.arc(7,-2,4.5,0,7); ctx.fill();
  ctx.fillStyle='#000'; ctx.beginPath(); ctx.arc(8,-2,2,0,7); ctx.fill();
  ctx.fillStyle='#fff'; ctx.beginPath(); ctx.moveTo(4,8); ctx.lineTo(7,14); ctx.lineTo(10,8); ctx.fill();
  ctx.restore();
}
function drawBadge(x,y,req){
  const ok=zombies.length>=req;
  miniHead(x-6,y+8,.9,1); miniHead(x+102,y+10,.9,-1);
  ctx.fillStyle='#0c0c10'; ctx.beginPath(); ctx.roundRect(x,y,96,48,14); ctx.fill();
  ctx.beginPath(); ctx.moveTo(x+14,y+46); ctx.lineTo(x+22,y+62); ctx.lineTo(x+36,y+46); ctx.fill();
  outText(String(zombies.length),x+38,y+37,30,ok?'#8bff3a':'#ff6a00','right');
  outText('/'+req,x+42,y+40,22,'#ffb000','left');
}
 
function drawCar(o){
  ctx.save(); ctx.translate(o.x,o.y);
  ctx.fillStyle='rgba(0,0,0,.28)'; ctx.beginPath(); ctx.ellipse(50,49,52,5,0,0,7); ctx.fill();
  let bg=ctx.createLinearGradient(0,0,0,42); bg.addColorStop(0,'#b5cde0'); bg.addColorStop(.5,'#8fb0c9'); bg.addColorStop(1,'#6a8ba6');
  ctx.fillStyle=bg; ctx.strokeStyle='#3d566b'; ctx.lineWidth=2;
  ctx.beginPath(); ctx.moveTo(10,22); ctx.bezierCurveTo(12,-2,26,-6,44,-6); ctx.bezierCurveTo(66,-6,80,0,90,22); ctx.closePath(); ctx.fill(); ctx.stroke();
  ctx.beginPath(); ctx.roundRect(0,14,100,28,12); ctx.fill(); ctx.stroke();
  ctx.fillStyle='#22364a';
  ctx.beginPath(); ctx.moveTo(16,20); ctx.bezierCurveTo(18,3,30,0,42,0); ctx.lineTo(42,20); ctx.closePath(); ctx.fill();
  ctx.beginPath(); ctx.moveTo(48,20); ctx.lineTo(48,0); ctx.bezierCurveTo(64,0,76,5,82,20); ctx.closePath(); ctx.fill();
  // người hét trong cửa sổ
  ctx.strokeStyle='#e9a07a'; ctx.lineWidth=3; ctx.lineCap='round';
  ctx.beginPath(); ctx.moveTo(24,18); ctx.lineTo(8,2); ctx.moveTo(38,18); ctx.lineTo(50,-8); ctx.stroke();
  ctx.fillStyle='#e9a07a'; ctx.beginPath(); ctx.arc(30,10,9,0,7); ctx.fill();
  ctx.fillStyle='#e57373'; ctx.beginPath(); ctx.arc(24,11,3,0,7); ctx.fill();
  ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(27,6,3.2,0,7); ctx.arc(34,6,3.2,0,7); ctx.fill();
  ctx.fillStyle='#000'; ctx.beginPath(); ctx.arc(26,6,1.3,0,7); ctx.arc(33,6,1.3,0,7); ctx.fill();
  ctx.fillStyle='#600'; ctx.beginPath(); ctx.ellipse(31,15,3.5,4.5,0,0,7); ctx.fill();
  ctx.fillStyle='#fff3a0'; ctx.beginPath(); ctx.arc(4,28,4,0,7); ctx.fill();
  ctx.fillStyle='#e53935'; ctx.beginPath(); ctx.arc(96,28,3,0,7); ctx.fill();
  ctx.fillStyle='#9aa7b3'; ctx.fillRect(0,36,100,4);
  [24,76].forEach(x=>{ ctx.fillStyle='#16161c'; ctx.beginPath(); ctx.arc(x,38,10,0,7); ctx.fill(); ctx.fillStyle='#c9ced6'; ctx.beginPath(); ctx.arc(x,38,4.5,0,7); ctx.fill(); });
  drawBadge(2,-70,o.reqZombies); ctx.restore();
}
 
function drawBus(o){
  ctx.save(); ctx.translate(o.x,o.y);
  ctx.fillStyle='rgba(0,0,0,.28)'; ctx.beginPath(); ctx.ellipse(80,63,84,5,0,0,7); ctx.fill();
  let bg=ctx.createLinearGradient(0,0,0,46); bg.addColorStop(0,'#ffe082'); bg.addColorStop(1,'#f9a825');
  ctx.fillStyle=bg; ctx.strokeStyle='#7a5200'; ctx.lineWidth=2; ctx.beginPath(); ctx.roundRect(0,0,160,46,10); ctx.fill(); ctx.stroke();
  ctx.fillStyle='#3b2b00'; ctx.fillRect(0,31,160,4);
  for(let k=0;k<5;k++){
    const wx=10+k*29; ctx.fillStyle='#2a4157'; ctx.beginPath(); ctx.roundRect(wx,6,22,19,4); ctx.fill();
    ctx.fillStyle='#e9a07a'; ctx.beginPath(); ctx.arc(wx+11,16,6,0,7); ctx.fill();
    ctx.fillStyle='#fff'; ctx.fillRect(wx+6,13,3,3); ctx.fillRect(wx+12,13,3,3);
    ctx.fillStyle='#600'; ctx.beginPath(); ctx.ellipse(wx+11,20,2,2.5,0,0,7); ctx.fill();
  }
  ctx.fillStyle='#fff3a0'; ctx.beginPath(); ctx.arc(3,38,3.5,0,7); ctx.fill();
  [32,128].forEach(x=>{ ctx.fillStyle='#16161c'; ctx.beginPath(); ctx.arc(x,52,10,0,7); ctx.fill(); ctx.fillStyle='#c9ced6'; ctx.beginPath(); ctx.arc(x,52,4.5,0,7); ctx.fill(); });
  drawBadge(32,-76,o.reqZombies); ctx.restore();
}
 
function drawHelicopter(o){
  ctx.save(); ctx.translate(o.x,o.y);
  ctx.fillStyle='#fff'; ctx.strokeStyle='#90a4ae'; ctx.lineWidth=2;
  ctx.beginPath(); ctx.moveTo(0,36); ctx.bezierCurveTo(-5,-14,60,-28,170,-18); ctx.lineTo(210,36); ctx.lineTo(0,36); ctx.fill(); ctx.stroke();
  ctx.fillStyle='#76ba1b'; ctx.fillRect(50,6,145,14);
  ctx.fillStyle='#263238'; ctx.beginPath(); ctx.arc(26,14,11,0,7); ctx.fill();
  ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(24,12,3.5,0,7); ctx.fill();
  for(let i=0;i<6;i++){
    const wx=64+i*20; ctx.fillStyle='#263238'; ctx.fillRect(wx,9,14,13);
    ctx.fillStyle='#f2bf94'; ctx.beginPath(); ctx.arc(wx+7,17,4.5,0,7); ctx.fill();
    ctx.fillStyle='#600'; ctx.beginPath(); ctx.arc(wx+7,19,1.6,0,7); ctx.fill();
  }
  ctx.fillStyle='#2e7d32'; ctx.font='900 15px sans-serif'; ctx.textAlign='left'; ctx.fillText('Z.AIRLINE',75,-2);
  const rw=30+Math.abs(Math.sin(frame*.8))*85;
  ctx.strokeStyle='#37474f'; ctx.lineWidth=5; ctx.beginPath(); ctx.moveTo(105,-24); ctx.lineTo(105,-30); ctx.stroke();
  ctx.strokeStyle='rgba(55,71,79,.8)'; ctx.lineWidth=4; ctx.beginPath(); ctx.moveTo(105-rw,-30); ctx.lineTo(105+rw,-30); ctx.stroke();
  ctx.strokeStyle='#546e7a'; ctx.lineWidth=4; ctx.beginPath(); ctx.moveTo(40,58); ctx.lineTo(180,58); ctx.moveTo(70,36); ctx.lineTo(70,58); ctx.moveTo(150,36); ctx.lineTo(150,58); ctx.stroke();
  drawBadge(57,-100,o.reqZombies); ctx.restore();
}
 
function drawWall(o){
  ctx.save(); ctx.translate(o.x,o.y);
  ctx.fillStyle='#b5523b'; ctx.fillRect(0,0,o.w,o.h); ctx.strokeStyle='#5d2a1c'; ctx.lineWidth=2;
  for(let y=0;y<o.h;y+=12){ ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(o.w,y); ctx.stroke();
    for(let x=((y/12)%2?9:18);x<o.w;x+=18){ ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x,y+12); ctx.stroke(); } }
  ctx.strokeRect(0,0,o.w,o.h); drawBadge(o.w/2-48,-70,o.reqZombies); ctx.restore();
}
function drawSpike(o){
  ctx.save(); ctx.translate(o.x,o.y); ctx.fillStyle='#4a4a55'; ctx.fillRect(0,18,o.w,4);
  for(let i=0;i<5;i++){ const x=i*13; let g=ctx.createLinearGradient(x,0,x+13,0); g.addColorStop(0,'#e0e6ec'); g.addColorStop(1,'#8a949e');
    ctx.fillStyle=g; ctx.beginPath(); ctx.moveTo(x,20); ctx.lineTo(x+6.5,0); ctx.lineTo(x+13,20); ctx.fill(); }
  ctx.restore();
}
function drawSpring(o){
  ctx.save(); ctx.translate(o.x,o.y); const top=2+(o.comp||0)*.7;
  ctx.fillStyle='#37474f'; ctx.fillRect(2,12,40,4);
  ctx.strokeStyle='#cfd8dc'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(8,12);
  for(let i=1;i<=5;i++) ctx.lineTo(i%2?36:8,12-(12-top-5)*i/5);
  ctx.stroke(); ctx.fillStyle='#e53935'; ctx.fillRect(0,top,44,5); ctx.restore();
}
function drawBullet(b){ ctx.fillStyle='#ffe082'; ctx.fillRect(b.x-8,b.y-2,14,4); ctx.fillStyle='#fff'; ctx.fillRect(b.x-8,b.y-1,6,2); }
 
function drawHUD(){
  ctx.fillStyle='rgba(0,0,0,.6)'; ctx.beginPath(); ctx.roundRect(0,0,150,84,[0,0,16,0]); ctx.fill();
  ctx.fillStyle='#caa020'; ctx.beginPath(); ctx.arc(26,24,15,0,7); ctx.fill();
  ctx.fillStyle='#ffe05a'; ctx.beginPath(); ctx.arc(26,24,11.5,0,7); ctx.fill();
  ctx.fillStyle='#b8860b'; ctx.font='900 15px Arial'; ctx.textAlign='center'; ctx.fillText('Z',26,30);
  outText(String(currentCoins),52,34,26,'#ff9100');
  ctx.fillStyle='#5a8f3a'; ctx.beginPath(); ctx.ellipse(26,60,17,12,0,0,7); ctx.fill();
  ctx.fillStyle='#8bc34a'; ctx.beginPath(); ctx.arc(18,57,7,0,7); ctx.arc(30,57,8,0,7); ctx.arc(24,65,7,0,7); ctx.fill();
  ctx.strokeStyle='#3d6b24'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(26,50); ctx.quadraticCurveTo(22,58,27,68); ctx.stroke();
  outText(String(zombies.length),52,70,26,'#ff9100');
  ctx.fillStyle='rgba(0,0,0,.55)'; ctx.fillRect(0,88,150,22);
  ctx.font='bold 13px sans-serif'; ctx.fillStyle='#fff'; ctx.textAlign='left'; ctx.fillText('📏 '+Math.floor(distance)+' m   🧟 '+score,8,104);
  let mapName='🌊 Bãi Biển'; if(currentMap==='CITY') mapName='🌆 Thành Phố'; else if(currentMap==='VILLAGE') mapName='🌾 Làng Quê';
  ctx.fillStyle='rgba(0,0,0,.55)'; ctx.beginPath(); ctx.roundRect(585,10,150,28,8); ctx.fill();
  ctx.fillStyle='#80d8ff'; ctx.font='bold 14px sans-serif'; ctx.textAlign='center'; ctx.fillText(mapName,660,29);
  ctx.fillStyle='rgba(0,0,0,.75)'; ctx.beginPath(); ctx.roundRect(752,0,48,48,[0,0,0,14]); ctx.fill();
  ctx.fillStyle='#fff'; ctx.fillRect(767,12,7,24); ctx.fillRect(780,12,7,24);
  if(!tutorialDone){
    const t=obstacles.find(o=>o.tut);
    if(t && t.x<760){
      const x=150,y=394,w=500,h=52;
      let gg=ctx.createLinearGradient(0,y,0,y+h); gg.addColorStop(0,'#b5e04a'); gg.addColorStop(1,'#78b021');
      ctx.fillStyle='#2f5a10'; ctx.beginPath(); ctx.roundRect(x-4,y-4,w+8,h+8,16); ctx.fill();
      ctx.fillStyle=gg; ctx.beginPath(); ctx.roundRect(x,y,w,h,13); ctx.fill();
      ctx.fillStyle='#9bd33a'; for(let i=0;i<8;i++){ ctx.beginPath(); ctx.arc(x+30+i*62,y-2,8,0,Math.PI); ctx.fill(); }
      ctx.fillStyle='#1a2a05'; ctx.font='900 15px "Arial Black",sans-serif'; ctx.textAlign='center';
      ctx.fillText('Look at the counter. Run with '+t.reqZombies+' zombies into',400,y+22);
      ctx.fillText('the car to flip it over',400,y+42);
    }
  }
  let bx=300; const full=bonusDur();
  [['🧲','#ff5252',buffs.magnet],['🛡️','#40c4ff',buffs.shield],['💰x2','#ffd740',buffs.double]].forEach(([ic,col,t])=>{
    if(t>0){ ctx.font='15px sans-serif'; ctx.textAlign='left'; ctx.fillStyle='#fff'; ctx.fillText(ic,bx,56);
      ctx.fillStyle='rgba(0,0,0,.55)'; ctx.fillRect(bx+34,46,60,9); ctx.fillStyle=col; ctx.fillRect(bx+35,47,58*Math.min(1,t/full),7); bx+=110; }
  });
  if(banner.life>0){ banner.life--; ctx.globalAlpha=Math.min(1,banner.life/20); outText(banner.t,400,140-(80-banner.life)*.3,34,'#ffffff','center'); ctx.globalAlpha=1; }
  if(paused){
    ctx.fillStyle='rgba(0,0,0,.6)'; ctx.fillRect(0,0,800,450);
    outText('PAUSED',400,215,54,'#76ba1b','center');
    outText('Nhấn P / chạm để tiếp tục',400,255,18,'#fff','center');
  }
}
 
function draw(){
  drawBackground();
  if(gameState==='MENU'){
    drawZombie({x:220,y:defaultGroundY-20,legAngle:frame*.2,variant:0,isGrounded:true},1.4);
    ctx.restore(); return;
  }
  coinTrails.forEach(drawCoin); powerups.forEach(drawMysteryBox); humans.forEach(drawHuman);
  const D={BOMB:drawBomb,CAR:drawCar,BUS:drawBus,HELI:drawHelicopter,SPIKE:drawSpike,SPRING:drawSpring,WALL:drawWall};
  obstacles.forEach(o => D[o.type](o));
  bullets.forEach(drawBullet);
  if(giantActive) drawGiantMonster();
  else zombies.forEach((z,idx) => {
    drawZombie(z, 1-Math.min(idx*.012,.25), (idx%3===2)?-6:0, (idx%2===1)?-Math.min(idx*1.8,18):0);
  });
  if(buffs.shield>0 && zombies[0] && !(buffs.shield<90 && Math.floor(frame/6)%2)){
    const cx=zombies[0].x-Math.min(zombies.length*4,60), rx=50+Math.min(zombies.length*5,110);
    ctx.fillStyle='rgba(80,200,255,.15)'; ctx.strokeStyle='rgba(120,220,255,.85)'; ctx.lineWidth=3;
    ctx.beginPath(); ctx.ellipse(cx,defaultGroundY-32,rx,62,0,0,7); ctx.fill(); ctx.stroke();
  }
  if(buffs.magnet>0 && zombies[0]){
    ctx.strokeStyle='rgba(255,82,82,.5)'; ctx.lineWidth=2;
    for(let r=0;r<3;r++){ ctx.beginPath(); ctx.arc(zombies[0].x+10,zombies[0].y-20,((frame*3+r*60)%180)+10,-1,1); ctx.stroke(); }
  }
  particles.forEach(p => { ctx.fillStyle=p.color; ctx.fillRect(p.x,p.y,4,4); });
  ctx.restore();
 
  drawHUD();
 
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
 
html_doc = game_code.strip()
try:
    # Streamlit mới (>= 1.56): components.html đã bị deprecated -> dùng st.iframe
    st.iframe(html_doc, height=480)
except Exception:
    # Streamlit cũ: dùng components.html
    import streamlit.components.v1 as components
    components.html(html_doc, height=480, scrolling=False)
