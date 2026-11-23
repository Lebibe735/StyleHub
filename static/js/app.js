
// ==============================
// GLOBAL VARIABLES
// ==============================

const API_URL = '/api';

let allProducts = [];
let filteredProducts = [];
let editingProductId = null;
// Shopping cart
// Load saved cart from browser storage
// Shopping cart
let cart = [];

function saveCart() {
    const username = localStorage.getItem('username');

    if (username) {
        localStorage.setItem(`cart_${username}`, JSON.stringify(cart));
    }
}

function loadCart() {
    const username = localStorage.getItem('username');

    if (username) {
        cart = JSON.parse(localStorage.getItem(`cart_${username}`)) || [];
    } else {
        cart = [];
    }

    updateCartCount();
    displayCart();
}
// Add product to cart
// ==============================
// ADD TO CART
// ==============================

function addToCart(productId) {

    const product = allProducts.find(p => p.id === productId);

    if (!product) return;

    const existingItem = cart.find(item => item.id === productId);

    if (existingItem) {
        existingItem.quantity++;
    } else {
        cart.push({
            id: product.id,
            name: product.name,
            price: Number(product.discounted_price),
            original_price: Number(product.price),
            discount_percentage: Number(product.discount_percentage),
            quantity: 1
        });
    }

    saveCart();
    updateCartCount();
    displayCart();
}


// Update cart counter and save cart
function updateCartCount() {

    const cartCount = document.getElementById('cartCount');

    const totalItems = cart.reduce(
        (total, item) => total + item.quantity,
        0
    );

    cartCount.textContent = totalItems;
saveCart();
    // Save cart in browser storage
    //localStorage.setItem('cart', JSON.stringify(cart));
}
// Display products inside the shopping cart
function displayCart() {

    const cartItems = document.getElementById('cartItems');
    const cartTotal = document.getElementById('cartTotal');

    cartItems.innerHTML = '';

    if (cart.length === 0) {
        cartItems.innerHTML = `
            <div class="empty-cart">
                <div class="empty-cart-icon">♡</div>
                <h3>Your bag is empty</h3>
                <p>Discover something you'll love.</p>
            </div>
        `;

        cartTotal.textContent = '€0.00';
        return;
    }

    let total = 0;

    cart.forEach(item => {
const price = Number(item.discounted_price ?? item.price);
        const originalPrice = Number(item.original_price || item.price);
        const discount = Number(item.discount_percentage || 0);

        total += price * item.quantity;

        const priceHTML = discount > 0
            ? `
                <span class="cart-original-price">
                    €${originalPrice.toFixed(2)}
                </span>
                <span class="cart-product-price">
                    €${price.toFixed(2)}
                </span>
                <span class="cart-discount">
                    -${discount}%
                </span>
            `
            : `
                <span class="cart-product-price">
                    €${price.toFixed(2)}
                </span>
            `;

        const imageHTML = item.image_url
            ? `<img src="${escapeHTML(item.image_url)}" alt="${escapeHTML(item.name)}">`
            : `<span class="cart-product-placeholder">STYLEHUB</span>`;

        cartItems.innerHTML += `
            <div class="cart-item">

                <div class="cart-product-image">
                    ${imageHTML}
                </div>

                <div class="cart-product-details">

                    <div>
                        <span class="cart-product-brand">
                            ${escapeHTML(item.brand || '')}
                        </span>

                        <h4>${escapeHTML(item.name)}</h4>

                        ${priceHTML}
                    </div>

                    <div class="cart-item-actions">

                        <div class="quantity-control">
                            <button class="decrease-cart" data-product-id="${item.id}">−</button>
                            <span>${item.quantity}</span>
                            <button class="increase-cart" data-product-id="${item.id}">+</button>
                        </div>

                        <button class="remove-cart" data-product-id="${item.id}">
                            Remove
                        </button>

                    </div>

                </div>

            </div>
        `;
    });

    cartTotal.textContent = `€${total.toFixed(2)}`;
}

// Close shopping cart
function closeCart() {

    document.getElementById('cartPanel').classList.remove('active');
    document.getElementById('cartOverlay').classList.remove('active');

}

// Continue shopping button
document.getElementById('continueShopping').addEventListener('click', closeCart);

document.getElementById('closeCart').addEventListener('click', closeCart);

document.getElementById('cartOverlay').addEventListener('click', closeCart);


// Handle quantity and removal buttons
document.addEventListener('click', event => {

    const button = event.target.closest(
        '.increase-cart, .decrease-cart, .remove-cart'
    );

    if (!button) {
        return;
    }

    const productId = Number(button.dataset.productId);

    const cartProduct = cart.find(
        item => Number(item.id) === productId
    );

    if (!cartProduct) {
        return;
    }

    // Increase quantity
    if (button.classList.contains('increase-cart')) {

        const product = allProducts.find(
            item => Number(item.id) === productId
        );

        if (!product || cartProduct.quantity >= Number(product.quantity)) {
            alert('Not enough stock available!');
            return;
        }

        cartProduct.quantity++;
    }

    // Decrease quantity
    else if (button.classList.contains('decrease-cart')) {

        cartProduct.quantity--;

        if (cartProduct.quantity <= 0) {
            cart = cart.filter(
                item => Number(item.id) !== productId
            );
        }
    }

    // Remove product
    else if (button.classList.contains('remove-cart')) {

        cart = cart.filter(
            item => Number(item.id) !== productId
        );
    }

    updateCartCount();
    displayCart();
    // Display order summary in checkout
function displayCheckoutSummary() {

    const summary = document.getElementById('checkoutSummary');
    const checkoutTotal = document.getElementById('checkoutTotal');

    summary.innerHTML = '';

    let total = 0;

    cart.forEach(item => {

        const price = Number(item.discounted_price ?? item.price);
        const subtotal = price * item.quantity;

        total += subtotal;

        summary.innerHTML += `
            <div class="checkout-summary-item">
                <span>${escapeHTML(item.name)} × ${item.quantity}</span>
                <strong>€${subtotal.toFixed(2)}</strong>
            </div>
        `;
    });

    checkoutTotal.textContent = `€${total.toFixed(2)}`;
}

});

