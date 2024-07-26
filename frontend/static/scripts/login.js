document.getElementById('loginForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
    };

    const response = await fetch('http://145.93.173.20:8080/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    if (!response.ok){
        return
    }

    const jsonResponse = await response.json()

    const token = jsonResponse['token']
    const customerId = jsonResponse['customer-id']
    const customerName = jsonResponse['customer-name']
    const cart = []

    localStorage.setItem('jwt-token', JSON.stringify(token))
    localStorage.setItem('customer-id', customerId)
    localStorage.setItem('customer-name', customerName)
    localStorage.setItem('cart', JSON.stringify(cart))

    window.location.href = '/'
});