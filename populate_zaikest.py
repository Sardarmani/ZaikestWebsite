import os
import django
from django.core.files import File
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zaikest_project.settings')
django.setup()

from store.models import Category, Product

def populate():
    print("Resetting Database (Categories & Products)...")
    # Clean up existing data to remove unwanted categories
    Product.objects.all().delete()
    Category.objects.all().delete()

    # Define Categories
    categories_list = [
        "Pastes",
        "Frozen chicken and meats",
        "Frozen vegetables",
        "Deals",
        "Desi products",
        "Zaikest meal box"
    ]

    print("Creating Categories...")
    # Path to the specific category icon
    icon_name = "category.png"
    icon_path = os.path.join(settings.MEDIA_ROOT, 'images', icon_name)
    
    created_cats = {}

    for cat_name in categories_list:
        slug = cat_name.lower().replace(" ", "-")
        category = Category.objects.create(name=cat_name, slug=slug)
        created_cats[cat_name] = category
        print(f"Created Category: {cat_name}")

        # Assign Icon
        if os.path.exists(icon_path):
            with open(icon_path, 'rb') as f:
                category.image.save(icon_name, File(f), save=True)

    # Define Products (Pastes)
    products_list = [
        {"name": "Chicken Achari", "image": "Chicken acharya.jpg", "price": 500},
        {"name": "Biryani", "image": "biryani.jpg", "price": 450},
        {"name": "Handi", "image": "handi.jpg", "price": 480},
        {"name": "Karahi", "image": "karahi paste.jpg", "price": 480},
        {"name": "Korma", "image": "korma .jpg", "price": 450},
        {"name": "Shashlik", "image": "shashikPaste.jpg", "price": 550},
        {"name": "White Karahi", "image": "white Karahi.jpg", "price": 500},
    ]

    images_dir = os.path.join(settings.MEDIA_ROOT, 'images')

    def create_products_for_category(cat_obj, prod_list):
        print(f"Creating Products for '{cat_obj.name}'...")
        for prod_data in prod_list:
             # Create unique slug if reusing names across categories
            base_slug = prod_data["name"].lower().replace(" ", "-")
            slug = f"{base_slug}-{cat_obj.slug}" 
            
            product = Product.objects.create(
                name=prod_data["name"],
                category=cat_obj,
                slug=slug,
                price=prod_data["price"],
                short_description=f"Authentic {prod_data['name']} paste.",
                is_available=True
            )
            print(f"  - Created: {product.name}")
            
            # Handle Image
            image_name = prod_data["image"]
            image_path = os.path.join(images_dir, image_name)
            
            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    product.image.save(image_name, File(f), save=True)

    # 1. Add products to "Pastes"
    if "Pastes" in created_cats:
        create_products_for_category(created_cats["Pastes"], products_list)

    # 2. Add SAME products to "Zaikest meal box" (as requested)
    if "Zaikest meal box" in created_cats:
        create_products_for_category(created_cats["Zaikest meal box"], products_list)

if __name__ == "__main__":
    populate()
    print("\nData population complete.")
