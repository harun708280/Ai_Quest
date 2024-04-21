from django.urls import path
from Shop import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . forms import LoginForm,mypasswordchange,MyPasswordResetForm,MySetPasswordForm
urlpatterns = [
    path('', views.productView.as_view(),name='home'),
    path('product-detail/<int:pk>', views.productDetialView.as_view(), name='product-detail'),
    path('add-to-card/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.Show_cart,name='cart'),
    path('pluscart/',views.plus_cart),
    path('minuscart',views.minus_cart),
    path('removecart/',views.remove_cart),

    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.customerprofileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),

    path('login/', auth_views.LoginView.as_view(template_name='Shop/login.html',authentication_form=LoginForm), name='login'),

    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='Shop/passwordchange.html',form_class=mypasswordchange,success_url='/passwordchangedone/'),name='passwordchange'),
    #('changepassword/', views.change_password, name='changepassword'),
   
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='Shop/passwordchangedone.html'),name='passwordchangedone'),
    path('lehenga/', views.lehenga, name='lehenga'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='Shop/password_reset.html', form_class=MyPasswordResetForm), name='password-reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Shop/password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='Shop/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='Shop/password_reset_complete.html'), name='password_reset_complete'),

    path('lehenga/<slug:data>', views.lehenga, name='lehengaitem'),

    #path('registration/', views.customerregistration, name='customerregistration'),
    path('registration/', views.CustomerRegistrationView.as_view(), name = 'customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('paymentdone/',views.payment_done,name='paymentdone')
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)