// // ==============================
// // DISPLAY CHECKOUT SUMMARY
// // ==============================

function displayCheckoutSummary() {

    const summary = document.getElementById('checkoutSummary');
    const checkoutTotal = document.getElementById('checkoutTotal');

    summary.innerHTML = '';

    let total = 0;

    cart.forEach(item => {

        const price = Number(item.discounted_price ?? item.price);
        const subtotal = price * item.quantity;

        total += subtotal;

        summary.innerHTML += `
            <div class="checkout-summary-item">
                <span>${escapeHTML(item.name)} × ${item.quantity}</span>
                <strong>€${subtotal.toFixed(2)}</strong>
            </div>
        `;

    });

    checkoutTotal.textContent = `€${total.toFixed(2)}`;
}

// ==============================
// SHOW ORDER CONFIRMATION
// ==============================

function showOrderConfirmation(order) {

    document.getElementById('confirmationOrderId').textContent =
        `#${order.id}`;

    const orderDate = new Date(order.order_date);

    document.getElementById('confirmationDate').textContent =
        orderDate.toLocaleString();

    document.getElementById('confirmationCustomer').textContent =
        order.client_name;

    document.getElementById('confirmationStatus').textContent =
        order.status.charAt(0).toUpperCase() + order.status.slice(1);

    const itemsContainer = document.getElementById('confirmationItems');

    itemsContainer.innerHTML = '';

    order.items.forEach(item => {

        itemsContainer.innerHTML += `
            <div class="confirmation-item">
                <span>
                    ${escapeHTML(item.product_name)} × ${item.quantity}
                </span>
                <strong>€${Number(item.subtotal).toFixed(2)}</strong>
            </div>
        `;

    });

    document.getElementById('confirmationTotal').textContent =
        `€${Number(order.total_amount).toFixed(2)}`;

    document.getElementById('confirmationOverlay').classList.add('active');
}
// ==============================
// LOAD CUSTOMER ORDERS
// ==============================

async function loadMyOrders() {

    const container = document.getElementById('myOrdersContainer');

    container.innerHTML = '<div class="orders-loading">Loading your orders...</div>';

    try {

        const token = localStorage.getItem('token');

        const response = await fetch(`${API_URL}/orders`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Could not load orders.');
        }

        displayMyOrders(data);

    } catch (error) {

        console.error('Orders error:', error);

        container.innerHTML = `
            <div class="no-orders">
                Could not load your orders. Please try again.
            </div>
        `;

    }
}
// ==============================
// DISPLAY CUSTOMER ORDERS
// ==============================

function displayMyOrders(orders) {

    const container = document.getElementById('myOrdersContainer');

    if (!Array.isArray(orders)) {
        orders = orders.orders || [];
    }

    if (orders.length === 0) {

        container.innerHTML = `
            <div class="no-orders">
                <h3>No orders yet</h3>
                <p>Your purchases will appear here.</p>
            </div>
        `;

        return;
    }

    container.innerHTML = '<div class="orders-list">';

    orders.forEach(order => {

        const productsHTML = order.items.map(item => `
            <div class="order-product">
                <span>${escapeHTML(item.product_name)} × ${item.quantity}</span>
                <strong>€${Number(item.subtotal).toFixed(2)}</strong>
            </div>
        `).join('');

        container.innerHTML += `
            <div class="order-card">

                <div class="order-card-header">

                    <div>
                        <div class="order-number">Order #${order.id}</div>
                        <div class="order-date">
                            ${new Date(order.order_date).toLocaleString()}
                        </div>
                    </div>

                    <span class="order-status ${escapeHTML(order.status)}">
                        ${escapeHTML(order.status)}
                    </span>

                </div>

                <div class="order-products">
                    ${productsHTML}
                </div>

                <div class="order-card-footer">
                    <span>Total</span>
                    <span class="order-total">
                        €${Number(order.total_amount).toFixed(2)}
                    </span>
                </div>

            </div>
        `;

    });

    container.innerHTML += '</div>';
}
// ==============================
// LOAD PRODUCTS
// ==============================

