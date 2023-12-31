from django.urls import path
from app import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .forms import *


urlpatterns = [
    path('', views.ProductView.as_view(),name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='show-cart'),
    path('paymentdone/',views.payment_done,name='payment_done'),

    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),name="passwordchange"),
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html',form_class=MyPasswordChangeForm),name="passwordchangedone"),

    #password reset
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('accounts/login/', views.login_user, name='login'),
    path('logout/',views.Userlogout,name='logout'),
    path('registration/', views.register_user, name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('remove-item<int:item_id>/',views.remove_item,name='remove_item'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)











