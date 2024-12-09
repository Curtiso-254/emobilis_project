from django.shortcuts import redirect, render
from django.shortcuts import render, get_object_or_404
from .models import Product
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def product_list(request):
    from django.db.models import Q

def product_list(request):
    query = request.GET.get('query', '')
    category = request.GET.get('category', '')
    sort_by = request.GET.get('sort', 'name')

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    if category:
        products = products.filter(category__name=category)

    if sort_by == 'price':
        products = products.order_by('price')
    else:
        products = products.order_by('name')

    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    return redirect ('cart')