async function loadProducts() {

    const productGrid = document.getElementById('productGrid');

    try {

        const token = localStorage.getItem('token');

        const headers = {};

        // Send the token only if the user is logged in
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_URL}/products`, {
            headers: headers
        });

        if (!response.ok) {
            throw new Error('Could not retrieve products.');
        }

        const data = await response.json();

        allProducts = Array.isArray(data)
            ? data
            : data.products || [];

        filteredProducts = [...allProducts];

        displayProducts(filteredProducts);

    } catch (error) {

        console.error('Error loading products:', error);

        productGrid.innerHTML = `
            <p class="loading-message">
                Could not load products. Please try again.
            </p>
        `;
    }
}

// ==============================
// DISPLAY PRODUCTS
// ==============================

function displayProducts(products) {

    const productGrid = document.getElementById('productGrid');

    productGrid.innerHTML = '';

    const role = localStorage.getItem('role');

    const isManagement = ['admin', 'advanced_user'].includes(role);

    if (products.length === 0) {
        productGrid.innerHTML = `
            <p class="loading-message">No products found.</p>
        `;
        return;
    }

    products.forEach(product => {

        const card = document.createElement('div');
        card.className = 'product-card';

        const name = escapeHTML(product.name);
        const brand = escapeHTML(product.brand || 'No brand');
        const category = escapeHTML(product.category || 'Other');

        const originalPrice = Number(product.price);
        const sellingPrice = Number(product.discounted_price ?? product.price);

        const hasDiscount = Number(product.discount_percentage || 0) > 0
            && sellingPrice < originalPrice;

        const priceHTML = hasDiscount
            ? `
                <div class="product-prices">
                    <span class="old-price">€${originalPrice.toFixed(2)}</span>
                    <span class="current-price">€${sellingPrice.toFixed(2)}</span>
                </div>
            `
            : `
                <div class="product-prices">
                    <span class="current-price">€${sellingPrice.toFixed(2)}</span>
                </div>
            `;

        const imageURL = product.image_url || product.image || '';

        const imageHTML = imageURL
            ? `<img src="${escapeHTML(imageURL)}" alt="${name}"
                    onerror="this.style.display='none';">`
            : `<div class="product-placeholder">STYLEHUB</div>`;

        card.innerHTML = `
            <div class="product-image">
                ${imageHTML}

                ${hasDiscount
                    ? `<span class="discount-badge">
                        -${Number(product.discount_percentage)}%
                       </span>`
                    : ''}
            </div>

            <div class="product-info">

                <p class="product-brand">${brand}</p>

                <h3>${name}</h3>

                <p class="product-category">${category}</p>

                ${priceHTML}

                <p class="product-stock">
                    ${isManagement
                        ? `Quantity: ${Number(product.quantity)}`
                        : Number(product.quantity) > 0
                            ? 'In Stock'
                            : 'Out of Stock'}
                </p>

                ${!isManagement ? `
                    <button class="add-to-cart-button"
                        ${Number(product.quantity) <= 0 ? 'disabled' : ''}
                        data-product-id="${Number(product.id)}">
                        ${Number(product.quantity) > 0
                            ? 'ADD TO CART'
                            : 'OUT OF STOCK'}
                    </button>
                ` : ''}

                ${role && ['admin', 'advanced_user', 'simple_user'].includes(role) ? `
                    <button class="edit-product-button"
                        data-product-id="${Number(product.id)}">
                        EDIT PRODUCT
                    </button>
                ` : ''}

                ${role && ['admin', 'advanced_user'].includes(role) ? `
                    <button class="delete-product-button"
                        data-product-id="${Number(product.id)}">
                        DELETE PRODUCT
                    </button>
                ` : ''}

            </div>
        `;

        productGrid.appendChild(card);

    });
}
// ==============================
// CREATE CLIENT
// ==============================

async function createCheckoutClient() {

    const token = localStorage.getItem('token');

    const clientData = {
        first_name: document.getElementById('checkoutFirstName').value.trim(),
        last_name: document.getElementById('checkoutLastName').value.trim(),
        email: document.getElementById('checkoutEmail').value.trim(),
        phone: document.getElementById('checkoutPhone').value.trim(),
        address: document.getElementById('checkoutAddress').value.trim()
    };

    const response = await fetch(`${API_URL}/clients`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(clientData)
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || 'Could not create client.');
    }

    return data;
}
// ==============================
// CREATE ORDER
// ==============================

async function createCheckoutOrder(clientId) {

    const token = localStorage.getItem('token');

    const orderData = {
        client_id: clientId,
        items: cart.map(item => ({
            product_id: item.id,
            quantity: item.quantity
        }))
    };

    const response = await fetch(`${API_URL}/orders`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(orderData)
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || 'Could not create order.');
    }

    return data;
}
// ==============================
// ESCAPE HTML
// ==============================

function escapeHTML(value) {

    return String(value ?? '').replace(/[&<>"']/g, character => {

        const characters = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        };

        return characters[character];

    });

}


// ==============================
// SEARCH PRODUCTS
// ==============================

function searchProducts() {

    const searchValue = document
        .getElementById('searchInput')
        .value
        .toLowerCase()
        .trim();

    filteredProducts = allProducts.filter(product => {

        return (
            (product.name || '').toLowerCase().includes(searchValue) ||
            (product.brand || '').toLowerCase().includes(searchValue) ||
            (product.category || '').toLowerCase().includes(searchValue)
        );

    });

    displayProducts(filteredProducts);

}


// ==============================
// FILTER PRODUCTS
// ==============================

function filterProducts() {

    const category = document.getElementById('categoryFilter').value;
    const gender = document.getElementById('genderFilter').value;
    const brand = document.getElementById('brandFilter').value;

    filteredProducts = allProducts.filter(product => {

        const matchesCategory = !category ||
    product.category.toLowerCase().includes(category.toLowerCase());

        const matchesGender =
            !gender || product.gender === gender;

        const matchesBrand =
            !brand || product.brand === brand;

        return matchesCategory && matchesGender && matchesBrand;

    });

    sortProducts();

}


// ==============================
// SORT PRODUCTS
// ==============================

function sortProducts() {

    const sortValue = document.getElementById('sortFilter').value;

    if (sortValue === 'price_asc') {

        filteredProducts.sort((a, b) =>
            Number(a.discounted_price ?? a.price) -
            Number(b.discounted_price ?? b.price)
        );

    }

    else if (sortValue === 'price_desc') {

        filteredProducts.sort((a, b) =>
            Number(b.discounted_price ?? b.price) -
            Number(a.discounted_price ?? a.price)
        );

    }

    else if (sortValue === 'name_asc') {

        filteredProducts.sort((a, b) =>
            a.name.localeCompare(b.name)
        );

    }

    displayProducts(filteredProducts);

}


// ==============================
// CATEGORY CARDS
// ==============================

document.querySelectorAll('.category-card').forEach(card => {

    card.addEventListener('click', () => {

        const category = card.dataset.category;

        document.getElementById('categoryFilter').value = category;

        filterProducts();

        document.getElementById('products').scrollIntoView({
            behavior: 'smooth'
        });

    });

});


// ==============================
// SEARCH BUTTON
// ==============================

document.getElementById('searchToggle').addEventListener('click', () => {

    document.getElementById('searchContainer').classList.toggle('active');

});

document.getElementById('searchButton').addEventListener('click', searchProducts);

document.getElementById('searchInput').addEventListener('keydown', event => {

    if (event.key === 'Enter') {
        searchProducts();
    }

});


// ==============================
// FILTER EVENTS
// ==============================

document.getElementById('categoryFilter').addEventListener('change', filterProducts);

document.getElementById('genderFilter').addEventListener('change', filterProducts);

document.getElementById('brandFilter').addEventListener('change', filterProducts);

document.getElementById('sortFilter').addEventListener('change', sortProducts);

// ==============================
// ADD TO CART EVENTS
// ==============================

document.addEventListener('click', event => {

    const button = event.target.closest('.add-to-cart-button');

    if (!button) {
        return;
    }

    const productId = Number(button.dataset.productId);

    addToCart(productId);

});
// Open checkout
// Handle checkout button
// ==============================
// CHECKOUT EVENTS
// ==============================

// Open checkout
document.addEventListener('click', event => {

    const button = event.target.closest('#checkoutButton');

    if (!button) {
        return;
    }

    if (cart.length === 0) {
        alert('Your shopping cart is empty!');
        return;
    }

    displayCheckoutSummary();

    closeCart();

    document.getElementById('checkoutOverlay').classList.add('active');

});


// Close checkout
document.getElementById('closeCheckout').addEventListener('click', () => {

    document.getElementById('checkoutOverlay').classList.remove('active');

});


// Close checkout by clicking outside
document.getElementById('checkoutOverlay').addEventListener('click', event => {

    if (event.target.id === 'checkoutOverlay') {
        document.getElementById('checkoutOverlay').classList.remove('active');
    }

});

// ==============================
// CHECKOUT FORM SUBMISSION
// ==============================

document.getElementById('checkoutForm').addEventListener('submit', async event => {

    event.preventDefault();

    try {

        const clientData = await createCheckoutClient();

        const clientId = clientData.client.id;

        const orderData = await createCheckoutOrder(clientId);

       showOrderConfirmation(orderData.order);

cart = [];

updateCartCount();

displayCart();

document.getElementById('checkoutForm').reset();

document.getElementById('checkoutOverlay').classList.remove('active');

    } catch (error) {

        alert(error.message);
        console.error('Checkout error:', error);

    }

});
// ==============================
// INITIALIZE WEBSITE
// ==============================
document.addEventListener('DOMContentLoaded', () => {

    loadCart();
    updateAccountButton();
    updateNavigation();
    updateProductManagementToolbar();
    loadProducts();

    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');

    if (
        token &&
        (role === 'admin' || role === 'advanced_user')
    ) {
        document.getElementById('my-orders').classList.add('active');
        loadMyOrders();
    } else {
        document.getElementById('my-orders').classList.remove('active');
    }

});
// ==============================
// CONTINUE SHOPPING
// ==============================

document.getElementById('continueAfterOrder').addEventListener('click', () => {

    document.getElementById('confirmationOverlay').classList.remove('active');

    window.location.hash = 'shop';

});
// Load orders when visiting My Orders

// Load orders when visiting My Orders

document.addEventListener('click', event => {

    const myOrdersLink = event.target.closest('#myOrdersLink');

    if (!myOrdersLink) return;

    const role = localStorage.getItem('role');

    if (role !== 'admin' && role !== 'advanced_user') {
        event.preventDefault();
        return;
    }

    loadMyOrders();

});
// ==============================
// LOGIN MODAL
// ==============================

document.addEventListener('click', function(event) {

    // Open login modal
    if (event.target.closest('#loginButton')) {

    if (localStorage.getItem('token')) {
        loadDashboard();
        document.getElementById('loginOverlay').classList.remove('active');

        document.getElementById('dashboard').scrollIntoView({
            behavior: 'smooth'
        });

    } else {
        document.getElementById('loginOverlay').classList.add('active');
    }
}

    // Close login modal
    if (event.target.closest('#closeLogin')) {
        document.getElementById('loginOverlay').classList.remove('active');
    }

    // Close when clicking outside the modal
    if (event.target.id === 'loginOverlay') {
        document.getElementById('loginOverlay').classList.remove('active');
    }

});
// ==============================
// USER LOGIN
// ==============================

document.addEventListener('submit', async event => {

    if (event.target.id !== 'loginForm') {
        return;
    }

    event.preventDefault();

    const username = document.getElementById('loginUsername').value.trim();
    const password = document.getElementById('loginPassword').value;
    const errorMessage = document.getElementById('loginError');

    errorMessage.textContent = '';

    try {

        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Invalid username or password.');
        }

        const user = data.user;

        if (!data.token) {
            throw new Error('The server did not return a valid token.');
        }

        // Save login information
        localStorage.setItem('token', data.token);
        localStorage.setItem('username', user.username);
        localStorage.setItem('role', user.role);
        loadCart();
        // Update account and navigation
        updateAccountButton();
        updateNavigation();
        updateProductManagementToolbar();
        // Close login window
        document.getElementById('loginOverlay').classList.remove('active');
        document.getElementById('loginForm').reset();

        // Refresh products
        await loadProducts();

        // Show orders only to Admin and Advanced Users
        const ordersSection = document.getElementById('my-orders');

        if (user.role === 'admin' || user.role === 'advanced_user') {
            ordersSection.classList.add('active');
            await loadMyOrders();
        } else {
            ordersSection.classList.remove('active');
            document.getElementById('myOrdersContainer').innerHTML = '';
        }

        // Open dashboard
        loadDashboard();

        // Go to dashboard
        document.getElementById('dashboard').scrollIntoView({
            behavior: 'smooth'
        });

        alert(`Welcome, ${user.username}!`);

    } catch (error) {

        errorMessage.textContent = error.message;
        console.error('Login error:', error);

    }

});
function updateNavigation() {

    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');

    const myOrdersLink = document.getElementById('myOrdersLink');

    if (!myOrdersLink) return;

    const canViewOrders =
        token && (role === 'admin' || role === 'advanced_user');

    myOrdersLink.style.display = canViewOrders ? 'inline-block' : 'none';
}
// Update account button based on login status
// ==============================
// UPDATE ACCOUNT BUTTON
// ==============================

function updateAccountButton() {

    const username = localStorage.getItem('username');
    const role = localStorage.getItem('role');

    const usernameElement = document.getElementById('accountUsername');
    const loginButton = document.getElementById('loginButton');

    if (username && role) {

        usernameElement.textContent = username;
        loginButton.title = `${username} (${role})`;

    } else {

        usernameElement.textContent = 'Sign In';
        loginButton.title = 'Sign In';

    }
}
// ==============================
// USER DASHBOARD
// ==============================

function loadDashboard() {

    const username = localStorage.getItem('username');
    const role = localStorage.getItem('role');

    const dashboard = document.getElementById('dashboard');
    const welcome = document.getElementById('dashboardWelcome');
    const content = document.getElementById('dashboardContent');

    if (!username || !role) {
        dashboard.classList.remove('active');
        return;
    }

    welcome.textContent = `Welcome, ${username}! Your role is ${role.replace('_', ' ')}.`;

    let cards = [];

    // Admin permissions
    if (role === 'admin') {
        cards = [
            {
                title: 'Product Management',
                description: 'Add, update and delete store products.',
                action: 'Manage Products',
                target: 'products'
            },
            {
                title: 'Order Management',
                description: 'View and manage customer orders.',
                action: 'View Orders',
                target: 'orderManagement'
            },
            {
                title: 'Reports',
                description: 'View sales reports and store performance.',
                action: 'View Reports',
                target: 'reports'
            },
            {
                title: 'User Management',
                description: 'Manage registered users and their roles.',
                action: 'Manage Users',
                target: 'users'
            },
            {
                title: 'Discount Management',
                description: 'Create and manage product discounts.',
                action: 'Manage Discounts',
                target: 'discounts'
            }
        ];
    }

    // Advanced User permissions
    else if (role === 'advanced_user') {
        cards = [
            {
                title: 'Product Management',
                description: 'Add, update and delete store products.',
                action: 'Manage Products',
                target: 'products'
            },
            {
                title: 'Order Management',
                description: 'View customer orders.',
                action: 'View Orders',
                target: 'orderManagement'
            },
            {
                title: 'Reports',
                description: 'View sales reports and store performance.',
                action: 'View Reports',
                target: 'reports'
            }
        ];
    }

    // Simple User permissions
    else if (role === 'simple_user') {
        cards = [
            {
                title: 'Product Management',
                description: 'Add and update store products.',
                action: 'Manage Products',
                target: 'products'
            }
        ];
    }

    content.innerHTML = cards.map(card => `
        <div class="dashboard-card">
            <h3>${card.title}</h3>
            <p>${card.description}</p>
            <button type="button" data-target="${card.target}">
                ${card.action}
            </button>
        </div>
    `).join('');

    dashboard.classList.add('active');
}
document.addEventListener('click', event => {

    const button = event.target.closest('.dashboard-card button');
    if (!button) return;

    const target = button.dataset.target;
    const section = document.getElementById(target);
    if (target === 'users') {

    const role = localStorage.getItem('role');

    if (role !== 'admin') {
        alert('Only administrators can manage users.');
        return;
    }

    section.classList.add('active');
    loadUsers();
    section.scrollIntoView({ behavior: 'smooth' });

    return;
}

    if (target === 'reports') {

    const role = localStorage.getItem('role');

    if (!['admin', 'advanced_user'].includes(role)) {
        alert('You do not have permission to view reports.');
        return;
    }

    section.classList.add('active');
    loadReports();
    section.scrollIntoView({ behavior: 'smooth' });

    return;
}

  if (section) {
    section.classList.add('active');

    if (target === 'orderManagement') {
    loadAllOrders();
}

if (target === 'discounts') {
    loadDiscounts();
}

    section.scrollIntoView({ behavior: 'smooth' });
}
});
// ==============================
// USER LOGOUT
// ==============================

document.addEventListener('click', event => {

    const logoutButton = event.target.closest('#logoutButton');

    if (!logoutButton) return;

    // Clear all login information
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    localStorage.removeItem('role');

    // Hide account-specific sections
    document.getElementById('dashboard').classList.remove('active');
    document.getElementById('reports').classList.remove('active');
    document.getElementById('users').classList.remove('active');
    document.getElementById('my-orders').classList.remove('active');

    // Clear account-specific content
    document.getElementById('dashboardContent').innerHTML = '';
    document.getElementById('myOrdersContainer').innerHTML = '';

    // Update account and navigation
    updateAccountButton();
    updateNavigation();
    updateProductManagementToolbar();
    // Return to homepage and reload
    window.location.href = '/#home';
    window.location.reload();

});
// ==============================
// LOAD SALES REPORTS
// ==============================

async function loadReports() {

    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');

    if (!token || !['admin', 'advanced_user'].includes(role)) {
        alert('You do not have permission to view reports.');
        return;
    }

    try {
        await Promise.all([
            loadDailyReports(token),
            loadMonthlyReports(token),
            loadTopProductsReports(token)
        ]);

    } catch (error) {
        console.error('Reports error:', error);
    }
}


// ==============================
// DAILY EARNINGS
// ==============================

async function loadDailyReports(token) {

    const container = document.getElementById('dailyReports');

    try {
        const response = await fetch(`${API_URL}/reports/daily-earnings`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Could not load daily reports.');
        }

        const reports = data.earnings || [];

        if (reports.length === 0) {
            container.innerHTML = '<p>No daily earnings available yet.</p>';
            return;
        }

        container.innerHTML = reports.map(report => `
            <div class="report-row">
                <span>${escapeHTML(String(report.date))}</span>
                <strong>€${Number(report.total_earnings).toFixed(2)}</strong>
            </div>
        `).join('');

    } catch (error) {
        container.innerHTML = '<p>Could not load daily earnings.</p>';
        console.error(error);
    }
}


// ==============================
// MONTHLY EARNINGS
// ==============================

async function loadMonthlyReports(token) {

    const container = document.getElementById('monthlyReports');

    try {
        const response = await fetch(`${API_URL}/reports/monthly-earnings`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Could not load monthly reports.');
        }

        const reports = data.earnings || [];

        if (reports.length === 0) {
            container.innerHTML = '<p>No monthly earnings available yet.</p>';
            return;
        }

        container.innerHTML = reports.map(report => `
            <div class="report-row">
                <span>${escapeHTML(String(report.year))}-${escapeHTML(String(report.month))}</span>
                <strong>€${Number(report.total_earnings).toFixed(2)}</strong>
            </div>
        `).join('');

    } catch (error) {
        container.innerHTML = '<p>Could not load monthly earnings.</p>';
        console.error(error);
    }
}


// ==============================
// TOP-SELLING PRODUCTS
// ==============================

async function loadTopProductsReports(token) {

    const container = document.getElementById('topProductsReports');

    try {
        const response = await fetch(`${API_URL}/reports/top-products`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Could not load top-selling products.');
        }

        const reports = Array.isArray(data) ? data : data.products || [];

        if (reports.length === 0) {
            container.innerHTML = '<p>No product sales available yet.</p>';
            return;
        }

        container.innerHTML = reports.map(product => `
            <div class="report-row">
                <span>${escapeHTML(product.product_name)}</span>
                <strong>${Number(product.quantity_sold)} sold</strong>
            </div>
        `).join('');

    } catch (error) {
        container.innerHTML = '<p>Could not load top-selling products.</p>';
        console.error(error);
    }
}
// ==============================
// LOAD USERS
// ==============================

async function loadUsers() {

    const container = document.getElementById('usersContainer');
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');

    if (!token || role !== 'admin') {
        container.innerHTML = '<p>You do not have permission to view users.</p>';
        return;
    }

    container.innerHTML = '<p>Loading users...</p>';

    try {

        const response = await fetch(`${API_URL}/users`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const users = await response.json();

        if (!response.ok) {
            throw new Error(users.error || 'Could not load users.');
        }

        displayUsers(users);

    } catch (error) {

        container.innerHTML = '<p>Could not load users.</p>';
        console.error('Users error:', error);
    }
}
function displayUsers(users) {

    const container = document.getElementById('usersContainer');

    if (!users || users.length === 0) {
        container.innerHTML = '<p>No registered users found.</p>';
        return;
    }

    container.innerHTML = `
        <table class="users-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Actions</th>
                </tr>
            </thead>

            <tbody>
                ${users.map(user => `
                    <tr>
                        <td>${user.id}</td>
                        <td>${escapeHTML(user.username)}</td>
                        <td>${escapeHTML(user.email)}</td>

                        <td>
                            <select class="user-role-select" data-id="${user.id}">
                                <option value="admin" ${user.role === 'admin' ? 'selected' : ''}>Admin</option>
                                <option value="advanced_user" ${user.role === 'advanced_user' ? 'selected' : ''}>Advanced User</option>
                                <option value="simple_user" ${user.role === 'simple_user' ? 'selected' : ''}>Simple User</option>
                            </select>
                        </td>

                        <td>
                            <button class="update-user-role" data-id="${user.id}">
                                SAVE
                            </button>

                            <button class="delete-user" data-id="${user.id}">
                                DELETE
                            </button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}
// ==============================
// OPEN AND CLOSE ADD PRODUCT MODAL
// ==============================

document.addEventListener('click', async event => {

    if (event.target.closest('#addProductButton')) {
        document.getElementById('productModalOverlay').classList.add('active');
        await loadProductOptions();
    }

    if (event.target.closest('#closeProductModal')) {
        document.getElementById('productModalOverlay').classList.remove('active');
    }

    if (event.target.id === 'productModalOverlay') {
        event.target.classList.remove('active');
    }

});

// Load product form options
async function loadProductOptions() {
const token = localStorage.getItem('token');
    const lookups = {
        productBrand: 'brands',
        productCategory: 'categories',
        productGender: 'genders',
        productSizes: 'sizes',
        productColors: 'colors'
    };

    for (const [elementId, lookupType] of Object.entries(lookups)) {

        const response = await fetch(`/api/lookups/${lookupType}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            console.error(`Could not load ${lookupType}`);
            continue;
        }

        const select = document.getElementById(elementId);

        select.innerHTML = '';

        if (elementId !== 'productSizes' && elementId !== 'productColors') {
            select.innerHTML = '<option value="">Select</option>';
        }

        data.items.forEach(item => {
            const option = document.createElement('option');

            option.value = item.id;
            option.textContent = item.name;

            select.appendChild(option);
        });
    }
}// ADD AND EDIT PRODUCT

