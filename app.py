
import streamlit as st
import base64, os
 
st.set_page_config(page_title="Zombie Tsunami Perfect Edition", layout="centered")
st.markdown("<h1 style='text-align: center; color: #76ba1b;'>🧟 ZOMBIE TSUNAMI - PERFECT EDITION ⚡</h1>", unsafe_allow_html=True)
 
# ================= NHẠC NỀN =================
# Cách 1: đặt file nhạc (mp3/ogg/wav/m4a) cùng thư mục với file .py này
#         (hoặc trong thư mục con music/ assets/ static/). Game tự tìm và nhúng vào.
# Cách 2: dùng ô "Nhạc nền" bên dưới để tải file lên.
AUDIO_MIME = {".mp3": "audio/mpeg", ".ogg": "audio/ogg", ".wav": "audio/wav",
              ".m4a": "audio/mp4", ".aac": "audio/aac", ".flac": "audio/flac"}
MAX_MB = 25
 
def _find_music():
    here = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
    folders = [here, os.path.join(here, "music"), os.path.join(here, "assets"),
               os.path.join(here, "static"), os.getcwd()]
    found, seen = [], set()
    for folder in folders:
        if folder in seen or not os.path.isdir(folder):
            continue
        seen.add(folder)
        for name in sorted(os.listdir(folder)):
            if os.path.splitext(name)[1].lower() in AUDIO_MIME:
                found.append(os.path.join(folder, name))
    pref = ("zombie", "tsunami", "theme", "music", "bgm", "nhac", "song")
    found.sort(key=lambda p: (0 if any(k in os.path.basename(p).lower() for k in pref) else 1))
    return found[0] if found else None
 
@st.cache_data(show_spinner=False)
def _file_to_uri(path, mtime):
    ext = os.path.splitext(path)[1].lower()
    with open(path, "rb") as f:
        data = f.read()
    return f"data:{AUDIO_MIME.get(ext, 'audio/mpeg')};base64," + base64.b64encode(data).decode()
 
music_uri, music_label = "", "Chưa có file nhạc -> dùng nhạc tổng hợp dự phòng"
with st.expander("🎵 Nhạc nền (bấm để tải file nhạc nếu game chưa có tiếng)"):
    up = st.file_uploader("Chọn file nhạc", type=[e[1:] for e in AUDIO_MIME])
    if up is not None:
        if up.size > MAX_MB * 1024 * 1024:
            st.warning(f"File lớn hơn {MAX_MB} MB, hãy chọn file nhỏ hơn.")
        else:
            ext = os.path.splitext(up.name)[1].lower()
            music_uri = f"data:{AUDIO_MIME.get(ext, 'audio/mpeg')};base64," + base64.b64encode(up.getvalue()).decode()
            music_label = f"Đang dùng file đã tải lên: {up.name}"
    if not music_uri:
        p = _find_music()
        if p and os.path.getsize(p) <= MAX_MB * 1024 * 1024:
            music_uri = _file_to_uri(p, os.path.getmtime(p))
            music_label = f"Đang dùng file: {os.path.basename(p)}"
    st.caption(music_label + "  •  Bấm PLAY trong game để nhạc bắt đầu phát.")
 
