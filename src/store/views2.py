from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Category, Glasses, Comment
from profiles.models import Customer
import cv2
import os
from sqlalchemy import null
from .views import showWishlist


face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def put_glass(glass, fc, x, y, w, h):
    face_width = w
    face_height = h
    hat_width = face_width
    hat_height = int(.50*face_height) + 1

    # print(hat_height,hat_width)

    glass = cv2.resize(glass, (hat_width, hat_height))

    for i in range(hat_height):
        for j in range(hat_width):
            for k in range(3):
                if glass[i][j][k] < 200:
                    fc[y+i - int(-0.20 * face_height)][x +
                                                       j][k] = glass[i][j][k]
    return fc





# ==================================================================

def showProduct(request, pk, title):
    

    obj = Glasses.objects.get(id=pk)
    moreProducts = Glasses.objects.exclude(id = obj.id)[0:4]

    allCommnets = obj.comment_set.all()
    image2 = ""

    if not request.user.is_authenticated:

        specifications = obj.specification.split(',')

        context = {
            "glass": obj,
            'specifications': specifications,
            "allCommnets": allCommnets,
            'image2': 'http://127.0.0.1:8000/media/wearedGlass/'+"logoutAlert.jpg",
        }
        return render(request, "productDetails.html", context)

    else:

        cusProfile = Customer.objects.get(user=request.user)
        cusAvatar = cusProfile.avatar
        glasses = cv2.imread(f'./media/{obj.image1}')
        customerImage = cv2.imread(f'./media/{cusAvatar}')

        try:

            gray = cv2.cvtColor(customerImage, cv2.COLOR_BGR2GRAY)
            face_det = face_classifier.detectMultiScale(
                gray, scaleFactor=1.3, minNeighbors=3)

            for (x, y, w, h) in face_det:
                frame = put_glass(glasses, customerImage, x, y, w, h)

                path = 'H:\Django\Glass Store\src\media\wearedGlass'
                cv2.imwrite(os.path.join(
                    path, f"{cusProfile.id}-{cusProfile.name}-{obj.title[0:25]}.png"), frame)
                break
            image2 = 'http://127.0.0.1:8000/media/wearedGlass/' + \
                f"{cusProfile.id}-{cusProfile.name}-{obj.title[0:25]}.png"
        except:
            image2 = 'http://127.0.0.1:8000/media/wearedGlass/'+"logoutAlert.jpg"

        specifications = obj.specification.split(',')

        context = {
            "glass": obj,
            "profile": cusProfile,
            'specifications': specifications,
            "allCommnets": allCommnets,
            'image2': image2,
            "moreProducts":moreProducts

        }

        return render(request, "productDetails.html", context)

