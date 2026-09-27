const initialTrades=[
["WIN","LONG","#BNBUSDC","Apr 22, 2025","614.85","0.65","Apr 23, 2025","616.74","$399.652","$1.43","0.36%","REVERSAL"],
["OPEN","LONG","#BTCUSDT","Apr 22, 2025","92990.2","0.004","—","—","$371.961","-$0.07432","-0.02%","REVERSAL"],
["WIN","LONG","#ETHUSDT","Apr 22, 2025","1631.37","2.00","Apr 22, 2025","1654.25","$3,262.74","$43.45","1.33%","REVERSAL"],
["LOSS","SHORT","#ETHUSDC","Apr 22, 2025","1608","5.00","Apr 22, 2025","1622.68","$8,074.41","-$38.99","-0.48%","BREAKOUT"],
["WIN","LONG","#BTCUSDC","Apr 21, 2025","88089.9","0.1","Apr 22, 2025","92188.6","$8,808.99","$405.57","4.60%","REVERSAL"],
["WIN","SHORT","#ETHUSDT","Apr 21, 2025","1619.92","5.00","Apr 21, 2025","1588.91","$8,140.07","$67.33","0.83%","FOMO"],
["LOSS","LONG","#BTCUSDC","Apr 21, 2025","87167.4","0.044","Apr 21, 2025","87260.7","$3,845.81","-$56.34","-0.16%","RSI CROSSED"],
["WIN","SHORT","#ETHUSDC","Apr 21, 2025","1632.53","2.434","Apr 21, 2025","1629.1","$3,998.70","$33.47","0.84%","RSI CROSSED"],
["WIN","LONG","#BTCUSDT","Apr 20, 2025","86674.7","0.3","Apr 21, 2025","87251.1","$26,002.40","$113.58","0.44%","REVERSAL"],
["WIN","LONG","#ETHUSDT","Apr 20, 2025","1611.97","0.826","Apr 21, 2025","1653.97","$1,332.58","$32.25","2.42%","REVERSAL"],
["LOSS","SHORT","#XRPUSDT","Apr 20, 2025","2.0858","3569.5","Apr 20, 2025","2.0695","$7,325.45","-$48.28","-0.66%",""],
["LOSS","SHORT","#BTCUSDT","Apr 20, 2025","84420","0.074","Apr 20, 2025","84825.7","$6,247.08","-$34.41","-0.55%",""],
["WIN","LONG","#ETHUSDT","Apr 20, 2025","1579.52","2.492","Apr 20, 2025","1629.1","$3,940.91","$56.11","1.68%","BREAKOUT"],
["WIN","LONG","#XRPUSDT","Apr 20, 2025","8779.8","2.0432","Apr 20, 2025","2.0589","$17,933.90","$125.22","0.70%",""],
["WIN","LONG","#BTCUSDT","Apr 20, 2025","83996","0.074","Apr 20, 2025","84088.9","$6,215.70","$2.52","0.04%",""],
["LOSS","LONG","#BNBUSDT","Apr 20, 2025","590.33","17.07","Apr 20, 2025","589.49","$10,076.90","-$21.39","-0.21%",""],
["LOSS","LONG","#AVAXUSDT","Apr 20, 2025","19.446","271","Apr 20, 2025","19.307","$5,269.87","-$41.53","-0.79%",""],
["WIN","LONG","#BTCUSDT","Apr 20, 2025","84483.8","0.1","Apr 20, 2025","85123.9","$8,448.38","$60.62","0.72%","BREAKOUT"],
["WIN","LONG","#ETHUSDT","Apr 20, 2025","1590.62","10","Apr 20, 2025","1653.97","$15,906.20","$4.63","0.03%","REVERSAL"],
["LOSS","LONG","#SUIUSDT","Apr 19, 2025","2.139","1889.3","Apr 20, 2025","2.0996","$4,041.13","-$77.13","-1.91%",""]
];

