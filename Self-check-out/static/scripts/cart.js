let cart = JSON.parse(localStorage.getItem('cart'))
renderCart();

function renderCart() {

    const cartBody = document.getElementById('cartBody');
    cartBody.innerHTML = '';

    cart.forEach(item => {
        const row = document.createElement('tr');

        const nameCell = document.createElement('td');
        nameCell.textContent = item.name;

        const descriptionCell = document.createElement('td');
        descriptionCell.textContent = item.description;

        const priceCell = document.createElement('td');
        priceCell.textContent = '$' + item.price;


        const actionCell = document.createElement('td');
        const removeLink = document.createElement('a');
        removeLink.href = 'javascript:void(0)';
        removeLink.textContent = 'Remove';
        removeLink.className = 'btn';
        removeLink.addEventListener('click', () => {
            removeItemById(item.id);
        });
        actionCell.appendChild(removeLink);

        row.appendChild(nameCell);
        row.appendChild(descriptionCell);
        row.appendChild(priceCell);
        row.appendChild(actionCell);

        cartBody.appendChild(row);
    });
    const totalPriceElement = document.getElementById('total-price');
    const totalPrice = cart.reduce((total, item) => {
        return total + item.price;
    }, 0);

    totalPriceElement.textContent = `Total Price: $${totalPrice}`
}

function removeItemById(itemId) {
    const index = cart.findIndex(item => {
        return item.id === itemId;
    });
    if (index !== -1) {
        cart.splice(index, 1);

        renderCart();
        localStorage.setItem('cart', JSON.stringify(cart))
    }
}

async function submitOrder() {
    let pizzas = [];

    cart.forEach(item => {
        const existingPizza = pizzas.find(pizza => {
            return pizza.title === item.name;
        });

        if (existingPizza) {
            existingPizza.quantity += 1;
            return
        }

        pizzas.push({
            title: item.name,
            quantity: 1
        });
    });

    const response = await fetch("http://145.93.173.20:8080/orders", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + JSON.parse(localStorage.getItem('jwt-token'))
        },
        body: JSON.stringify({pizzas})
    })

    if (!response.ok) {
        return
    }

    cart = []
    localStorage.setItem('cart', JSON.stringify(cart))

    renderCart()
}