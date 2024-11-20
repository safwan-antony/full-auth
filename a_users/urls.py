from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/',loginPage,name='account_login'),
    path('logout/',logoutPage,name='account_logout'),
    path('signup/',signupPage,name='account_signup'),
    path('profile/<str:pk>/',profilePage,name='account_profile'),
    path('edit-profile/<str:pk>/',editProfile,name='account_edit_profile'),
    path('profile-settings/',profileSettings,name='account_profile_settings'),
    path('email-change/',profile_emailchange,name='account_email_change'),
    path('delete-profile/<str:pk>/',deleteProfile,name='account_delete_profile'),
   # path('change-password/',changePassword,name='account_change_password'),
   #path('change_password/', ChangePasswordView.as_view(), name='change_password'),
   path('password-change/',Change_Password,name='change_password'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),
     #path('activate/<uidb64>/<token>', activate, name='account_confirmation_email'),
     


]