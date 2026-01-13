from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Product, Category, Order, OrderItem, Coupon
from .cart import Cart
from django.utils import timezone
from django.contrib import messages

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'store/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    return render(request, 'store/product_detail.html', {'product': product})

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity)
    messages.success(request, "Product added to cart!")
    return redirect('cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart_detail.html', {'cart': cart})

@require_POST
def coupon_apply(request):
    code = request.POST.get('code')
    now = timezone.now()
    try:
        coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
        request.session['coupon_id'] = coupon.id
        messages.success(request, "Coupon applied!")
    except Coupon.DoesNotExist:
        request.session['coupon_id'] = None
        messages.error(request, "Invalid coupon code")
    return redirect('cart_detail')

def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('product_list')
    
    if request.method == 'POST':
        # Simple form handling
        customer_name = request.POST.get('customer_name')
        phone_number = request.POST.get('phone_number')
        delivery_address = request.POST.get('delivery_address')
        city = request.POST.get('city')
        order_notes = request.POST.get('order_notes')
        
        order = Order.objects.create(
            customer_name=customer_name,
            phone_number=phone_number,
            delivery_address=delivery_address,
            city=city,
            order_notes=order_notes,
            total_amount=cart.get_total_price_after_discount()
        )
        
        # Link coupon if used
        if cart.coupon_id:
             try:
                 order.coupon = Coupon.objects.get(id=cart.coupon_id)
             except Coupon.DoesNotExist:
                 pass
        order.save()

        # Create Order Items
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
            
        # Clear the cart
        cart.clear()
        
        # In a real app, send email/whatsapp here
        
        return render(request, 'store/order_created.html', {'order': order})
        
    return render(request, 'store/checkout.html', {'cart': cart})
