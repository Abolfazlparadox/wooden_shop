// static/js/product.js
document.addEventListener('DOMContentLoaded', function() {
    const mainImage = document.getElementById('main-image');
    const mainPriceDisplay = document.getElementById('main-price');
    const stockBadge = document.getElementById('stock-badge');
    const addToCartForm = document.getElementById('add-to-cart-form');
    const quantityInput = document.getElementById('quantity-input');

    const toPersianDigits = (str) => {
        const persian = { '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴', '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹' };
        return str.toString().replace(/[0-9]/g, (w) => persian[w]);
    };

    const updateProductDetails = (selectedRadio) => {
        if (!selectedRadio) return;

        // Safely parse the unlocalized integer from data attribute
        const priceStr = selectedRadio.dataset.price.toString().replace(/,/g, '').replace(/٬/g, '');
        const price = parseInt(priceStr, 10);
        const stock = parseInt(selectedRadio.dataset.stock.toString(), 10);
        const variationId = selectedRadio.value;

        // Update main price display using Persian locale
        if (mainPriceDisplay) {
            mainPriceDisplay.innerText = price.toLocaleString('fa-IR') + ' تومان';
        }

        // Update stock badge
        if (stockBadge) {
            if (stock > 0) {
                stockBadge.innerText = 'موجود در انبار';
                stockBadge.className = 'bg-green-100 text-green-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-green-900 dark:text-green-300';
            } else {
                stockBadge.innerText = 'ناموجود';
                stockBadge.className = 'bg-red-100 text-red-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300';
            }
        }

        // Dynamically update form action URL
        if (addToCartForm) {
            const baseUrl = addToCartForm.dataset.baseUrl;
            addToCartForm.action = baseUrl.replace('/0/', '/' + variationId + '/');
        }
    };

    document.querySelectorAll('input[name="variation"]').forEach(radio => {
        radio.addEventListener('change', () => updateProductDetails(radio));
    });

    const initiallyChecked = document.querySelector('input[name="variation"]:checked');
    if (initiallyChecked) {
        updateProductDetails(initiallyChecked);
    }

    // --- Quantity Selector ---
    document.getElementById('quantity-plus').addEventListener('click', () => quantityInput.stepUp());
    document.getElementById('quantity-minus').addEventListener('click', () => quantityInput.stepDown());

    // --- Image Gallery & Lightbox ---
    const thumbnails = document.querySelectorAll('.thumbnail-container');
    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', function() {
            mainImage.src = this.dataset.imageUrl;
            thumbnails.forEach(t => t.classList.remove('border-walnut-900', 'dark:border-walnut-700'));
            this.classList.add('border-walnut-900', 'dark:border-walnut-700');
        });
    });
    
    const lightbox = document.getElementById('lightbox-overlay');
    const lightboxImg = document.getElementById('lightbox-image');
    document.getElementById('main-image-container').addEventListener('click', () => {
        lightboxImg.src = mainImage.src;
        lightbox.classList.remove('hidden');
        lightbox.classList.add('flex');
    });
    document.getElementById('lightbox-close').addEventListener('click', () => {
        lightbox.classList.remove('flex');
        lightbox.classList.add('hidden');
    });
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) {
            lightbox.classList.remove('flex');
            lightbox.classList.add('hidden');
        }
    });

    // --- Image Zoomer ---
    const zoomer = document.getElementById('main-image-container');
    const lens = document.getElementById('zoom-lens');
    const zoomedImg = document.getElementById('zoomed-image');
    zoomer.addEventListener('mousemove', (e) => {
        const rect = zoomer.getBoundingClientRect();
        let x = e.clientX - rect.left - (lens.offsetWidth / 2);
        let y = e.clientY - rect.top - (lens.offsetHeight / 2);

        if (x > zoomer.offsetWidth - lens.offsetWidth) x = zoomer.offsetWidth - lens.offsetWidth;
        if (x < 0) x = 0;
        if (y > zoomer.offsetHeight - lens.offsetHeight) y = zoomer.offsetHeight - lens.offsetHeight;
        if (y < 0) y = 0;

        lens.style.left = x + 'px';
        lens.style.top = y + 'px';

        const fx = zoomedImg.offsetWidth / lens.offsetWidth;
        const fy = zoomedImg.offsetHeight / lens.offsetHeight;

        zoomedImg.style.backgroundImage = `url('${mainImage.src}')`;
        zoomedImg.style.backgroundSize = `${zoomer.offsetWidth * fx}px ${zoomer.offsetHeight * fy}px`;
        zoomedImg.style.backgroundPosition = `-${x * fx}px -${y * fy}px`;
    });

    // --- Global Persian Digit Converter ---
    const convertAllDigitsToPersian = () => {
        document.querySelectorAll('.price, .intcomma, #main-price, #stock-badge, .quantity-selector input').forEach(el => {
            el.textContent = toPersianDigits(el.textContent);
            if(el.value) el.value = toPersianDigits(el.value);
        });
    };
    // convertAllDigitsToPersian(); // Uncomment if you want to force all numbers to be Persian
});
