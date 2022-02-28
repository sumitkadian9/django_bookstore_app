from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .basket import Basket
from store.models import Product

def basket_summary(request):
    basket = Basket(request)
    return render(request, 'store/basket/summary.html', {'basket':basket})

def basket_add(request):
    basket = Basket(request)

    #if request received from ajax is POST
    if request.POST.get('action') == 'post' :
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)
        basket_qty = basket.__len__()
        response = JsonResponse({'qty' : basket_qty}) #return updated quantity to frontend
        return response

def basket_update(request):
    basket = Basket(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)
        return JsonResponse({'Success':'True'})

def basket_delete(request):
    basket = Basket(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.remove(product=product_id)
        response = JsonResponse({'Success':'True'})
        return response
