<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Kortex Threat Visualizer</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css"/>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body { margin:0; font-family:'Inter', sans-serif; background:#0f111a; color:#f0f0f0; }
header { background:#1a1f2a; padding:1rem 2rem; display:flex; justify-content:space-between; align-items:center; box-shadow:0 2px 5px rgba(0,0,0,0.5); }
header h1 { font-size:1.5rem; color:#00d4ff; }
main { display:flex; flex-wrap:wrap; padding:1rem; gap:1rem; }
.panel { background:#1f2633; border-radius:10px; padding:1rem; flex:1 1 300px; min-height:300px; box-shadow:0 2px 10px rgba(0,0,0,0.5); }
h2 { font-size:1.2rem; color:#00d4ff; margin-bottom:0.5rem; }
#networkMap { width:100%; height:300px; background:#111; border-radius:10px; position:relative; overflow:hidden; }
.node { position:absolute; width:10px; height:10px; border-radius:50%; background:#ff4c4c; transition: all 0.3s; }
ul#alerts { list-style:none; padding:0; margin:0; max-height:250px; overflow-y:auto; }
ul#alerts li { margin:0.3rem 0; padding:0.3rem; border-bottom:1px solid #333; }
canvas { background:#111; border-radius:10px; }
.filter { margin-bottom:0.5rem; display:flex; gap:0.5rem; }
.filter input { flex:1; padding:0.3rem; border-radius:5px; border:none; }
</style>
</head>
<body>

<header>
  <h1>Kortex Threat Visualizer</h1>
  <span id="liveTime"></span>
</header>

<main>
  <div class="panel">
    <h2>Live Threat Map</h2>
    <div id="networkMap"></div>
  </div>

  <div class="panel">
    <h2>Live Alerts</h2>
    <div class="filter">
      <input type="text" id="ipFilter" placeholder="Filter by IP">
    </div>
    <ul id="alerts"></ul>
  </div>

  <div class="panel">
    <h2>Threat Score Trend</h2>
    <canvas id="scoreChart" height="300"></canvas>
  </div>
</main>

<script>
// Live time
function updateTime() {
  document.getElementById('liveTime').textContent = new Date().toLocaleString();
}
setInterval(updateTime,1000);

// Mock detection data generator (replace with real log parsing)
const nodes=[];
const alerts=[];
function generateDetection() {
  const ip = `192.168.${Math.floor(Math.random()*255)}.${Math.floor(Math.random()*255)}`;
  const score = (Math.random()*5).toFixed(2);
  const payloads = ['SQLi','XSS','RCE','LFI','Directory Scan'];
  const payload = payloads[Math.floor(Math.random()*payloads.length)];
  const detection = {timestamp:new Date().toISOString(),client_ip:ip,score:score,payload:payload};
  alerts.push(detection);
  if(alerts.length>50) alerts.shift();
  return detection;
}

// Network Map
const mapDiv = document.getElementById('networkMap');
function updateNetworkMap(detection){
  const node=document.createElement('div');
  node.className='node';
  node.style.top=Math.random()*90+'%';
  node.style.left=Math.random()*90+'%';
  node.title=`IP: ${detection.client_ip}\nScore: ${detection.score}\nPayload: ${detection.payload}`;
  mapDiv.appendChild(node);
  setTimeout(()=>node.remove(),5000);
}

// Live Alerts List
const alertsList=document.getElementById('alerts');
const ipFilter=document.getElementById('ipFilter');
function renderAlerts(){
  const filter=ipFilter.value.toLowerCase();
  alertsList.innerHTML=alerts.filter(a=>a.client_ip.includes(filter)).map(a=>`<li>[${new Date(a.timestamp).toLocaleTimeString()}] ${a.client_ip} - Score: ${a.score} - ${a.payload}</li>`).join('');
}

// Chart.js Trend
const ctx=document.getElementById('scoreChart').getContext('2d');
const scoreChart=new Chart(ctx,{
  type:'line',
  data:{labels:[], datasets:[{label:'Threat Score', data:[], borderColor:'#ff4c4c', tension:0.3, fill:false}]},
  options:{scales:{y:{beginAtZero:true, max:5}}, animation:false}
});

function updateChart(detection){
  scoreChart.data.labels.push(new Date(detection.timestamp).toLocaleTimeString());
  scoreChart.data.datasets[0].data.push(detection.score);
  if(scoreChart.data.labels.length>20){
    scoreChart.data.labels.shift();
    scoreChart.data.datasets[0].data.shift();
  }
  scoreChart.update();
}

// Polling every 1.5s
setInterval(()=>{
  const detection=generateDetection();
  updateNetworkMap(detection);
  renderAlerts();
  updateChart(detection);
},1500);

ipFilter.addEventListener('input',renderAlerts);

</script>
</body>
</html>
