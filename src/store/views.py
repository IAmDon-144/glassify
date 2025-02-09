from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Category, Glasses, Comment,Glasses2,Notice
from profiles.models import Customer
import cv2
import os
from sqlalchemy import null
import datetime
from .filters import PostFilter


def home(request):

    allNotice = Notice.objects.all()
    brking = ""
    for notice in allNotice:
        brking += notice.title + "------ "

    now = datetime.datetime.now()
    dayName = (now.day)

    allCategories = Category.objects.all()
    allProds = Glasses.objects.all()
    allProds2 = Glasses2.objects.all()
    myfilter = PostFilter(request.GET, allProds)
    allProds = myfilter.qs

    context = {'category': allCategories,
               'allProds': allProds,
               'allProds2':allProds2,
               'dayName:': dayName,
                'myfilter': myfilter,
                'allNotice':brking,
               }


    return render(request, 'home.html', context)



def getGlass(request,pk,title):
    obj = Glasses2.objects.get(id = pk) 
    moreProducts = Glasses2.objects.exclude(id = obj.id)[0:3]


    context = {
        "glass":obj,
        "moreProducts":moreProducts
    }

    return render(request, 'productDetails2.html',context)


def commentPost(request, pk):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('login-account')

    else:


        profile = null

        post = Glasses.objects.get(id=pk)

        profile = Customer.objects.get(user=user)

        if request.method == 'POST' and request.POST['commnet-box'] != null:
            Comment.objects.create(user=profile, post=post,
                                body=request.POST['commnet-box'])
            return redirect('show-product', pk=pk, title=post.title.replace(' ', '-'))


def deleteComment(request, pk, ck):
    profile = Customer.objects.get(user=request.user)
    post = Glasses.objects.get(id=ck)

    comment = Comment.objects.get(id=pk)
    if comment.user == profile:
        comment.delete()
        return redirect('show-product', pk=ck, title=post.title.replace(' ', '-'))

    else:
        return HttpResponse("You Are Not Authorized")


def addWishlist(request):

    
    if request.method == 'POST':

        data = {
            'lvalue': 'Like',

        }
        profileID = request.POST['profileID']
        postID = request.POST['postID']

        profile = Customer.objects.get(id = profileID)
        post = Glasses.objects.get(id = postID)

        if profile in post.liked.all():
            post.liked.remove(profile)
        else:
            post.liked.add(profile)
            data['lvalue'] = 'Unlike'

        return JsonResponse(data, safe=False)


def addCartlist(request):
    if request.method == 'POST':

        data = {
            'lvalue': 'Add to Cart',

        }
        profileID = request.POST['profileID']
        postID = request.POST['postID']

        profile = Customer.objects.get(id = profileID)
        post = Glasses.objects.get(id = postID)

        if profile in post.cart.all():
            post.cart.remove(profile)
        else:
            post.cart.add(profile)
            data['lvalue'] = 'Remove Cart'

        return JsonResponse(data, safe=False)



def crossProduct(request,pk):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('login-account')
    else:
        profile = Customer.objects.get(user=user)
        glass  = Glasses.objects.get(id = pk)
        glass.cart.remove(profile)
        return redirect('cartlist')







def showWishlist(request):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('login-account')


    else:
        
        profile = Customer.objects.get(user=user)
        wishListId = []

        allGlass = Glasses.objects.all()

        for glass in allGlass:
            if profile in glass.liked.all():
                wishListId.append(glass)


        context = {
            "profile":profile,
            "wishlists":wishListId,
        }

        return render(request, 'wishlist.html', context)





def showCartlist(request):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('login-account')


    else:
        
        profile = Customer.objects.get(user=user)
        cartistId = []

        allGlass = Glasses.objects.all()
        price = 0

        for glass in allGlass:
            if profile in glass.cart.all():
                cartistId.append(glass)
                priceAfterDiscount = (glass.price)*((100-glass.discount)/100)
                price+=priceAfterDiscount


        context = {

            "cartists":cartistId,
            "price":price
        }

        return render(request, 'calculatePrice.html', context)

def checkOut(request):
    if request.method == "POST":
        grandTotal = request.POST['totalPrice']

        context = {
            "grandTotal":grandTotal
        }

        return render(request,"checkout.html",context)


def about(request):
    return render(request,"about.html")



def help(request):
    return render(request, 'help.html',)


def contact(request):
    now = datetime.datetime.now()
    hour = (now.hour)
    print(hour,"fsfsdfc")
    status  =""
    if(hour<9 or hour>=21):
        status = "Closed"
    else:
        status = "Open"
    


    context = {
        "status":status
    }
    return render(request, 'contact.html',context)
