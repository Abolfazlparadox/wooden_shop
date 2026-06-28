"""
shop/management/commands/seed_shop.py

Deletes all existing shop data and seeds 5 premium wooden products
with categories, variations, images (from picsum.photos), and tags.

Usage:
    python manage.py seed_shop
    python manage.py seed_shop --skip-cleanup    # keep existing data
"""

import time

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from orders.models import Order
from shop.models import Category, Product, ProductImage, ProductVariation, Tag

# ── picsum seeds (deterministic — same image every run) ──────────────────────
# 6 seeds per product group for up to 3 images each
IMAGE_SEEDS = {
    "table": ["wooden-table-1", "wooden-table-2", "wooden-table-3"],
    "serving": ["wood-serve-1", "wood-serve-2", "wood-serve-3"],
    "board": ["cutboard-1", "cutboard-2", "cutboard-3"],
    "shelf": ["wood-shelf-1", "wood-shelf-2", "wood-shelf-3"],
    "bowl": ["walnut-bowl-1", "walnut-bowl-2", "walnut-bowl-3"],
}

# ── Category tree ─────────────────────────────────────────────────────────────
CATEGORIES = [
    # (name, parent_name or None)
    ("مبلمان چوبی", None),
    ("میز و صندلی", "مبلمان چوبی"),
    ("قفسه و کتابخانه", "مبلمان چوبی"),
    ("ظروف و لوازم آشپزخانه", None),
    ("ظروف سرو و پذیرایی", "ظروف و لوازم آشپزخانه"),
    ("ابزار و لوازم آشپزخانه", "ظروف و لوازم آشپزخانه"),
    ("دکور و تزئین", None),
]

# ── Tags ──────────────────────────────────────────────────────────────────────
TAGS = [
    "چوب گردو",
    "مبلمان",
    "دکوراسیون داخلی",
    "صنایع دستی",
    "ظروف روستیک",
    "هدیه چوبی",
    "آشپزخانه روستیک",
    "چوب اقاقیا",
    "هنر چوب",
    "طراحی خانه",
    "چوب بلوط",
]

