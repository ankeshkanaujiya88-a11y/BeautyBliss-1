"""
Script to update product prices in fixtures and the database.
Run: .venv\Scripts\python scripts/update_prices.py
"""
import os
import json
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURE_PATH = os.path.join(BASE_DIR, 'products', 'fixtures', 'products.json')
PRICE_LIST = [249, 399, 199, 499, 449, 239, 169]

def update_fixture():
    with open(FIXTURE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for i, item in enumerate(data):
        price = PRICE_LIST[i % len(PRICE_LIST)]
        price_str = f"{price:.2f}"
        fields = item.get('fields', {})
        # Update both original_price and selling_price
        if 'original_price' in fields:
            fields['original_price'] = price_str
        if 'selling_price' in fields:
            fields['selling_price'] = price_str

    with open(FIXTURE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Updated fixture at {FIXTURE_PATH} with {len(data)} prices (cycled from {PRICE_LIST}).")


def update_database():
    # Configure Django environment
    sys.path.insert(0, BASE_DIR)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gambo.settings')
    try:
        import django
        django.setup()
    except Exception as e:
        print("Failed to setup Django:", e)
        return

    try:
        from products.models import Product
    except Exception as e:
        print("Failed to import Product model:", e)
        return

    updated = 0
    for i, item in enumerate(get_fixture_data()):
        pk = item.get('pk')
        price = PRICE_LIST[i % len(PRICE_LIST)]
        try:
            obj = Product.objects.filter(pk=pk).first()
            if not obj:
                continue
            # Try setting fields if they exist on model
            if hasattr(obj, 'original_price'):
                setattr(obj, 'original_price', price)
            if hasattr(obj, 'selling_price'):
                setattr(obj, 'selling_price', price)
            obj.save()
            updated += 1
        except Exception as e:
            print(f"Failed updating product pk={pk}: {e}")

    print(f"Updated {updated} Product rows in the database.")


def get_fixture_data():
    with open(FIXTURE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == '__main__':
    update_fixture()
    update_database()
