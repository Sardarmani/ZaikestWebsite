from django.shortcuts import render
from store.models import Product, Category

def home(request):
    pastes = Product.objects.filter(category__name="Pastes", is_available=True)
    categories = Category.objects.all()
    return render(request, 'pages/home.html', {
        'pastes': pastes,
        'categories': categories
    })

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    return render(request, 'pages/contact.html')
