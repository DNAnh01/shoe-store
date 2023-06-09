from django.shortcuts import render, redirect
from store_app.models import Product, Categories, Filter_Price, Color, Brand, Tag, Contact_us, Order, OrderItem
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart


def BASE(request):
    return render(request, 'Main/base.html')

def HOME(request):
    product = Product.objects.filter(status='Publish')

    context = {
        'product': product
    }

    return render(request, 'Main/index.html', context)

def PRODUCT(request):
    categories = Categories.objects.all()
    filter_price = Filter_Price.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()

    CATID = request.GET.get('categories')
    PRICE_FILTER_ID = request.GET.get('filter_price')
    COLOR_ID = request.GET.get('color')
    BRANDID = request.GET.get('brand')

    ATOZID = request.GET.get('ATOZ')
    ZTOAID = request.GET.get('ZTOA')

    PRICE_LOWTOHIGHID = request.GET.get('PRICE_LOWTOHIGH') 
    PRICE_HIGHTOLOWID = request.GET.get('PRICE_HIGHTOLOW')

    NEW_PRODUCTID = request.GET.get('NEW_PRODUCT')
    OLD_PRODUCTID = request.GET.get('OLD_PRODUCT')

    if CATID:
        product = Product.objects.filter(categories = CATID, status='Publish')
    elif PRICE_FILTER_ID:
        product = Product.objects.filter(filter_price = PRICE_FILTER_ID, status='Publish')
    elif COLOR_ID:
        product = Product.objects.filter(color = COLOR_ID, status='Publish')
    elif BRANDID:
        product = Product.objects.filter(brand = BRANDID, status='Publish')
    elif ATOZID:
        product = Product.objects.filter(status='Publish').order_by('name')
    elif ZTOAID:
        product = Product.objects.filter(status='Publish').order_by('-name')
    elif PRICE_LOWTOHIGHID:
        product = Product.objects.filter(status='Publish').order_by('price')
    elif PRICE_HIGHTOLOWID:
        product = Product.objects.filter(status='Publish').order_by('-price')
    elif NEW_PRODUCTID:
        product = Product.objects.filter(status='Publish', condition='New').order_by('-id')
    elif OLD_PRODUCTID:
        product = Product.objects.filter(status='Publish', condition='Old').order_by('-id')
    else:
        product = Product.objects.filter(status='Publish')

    context = {
        'product': product,
        'categories': categories,
        'filter_price': filter_price,
        'color': color,
        'brand': brand,
    }

    return render(request, 'Main/product.html', context)

def SEARCH(request):
    query = request.GET.get('query')
    # print(query)
    product = Product.objects.filter(name__icontains = query)

    context = {
        'product': product
    }

    return render(request, 'Main/search.html', context)

def PRODUCT_DETAIL_PAGE(request, id):
    prod = Product.objects.filter(id = id).first()
    context = {
        'prod': prod,
    }
    return render(request, 'Main/product_single.html', context)

def CONTACT_PAGE(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        # print(name, email, subject, message)
        contact = Contact_us(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        contact.save()
        return redirect('home')
    
        '''
            chưa bật được chế độ hỗ trợ truy cập kém an toàn bên thứ 3
        '''

        # subject = subject
        # message = message
        # email_from = settings.EMAIL_HOST_USER
        # try:
        #     send_mail(subject, message, email_from, ['donguyenanh12345@gmail.com'])
        #     contact.save()
        #     return redirect('home')
        # except:
        #     return redirect('contact')

    return render(request, 'Main/contact.html')

# def AUTH(request):
#     return render(request, 'Registration/auth.html')

def HandleRegister(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        customer = User.objects.create_user(username,email,pass1)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.save()
        return redirect('home')

    return render(request, 'Registration/auth.html')

def HandleLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
            # 12345 12345
        else:
            return redirect('login')

    return render(request, 'Registration/auth.html')

def HandleLogout(request):
    logout(request)
    # redirect('home')
    return redirect('home')

# def CART(request):
#     return render(request, 'Cart/cart_details.html')

@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    return render(request, 'Cart/cart_details.html')


def Check_out(request):
    amount = request.POST.get("amount")
    print(amount)
    return render(request, 'Cart/checkout.html')


def PLACE_ORDER(request):
    if request.method == "POST":
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id = uid)
        # print(user)
        cart = request.session.get('cart')
        # print(cart)
        '''
        {'3': {'userid': 4, 'product_id': 3, 'name': 'Under Armour mens Charged Assert 9 Running Shoe, Black (003 Black, 9.5 US)', 'quantity': 2, 'price': '67', 'image': '/Product_images/img/download_1_5C5FXsO.jpg'}, '4': {'userid': 4, 'product_id': 4, 'name': "Skechers Men's Energy Afterburn Shoes Lace-Up Sneaker", 'quantity': 3, 'price': '42', 'image': '/Product_images/img/download_5_cxj6fIW.jpg'}}
        '''
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        # print(amount)
        # print(firstname, lastname, country, address, city, state, postcode, phone, email)
        order = Order(
            user=user,
            firstname=firstname,
            lastname=lastname,
            country=country,
            city=city,
            address=address,
            state=state,
            postcode=postcode,
            phone=phone,
            email=email,
            amount=amount,
        )
        order.save()
        for i in cart:
            a = (int(cart[i]['price']))
            b = cart[i]['quantity']
            total = a*b
            # print("----------------------", total)
            item = OrderItem(
                user=user,
                order=order,
                product=cart[i]['name'],
                image=cart[i]['image'],
                quantity=cart[i]['quantity'],
                price=cart[i]['price'],
                total = total
            )
            item.save()
        return render(request, 'Cart/placeorder.html')
    

def success(request):
    return render(request, 'Cart/thank_you.html')

def Your_Order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id = uid)

    # print(user)
    order = OrderItem.objects.filter(user=user)
    # print(order)
    context = {
        'order': order
    }
    return render(request, 'Main/your_order.html', context)