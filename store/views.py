from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from datetime import datetime
from store.forms import DeliveryForm, ProductReservationForm, ReservationForm
from .models import *
from django.contrib import messages
from django.views import View
import decimal
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponseRedirect
from django.db.models import Sum
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.

def home(request):
    categories = Category.objects.filter(is_active=True, is_featured=True)[:3]
    products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    not_products = Product.objects.filter(is_active=False, is_featured=True)[:8]
    context = {
        'categories': categories,
        'products': products,
        'not_products': not_products,
    }
    return render(request, 'store/index.html', context)

def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    not_products = Product.objects.filter(is_active=False, id=product.id)
    related_products = Product.objects.exclude(id=product.id).filter(is_active=True, category=product.category)
    context = {
        'product': product,
        'related_products': related_products,
        'not_products': not_products,
    }
    return render(request, 'store/detail.html', context)

def all_categories(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'store/categories.html', {'categories':categories})

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(is_active=True, category=category)
    categories = Category.objects.filter(is_active=True)
    not_products = Product.objects.filter(is_active=False, category=category)
    context = {
        'category': category,
        'products': products,
        'categories': categories,
        'not_products': not_products,
    }
    return render(request, 'store/category_products.html', context)

def gallery_view(request):
    gallery = Gallery.objects.all()
    context = {
        'gallery': gallery,
    }
    return render(request, 'store/gallery.html', context)

def location_view(request):
    return render(request, 'store/location.html')

def aboutus_view(request):
    return render(request, 'store/about_us.html')

@login_required
def profile(request):
    delivery_information = DeliveryInformation.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    reservations = Reservation.objects.filter(user=request.user)
    order_item = OrderItem.objects.filter(user=request.user)
    order_pending = Order.objects.filter(user=request.user, status="Pending")
    return render(request, 'account/profile.html', {'delivery_information':delivery_information, 'orders':orders, 'reservations':reservations,'order_items':order_item, 'order_pending':order_pending})

@method_decorator(login_required, name='dispatch')
class DeliveryView(View):
    def get(self, request):
        form = DeliveryForm()
        return render(request, 'account/add_address.html', {'form': form})

    def post(self, request):
        form = DeliveryForm(request.POST)
        if form.is_valid():
            user=request.user
            fname = form.cleaned_data['fname']
            phone_number = form.cleaned_data['phone_number']
            barangay = form.cleaned_data['barangay']
            landmark = form.cleaned_data['landmark']
            location = form.cleaned_data['location']
            notes = form.cleaned_data['notes']
            reg = DeliveryInformation(user=user, fname=fname, phone_number=phone_number,barangay=barangay,landmark=landmark,location=location,notes=notes)
            reg.save()
            messages.success(request, "New Delivery Address Added Successfully.")
        return redirect('store:home')

@method_decorator(login_required, name='dispatch')
class ReservationView(View):
    def get(self, request):
        form = ReservationForm()
        return render(request, 'store/reservation.html', {'form': form})
    
    def post(self, request):
        form = ReservationForm(request.POST)
        if form.is_valid():
            user=request.user
            phone_number = form.cleaned_data['phone_number']
            pax = form.cleaned_data['pax']
            pax_expected = form.cleaned_data['pax_expected']
            event_name = form.cleaned_data['event_name']
            event_type = form.cleaned_data['event_type']
            event_time = form.cleaned_data['event_time']
            event_time_end = form.cleaned_data['event_time_end']
            event_date = form.cleaned_data['event_date']
            remarks = form.cleaned_data['remarks']
            reg = Reservation(user=user, phone_number=phone_number, pax_expected=pax_expected, pax=pax, event_name=event_name, event_type=event_type, event_time=event_time,event_time_end=event_time_end ,event_date=event_date, remarks=remarks)
            reg.save()
            messages.success(request, "Reservation Added Successfully!")
        else:
            messages.error(request, "The Scheduled Date Is Already Taken!")
        return redirect('store:profile')