game_code = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
*{box-sizing:border-box}
body{margin:0;padding:0;background:#0d1b2a;display:flex;justify-content:center;align-items:center;font-family:'Arial Black',sans-serif;height:100vh;overflow:hidden;user-select:none}
#gameContainer{position:relative;width:808px;height:458px;border:4px solid #76ba1b;border-radius:12px;box-shadow:0 8px 30px rgba(118,186,27,.4);overflow:hidden;background:#111}
canvas{display:block;width:800px;height:450px}
#menuOverlay{position:absolute;top:0;left:0;width:800px;height:450px;z-index:10}
.pill{position:absolute;top:12px;left:12px;background:rgba(0,0,0,.6);border:3px solid #fff;border-radius:24px;padding:3px 16px 3px 8px;color:#ffe066;font-size:20px;display:flex;gap:8px;align-items:center;text-shadow:2px 2px 0 #000}
.pill .coin{width:28px;height:28px;border-radius:50%;background:radial-gradient(#ffe97a,#d9a400);border:2px solid #b8860b;color:#9a6a00;font-size:15px;display:flex;align-items:center;justify-content:center}
.logo-container{position:absolute;top:14px;left:50%;transform:translateX(-56%) rotate(-3deg);text-align:center;pointer-events:none}
.logo-title{font-size:62px;line-height:.9;color:#a6ee3b;-webkit-text-stroke:6px #16300a;paint-order:stroke fill;text-shadow:0 7px 0 #2e5d12,0 12px 14px rgba(0,0,0,.6);letter-spacing:3px;position:relative}
.drip{position:absolute;top:56px;width:11px;background:#a6ee3b;border:3px solid #16300a;border-top:none;border-radius:0 0 9px 9px}
.logo-sub{font-size:46px;color:#ff7a1a;-webkit-text-stroke:6px #3a1200;paint-order:stroke fill;text-shadow:0 6px 0 #8a2a00;letter-spacing:8px;margin-top:-4px;transform:rotate(2deg)}
.top-right-btns{position:absolute;top:12px;right:12px;display:flex;gap:10px;z-index:20}
.btn-icon{width:44px;height:44px;background:#424242;border:3px solid #fff;border-radius:10px;color:#fff;font-size:22px;display:flex;justify-content:center;align-items:center;cursor:pointer;box-shadow:0 4px 0 #111}
.btn-icon:active{transform:translateY(2px);box-shadow:0 2px 0 #111}
.side-menu-right{position:absolute;right:16px;top:100px;display:flex;flex-direction:column;gap:14px}
.btn-side{position:relative;width:190px;height:48px;background:linear-gradient(135deg,#e91e63,#c2185b);border:3px solid #000;border-radius:10px;color:#fff;font-size:19px;display:flex;align-items:center;padding-left:12px;box-shadow:3px 5px 0 #000;cursor:pointer;transform:rotate(2deg);text-shadow:1px 1px 2px #000}
.btn-side:nth-child(2){transform:rotate(-2deg);background:linear-gradient(135deg,#f57c00,#e65100)}
.btn-side:active{transform:scale(.96)}
.btn-side span{margin-right:10px;font-size:22px}
.badge{position:absolute;right:-9px;top:-11px;background:#ff1744;color:#fff;border:2px solid #fff;border-radius:50%;width:26px;height:26px;font-size:14px;display:none;align-items:center;justify-content:center}
.btn-play{position:absolute;bottom:22px;right:20px;width:200px;height:86px;background:linear-gradient(180deg,#ffb020,#ff3d00);border:4px solid #fff;outline:4px solid #000;border-radius:16px;color:#fff;font-size:42px;font-weight:900;display:flex;justify-content:center;align-items:center;cursor:pointer;box-shadow:0 9px 0 #801300,0 14px 16px rgba(0,0,0,.5);text-shadow:3px 3px 0 #000;transform:rotate(-3deg);animation:pulse 1.4s ease-in-out infinite}
@keyframes pulse{0%,100%{transform:rotate(-3deg) scale(1)}50%{transform:rotate(-3deg) scale(1.06)}}
.btn-play:active{animation:none;transform:rotate(-3deg) translateY(6px);box-shadow:0 2px 0 #801300}
.best-score-box{position:absolute;bottom:20px;left:18px;background:rgba(0,0,0,.65);border:3px solid #fff;border-radius:12px;padding:6px 16px;color:#fff}
.best-score-title{font-size:14px;color:#ddd}
.best-score-val{font-size:26px;color:#ffeb3b}
.modal-overlay{position:absolute;top:0;left:0;width:800px;height:450px;background:rgba(0,0,0,.85);display:none;align-items:center;justify-content:center;z-index:100}
.modal-box{width:740px;height:410px;background:#1e272e;border:4px solid #fbc02d;border-radius:16px;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 0 30px rgba(251,192,45,.4)}
.modal-header{background:#fbc02d;color:#000;padding:9px 20px;display:flex;justify-content:space-between;align-items:center;font-size:21px;font-weight:bold}
.close-btn{background:#d32f2f;color:#fff;border:2px solid #fff;border-radius:50%;width:32px;height:32px;display:flex;justify-content:center;align-items:center;cursor:pointer;font-size:17px}
.market-tabs{display:flex;background:#0f171e;border-bottom:2px solid #333}
.tab-btn{flex:1;padding:9px 4px;text-align:center;color:#aaa;font-size:14px;cursor:pointer;border-right:1px solid #222;font-weight:bold}
.tab-btn.active{background:#1e272e;color:#76ba1b;border-bottom:3px solid #76ba1b}
.shop-grid{flex:1;padding:12px;overflow-y:auto;display:flex;flex-wrap:wrap;gap:12px;justify-content:center;align-content:flex-start}
.shop-item{width:152px;height:192px;background:#2f3640;border:3px solid #485460;border-radius:12px;display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:10px;position:relative}
.shop-img{font-size:38px;height:46px;display:flex;align-items:center}
.swatch{width:38px;height:38px;border-radius:50%;border:3px solid #fff}
.shop-title{color:#fff;font-size:13px;text-align:center;font-weight:bold}
.shop-desc{color:#aaa;font-size:10px;text-align:center;line-height:1.3}
.buy-btn{background:#4cd137;color:#000;border:none;padding:7px 8px;border-radius:20px;font-weight:bold;cursor:pointer;font-size:13px;box-shadow:0 4px 0 #44bd32;width:100%}
.buy-btn.equipped{background:#fbc02d;box-shadow:0 4px 0 #f57f17}
.buy-btn.maxed,.buy-btn:disabled{background:#718093;color:#ccc;box-shadow:none;cursor:not-allowed}
.mission-list{flex:1;padding:14px 18px;display:flex;flex-direction:column;gap:10px;overflow-y:auto}
.mission-card{background:#2f3640;border:3px solid #485460;border-radius:12px;display:flex;align-items:center;padding:8px 14px;gap:12px}
.mission-icon{width:44px;height:44px;background:#111;border:2px solid #fff;border-radius:10px;display:flex;justify-content:center;align-items:center;font-size:24px;flex:none}
.mission-info{flex:1;color:#fff}
.mission-title{font-size:13px;font-weight:bold;margin-bottom:5px}
.rw{color:#ffd54f}
.bar{height:9px;background:#111;border-radius:6px;overflow:hidden;border:1px solid #555}
.bar div{height:100%;background:linear-gradient(90deg,#76ba1b,#c6ff5a)}
.mission-progress{font-size:11px;color:#ffeb3b;margin-top:3px}
.collect-btn{background:#fbc02d;color:#000;border:none;padding:9px 14px;border-radius:8px;font-weight:bold;font-size:13px;cursor:pointer;box-shadow:0 4px 0 #f57f17;flex:none;min-width:96px}
.collect-btn:disabled{background:#718093;box-shadow:none;cursor:not-allowed;color:#aaa}
#toast{position:absolute;left:50%;bottom:30px;transform:translateX(-50%);background:#000c;color:#fff;border:2px solid #ffd54f;border-radius:20px;padding:8px 20px;font-size:15px;z-index:200;display:none}
</style>
</head>
<body>
<audio id="bgMusic" loop preload="auto"></audio>
<div id="gameContainer">
<canvas id="gameCanvas" width="800" height="450"></canvas>
 
<div id="menuOverlay">
  <div class="pill"><div class="coin">Z</div><span id="menuCoins">0</span></div>
  <div class="logo-container">
    <div class="logo-title">ZOMBIE<div class="drip" style="left:30px;height:16px"></div><div class="drip" style="left:140px;height:26px"></div><div class="drip" style="left:250px;height:14px"></div></div>
    <div class="logo-sub">TSUNAMI</div>
  </div>
  <div class="top-right-btns">
    <div class="btn-icon" id="musicToggleBtn" title="Bật/Tắt nhạc nền">🔊</div>
    <div class="btn-icon" id="sfxBtn" title="Bật/Tắt hiệu ứng âm thanh">🔔</div>
  </div>
  <div class="side-menu-right">
    <div class="btn-side" id="openMissionBtn"><span>🧪</span> MISSION<div class="badge" id="missionBadge">0</div></div>
    <div class="btn-side" id="openMarketBtn"><span>🪙</span> MARKET</div>
  </div>
  <div class="best-score-box"><div class="best-score-title">Best score:</div><div class="best-score-val">🧠 <span id="bestScoreText">0</span></div></div>
  <div class="btn-play" id="playBtn">PLAY</div>
</div>
 
<div id="marketModal" class="modal-overlay"><div class="modal-box">
  <div class="modal-header"><div>🛒 MARKET (Xu: 🪙 <span id="marketCoinText">0</span>)</div><div class="close-btn" id="closeMarketBtn">✖</div></div>
  <div class="market-tabs">
    <div class="tab-btn active" id="tab_outfit">TRANG PHỤC</div>
    <div class="tab-btn" id="tab_hat">PHỤ KIỆN</div>
    <div class="tab-btn" id="tab_skin">MÀU DA</div>
    <div class="tab-btn" id="tab_power">NÂNG CẤP</div>
  </div>
  <div class="shop-grid" id="shopGrid"></div>
</div></div>
 
<div id="missionModal" class="modal-overlay"><div class="modal-box">
  <div class="modal-header"><div>📜 MISSIONS</div><div class="close-btn" id="closeMissionBtn">✖</div></div>
  <div class="mission-list" id="missionList"></div>
</div></div>
<div id="toast"></div>
</div>
 
<script>
 
const MUSIC_SRC = "__MUSIC_SRC__";
// ---------- Storage an toàn (iframe có thể chặn localStorage) ----------
const store = {
  getItem(k){ try { return localStorage.getItem(k); } catch(e){ return null; } },
  setItem(k,v){ try { localStorage.setItem(k,v); } catch(e){} }
};
if(typeof CanvasRenderingContext2D!=='undefined' && !CanvasRenderingContext2D.prototype.roundRect){
  CanvasRenderingContext2D.prototype.roundRect=function(x,y,w,h,r){ r=Array.isArray(r)?(r[0]||0):(r||0);
    this.moveTo(x+r,y); this.arcTo(x+w,y,x+w,y+h,r); this.arcTo(x+w,y+h,x,y+h,r); this.arcTo(x,y+h,x,y,r); this.arcTo(x,y,x+w,y,r); this.closePath(); };
}
const $ = id => document.getElementById(id);
const canvas = $('gameCanvas'); let ctx = canvas.getContext('2d');
const menuOverlay=$('menuOverlay'), playBtn=$('playBtn'), bestScoreText=$('bestScoreText');
const bgMusic=$('bgMusic'), musicToggleBtn=$('musicToggleBtn'), sfxBtn=$('sfxBtn');
let isMuted = store.getItem('zt_muted')==='1', sfxOn = store.getItem('zt_sfx')!=='0';
musicToggleBtn.innerText = isMuted ? '🔇' : '🔊'; sfxBtn.innerText = sfxOn ? '🔔' : '🔕';
 
// ---------- Âm thanh hiệu ứng ----------
const AudioCtx = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;
function initAudio(){ try{ if(!audioCtx && AudioCtx) audioCtx = new AudioCtx(); if(audioCtx && audioCtx.state==='suspended') audioCtx.resume(); }catch(e){ audioCtx=null; } }
const SFX = {
  jump:['sine',280,580,.12,.2,'exponentialRampToValueAtTime'],
  eat:['triangle',150,350,.1,.3,'exponentialRampToValueAtTime'],
  coin:['sine',988,1318,.18,.18,'setValueAtTime'],
  powerup:['square',300,900,.25,.25,'exponentialRampToValueAtTime'],
  shot:['square',700,200,.08,.12,'exponentialRampToValueAtTime'],
  fall:['sine',500,70,.4,.25,'exponentialRampToValueAtTime'],
  slash:['sawtooth',1400,300,.12,.15,'exponentialRampToValueAtTime'],
  explode:['sawtooth',120,30,.35,.4,'linearRampToValueAtTime']
};
function playSound(type){
  if(!sfxOn) return; initAudio(); if(!audioCtx) return;
  const [wave,f1,f2,dur,vol,ramp] = SFX[type]; const now = audioCtx.currentTime;
  const osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
  osc.type = wave; osc.frequency.setValueAtTime(f1, now);
  if(ramp==='setValueAtTime') osc.frequency.setValueAtTime(f2, now+.08); else osc.frequency[ramp](f2, now+dur);
  gain.gain.setValueAtTime(vol, now); gain.gain.linearRampToValueAtTime(.01, now+dur);
  osc.connect(gain); gain.connect(audioCtx.destination); osc.start(now); osc.stop(now+dur);
}
 
// ---------- Nhạc nền: file nhạc nhúng từ Python; nếu lỗi thì dùng nhạc tổng hợp ----------
let useSynth = !MUSIC_SRC || MUSIC_SRC.indexOf('__MUSIC')===0, musicStarted=false, synthTimer=null, synthStep=0;
if(!useSynth){
  bgMusic.src = MUSIC_SRC; bgMusic.volume = .7;
  bgMusic.addEventListener('error', () => { useSynth = true; if(musicStarted && !isMuted) startSynth(); });
}
const MEL=[392,440,494,587,494,440,392,330,392,440,494,587,659,587,494,440], BASS=[98,98,110,110,123,123,110,110];
function synthNote(type,f,d,v,t){ const o=audioCtx.createOscillator(), g=audioCtx.createGain(); o.type=type; o.frequency.value=f; g.gain.setValueAtTime(v,t); g.gain.linearRampToValueAtTime(.0001,t+d); o.connect(g); g.connect(audioCtx.destination); o.start(t); o.stop(t+d); }
function startSynth(){
  if(synthTimer) return; initAudio(); if(!audioCtx) return;
  synthTimer = setInterval(() => { if(paused || isMuted) return; const now=audioCtx.currentTime;
    synthNote('square',MEL[synthStep%16],.2,.04,now); if(synthStep%2===0) synthNote('triangle',BASS[(synthStep>>1)%8],.38,.08,now); synthStep++; }, 230);
}
function stopSynth(){ if(synthTimer){ clearInterval(synthTimer); synthTimer=null; } }
function playMusic(){ if(isMuted) return; if(useSynth){ startSynth(); return; } try{ const p=bgMusic.play(); if(p && p.catch) p.catch(()=>{}); }catch(e){} }
function pauseMusic(){ stopSynth(); try{ bgMusic.pause(); }catch(e){} }
['pointerdown','keydown','touchstart'].forEach(ev => window.addEventListener(ev, () => { if(!musicStarted){ musicStarted=true; playMusic(); } }));
musicToggleBtn.addEventListener('click', e => {
  e.stopPropagation(); isMuted=!isMuted; store.setItem('zt_muted', isMuted?'1':'0');
  musicToggleBtn.innerText = isMuted?'🔇':'🔊'; if(isMuted) pauseMusic(); else playMusic();
});
sfxBtn.addEventListener('click', e => { e.stopPropagation(); sfxOn=!sfxOn; store.setItem('zt_sfx', sfxOn?'1':'0'); sfxBtn.innerText = sfxOn?'🔔':'🔕'; });
 
// ---------- Dữ liệu người chơi ----------
let gameState='MENU', score=0, distance=0;
let bestScore = parseInt(store.getItem('zt_best_score')||'0'); bestScoreText.innerText = bestScore;
let totalCoins = parseInt(store.getItem('zt_total_coins')||'0');
let totalEatenHumans = parseInt(store.getItem('zt_total_eaten')||'0');
let maxSingleRunEaten = parseInt(store.getItem('zt_max_single_eaten')||'0');
let stat = {veh:0,boxes:0,cops:0,games:0,maxDist:0,maxHorde:1,coins:0};
try{ const s=JSON.parse(store.getItem('zt_stats')||'null'); if(s) stat=Object.assign(stat,s); }catch(e){}
let claimed = {}; try{ claimed = JSON.parse(store.getItem('zt_claimed')||'{}')||{}; }catch(e){}
let equippedOutfit = store.getItem('zt_equipped_outfit')||'NONE';
let equippedHat = store.getItem('zt_equipped_hat')||'NONE';
let equippedSkin = store.getItem('zt_equipped_skin')||'NONE';
let ownedItems = []; try{ ownedItems = JSON.parse(store.getItem('zt_owned_items')||'[]'); }catch(e){}
let lv = {start:parseInt(store.getItem('zt_p1_level')||'1'),time:parseInt(store.getItem('zt_p2_level')||'1'),box:1,jump:1};
try{ const s=JSON.parse(store.getItem('zt_lv')||'null'); if(s) lv=Object.assign(lv,s); }catch(e){}
const MAP_LIST=['BEACH','CITY','VILLAGE','GRAVEYARD'];
const MAP_NAMES={BEACH:'🌊 Bãi Biển',CITY:'🌆 Thành Phố',VILLAGE:'🌾 Làng Quê',GRAVEYARD:'🎃 Nghĩa Địa'};
let currentMap = MAP_LIST[Math.floor(Math.random()*MAP_LIST.length)], mapTimer=0, shakeDuration=0;
function triggerShake(d=12){ shakeDuration=d; }
let spriteCache = {};
 
function persist(){
  store.setItem('zt_total_coins',totalCoins); store.setItem('zt_total_eaten',totalEatenHumans);
  store.setItem('zt_max_single_eaten',maxSingleRunEaten); store.setItem('zt_stats',JSON.stringify(stat));
  store.setItem('zt_claimed',JSON.stringify(claimed)); store.setItem('zt_equipped_outfit',equippedOutfit);
  store.setItem('zt_equipped_hat',equippedHat); store.setItem('zt_equipped_skin',equippedSkin);
  store.setItem('zt_owned_items',JSON.stringify(ownedItems)); store.setItem('zt_lv',JSON.stringify(lv));
}
function saveUserData(){
  persist(); $('marketCoinText').innerText=totalCoins; $('menuCoins').innerText=totalCoins; updateBadge();
  if($('marketModal').style.display==='flex') renderShop();
  if($('missionModal').style.display==='flex') renderMissions();
}
let toastT=null;
function toast(msg){ const t=$('toast'); t.innerText=msg; t.style.display='block'; clearTimeout(toastT); toastT=setTimeout(()=>{ t.style.display='none'; },1600); }
 
// ---------- Market ----------
const SHOP = {
  outfit:[
    {id:'MUMMY',name:'Xác Ướp',icon:'🩹',price:300,desc:'Bọc băng cổ đại'},
    {id:'HERO',name:'Siêu Nhân',icon:'🦸',price:400,desc:'Áo choàng đỏ oai vệ'},
    {id:'PIRATE',name:'Cướp Biển',icon:'🏴‍☠️',price:350,desc:'Áo sọc, móc câu'},
    {id:'CLOWN',name:'Chú Hề',icon:'🤡',price:300,desc:'Mũi đỏ, áo chấm bi'}
  ],
  hat:[
    {id:'HAT',name:'Mũ Cao Bồi',icon:'🤠',price:200,desc:'Phong cách miền Tây'},
    {id:'PUMPKIN',name:'Đầu Bí Ngô',icon:'🎃',price:200,desc:'Phụ kiện Halloween'},
    {id:'CROWN',name:'Vương Miện',icon:'👑',price:500,desc:'Vua của bầy zombie'},
    {id:'SANTA',name:'Mũ Ông Già Noel',icon:'🎅',price:250,desc:'Giáng sinh vui vẻ'},
    {id:'PARTY',name:'Mũ Dự Tiệc',icon:'🎉',price:150,desc:'Tiệc tùng nào!'},
    {id:'WITCH',name:'Mũ Phù Thủy',icon:'🧙',price:300,desc:'Đầy bùa phép'}
  ],
  skin:[
    {id:'ICE',name:'Zombie Băng',color:'#8fdcff',price:500,desc:'Lạnh như băng'},
    {id:'GOLD',name:'Zombie Vàng',color:'#ffd54a',price:1000,desc:'Sang chảnh lấp lánh'},
    {id:'PURPLE',name:'Zombie Tím',color:'#b57bff',price:500,desc:'Bí ẩn và độc'},
    {id:'PINK',name:'Zombie Hồng',color:'#ff8fb8',price:500,desc:'Ngọt như kẹo'},
    {id:'RED',name:'Zombie Máu',color:'#ff7a6b',price:600,desc:'Đỏ au đáng sợ'}
  ]
};
const UPG = [
  {id:'start',icon:'🧠',name:'Zombie Ban Đầu',desc:'Bắt đầu với nhiều zombie hơn',max:5,cost:50},
  {id:'time',icon:'⏱️',name:'Thời Gian Bổ Trợ',desc:'Bổ trợ kéo dài hơn',max:5,cost:50},
  {id:'box',icon:'🎁',name:'Hộp Bí Ẩn',desc:'Hộp xuất hiện thường xuyên hơn',max:3,cost:100},
  {id:'jump',icon:'🦘',name:'Nhảy Cao',desc:'Bật nhảy mạnh hơn',max:3,cost:80}
];
let shopTab='outfit';
const equippedOf = k => k==='outfit'?equippedOutfit:(k==='hat'?equippedHat:equippedSkin);
function renderShop(){
  $('marketCoinText').innerText=totalCoins;
  ['outfit','hat','skin','power'].forEach(t => $('tab_'+t).classList.toggle('active',t===shopTab));
  let h='';
  if(shopTab==='power'){
    UPG.forEach(u => { const l=lv[u.id], mx=l>=u.max;
      h+='<div class="shop-item"><div class="shop-img">'+u.icon+'</div><div class="shop-title">'+u.name+'</div><div class="shop-desc">'+u.desc+'<br>Cấp '+l+'/'+u.max+'</div><button class="buy-btn'+(mx?' maxed':'')+'" data-up="'+u.id+'"'+(mx?' disabled':'')+'>'+(mx?'TỐI ĐA':(u.cost*l)+' Xu')+'</button></div>'; });
  } else {
    SHOP[shopTab].forEach(it => { const own=ownedItems.includes(it.id), eq=equippedOf(shopTab)===it.id;
      const img = it.color ? '<div class="swatch" style="background:'+it.color+'"></div>' : it.icon;
      h+='<div class="shop-item"><div class="shop-img">'+img+'</div><div class="shop-title">'+it.name+'</div><div class="shop-desc">'+it.desc+'</div><button class="buy-btn'+(eq?' equipped':'')+'" data-item="'+it.id+'" data-kind="'+shopTab+'">'+(own?(eq?'Đang dùng ✓':'Trang bị'):it.price+' Xu')+'</button></div>'; });
  }
  $('shopGrid').innerHTML=h;
}
function setEquipped(kind,id){ if(kind==='outfit') equippedOutfit=id; else if(kind==='hat') equippedHat=id; else equippedSkin=id; spriteCache={}; }
function buyItem(id,kind){
  const it=SHOP[kind].find(x=>x.id===id); if(!it) return;
  if(!ownedItems.includes(id)){
    if(totalCoins<it.price){ toast('Bạn không đủ xu!'); return; }
    totalCoins-=it.price; ownedItems.push(id); setEquipped(kind,id); toast('Đã mua '+it.name+'!');
  } else setEquipped(kind, equippedOf(kind)===id ? 'NONE' : id);
  saveUserData();
}
function buyUpg(id){
  const u=UPG.find(x=>x.id===id), l=lv[id]; if(!u||l>=u.max) return;
  if(totalCoins<u.cost*l){ toast('Bạn không đủ xu!'); return; }
  totalCoins-=u.cost*l; lv[id]++; toast(u.name+' lên cấp '+lv[id]+'!'); saveUserData();
}
$('shopGrid').addEventListener('click', e => { const b=e.target.closest('button'); if(!b||b.disabled) return; if(b.dataset.up) buyUpg(b.dataset.up); else buyItem(b.dataset.item,b.dataset.kind); });
['outfit','hat','skin','power'].forEach(t => $('tab_'+t).addEventListener('click', () => { shopTab=t; renderShop(); }));
$('openMarketBtn').addEventListener('click', () => { renderShop(); $('marketModal').style.display='flex'; });
$('closeMarketBtn').addEventListener('click', () => { $('marketModal').style.display='none'; });
 
// ---------- Missions ----------
const MISSIONS = [
  {id:'eat100',icon:'🧟',t:'Ăn thịt tổng cộng 100 người',goal:100,reward:100,val:()=>totalEatenHumans},
  {id:'run10',icon:'🧠',t:'Ăn thịt 10 người trong 1 màn chơi',goal:10,reward:50,val:()=>maxSingleRunEaten},
  {id:'run30',icon:'🍖',t:'Ăn thịt 30 người trong 1 màn chơi',goal:30,reward:150,val:()=>maxSingleRunEaten},
  {id:'eat300',icon:'🧟',t:'Ăn thịt tổng cộng 300 người',goal:300,reward:200,val:()=>totalEatenHumans},
  {id:'dist500',icon:'🏃',t:'Chạy 500 m trong 1 màn chơi',goal:500,reward:100,val:()=>stat.maxDist},
  {id:'dist2000',icon:'🚀',t:'Chạy 2000 m trong 1 màn chơi',goal:2000,reward:300,val:()=>stat.maxDist},
  {id:'veh10',icon:'🚗',t:'Lật 10 phương tiện / vật cản',goal:10,reward:100,val:()=>stat.veh},
  {id:'veh40',icon:'🚌',t:'Lật 40 phương tiện / vật cản',goal:40,reward:300,val:()=>stat.veh},
  {id:'box5',icon:'🎁',t:'Nhặt 5 hộp bí ẩn',goal:5,reward:100,val:()=>stat.boxes},
  {id:'box20',icon:'🎁',t:'Nhặt 20 hộp bí ẩn',goal:20,reward:300,val:()=>stat.boxes},
  {id:'cop5',icon:'👮',t:'Ăn thịt 5 cảnh sát',goal:5,reward:150,val:()=>stat.cops},
  {id:'games10',icon:'🎮',t:'Chơi 10 ván',goal:10,reward:60,val:()=>stat.games},
  {id:'horde20',icon:'👥',t:'Có 20 zombie cùng lúc',goal:20,reward:200,val:()=>stat.maxHorde},
  {id:'coins1000',icon:'🪙',t:'Thu thập tổng cộng 1000 xu',goal:1000,reward:250,val:()=>stat.coins}
];
function updateBadge(){
  const n=MISSIONS.filter(m => !claimed[m.id] && m.val()>=m.goal).length, b=$('missionBadge');
  b.style.display = n ? 'flex' : 'none'; b.innerText = n;
}
function renderMissions(){
  let h='';
  MISSIONS.forEach(m => { const val=m.val(), v=Math.min(val,m.goal), done=!!claimed[m.id], can=!done && val>=m.goal;
    h+='<div class="mission-card"><div class="mission-icon">'+m.icon+'</div><div class="mission-info"><div class="mission-title">'+m.t+' <span class="rw">(+'+m.reward+' Xu)</span></div><div class="bar"><div style="width:'+(v/m.goal*100)+'%"></div></div><div class="mission-progress">'+Math.floor(v)+'/'+m.goal+'</div></div><button class="collect-btn" data-id="'+m.id+'"'+(can?'':' disabled')+'>'+(done?'ĐÃ NHẬN':(can?'NHẬN':'CHƯA ĐẠT'))+'</button></div>'; });
  $('missionList').innerHTML=h; updateBadge();
}
$('missionList').addEventListener('click', e => {
  const b=e.target.closest('button'); if(!b||b.disabled) return;
  const m=MISSIONS.find(x=>x.id===b.dataset.id); if(!m||claimed[m.id]||m.val()<m.goal) return;
  claimed[m.id]=true; totalCoins+=m.reward; toast('+'+m.reward+' xu!'); saveUserData();
});
$('openMissionBtn').addEventListener('click', () => { renderMissions(); $('missionModal').style.display='flex'; });
$('closeMissionBtn').addEventListener('click', () => { $('missionModal').style.display='none'; });
 
// ---------- Trạng thái game ----------
let currentCoins=0, speed=4.5, frame=0, holding=false, paused=false, tutSpawned=false, grace=0, fade=0, groundRef=330;
let bullets=[], slashes=[], zombies=[], humans=[], obstacles=[], powerups=[], coinTrails=[], particles=[], ground=[], humanXs=[];
let bgOffset=0;
let tutorialDone = store.getItem('zt_tut')==='1';
const SOLID=['CAR','BUS','HELI','WALL'];
const buffs={shield:0};
let banner={t:'',life:0};
const bonusDur=()=>360+(lv.time-1)*120;
const gravity=.65, defaultGroundY=330, LVL=[262,296,330,364];
let tsunamiActive=false,tsunamiTimer=0,giantActive=false,giantTimer=0,ninjaActive=false,ninjaTimer=0,lionActive=false,lionTimer=0;
 
function addParticles(x,y,color,count=12){
  if(particles.length>200) return;
  for(let i=0;i<count;i++) particles.push({x,y,vx:(Math.random()-.5)*8,vy:(Math.random()-.5)*8,life:25,color});
}
 
// ---------- Địa hình lúc cao lúc thấp ----------
function initTerrain(){ ground=[{x:-300,w:1700,y0:330,y1:330}]; genTerrain(); groundRef=330; }
function genTerrain(){
  let last=ground[ground.length-1];
  while(last.x+last.w<1500){
    const x=last.x+last.w, lvlY=last.y1, flat=(last.y0===last.y1 && !last.pit), roll=Math.random();
    let seg;
    if(flat && last.w>380 && roll<.26) seg={x,w:115+Math.random()*40,y0:lvlY,y1:lvlY,pit:true};
    else if(flat && roll<.62){
      const opts=LVL.filter(v=>v!==lvlY), ny=opts[Math.floor(Math.random()*opts.length)];
      seg={x,w:Math.abs(ny-lvlY)*2.4+70,y0:lvlY,y1:ny};
    } else seg={x,w:430+Math.random()*420,y0:lvlY,y1:lvlY};
    ground.push(seg); last=seg;
  }
}
function segAt(x){ for(let i=0;i<ground.length;i++){ const g=ground[i]; if(x>=g.x && x<g.x+g.w) return g; } return null; }
function terrainY(x){ const g=segAt(x); if(!g||g.pit) return null; return g.y0+(g.y1-g.y0)*(x-g.x)/g.w; }
function pitSurf(x){ const g=segAt(x); return (g&&g.pit)?g.y0:null; }
function flatAt(x,w){ const g=segAt(x); return (g && !g.pit && g.y0===g.y1 && x+w<g.x+g.w) ? g.y0 : null; }
 
// ---------- Điều khiển ----------
function startGame(){ resetGame(); gameState='PLAYING'; menuOverlay.style.display='none'; playMusic(); }
playBtn.addEventListener('click', startGame);
function togglePause(){ if(gameState!=='PLAYING') return; paused=!paused; if(paused) pauseMusic(); else playMusic(); }
function handleInput(){
  if(paused) return;
  playMusic();
  if(gameState==='GAMEOVER'){
    gameState='MENU'; menuOverlay.style.display='block'; initTerrain(); zombies=[]; humans=[]; obstacles=[]; coinTrails=[]; powerups=[]; bullets=[]; slashes=[]; particles=[];
    currentMap=MAP_LIST[Math.floor(Math.random()*MAP_LIST.length)]; saveUserData();
  } else if(gameState==='PLAYING'){
    const JV=13.5+(lv.jump-1)*.8;
    zombies.forEach((z,idx) => {
      if(z.isGrounded || (ninjaActive && !z.dj)) setTimeout(() => {
        if(gameState!=='PLAYING' || paused) return;
        if(z.isGrounded || (ninjaActive && !z.dj)){ if(!z.isGrounded) z.dj=true; z.vy=-JV-idx*.02; z.isGrounded=false; playSound('jump'); }
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
 
function switchRandomMap(){ const a=MAP_LIST.filter(m=>m!==currentMap); currentMap=a[Math.floor(Math.random()*a.length)]; fade=1; }
function clearModes(){ tsunamiActive=giantActive=ninjaActive=lionActive=false; tsunamiTimer=giantTimer=ninjaTimer=lionTimer=0; }
function resetGame(){
  score=0; currentCoins=0; speed=4.5; frame=0; distance=0; grace=0;
  initTerrain();
  zombies=[]; for(let i=0;i<lv.start;i++) zombies.push({x:180-i*22,y:defaultGroundY-19,vy:0,isGrounded:true,legAngle:i*.5,variant:i%3,dj:false});
  humans=[]; obstacles=[]; powerups=[]; coinTrails=[]; particles=[]; bullets=[]; slashes=[];
  paused=false; tutSpawned=false; buffs.shield=0; banner.life=0; clearModes();
  currentMap=MAP_LIST[Math.floor(Math.random()*MAP_LIST.length)]; mapTimer=0;
}
function triggerGameOver(){
  gameState='GAMEOVER'; stat.games++; stat.coins+=currentCoins;
  if(Math.floor(distance)>stat.maxDist) stat.maxDist=Math.floor(distance);
  if(score>bestScore){ bestScore=score; store.setItem('zt_best_score',bestScore); bestScoreText.innerText=bestScore; }
  saveUserData();
}
function addZombie(spacing){
  if(zombies.length>=40) return;
  const tail=zombies[zombies.length-1];
  zombies.push({x:tail.x-spacing,y:tail.y,vy:0,isGrounded:true,legAngle:0,variant:Math.floor(Math.random()*3),dj:false});
}
function eatReward(n,mult){
  score+=n; const gain=n*mult*(lionActive?2:1); currentCoins+=gain; totalCoins+=gain; totalEatenHumans+=n;
  if(mult===10) stat.veh++;
  if(score>maxSingleRunEaten) maxSingleRunEaten=score;
}
function collectBonus(x,y,dur){
  const roll=Math.floor(Math.random()*6);
  if(roll<4) clearModes();
  if(roll===0){ tsunamiActive=true; tsunamiTimer=dur; addParticles(x,y,'#00e5ff',35); banner={t:'🌊 SÓNG THẦN!',life:80}; }
  else if(roll===1){ giantActive=true; giantTimer=dur; addParticles(x,y,'#76ba1b',35); banner={t:'👹 QUÁI VẬT KHỔNG LỒ!',life:80}; playSound('slash'); }
  else if(roll===2){ ninjaActive=true; ninjaTimer=dur; addParticles(x,y,'#ffffff',35); banner={t:'🥷 NINJA!',life:80}; }
  else if(roll===3){ lionActive=true; lionTimer=dur; addParticles(x,y,'#ffca28',35); banner={t:'🦁 MÚA LÂN!',life:80}; }
  else if(roll===4){ buffs.shield=dur; addParticles(x,y,'#40c4ff',30); banner={t:'🛡️ KHIÊN BẢO VỆ!',life:80}; }
  else { for(let q=0;q<6;q++) addZombie(20); addParticles(x,y,'#8bc34a',30); banner={t:'🧟 +6 ZOMBIE!',life:80}; }
}
 
// ---------- Update ----------
function update(){
  if(paused) return;
  frame++;
  bgOffset += (gameState==='MENU' ? 1.5 : speed);
  if(gameState!=='PLAYING') return;
 
  distance += speed/10;
  if(frame%90===0) persist();
  mapTimer++; if(mapTimer>=1500){ mapTimer=0; switchRandomMap(); }
  speed = 4.5+Math.floor(frame/600)*.4; if(ninjaActive) speed*=1.35; speed=Math.min(speed,9);
 
  if(tsunamiActive && --tsunamiTimer<=0){ tsunamiActive=false; grace=70; }
  if(giantActive && --giantTimer<=0){ giantActive=false; grace=70; }
  if(ninjaActive && --ninjaTimer<=0){ ninjaActive=false; grace=40; }
  if(lionActive && --lionTimer<=0){ lionActive=false; grace=40; }
  if(buffs.shield>0) buffs.shield--; if(grace>0) grace--;
  const power=tsunamiActive||giantActive, rush=power||ninjaActive||lionActive, bonusDuration=bonusDur();
  if(zombies.length>stat.maxHorde) stat.maxHorde=zombies.length;
 
  // địa hình
  ground.forEach(g => g.x-=speed);
  while(ground.length>2 && ground[0].x+ground[0].w<-150) ground.shift();
  genTerrain();
 
  // xu
  if(frame%160===0 && Math.random()<.6){
    const gy=flatAt(850,200);
    if(gy!==null){ const count=5+Math.floor(Math.random()*4), cy=gy-40-(Math.random()>.5?40:0); for(let c=0;c<count;c++) coinTrails.push({x:850+c*24,y:cy,collected:false}); }
  }
  ground.forEach(g => { if(g.pit && !g.coined && g.x>600 && g.x<1000){ g.coined=true;
    for(let c=0;c<7;c++){ const t=c/6; coinTrails.push({x:g.x-10+t*(g.w+20),y:g.y0-45-Math.sin(t*Math.PI)*55,collected:false}); } } });
  // hộp bí ẩn
  if(frame%(600-(lv.box-1)*80)===0 && !rush && Math.random()<.75){
    const gy=flatAt(840,120); if(gy!==null) powerups.push({x:850,y:gy-70,w:38,h:38,collected:false});
  }
  // người / cảnh sát / vật cản
  if(frame%130===0){
    const G=flatAt(850,230);
    if(G!==null){
      const r=(frame===130 && !tutorialDone) ? .4 : Math.random(), X=850;
      if(r<.26) humans.push({x:X,y:G-20,gender:Math.random()>.5?'MALE':'FEMALE',eaten:false,panic:false,step:0,cop:Math.random()<.25,cd:70,flash:0});
      else if(r<.46){ const tut=!tutorialDone&&!tutSpawned; if(tut) tutSpawned=true;
        obstacles.push({x:X,y:G-48,w:100,h:48,type:'CAR',reqZombies:tut?Math.max(1,lv.start):4,peopleInside:3,hitCooldown:0,tut}); }
      else if(r<.58) obstacles.push({x:X,y:G-62,w:160,h:62,type:'BUS',reqZombies:6,peopleInside:6,hitCooldown:0});
      else if(r<.66) obstacles.push({x:X,y:G-78,w:210,h:68,type:'HELI',reqZombies:8,peopleInside:8,hitCooldown:0});
      else if(r<.76) obstacles.push({x:X,y:G-45,w:45,h:45,type:'BOMB'});
      else if(r<.86) obstacles.push({x:X,y:G-22,w:64,h:22,type:'SPIKE'});
      else if(r<.94) obstacles.push({x:X,y:G-16,w:44,h:16,type:'SPRING',comp:0});
      else obstacles.push({x:X,y:G-72,w:36,h:72,type:'WALL',reqZombies:3,peopleInside:0,hitCooldown:0});
    }
  }
 
  coinTrails.forEach(c => {
    c.x-=speed;
    if(!c.collected && zombies.some(z => Math.abs(z.x-c.x)<25 && Math.abs(z.y-c.y)<30)){
      c.collected=true; currentCoins++; totalCoins++; playSound('coin'); addParticles(c.x,c.y,'#fbc02d',5);
    }
  });
  coinTrails=coinTrails.filter(c => c.x>-30 && !c.collected);
 
  powerups.forEach(pw => {
    pw.x-=speed;
    const picker=zombies.find(z => Math.abs(z.x-pw.x)<35 && Math.abs(z.y-pw.y)<40);
    if(!pw.collected && picker){ pw.collected=true; stat.boxes++; playSound('powerup'); triggerShake(16); collectBonus(pw.x,pw.y,bonusDuration); }
  });
  powerups=powerups.filter(p => p.x>-50 && !p.collected);
 
  // vật cản
  let blocked=false;
  for(let oi=obstacles.length-1;oi>=0;oi--){
    const obs=obstacles[oi]; obs.x-=speed; if(obs.hitCooldown>0) obs.hitCooldown--;
    const isVeh=SOLID.includes(obs.type), lead=zombies[0];
    if(rush){
      if(lead && obs.type!=='SPRING'){
        const d=obs.x-lead.x;
        if(d<150 && d>-obs.w-40){
          playSound(ninjaActive?'slash':'explode'); triggerShake(ninjaActive?5:10);
          addParticles(obs.x+obs.w/2,obs.y,giantActive?'#e040fb':(ninjaActive?'#ffffff':(lionActive?'#ffca28':'#00e5ff')),ninjaActive?14:28);
          if(ninjaActive) slashes.push({x:obs.x+obs.w/2,y:obs.y+obs.h/2,life:14});
          if(isVeh){ eatReward(obs.peopleInside,10); for(let k=0;k<obs.peopleInside;k++) addZombie(20); } else score+=2;
          obstacles.splice(oi,1);
        }
      }
    } else if(isVeh){
      const above=lead && lead.y<obs.y-12;
      if(lead && !above && lead.x+8>=obs.x && lead.x-12<=obs.x+obs.w && lead.y>=obs.y-15){
        if(zombies.length>=obs.reqZombies){
          playSound('explode'); triggerShake(15); addParticles(obs.x+obs.w/2,obs.y+obs.h/2,'#ff9800',32);
          eatReward(obs.peopleInside,10); for(let k=0;k<obs.peopleInside;k++) addZombie(22);
          obstacles.splice(oi,1);
        } else {
          blocked=true;
          if(obs.hitCooldown===0){
            obs.hitCooldown=30; playSound('explode'); triggerShake(8);
            if(buffs.shield<=0){ const v=zombies.pop(); if(v) addParticles(v.x,v.y,'#ff1744',25); }
            if(zombies.length===0){ triggerGameOver(); return; }
          }
        }
      }
    } else if(obs.type==='SPIKE'){
      const i=zombies.findIndex(z => z.y+19>obs.y+8 && z.x>obs.x-8 && z.x<obs.x+obs.w+8);
      if(i>=0){ playSound('explode'); triggerShake(10); addParticles(zombies[i].x,zombies[i].y,'#ff1744',22); if(buffs.shield<=0) zombies.splice(i,1); obstacles.splice(oi,1); }
    } else if(obs.type==='SPRING'){
      if(obs.comp>0) obs.comp--;
      zombies.forEach(z => { if(z.vy>=0 && z.y+19>=obs.y+10 && z.y+19<=obs.y+34 && z.x>obs.x-6 && z.x<obs.x+obs.w+6){ z.vy=-19; z.isGrounded=false; z.dj=false; obs.comp=10; playSound('jump'); } });
    } else {
      const bx=obs.x+22, by=obs.y+22;
      for(let i=zombies.length-1;i>=0;i--){
        const z=zombies[i];
        if(Math.hypot(z.x-bx,z.y-by)<40){ playSound('explode'); triggerShake(20); addParticles(bx,by,'#ff1744',40); if(buffs.shield<=0) zombies.splice(i,1); obstacles.splice(oi,1); break; }
      }
    }
  }
  if(zombies.length===0){ triggerGameOver(); return; }
 
  // vật lý zombie + địa hình + rơi xuống hố
  { const g0=terrainY(zombies[0].x); if(g0!==null) groundRef+=(g0-groundRef)*.15; }
  for(let i=zombies.length-1;i>=0;i--){
    const z=zombies[i];
    if(tsunamiActive){ z.y=groundRef-110+Math.sin(frame*.15+i*.4)*8; z.vy=0; z.isGrounded=true; }
    else if(giantActive){ z.y=groundRef-35; z.vy=0; z.isGrounded=true; }
    else {
      z.vy += (holding && z.vy<0) ? gravity*.6 : gravity; z.y += z.vy;
      let onVeh=false;
      for(let o=0;o<obstacles.length;o++){
        const obs=obstacles[o];
        if(SOLID.includes(obs.type) && z.x>=obs.x-5 && z.x<=obs.x+obs.w+5){
          const roofY=obs.y-18;
          if(z.y>=roofY-5 && z.y<=obs.y+12 && z.vy>=0){ z.y=roofY; z.vy=0; z.isGrounded=true; z.dj=false; onVeh=true; }
        }
      }
      if(!onVeh){
        let gy=terrainY(z.x); if(gy===null && (rush||grace>0)) gy=pitSurf(z.x);
        if(gy!==null && z.vy>=0 && (z.y+19>=gy || (z.isGrounded && gy-(z.y+19)<=14))){ z.y=gy-19; z.vy=0; z.isGrounded=true; z.dj=false; }
        else if(gy===null) z.isGrounded=false;
      }
    }
    z.legAngle += z.isGrounded ? .22 : .08;
    if(blocked && i===0) z.x=Math.max(100,z.x-speed);
    const pg=pitSurf(z.x);
    if(!rush && grace<=0 && pg!==null && z.y+19>pg+30){
      playSound('fall'); triggerShake(6); addParticles(z.x,pg+34,'#76ba1b',16); zombies.splice(i,1); continue;
    }
    if(z.y>canvas.height+30) zombies.splice(i,1);
  }
  if(zombies.length===0){ triggerGameOver(); return; }
 
  // đội hình
  zombies.forEach((z,i) => {
    if(i===0){ z.x += (180-z.x)*.05; return; }
    const ring=Math.ceil(Math.sqrt(i)), slot=zombies[0].x-ring*18+(i%3)*7;
    z.x += (slot-z.x)*.12;
  });
 
  // người & cảnh sát
  const lead=zombies[0];
  humans.forEach(h => {
    h.x-=speed;
    if(h.cop){
      h.cd--; if(h.flash>0) h.flash--;
      if(h.cd<=0 && h.x<760 && h.x>lead.x+90 && !rush){ bullets.push({x:h.x-24,y:h.y-6}); h.cd=110; h.flash=6; playSound('shot'); }
    } else if(h.x>lead.x && h.x-lead.x<280) h.panic=true;
    if(h.panic){ h.x+=2.2; h.step+=.4; }
    const gy=terrainY(h.x); if(gy!==null) h.y=gy-20; else h.y+=5;
    if(h.eaten) return;
    const rng = power ? 450 : (lionActive ? lead.x+260 : (ninjaActive ? lead.x+170 : 0));
    const eater = rng ? ((h.x<rng && h.x>lead.x-40) ? lead : null) : zombies.find(z => Math.abs(z.x-h.x)<30 && Math.abs(z.y-h.y)<50);
    if(eater){
      h.eaten=true; eatReward(1,5); if(h.cop) stat.cops++; playSound('eat');
      if(ninjaActive) slashes.push({x:h.x,y:h.y-10,life:14});
      addParticles(h.x,h.y-10,giantActive?'#e040fb':(tsunamiActive?'#00e5ff':'#76ba1b'),12); addZombie(20);
    }
  });
  // đạn
  bullets.forEach(b => b.x-=speed+7);
  for(let bi=bullets.length-1;bi>=0;bi--){
    const b=bullets[bi]; if(b.x<-20){ bullets.splice(bi,1); continue; }
    if(rush) continue;
    const zi=zombies.findIndex(z => Math.abs(z.x-b.x)<12 && b.y>z.y-42 && b.y<z.y+18);
    if(zi>=0){ playSound('explode'); triggerShake(6); addParticles(zombies[zi].x,zombies[zi].y,'#ff1744',16); if(buffs.shield<=0) zombies.splice(zi,1); bullets.splice(bi,1); }
  }
  if(zombies.length===0){ triggerGameOver(); return; }
  humans=humans.filter(h => h.x>-50 && !h.eaten && h.y<500);
  obstacles=obstacles.filter(o => o.x>-260);
  if(!tutorialDone && tutSpawned && !obstacles.some(o=>o.tut)){ tutorialDone=true; store.setItem('zt_tut','1'); }
  slashes.forEach(s=>s.life--); slashes=slashes.filter(s=>s.life>0);
  particles.forEach(p => { p.x+=p.vx; p.y+=p.vy; p.life--; });
  particles=particles.filter(p => p.life>0);
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
 
function outText(t,x,y,size,fill,align){
  ctx.font='900 '+size+'px "Arial Black",sans-serif'; ctx.textAlign=align||'left';
  ctx.lineWidth=5; ctx.lineJoin='round'; ctx.strokeStyle='#3a1500'; ctx.strokeText(t,x,y);
  ctx.fillStyle=fill; ctx.fillText(t,x,y);
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
 
 
function rnd(k,n){ const v=Math.sin(k*127.1+n*311.7)*43758.5453; return v-Math.floor(v); }
 
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
 
 
function drawGiantMonster(){
  const gX=180, gY=groundRef-50;
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
// ---------- Lớp nền cache (tối ưu): vẽ 1 lần vào canvas phụ rồi chỉ dán lại ----------
let tileIdx=0, layerCache={}, layerMap='';
function tiles(sp,w,fn,live){
  if(live){ const base=Math.floor(bgOffset*sp/w); for(let i=-1;i<=800/w+1;i++){ const k=base+i; fn(k*w-bgOffset*sp,k); } return; }
  const key=(tileIdx++)+':'+sp+':'+w, P=w*Math.ceil(1600/w);
  let c=layerCache[key];
  if(!c){
    c=document.createElement('canvas'); c.width=P; c.height=410;
    const o=c.getContext('2d'), saved=ctx; ctx=o;
    try{ for(let k=0;k<P/w;k++){ fn(k*w,k); fn(k*w-P,k); } } finally { ctx=saved; }
    layerCache[key]=c;
  }
  const off=(bgOffset*sp)%P; ctx.drawImage(c,-off,0); ctx.drawImage(c,P-off,0);
}
function hillPoly(sp,y0,amp,col,f){
  ctx.fillStyle=col; ctx.beginPath(); ctx.moveTo(0,400);
  for(let x=0;x<=800;x+=16) ctx.lineTo(x,y0+Math.sin((x+bgOffset*sp)*f)*amp+Math.sin((x+bgOffset*sp)*f*2.3)*amp*.4);
  ctx.lineTo(800,400); ctx.fill();
}
function cloudC(x,y,sc,col){ ctx.fillStyle=col; ctx.beginPath(); ctx.arc(x,y,16*sc,0,7); ctx.arc(x+20*sc,y-8*sc,22*sc,0,7); ctx.arc(x+44*sc,y,17*sc,0,7); ctx.arc(x+22*sc,y+6*sc,18*sc,0,7); ctx.fill(); }
 
// ================= BÃI BIỂN =================
function drawBeachMap(){
  let g=ctx.createLinearGradient(0,0,0,215); g.addColorStop(0,'#2f9de0'); g.addColorStop(.6,'#8fd8f5'); g.addColorStop(1,'#fff0c2'); ctx.fillStyle=g; ctx.fillRect(0,0,800,215);
  let sg=ctx.createRadialGradient(140,95,6,140,95,150); sg.addColorStop(0,'rgba(255,255,220,1)'); sg.addColorStop(.25,'rgba(255,240,170,.8)'); sg.addColorStop(1,'rgba(255,240,170,0)'); ctx.fillStyle=sg; ctx.fillRect(0,0,440,270);
  ctx.fillStyle='#fffbe0'; ctx.beginPath(); ctx.arc(140,95,26,0,7); ctx.fill();
  tiles(.05,300,(x,k)=>cloud(x+rnd(k,2)*140,24+rnd(k,1)*70,.8+rnd(k,3)*.7,.9));
  let sea=ctx.createLinearGradient(0,205,0,305); sea.addColorStop(0,'#8fe3f0'); sea.addColorStop(.35,'#19b0d0'); sea.addColorStop(1,'#0a6f9c'); ctx.fillStyle=sea; ctx.fillRect(0,205,800,100);
  tiles(.05,760,(x,k)=>{
    if(rnd(k,1)>.25){
      const ix=x+300; ctx.fillStyle='#4f9a62'; ctx.beginPath(); ctx.ellipse(ix,208,130,20,0,Math.PI,0); ctx.fill();
      ctx.fillStyle='#3d7f50'; ctx.beginPath(); ctx.ellipse(ix-40,208,60,12,0,Math.PI,0); ctx.fill();
      const lx=ix+40;
      for(let i=0;i<4;i++){ const y1=208-i*14.5, w1=8-i*.7; ctx.fillStyle=i%2?'#e53935':'#ffffff'; ctx.beginPath(); ctx.moveTo(lx-w1,y1); ctx.lineTo(lx+w1,y1); ctx.lineTo(lx+w1-.7,y1-14.5); ctx.lineTo(lx-w1+.7,y1-14.5); ctx.fill(); }
      ctx.fillStyle='#37474f'; ctx.fillRect(lx-9,146,18,4); ctx.fillStyle='#ffe66b'; ctx.fillRect(lx-5,136,10,10);
      ctx.fillStyle='#e53935'; ctx.beginPath(); ctx.moveTo(lx-8,136); ctx.lineTo(lx,124); ctx.lineTo(lx+8,136); ctx.fill();
    }
  });
  tiles(.1,430,(x,k)=>{
    if(rnd(k,4)>.4){ const bx=x+150, by=236+rnd(k,5)*22;
      ctx.fillStyle='#6d4c41'; ctx.beginPath(); ctx.moveTo(bx-22,by); ctx.lineTo(bx+24,by); ctx.lineTo(bx+16,by+9); ctx.lineTo(bx-16,by+9); ctx.fill();
      ctx.fillStyle='#fff'; ctx.beginPath(); ctx.moveTo(bx,by-2); ctx.lineTo(bx,by-34); ctx.lineTo(bx+20,by-2); ctx.fill();
      ctx.fillStyle='#e53935'; ctx.beginPath(); ctx.moveTo(bx-3,by-2); ctx.lineTo(bx-3,by-28); ctx.lineTo(bx-18,by-2); ctx.fill(); }
  });
  for(let r=0;r<3;r++){
    ctx.strokeStyle='rgba(255,255,255,'+(.3+r*.12)+')'; ctx.lineWidth=2; ctx.beginPath();
    for(let x=0;x<=800;x+=14){ const y=230+r*24+Math.sin((x+bgOffset*(.3+r*.1))*.04+r)*3; if(x) ctx.lineTo(x,y); else ctx.moveTo(x,y); }
    ctx.stroke();
  }
  for(let i=0;i<14;i++){ const x=(i*97+frame*.15)%800, y=215+(i*29)%80; ctx.fillStyle='rgba(255,255,255,'+(.35+.35*Math.sin(frame*.08+i))+')'; ctx.fillRect(x,y,6,2); }
  let sand=ctx.createLinearGradient(0,294,0,400); sand.addColorStop(0,'#f8e0a0'); sand.addColorStop(1,'#e2b96a'); ctx.fillStyle=sand; ctx.fillRect(0,296,800,110);
  ctx.fillStyle='rgba(255,255,255,.85)'; ctx.beginPath(); ctx.moveTo(0,304);
  for(let x=0;x<=800;x+=10) ctx.lineTo(x,296+Math.sin((x+frame*1.2)*.05)*3+Math.sin(frame*.03)*2);
  ctx.lineTo(800,304); ctx.fill();
  tiles(.5,560,(x,k)=>{
    if(rnd(k,6)>.35){ const hx=x+100;
      ctx.fillStyle='#8d6e4a'; ctx.fillRect(hx,222,6,76); ctx.fillRect(hx+84,222,6,76);
      ctx.fillStyle='#d6a93f'; ctx.beginPath(); ctx.moveTo(hx-14,228); ctx.lineTo(hx+45,178); ctx.lineTo(hx+104,228); ctx.fill();
      ctx.strokeStyle='#a87d1f'; ctx.lineWidth=2; for(let l=0;l<6;l++){ ctx.beginPath(); ctx.moveTo(hx+45,180); ctx.lineTo(hx-8+l*19,226); ctx.stroke(); }
      ['#e53935','#fdd835','#43a047','#1e88e5','#8e24aa','#fb8c00'].forEach((c,i)=>{ ctx.fillStyle=c; ctx.beginPath(); ctx.moveTo(hx-8+i*20,228); ctx.lineTo(hx+2+i*20,228); ctx.lineTo(hx-3+i*20,240); ctx.fill(); });
      ctx.fillStyle='#a1693a'; ctx.fillRect(hx+8,264,74,34); ctx.fillStyle='#c98a4b'; ctx.fillRect(hx+4,260,82,6);
      ctx.fillStyle='#ff7043'; ctx.fillRect(hx+22,242,46,14); ctx.fillStyle='#fff'; ctx.font='900 10px "Arial Black",sans-serif'; ctx.textAlign='center'; ctx.fillText('TIKI BAR',hx+45,253);
      ctx.fillStyle='#4fc3f7'; ctx.fillRect(hx+16,248+22,8,12); ctx.fillStyle='#ffd54f'; ctx.fillRect(hx+30,250+22,8,10);
    }
  });
  tiles(.7,380,(x,k)=>{
    const tx=x+70+rnd(k,1)*80, sway=(rnd(k,2)-.5)*50, topx=tx+sway, topy=150+rnd(k,3)*20;
    ctx.strokeStyle='#8d6234'; ctx.lineWidth=12; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(tx,300); ctx.quadraticCurveTo(tx+sway*.2,230,topx,topy); ctx.stroke();
    ctx.strokeStyle='#6b4a26'; ctx.lineWidth=2; for(let i=0;i<7;i++){ const t=i/7, px=(1-t)*(1-t)*tx+2*(1-t)*t*(tx+sway*.2)+t*t*topx, py=(1-t)*(1-t)*300+2*(1-t)*t*230+t*t*topy; ctx.beginPath(); ctx.moveTo(px-6,py); ctx.lineTo(px+6,py+2); ctx.stroke(); }
    for(let a=0;a<7;a++){ const an=-Math.PI+(a/6)*Math.PI*1.0-.1, ex=topx+Math.cos(an)*58, ey=topy+Math.sin(an)*30+22;
      ctx.strokeStyle='#2e7d32'; ctx.lineWidth=9; ctx.beginPath(); ctx.moveTo(topx,topy); ctx.quadraticCurveTo(topx+Math.cos(an)*30,topy-16,ex,ey); ctx.stroke();
      ctx.strokeStyle='#66bb6a'; ctx.lineWidth=4; ctx.beginPath(); ctx.moveTo(topx,topy); ctx.quadraticCurveTo(topx+Math.cos(an)*30,topy-16,ex,ey); ctx.stroke(); }
    ctx.fillStyle='#5d4037'; ctx.beginPath(); ctx.arc(topx-4,topy+6,5,0,7); ctx.arc(topx+5,topy+8,5,0,7); ctx.fill();
  });
  tiles(.82,250,(x,k)=>{
    if(rnd(k,5)>.3){ const ux=x+120, cols=rnd(k,6)>.5?['#e53935','#ffffff']:['#1e88e5','#fdd835'];
      ctx.fillStyle='#eee'; ctx.fillRect(ux-2,250,4,48);
      for(let i=0;i<6;i++){ ctx.fillStyle=cols[i%2]; ctx.beginPath(); ctx.moveTo(ux,250); ctx.arc(ux,250,42,Math.PI+i*Math.PI/6,Math.PI+(i+1)*Math.PI/6); ctx.closePath(); ctx.fill(); }
      for(let i=0;i<5;i++){ ctx.fillStyle=i%2?'#fff':'#ff80ab'; ctx.fillRect(ux+30+i*9,292,9,8); }
    }
  });
  tiles(.95,100,(x,k)=>{
    const t=Math.floor(rnd(k,7)*6), sy=310+rnd(k,8)*22, sx=x+30;
    if(t===0){ ctx.fillStyle='#ff8a3d'; ctx.beginPath(); for(let i=0;i<10;i++){ const r=i%2?3:8, an=i*Math.PI/5-Math.PI/2; ctx.lineTo(sx+Math.cos(an)*r,sy+Math.sin(an)*r); } ctx.fill(); }
    else if(t===1){ ctx.fillStyle='#f8bbd0'; ctx.beginPath(); ctx.ellipse(sx,sy,8,5,0,0,7); ctx.fill(); ctx.strokeStyle='#e57fa2'; ctx.lineWidth=1; ctx.stroke(); }
    else if(t===2){ const cols=['#e53935','#fff','#1e88e5','#fdd835']; for(let i=0;i<4;i++){ ctx.fillStyle=cols[i]; ctx.beginPath(); ctx.moveTo(sx,sy-8); ctx.arc(sx,sy-8,9,i*Math.PI/2,(i+1)*Math.PI/2); ctx.fill(); } }
    else if(t===3){ ctx.fillStyle='#d9b26a'; ctx.fillRect(sx-12,sy-10,24,12); ctx.fillRect(sx-14,sy-20,8,10); ctx.fillRect(sx+6,sy-20,8,10); ctx.fillStyle='#e53935'; ctx.fillRect(sx-1,sy-30,2,12); ctx.fillRect(sx,sy-30,9,5); }
  });
  birds('#ffffff');
}
 
// ================= NGHĨA ĐỊA (HALLOWEEN) =================
function drawGraveMap(){
  let g=ctx.createLinearGradient(0,0,0,300); g.addColorStop(0,'#060a22'); g.addColorStop(.55,'#2b1553'); g.addColorStop(1,'#80407f'); ctx.fillStyle=g; ctx.fillRect(0,0,800,400);
  tiles(.02,110,(x,k)=>{ for(let i=0;i<3;i++){ const sx=x+rnd(k,i)*100, sy=rnd(k,i+5)*190, r=rnd(k,i+9)>.8?2:1; ctx.fillStyle='rgba(255,255,255,'+(.4+rnd(k,i+3)*.6)+')'; ctx.fillRect(sx,sy,r,r); } });
  let mg=ctx.createRadialGradient(620,95,10,620,95,160); mg.addColorStop(0,'rgba(255,245,190,.5)'); mg.addColorStop(1,'rgba(255,245,190,0)'); ctx.fillStyle=mg; ctx.fillRect(440,0,360,260);
  ctx.fillStyle='#fff6d0'; ctx.beginPath(); ctx.arc(620,95,40,0,7); ctx.fill();
  ctx.fillStyle='#ecdfae'; ctx.beginPath(); ctx.arc(606,84,8,0,7); ctx.arc(632,108,10,0,7); ctx.arc(628,78,5,0,7); ctx.fill();
  tiles(.05,320,(x,k)=>cloudC(x+rnd(k,2)*150,40+rnd(k,1)*90,.9+rnd(k,3)*.6,'rgba(60,30,90,.65)'));
  hillPoly(.06,225,22,'#1c0f3a',.009); hillPoly(.12,252,16,'#150b2c',.013);
  tiles(.18,300,(x,k)=>{
    if(rnd(k,1)>.35){ const tx=x+120; ctx.strokeStyle='#0c0718'; ctx.lineCap='round'; ctx.lineWidth=9; ctx.beginPath(); ctx.moveTo(tx,300); ctx.quadraticCurveTo(tx+8,240,tx-4,190); ctx.stroke();
      const br=(bx,by,ex,ey,w)=>{ ctx.lineWidth=w; ctx.beginPath(); ctx.moveTo(bx,by); ctx.quadraticCurveTo((bx+ex)/2,by-12,ex,ey); ctx.stroke(); };
      br(tx-2,205,tx-40,170,5); br(tx-2,215,tx+36,176,5); br(tx-4,192,tx-14,150,4); br(tx-30,176,tx-52,168,3); br(tx+24,182,tx+46,160,3); }
  });
  tiles(.28,950,(x,k)=>{
    if(rnd(k,1)>.25){ const mx=x+100;
      ctx.fillStyle='#140b27'; ctx.fillRect(mx+50,180,200,120); ctx.beginPath(); ctx.moveTo(mx+40,182); ctx.lineTo(mx+150,120); ctx.lineTo(mx+260,182); ctx.fill();
      ctx.fillRect(mx,142,44,158); ctx.beginPath(); ctx.moveTo(mx-8,144); ctx.lineTo(mx+22,92); ctx.lineTo(mx+52,144); ctx.fill(); ctx.fillRect(mx+200,126,14,40);
      ctx.shadowColor='#ffb300'; ctx.shadowBlur=14; ctx.fillStyle='#ffcc33';
      [[mx+66,200],[mx+110,200],[mx+190,200],[mx+66,244],[mx+190,244],[mx+12,170],[mx+12,220],[mx+140,150]].forEach(([wx,wy],i)=>{ if(rnd(k,i+20)>.25) ctx.fillRect(wx,wy,18,26); });
      ctx.shadowBlur=0; ctx.fillStyle='#140b27'; ctx.fillRect(mx+120,262,32,38); ctx.beginPath(); ctx.arc(mx+136,262,16,Math.PI,0); ctx.fill();
      ctx.strokeStyle='#3b2a55'; ctx.lineWidth=1.5; [[mx+66,200],[mx+110,200],[mx+190,200]].forEach(([wx,wy])=>{ ctx.strokeRect(wx,wy,18,26); ctx.beginPath(); ctx.moveTo(wx+9,wy); ctx.lineTo(wx+9,wy+26); ctx.moveTo(wx,wy+13); ctx.lineTo(wx+18,wy+13); ctx.stroke(); });
    }
  });
  let st=ctx.createLinearGradient(0,296,0,406); st.addColorStop(0,'#273526'); st.addColorStop(1,'#121812'); ctx.fillStyle=st; ctx.fillRect(0,296,800,110);
  tiles(.6,160,(x,k)=>{
    const t=Math.floor(rnd(k,2)*4), sx=x+60+rnd(k,3)*40; ctx.save(); ctx.translate(sx,296); ctx.rotate((rnd(k,4)-.5)*.18);
    ctx.fillStyle='#7b7b92'; ctx.strokeStyle='#4b4b5e'; ctx.lineWidth=2;
    if(t===0){ ctx.beginPath(); ctx.moveTo(-13,0); ctx.lineTo(-13,-34); ctx.arc(0,-34,13,Math.PI,0); ctx.lineTo(13,0); ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.fillStyle='#3b3b4b'; ctx.font='900 8px Arial'; ctx.textAlign='center'; ctx.fillText('R.I.P',0,-28); }
    else if(t===1){ ctx.fillRect(-4,-46,8,46); ctx.fillRect(-14,-36,28,8); ctx.strokeRect(-4,-46,8,46); }
    else if(t===2){ ctx.beginPath(); ctx.moveTo(-9,0); ctx.lineTo(-6,-52); ctx.lineTo(0,-60); ctx.lineTo(6,-52); ctx.lineTo(9,0); ctx.closePath(); ctx.fill(); ctx.stroke(); }
    else { ctx.fillRect(-16,-22,32,22); ctx.strokeRect(-16,-22,32,22); ctx.fillStyle='#3d5a3a'; ctx.fillRect(-16,-4,32,4); }
    ctx.restore();
    ctx.fillStyle='#2f4a2c'; ctx.beginPath(); ctx.ellipse(sx,297,20,4,0,0,7); ctx.fill();
  });
  tiles(.62,24,(x,k)=>{ ctx.fillStyle='#0f0a1c'; ctx.fillRect(x,266,3,32); ctx.beginPath(); ctx.moveTo(x-2,266); ctx.lineTo(x+1.5,258); ctx.lineTo(x+5,266); ctx.fill(); if(k%2===0){ ctx.fillRect(x,274,24,2); ctx.fillRect(x,288,24,2); } });
  tiles(.85,330,(x,k)=>{
    if(rnd(k,10)>.4){ const px=x+150, py=290;
      ctx.shadowColor='#ff9a00'; ctx.shadowBlur=16; ctx.fillStyle='#ff7a00'; ctx.beginPath(); ctx.ellipse(px,py,17,14,0,0,7); ctx.fill(); ctx.shadowBlur=0;
      ctx.strokeStyle='#c45500'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.ellipse(px,py,8,14,0,0,7); ctx.stroke();
      ctx.fillStyle='#2e6b1a'; ctx.fillRect(px-2,py-18,4,7);
      ctx.fillStyle='#ffe066'; ctx.beginPath(); ctx.moveTo(px-9,py-4); ctx.lineTo(px-3,py-4); ctx.lineTo(px-6,py-10); ctx.fill(); ctx.beginPath(); ctx.moveTo(px+3,py-4); ctx.lineTo(px+9,py-4); ctx.lineTo(px+6,py-10); ctx.fill();
      ctx.beginPath(); ctx.moveTo(px-10,py+3); ctx.lineTo(px-5,py+8); ctx.lineTo(px,py+4); ctx.lineTo(px+5,py+8); ctx.lineTo(px+10,py+3); ctx.lineTo(px+8,py+9); ctx.lineTo(px-8,py+9); ctx.fill();
    }
  });
  tiles(.78,420,(x,k)=>{
    const lx=x+200; ctx.fillStyle='#0b0814'; ctx.fillRect(lx,222,4,76); ctx.fillRect(lx-2,296,8,4); ctx.fillRect(lx,222,16,3);
    let lg=ctx.createRadialGradient(lx+16,236,2,lx+16,236,48); lg.addColorStop(0,'rgba(140,255,160,.75)'); lg.addColorStop(1,'rgba(140,255,160,0)'); ctx.fillStyle=lg; ctx.fillRect(lx-34,190,100,92);
    ctx.fillStyle='#b9ffc6'; ctx.fillRect(lx+11,226,10,14); ctx.strokeStyle='#0b0814'; ctx.lineWidth=2; ctx.strokeRect(lx+11,226,10,14);
  });
  tiles(1,16,(x,k)=>{ ctx.strokeStyle='#355a30'; ctx.lineWidth=2; const y=306+rnd(k,1)*24, h=4+rnd(k,2)*7; ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x+2,y-h); ctx.stroke(); });
  for(let i=0;i<4;i++){ const x=((i*260-bgOffset*.4)%1000+1000)%1000-100; ctx.fillStyle='rgba(190,170,230,.10)'; ctx.beginPath(); ctx.ellipse(x,292+Math.sin(frame*.02+i)*6,220,26,0,0,7); ctx.fill(); }
  ctx.fillStyle='#0d0819';
  for(let i=0;i<5;i++){ const x=((900-(frame*1.6+i*95))%1000+1000)%1000-100, y=60+i*22+Math.sin(frame*.07+i)*14, f=Math.sin(frame*.4+i)*8;
    ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x-16,y-6-f); ctx.lineTo(x-12,y+4); ctx.fill(); ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x+16,y-6-f); ctx.lineTo(x+12,y+4); ctx.fill();
    ctx.beginPath(); ctx.arc(x,y+1,4,0,7); ctx.fill(); }
  for(let i=0;i<2;i++){ const gx=((i*500+300-bgOffset*.35)%1100+1100)%1100-150, gy=150+Math.sin(frame*.04+i*2)*14+i*34;
    ctx.fillStyle='rgba(235,240,255,.5)'; ctx.beginPath(); ctx.arc(gx,gy,18,Math.PI,0); ctx.lineTo(gx+18,gy+30); ctx.lineTo(gx+9,gy+24); ctx.lineTo(gx,gy+32); ctx.lineTo(gx-9,gy+24); ctx.lineTo(gx-18,gy+30); ctx.closePath(); ctx.fill();
    ctx.fillStyle='#1a1030'; ctx.beginPath(); ctx.arc(gx-6,gy-2,3,0,7); ctx.arc(gx+6,gy-2,3,0,7); ctx.fill(); ctx.beginPath(); ctx.ellipse(gx,gy+9,3,4,0,0,7); ctx.fill(); }
  for(let i=0;i<10;i++){ const x=((i*97-bgOffset*.5)%800+800)%800, y=270+Math.sin(frame*.05+i)*18; ctx.fillStyle='rgba(150,255,170,'+(.4+.4*Math.sin(frame*.1+i))+')'; ctx.beginPath(); ctx.arc(x,y,2.5,0,7); ctx.fill(); }
}
 
// ================= MẶT ĐẤT THEO ĐỊA HÌNH =================
const GTHEME={
  BEACH:{lip:'#f0d08e',road:'#b98a52',dash:'#8f6a3a',dirt:'#7a5a3a',dirt2:'#8d6a46'},
  CITY:{lip:'#9a9db8',road:'#2e2b4b',dash:'#e8e8f0',dirt:'#5a3b2a',dirt2:'#6b4733'},
  VILLAGE:{lip:'#7cb342',road:'#8a6a45',dash:'#b89464',dirt:'#5a3b2a',dirt2:'#6b4733'},
  GRAVEYARD:{lip:'#4a5d3a',road:'#33293f',dash:'#6a5a7a',dirt:'#3a2a30',dirt2:'#4a3640'}
};
function drawGround(){
  const th=GTHEME[currentMap];
  for(let gi=0;gi<ground.length;gi++){
    const g=ground[gi]; if(g.x+g.w<-10 || g.x>810) continue;
    const x0=g.x, x1=g.x+g.w, y0=g.y0, y1=g.y1;
    if(g.pit){
      ctx.fillStyle='#0a0a0a'; ctx.fillRect(x0,y0,g.w,450-y0);
      ctx.fillStyle='#161616'; ctx.fillRect(x0,y0,6,450-y0); ctx.fillRect(x1-6,y0,6,450-y0);
      continue;
    }
    const sy=x=>y0+(y1-y0)*(x-x0)/g.w;
    const band=(o1,o2,col)=>{ ctx.fillStyle=col; ctx.beginPath(); ctx.moveTo(x0,y0+o1); ctx.lineTo(x1,y1+o1); ctx.lineTo(x1,y1+o2); ctx.lineTo(x0,y0+o2); ctx.closePath(); ctx.fill(); };
    band(13,62,th.road); band(0,13,th.lip); band(62,520,th.dirt);
    band(0,3,'rgba(255,255,255,.25)'); band(13,16,'rgba(0,0,0,.35)'); band(62,66,'rgba(0,0,0,.25)');
    ctx.fillStyle=th.dash;
    for(let x=-(bgOffset%90); x<800; x+=90){ if(x>=x0 && x+48<=x1){ ctx.beginPath(); ctx.moveTo(x,sy(x)+36); ctx.lineTo(x+48,sy(x+48)+36); ctx.lineTo(x+48,sy(x+48)+40); ctx.lineTo(x,sy(x)+40); ctx.fill(); } }
    ctx.fillStyle=th.dirt2;
    for(let i=0;i<14;i++){ const x=((i*97-bgOffset)%900+900)%900-50; if(x>x0+10 && x<x1-10){ ctx.beginPath(); ctx.ellipse(x,sy(x)+72+(i*37)%40,14+(i%3)*5,8,0,0,7); ctx.fill(); } }
    ctx.strokeStyle='rgba(0,0,0,.35)'; ctx.lineWidth=2;
    for(let i=0;i<5;i++){ const x=((i*173-bgOffset)%900+900)%900-50; if(x>x0+4 && x<x1-24){ const b=sy(x); ctx.beginPath(); ctx.moveTo(x,b+20); ctx.lineTo(x+10,b+30); ctx.lineTo(x+4,b+38); ctx.lineTo(x+16,b+52); ctx.stroke(); } }
  }
}
 
function drawBackground(){
  if(layerMap!==currentMap){ layerCache={}; layerMap=currentMap; }
  tileIdx=0;
  ctx.clearRect(0,0,800,450); ctx.save();
  if(shakeDuration>0){ shakeDuration--; ctx.translate((Math.random()-.5)*10,(Math.random()-.5)*10); }
  if(currentMap==='BEACH') drawBeachMap(); else if(currentMap==='CITY') drawCityMap(); else if(currentMap==='VILLAGE') drawVillageMap(); else drawGraveMap();
  drawGround();
  if(tsunamiActive && gameState==='PLAYING'){
    const wx=zombies[0]?zombies[0].x+40:250, base=groundRef+50;
    let wg=ctx.createLinearGradient(0,30,0,base); wg.addColorStop(0,'#fff'); wg.addColorStop(.25,'#80d8ff'); wg.addColorStop(.65,'#0097a7'); wg.addColorStop(1,'#002f6c');
    ctx.fillStyle=wg; ctx.beginPath(); ctx.moveTo(-100,base); ctx.lineTo(-100,90);
    ctx.bezierCurveTo(wx-180,50,wx-30,10,wx+35,100); ctx.bezierCurveTo(wx+90,170,wx+110,260,wx+40,base);
    ctx.closePath(); ctx.fill(); ctx.fillStyle='#fff';
    for(let b=0;b<8;b++){ ctx.beginPath(); ctx.arc(wx+12+b*11,95-b*5,16-b*1.3,0,7); ctx.fill(); }
  }
}
 
function drawCityMap(){
  let g=ctx.createLinearGradient(0,0,0,300); g.addColorStop(0,'#7fb8e0'); g.addColorStop(1,'#e2f3fa'); ctx.fillStyle=g; ctx.fillRect(0,0,800,400);
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
  ctx.fillStyle='#55627e'; ctx.fillRect(0,296,800,110);
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
  },true);
  birds('#46566e');
}
 
 
function drawVillageMap(){
  let g=ctx.createLinearGradient(0,0,0,300); g.addColorStop(0,'#ff8f5a'); g.addColorStop(.5,'#ffc27a'); g.addColorStop(1,'#ffeab8'); ctx.fillStyle=g; ctx.fillRect(0,0,800,400);
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
  },true);
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
  },true);
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
  let gg=ctx.createLinearGradient(0,296,0,400); gg.addColorStop(0,'#7cc243'); gg.addColorStop(1,'#4f8f2a'); ctx.fillStyle=gg; ctx.fillRect(0,296,800,110);
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
 
 
// ---------- Zombie: vẽ 1 lần vào sprite rồi dán lại (giảm lag khi đông) ----------
const SW=110, SH=140, AX=50, AY=128;
const SKINS={ICE:['#8fdcff','#4fa9d6','#d3f3ff'],GOLD:['#ffd54a','#c79a12','#fff0a0'],PURPLE:['#b57bff','#7a45c9','#dcc2ff'],PINK:['#ff8fb8','#d05a86','#ffc9de'],RED:['#ff7a6b','#c4443a','#ffb3a9']};
function zombieRaw(z,near,mode){
  const v=(z.variant||0)%3, ninja=mode==='N', out=ninja?'NINJA':equippedOutfit;
  let skin='#8cc63f', skinD='#5f9a25', skinL='#b7e35a';
  if(!ninja && SKINS[equippedSkin]) [skin,skinD,skinL]=SKINS[equippedSkin];
  const mummy=out==='MUMMY'; if(mummy){ skin='#d8ccb4'; skinD='#b9ab90'; skinL='#efe6d2'; }
  const iris=['#7b3fd1','#2f8fe0','#ff8a1f'][v];
  let shirt=['#3c5a9a','#8e3b7e','#c9a45a'][v], pant=['#4b5873','#5b4636','#6b6f3a'][v];
  if(out==='HERO'){ shirt='#1e5bd6'; pant='#1746a8'; } else if(out==='PIRATE'){ shirt='#f2f2f2'; pant='#5b4636'; }
  else if(out==='CLOWN'){ shirt='#ffeb3b'; pant='#e91e63'; } else if(ninja){ shirt='#17171d'; pant='#17171d'; } else if(mummy){ shirt='#efe6d2'; pant='#e6dcc6'; }
  const limb = ninja ? '#17171d' : null;
  const s=Math.sin(z.legAngle), air=!z.isGrounded, bob=air?0:Math.abs(s)*2;
  ctx.save(); ctx.scale(1.2,1.2);
  if(out==='HERO'){ ctx.fillStyle='#d32f2f'; ctx.beginPath(); ctx.moveTo(-6,-33); ctx.quadraticCurveTo(-28-Math.abs(s)*4,-24,-34-Math.abs(s)*5,-8-(air?6:0)); ctx.lineTo(-8,-14); ctx.closePath(); ctx.fill(); }
  ctx.fillStyle='rgba(0,0,0,.3)'; ctx.beginPath(); ctx.ellipse(0,1,15,4,0,0,7); ctx.fill();
  const leg=(p,col)=>{ const fx=air?p*7:p*10, fy=air?-5:-2-Math.max(0,p)*5;
    ctx.strokeStyle=limb||col; ctx.lineWidth=6; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(0,-14); ctx.lineTo(fx,fy); ctx.stroke();
    ctx.fillStyle=ninja?'#0b0b10':(mummy?skinD:'#4a3a2a'); ctx.beginPath(); ctx.ellipse(fx+3,fy+1,5,3,0,0,7); ctx.fill(); };
  leg(-s,skinD); leg(s,skin);
  ctx.fillStyle=pant; ctx.fillRect(-8,-21,16,9);
  ctx.fillStyle=shirt; ctx.beginPath(); ctx.moveTo(-9,-33); ctx.quadraticCurveTo(0,-37,9,-33); ctx.lineTo(10,-19); ctx.lineTo(6,-17); ctx.lineTo(3,-20); ctx.lineTo(-1,-16); ctx.lineTo(-5,-19); ctx.lineTo(-10,-17); ctx.closePath(); ctx.fill();
  if(out==='PIRATE'){ ctx.fillStyle='#d32f2f'; for(let y=-31;y<-19;y+=5) ctx.fillRect(-9,y,19,2.5); ctx.fillStyle='#111'; ctx.fillRect(-9,-21,19,3); ctx.fillStyle='#ffd54f'; ctx.fillRect(-2,-21,4,3); }
  else if(out==='HERO'){ ctx.fillStyle='#ffd54f'; ctx.fillRect(-9,-21,19,3); ctx.beginPath(); ctx.arc(0,-27,3.6,0,7); ctx.fill(); }
  else if(out==='CLOWN'){ ctx.fillStyle='#e53935'; [[-4,-28],[4,-26],[-2,-22],[6,-22]].forEach(([a,b])=>{ ctx.beginPath(); ctx.arc(a,b,2,0,7); ctx.fill(); }); ['#e53935','#fdd835','#1e88e5','#43a047','#fff'].forEach((c,i)=>{ ctx.fillStyle=c; ctx.beginPath(); ctx.arc(-8+i*4.5,-33,2.6,0,7); ctx.fill(); }); }
  else if(ninja){ ctx.fillStyle='#e53935'; ctx.fillRect(-9,-22,19,3); }
  else if(mummy){ ctx.strokeStyle='rgba(120,100,70,.7)'; ctx.lineWidth=1.5; for(let y=-30;y<-18;y+=4){ ctx.beginPath(); ctx.moveTo(-9,y); ctx.lineTo(10,y-3); ctx.stroke(); } }
  const arm=(ay,ph,col)=>{ const hy=ay+3+ph*2; ctx.strokeStyle=limb||col; ctx.lineWidth=5; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(3,ay); ctx.lineTo(19,hy); ctx.stroke();
    if(out==='PIRATE' && col===skinD){ ctx.strokeStyle='#cfd8dc'; ctx.lineWidth=3; ctx.beginPath(); ctx.arc(21,hy-1,4,Math.PI*.6,Math.PI*2.1); ctx.stroke(); }
    else { ctx.fillStyle=ninja?'#0b0b10':col; ctx.beginPath(); ctx.arc(20,hy,3.5,0,7); ctx.fill(); } };
  arm(-29,-s,skinD); arm(-26,s,skin);
  ctx.save(); ctx.translate(3,-44-bob); ctx.rotate(.1);
  if(out==='CLOWN'){ ctx.fillStyle='#ff7043'; ctx.beginPath(); ctx.arc(-16,-6,8,0,7); ctx.arc(-15,8,7,0,7); ctx.arc(-6,-17,7,0,7); ctx.fill(); }
  ctx.fillStyle=mummy?skinD:'#7a9a8a'; ctx.beginPath(); ctx.ellipse(-14,2,6,8,0,0,7); ctx.fill();
  let hg=ctx.createRadialGradient(-4,-8,3,0,0,22); hg.addColorStop(0,skinL); hg.addColorStop(1,skin);
  ctx.fillStyle=hg; ctx.strokeStyle=skinD; ctx.lineWidth=1.5; ctx.beginPath(); ctx.ellipse(0,0,19,17,0,0,7); ctx.fill(); ctx.stroke();
  ctx.fillStyle=skin; ctx.beginPath(); ctx.ellipse(10,9,10,7,0,0,7); ctx.fill();
  if(ninja){ ctx.fillStyle='#14141a'; ctx.beginPath(); ctx.ellipse(0,0,19.5,17.5,0,0,7); ctx.fill(); ctx.beginPath(); ctx.ellipse(10,9,10.5,7.5,0,0,7); ctx.fill(); }
  if(mummy){ ctx.strokeStyle='rgba(120,100,70,.7)'; ctx.lineWidth=2; for(let i=-2;i<3;i++){ ctx.beginPath(); ctx.moveTo(-16,i*6+2); ctx.lineTo(16,i*6-4); ctx.stroke(); } }
  ctx.fillStyle='#fff'; ctx.strokeStyle=ninja?'#000':skinD; ctx.lineWidth=1.5; ctx.beginPath(); ctx.arc(7,-3,10.5,0,7); ctx.fill(); ctx.stroke();
  ctx.fillStyle=(mummy||ninja)?'#e53935':iris; ctx.beginPath(); ctx.arc(9.5,-2.5,6.2,0,7); ctx.fill();
  ctx.fillStyle='#000'; ctx.beginPath(); ctx.arc(10.5,-2.5,3,0,7); ctx.fill();
  ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(8.5,-5,1.8,0,7); ctx.fill();
  ctx.strokeStyle=ninja?'#000':skinD; ctx.lineWidth=3.5; ctx.beginPath(); ctx.moveTo(-3,-12); ctx.lineTo(16,-8); ctx.stroke();
  if(ninja){
    ctx.fillStyle='#e53935'; ctx.fillRect(-19,-13,38,6);
    ctx.fillStyle='#e53935'; ctx.beginPath(); ctx.moveTo(-18,-12); ctx.quadraticCurveTo(-30,-14-Math.abs(s)*4,-38,-6+s*5); ctx.lineTo(-37,-1+s*5); ctx.quadraticCurveTo(-28,-8,-17,-7); ctx.fill();
  } else if(near){
    ctx.fillStyle='#3a0d12'; ctx.beginPath(); ctx.ellipse(12,10,9,7,0,0,7); ctx.fill();
    ctx.fillStyle='#e88'; ctx.beginPath(); ctx.ellipse(12,13,5,3,0,0,7); ctx.fill();
    ctx.fillStyle='#fff'; ctx.beginPath(); ctx.moveTo(5,5); ctx.lineTo(8,11); ctx.lineTo(11,5); ctx.moveTo(13,5); ctx.lineTo(16,11); ctx.lineTo(19,5); ctx.fill();
  } else {
    ctx.strokeStyle='#2c5a14'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(4,11); ctx.quadraticCurveTo(12,15,19,9); ctx.stroke();
    ctx.fillStyle='#fff'; ctx.beginPath(); ctx.moveTo(8,12); ctx.lineTo(10,16); ctx.lineTo(12,12); ctx.moveTo(14,12); ctx.lineTo(16,15.5); ctx.lineTo(18,11); ctx.fill();
  }
  if(out==='CLOWN'){ ctx.fillStyle='#e53935'; ctx.beginPath(); ctx.arc(15,5,4.6,0,7); ctx.fill(); }
  if(out==='PIRATE'){ ctx.strokeStyle='#111'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.moveTo(-17,-8); ctx.lineTo(17,-14); ctx.stroke(); }
  ctx.restore();
  const hy=-44-bob-15;
  if(!ninja){
    if(equippedHat==='HAT'){ ctx.fillStyle='#6d4c2f'; ctx.beginPath(); ctx.ellipse(3,hy+4,24,5,0,0,7); ctx.fill(); ctx.fillStyle='#8d6238'; ctx.beginPath(); ctx.moveTo(-7,hy+3); ctx.quadraticCurveTo(-5,hy-14,3,hy-12); ctx.quadraticCurveTo(11,hy-14,13,hy+3); ctx.fill(); ctx.fillStyle='#c62828'; ctx.fillRect(-7,hy-2,20,3); }
    else if(equippedHat==='PUMPKIN'){ ctx.fillStyle='#ff7a00'; ctx.beginPath(); ctx.ellipse(3,hy-2,17,13,0,0,7); ctx.fill(); ctx.strokeStyle='#c45500'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.ellipse(3,hy-2,8,13,0,0,7); ctx.stroke(); ctx.fillStyle='#2e6b1a'; ctx.fillRect(1,hy-18,4,7); }
    else if(equippedHat==='CROWN'){ ctx.fillStyle='#ffd700'; ctx.strokeStyle='#b8860b'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(-9,hy+6); ctx.lineTo(-9,hy-6); ctx.lineTo(-4,hy); ctx.lineTo(3,hy-9); ctx.lineTo(10,hy); ctx.lineTo(15,hy-6); ctx.lineTo(15,hy+6); ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.fillStyle='#e53935'; ctx.beginPath(); ctx.arc(3,hy+1,2.4,0,7); ctx.fill(); ctx.fillStyle='#2196f3'; ctx.beginPath(); ctx.arc(-5,hy+2,1.8,0,7); ctx.arc(11,hy+2,1.8,0,7); ctx.fill(); }
    else if(equippedHat==='SANTA'){ ctx.fillStyle='#d32f2f'; ctx.beginPath(); ctx.moveTo(-12,hy+6); ctx.quadraticCurveTo(0,hy-30,20,hy-4); ctx.lineTo(16,hy+6); ctx.closePath(); ctx.fill(); ctx.fillStyle='#fff'; ctx.fillRect(-14,hy+2,32,7); ctx.beginPath(); ctx.arc(21,hy-4,5,0,7); ctx.fill(); }
    else if(equippedHat==='PARTY'){ ctx.fillStyle='#ab47bc'; ctx.beginPath(); ctx.moveTo(-8,hy+6); ctx.lineTo(14,hy+6); ctx.lineTo(3,hy-26); ctx.closePath(); ctx.fill(); ctx.strokeStyle='#ffeb3b'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(-3,hy-2); ctx.lineTo(9,hy-8); ctx.moveTo(-6,hy+3); ctx.lineTo(12,hy-4); ctx.stroke(); ctx.fillStyle='#ffeb3b'; ctx.beginPath(); ctx.arc(3,hy-27,3.5,0,7); ctx.fill(); }
    else if(equippedHat==='WITCH'){ ctx.fillStyle='#1f1330'; ctx.beginPath(); ctx.ellipse(3,hy+5,25,5,0,0,7); ctx.fill(); ctx.beginPath(); ctx.moveTo(-8,hy+5); ctx.quadraticCurveTo(0,hy-14,10,hy-32); ctx.quadraticCurveTo(12,hy-12,15,hy+5); ctx.closePath(); ctx.fill(); ctx.fillStyle='#7b1fa2'; ctx.fillRect(-8,hy-2,23,5); ctx.fillStyle='#ffd54f'; ctx.fillRect(1,hy-3,6,7); }
  }
  ctx.restore();
}
function zombieSprite(v,fi,near,mode){
  const key=v+'|'+fi+'|'+(near?1:0)+'|'+mode+'|'+equippedOutfit+'|'+equippedHat+'|'+equippedSkin;
  let c=spriteCache[key]; if(c) return c;
  c=document.createElement('canvas'); c.width=SW; c.height=SH;
  const o=c.getContext('2d'), saved=ctx; ctx=o; ctx.translate(AX,AY);
  try{ zombieRaw({variant:v,legAngle:fi<12?fi*Math.PI*2/12:0,isGrounded:fi<12},near,mode); } finally { ctx=saved; }
  spriteCache[key]=c; return c;
}
function drawZombie(z,scale=1,ox=0,oy=0){
  let fi=12;
  if(z.isGrounded){ const a=((z.legAngle%(Math.PI*2))+Math.PI*2)%(Math.PI*2); fi=Math.floor(a/(Math.PI*2)*12)%12; }
  let near=false; for(let i=0;i<humanXs.length;i++){ const d=humanXs[i]-z.x; if(d>0&&d<110){ near=true; break; } }
  const sp=zombieSprite((z.variant||0)%3,fi,near,ninjaActive?'N':'');
  ctx.drawImage(sp,z.x+ox-AX*scale,z.y+19+oy-AY*scale,SW*scale,SH*scale);
}
 
function drawLion(){
  const z0=zombies[0]; if(!z0) return;
  const n=Math.min(zombies.length,14), t=frame*.2;
  for(let i=n-1;i>=0;i--){
    const z=zombies[Math.floor(i*(zombies.length-1)/Math.max(1,n-1))], x=z.x, y=z.y+19, w=30, wob=Math.sin(t+i*.8)*3;
    ctx.fillStyle=i%2?'#d32f2f':'#ffb300'; ctx.beginPath(); ctx.roundRect(x-w/2,y-54+wob,w,48,8); ctx.fill();
    ctx.strokeStyle='#7f0000'; ctx.lineWidth=2; ctx.stroke();
    ctx.fillStyle=i%2?'#ffd54f':'#c62828'; ctx.fillRect(x-w/2+4,y-42+wob,w-8,5); ctx.beginPath(); ctx.arc(x,y-26+wob,5,0,7); ctx.fill();
  }
  const tl=zombies[zombies.length-1]; ctx.fillStyle='#ffb300';
  for(let i=0;i<4;i++){ ctx.beginPath(); ctx.arc(tl.x-24-i*4,tl.y-16-Math.sin(t+i)*6-i*3,8-i,0,7); ctx.fill(); }
  const hx=z0.x+36, hy=z0.y-40+Math.sin(t)*3, jaw=(Math.sin(t*1.5)+1)*5;
  ctx.fillStyle='#ffb300'; for(let a=0;a<14;a++){ ctx.beginPath(); ctx.arc(hx+Math.cos(a*.45+.4)*42,hy+Math.sin(a*.45+.4)*38,9,0,7); ctx.fill(); }
  ctx.fillStyle='#d32f2f'; ctx.strokeStyle='#ffd54f'; ctx.lineWidth=4; ctx.beginPath(); ctx.ellipse(hx,hy,42,36,0,0,7); ctx.fill(); ctx.stroke();
  ctx.fillStyle='#fff'; ctx.strokeStyle='#d32f2f'; ctx.lineWidth=3; [[-30,-34],[30,-34]].forEach(([dx,dy])=>{ ctx.beginPath(); ctx.arc(hx+dx,hy+dy,9,0,7); ctx.fill(); ctx.stroke(); });
  ctx.fillStyle='#ffd54f'; ctx.beginPath(); ctx.moveTo(hx-6,hy-34); ctx.lineTo(hx,hy-54); ctx.lineTo(hx+6,hy-34); ctx.fill();
  const blink=Math.floor(frame/90)%7===0;
  [[-15,-10],[15,-10]].forEach(([dx,dy])=>{ if(blink){ ctx.strokeStyle='#000'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(hx+dx-9,hy+dy); ctx.lineTo(hx+dx+9,hy+dy); ctx.stroke(); }
    else { ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(hx+dx,hy+dy,11,0,7); ctx.fill(); ctx.fillStyle='#000'; ctx.beginPath(); ctx.arc(hx+dx+3,hy+dy,5.5,0,7); ctx.fill(); ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(hx+dx+1,hy+dy-2,1.8,0,7); ctx.fill(); } });
  ctx.fillStyle='#ffd54f'; ctx.beginPath(); ctx.arc(hx,hy+4,6,0,7); ctx.fill();
  ctx.fillStyle='#3a0000'; ctx.beginPath(); ctx.ellipse(hx,hy+20+jaw/2,25,9+jaw,0,0,7); ctx.fill();
  ctx.fillStyle='#fff'; for(let i=-2;i<=2;i++){ ctx.beginPath(); ctx.moveTo(hx+i*9-4,hy+14); ctx.lineTo(hx+i*9,hy+21); ctx.lineTo(hx+i*9+4,hy+14); ctx.fill(); }
  ctx.fillStyle='#ff7a9a'; ctx.beginPath(); ctx.ellipse(hx,hy+26+jaw,12,5,0,0,7); ctx.fill();
  ctx.fillStyle='#fff'; for(let i=-2;i<=2;i++){ ctx.beginPath(); ctx.arc(hx+i*9,hy+36+jaw,7,0,7); ctx.fill(); }
}
function drawSlashes(){
  slashes.forEach(s => { const a=s.life/14; ctx.strokeStyle='rgba(255,255,255,'+a+')'; ctx.lineWidth=5*a; ctx.lineCap='round';
    const r=38*(1.2-a*.3); ctx.beginPath(); ctx.arc(s.x,s.y,r,-2.3,-.6); ctx.stroke(); ctx.beginPath(); ctx.arc(s.x,s.y,r,.8,2.5); ctx.stroke(); });
}
 
function drawMenuScene(){
  humanXs=[]; const base=defaultGroundY-20;
  [{x:340,g:'MALE'},{x:400,g:'FEMALE'}].forEach(o => drawHuman({x:o.x+Math.sin(frame*.05)*4,y:base,gender:o.g,panic:true,step:frame*.35}));
  for(let i=5;i>=0;i--) drawZombie({x:230-i*30+(i%2)*10,y:base,legAngle:frame*.22+i*.9,variant:i%3,isGrounded:true},1-i*.02,0,(i%2)?-4:0);
}
 
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
  ctx.fillStyle='rgba(0,0,0,.55)'; ctx.beginPath(); ctx.roundRect(585,10,150,28,8); ctx.fill();
  ctx.fillStyle='#80d8ff'; ctx.font='bold 14px sans-serif'; ctx.textAlign='center'; ctx.fillText(MAP_NAMES[currentMap],660,29);
  ctx.fillStyle='rgba(0,0,0,.75)'; ctx.beginPath(); ctx.roundRect(752,0,48,48,[0,0,0,14]); ctx.fill();
  ctx.fillStyle='#fff'; ctx.fillRect(767,12,7,24); ctx.fillRect(780,12,7,24);
  let bx=170; const full=bonusDur();
  [['🌊','#00e5ff',tsunamiActive?tsunamiTimer:0],['👹','#e040fb',giantActive?giantTimer:0],['🥷','#b388ff',ninjaActive?ninjaTimer:0],['🦁','#ffb300',lionActive?lionTimer:0],['🛡️','#40c4ff',buffs.shield]].forEach(([ic,col,t]) => {
    if(t>0){ ctx.font='16px sans-serif'; ctx.textAlign='left'; ctx.fillStyle='#fff'; ctx.fillText(ic,bx,24);
      ctx.fillStyle='rgba(0,0,0,.55)'; ctx.fillRect(bx+24,12,70,12); ctx.fillStyle=col; ctx.fillRect(bx+25,13,68*Math.min(1,t/full),10); bx+=112; }
  });
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
  if(banner.life>0){ banner.life--; ctx.globalAlpha=Math.min(1,banner.life/20); outText(banner.t,400,140-(80-banner.life)*.3,34,'#ffffff','center'); ctx.globalAlpha=1; }
  if(paused){
    ctx.fillStyle='rgba(0,0,0,.6)'; ctx.fillRect(0,0,800,450);
    outText('PAUSED',400,215,54,'#76ba1b','center');
    outText('Nhấn P / chạm để tiếp tục',400,255,18,'#fff','center');
  }
}
 
const D={BOMB:drawBomb,CAR:drawCar,BUS:drawBus,HELI:drawHelicopter,SPIKE:drawSpike,SPRING:drawSpring,WALL:drawWall};
function draw(){
  humanXs=humans.map(h=>h.x);
  drawBackground();
  if(gameState==='MENU'){ drawMenuScene(); ctx.restore(); return; }
  coinTrails.forEach(drawCoin); powerups.forEach(drawMysteryBox); humans.forEach(drawHuman);
  obstacles.forEach(o => D[o.type](o)); bullets.forEach(drawBullet);
  if(giantActive) drawGiantMonster();
  else {
    for(let i=zombies.length-1;i>=0;i--) drawZombie(zombies[i],1-Math.min(i*.012,.25),(i%3===2)?-6:0,(i%2===1)?-Math.min(i*1.8,18):0);
    if(lionActive) drawLion();
  }
  if(buffs.shield>0 && zombies[0] && !(buffs.shield<90 && Math.floor(frame/6)%2)){
    const cx=zombies[0].x-Math.min(zombies.length*4,60), rx=50+Math.min(zombies.length*5,110);
    ctx.fillStyle='rgba(80,200,255,.15)'; ctx.strokeStyle='rgba(120,220,255,.85)'; ctx.lineWidth=3;
    ctx.beginPath(); ctx.ellipse(cx,groundRef-32,rx,62,0,0,7); ctx.fill(); ctx.stroke();
  }
  drawSlashes();
  for(let i=0;i<particles.length;i++){ const p=particles[i]; ctx.fillStyle=p.color; ctx.fillRect(p.x,p.y,4,4); }
  ctx.restore();
  drawHUD();
  if(fade>0){ ctx.fillStyle='rgba(0,0,0,'+fade+')'; ctx.fillRect(0,0,800,450); fade=Math.max(0,fade-.05); }
  if(gameState==='GAMEOVER'){
    ctx.fillStyle='rgba(0,0,0,.85)'; ctx.fillRect(0,0,800,450);
    ctx.textAlign='center';
    ctx.fillStyle='#ff1744'; ctx.font='bold 42px sans-serif'; ctx.fillText('GAME OVER',400,160);
    ctx.fillStyle='#fff'; ctx.font='22px sans-serif';
    ctx.fillText('Số người nuốt chửng: '+score,400,210);
    ctx.fillText('Quãng đường: '+Math.floor(distance)+' m',400,240);
    ctx.fillText('Xu thu thập được: 🪙 +'+currentCoins,400,270);
    ctx.fillText('Nhấn Space / Chạm để quay về Menu',400,315);
  }
}
 
function loop(){ update(); draw(); requestAnimationFrame(loop); }
initTerrain(); saveUserData();
loop();
 
</script>
</body>
</html>
"""
 
html_doc = game_code.strip().replace("__MUSIC_SRC__", music_uri)
try:
    # Streamlit mới (>= 1.56): components.html đã bị deprecated -> dùng st.iframe
    st.iframe(html_doc, height=480)
except Exception:
    # Streamlit cũ: dùng components.html
    import streamlit.components.v1 as components
    components.html(html_doc, height=480, scrolling=False
 
