// 产品数据
const products = [
    {
        id: 1,
        name: 'iPhone 15 Pro Max',
        category: 'electronics',
        price: 9999,
        rating: 4.8,
        reviews: 1256,
        image: 'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=500',
        badge: '热销'
    },
    {
        id: 2,
        name: 'MacBook Pro M3',
        category: 'electronics',
        price: 15999,
        rating: 4.9,
        reviews: 892,
        image: 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500',
        badge: '新品'
    },
    {
        id: 3,
        name: 'AirPods Pro 2',
        category: 'electronics',
        price: 1999,
        rating: 4.7,
        reviews: 2341,
        image: 'https://images.unsplash.com/photo-1606841837239-c5a1a4a07af7?w=500',
        badge: ''
    },
    {
        id: 4,
        name: '高端羊绒大衣',
        category: 'fashion',
        price: 3999,
        rating: 4.6,
        reviews: 567,
        image: 'https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=500',
        badge: '热销'
    },
    {
        id: 5,
        name: '真皮手提包',
        category: 'fashion',
        price: 2599,
        rating: 4.5,
        reviews: 432,
        image: 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=500',
        badge: ''
    },
    {
        id: 6,
        name: '瑞士机械腕表',
        category: 'fashion',
        price: 8999,
        rating: 4.9,
        reviews: 789,
        image: 'https://images.unsplash.com/photo-1523170335258-f5ed11844a49?w=500',
        badge: '限量'
    },
    {
        id: 7,
        name: '智能咖啡机',
        category: 'home',
        price: 4599,
        rating: 4.7,
        reviews: 634,
        image: 'https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=500',
        badge: '新品'
    },
    {
        id: 8,
        name: '北欧风沙发',
        category: 'home',
        price: 12999,
        rating: 4.8,
        reviews: 456,
        image: 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=500',
        badge: ''
    },
    {
        id: 9,
        name: '空气净化器',
        category: 'home',
        price: 2899,
        rating: 4.6,
        reviews: 1123,
        image: 'https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=500',
        badge: '热销'
    },
    {
        id: 10,
        name: 'SK-II神仙水',
        category: 'beauty',
        price: 1299,
        rating: 4.8,
        reviews: 3456,
        image: 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=500',
        badge: '经典'
    },
    {
        id: 11,
        name: 'LA MER面霜',
        category: 'beauty',
        price: 2599,
        rating: 4.9,
        reviews: 2789,
        image: 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=500',
        badge: '奢华'
    },
    {
        id: 12,
        name: 'Dior口红套装',
        category: 'beauty',
        price: 899,
        rating: 4.7,
        reviews: 4567,
        image: 'https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=500',
        badge: '热销'
    }
];

// 购物车数组
let cart = [];

// DOM 元素
const productsGrid = document.getElementById('productsGrid');
const cartBtn = document.getElementById('cartBtn');
const cartSidebar = document.getElementById('cartSidebar');
const closeCartBtn = document.getElementById('closeCartBtn');
const overlay = document.getElementById('overlay');
const cartCount = document.getElementById('cartCount');
const cartItems = document.getElementById('cartItems');
const totalPrice = document.getElementById('totalPrice');
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileMenu = document.getElementById('mobileMenu');
const closeMenuBtn = document.getElementById('closeMenuBtn');
const backToTop = document.getElementById('backToTop');
const filterBtns = document.querySelectorAll('.filter-btn');

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    renderProducts(products);
    initEventListeners();
    initScrollAnimations();
    initSmoothScroll();
});