let trades=JSON.parse(localStorage.getItem("tradingJournalTrades")||"null")||initialTrades;
const $=id=>document.getElementById(id);
function render(){
  const body=$("tradeRows"); body.innerHTML="";
  trades.forEach((t,i)=>{
    const [status,side,symbol,od,entry,size,cd,exit,cost,ret,pct,setup,note=""] = t;
    const tr=document.createElement("tr");
    tr.innerHTML=`<td><input type="checkbox"></td><td><span class="badge ${status.toLowerCase()}">${status}</span></td><td><span class="badge ${side.toLowerCase()}">${side}</span></td><td class="symbol">${symbol}</td><td>${od}</td><td>${entry}</td><td>${size}</td><td>${cd}</td><td>${exit}</td><td>${cost}</td><td class="${String(ret).includes("-")?"negative":"positive"}">${ret}</td><td class="${String(pct).includes("-")?"negative":"positive"}">${pct}</td><td>${setup?`<span class="setup">${setup}</span>`:""}</td><td>${note}</td><td></td>`;
    body.appendChild(tr);
  });
  $("tradeCount").textContent=trades.length;
  const wins=trades.filter(t=>t[0]==="WIN").length, losses=trades.filter(t=>t[0]==="LOSS").length;
  $("winPct").textContent=(wins/(wins+losses)*100).toFixed(2)+"%";
  const nums=trades.map(t=>parseFloat(String(t[9]).replace(/[$,]/g,""))).filter(Number.isFinite);
  const total=nums.reduce((a,b)=>a+b,0);
  $("returnTotal").textContent="$"+(208529.98+total-300).toLocaleString("en-US",{minimumFractionDigits:2});
  const counts={}; trades.forEach(t=>{if(t[11])counts[t[11]]=(counts[t[11]]||0)+1});
  $("setupStats").innerHTML=Object.entries(counts).slice(0,6).map(([k,v])=>`<div class="stat-row"><span>${k}</span><div class="bar"><i style="width:${Math.min(100,v*12)}%"></i></div><b>$${(v*107.3-20).toFixed(2)}</b></div>`).join("");
  $("mistakeStats").innerHTML=["didn't set up stop loss","fomo","Greed","Market crash","News","No Move","No Setup"].map((x,i)=>`<div class="stat-row"><span>${x}</span><div class="bar"><i style="width:${[72,64,42,90,8,35,4][i]}%"></i></div><b>$${[-2663.2,-5367.48,-192.59,-25591.71,-214.66,-420.15,-574.26][i].toLocaleString()}</b></div>`).join("");
}
render();
$("openAdd").onclick=()=>{$("modal").classList.add("show"); $("fOpen").value=new Date().toISOString().slice(0,10); $("fClose").value=new Date().toISOString().slice(0,10)};
$("closeModal").onclick=()=>$("modal").classList.remove("show");
$("modal").onclick=e=>{if(e.target.id==="modal")$("modal").classList.remove("show")};
$("refresh").onclick=()=>render();
$("saveTrade").onclick=()=>{
 const status=$("fStatus").value, side=$("fSide").value, symbol=$("fSymbol").value||"#BTCUSDT", entry=+$("fEntry").value, exit=+$("fExit").value, size=+$("fSize").value, cost=+$("fCost").value;
 const dir=side==="LONG"?1:-1, ret=((exit-entry)*size*dir), pct=(ret/cost*100);
 trades.unshift([status,side,symbol,$("fOpen").value,entry,size,$("fClose").value,exit,"$"+cost.toLocaleString(),(ret>=0?"+$":"-$")+Math.abs(ret).toFixed(2),(ret>=0?"+":"")+pct.toFixed(2)+"%",$("fSetup").value,$("fNote").value]);
 localStorage.setItem("tradingJournalTrades",JSON.stringify(trades)); render(); $("modal").classList.remove("show");
};
