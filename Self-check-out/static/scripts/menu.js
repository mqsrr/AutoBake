let menuData = JSON.parse(localStorage.getItem('menu-data'))
if (menuData === null) {
    getMenu().then(result => menuData = result)

}
const customerName = localStorage.getItem('customer-name')
if (customerName !== 'self-checkout') {
    getLoggedInCustomer().catch(reason => console.log(reason))
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

async function getLoggedInCustomer() {
    let formData = {
        email: 'self-checkout@service.com',
        password: 'CloseToTheTruth'
    };


    let response = await fetch('http://145.93.173.20:8080/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })

    if (response.status !== 401) {
        const data = await response.json()
        setCustomerCredentials(data)

        return
    }

    formData = {
        name: 'self-checkout',
        email: 'self-checkout@service.com',
        password: 'CloseToTheTruth',
        street: "Mario&Luigi Pizzeria",
        postcode: '0000AA'
    };

    response = await fetch('http://145.93.173.20:8080/auth/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })

    const data = await response.json()
    setCustomerCredentials(data)
}

function setCustomerCredentials(jsonResponse) {
    const token = jsonResponse['token']
    const customerId = jsonResponse['customer-id']
    const customerName = jsonResponse['customer-name']

    localStorage.setItem('jwt-token', JSON.stringify(token))
    localStorage.setItem('customer-id', customerId)
    localStorage.setItem('customer-name', customerName)
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
        cartCounter.textContent = count;
    }
}