document.getElementById('addProductForm').addEventListener('submit', async event => {

    event.preventDefault();

    const token = localStorage.getItem('token');
    const errorMessage = document.getElementById('productFormError');

    const productData = {
        name: document.getElementById('productName').value.trim(),
        description: document.getElementById('productDescription').value.trim(),
        price: Number(document.getElementById('productPrice').value),
        quantity: Number(document.getElementById('productQuantity').value),
        brand_id: Number(document.getElementById('productBrand').value),
        category_id: Number(document.getElementById('productCategory').value),
        gender_id: Number(document.getElementById('productGender').value),
        size_ids: Array.from(document.getElementById('productSizes').selectedOptions)
            .map(option => Number(option.value)),
        color_ids: Array.from(document.getElementById('productColors').selectedOptions)
            .map(option => Number(option.value))
    };

    try {

        const url = editingProductId
            ? `${API_URL}/products/${editingProductId}`
            : `${API_URL}/products`;

        const response = await fetch(url, {
            method: editingProductId ? 'PUT' : 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(productData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Could not save product.');
        }

        alert(editingProductId
            ? 'Product updated successfully!'
            : 'Product added successfully!');

        editingProductId = null;

        document.getElementById('addProductForm').reset();
        document.getElementById('productModalOverlay').classList.remove('active');
        document.getElementById('productModalTitle').textContent = 'Add New Product';
        document.getElementById('saveProductButton').textContent = 'SAVE PRODUCT';

        await loadProducts();

    } catch (error) {

        errorMessage.textContent = error.message;
        console.error('Product save error:', error);

    }

});// EDIT PRODUCT BUTTON

document.addEventListener('click', async event => {

    const button = event.target.closest('.edit-product-button');

    if (!button) return;

    const productId = Number(button.dataset.productId);
    const product = allProducts.find(item => Number(item.id) === productId);

    if (!product) return;

    editingProductId = productId;

    await loadProductOptions();

    document.getElementById('productModalTitle').textContent = 'Edit Product';
    document.getElementById('saveProductButton').textContent = 'UPDATE PRODUCT';

    document.getElementById('productName').value = product.name;
    document.getElementById('productDescription').value = product.description || '';
    document.getElementById('productPrice').value = product.price;
    document.getElementById('productQuantity').value = product.total_quantity;

    const selectOption = (id, name) => {
        const select = document.getElementById(id);
        const option = [...select.options].find(item => item.textContent === name);

        if (option) select.value = option.value;
    };

    selectOption('productBrand', product.brand);
    selectOption('productCategory', product.category);
    selectOption('productGender', product.gender);

    ['productSizes', 'productColors'].forEach(id => {

        const names = id === 'productSizes' ? product.sizes : product.colors;
        const select = document.getElementById(id);

        [...select.options].forEach(option => {
            option.selected = names.includes(option.textContent);
        });

    });

    document.getElementById('productModalOverlay').classList.add('active');

});
// DELETE PRODUCT

document.addEventListener('click', async event => {

    const button = event.target.closest('.delete-product-button');

    if (!button) return;

    const productId = button.dataset.productId;

    if (!confirm('Are you sure you want to delete this product?')) {
        return;
    }

    try {

        const response = await fetch(`${API_URL}/products/${productId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Could not delete product.');
        }

        alert('Product deleted successfully!');

        await loadProducts();

    } catch (error) {

        alert(error.message);
        console.error('Delete product error:', error);

    }

});
// LOAD ALL ORDERS

async function loadAllOrders() {

    const container = document.getElementById('allOrdersContainer');

    container.innerHTML = 'Loading orders...';

    try {

        const response = await fetch(`${API_URL}/orders`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Could not load orders.');
        }

        const orders = Array.isArray(data) ? data : data.orders || [];

        if (orders.length === 0) {
            container.innerHTML = '<p>No orders found.</p>';
            return;
        }

        container.innerHTML = orders.map(order => `

            <div class="order-card">

                <h3>Order #${order.id}</h3>

                <p>Date: ${new Date(order.order_date).toLocaleString()}</p>

                <p>Status: <strong>${escapeHTML(order.status)}</strong></p>

                <div class="order-products">
                    ${order.items.map(item => `
                        <div>
                            ${escapeHTML(item.product_name)} × ${item.quantity}
                        </div>
                    `).join('')}
                </div>

                <p>
                    Total: €${Number(order.total_amount).toFixed(2)}
                </p>

                <select id="orderStatus${order.id}">
                    ${['pending', 'confirmed', 'shipped', 'cancelled'].map(status => `
                        <option value="${status}"
                            ${order.status === status ? 'selected' : ''}>
                            ${status.charAt(0).toUpperCase() + status.slice(1)}
                        </option>
                    `).join('')}
                </select>

                <button class="update-order-status-button"
                    data-order-id="${order.id}">
                    UPDATE STATUS
                </button>

            </div>

        `).join('');

    } catch (error) {

        container.innerHTML = `<p>${escapeHTML(error.message)}</p>`;
        console.error('Load orders error:', error);

    }
}// UPDATE ORDER STATUS

document.addEventListener('click', async event => {

    const button = event.target.closest('.update-order-status-button');

    if (!button) return;

    const orderId = button.dataset.orderId;
    const status = document.getElementById(`orderStatus${orderId}`).value;

    try {

        const response = await fetch(`${API_URL}/orders/${orderId}/status`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ status: status })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Could not update order status.');
        }

        alert('Order status updated successfully!');

        await loadAllOrders();
        await loadProducts();

    } catch (error) {

        alert(error.message);
        console.error('Update status error:', error);

    }

});
// ==============================
// LOAD DISCOUNTS
// ==============================

async function loadDiscounts() {
    const container = document.getElementById('discountsContainer');

    container.innerHTML = 'Loading discounts...';

    try {
        const token = localStorage.getItem('token');

        const response = await fetch(`${API_URL}/products`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Could not load products.');
        }

        const products = Array.isArray(data) ? data : data.products || [];

        let discounts = [];

        for (const product of products) {
            const result = await fetch(`${API_URL}/products/${product.id}/discounts`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            const discountData = await result.json();

            if (result.ok && discountData.discounts) {
                discounts.push(...discountData.discounts);
            }
        }

        if (discounts.length === 0) {
            container.innerHTML = '<p>No discounts found.</p>';
            return;
        }

        container.innerHTML = discounts.map(discount => `
            <div class="order-card">
                <h3>${escapeHTML(discount.product_name)}</h3>
                <p>Discount: ${discount.percentage}%</p>
                <p>Start: ${new Date(discount.start_date).toLocaleString()}</p>
                <p>End: ${new Date(discount.end_date).toLocaleString()}</p>
                <button class="edit-discount-button" data-id="${discount.id}">
                    EDIT
                </button>
                <button class="delete-discount-button" data-id="${discount.id}">
                    DELETE
                </button>
            </div>
        `).join('');

    } catch (error) {
        container.innerHTML = `<p>${escapeHTML(error.message)}</p>`;
        console.error('Load discounts error:', error);
    }
}document.getElementById('refreshDiscounts').addEventListener('click', loadDiscounts);
// ==============================
// DISCOUNT MODAL
// ==============================

document.getElementById('addDiscountButton').addEventListener('click', async () => {

    const token = localStorage.getItem('token');
    const select = document.getElementById('discountProduct');

    const response = await fetch(`${API_URL}/products`);
    const data = await response.json();

    const products = Array.isArray(data) ? data : data.products || [];

    select.innerHTML = '<option value="">Select Product</option>';

    products.forEach(product => {
        const option = document.createElement('option');
        option.value = product.id;
        option.textContent = product.name;
        select.appendChild(option);
    });

    document.getElementById('discountForm').reset();
    document.getElementById('discountModalTitle').textContent = 'Add Discount';
    document.getElementById('discountModalOverlay').classList.add('active');
});

document.getElementById('closeDiscountModal').addEventListener('click', () => {
    document.getElementById('discountModalOverlay').classList.remove('active');
});// ==============================
// SAVE DISCOUNT
// ==============================

document.getElementById('discountForm').addEventListener('submit', async event => {

    event.preventDefault();

    const productId = document.getElementById('discountProduct').value;
    const error = document.getElementById('discountError');

    const discount = {
        percentage: document.getElementById('discountPercentage').value,
        start_date: document.getElementById('discountStart').value,
        end_date: document.getElementById('discountEnd').value
    };

    try {
        const url = editingDiscountId
            ? `${API_URL}/discounts/${editingDiscountId}`
            : `${API_URL}/products/${productId}/discounts`;

        const response = await fetch(url, {
            method: editingDiscountId ? 'PUT' : 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify(discount)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Could not save discount.');
        }

        alert(editingDiscountId
            ? 'Discount updated successfully!'
            : 'Discount created successfully!');

        editingDiscountId = null;

        document.getElementById('discountProduct').disabled = false;
        document.getElementById('discountModalOverlay').classList.remove('active');
        document.getElementById('discountForm').reset();

        await loadDiscounts();
        await loadProducts();

    } catch (err) {
        error.textContent = err.message;
    }
});// ==============================
// EDIT DISCOUNT
// ==============================

let editingDiscountId = null;

document.addEventListener('click', async event => {

    const button = event.target.closest('.edit-discount-button');

    if (!button) return;

    editingDiscountId = button.dataset.id;

    try {
        const response = await fetch(`${API_URL}/discounts/${editingDiscountId}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Could not load discount.');
        }

        // Load products
        const productsResponse = await fetch(`${API_URL}/products`);
        const productsData = await productsResponse.json();

        const select = document.getElementById('discountProduct');

        select.innerHTML = '<option value="">Select Product</option>';

        productsData.products.forEach(product => {
            const option = document.createElement('option');
            option.value = product.id;
            option.textContent = product.name;
            select.appendChild(option);
        });

        // Fill discount information
        const discount = data.discount;

        select.value = discount.product_id;

        document.getElementById('discountPercentage').value = discount.percentage;
        document.getElementById('discountStart').value = discount.start_date.slice(0, 16);
        document.getElementById('discountEnd').value = discount.end_date.slice(0, 16);

        document.getElementById('discountModalTitle').textContent = 'Edit Discount';
        document.getElementById('discountModalOverlay').classList.add('active');

    } catch (error) {
        alert(error.message);
    }
});

// ==============================
// DELETE DISCOUNT
// ==============================

document.addEventListener('click', async event => {

    const button = event.target.closest('.delete-discount-button');

    if (!button) return;

    const discountId = button.dataset.id;

    if (!confirm('Are you sure you want to delete this discount?')) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/discounts/${discountId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Could not delete discount.');
        }

        alert('Discount deleted successfully!');

        await loadDiscounts();
        await loadProducts();

    } catch (error) {
        alert(error.message);
    }
});
document.addEventListener('click', event => {

    const button = event.target.closest('#cartButton');

    if (!button) return;

    displayCart();

    document.getElementById('cartPanel').classList.add('active');
    document.getElementById('cartOverlay').classList.add('active');

});
// UPDATE USER ROLE
document.addEventListener('click', async event => {

    const button = event.target.closest('.update-user-role');

    if (!button) return;

    const userId = button.dataset.id;
    const role = document.querySelector(
        `.user-role-select[data-id="${userId}"]`
    ).value;

    const token = localStorage.getItem('token');

    try {
        const response = await fetch(`${API_URL}/users/${userId}/role`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ role })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Could not update role.');
        }

        alert('User role updated successfully!');
        loadUsers();

    } catch (error) {
        alert(error.message);
    }
});


