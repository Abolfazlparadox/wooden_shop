// static/js/product.js
document.addEventListener('DOMContentLoaded', function() {
    // --- تغییر عکس با کلیک روی تامنیل‌ها ---
    const mainImage = document.getElementById('main-image');
    document.querySelectorAll('.thumbnail-container').forEach(thumb => {
        thumb.addEventListener('click', function() {
            mainImage.src = this.dataset.imageUrl;
            document.querySelectorAll('.thumbnail-container').forEach(t => t.classList.remove('border-walnut-900', 'dark:border-walnut-700'));
            this.classList.add('border-walnut-900', 'dark:border-walnut-700');
        });
    });

    // --- آپدیت داینامیک قیمت، موجودی و آدرس سبد خرید ---
    const updateProductDetails = (selectedRadio) => {
        if (!selectedRadio) return;
        const price = parseInt(selectedRadio.dataset.price);
        const stock = parseInt(selectedRadio.dataset.stock);
        const variationId = selectedRadio.value;

        // فرمت کردن قیمت با ویرگول (سه تا سه تا)
        document.getElementById('main-price').innerText = price.toLocaleString('fa-IR') + ' تومان';

        // آپدیت وضعیت موجودی
        const stockBadge = document.getElementById('stock-badge');
        if (stock > 0) {
            stockBadge.innerText = 'موجود در انبار';
            stockBadge.className = 'bg-green-100 text-green-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-green-900 dark:text-green-300';
        } else {
            stockBadge.innerText = 'ناموجود';
            stockBadge.className = 'bg-red-100 text-red-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300';
        }

        // آپدیت لینک فرم برای ثبت در سبد خرید
        const form = document.getElementById('add-to-cart-form');
        const baseUrl = form.dataset.baseUrl;
        form.action = baseUrl.replace('/0/', '/' + variationId + '/');
    };

    const radios = document.querySelectorAll('input[name="variation"]');
    radios.forEach(radio => radio.addEventListener('change', () => updateProductDetails(radio)));

    // اجرای آپدیت برای گزینه‌ای که به صورت پیش‌فرض انتخاب شده
    const checkedRadio = document.querySelector('input[name="variation"]:checked');
    if (checkedRadio) updateProductDetails(checkedRadio);

    // --- دکمه‌های کم و زیاد کردن تعداد ---
    const qtyInput = document.getElementById('quantity-input');
    document.getElementById('quantity-plus').addEventListener('click', () => {
        qtyInput.value = parseInt(qtyInput.value) + 1;
    });
    document.getElementById('quantity-minus').addEventListener('click', () => {
        if (parseInt(qtyInput.value) > 1) {
            qtyInput.value = parseInt(qtyInput.value) - 1;
        }
    });

    // --- لایت‌باکس (فول اسکرین کردن عکس) ---
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

    // --- افکت زوم (بزرگنمایی) ---
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
});