from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Coupon

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'is_available', 'is_best_seller', 'updated_at']
    list_filter = ['is_available', 'is_best_seller', 'category']
    list_editable = ['price', 'is_available', 'is_best_seller']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'short_description']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'phone_number', 'city', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'city']
    inlines = [OrderItemInline]
    search_fields = ['customer_name', 'phone_number', 'id']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to', 'discount_amount', 'discount_percentage', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']
