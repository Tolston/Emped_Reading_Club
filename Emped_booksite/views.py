from django.shortcuts import render, redirect
from .models import *
from django.http import Http404, JsonResponse
from django.http import HttpResponse
from django.core import serializers
import random
from json import dumps
from django.core.serializers.json import DjangoJSONEncoder
import requests
import ast
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

def main_func(request):
    """ Getting all available books"""
    books = Book.objects.all()
    genres = Category.objects.all()
    agerange = Range.objects.all()
    authors = Author.objects.all()
    return render(request, 'Emped_booksite/home.html',
                  {'books': books, 'genres': genres, 'agerange': agerange, 'authors': authors})


def profile_page(request):
    if request.session.get('userphone'):
        try:
            customer = Customer.objects.filter(PhoneNo=request.session.get('userphone'))
        except Customer.DoesNotExist:
            raise Http404('Oops Sorry! Customer Profile  does not exist!!!')
        try:
            current_reading = Rent.objects.filter(Customer_id=request.session.get('userid'), Status="On Rent")
            previous_reading = Rent.objects.filter(Customer_id=request.session.get('userid'), Status="Returned")
        except Rent.DoesNotExist:
            raise Http404('Oops Sorry! Couldn\'t find customers orders!!!')
    return render(request, 'Emped_booksite/Profile.html', {'customer': customer, 'current_reading': current_reading,
                                                           'previous_reading': previous_reading})


