import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from shop.models import Category, Product, ProductVariation, ProductImage

class Command(BaseCommand):
    help = 'Populates the shop with initial data including categories, products, variations, and images.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate the database...'))

        # 1. Create Categories
        cat_serving, _ = Category.objects.get_or_create(
            name='ظروف پذیرایی',
            defaults={'slug': 'serving-dishes'}
        )
        cat_decor, _ = Category.objects.get_or_create(
            name='دکوریجات',
            defaults={'slug': 'decorations'}
        )
        self.stdout.write(self.style.SUCCESS(f'Created categories: "{cat_serving.name}" and "{cat_decor.name}"'))

        # 2. Create Products
        products_data = [
            {
                'category': cat_serving,
                'title': 'شیرینی‌خوری چوبی دو طبقه',
                'description': 'این شیرینی‌خوری دو طبقه با طراحی منحصربه‌فرد و ساخته شده از چوب با کیفیت، زیبایی خاصی به میز پذیرایی شما می‌بخشد. مناسب برای سرو انواع شیرینی، میوه و فینگرفود.',
                'variations': [
                    {'sku': 'WPS-01-S', 'wood_type': 'گردو', 'dimensions': 'قطر طبقه پایین ۲۵، بالا ۲۰ سانتی‌متر', 'price': 680000, 'stock': 5},
                    {'sku': 'WPS-01-L', 'wood_type': 'راش', 'dimensions': 'قطر طبقه پایین ۳۰، بالا ۲۵ سانتی‌متر', 'price': 850000, 'stock': 3},
                ]
            },
            {
                'category': cat_decor,
                'title': 'کاسه چوب گردو خراطی شده',
                'description': 'کاسه‌ای زیبا و دست‌ساز که با هنر خراطی روی چوب گردو خلق شده است. رگه‌های طبیعی چوب، هر کاسه را به یک اثر هنری بی‌همتا تبدیل کرده است. مناسب برای دکور یا سرو خشکبار.',
                'variations': [
                    {'sku': 'WNB-01-M', 'wood_type': 'گردو', 'dimensions': 'قطر ۲۰ سانتی‌متر', 'price': 450000, 'stock': 10},
                    {'sku': 'WNB-01-L', 'wood_type': 'گردو', 'dimensions': 'قطر ۲۸ سانتی‌متر', 'price': 720000, 'stock': 0, 'preparation_days': 7},
                ]
            },
            {
                'category': cat_serving,
                'title': 'سینی چوبی روستیک',
                'description': 'سینی چوبی با طراحی روستیک و لبه‌های طبیعی که حس طبیعت را به خانه شما می‌آورد. ایده‌آل برای سرو صبحانه، نوشیدنی یا به عنوان زیرگلدانی.',
                'variations': [
                    {'sku': 'WST-01-B', 'wood_type': 'چنار', 'dimensions': 'تقریبی ۴۰x۲۵ سانتی‌متر', 'price': 520000, 'stock': 8},
                    {'sku': 'WST-01-O', 'wood_type': 'بلوط', 'dimensions': 'تقریبی ۴۵x۳۰ سانتی‌متر', 'price': 690000, 'stock': 4},
                ]
            }
        ]

        for data in products_data:
            product, created = Product.objects.get_or_create(
                title=data['title'],
                defaults={
                    'category': data['category'],
                    'slug': slugify(data['title'], allow_unicode=True),
                    'description': data['description'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: "{product.title}"'))
            else:
                self.stdout.write(self.style.WARNING(f'Product "{product.title}" already exists.'))


            # 3. Create Variations
            for var_data in data['variations']:
                variation, var_created = ProductVariation.objects.get_or_create(
                    sku=var_data['sku'],
                    defaults={
                        'product': product,
                        **var_data
                    }
                )
                if var_created:
                     self.stdout.write(f'  - Created variation: {variation.sku}')


            # 4. Download and attach image
            if not product.images.exists():
                try:
                    image_url = 'https://loremflickr.com/600/600/wood,craft'
                    response = requests.get(image_url, stream=True)
                    response.raise_for_status()

                    # Create a ContentFile from the response content
                    image_content = ContentFile(response.content)
                    image_name = f'{product.slug}.jpg'

                    product_image = ProductImage(product=product, is_main=True)
                    product_image.image.save(image_name, image_content, save=True)

                    self.stdout.write(self.style.SUCCESS(f'  - Successfully downloaded and attached image to "{product.title}"'))

                except requests.exceptions.RequestException as e:
                    self.stdout.write(self.style.ERROR(f'  - Could not download image for "{product.title}": {e}'))

        self.stdout.write(self.style.SUCCESS('Database population complete!'))
