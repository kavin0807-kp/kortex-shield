<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Kortex Corp - Interactive Portal</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css"/>
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

body { font-family: 'Roboto', sans-serif; margin:0; background:#f0f2f5; color:#333; }
.navbar { background:#fff; display:flex; justify-content:space-between; align-items:center; padding:10px 5%; box-shadow:0 2px 4px rgba(0,0,0,0.1); position:sticky; top:0; z-index:1000; }
.navbar .logo { font-weight:700; font-size:1.5rem; color:#2c3e50; }
.navbar nav a { margin-left:15px; text-decoration:none; color:#555; font-weight:600; transition:0.3s; }
.navbar nav a.active, .navbar nav a:hover { color:#3498db; }

.page { display:none; padding:2rem 5%; }
.page.active { display:block; }
.hero { background:#3498db; color:#fff; padding:4rem 2rem; border-radius:10px; text-align:center; }
.team-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:1.5rem; margin-top:2rem; }
.team-card { background:#fff; padding:1.5rem; border-radius:10px; text-align:center; box-shadow:0 4px 10px rgba(0,0,0,0.1); cursor:pointer; transition:0.3s; }
.team-card:hover { transform:translateY(-5px); box-shadow:0 8px 20px rgba(0,0,0,0.2); }
.team-card img { width:100px; height:100px; border-radius:50%; margin-bottom:1rem; }
.modal { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:2000; }
.modal-content { background:#fff; margin:10% auto; padding:2rem; width:90%; max-width:500px; border-radius:10px; position:relative; }
.close { position:absolute; top:10px; right:15px; font-size:28px; cursor:pointer; }
form input, form textarea, form button { width:100%; padding:10px; margin-bottom:10px; border-radius:5px; border:1px solid #ccc; }
form button { background:#3498db; color:#fff; font-weight:600; cursor:pointer; border:none; }
#searchResults { margin-top:1rem; }
</style>
</head>
<body>

<header class="navbar">
  <div class="logo">Kortex Corp</div>
  <nav>
    <a href="#home" class="nav-link active">Home</a>
    <a href="#team" class="nav-link">Team</a>
    <a href="#directory" class="nav-link">Directory</a>
    <a href="#contact" class="nav-link">Contact</a>
  </nav>
</header>

<main>
  <section id="home" class="page active hero">
    <h1>Welcome to Kortex Corp</h1>
    <p>Innovating for a secure future. Explore our team and resources.</p>
  </section>

  <section id="team" class="page">
    <h1>Meet Our Team</h1>
    <div class="team-grid" id="teamGrid"></div>
  </section>

  <section id="directory" class="page">
    <h1>Employee Directory</h1>
    <input type="text" id="searchInput" placeholder="Search by name or department...">
    <div id="searchResults"></div>
  </section>

  <section id="contact" class="page">
    <h1>Contact Us</h1>
    <form id="contactForm">
      <input type="text" name="name" placeholder="Your Name" required>
      <input type="email" name="email" placeholder="Your Email" required>
      <textarea name="message" placeholder="Your Message..." required></textarea>
      <button type="submit">Send Message</button>
      <p id="formStatus"></p>
    </form>
  </section>
</main>

<!-- Modal for Team Member -->
<div class="modal" id="teamModal">
  <div class="modal-content">
    <span class="close" id="modalClose">&times;</span>
    <h2 id="modalName"></h2>
    <p id="modalTitle"></p>
    <p id="modalDept"></p>
  </div>
</div>

<script>
const pages = document.querySelectorAll('.page');
const navLinks = document.querySelectorAll('.nav-link');
function showPage(id){
  pages.forEach(p=>p.classList.remove('active'));
  navLinks.forEach(l=>l.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  document.querySelector(`.nav-link[href="#${id}"]`).classList.add('active');
}
navLinks.forEach(l=>l.addEventListener('click',e=>{e.preventDefault(); showPage(e.currentTarget.hash.substring(1));}));

// Team Members
const team = [
  {name:'Alice Johnson',title:'Lead Engineer',dept:'Engineering'},
  {name:'Bob Williams',title:'Marketing Head',dept:'Marketing'},
  {name:'Charlie Brown',title:'Sales Director',dept:'Sales'},
  {name:'Diana Miller',title:'Senior Developer',dept:'Engineering'}
];

const teamGrid = document.getElementById('teamGrid');
team.forEach((t,i)=>{
  const card=document.createElement('div');
  card.className='team-card';
  card.innerHTML=`<img src="https://i.pravatar.cc/100?u=${i}"><h3>${t.name}</h3><p>${t.title}</p>`;
  card.addEventListener('click',()=>{
    document.getElementById('modalName').textContent=t.name;
    document.getElementById('modalTitle').textContent=t.title;
    document.getElementById('modalDept').textContent='Department: '+t.dept;
    document.getElementById('teamModal').style.display='block';
  });
  teamGrid.appendChild(card);
});
document.getElementById('modalClose').onclick = ()=>document.getElementById('teamModal').style.display='none';
window.onclick = e=>{if(e.target==document.getElementById('teamModal'))document.getElementById('teamModal').style.display='none';};

// Employee Directory Search
const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');
searchInput.addEventListener('input',()=>{
  const q=searchInput.value.toLowerCase();
  const results=team.filter(t=>t.name.toLowerCase().includes(q)||t.dept.toLowerCase().includes(q));
  searchResults.innerHTML=results.map(r=>`<p>${r.name} - ${r.title} (${r.dept})</p>`).join('')||'<p>No results found</p>';
});

// Contact Form
document.getElementById('contactForm').addEventListener('submit',e=>{
  e.preventDefault();
  document.getElementById('formStatus').textContent='Thank you! We received your message.';
  e.target.reset();
});
</script>
</body>
</html>
