from django.urls import path, include
from .views2 import showProduct
from .views import home,commentPost,deleteComment,addWishlist,showWishlist,about,addCartlist,showCartlist,checkOut,getGlass,help,contact,crossProduct

urlpatterns = [


    path('', home, name='home'),
    path('<pk>/<str:title>/show', showProduct, name='show-product'),
    path('<pk>/<str:title>/display', getGlass, name='display-product'),
    path('<pk>/comment/', commentPost, name='comment-post'),
    path('<pk>/<ck>/dc/', deleteComment, name='delete-comment'),
    path('add-wishlist/', addWishlist, name='add-wishlist'),
    path('add-cart/', addCartlist, name='add-cart'),
    path('wishlist/', showWishlist, name='wishlist'),
    path('cartlist/', showCartlist, name='cartlist'),
    path('check-out/', checkOut, name='check-out'),
    path('about/', about, name='about'),
    path('help/', help, name='help'),
    path('contact/', contact, name='contact'),
    path('cross-product/<pk>/', crossProduct, name='cross-product'),






]
