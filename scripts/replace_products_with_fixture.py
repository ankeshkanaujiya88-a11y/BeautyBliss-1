"""
Replace existing products in DB with the fixture at
`products/fixtures/beautybliss_products_60.json`.

Run:
.venv\Scripts\python scripts\replace_products_with_fixture.py
"""
import os
import sys
import shutil
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURE_SRC = os.path.join(BASE_DIR, 'products', 'fixtures', 'beautybliss_products_60.json')
FIXTURE_TARGET = os.path.join(BASE_DIR, 'products', 'fixtures', 'products.json')

# Ensure DJANGO_SETTINGS_MODULE is set
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gambo.settings')

try:
    import django
    django.setup()
    from django.core.management import call_command
except Exception as e:
    print('Failed to setup Django:', e)
    sys.exit(1)

# Backup current products.json if present
if os.path.exists(FIXTURE_TARGET):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    backup_path = FIXTURE_TARGET + '.backup.' + timestamp
    shutil.copy2(FIXTURE_TARGET, backup_path)
    print(f'Backed up existing fixture to {backup_path}')

# Copy the provided fixture to products.json so loaddata uses it consistently
if os.path.exists(FIXTURE_SRC):
    shutil.copy2(FIXTURE_SRC, FIXTURE_TARGET)
    print(f'Copied {FIXTURE_SRC} -> {FIXTURE_TARGET}')
else:
    print(f'Fixture source not found: {FIXTURE_SRC}')
    sys.exit(1)

# Delete existing product-related rows
try:
    from products.models import Product, ProductVariant, ProductImage
    v_count = ProductVariant.objects.count()
    i_count = ProductImage.objects.count()
    p_count = Product.objects.count()
    ProductVariant.objects.all().delete()
    ProductImage.objects.all().delete()
    Product.objects.all().delete()
    print(f'Deleted {v_count} variants, {i_count} images, {p_count} products from DB')
except Exception as e:
    print('Failed to delete existing product data:', e)

# Load fixture
try:
    # Use the relative fixture path
    call_command('loaddata', FIXTURE_TARGET)
    from products.models import Product
    print(f'Loaded fixture; Product count is now {Product.objects.count()}')
except Exception as e:
    print('Failed to load fixture:', e)
    sys.exit(1)