// DELETE USER
document.addEventListener('click', async event => {

    const button = event.target.closest('.delete-user');

    if (!button) return;

    if (!confirm('Are you sure you want to delete this user?')) {
        return;
    }

    const userId = button.dataset.id;
    const token = localStorage.getItem('token');

    try {
        const response = await fetch(`${API_URL}/users/${userId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Could not delete user.');
        }

        alert('User deleted successfully!');
        loadUsers();

    } catch (error) {
        alert(error.message);
    }
});
// SHOW ADD USER FORM
document.getElementById('addUserButton').addEventListener('click', () => {
    document.getElementById('addUserForm').style.display = 'block';
});

// CANCEL
document.getElementById('cancelAddUser').addEventListener('click', () => {
    document.getElementById('addUserForm').style.display = 'none';
});


// CREATE USER
document.getElementById('saveNewUser').addEventListener('click', async () => {

    const username = document.getElementById('newUsername').value.trim();
    const email = document.getElementById('newEmail').value.trim();
    const password = document.getElementById('newPassword').value;
    const role = document.getElementById('newUserRole').value;
    const error = document.getElementById('addUserError');

    const token = localStorage.getItem('token');

    error.textContent = '';

    try {
        const response = await fetch(`${API_URL}/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ username, email, password, role })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Could not create user.');
        }

        alert('User created successfully!');

        document.getElementById('addUserForm').style.display = 'none';
        document.getElementById('newUsername').value = '';
        document.getElementById('newEmail').value = '';
        document.getElementById('newPassword').value = '';

        loadUsers();

    } catch (err) {
        error.textContent = err.message;
    }
});// UPDATE PRODUCT MANAGEMENT TOOLBAR
function updateProductManagementToolbar() {

    const toolbar = document.getElementById('productManagementToolbar');

    if (!toolbar) return;

    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');

    if (token && ['admin', 'advanced_user', 'simple_user'].includes(role)) {
        toolbar.style.display = 'flex';
    } else {
        toolbar.style.display = 'none';
    }
}

// ==============================
// REGISTER USER
// ==============================

// Switch between Login and Register
document.getElementById('showRegister').addEventListener('click', event => {
    event.preventDefault();

    document.getElementById('loginSection').style.display = 'none';
    document.getElementById('registerSection').style.display = 'block';
});

document.getElementById('showLogin').addEventListener('click', event => {
    event.preventDefault();

    document.getElementById('registerSection').style.display = 'none';
    document.getElementById('loginSection').style.display = 'block';
});

// Register new user
document.getElementById('registerForm').addEventListener('submit', async event => {
    event.preventDefault();

    const username = document.getElementById('registerUsername').value.trim();
    const email = document.getElementById('registerEmail').value.trim();
    const password = document.getElementById('registerPassword').value;

    const error = document.getElementById('registerError');

    error.textContent = '';

    try {
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Registration failed.');
        }

        alert('Account created successfully! You can now sign in.');

        document.getElementById('registerForm').reset();
        document.getElementById('registerSection').style.display = 'none';
        document.getElementById('loginSection').style.display = 'block';

    } catch (err) {
        error.textContent = err.message;
    }
});