@method_decorator(login_required, name='dispatch')
class ProductReservationView(View):
    def get(self, request):
        form = ProductReservationForm()
        return render(request, 'store/product_reservation.html', {'form': form})
    
    def post(self, request):
        form = ProductReservationForm(request.POST)
        if form.is_valid():
            user=request.user
            fname = form.cleaned_data['fname']
            phone_number = form.cleaned_data['phone_number']
            delivery_time = form.cleaned_data['delivery_time']
            pickup_date = form.cleaned_data['pickup_date']
            remarks = form.cleaned_data['remarks']
            reg = ProductReservation(user=user, fname=fname ,phone_number=phone_number, delivery_time=delivery_time,pickup_date=pickup_date , remarks=remarks)
            reg.save()
            messages.success(request, "Reservation Added Successfully!")
        return redirect('store:profile')

@login_required
def remove_address(request, id):
    a = get_object_or_404(DeliveryInformation, user=request.user, id=id)
    a.delete()
    messages.success(request, "Delivery Address removed.")
    return redirect('store:profile')

@login_required
def remove_reservation(request, id):
    r = get_object_or_404(Reservation, user=request.user, id=id)
    r.delete()
    messages.success(request, "Reservation removed.")
    return redirect('store:profile')

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    item_already_in_cart = Cart.objects.filter(product=product_id, user=user)
    if item_already_in_cart:
        cp = get_object_or_404(Cart, product=product_id, user=user)
        cp.quantity += 1
        cp.save()
    else:
        Cart(user=user, product=product).save()
    messages.success(request, 'Added to Cart successfully!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def cart(request):
    user = request.user
    cart_products = Cart.objects.filter(user=user)

    amount = decimal.Decimal(0)
    delivery_fee = decimal.Decimal(50)
    one_radius = decimal.Decimal(0)
    two_radius = decimal.Decimal(30)
    three_radius = decimal.Decimal(40)
    four_radius = decimal.Decimal(50)
    five_radius = decimal.Decimal(60)
    six_radius = decimal.Decimal(70)
    seven_radius = decimal.Decimal(80)
    eight_radius = decimal.Decimal(90)
    nine_radius = decimal.Decimal(100)

    one_total = delivery_fee + one_radius
    two_total = delivery_fee + two_radius
    three_total = delivery_fee + three_radius
    four_total = delivery_fee + four_radius
    five_total = delivery_fee + five_radius
    six_total = delivery_fee + six_radius
    seven_total = delivery_fee + seven_radius
    eight_total = delivery_fee + eight_radius
    nine_total = delivery_fee + nine_radius

    total_fee_1 = one_total
    total_fee_2 = two_total
    total_fee_3 = three_total
    total_fee_4 = four_total
    total_fee_5 = five_total
    total_fee_6 = six_total
    total_fee_7 = seven_total
    total_fee_8 = eight_total
    total_fee_9 = nine_total

    ayala = DeliveryInformation.objects.filter(user=user, barangay="Ayala")
    baliwasan = DeliveryInformation.objects.filter(user=user, barangay="Baliwasan")
    boalan = DeliveryInformation.objects.filter(user=user, barangay="Boalan")
    cabatangan = DeliveryInformation.objects.filter(user=user, barangay="Cabatangan")
    calarian = DeliveryInformation.objects.filter(user=user, barangay="Calarian")
    campo_islam = DeliveryInformation.objects.filter(user=user, barangay="Campo Islam")
    canelar = DeliveryInformation.objects.filter(user=user, barangay="Canelar")
    cawit = DeliveryInformation.objects.filter(user=user, barangay="Cawit")
    city_proper = DeliveryInformation.objects.filter(user=user, barangay="City Proper")
    divisoria = DeliveryInformation.objects.filter(user=user, barangay="Divisoria")
    guiwan = DeliveryInformation.objects.filter(user=user, barangay="Guiwan")
    lumbangan = DeliveryInformation.objects.filter(user=user, barangay="Lumbangan")
    lunzuran = DeliveryInformation.objects.filter(user=user, barangay="Lunzuran")
    maasin = DeliveryInformation.objects.filter(user=user, barangay="Maasin")
    malagutay = DeliveryInformation.objects.filter(user=user, barangay="Malagutay")
    pasonanca = DeliveryInformation.objects.filter(user=user, barangay="Pasonanca")
    putik = DeliveryInformation.objects.filter(user=user, barangay="Putik")
    recodo = DeliveryInformation.objects.filter(user=user, barangay="Recodo")
    santo_nino = DeliveryInformation.objects.filter(user=user, barangay="Santo Niño")
    santa_maria = DeliveryInformation.objects.filter(user=user, barangay="Santa Maria")
    san_roque = DeliveryInformation.objects.filter(user=user, barangay="San Roque")
    san_jose_cawa = DeliveryInformation.objects.filter(user=user, barangay="San Jose Cawa-cawa")
    san_jose_gusu = DeliveryInformation.objects.filter(user=user, barangay="San Jose Gusu")
    sinunoc = DeliveryInformation.objects.filter(user=user, barangay="Sinunoc")
    talon = DeliveryInformation.objects.filter(user=user, barangay="Talon-talon")
    tetuan = DeliveryInformation.objects.filter(user=user, barangay="Tetuan")
    tumaga = DeliveryInformation.objects.filter(user=user, barangay="Tumaga")
    zambowood = DeliveryInformation.objects.filter(user=user, barangay="Zambowood")

    cp = [p for p in Cart.objects.all() if p.user==user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount

    # Customer Addresses
    delivery_addresses = DeliveryInformation.objects.filter(user=user)

    if delivery_addresses is ayala or zambowood:
        nine_total
    
    if delivery_addresses is cawit:
        eight_total

    if delivery_addresses is talon or recodo or boalan:
        seven_total
    
    if delivery_addresses is campo_islam or city_proper or divisoria or maasin or malagutay or san_jose_cawa or san_jose_gusu or sinunoc or tetuan:
        six_total
    
    if delivery_addresses is calarian or guiwan or lumbangan or lunzuran or santo_nino:
        five_total

    if delivery_addresses is baliwasan or canelar or putik:
        four_total

    if delivery_addresses is tumaga:
        three_total

    if delivery_addresses is pasonanca or san_roque or santa_maria:
        two_total

    if delivery_addresses is cabatangan:
        one_total

    if delivery_addresses is None:
        amount

    context = {
        'cart_products': cart_products,
        'amount': amount,
        'delivery_fee': delivery_fee,
        'one_radius': one_radius,
        'two_radius': two_radius,
        'three_radius': three_radius,
        'four_radius': four_radius,
        'five_radius': five_radius,
        'six_radius': six_radius,
        'seven_radius': seven_radius,
        'eight_radius': eight_radius,
        'nine_radius': nine_radius,
        'ayala':ayala,
        'baliwasan':baliwasan,
        'boalan':boalan,
        'cabatangan':cabatangan,
        'calarian':calarian,
        'campo_islam':campo_islam,
        'canelar':canelar,
        'cawit':cawit,
        'city_proper':city_proper,
        'divisoria':divisoria,
        'guiwan':guiwan,
        'lumbangan':lumbangan,
        'lunzaran':lunzuran,
        'maasin':maasin,
        'malagutay':malagutay,
        'pasonanca':pasonanca,
        'putik':putik,
        'recodo':recodo,
        'san_jose_cawa':san_jose_cawa,
        'san_jose_gusu':san_jose_gusu,
        'san_roque':san_roque,
        'santa_maria':santa_maria,
        'santo_nino':santo_nino,
        'sinunoc':sinunoc,
        'talon':talon,
        'tetuan':tetuan,
        'tumaga':tumaga,
        'zambowood':zambowood,
        'cabatangan':cabatangan,
        'total_fee_1': total_fee_1,
        'total_fee_2': total_fee_2,
        'total_fee_3': total_fee_3,
        'total_fee_4': total_fee_4,
        'total_fee_5': total_fee_5,
        'total_fee_6': total_fee_6,
        'total_fee_7': total_fee_7,
        'total_fee_8': total_fee_8,
        'total_fee_9': total_fee_9,
        'total_amount_1': amount,
        'total_amount_2': amount + total_fee_2,
        'total_amount_3': amount + total_fee_3,
        'total_amount_4': amount + total_fee_4,
        'total_amount_5': amount + total_fee_5,
        'total_amount_6': amount + total_fee_6,
        'total_amount_7': amount + total_fee_7,
        'total_amount_8': amount + total_fee_8,
        'total_amount_9': amount + total_fee_9,
        'delivery_addresses': delivery_addresses,
    }
    return render(request, 'store/cart.html', context)

@login_required
def remove_cart(request, cart_id):
    if request.method == 'GET':
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        messages.success(request, "Item removed from Cart.")
    return redirect('store:cart')

@login_required
def remove_favorites(request, favorites_id):
    if request.method == 'GET':
        c = get_object_or_404(Favorites, id=favorites_id)
        c.delete()
        messages.error(request, "Item remove from Favorites.")
    return redirect('store:favorites')

@login_required
def remove_order(request, order_id):
    if request.method == 'GET':
        c = get_object_or_404(Order, id=order_id)
        c.delete()
        messages.error(request, "Item is now cancelled!")
    return redirect('store:profile')

@login_required
def plus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity += 1
        cp.save()
    messages.success(request, "Item quantity is now added!")
    return redirect('store:cart')

@login_required
def minus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        if cp.quantity == 1:
            messages.success(request, 'Item is now deleted from cart!')
            cp.delete()
        else:
            cp.quantity -= 1
            messages.success(request, 'Item is removed by 1')
            cp.save()
    return redirect('store:cart')

@login_required
def favorite_view(request):
    user = request.user
    favorite_products = Favorites.objects.filter(user=user)
    context = {
        'favorite_products': favorite_products,
    }
    return render(request, 'store/favorites.html', context)

@login_required
def add_to_favorite(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    item_already_in_favorite = Favorites.objects.filter(product=product_id, user=user)
    if item_already_in_favorite:
        messages.error(request, 'Item is already in favorites!')
    else:
        messages.add_message(request, messages.SUCCESS, 'Item is now added in favorites!')
        Favorites(user=user, product=product).save()

    return redirect('store:favorites')

@login_required
def checkout(request):
    user = request.user
    address_id = request.GET.get('address')
    address = get_object_or_404(DeliveryInformation, id=address_id)
    amount = decimal.Decimal(0)
    cp = [p for p in Cart.objects.all() if p.user==user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount

    order = Order.objects.create(
        user=user,
        address=address,
        total_price = amount,
    )
    order.save()
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderItem(invoice_no='INV-'+str(order.id),user=user,product=c.product,quantity=c.quantity,price=c.quantity*c.product.price).save()
    
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderManagement(invoice_no='INV-'+str(order.id),user=user,product=c.product,quantity=c.quantity,price=c.quantity*c.product.price).save()
        c.delete()

    counter = Order.objects.all().count()
    sum = Order.objects.all().aggregate(Sum('total_price'))['total_price__sum']
    sum2 = OrderManagement.objects.all().aggregate(Sum('price'))['price__sum']
    quantity = OrderManagement.objects.all().aggregate(Sum('quantity'))['quantity__sum']
    sales = Sales.objects.create(
        total_orders = counter,
        revenue = sum,  
        subtotal = sum2,
        total_products = quantity,
    )
    sales.save()
    return redirect('store:orders')

    
@login_required
def orders(request):
    order_item = OrderItem.objects.filter(user=request.user)
    order_list = Order.objects.filter(user=request.user)
    address_list = DeliveryInformation.objects.filter(user=request.user)

    template_path = 'store/orders.html'
    context = {'order_items':order_item,'order_lists':order_list,'address_lists':address_list}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reciept.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    OrderItem.objects.all().delete()
    return response

@staff_member_required
def sales(request):
    sales = Sales.objects.all()
    x = datetime.now()
    orders = Sales.objects.all()
    pending = Order.objects.filter(status="Pending").count()
    reseravation = Reservation.objects.filter(status="Pending").count()
    delivered = Order.objects.filter(status="Delivered").count()
    order_pending = Order.objects.filter(user=request.user, status="Pending")
    reseravation_pending = Reservation.objects.filter(user=request.user, status="Pending")
    context = {
        "sales":sales,
        'date':x,
        'orders':orders,
        'pending':pending,
        'reservation':reseravation,
        'delivered':delivered,
        'order_pending':order_pending,
        'reseravation_pending':reseravation_pending,
    }
    
    return render(request, 'store/sales.html', context)
