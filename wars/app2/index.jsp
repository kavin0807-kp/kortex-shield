<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Kortex Shop</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
body { font-family:'Poppins', sans-serif; margin:0; background:#f1f3f6; }
.header { background:#2874f0; color:white; padding:1rem 5%; display:flex; justify-content:space-between; align-items:center; position:sticky; top:0; z-index:10; }
.header .logo { font-size:1.5rem; font-weight:600; }
.cart-icon { font-size:1.2rem; cursor:pointer; position:relative; }
#cart-count { background:#ff6161; border-radius:50%; padding:2px 6px; font-size:0.8rem; position:absolute; top:-8px; right:-10px; }
.container { padding:1rem 5%; }
.filters { margin-bottom:1rem; display:flex; flex-wrap:wrap; gap:0.5rem; }
.filters button { padding:8px 12px; border:1px solid #ccc; background:#fff; cursor:pointer; border-radius:5px; }
.filters button.active { background:#2874f0; color:#fff; border-color:#2874f0; }
.product-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:1rem; }
.product-card { background:#fff; padding:1rem; text-align:center; transition:0.3s; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.1); cursor:pointer; }
.product-card:hover { box-shadow:0 4px 15px rgba(0,0,0,0.2); }
.product-card img { max-width:100%; height:150px; object-fit:contain; border-radius:5px; }
.product-card h4 { margin:10px 0 5px 0; } .price { color:#388e3c; font-weight:600; }
.modal { display:none; position:fixed; z-index:100; left:0; top:0; width:100%; height:100%; background:rgba(0,0,0,0.5); }
.modal-content { background:#fff; margin:10% auto; padding:20px; border-radius:8px; width:80%; max-width:500px; position:relative; }
.close { position:absolute; top:10px; right:15px; font-size:25px; cursor:pointer; }
.cart-items { max-height:200px; overflow-y:auto; margin-bottom:1rem; }
.cart-item { display:flex; justify-content:space-between; margin:0.3rem 0; }
button.add-to-cart, button.update-btn { margin-top:0.5rem; padding:5px 10px; border:none; background:#2874f0; color:white; border-radius:5px; cursor:pointer; }
button.add-to-cart:hover, button.update-btn:hover { background:#1d5ec0; }
</style>
</head>
<body>

<header class="header">
  <div class="logo">KortexShop</div>
  <div class="cart-icon" id="cart-btn">🛒 <span id="cart-count">0</span></div>
</header>

<div class="container">
  <div class="filters" id="filters">
    <button class="active" data-category="all">All</button>
    <button data-category="audio">Audio</button>
    <button data-category="wearable">Wearables</button>
    <button data-category="pc">PC Peripherals</button>
  </div>

  <input type="text" id="searchInput" placeholder="Search products..." style="padding:8px;width:100%;margin-bottom:1rem;border-radius:5px;border:1px solid #ccc;">

  <div class="product-grid" id="product-grid"></div>
</div>

<div id="cartModal" class="modal">
  <div class="modal-content">
    <span class="close" id="closeModal">&times;</span>
    <h2>Your Cart</h2>
    <div class="cart-items" id="cart-items"></div>
    <p><strong>Total: $<span id="cart-total">0.00</span></strong></p>
    <button class="update-btn" id="checkoutBtn">Checkout</button>
  </div>
</div>

<script>
const products=[
  {id:1,name:'Wireless Headset',price:199.99,img:'https://i.imgur.com/8u4y2V0.jpeg',category:'audio',desc:'High quality wireless headset with noise cancellation.'},
  {id:2,name:'Smart Watch',price:249.50,img:'https://i.imgur.com/7D7I6dI.jpeg',category:'wearable',desc:'Smart watch with health monitoring and notifications.'},
  {id:3,name:'Portable Speaker',price:89.00,img:'https://i.imgur.com/83Ff7gN.jpeg',category:'audio',desc:'Compact speaker with deep bass and Bluetooth 5.0.'},
  {id:4,name:'Gaming Mouse',price:55.25,img:'https://i.imgur.com/8C3T43c.jpeg',category:'pc',desc:'Ergonomic mouse with RGB lighting and programmable buttons.'}
];

const grid=document.getElementById('product-grid');
const filterButtons=document.querySelectorAll('#filters button');
const searchInput=document.getElementById('searchInput');
const cart={};

function renderProducts(category='all',search=''){
  grid.innerHTML='';
  const filtered=products.filter(p=>(category==='all'||p.category===category) && p.name.toLowerCase().includes(search.toLowerCase()));
  filtered.forEach(p=>{
    const card=document.createElement('div');
    card.className='product-card';
    card.innerHTML=`<img src="${p.img}"><h4>${p.name}</h4><p class="price">$${p.price.toFixed(2)}</p><p>${p.desc}</p><button class="add-to-cart">Add to Cart</button>`;
    card.querySelector('button').addEventListener('click',(e)=>{e.stopPropagation(); addToCart(p.id);});
    grid.appendChild(card);
  });
}

// Filters
filterButtons.forEach(btn=>btn.addEventListener('click',()=>{
  filterButtons.forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  renderProducts(btn.dataset.category,searchInput.value);
}));

searchInput.addEventListener('input',()=>renderProducts(document.querySelector('.filters button.active').dataset.category,searchInput.value));

// Cart Functions
const cartCountEl=document.getElementById('cart-count');
const cartModal=document.getElementById('cartModal');
const cartItemsDiv=document.getElementById('cart-items');
const cartTotalEl=document.getElementById('cart-total');

function addToCart(productId){
  cart[productId]=(cart[productId]||0)+1;
  updateCart();
}

function updateCart(){
  let total=0,count=0,html='';
  for(const id in cart){
    const p=products.find(pr=>pr.id==id);
    count+=cart[id];
    total+=cart[id]*p.price;
    html+=`<div class="cart-item">${p.name} x ${cart[id]} <button onclick="removeFromCart(${id})">❌</button></div>`;
  }
  cartCountEl.textContent=count;
  cartItemsDiv.innerHTML=html;
  cartTotalEl.textContent=total.toFixed(2);
}

function removeFromCart(id){
  delete cart[id];
  updateCart();
}

// Modal Controls
document.getElementById('cart-btn').onclick=()=>cartModal.style.display='block';
document.getElementById('closeModal').onclick=()=>cartModal.style.display='none';
window.onclick=(e)=>{if(e.target==cartModal) cartModal.style.display='none';};

// Checkout
document.getElementById('checkoutBtn').onclick=()=>{
  if(Object.keys(cart).length===0){alert('Cart is empty');return;}
  alert('Thank you for your purchase!');
  for(const id in cart) delete cart[id];
  updateCart();
};

renderProducts();
</script>
</body>
</html>