def book_details_view(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        more_books_genre = Book.objects.filter(Genre__in=book.Genre.all()).exclude(pk=pk)
        more_books_author = Book.objects.filter(Author__in=book.Author.all()).exclude(pk=pk)
        more_books = (more_books_genre | more_books_author).distinct
        # for genre in book.Genre.all():
        #     more_books.append(Book.objects.filter(Genre=genre, Status='Available').exclude(pk=pk))
        # for author in book.Author.all():
        #     more_books.append(Book.objects.filter(Author=author, Status='Available').exclude(pk=pk))
        # random.shuffle(more_books)
    except Book.DoesNotExist:
        raise Http404('Oops Sorry! Book does not exist!!!')
    return render(request, 'Emped_booksite/book_details.html', {'book': book, 'more_books': more_books})


def genres_details_view(request, pk):
    try:
        genre = Category.objects.filter(pk=pk)
        try:
            books = Book.objects.filter(Genre=pk)
        except Book.DoesNotExist:
            raise Http404('Oops Sorry! Books does not exist for this Genre!!!')
    except Category.DoesNotExist:
        raise Http404('Oops Sorry! This Genre is temporarily not available!!!')
    return render(request, 'Emped_booksite/genre_details.html', {'books': books, 'genre': genre})


def range_details_view(request, pk):
    try:
        range = Range.objects.filter(pk=pk)
        try:
            books = Book.objects.filter(Age=pk)
        except Book.DoesNotExist:
            raise Http404('Oops Sorry! Books does not exist for this Range!!!')
    except Range.DoesNotExist:
        raise Http404('Oops Sorry! Book does not exist!!!')
    return render(request, 'Emped_booksite/range_details.html', {'books': books, 'range': range})


def author_details_view(request, pk):
    try:
        authors = Author.objects.filter(pk=pk)
        try:
            books = Book.objects.filter(Author=pk)
        except Book.DoesNotExist:
            raise Http404('Oops Sorry! Books does not exist for this Range!!!')
    except Author.DoesNotExist:
        raise Http404('Oops Sorry! Book does not exist!!!')
    return render(request, 'Emped_booksite/author_details.html', {'books': books, 'authors': authors})


def customer_authenticate(request):
    if request.is_ajax():
        phone_no = request.POST['Phoneno']
        otp = request.POST['OTP']
        if Customer.objects.filter(PhoneNo=phone_no).exists():
            if Customer.objects.filter(PhoneNo=phone_no, OTP=otp).exists():
                customer = Customer.objects.filter(PhoneNo=phone_no)
                # customer_list = serializers.serialize('json', customer)
                for cust in customer:
                    request.session['userid'] = str(cust.id)
                    request.session['userphone'] = str(cust.PhoneNo)
                    request.session['userName'] = str(cust.FirstName)
                return HttpResponse(request.session.get('userName'))
            else:
                return HttpResponse("no_match")
        else:
            request.session["new_customer_phoneno"] = request.POST['Phoneno']
            return HttpResponse("new_customer")
    return ""


def customer_logout(request):
    if request.is_ajax():
        try:
            del request.session['userid']
            del request.session['userphone']
            del request.session['userName']
        except KeyError:
            pass
        return HttpResponse('success')
    return ""


def customer_register(request):
    if request.is_ajax():
        phone_no = request.session.get('new_customer_phoneno')
        otp = request.session.get(""+request.session.get('new_customer_phoneno')+"OTP")
        f_name = request.POST['Fname']
        l_name = request.POST['Lname']
        door = request.POST['Door']
        address = request.POST['Address']
        landmark = request.POST['Landmark']
        customer = Customer(PhoneNo=phone_no, OTP=otp, FirstName=f_name, LastName=l_name)
        customer.save()
        try:
            # user = Customer.objects.filter(PhoneNo=phone_no).first()
            request.session['userid'] = str(customer.pk)
            request.session['userphone'] = str(customer.PhoneNo)
            request.session['userName'] = str(customer.FirstName)
            address = CustomerAddress(Customer_id=customer.pk, DoorNo=door, Address=address,
                                      LandMark=landmark, IsDefault=True)
            address.save()
        except Customer.DoesNotExist:
            return HttpResponse('Failed')
        return HttpResponse(request.session.get('userName'))
    return HttpResponse('Failed')


def personal_info_view(request, pk):
    try:
        customer = Customer.objects.filter(pk=pk)
    except Customer.DoesNotExist:
        raise Http404('Oops Sorry! Customer record not found!!!')
    try:
        address = CustomerAddress.objects.filter(Customer_id=request.session.get('userid'),IsDeleted=False)
    except CustomerAddress.DoesNotExist:
        raise Http404('Oops Sorry! Addresses of the customer not found!!!')
    return render(request, 'Emped_booksite/Personal_information.html', {'customer': customer, 'address': address})


def update_customer(request):
    if request.is_ajax:
        try:
            if request.POST["OTP"] == "match":
                Customer.objects.filter(pk=request.session.get('userid')).update(PhoneNo=request.POST['PhoneNo'],
                                                                                 FirstName=request.POST['FirstName'],
                                                                                 LastName=request.POST['LastName'],)
                if request.session.get('userphone') != request.POST['PhoneNo']:
                    request.session['userphone'] = request.POST['PhoneNo']
            else:
                Customer.objects.filter(pk=request.session.get('userid')).update(FirstName=request.POST['FirstName'],
                                                                                 LastName=request.POST['LastName'],)

        except Customer.DoesNotExist:
            raise Http404('Oops Sorry! Customer record not found!!!')
        return HttpResponse('success')
    return ""


def cart(request):
    try:
        cart_items = Cart.objects.filter(Customer_id=request.session.get('userid'), IsDeleted=False, IsActive=True)
        if cart_items.exists():
            available = True
        else:
            available = False
    except Cart.DoesNotExist:
        raise Http404('Oops Sorry! The cart is Empty!!!')

    try:
        saveforlater_items = Cart.objects.filter(Customer_id=request.session.get('userid'), IsDeleted=False, IsActive=False, IsSaveForLater=True)
        if saveforlater_items.exists():
            saveforlater_available = True
        else:
            saveforlater_available = False
    except Cart.DoesNotExist:
        raise Http404('Oops Sorry! There is no item saved for later!!!')

    try:
        address = CustomerAddress.objects.filter(Customer_id=request.session.get('userid'))
    except CustomerAddress.DoesNotExist:
        raise Http404('Oops Sorry! Customers Default Address not found!!!')
    return render(request, 'Emped_booksite/cart.html', {'cart': cart_items, 'available': available,
                                                        'saveforlater_items': saveforlater_items,
                                                        'saveforlater_available': saveforlater_available,
                                                        'address': address})


def remove_item(request):
    if request.is_ajax:
        try:
            Cart.objects.filter(pk=request.POST['id']).update(IsDeleted=True, IsActive=False)
        except Cart.DoesNotExist:
            raise Http404('Oops Sorry! User does not have this item in the cart!!!')
        return HttpResponse('success')
    return ""


def save_for_later_item(request):
    if request.is_ajax:
        try:
            Cart.objects.filter(pk=request.POST['id']).update(IsDeleted=False, IsActive=False, IsSaveForLater=True)
        except Cart.DoesNotExist:
            raise Http404('Oops Sorry! User does not have this item in the cart!!!')
        return HttpResponse('success')
    return ""


def move_to_cart_item(request):
    if request.is_ajax:
        try:
            Cart.objects.filter(pk=request.POST['id']).update(IsDeleted=False, IsActive=True, IsSaveForLater=False)
        except Cart.DoesNotExist:
            raise Http404('Oops Sorry! User does not have this item in the cart!!!')
        return HttpResponse('success')
    return ""


def update_default_address(request):
    if request.is_ajax:
        try:
            CustomerAddress.objects.filter(IsDefault=True).update(IsDefault=False)
            CustomerAddress.objects.filter(pk=request.POST['Address']).update(IsDefault=True)
        except CustomerAddress.DoesNotExist:
            raise Http404('Oops Sorry! Unable to update default address!!!')
        return HttpResponse('success')
    return "Failed"


def delete_address(request):
    if request.is_ajax:
        try:
            CustomerAddress.objects.filter(pk=request.POST['Address']).update(IsDeleted=True)
        except CustomerAddress.DoesNotExist:
            raise Http404('Oops Sorry! Unable to delete address!!!')
        return HttpResponse('success')
    return "Failed"


def edit_address(request):
    if request.is_ajax:
        try:
            CustomerAddress.objects.filter(pk=request.POST['value']).update(DoorNo=request.POST["doorNo"],
                                                                            Address=request.POST["address"],
                                                                            PinCode=request.POST["pinCode"],
                                                                            LandMark=request.POST["landmark"])
        except CustomerAddress.DoesNotExist:
            raise Http404('Oops Sorry! Unable to edit address!!!')
        return HttpResponse('success')
    return "Failed"


def add_address(request):
    if request.is_ajax:
        if CustomerAddress.objects.filter(Customer_id=request.session.get('userid'), DoorNo=request.POST["doorNo"],
                                          Address=request.POST["address"], PinCode=request.POST["pinCode"],
                                          LandMark=request.POST["landmark"]).exists():
            CustomerAddress.objects.filter(Customer_id=request.session.get('userid'), DoorNo=request.POST["doorNo"],
                                           Address=request.POST["address"], PinCode=request.POST["pinCode"],
                                           LandMark=request.POST["landmark"]).update(
                IsDeleted=False)
        else:
            address = CustomerAddress(Customer_id=request.session.get('userid'), DoorNo=request.POST["doorNo"],
                                      Address=request.POST["address"], PinCode=request.POST["pinCode"],
                                      LandMark=request.POST["landmark"])
            address.save()
        return HttpResponse('success')
    return "Failed"


def order(request):
    orders = []
    status = ""
    if request.is_ajax:
        if Cart.objects.filter(Customer_id=request.session.get('userid'), IsActive=True, IsDeleted=False).exists():
            items = Cart.objects.filter(Customer_id=request.session.get('userid'), IsActive=True, IsDeleted=False)
            for item in items:
                books = Book.objects.filter(pk=item.Book.id)
                for book in books:
                    if book.Status != "Available":
                        status = "Failed"
                        break
            if status != "Failed":
                for item in items:
                    rent_order = Rent(Book_id=item.Book.id, Customer_id=request.session.get('userid'),
                                      CustomerAddress_id=request.POST["value"])
                    rent_order.save()
                    orders.append(rent_order.id)
                    email_from = settings.EMAIL_HOST_USER
                    subject = 'Received Order: '+str(rent_order.pk)
                    message = 'Received Rent order Details: \n Rent order: '+str(rent_order.pk)+'\nBook: '+rent_order.Book.Name+'\nCustomer: '+rent_order.Customer.FirstName+'\nPhone no: ' +str(rent_order.Customer.PhoneNo) + '\nAddress: \n' + rent_order.CustomerAddress.DoorNo +'\n'+rent_order.CustomerAddress.Address+'\n'+rent_order.CustomerAddress.PinCode+'\n\n'+rent_order.CustomerAddress.LandMark
                    send_mail(subject, message, email_from, ['tolston7v@gmail.com'], fail_silently=False,)
                    request.session['orders'] = orders
                    cust = Customer.objects.get(pk=request.session.get('userid'))
                    status = "success"
                    books = Book.objects.filter(pk=item.Book.id).update(Status="Rented")
                    Cart.objects.filter(Customer_id=request.session.get('userid'), IsActive=True, IsDeleted=False).\
                        update(IsActive=False, IsDeleted=True)
            else:
                return HttpResponse("Oops Sorry!!! You have Books in you cart which aren't available at the moment!")
            return HttpResponse("success")
        else:
            return HttpResponse("empty")
    return ""


def order_message(request):
    orders = Rent.objects.filter(pk__in=request.session.get('orders'))
    return render(request, 'Emped_booksite/Order_Message.html', {'orders': orders})


def add_to_cart(request):
    if Cart.objects.filter(Book_id=request.POST["book"], Customer_id=request.session.get('userid'),  IsActive=True,
                           IsDeleted=False).exists():
        return HttpResponse("Book already present in the cart!!!")
    elif Cart.objects.filter(Book_id=request.POST["book"], Customer_id=request.session.get('userid'),
                             IsSaveForLater=True, IsDeleted=False).exists():
        Cart.objects.filter(Book_id=request.POST["book"], Customer_id=request.session.get('userid'),
                            IsActive=False, IsSaveForLater=True, IsDeleted=False).update(IsActive=True,
                                                                                         IsSaveForLater=False,
                                                                                         IsDeleted=False)
        return HttpResponse("success")
    else:
        cart_item = Cart(Book_id=request.POST["book"], Customer_id=request.session.get('userid'), IsActive=True,
                         IsSaveForLater=False, IsDeleted=False)
        cart_item.save()
        return HttpResponse("success")


def return_book(request):
    if request.is_ajax:
        try:
            books = Rent.objects.filter(pk=request.POST["bookValue"], Status="On Rent")
            for book in books:
                Book.objects.filter(pk=book.Book.id).update(Status="Available")
                Rent.objects.filter(pk=book.id).update(Status="Returned", ReturnedDate=date.today())
                request.session["returning_book"] = str(book.id)
        except Rent.DoesNotExist:
            return HttpResponse("Oops sorry!!! couldn't return the book")
        return HttpResponse("success")
    return ""


def return_message(request):
    returning_book = Rent.objects.filter(pk=request.session.get('returning_book'))
    return render(request, 'Emped_booksite/return_book_message.html', {'returning_book': returning_book})


def notify(request, pk):
    try:
        rent_record = Rent.objects.get(pk=pk)
        return format_html(f'')
    except Rent.DoesNotExist:
        raise Http404('Oops Sorry! Book does not exist!!!')
    pass


def add_to_wishlist(request):
    if Cart.objects.filter(Book_id=request.POST["book"], Customer_id=request.session.get('userid'),  IsWishList=True,
                           IsDeleted=False).exists():
        return HttpResponse("Book already present in the WishList!!!")
    elif Cart.objects.filter(Book_id=request.POST["book"], Customer_id=request.session.get('userid'),
                             IsWishList=False, IsDeleted=True).exists():
        Cart.objects.filter(Book_id=request.POST["book"], Customer_id=request.session.get('userid'),
                            IsWishList=False, IsDeleted=True).update(IsWishList=True, IsDeleted=False)
        return HttpResponse("success")
    else:
        cart_item = Cart(Book_id=request.POST["book"], Customer_id=request.session.get('userid'), IsWishList=True,
                         IsActive=False, IsSaveForLater=False, IsDeleted=False)
        cart_item.save()
        return HttpResponse("success")


def wish_list(request):
    try:
        books = Cart.objects.filter(Customer__id=request.session.get('userid'),IsWishList=True)
        is_null = False
    except Cart.DoesNotExist:
        is_null = True
    return render(request,'Emped_booksite/WishList.html', {'books': books, 'is_null': is_null})


def search(request):
    request.session["is_present"] = False
    request.session["category"] = request.POST["category"]
    request.session["search_text"] = request.POST["search_text"]
    if request.POST["category"] == "Authors" and Author.objects.filter(Name__contains=request.POST["search_text"]).exists():
        request.session["is_present"] = True
        request.session["match"] = "same"
        request.session["is_author_present"] = True
    elif request.POST["category"] == "Books" and Book.objects.filter(Name__contains=request.POST["search_text"]).exists():
        request.session["is_present"] = True
        request.session["match"] = "same"
        request.session["is_book_present"] = True
    elif request.POST["category"] == "Genres" and Category.objects.filter(Name__contains=request.POST["search_text"]).exists():
        request.session["is_present"] = True
        request.session["match"] = "same"
        request.session["is_genre_present"] = True
    else:
        if request.POST["category"] != "All":
            request.session["match"] = "different"
            request.session["is_author_present"] = False
            request.session["is_book_present"] = False
            request.session["is_genre_present"] = False
        else:
            request.session["match"] = "All"
        if Book.objects.filter(Name__contains=request.POST["search_text"]).exists():
            request.session["is_present"] = True
            request.session["is_book_present"] = True
        if Category.objects.filter(Name__contains=request.POST["search_text"]).exists():
            request.session["is_present"] = True
            request.session["is_genre_present"] = True
        if Author.objects.filter(Name__contains=request.POST["search_text"]).exists():
            request.session["is_present"] = True
            request.session["is_author_present"] = True
    return HttpResponse("success")


def result_page(request):
    category = ""
    match = ""
    result_book = ""
    result_author = ""
    result_genre = ""
    if request.session.get('is_present', False):
        if request.session.get('match') == "same":
            match = "same match"
            if request.session.get('category') == "Books":
                category = "Books"
                result = Book.objects.filter(Name__contains=request.session.get('search_text'))
            elif request.session.get('category') == "Authors":
                category = "Authors"
                result = Author.objects.filter(Name__contains=request.session.get('search_text'))
            else:
                category = "Genres"
                result = Category.objects.filter(Name__contains=request.session.get('search_text'))
            return render(request, "Emped_booksite/search_result.html", {'is_present': request.session.get('is_present'),
                                                                         'match': match, 'result': result,
                                                                         'category': category,
                                                                         'search_text': request.session.get('search_text')})
        elif request.session.get('match') == "different":
            match = "different match"
            if request.session.get('category') == "Books":
                category = "Books"
                result = Book.objects.filter()
            elif request.session.get('category') == "Authors":
                category = "Authors"
                result = Author.objects.filter()
            else:
                category = "Genres"
                result = Category.objects.filter()
            return render(request, "Emped_booksite/search_result.html", {'is_present': request.session.get('is_present'),
                                                                         'match': match, 'result': result,
                                                                         'category': category,
                                                                         'search_text': request.session.get('search_text')})
        else:
            match = "All"
        if request.session.get('is_book_present'):
            result_book = Book.objects.filter(Name__contains=request.session.get('search_text'))
        if request.session.get('is_author_present'):
            result_author = Author.objects.filter(Name__contains=request.session.get('search_text'))
        if request.session.get('is_genre_present'):
            result_genre = Category.objects.filter(Name__contains=request.session.get('search_text'))
        return render(request, "Emped_booksite/search_result.html", {'is_present': request.session.get('is_present'),
                                                                     'match': match, 'result_book': result_book,
                                                                     'is_book_present': request.session.get('is_book_present'),
                                                                     'is_author_present': request.session.get('is_author_present'),
                                                                     'is_genre_present': request.session.get('is_genre_present'),
                                                                     'result_author': result_author,
                                                                     'result_genre': result_genre,
                                                                     'search_text': request.session.get('search_text')})
    else:
        return render(request, "Emped_booksite/search_result.html", {'is_present': request.session.get('is_present'),
                                                                     'search_text': request.session.get('search_text')})
    pass


def send_otp(request):

    url = "https://www.fast2sms.com/dev/bulkV2"

    otpnumber = str(random.randint(1111, 9999))
    payload = "variables_values="+otpnumber+"&route=otp&numbers="+str(request.POST['Phoneno'])
    headers = {
        'authorization': "0fejv4NX8zcrW1CaKGEZ9ph3AuVMgI2UQxRbB6H5mtLFyniTOk4DYfwnsx7iu92hpLUGKeAQVmgzd0IR",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    if request.POST['type'] == 'update' and Customer.objects.filter(PhoneNo=request.POST['Phoneno']).exists():
        res = 'exists'
    else:
        response = requests.request("POST", url, data=payload, headers=headers)
        if "true" in response.text:
            res = "success"
            if Customer.objects.filter(PhoneNo=request.POST['Phoneno']).exists():
                Customer.objects.filter(PhoneNo=request.POST['Phoneno']).update(OTP=otpnumber)
            else:
                request.session[""+request.POST['Phoneno']+"OTP"] = otpnumber
        else:
            res = "failed"
    return HttpResponse(res)


def otp_verify(request):
    phone_no = request.POST['Phoneno']
    otp = request.session.get(""+phone_no+"OTP")
    print(otp)
    print(request.POST['OTP'])
    if request.POST['OTP'] == otp:
        res = "match"
    else:
        res = "no match"
    return HttpResponse(res)