// 渲染产品
function renderProducts(productsToRender) {
    productsGrid.innerHTML = productsToRender.map(product => `
        <div class="product-card" data-category="${product.category}">
            <div class="product-image">
                <img src="${product.image}" alt="${product.name}" loading="lazy">
                ${product.badge ? `<div class="product-badge">${product.badge}</div>` : ''}
                <div class="product-actions">
                    <button class="action-btn" onclick="addToCart(${product.id})">
                        <i class="fas fa-shopping-cart"></i>
                    </button>
                    <button class="action-btn">
                        <i class="fas fa-heart"></i>
                    </button>
                </div>
            </div>
            <div class="product-info">
                <div class="product-category">${getCategoryName(product.category)}</div>
                <h3 class="product-title">${product.name}</h3>
                <div class="product-rating">
                    <div class="stars">
                        ${getStars(product.rating)}
                    </div>
                    <span class="rating-count">(${product.reviews})</span>
                </div>
                <div class="product-footer">
                    <div class="product-price">¥${product.price.toLocaleString()}</div>
                    <button class="add-to-cart-btn" onclick="addToCart(${product.id})">
                        加入购物车
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// 获取分类名称
function getCategoryName(category) {
    const names = {
        electronics: '电子产品',
        fashion: '时尚服饰',
        home: '家居生活',
        beauty: '美妆护肤'
    };
    return names[category] || category;
}

// 生成星级评分
function getStars(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    let stars = '';

    for (let i = 0; i < fullStars; i++) {
        stars += '<i class="fas fa-star"></i>';
    }

    if (hasHalfStar) {
        stars += '<i class="fas fa-star-half-alt"></i>';
    }

    const emptyStars = 5 - Math.ceil(rating);
    for (let i = 0; i < emptyStars; i++) {
        stars += '<i class="far fa-star"></i>';
    }

    return stars;
}

// 添加到购物车
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    const existingItem = cart.find(item => item.id === productId);

    if (existingItem) {
        existingItem.quantity++;
    } else {
        cart.push({
            ...product,
            quantity: 1
        });
    }

    updateCart();
    showNotification('商品已添加到购物车！');
}

// 更新购物车
function updateCart() {
    // 更新购物车计数
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;
    cartCount.style.display = totalItems > 0 ? 'block' : 'none';

    // 渲染购物车项目
    if (cart.length === 0) {
        cartItems.innerHTML = `
            <div class="empty-cart">
                <i class="fas fa-shopping-cart"></i>
                <p>购物车是空的</p>
            </div>
        `;
    } else {
        cartItems.innerHTML = cart.map(item => `
            <div class="cart-item">
                <div class="cart-item-image">
                    <img src="${item.image}" alt="${item.name}">
                </div>
                <div class="cart-item-info">
                    <div class="cart-item-title">${item.name}</div>
                    <div class="cart-item-price">¥${item.price.toLocaleString()}</div>
                    <div class="cart-item-controls">
                        <button class="quantity-btn" onclick="updateQuantity(${item.id}, -1)">
                            <i class="fas fa-minus"></i>
                        </button>
                        <span>${item.quantity}</span>
                        <button class="quantity-btn" onclick="updateQuantity(${item.id}, 1)">
                            <i class="fas fa-plus"></i>
                        </button>
                        <button class="remove-item-btn" onclick="removeFromCart(${item.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }

    // 更新总价
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    totalPrice.textContent = `¥${total.toLocaleString()}`;
}

// 更新商品数量
function updateQuantity(productId, change) {
    const item = cart.find(item => item.id === productId);
    if (item) {
        item.quantity += change;
        if (item.quantity <= 0) {
            removeFromCart(productId);
        } else {
            updateCart();
        }
    }
}

// 从购物车移除
function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    updateCart();
}

// 显示通知
function showNotification(message) {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 90px;
        right: 20px;
        background: white;
        padding: 1rem 2rem;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 2000);
}

// 初始化事件监听器
function initEventListeners() {
    // 购物车按钮
    cartBtn.addEventListener('click', () => {
        cartSidebar.classList.add('active');
        overlay.classList.add('active');
    });

    closeCartBtn.addEventListener('click', () => {
        cartSidebar.classList.remove('active');
        overlay.classList.remove('active');
    });

    // 移动端菜单
    mobileMenuBtn.addEventListener('click', () => {
        mobileMenu.classList.add('active');
        overlay.classList.add('active');
    });

    closeMenuBtn.addEventListener('click', () => {
        mobileMenu.classList.remove('active');
        overlay.classList.remove('active');
    });

    // 遮罩层
    overlay.addEventListener('click', () => {
        cartSidebar.classList.remove('active');
        mobileMenu.classList.remove('active');
        overlay.classList.remove('active');
    });

    // 返回顶部
    backToTop.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // 滚动监听
    window.addEventListener('scroll', () => {
        // 导航栏滚动效果
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.boxShadow = '0 4px 20px rgba(0,0,0,0.1)';
        } else {
            navbar.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
        }

        // 返回顶部按钮
        if (window.scrollY > 300) {
            backToTop.classList.add('show');
        } else {
            backToTop.classList.remove('show');
        }
    });

    // 产品筛选
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // 更新激活状态
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // 筛选产品
            const category = btn.dataset.category;
            const filteredProducts = category === 'all'
                ? products
                : products.filter(p => p.category === category);

            renderProducts(filteredProducts);
        });
    });

    // 移动端导航链接
    document.querySelectorAll('.mobile-nav-link').forEach(link => {
        link.addEventListener('click', () => {
            mobileMenu.classList.remove('active');
            overlay.classList.remove('active');
        });
    });

    // 导航链接
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });

    // 表单提交
    const contactForm = document.getElementById('contactForm');
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        showNotification('消息已发送，我们会尽快回复您！');
        contactForm.reset();
    });
}

// 滚动动画
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('aos-animate');
            }
        });
    }, observerOptions);

    document.querySelectorAll('[data-aos]').forEach(el => {
        observer.observe(el);
    });
}

// 平滑滚动
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    const navbarHeight = document.querySelector('.navbar').offsetHeight;
                    const targetPosition = target.offsetTop - navbarHeight;
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
}

// 添加动画样式
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
