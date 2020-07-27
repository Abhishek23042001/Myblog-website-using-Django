from django.urls import path, include
from .import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

urlpatterns = [
    path('',views.home,name='home'),
    path('contact',views.contact,name='contact'),
    path('about',views.about,name='about'),
    path('search',views.search,name="search"),
    path('signup',views.handlesignup,name="signup"),
    path('login',views.handlelogin, name="handlelogin"),
    path('logout',views.handlelogout,name="handlelogout"),
    path('profile',views.index,name="profile"),
    path('uploadimage',views.upload,name="uploadimage"),
    path('passchange',views.password_change,name="password_change"),
    path('mail',views.send_mails,name="mail"),
    path(r'^password_reset/$', auth_views.PasswordResetView.as_view(template_name='home/password_reset_form.html'), name='password_reset'),
    path(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='home/password_reset_done.html')),
    path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.PasswordResetConfirmView.as_view(template_name='home/password_reset_confirm.html')),
    path(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(template_name='home/password_reset_complete.html')), 
    ]