# ── Products ──────────────────────────────────────────────────────────────────
PRODUCTS = [
    {
        "title": "میز ناهارخوری روستیک چوب گردو",
        "category": "میز و صندلی",
        "tags": ["چوب گردو", "مبلمان", "دکوراسیون داخلی"],
        "images": IMAGE_SEEDS["table"],
        "description": (
            "میز ناهارخوری روستیک چوب گردو، شاهکاری از هنر صنایع دستی ایرانی است که صمیمیت روستایی را با "
            "زیبایی مدرن درهم می‌آمیزد. هر میز از یک تنه گردوی طبیعی ساخته می‌شود که رگه‌های منحصربه‌فرد آن "
            "داستانی از دهه‌ها رشد را روایت می‌کند.\n\n"
            "صفحه ضخیم این میز با پرداخت دستی و روغن گردوی خالص محافظت شده، که نه‌تنها جلای طبیعی چوب را حفظ "
            "می‌کند بلکه در برابر رطوبت و خراش نیز مقاوم است. پایه‌های فولادی مات با رنگ کوره‌ای سیاه، کنتراستی "
            "شاعرانه با گرمای چوب ایجاد می‌کنند.\n\n"
            "این میز در سه اندازه ارائه می‌شود و برای ۴ تا ۸ نفر مناسب است. مدت آماده‌سازی به دلیل ماهیت "
            "دست‌ساز این محصول ۲۱ روز کاری است. با هر سفارش، یک کیت روغن‌کاری رایگان دریافت می‌کنید."
        ),
        "variations": [
            {
                "sku": "TBL-WLN-120",
                "wood_type": "گردو",
                "dimensions": "۱۲۰×۸۰ سانتیمتر",
                "price": 8_500_000,
                "discount_price": None,
                "stock": 3,
                "prep": 21,
            },
            {
                "sku": "TBL-WLN-140",
                "wood_type": "گردو",
                "dimensions": "۱۴۰×۹۰ سانتیمتر",
                "price": 11_200_000,
                "discount_price": 10_500_000,
                "stock": 2,
                "prep": 21,
            },
            {
                "sku": "TBL-WLN-160",
                "wood_type": "گردو",
                "dimensions": "۱۶۰×۹۰ سانتیمتر",
                "price": 13_800_000,
                "discount_price": None,
                "stock": 1,
                "prep": 28,
            },
        ],
    },
    {
        "title": "ست ظروف پذیرایی چوبی دست‌ساز",
        "category": "ظروف سرو و پذیرایی",
        "tags": ["صنایع دستی", "ظروف روستیک", "هدیه چوبی"],
        "images": IMAGE_SEEDS["serving"],
        "description": (
            "ست ظروف پذیرایی چوبی دست‌ساز، مجموعه‌ای بی‌نظیر برای میهمانی‌های خاص و سفره‌آرایی‌های متمایز. "
            "این ست شامل یک سینی بزرگ، دو کاسه متوسط، چهار زیرلیوانی و یک قاشق سرو بزرگ است.\n\n"
            "تمامی قطعات از چوب اقاقیای یکدست انتخاب شده‌اند تا هماهنگی رنگ و بافت در کل مجموعه حفظ شود. "
            "سطح داخلی ظروف با روغن بذر کتان درجه غذایی پرداخت شده که استفاده آن‌ها را ایمن و بهداشتی می‌کند. "
            "گره‌های طبیعی چوب که در هر قطعه دیده می‌شود، نشانه اصالت و ماهیت طبیعی محصول است.\n\n"
            "این ست به عنوان هدیه ازدواج، افتتاح خانه جدید یا جشن تولد، گزینه‌ای فوق‌العاده و به‌یادماندنی است. "
            "بسته‌بندی لوکس با جعبه چوبی اختصاصی، شأن هدیه را دوچندان می‌کند."
        ),
        "variations": [
            {
                "sku": "SRV-ACA-6PC",
                "wood_type": "اقاقیا",
                "dimensions": "ست ۶ تکه",
                "price": 1_850_000,
                "discount_price": 1_650_000,
                "stock": 8,
                "prep": 7,
            },
            {
                "sku": "SRV-ACA-12PC",
                "wood_type": "اقاقیا",
                "dimensions": "ست ۱۲ تکه",
                "price": 3_200_000,
                "discount_price": None,
                "stock": 5,
                "prep": 10,
            },
        ],
    },
    {
        "title": "تخته برش لوکس چوب اقاقیا",
        "category": "ابزار و لوازم آشپزخانه",
        "tags": ["ظروف روستیک", "آشپزخانه روستیک", "هدیه چوبی", "چوب اقاقیا"],
        "images": IMAGE_SEEDS["board"],
        "description": (
            "تخته برش لوکس چوب اقاقیا، ستاره آشپزخانه‌های مدرن و روستیک است. اقاقیا از سخت‌ترین چوب‌های "
            "موجود است و در برابر خراش چاقو مقاومت فوق‌العاده‌ای دارد؛ در عین حال آنقدر نرم است که لبه تیغه "
            "شما را حفظ کند.\n\n"
            "ساختار اندانه (End-grain) این تخته باعث می‌شود شیارهای ایجادشده توسط چاقو به مرور زمان خودبه‌خود "
            "بسته شوند، که عمر محصول را به میزان قابل توجهی افزایش می‌دهد. رگه‌های طلایی و قهوه‌ای طبیعی "
            "اقاقیا، هر تخته را به یک قطعه هنری منحصربه‌فرد تبدیل کرده است.\n\n"
            "همراه با هر تخته، دستورالعمل نگهداری و یک بطری کوچک روغن معدنی درجه غذایی تقدیم می‌شود. "
            "امکان حکاکی نام یا پیام دلخواه روی تخته وجود دارد (با هزینه اضافی)."
        ),
        "variations": [
            {
                "sku": "CUT-ACA-SM",
                "wood_type": "اقاقیا",
                "dimensions": "۳۵×۲۵ سانتیمتر",
                "price": 580_000,
                "discount_price": None,
                "stock": 15,
                "prep": 3,
            },
            {
                "sku": "CUT-ACA-MD",
                "wood_type": "اقاقیا",
                "dimensions": "۴۵×۳۰ سانتیمتر",
                "price": 850_000,
                "discount_price": 780_000,
                "stock": 10,
                "prep": 3,
            },
            {
                "sku": "CUT-ACA-LG",
                "wood_type": "اقاقیا",
                "dimensions": "۵۵×۳۵ سانتیمتر",
                "price": 1_200_000,
                "discount_price": None,
                "stock": 6,
                "prep": 5,
            },
        ],
    },
    {
        "title": "قفسه دیواری صنعتی چوب و فلز",
        "category": "قفسه و کتابخانه",
        "tags": ["دکوراسیون داخلی", "طراحی خانه", "هنر چوب"],
        "images": IMAGE_SEEDS["shelf"],
        "description": (
            "قفسه دیواری صنعتی چوب و فلز، ترکیبی شاعرانه از گرمای طبیعت و سردی مدرنیته است. صفحات قفسه از "
            "چوب بلوط ایرانی با ضخامت ۴ سانتیمتر ساخته شده که استحکام کافی برای نگهداری کتاب، گلدان و وسایل "
            "تزئینی سنگین را دارد.\n\n"
            "سازه نگهدارنده از پروفیل‌های فولادی ۲۰×۲۰ با رنگ الکترواستاتیک مشکی مات ساخته شده که علاوه بر "
            "زیبایی، در برابر زنگ‌زدگی کاملاً مقاوم است. سیستم نصب آسان با دوبل و پیچ استیل ضد زنگ، نصب را "
            "حتی برای غیرمتخصصان ساده می‌کند.\n\n"
            "این قفسه در سه نسخه یک‌طبقه، دوطبقه و سه‌طبقه موجود است. با انتخاب بیشترین تعداد طبقه، "
            "۱۵ درصد تخفیف نسبت به خرید جداگانه دریافت می‌کنید."
        ),
        "variations": [
            {
                "sku": "SHF-OAK-1T",
                "wood_type": "بلوط",
                "dimensions": "۸۰×۲۰ - ۱ طبقه",
                "price": 2_100_000,
                "discount_price": None,
                "stock": 7,
                "prep": 10,
            },
            {
                "sku": "SHF-OAK-2T",
                "wood_type": "بلوط",
                "dimensions": "۸۰×۲۰ - ۲ طبقه",
                "price": 3_600_000,
                "discount_price": 3_200_000,
                "stock": 5,
                "prep": 12,
            },
            {
                "sku": "SHF-OAK-3T",
                "wood_type": "بلوط",
                "dimensions": "۸۰×۲۰ - ۳ طبقه",
                "price": 4_900_000,
                "discount_price": 4_400_000,
                "stock": 3,
                "prep": 14,
            },
        ],
    },
    {
        "title": "کاسه دست‌ساز چوب گردو",
        "category": "ظروف سرو و پذیرایی",
        "tags": ["چوب گردو", "ظروف روستیک", "صنایع دستی", "هدیه چوبی"],
        "images": IMAGE_SEEDS["bowl"],
        "description": (
            "کاسه دست‌ساز چوب گردو، اثری که در آن هنر و کاربرد در هم تنیده‌اند. هر کاسه از یک قطعه تنه "
            "گردوی کامل تراشیده می‌شود و رگه‌های تیره و روشن آن الگویی بی‌تکرار ایجاد می‌کند که هیچ دو "
            "کاسه‌ای عینهم نیستند.\n\n"
            "عمق مناسب و لبه صاف این کاسه برای سرو سالاد، میوه، آجیل و تنقلات در مهمانی‌ها فوق‌العاده است. "
            "سطح داخلی با روغن گردوی خالص پرداخت شده که ایمنی کامل برای تماس با مواد غذایی را تضمین می‌کند. "
            "پایه حلقه‌ای شکل در زیر کاسه از لغزش آن جلوگیری می‌کند.\n\n"
            "این کاسه در دو اندازه موجود است و گزینه‌ای استثنایی برای هدیه دادن در مناسبت‌های ویژه است. "
            "با گذشت زمان و روغن‌کاری منظم، عمق رنگ و زیبایی این کاسه افزایش می‌یابد."
        ),
        "variations": [
            {
                "sku": "BWL-WLN-20",
                "wood_type": "گردو",
                "dimensions": "قطر ۲۰ سانتیمتر",
                "price": 920_000,
                "discount_price": 840_000,
                "stock": 12,
                "prep": 5,
            },
            {
                "sku": "BWL-WLN-28",
                "wood_type": "گردو",
                "dimensions": "قطر ۲۸ سانتیمتر",
                "price": 1_450_000,
                "discount_price": None,
                "stock": 8,
                "prep": 7,
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Clean all shop/order data and seed 5 premium wooden products."

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-cleanup",
            action="store_true",
            help="Do not delete existing data before seeding.",
        )

    # ── helpers ──────────────────────────────────────────────────────────────

    def _download_image(self, seed, index):
        url = f"https://picsum.photos/seed/{seed}/900/900"
        try:
            self.stdout.write(f"      ↳ [img] Fetching {url} …", ending="")
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            filename = f"product_{index:02d}_{seed}.jpg"
            self.stdout.write(" OK")
            return ContentFile(resp.content, name=filename)
        except requests.RequestException as exc:
            self.stdout.write(self.style.WARNING(f" FAILED ({exc})"))
            return None

    def _get_or_create_tags(self):
        tag_map = {}
        for name in TAGS:
            tag, created = Tag.objects.get_or_create(
                name=name,
                defaults={"slug": slugify(name, allow_unicode=True)},
            )
            tag_map[name] = tag
        return tag_map

    def _build_category_map(self):
        cat_map = {}
        for name, parent_name in CATEGORIES:
            parent = cat_map.get(parent_name) if parent_name else None
            cat, _ = Category.objects.get_or_create(
                name=name,
                defaults={"slug": slugify(name, allow_unicode=True), "parent": parent},
            )
            # Update parent in case the row already existed without one
            if parent and not cat.parent:
                cat.parent = parent
                cat.save()
            cat_map[name] = cat
        return cat_map

    # ── main handle ──────────────────────────────────────────────────────────

    def handle(self, *args, **options):

        # ── 1. Cleanup ────────────────────────────────────────────────────────
        if not options["skip_cleanup"]:
            self.stdout.write(self.style.WARNING("🗑  Cleaning existing data …"))
            o_count, _ = Order.objects.all().delete()
            p_count, _ = (
                Product.objects.all().delete()
            )  # cascades to variations/images/reviews
            c_count, _ = Category.objects.all().delete()
            t_count, _ = Tag.objects.all().delete()
            self.stdout.write(
                f"   Deleted: {o_count} orders | {p_count} products "
                f"| {c_count} categories | {t_count} tags"
            )

        # ── 2. Tags & Categories ──────────────────────────────────────────────
        self.stdout.write("\n🏷  Creating tags …")
        tag_map = self._get_or_create_tags()
        self.stdout.write(f"   {len(tag_map)} tags ready.")

        self.stdout.write("\n📂 Creating categories …")
        cat_map = self._build_category_map()
        self.stdout.write(f"   {len(cat_map)} categories ready.")

        # ── 3. Products ───────────────────────────────────────────────────────
        self.stdout.write("\n📦 Seeding products …\n")
        created = 0

        for idx, data in enumerate(PRODUCTS, start=1):
            title = data["title"]
            self.stdout.write(f"[{idx}/5] {title}")

            if Product.objects.filter(title=title).exists():
                self.stdout.write(self.style.WARNING(f"   SKIP — already exists.\n"))
                continue

            # ── Product object ────────────────────────────────────────────────
            slug = slugify(title, allow_unicode=True)
            if Product.objects.filter(slug=slug).exists():
                slug = f"{slug}-{idx}"

            category = cat_map.get(data["category"])
            if not category:
                self.stdout.write(
                    self.style.ERROR(
                        f"   Category '{data['category']}' not found, skipping."
                    )
                )
                continue

            product = Product.objects.create(
                title=title,
                slug=slug,
                category=category,
                description=data["description"],
                is_active=True,
            )
            product.tags.set([tag_map[t] for t in data["tags"] if t in tag_map])
            self.stdout.write(f"   Product pk={product.pk} created.")

            # ── Variations ────────────────────────────────────────────────────
            variations = []
            for v in data["variations"]:
                var = ProductVariation.objects.create(
                    product=product,
                    sku=v["sku"],
                    wood_type=v["wood_type"],
                    dimensions=v["dimensions"],
                    price=v["price"],
                    discount_price=v.get("discount_price"),
                    stock=v["stock"],
                    preparation_days=v["prep"],
                )
                variations.append(var)
            self.stdout.write(f"   {len(variations)} variation(s) created.")

            # ── Images ────────────────────────────────────────────────────────
            img_count = 0
            for i, seed in enumerate(data["images"]):
                img_file = self._download_image(seed, idx)
                if img_file:
                    pi = ProductImage(product=product, is_main=(i == 0))
                    pi.image.save(img_file.name, img_file, save=True)
                    img_count += 1
                time.sleep(0.35)  # be polite to picsum

            self.stdout.write(self.style.SUCCESS(f"   {img_count} image(s) saved.\n"))
            created += 1

        # ── 4. Summary ────────────────────────────────────────────────────────
        self.stdout.write("─" * 55)
        self.stdout.write(
            self.style.SUCCESS(f"Done. {created}/{len(PRODUCTS)} products seeded.")
        )
