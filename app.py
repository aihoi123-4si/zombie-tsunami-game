.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:12px}
.hidden{display:none!important}.small{font-size:13px;color:#c5d5dd}
#toast{position:absolute;bottom:12px;left:50%;transform:translateX(-50%);background:#111e;color:#fff;padding:8px 12px;border-radius:8px;display:none;font-weight:bold}
@media(max-width:600px){.panel{padding:12px}.grid{grid-template-columns:1fr}button{padding:9px 12px}}
</style></head><body>
<div id="wrap">
<canvas id="game" width="960" height="540" aria-label="Zombie Tsunami game"></canvas>
<div id="hud"><div class="pill">🪙 <span id="coins">0</span><br>🧠 <span id="count">1</span></div><div class="pill">SCORE <span id="score">0</span><br>BEST <span id="best">0</span></div></div>
<div id="overlay"><div class="panel" id="mainPanel">
<div class="logo">ZOMBIE</div><div class="sub">TSUNAMI</div>
<p>Chạy thật xa, ăn người để tạo thành đàn zombie, lật xe buýt, nhặt xu và né hố cùng bom!</p>
<div><button id="play">▶ CHƠI NGAY</button></div>
<div class="grid"><button class="secondary" id="missions">📜 NHIỆM VỤ</button><button class="secondary" id="shop">🛒 CỬA HÀNG</button></div>
<p class="small">SPACE / ↑ / chạm để nhảy · P để tạm dừng<br>Hộp bí ẩn: sóng thần, khổng lồ, nam châm hoặc xu x2</p>
</div></div><div id="toast"></div></div>
<script>
(()=> {
const canvas=document.getElementById('game'), c=canvas.getContext('2d');
const $=id=>document.getElementById(id), overlay=$('overlay');
const W=canvas.width,H=canvas.height,ground=405;
let state='menu',frame=0,score=0,runCoins=0,speed=5,world=0,shake=0;
let coins=+(localStorage.ztCoins||0),best=+(localStorage.ztBest||0),totalEaten=+(localStorage.ztEaten||0),bestRun=+(localStorage.ztRun||0);
let owned=JSON.parse(localStorage.ztOwned||'[]'), outfit=localStorage.ztOutfit||'normal',hat=localStorage.ztHat||'none';
let zombies=[],people=[],obstacles=[],holes=[],coinItems=[],boxes=[],particles=[];
let power='none',powerTimer=0,spawnTimer=0,paused=false,combo=0,comboTimer=0,runMultiplier=1;
$('coins').textContent=coins;$('best').textContent=best;
function save(){localStorage.ztCoins=coins;localStorage.ztBest=best;localStorage.ztEaten=totalEaten;localStorage.ztRun=bestRun;localStorage.ztOwned=JSON.stringify(owned);localStorage.ztOutfit=outfit;localStorage.ztHat=hat;$('coins').textContent=coins;$('best').textContent=best}
function toast(t){let el=$('toast');el.textContent=t;el.style.display='block';setTimeout(()=>el.style.display='none',1600)}
function rand(a,b){return a+Math.random()*(b-a)}
function reset(){frame=0;score=0;runCoins=0;speed=5;world=0;power='none';powerTimer=0;spawnTimer=0;paused=false;zombies=[{x:180,y:ground-22,vy:0,grounded:true,phase:0,v:0}];people=[];obstacles=[];holes=[];coinItems=[];boxes=[];particles=[]}
function start(){reset();state='play';overlay.classList.add('hidden')}
function end(){state='over';best=Math.max(best,score);bestRun=Math.max(bestRun,score);save();showPanel('over')}
function showPanel(kind){
 overlay.classList.remove('hidden');
 const panel=$('mainPanel');
 if(kind==='over'){panel.innerHTML=`<div class="logo">GAME OVER</div><div class="sub">${score} NGƯỜI ĐÃ ĂN</div><p>Xu nhặt được: 🪙 ${runCoins}<br>Số zombie còn lại: ${zombies.length}</p><button id="again">↻ CHƠI LẠI</button><button class="secondary" id="home">⌂ MENU</button>`;$('again').onclick=start;$('home').onclick=()=>showPanel('menu')}
 else if(kind==='pause'){panel.innerHTML=`<div class="logo">TẠM DỪNG</div><button id="resume">▶ TIẾP TỤC</button><button class="secondary" id="home">⌂ MENU</button>`;$('resume').onclick=()=>{paused=false;overlay.classList.add('hidden')};$('home').onclick=()=>showPanel('menu')}
 else if(kind==='menu'){panel.innerHTML=`<div class="logo">ZOMBIE</div><div class="sub">TSUNAMI</div><p>Chạy thật xa, ăn người để tạo thành đàn zombie, lật xe buýt, nhặt xu và né hố cùng bom!</p><button id="play2">▶ CHƠI NGAY</button><div class="grid"><button class="secondary" id="missions2">📜 NHIỆM VỤ</button><button class="secondary" id="shop2">🛒 CỬA HÀNG</button></div><p class="small">SPACE / ↑ / chạm để nhảy · P để tạm dừng<br>Hộp bí ẩn có 4 sức mạnh đặc biệt</p>`;$('play2').onclick=start;$('missions2').onclick=()=>showPanel('missions');$('shop2').onclick=()=>showPanel('shop')}
 else if(kind==='missions'){panel.innerHTML=`<div class="logo">NHIỆM VỤ</div><p>🧟 Ăn tổng cộng 100 người: <b>${Math.min(totalEaten,100)}/100</b></p><button id="claim1" ${totalEaten<100||localStorage.ztM1?'disabled':''}>${localStorage.ztM1?'ĐÃ NHẬN':'Nhận 100 xu'}</button><p>🧠 Ăn 10 người trong một lượt: <b>${Math.min(bestRun,10)}/10</b></p><button id="claim2" ${bestRun<10||localStorage.ztM2?'disabled':''}>${localStorage.ztM2?'ĐÃ NHẬN':'Nhận 50 xu'}</button><br><button class="secondary" id="back">← QUAY LẠI</button>`;$('claim1').onclick=()=>{coins+=100;localStorage.ztM1='1';save();showPanel('missions')};$('claim2').onclick=()=>{coins+=50;localStorage.ztM2='1';save();showPanel('missions')};$('back').onclick=()=>showPanel('menu')}
 else if(kind==='shop'){panel.innerHTML=`<div class="logo">CỬA HÀNG</div><p>Xu hiện có: 🪙 <b>${coins}</b></p><div class="grid"><button id="mummy">🩹 Xác ướp · ${owned.includes('mummy')?'Đã sở hữu':'300 xu'}</button><button id="cowboy">🤠 Mũ cao bồi · ${owned.includes('cowboy')?'Đã sở hữu':'200 xu'}</button><button id="pumpkin">🎃 Đầu bí ngô · ${owned.includes('pumpkin')?'Đã sở hữu':'200 xu'}</button><button id="normal" class="secondary">Mặc mặc định</button></div><button class="secondary" id="back">← QUAY LẠI</button>`;[['mummy',300],['cowboy',200],['pumpkin',200]].forEach(([id,cost])=>$(id).onclick=()=>{if(!owned.includes(id)){if(coins<cost){toast('Bạn không đủ xu!');return}coins-=cost;owned.push(id)}if(id==='mummy')outfit='mummy';else hat=id;save();showPanel('shop')});$('normal').onclick=()=>{outfit='normal';hat='none';save();showPanel('shop')};$('back').onclick=()=>showPanel('menu')}
}
$('play').onclick=start;$('missions').onclick=()=>showPanel('missions');$('shop').onclick=()=>showPanel('shop');
function jump(){if(state!=='play')return;if(paused)return;let lead=zombies[0];if(lead&&lead.grounded){zombies.forEach((z,i)=>{if(z.grounded){z.vy=-14.5-i*.025;z.grounded=false}})}}
window.addEventListener('keydown',e=>{if(e.code==='Space'||e.code==='ArrowUp'){e.preventDefault();if(state==='menu'||state==='over')start();else jump()}if(e.key.toLowerCase()==='p'&&state==='play'){paused=!paused;if(paused)showPanel('pause');else overlay.classList.add('hidden')}});
canvas.addEventListener('pointerdown',()=>{if(state==='play')jump()});
function particle(x,y,color,n=10){for(let i=0;i<n;i++)particles.push({x,y,vx:rand(-4,4),vy:rand(-5,2),life:25,color})}
function spawn(){
 if(frame%125===0){let r=Math.random();if(r<.43){let n=1+Math.floor(Math.random()*3);for(let j=0;j<n;j++)people.push({x:1000+j*30,y:ground-20,shirt:['#e84a5f','#3478db','#f0a12d'][Math.floor(Math.random()*3)],eaten:false})}else if(r<.68)obstacles.push({x:1000,y:ground-44,w:90,h:44,type:'car',need:3,inside:3});else if(r<.86)obstacles.push({x:1000,y:ground-57,w:130,h:57,type:'bus',need:5,inside:6});else obstacles.push({x:1000,y:ground-32,w:38,h:32,type:'bomb'})}
 if(frame%255===0&&Math.random()<.75){let x=1000,w=rand(85,140);holes.push({x,w})}
 if(frame%105===0&&Math.random()<.8){let y=ground-rand(40,120);for(let i=0;i<7;i++)coinItems.push({x:1000+i*28,y:y+Math.sin(i*.6)*10})}
 if(frame%430===0)boxes.push({x:1000,y:ground-80,w:42,h:42})
}
function update(){
 if(state!=='play'||paused)return;frame++;world+=speed;speed=5+Math.min(3,frame/1400);spawn();
 if(powerTimer>0){powerTimer--;if(powerTimer===0)power='none'}
 holes.forEach(h=>h.x-=speed);holes=holes.filter(h=>h.x+h.w>0);
 coinItems.forEach(a=>{a.x-=speed;if(power==='magnet'&&zombies.length){let z=zombies[0];let dx=z.x-a.x,dy=z.y-a.y;if(Math.abs(dx)<230&&Math.abs(dy)<180){a.x+=dx*.08;a.y+=dy*.08}}for(let z of zombies){if(Math.abs(z.x-a.x)<24&&Math.abs(z.y-a.y)<34){a.got=true;let value=power==='gold'?2:1;coins+=value;runCoins+=value;particle(a.x,a.y,'#ffdf3e',4);save();break}}});coinItems=coinItems.filter(a=>a.x>-30&&!a.got);
 boxes.forEach(b=>{b.x-=speed;if(!b.got&&Math.abs(b.x-zombies[0].x)<35&&Math.abs(b.y-zombies[0].y)<45){b.got=true;let kinds=['wave','giant','magnet','gold'];power=kinds[Math.floor(Math.random()*kinds.length)];powerTimer=power==='gold'?360:300;particle(b.x,b.y,'#5de6ff',30);toast(({wave:'SÓNG THẦN!',giant:'ZOMBIE KHỔNG LỒ!',magnet:'NAM CHÂM HÚT XU!',gold:'NHÂN ĐÔI XU!'})[power])}});boxes=boxes.filter(b=>b.x>-50&&!b.got);
 let lead=zombies[0];let invincible=power!=='none';
 obstacles.forEach(o=>{o.x-=speed;if(o.type==='bomb'){if(Math.abs(o.x-lead.x)<50&&Math.abs(o.y-lead.y)<65){if(invincible){o.dead=true;particle(o.x,o.y,'#ff713d',25)}else{let gone=zombies.pop();if(gone)particle(gone.x,gone.y,'#9be23c',12);o.dead=true;if(!zombies.length)end()}}}else if(!o.dead&&lead.x+18>o.x&&lead.x<o.x+o.w&&lead.y>o.y-22){if(invincible||zombies.length>=o.need){o.dead=true;score+=o.inside;totalEaten+=o.inside;coins+=o.inside*5;for(let i=0;i<o.inside&&zombies.length<35;i++){let t=zombies[zombies.length-1];zombies.push({x:t.x-22,y:t.y,vy:0,grounded:true,phase:rand(0,6),v:Math.floor(rand(0,3))})}particle(o.x,o.y,'#ff9d2e',25);save()}else{let gone=zombies.pop();if(gone)particle(gone.x,gone.y,'#9be23c',12);o.dead=true;if(!zombies.length)end()}}});obstacles=obstacles.filter(o=>o.x+o.w>-30&&!o.dead);
 people.forEach(p=>{p.x-=speed;if(!p.eaten&&lead&&Math.abs(lead.x-p.x)<34&&Math.abs(lead.y-p.y)<54){p.eaten=true;score++;totalEaten++;coins+=5;runCoins+=5;if(zombies.length<35){let t=zombies[zombies.length-1];zombies.push({x:t.x-22,y:t.y,vy:0,grounded:true,phase:rand(0,6),v:Math.floor(rand(0,3))})}particle(p.x,p.y,'#9be23c',12);save()}});
 people=people.filter(p=>p.x>-50&&!p.eaten);
 zombies.forEach((z,i)=>{z.phase+=.22;z.x=180-i*21;if(power==='wave'){z.y=ground-95+Math.sin(frame*.15+i*.4)*7;z.vy=0;z.grounded=true}else if(power==='giant'){z.y=ground-36;z.vy=0;z.grounded=true}else{z.vy+=.65;z.y+=z.vy;let pit=holes.some(h=>z.x+8>h.x&&z.x-8<h.x+h.w);if(!pit&&z.y>=ground-20){z.y=ground-20;z.vy=0;z.grounded=true}else z.grounded=false;if(pit&&z.y>ground+40){z.dead=true}}});
 zombies=zombies.filter(z=>!z.dead);if(!zombies.length){end();return}
 if(zombies[0].y>ground+45){zombies.shift();if(!zombies.length){end();return}}
 particles.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.vy+=.12;p.life--});particles=particles.filter(p=>p.life>0);
 $('score').textContent=score;$('count').textContent=zombies.length;$('coins').textContent=coins;
}
function roundRect(x,y,w,h,r,fill,stroke){c.beginPath();c.roundRect(x,y,w,h,r);if(fill){c.fillStyle=fill;c.fill()}if(stroke){c.strokeStyle=stroke;c.stroke()}}
function background(){
 let g=c.createLinearGradient(0,0,0,ground);g.addColorStop(0,'#56c8ff');g.addColorStop(1,'#d7f6ff');c.fillStyle=g;c.fillRect(0,0,W,H);
 // clouds
 for(let i=0;i<5;i++){let x=((i*230-world*.18)%(W+180)+W+180)%(W+180)-60;c.fillStyle='#ffffffcc';c.beginPath();c.arc(x,75+i%2*35,24,0,7);c.arc(x+28,67+i%2*35,31,0,7);c.arc(x+58,78+i%2*35,23,0,7);c.fill()}
 // skyline
 for(let i=0;i<11;i++){let x=((i*112-world*.38)%(W+130)+W+130)%(W+130)-70,h=100+(i*47%130);c.fillStyle=['#a4b8c7','#849bab','#b8c8d4'][i%3];c.fillRect(x,ground-35-h,76,h);c.fillStyle='#d8e7ee';for(let y=ground-25-h;y<ground-45;y+=20)for(let xx=x+10;xx<x+68;xx+=19)c.fillRect(xx,y,8,10)}
 // brick buildings
 for(let i=0;i<3;i++){let x=((i*380-world*.65)%(W+420)+W+420)%(W+420)-180;c.fillStyle='#9b4f3b';c.fillRect(x,245,210,160);c.fillStyle='#6f332b';c.fillRect(x-5,239,220,12);for(let y=265;y<385;y+=27)for(let xx=x+12;xx<x+195;xx+=31){c.fillStyle='#342f37';c.fillRect(xx,y,18,17);c.fillStyle='#c07858';c.fillRect(xx-2,y-2,22,3)}c.fillStyle='#303e48';c.fillRect(x+135,208,36,32);c.fillStyle='#567b87';c.fillRect(x+143,185,20,24)}
 // road
 c.fillStyle='#303943';c.fillRect(0,ground,W,H-ground);c.fillStyle='#1e272e';c.fillRect(0,ground,W,12);c.fillStyle='#f8d34c';for(let x=-(world%85);x<W;x+=85)c.fillRect(x,ground+76,43,5);
 // holes cut visual
 holes.forEach(h=>{c.fillStyle='#07111b';c.fillRect(h.x,ground,h.w,H-ground);c.fillStyle='#596b75';c.fillRect(h.x-5,ground,h.w+10,7)})
}
function drawZombie(z,i){
 c.save();c.translate(z.x,z.y);let scale=1-Math.min(i*.008,.18);c.scale(scale,scale);
 let colors=['#263746','#cf3d49','#edbd28'];let pants=['#493a2e','#6c315b','#38652b'];let shirt=colors[z.v||0];
 if(outfit==='mummy'){c.strokeStyle='#e7ded1';c.lineWidth=5;c.beginPath();c.moveTo(-5,5);c.lineTo(-8+Math.sin(z.phase)*7,19);c.moveTo(5,5);c.lineTo(8-Math.sin(z.phase)*7,19);c.stroke();c.fillStyle='#e8dfd4';c.fillRect(-10,-8,20,17);c.beginPath();c.arc(0,-19,17,0,7);c.fill();c.strokeStyle='#c6b9aa';c.lineWidth=2;for(let j=-2;j<3;j++) {c.beginPath();c.moveTo(-12,-23+j*5);c.lineTo(12,-20+j*5);c.stroke()}}
 else {c.strokeStyle='#78b92d';c.lineWidth=5;c.beginPath();c.moveTo(-5,7);c.lineTo(-7+Math.sin(z.phase)*8,20);c.moveTo(5,7);c.lineTo(7-Math.sin(z.phase)*8,20);c.stroke();c.fillStyle=pants[z.v||0];c.fillRect(-8,3,16,8);c.fillStyle=shirt;c.fillRect(-10,-8,20,13);c.fillStyle='#79c52b';c.beginPath();c.ellipse(0,-21,20,19,0,0,7);c.fill();c.fillStyle='#4e9c20';c.beginPath();c.arc(-12,-30,7,0,7);c.fill();c.fillStyle='#fff';c.beginPath();c.ellipse(7,-23,10,12,0,0,7);c.fill();c.fillStyle=['#16c8f0','#ffdd32','#d5f7ff'][z.v||0];c.beginPath();c.arc(9,-23,5.8,0,7);c.fill();c.fillStyle='#111';c.beginPath();c.arc(10,-23,2.8,0,7);c.fill();c.fillStyle='#162b17';c.beginPath();c.ellipse(8,-10,7,5,0,0,7);c.fill();c.fillStyle='#fff';c.beginPath();c.moveTo(3,-13);c.lineTo(6,-7);c.lineTo(8,-13);c.fill();c.strokeStyle='#79c52b';c.lineWidth=4;c.beginPath();c.moveTo(4,-5);c.lineTo(17,1);c.stroke()}
 if(hat==='cowboy'){c.fillStyle='#79502d';c.fillRect(-22,-39,44,5);c.fillRect(-12,-51,25,14);c.fillStyle='#e8c27a';c.fillRect(-12,-42,25,3)}else if(hat==='pumpkin'){c.fillStyle='#ff7a12';c.beginPath();c.ellipse(0,-41,13,11,0,0,7);c.fill();c.fillStyle='#287a28';c.fillRect(-2,-54,4,6)}
 c.restore()
}
function draw(){
 background();
 // people
 people.forEach(p=>{c.save();c.translate(p.x,p.y);c.fillStyle='#ffcf9e';c.beginPath();c.arc(0,-16,8,0,7);c.fill();c.fillStyle='#633c2a';c.beginPath();c.arc(0,-19,8,Math.PI,Math.PI*2);c.fill();c.fillStyle=p.shirt;c.fillRect(-7,-8,14,17);c.strokeStyle='#e8c5a1';c.lineWidth=4;c.beginPath();c.moveTo(5,-3);c.lineTo(13,4);c.stroke();c.restore()});
 obstacles.forEach(o=>{if(o.type==='bomb'){c.fillStyle='#1a1a1a';c.beginPath();c.arc(o.x+19,o.y+18,18,0,7);c.fill();c.fillStyle='#ff3b2f';c.beginPath();c.arc(o.x+19,o.y+18,7+Math.sin(frame*.3)*2,0,7);c.fill()}else{c.fillStyle=o.type==='bus'?'#f7bf28':'#e43d32';c.fillRect(o.x,o.y,o.w,o.h-8);c.fillStyle='#9ee6ff';for(let x=o.x+10;x<o.x+o.w-8;x+=26)c.fillRect(x,o.y+6,19,o.h*.35);c.fillStyle='#111';c.beginPath();c.arc(o.x+20,o.y+o.h-5,10,0,7);c.arc(o.x+o.w-20,o.y+o.h-5,10,0,7);c.fill();roundRect(o.x+o.w/2-30,o.y-30,60,24,6,'#101820','#f8d34c');c.fillStyle='#9be23c';c.beginPath();c.arc(o.x+o.w/2-15,o.y-18,8,0,7);c.fill();c.fillStyle='#fff';c.font='bold 15px Arial';c.fillText('/'+o.need,o.x+o.w/2-4,o.y-13)}});
 coinItems.forEach(a=>{c.fillStyle='#f8c62d';c.beginPath();c.arc(a.x,a.y,9,0,7);c.fill();c.strokeStyle='#fff2a4';c.lineWidth=3;c.stroke()});
 boxes.forEach(b=>{c.save();c.translate(b.x,b.y+Math.sin(frame*.1)*4);c.rotate(-.08);roundRect(-b.w/2,-b.h/2,b.w,b.h,5,'#f6f8f9','#344b5b');c.fillStyle='#13aee9';c.font='bold 30px Arial';c.textAlign='center';c.fillText('?',0,10);c.restore()});
 if(power==='wave'){c.fillStyle='#08bde9bb';c.beginPath();c.moveTo(0,ground);c.bezierCurveTo(70,ground-100,125,ground-190,225,ground-145);c.bezierCurveTo(300,ground-110,320,ground-35,365,ground);c.closePath();c.fill()}
 zombies.forEach((z,i)=>drawZombie(z,i));
 if(power==='giant'){c.save();c.translate(190,ground-100);c.fillStyle='#4fba27';c.beginPath();c.arc(0,0,75,0,7);c.fill();for(let i=0;i<4;i++){let a=i*Math.PI/2;c.fillStyle='#fff';c.beginPath();c.arc(Math.cos(a)*35,Math.sin(a)*25-8,17,0,7);c.fill();c.fillStyle='#16bde7';c.beginPath();c.arc(Math.cos(a)*35+3,Math.sin(a)*25-8,8,0,7);c.fill()}c.restore()}
 particles.forEach(p=>{c.globalAlpha=Math.max(0,p.life/25);c.fillStyle=p.color;c.fillRect(p.x,p.y,5,5);c.globalAlpha=1});
 if(state==='menu'){drawZombie({x:250,y:ground-20,phase:frame*.2,v:0},0)}
 if(power!=='none'&&state==='play'){let label=({wave:'SÓNG THẦN',giant:'KHỔNG LỒ',magnet:'NAM CHÂM',gold:'XU x2'})[power]||'';c.fillStyle='#07111bd9';roundRect(390,16,180,32,9,'#07111bd9','#ffffff88');c.fillStyle='#ffe45c';c.font='bold 17px Arial';c.textAlign='center';c.fillText(label+'  '+Math.ceil(powerTimer/60)+'s',480,38)}
 if(state==='play'&&paused){c.fillStyle='#0009';c.fillRect(0,0,W,H);c.fillStyle='#fff';c.font='bold 40px Arial';c.textAlign='center';c.fillText('TẠM DỪNG',W/2,H/2)}
}
function loop(){if(state==='play'&&!paused)update();else if(state==='menu')world+=1.5;draw();requestAnimationFrame(loop)}
reset();loop();showPanel('menu');
})();
</script></body></html>
"""
components.html(game_code, height=650, scrolling=False)

st.markdown("""
---
**Cách chạy trên máy tính**
1. Lưu file này thành `zombie_tsunami.py`.
2. Cài thư viện: `pip install streamlit`
3. Mở Terminal/CMD tại thư mục chứa file và chạy: `streamlit run zombie_tsunami.py`

Đây là bản fan-made lấy cảm hứng từ lối chơi Zombie Tsunami, không phải bản game chính thức.
""")
