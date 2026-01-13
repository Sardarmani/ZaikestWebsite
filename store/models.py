from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    short_description = models.TextField(blank=True)
    
    # Specific Paste Info
    recipe_usage = models.TextField(help_text="Recipe usage suggestion per paste", blank=True)
    how_to_cook = models.TextField(help_text="How to Cook section", blank=True)
    shelf_life = models.CharField(max_length=200, help_text="Shelf life & storage info", blank=True)
    
    # Badges & Status
    is_best_seller = models.BooleanField(default=False, verbose_name="Best Seller Badge")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    youtube_url = models.URLField(blank=True, null=True, help_text="Paste full YouTube URL here (e.g. https://www.youtube.com/watch?v=...)")

    def __str__(self):
        return self.name

    def get_youtube_embed_url(self):
        if not self.youtube_url:
            return None
        # Simple extraction for standard youtube URLs
        import re
        # Covers: youtube.com/watch?v=ID, youtube.com/v/ID, youtu.be/ID
        regex = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
        match = re.search(regex, self.youtube_url)
        if match:
            return f"https://www.youtube.com/embed/{match.group(1)}"
        return None

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_percentage = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Dispatched', 'Dispatched'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    # Customer Info
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    delivery_address = models.TextField()
    city = models.CharField(max_length=100)
    order_notes = models.TextField(blank=True)

    # Order Info
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_cost(self):
        return self.price * self.quantity
