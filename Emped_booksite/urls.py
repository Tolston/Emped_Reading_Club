from django.urls import path
from . import views


urlpatterns = [
    path(r'', views.main_func, name='index-page'),
    path(r'profile/', views.profile_page, name='profile-page'),
    path(r'book-details/<int:pk>/', views.book_details_view, name='book-detail'),
    path(r'Genres-details/<int:pk>/', views.genres_details_view, name='Genres-detail'),
    path(r'Range-details/<int:pk>/', views.range_details_view, name='Range-detail'),
    path(r'Author-details/<int:pk>/', views.author_details_view, name='Author-detail'),
    path(r'authenticate/', views.customer_authenticate, name='login'),
    path(r'logout/', views.customer_logout, name='logout'),
    path(r'personal-information/<int:pk>/', views.personal_info_view, name='personal_info'),
    path(r'update/', views.update_customer, name='update'),
    path(r'cart/', views.cart, name='cart'),
    path(r'remove/', views.remove_item, name='removeItem'),
    path(r'saveforlater/', views.save_for_later_item, name='saveForLater'),
    path(r'movetocart/', views.move_to_cart_item, name='moveToCart'),
    path(r'register/', views.customer_register, name='register'),
    path(r'update_Default_address/', views.update_default_address, name='defaultAddress'),
    path(r'delete_address/', views.delete_address, name='deleteAddress'),
    path(r'edit_address/', views.edit_address, name='edit_address'),
    path(r'add_address/', views.add_address, name='add_address'),
    path(r'order/', views.order, name='order'),
    path(r'order message/', views.order_message, name='order_message'),
    path(r'add to cart/', views.add_to_cart, name='addToCart'),
    path(r'return book/', views.return_book, name='return_book'),
    path(r'return book message/', views.return_message, name='return_message'),
    path(r'notify/<int:pk>/', views.notify, name='notify'),
    path(r'add to wishlist/', views.add_to_wishlist, name='addToWishList'),
    path(r'Wish List/', views.wish_list, name='wishList'),
    path(r'search/', views.search, name='search'),
    path(r'search result/', views.result_page, name='result'),
    path(r'send otp/', views.send_otp, name='otp'),
    path(r'verify otp/', views.otp_verify, name='otp_verify')
]
