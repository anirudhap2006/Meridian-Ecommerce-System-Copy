def cart_count(request):
 count=sum(i.quantity for i in request.user.cart_items.select_related('product')) if request.user.is_authenticated else 0
 return {'cart_count':count}
