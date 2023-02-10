from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from .recommender import Recommender
from django.core.paginator import Paginator




#list all the products or filter products by a given category
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        products = products.filter(category=category)
    return render(request,
        'shop/product/list.html',
        {'category': category,
        'categories': categories,
        'products': products,'posts': posts})
    
# retrieve and display a single product 
def product_detail(request, id, slug):
     product = get_object_or_404(Product,id=id,slug=slug,available=True)
     cart_product_form = CartAddProductForm()
     r = Recommender()
     recommended_products = r.suggest_products_for([product], 4)
     return render(request,'shop/product/detail.html',{'product': product,'cart_product_form': cart_product_form,'recommended_products': recommended_products}) 
 
