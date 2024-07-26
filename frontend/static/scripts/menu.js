let menuData = JSON.parse(localStorage.getItem('menu-data'))
if (menuData === null) {
    getMenu().then(result => menuData = result)
}

const customerName = localStorage.getItem('customer-name')
if (customerName === 'self-checkout' || customerName === null) {
    requireLogin()
}


function redirectToLoginPage() {
    window.location.href = "/auth/login"
}


function requireLogin() {
    const addToCartBtn = document.getElementById("addToCartBtn");
    addToCartBtn.textContent = "Add to Cart";
    addToCartBtn.addEventListener("click", redirectToLoginPage);

    const cartLink = document.getElementById('cart-link');
    cartLink.href = '/auth/login'
    cartLink.innerText = 'Login'

}

function addToCart(itemId) {
    const quantityInput = document.getElementById(`quantity_${itemId}`);
    const quantity = parseInt(quantityInput.value);

    let cart = JSON.parse(localStorage.getItem('cart'))
    cart = cart === null ? [] : cart

    const menuItem = menuData.find(item => item.id === itemId)
    for (let i = 0; i < quantity; i++) {
        cart.push(menuItem);
    }

    localStorage.setItem('cart', JSON.stringify(cart))
    updateCartCounter(cart.length)
}

function updateCartCounter(count) {
    const cartCounter = document.getElementById('cart-counter');
    if (cartCounter) {
        cartCounter.textContent = '(' + count + ')';
    }
}

async function getMenu() {
    const response = await fetch('/menu/data', {
        headers: {
            'Content-Type': 'application/json'
        },
    })

    const jsonData = await response.json()
    localStorage.setItem('menu-data', JSON.stringify(jsonData))

    return jsonData
}